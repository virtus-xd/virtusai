"""
Speech Recognition - Konuşmayı metne çevirir
"""
import speech_recognition as sr
import logging
from config.settings import LANGUAGE, LISTENING_TIMEOUT, PHRASE_TIMEOUT

logger = logging.getLogger(__name__)


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        try:
            self.microphone = sr.Microphone()
        except Exception as e:
            logger.error(f"Mikrofon başlatılamadı: {e}")
            logger.error("PyAudio kurulu değil. Test modu için: python main.py --test")
            raise
        
        # Hassasiyet ayarları
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
    
    def listen_command(self):
        """Kullanıcıdan komut dinle"""
        try:
            logger.info("🎧 Dinliyorum...")
            
            with self.microphone as source:
                # Ortam gürültüsüne göre ayarla
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Ses al
                audio = self.recognizer.listen(
                    source,
                    timeout=LISTENING_TIMEOUT,
                    phrase_time_limit=PHRASE_TIMEOUT
                )
            
            logger.info("🔄 Ses işleniyor...")
            
            # Google Speech Recognition kullan
            text = self.recognizer.recognize_google(audio, language=LANGUAGE)
            
            logger.info(f"📝 Algılanan: {text}")
            return text
            
        except sr.WaitTimeoutError:
            logger.warning("⏱️ Zaman aşımı - komut alınamadı")
            return None
            
        except sr.UnknownValueError:
            logger.warning("❌ Ses anlaşılamadı")
            return None
            
        except sr.RequestError as e:
            logger.error(f"❌ Speech recognition servisi hatası: {e}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Beklenmeyen hata: {e}")
            return None
    
    def calibrate(self):
        """Mikrofonu ortam gürültüsüne göre kalibre et"""
        try:
            with self.microphone as source:
                logger.info("🎙️ Mikrofon kalibre ediliyor... Lütfen sessiz kalın.")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                logger.info("✅ Kalibrasyon tamamlandı")
                return True
        except Exception as e:
            logger.error(f"Kalibrasyon hatası: {e}")
            return False
