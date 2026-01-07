"""
Virtus Kurulum ve Yapılandırma
"""
import os
import sys


def create_env_file():
    """İlk .env dosyasını oluştur"""
    if not os.path.exists('.env'):
        print("\n📝 .env dosyası oluşturuluyor...")
        
        print("\n" + "="*50)
        print("GOOGLE GEMINI API KEY")
        print("="*50)
        print("1. https://makersuite.google.com/app/apikey adresine gidin")
        print("2. API key oluşturun")
        print("3. Aşağıya yapıştırın\n")
        
        api_key = input("Google API Key: ").strip()
        
        with open('.env', 'w') as f:
            f.write(f"GOOGLE_API_KEY={api_key}\n")
            f.write("PORCUPINE_ACCESS_KEY=\n")
            f.write("WAKE_WORD=virtus\n")
            f.write("LANGUAGE=tr-TR\n")
            f.write("VOICE_RATE=150\n")
        
        print("✅ .env dosyası oluşturuldu!\n")
    else:
        print("✅ .env dosyası zaten var\n")


def check_dependencies():
    """Bağımlılıkları kontrol et"""
    print("\n🔍 Bağımlılıklar kontrol ediliyor...")
    
    required = [
        'dotenv',
        'speech_recognition',
        'pyttsx3',
        'google.generativeai',
        'pyaudio'
    ]
    
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('.', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Eksik paketler bulundu!")
        print("Yüklemek için: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ Tüm bağımlılıklar yüklü!")
        return True


def create_data_folder():
    """Data klasörünü oluştur"""
    os.makedirs('data', exist_ok=True)
    print("✅ Data klasörü hazır")


def test_microphone():
    """Mikrofon testi"""
    print("\n🎤 Mikrofon testi yapılıyor...")
    
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        
        # Mikrofonları listele
        print("\nMevcut mikrofonlar:")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"  [{index}] {name}")
        
        # Test
        with sr.Microphone() as source:
            print("\n🔊 Mikrofon çalışıyor!")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Mikrofon testi başarılı")
            return True
            
    except Exception as e:
        print(f"❌ Mikrofon hatası: {e}")
        return False


def test_tts():
    """Text-to-Speech testi"""
    print("\n🔊 TTS testi yapılıyor...")
    
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        print("✅ TTS motoru hazır")
        
        # Sesleri listele
        voices = engine.getProperty('voices')
        print(f"\nMevcut sesler: {len(voices)}")
        for i, voice in enumerate(voices[:3]):  # İlk 3 tane göster
            print(f"  [{i}] {voice.name}")
        
        response = input("\nTest sesi duymak ister misiniz? (e/h): ")
        if response.lower() == 'e':
            engine.say("Merhaba! Ben Virtus. Size nasıl yardımcı olabilirim?")
            engine.runAndWait()
            print("✅ TTS testi tamamlandı")
        
        return True
        
    except Exception as e:
        print(f"❌ TTS hatası: {e}")
        return False


def main():
    """Ana kurulum fonksiyonu"""
    print("""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║     VIRTUS AI ASISTAN - KURULUM           ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    """)
    
    # 1. Data klasörü
    create_data_folder()
    
    # 2. .env dosyası
    create_env_file()
    
    # 3. Bağımlılıklar
    if not check_dependencies():
        print("\n⚠️  Önce bağımlılıkları yükleyin!")
        return
    
    # 4. Mikrofon testi
    if not test_microphone():
        print("\n⚠️  Mikrofon sorunu var!")
    
    # 5. TTS testi
    if not test_tts():
        print("\n⚠️  TTS sorunu var!")
    
    print("\n" + "="*50)
    print("✨ KURULUM TAMAMLANDI!")
    print("="*50)
    print("\nVirtus'u başlatmak için:")
    print("  python main.py              # Normal mod")
    print("  python main.py --test       # Test modu")
    print("\n")


if __name__ == "__main__":
    main()
