"""
VIRTUS - Basit Test Modu (PyAudio Olmadan)
Klavyeden komut yazın
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.ai_brain import AIBrain
from core.action_executor import ActionExecutor
from modules.text_to_speech import TextToSpeech
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    print("""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║         VIRTUS AI ASISTAN - DEMO          ║
    ║         Powered by Google Gemini          ║
    ║                                           ║
    ║       Klavyeden komut yazın!              ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    """)
    
    try:
        print("🔧 Başlatılıyor...\n")
        
        ai = AIBrain()
        print("✅ AI Brain")
        
        executor = ActionExecutor()
        print("✅ Action Executor")
        
        try:
            tts = TextToSpeech()
            print("✅ Text-to-Speech")
            tts.speak("Merhaba! Ben Virtus.")
        except:
            print("⚠️  TTS başlatılamadı (ses çıkmayacak)")
            tts = None
        
        print("\n" + "="*50)
        print("💬 KOMUT GİRİN ('q' = çıkış)")
        print("="*50)
        
        while True:
            cmd = input("\n> ").strip()
            
            if not cmd:
                continue
            
            if cmd.lower() in ['q', 'quit', 'exit', 'çıkış']:
                print("\n👋 Görüşürüz!")
                if tts:
                    tts.speak("Görüşürüz!")
                break
            
            # AI ile işle
            result = ai.process_command(cmd)
            
            # Yanıt
            response = result.get('response', '')
            print(f"\n🤖 Virtus: {response}")
            
            if tts:
                tts.speak(response)
            
            # Aksiyon
            executor.execute(result)
    
    except KeyboardInterrupt:
        print("\n\n👋 Görüşürüz!")
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
