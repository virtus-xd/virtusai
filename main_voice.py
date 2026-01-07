"""
VIRTUS AI Asistan - Sesli Mod (Wake Word Olmadan)
Her seferinde Enter'a basıp konuşun
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.ai_brain import AIBrain
from core.action_executor import ActionExecutor
from modules.speech_recognition_module import SpeechRecognizer
from modules.text_to_speech import TextToSpeech
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Ana fonksiyon - Wake word olmadan sesli komut"""
    print("""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║        VIRTUS AI ASISTAN - SESLİ MOD      ║
    ║         Powered by Google Gemini          ║
    ║                                           ║
    ║   Enter'a basıp konuşun! (PyAudio yok)   ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    """)
    
    try:
        # Modülleri başlat
        print("🔧 Başlatılıyor...\n")
        
        ai = AIBrain()
        print("✅ AI Brain (Gemini)")
        
        executor = ActionExecutor()
        print("✅ Action Executor")
        
        speech = SpeechRecognizer()
        print("✅ Speech Recognizer")
        speech.calibrate()
        
        tts = TextToSpeech()
        print("✅ Text-to-Speech\n")
        
        tts.speak("Merhaba! Ben Virtus. Size nasıl yardımcı olabilirim?")
        
        print("=" * 50)
        print("🎤 ENTER'A BASIN VE KONUŞUN")
        print("Çıkmak için 'q' yazın")
        print("=" * 50 + "\n")
        
        while True:
            # Enter bekle
            cmd = input("\n[Enter'a basın ve konuşun, 'q' = çıkış]: ")
            
            if cmd.lower() == 'q':
                print("\n👋 Görüşürüz!")
                tts.speak("Görüşürüz!")
                break
            
            # Sesli komut al
            print("\n🎤 DİNLİYORUM...")
            command = speech.listen_command()
            
            if command:
                print(f"📝 Algılanan: {command}\n")
                
                # AI ile işle
                result = ai.process_command(command)
                
                # Yanıtı göster ve söyle
                response = result.get('response', '')
                print(f"🤖 Virtus: {response}\n")
                tts.speak(response)
                
                # Aksiyonu çalıştır
                executor.execute(result)
            else:
                print("❌ Komut algılanamadı, tekrar deneyin\n")
                
    except KeyboardInterrupt:
        print("\n\n👋 Görüşürüz!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Hata: {e}")


if __name__ == "__main__":
    main()
