"""
VIRTUS - Ana Asistan Sistemi
"""
import logging
import time
from modules.wake_word_detector import SimpleWakeWordDetector
from modules.speech_recognition_module import SpeechRecognizer
from modules.text_to_speech import TextToSpeech
from core.ai_brain import AIBrain
from core.action_executor import ActionExecutor
from config.settings import ASSISTANT_NAME

# Logging ayarla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Virtus:
    """VIRTUS AI Asistan Ana Sınıfı"""
    
    def __init__(self):
        self.name = ASSISTANT_NAME
        self.is_running = False
        self.is_listening = False
        
        # Modülleri başlat
        logger.info("=" * 50)
        logger.info(f"🚀 {self.name} başlatılıyor...")
        logger.info("=" * 50)
        
        try:
            self.wake_detector = SimpleWakeWordDetector()
            logger.info("✅ Wake Word Detector hazır")
        except Exception as e:
            logger.error(f"❌ Wake Word Detector başlatılamadı: {e}")
            self.wake_detector = None
        
        try:
            self.speech_recognizer = SpeechRecognizer()
            self.speech_recognizer.calibrate()
            logger.info("✅ Speech Recognizer hazır")
        except Exception as e:
            logger.error(f"❌ Speech Recognizer başlatılamadı: {e}")
            self.speech_recognizer = None
        
        try:
            self.tts = TextToSpeech()
            logger.info("✅ Text-to-Speech hazır")
        except Exception as e:
            logger.error(f"❌ TTS başlatılamadı: {e}")
            self.tts = None
        
        try:
            self.ai_brain = AIBrain()
            logger.info("✅ AI Brain (Gemini) hazır")
        except Exception as e:
            logger.error(f"❌ AI Brain başlatılamadı: {e}")
            self.ai_brain = None
        
        try:
            self.action_executor = ActionExecutor()
            logger.info("✅ Action Executor hazır")
        except Exception as e:
            logger.error(f"❌ Action Executor başlatılamadı: {e}")
            self.action_executor = None
        
        logger.info("=" * 50)
        logger.info(f"✨ {self.name} hazır! Wake word: '{self.name}'")
        logger.info("=" * 50)
    
    def start(self):
        """Asistanı başlat"""
        self.is_running = True
        self.speak(f"Merhaba! Ben {self.name}. Size nasıl yardımcı olabilirim?")
        
        try:
            while self.is_running:
                # Wake word'ü dinle
                if self.wake_detector.listen():
                    self.handle_wake_word()
                    
        except KeyboardInterrupt:
            logger.info("\n⚠️ Kullanıcı tarafından durduruldu")
            self.stop()
        except Exception as e:
            logger.error(f"❌ Kritik hata: {e}")
            self.stop()
    
    def handle_wake_word(self):
        """Wake word tespit edildiğinde çağrılır"""
        logger.info(f"🎤 {self.name} aktif!")
        self.speak("Evet, dinliyorum.")
        
        # Komutu dinle
        command = self.speech_recognizer.listen_command()
        
        if command:
            self.process_command(command)
        else:
            self.speak("Sizi anlayamadım. Tekrar eder misiniz?")
    
    def process_command(self, command):
        """Komutu işle ve çalıştır"""
        try:
            logger.info(f"💬 Komut: {command}")
            
            # AI ile işle
            intent_data = self.ai_brain.process_command(command)
            
            # Yanıtı söyle
            response = intent_data.get('response', '')
            if response:
                self.speak(response)
            
            # Aksiyonu çalıştır
            success = self.action_executor.execute(intent_data)
            
            if not success:
                self.speak("Komutu çalıştıramadım, üzgünüm.")
            
        except Exception as e:
            logger.error(f"Komut işleme hatası: {e}")
            self.speak("Bir hata oluştu, lütfen tekrar deneyin.")
    
    def speak(self, text):
        """Konuş"""
        if self.tts:
            self.tts.speak(text)
        else:
            logger.warning(f"TTS yok: {text}")
    
    def stop(self):
        """Asistanı durdur"""
        self.is_running = False
        logger.info(f"👋 {self.name} kapatılıyor...")
        self.speak(f"Görüşürüz!")
        
        # Cleanup
        if hasattr(self.wake_detector, 'cleanup'):
            self.wake_detector.cleanup()
        
        logger.info("✅ Kapatıldı")
    
    def manual_command(self, command_text):
        """Manuel komut (test için)"""
        logger.info(f"🔧 Manuel komut: {command_text}")
        self.process_command(command_text)


def main():
    """Ana fonksiyon"""
    try:
        virtus = Virtus()
        virtus.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}")


if __name__ == "__main__":
    main()
