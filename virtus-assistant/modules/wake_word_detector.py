"""
Wake Word Detection - "Virtus" kelimesini dinler
Porcupine wake word engine kullanır
"""
import struct
import logging
from config.settings import PORCUPINE_ACCESS_KEY, WAKE_WORD

logger = logging.getLogger(__name__)

# PyAudio ve Porcupine opsiyonel
try:
    import pyaudio
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False
    logger.warning("PyAudio veya Porcupine bulunamadı - SimpleWakeWordDetector kullanılacak")


class WakeWordDetector:
    def __init__(self):
        self.porcupine = None
        self.audio_stream = None
        self.pa = None
        
    def initialize(self):
        """Wake word detector'ı başlat"""
        if not PORCUPINE_AVAILABLE:
            logger.error("Porcupine kütüphaneleri yüklü değil")
            return False
            
        try:
            # Porcupine'i başlat (built-in wake words veya custom)
            # Not: Custom wake word için Picovoice Console'dan .ppn dosyası gerekir
            self.porcupine = pvporcupine.create(
                access_key=PORCUPINE_ACCESS_KEY,
                keywords=['jarvis']  # Yakın alternatif, sonra custom yapacağız
            )
            
            self.pa = pyaudio.PyAudio()
            
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            logger.info("Wake word detector başlatıldı")
            return True
            
        except Exception as e:
            logger.error(f"Wake word detector başlatılamadı: {e}")
            return False
    
    def listen(self):
        """Wake word'ü dinle, tespit edildiğinde True döndür"""
        try:
            pcm = self.audio_stream.read(self.porcupine.frame_length)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            
            keyword_index = self.porcupine.process(pcm)
            
            if keyword_index >= 0:
                logger.info(f"🎤 Wake word tespit edildi!")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Wake word listening error: {e}")
            return False
    
    def cleanup(self):
        """Kaynakları temizle"""
        if self.audio_stream:
            self.audio_stream.close()
        if self.pa:
            self.pa.terminate()
        if self.porcupine:
            self.porcupine.delete()
        logger.info("Wake word detector kapatıldı")


# Alternatif: Basit bir keyword spotter (API key gerektirmez)
class SimpleWakeWordDetector:
    """Basit wake word detection (speech recognition ile)"""
    def __init__(self):
        import speech_recognition as sr
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def listen(self):
        """Sürekli dinle ve 'virtus' kelimesini ara"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=2)
                
            text = self.recognizer.recognize_google(audio, language='tr-TR').lower()
            
            if 'virtus' in text or 'virtüs' in text:
                logger.info(f"🎤 Wake word tespit edildi: {text}")
                return True
                
        except Exception as e:
            # Timeout ve diğer hatalar normal, sessizce devam et
            pass
            
        return False
