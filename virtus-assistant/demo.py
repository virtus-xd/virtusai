"""
VIRTUS Demo - Komut testleri
"""
import sys
sys.path.insert(0, '.')

from core.ai_brain import AIBrain
from core.action_executor import ActionExecutor
from modules.text_to_speech import TextToSpeech
import time


def demo():
    """Demo komutları çalıştır"""
    
    print("""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║         VIRTUS AI ASISTAN - DEMO          ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    
    Bu demo, Virtus'un yeteneklerini gösterir.
    """)
    
    # Modülleri başlat
    print("\n🔧 Modüller başlatılıyor...\n")
    
    try:
        ai = AIBrain()
        print("✅ AI Brain (Gemini)")
    except Exception as e:
        print(f"❌ AI Brain başlatılamadı: {e}")
        return
    
    try:
        executor = ActionExecutor()
        print("✅ Action Executor")
    except Exception as e:
        print(f"❌ Action Executor başlatılamadı: {e}")
        return
    
    try:
        tts = TextToSpeech()
        print("✅ Text-to-Speech")
    except Exception as e:
        print(f"❌ TTS başlatılamadı: {e}")
        tts = None
    
    # Demo komutları
    demo_commands = [
        "Chrome'u aç",
        "Hesap makinesini aç",
        "5 çarpı 7 kaç eder?",
        "Ankara'nın nüfusu kaç?",
        "YouTube'da Python tutorial ara",
        "Ses seviyesini 50 yap",
    ]
    
    print("\n" + "="*50)
    print("🎬 DEMO BAŞLIYOR")
    print("="*50 + "\n")
    
    for i, command in enumerate(demo_commands, 1):
        print(f"\n[{i}/{len(demo_commands)}] 💬 Komut: {command}")
        print("-" * 50)
        
        try:
            # AI ile işle
            result = ai.process_command(command)
            
            # Sonucu göster
            print(f"🧠 Intent: {result.get('intent')}")
            print(f"⚡ Action: {result.get('action')}")
            print(f"📦 Params: {result.get('parameters')}")
            print(f"💬 Response: {result.get('response')}")
            
            # TTS varsa konuş
            if tts:
                tts.speak(result.get('response', ''))
            
            # Aksiyonu çalıştır (tehlikeli olmayanlar)
            if result.get('intent') in ['calculation', 'information', 'search']:
                executor.execute(result)
            else:
                print("⚠️  Güvenlik nedeniyle aksiyon atlandı (demo mode)")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    print("\n" + "="*50)
    print("✨ DEMO TAMAMLANDI")
    print("="*50)
    print("\nGerçek kullanım için: python main.py")
    print("Test modu için: python main.py --test\n")


def interactive_demo():
    """İnteraktif demo"""
    
    print("""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║      VIRTUS - İNTERAKTİF DEMO             ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    
    Komutlarınızı yazın, Virtus nasıl yanıt vereceğini göreceksiniz.
    Çıkmak için 'exit' yazın.
    """)
    
    try:
        ai = AIBrain()
        executor = ActionExecutor()
        tts = TextToSpeech()
        
        print("✅ Virtus hazır!\n")
        
        while True:
            print("-" * 50)
            command = input("💬 Siz: ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['exit', 'quit', 'çıkış', 'kapat']:
                print("\n👋 Görüşürüz!")
                break
            
            try:
                # İşle
                result = ai.process_command(command)
                
                # Yanıtı göster ve söyle
                response = result.get('response', '')
                print(f"🤖 Virtus: {response}\n")
                
                # Detayları göster
                print(f"   📊 Intent: {result.get('intent')}")
                print(f"   📊 Action: {result.get('action')}")
                print(f"   📊 Params: {result.get('parameters')}\n")
                
                tts.speak(response)
                
                # Güvenli aksiyonları çalıştır
                safe_intents = ['open_app', 'search', 'calculation', 'information']
                if result.get('intent') in safe_intents:
                    confirm = input("   ⚠️  Bu aksiyonu çalıştırmak ister misiniz? (e/h): ")
                    if confirm.lower() == 'e':
                        success = executor.execute(result)
                        if success:
                            print("   ✅ Aksiyon tamamlandı!\n")
                        else:
                            print("   ❌ Aksiyon başarısız!\n")
                
            except Exception as e:
                print(f"❌ Hata: {e}\n")
                
    except Exception as e:
        print(f"❌ Başlatma hatası: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_demo()
    else:
        demo()
