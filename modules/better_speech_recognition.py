"""
İyileştirilmiş Speech Recognition - PyAudio olmadan
sounddevice veya web API kullanır
"""
import logging
import speech_recognition as sr

logger = logging.getLogger(__name__)


class BetterSpeechRecognizer:
    """PyAudio gerektirmeyen ses tanıma"""
    
    def __init__(self, language='tr-TR'):
        self.language = language
        self.recognizer = sr.Recognizer()
        
        # Hassasiyet
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # Mikrofon testi
        self.microphone_available = self._test_microphone()
    
    def _test_microphone(self):
        """Mikrofon çalışıyor mu?"""
        try:
            # PyAudio olmadan mikrofon listesi
            mic_list = sr.Microphone.list_microphone_names()
            
            if not mic_list:
                logger.warning("❌ Mikrofon bulunamadı")
                return False
            
            logger.info(f"🎤 {len(mic_list)} mikrofon bulundu")
            logger.info(f"   Varsayılan: {mic_list[0] if mic_list else 'Yok'}")
            
            # Test et
            with sr.Microphone() as source:
                pass
            
            return True
            
        except Exception as e:
            logger.error(f"Mikrofon testi başarısız: {e}")
            logger.error("PyAudio kurmak için: pip install pipwin && python -m pipwin install pyaudio")
            logger.error("VEYA Python 3.11 kullanın")
            return False
    
    def listen_command(self, timeout=5, phrase_limit=10):
        """
        Sesli komut dinle
        
        Args:
            timeout: Sessizlik timeout (saniye)
            phrase_limit: Maksimum konuşma süresi
            
        Returns:
            str: Algılanan metin veya None
        """
        if not self.microphone_available:
            logger.error("Mikrofon kullanılamıyor!")
            return None
        
        try:
            logger.info("🎤 DİNLİYORUM...")
            
            with sr.Microphone() as source:
                # Gürültü ayarı
                logger.info("   Ortam gürültüsü ölçülüyor...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Dinle
                logger.info("   🔴 Konuşun!")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )
            
            logger.info("🔄 Ses işleniyor...")
            
            # Google Speech API
            text = self.recognizer.recognize_google(audio, language=self.language)
            
            logger.info(f"✅ Algılanan: {text}")
            return text
            
        except sr.WaitTimeoutError:
            logger.warning("⏱️ Zaman aşımı - ses algılanamadı")
            return None
        
        except sr.UnknownValueError:
            logger.warning("❓ Ses anlaşılamadı")
            return None
        
        except sr.RequestError as e:
            logger.error(f"❌ Google Speech API hatası: {e}")
            return None
        
        except OSError as e:
            logger.error(f"❌ Mikrofon hatası: {e}")
            logger.error("   PyAudio kurulu değil! pip install pipwin && python -m pipwin install pyaudio")
            return None
        
        except Exception as e:
            logger.error(f"❌ Beklenmeyen hata: {e}")
            return None
    
    def calibrate(self):
        """Mikrofon kalibrasyonu"""
        if not self.microphone_available:
            return False
        
        try:
            logger.info("🎙️ Mikrofon kalibre ediliyor...")
            logger.info("   Lütfen 2 saniye sessiz kalın...")
            
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            
            logger.info(f"✅ Kalibrasyon tamamlandı")
            logger.info(f"   Enerji eşiği: {self.recognizer.energy_threshold}")
            return True
            
        except Exception as e:
            logger.error(f"Kalibrasyon hatası: {e}")
            return False
    
    def is_available(self):
        """Mikrofon kullanılabilir mi?"""
        return self.microphone_available


# Basit kullanım testi
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    recognizer = BetterSpeechRecognizer()
    
    if recognizer.is_available():
        print("\n🎤 Mikrofon hazır!")
        print("3 saniye içinde konuşun...\n")
        
        recognizer.calibrate()
        
        input("Enter'a basıp konuşun: ")
        result = recognizer.listen_command()
        
        if result:
            print(f"\n✅ Sonuç: {result}")
        else:
            print("\n❌ Ses algılanamadı")
    else:
        print("\n❌ Mikrofon kullanılamıyor")
        print("PyAudio kurmak için:")
        print("  pip install pipwin")
        print("  python -m pipwin install pyaudio")
