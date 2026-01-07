"""
Gelişmiş Speech Recognition Sistemi
- Otomatik mikrofon kalibrasyonu
- Gürültü filtreleme
- Çoklu backend desteği (Google, Whisper)
- Wake word detection entegrasyonu

Python 3.11 uyumlu
"""
import logging
import speech_recognition as sr
import time

try:
    from config.settings import (
        LANGUAGE, LISTENING_TIMEOUT, PHRASE_TIMEOUT,
        ENERGY_THRESHOLD, DYNAMIC_ENERGY, PAUSE_THRESHOLD
    )
except ImportError:
    # Fallback değerler
    LANGUAGE = 'tr-TR'
    LISTENING_TIMEOUT = 5
    PHRASE_TIMEOUT = 10
    ENERGY_THRESHOLD = 3000
    DYNAMIC_ENERGY = True
    PAUSE_THRESHOLD = 0.8

logger = logging.getLogger(__name__)


class AdvancedSpeechRecognition:
    """Profesyonel seviye ses tanıma"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_calibrated = False
        
        # Hassasiyet ayarları
        self.recognizer.energy_threshold = ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = DYNAMIC_ENERGY
        self.recognizer.pause_threshold = PAUSE_THRESHOLD
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5
        
        # Mikrofonu başlat
        self._initialize_microphone()
    
    def _initialize_microphone(self):
        """Mikrofonu başlat ve test et"""
        try:
            # Mevcut mikrofonları listele
            mic_list = sr.Microphone.list_microphone_names()
            
            if not mic_list:
                logger.error("❌ Hiç mikrofon bulunamadı!")
                raise RuntimeError("Mikrofon bulunamadı")
            
            logger.info(f"🎤 {len(mic_list)} mikrofon bulundu:")
            for i, name in enumerate(mic_list[:5]):  # İlk 5'ini göster
                logger.info(f"   [{i}] {name}")
            
            # Varsayılan mikrofonu kullan
            self.microphone = sr.Microphone()
            logger.info("✅ Mikrofon hazır")
            
            # Otomatik kalibrasyon yap
            self.calibrate()
            
        except OSError as e:
            logger.error(f"❌ Mikrofon başlatma hatası: {e}")
            logger.error("PyAudio kurulu değil olabilir!")
            logger.error("Çözüm: pip install pipwin && python -m pipwin install pyaudio")
            raise
        except Exception as e:
            logger.error(f"❌ Beklenmeyen mikrofon hatası: {e}")
            raise
    
    def calibrate(self, duration=2):
        """
        Mikrofonu ortam gürültüsüne göre kalibre et
        
        Args:
            duration: Kalibrasyon süresi (saniye)
        """
        if not self.microphone:
            logger.error("Mikrofon yok!")
            return False
        
        try:
            logger.info(f"🎙️ Mikrofon kalibre ediliyor... ({duration}s sessiz kalın)")
            
            with self.microphone as source:
                # Ortam gürültüsünü ölç
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
                
                # Ayarları logla
                logger.info(f"✅ Kalibrasyon tamamlandı")
                logger.info(f"   Enerji eşiği: {self.recognizer.energy_threshold:.0f}")
                logger.info(f"   Dinamik ayar: {self.recognizer.dynamic_energy_threshold}")
                
            self.is_calibrated = True
            return True
            
        except Exception as e:
            logger.error(f"Kalibrasyon hatası: {e}")
            return False
    
    def listen_command(self, timeout=None, phrase_limit=None):
        """
        Kullanıcıdan sesli komut al
        
        Args:
            timeout: Maksimum bekleme süresi
            phrase_limit: Maksimum konuşma süresi
            
        Returns:
            str: Algılanan metin veya None
        """
        if not self.microphone:
            logger.error("Mikrofon kullanılamıyor!")
            return None
        
        # Varsayılan değerler
        timeout = timeout or LISTENING_TIMEOUT
        phrase_limit = phrase_limit or PHRASE_TIMEOUT
        
        try:
            logger.info("🎧 DİNLİYORUM...")
            
            with self.microphone as source:
                # Kısa kalibrasyon (gürültü değişmişse)
                if not self.is_calibrated:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Kullanıcının konuşmasını bekle
                logger.info("   🔴 Konuşabilirsiniz...")
                
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )
            
            # Sesi metne çevir
            logger.info("🔄 İşleniyor...")
            text = self._recognize_audio(audio)
            
            if text:
                logger.info(f"✅ Algılanan: '{text}'")
                return text
            else:
                logger.warning("❓ Ses anlaşılamadı")
                return None
            
        except sr.WaitTimeoutError:
            logger.warning("⏱️ Zaman aşımı - ses algılanamadı")
            return None
            
        except Exception as e:
            logger.error(f"❌ Dinleme hatası: {e}")
            return None
    
    def _recognize_audio(self, audio):
        """Ses dosyasını metne çevir - çoklu backend desteği"""
        
        # Öncelik 1: Google Speech Recognition (ücretsiz ve iyi)
        try:
            text = self.recognizer.recognize_google(audio, language=LANGUAGE)
            return text.strip()
        except sr.UnknownValueError:
            logger.debug("Google: Ses anlaşılamadı")
        except sr.RequestError as e:
            logger.warning(f"Google API hatası: {e}")
        
        # Öncelik 2: Whisper (offline ama yavaş)
        try:
            text = self.recognizer.recognize_whisper(audio, language='turkish')
            return text.strip()
        except:
            pass
        
        return None
    
    def listen_for_wake_word(self, wake_word='virtus', timeout=3):
        """
        Wake word'ü dinle (geliştirilmiş versiyon)
        
        Args:
            wake_word: Aranacak kelime
            timeout: Zaman aşımı (daha uzun süre dinle)
            
        Returns:
            bool: Wake word tespit edildiyse True
        """
        try:
            with self.microphone as source:
                # Arka plan gürültüsünü filtrele
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                
                # Daha uzun dinle (wake word için)
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=3
                )
                
            # Hızlı tanıma
            try:
                text = self.recognizer.recognize_google(audio, language=LANGUAGE).lower()
                logger.debug(f"Duyulan: '{text}'")
            except sr.UnknownValueError:
                return False
            except sr.RequestError:
                # API hatası varsa tekrar dene
                return False
            
            # Wake word kontrolü - çok geniş varyantlar
            wake_word_variants = [
                wake_word.lower(),
                wake_word.lower().replace('ı', 'i'),
                wake_word.lower().replace('u', 'ü'),
                'virtus',
                'virtüs',
                'wirtus',
                'virtüüs',
                'wirtüs',
                'birtuş',  # Türkçe aksan
                'virtüüs',
                'virtus.',  # Noktalama ile
            ]
            
            # Fuzzy matching - kısmen benzer kelimeler
            for variant in wake_word_variants:
                if variant in text:
                    logger.info(f"🎤 Wake word tespit edildi: '{text}'")
                    return True
            
            # Kelime kelime kontrol (wake word 2 kelime de olabilir)
            words = text.split()
            for word in words:
                for variant in wake_word_variants:
                    if word == variant or variant in word:
                        logger.info(f"🎤 Wake word tespit edildi: '{text}'")
                        return True
            
            return False
            
        except sr.WaitTimeoutError:
            # Timeout normal, sessizce devam et
            return False
        except Exception as e:
            logger.debug(f"Wake word dinleme hatası: {e}")
            return False
    
    def continuous_listen(self, callback, wake_word='virtus'):
        """
        Sürekli dinleme modu - wake word bekle
        
        Args:
            callback: Wake word tespit edildiğinde çağrılacak fonksiyon
            wake_word: Beklenecek wake word
        """
        logger.info(f"🔄 Sürekli dinleme başladı - '{wake_word}' bekliyor...")
        
        try:
            while True:
                if self.listen_for_wake_word(wake_word):
                    # Wake word bulundu, callback çağır
                    callback()
                    
                # Kısa bekleme (CPU yükünü azalt)
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logger.info("⚠️ Dinleme durduruldu")
    
    def test_microphone(self):
        """Mikrofon testi yap"""
        print("\n" + "=" * 50)
        print("🎤 MİKROFON TESTİ")
        print("=" * 50)
        
        if not self.microphone:
            print("❌ Mikrofon başlatılamadı!")
            return False
        
        print("\n1️⃣ Kalibrasyon...")
        self.calibrate(duration=2)
        
        print("\n2️⃣ Ses Testi")
        print("5 saniye içinde bir şeyler söyleyin:\n")
        
        result = self.listen_command(timeout=5, phrase_limit=10)
        
        if result:
            print(f"\n✅ Başarılı! Algılanan: '{result}'")
            return True
        else:
            print("\n❌ Ses algılanamadı!")
            print("\nOlası nedenler:")
            print("- Mikrofon bağlı değil")
            print("- Mikrofon izni verilmemiş")
            print("- PyAudio kurulu değil")
            print("- Çok sessiz konuşuyorsunuz")
            return False
    
    def is_available(self):
        """Mikrofon kullanılabilir mi?"""
        return self.microphone is not None


# Test kodu
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("""
    ╔═══════════════════════════════════════════╗
    ║      VIRTUS SPEECH RECOGNITION TEST       ║
    ╚═══════════════════════════════════════════╝
    """)
    
    try:
        speech = AdvancedSpeechRecognition()
        speech.test_microphone()
        
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        print("\nPyAudio kurulumu için:")
        print("  pip install pipwin")
        print("  python -m pipwin install pyaudio")
        import traceback
        traceback.print_exc()