"""
VIRTUS - Gelişmiş Kurulum ve Test Scripti
Tüm bileşenleri kontrol eder ve yapılandırır
"""
import os
import sys
import subprocess
import platform


def print_header(text):
    """Başlık yazdır"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def check_python_version():
    """Python versiyonunu kontrol et"""
    print_header("🐍 Python Versiyonu")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 veya üzeri gerekli!")
        return False
    
    print("✅ Python versiyonu uygun")
    return True


def install_dependencies():
    """Bağımlılıkları yükle"""
    print_header("📦 Bağımlılıklar Yükleniyor")
    
    print("Temel paketler yükleniyor...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_complete.txt"])
    
    # PyAudio özel kurulum
    if platform.system() == 'Windows':
        print("\n🎤 PyAudio (mikrofon) kuruluyor...")
        print("Bu biraz zaman alabilir...\n")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pipwin"], check=True)
            subprocess.run([sys.executable, "-m", "pipwin", "install", "pyaudio"], check=True)
            print("✅ PyAudio kuruldu")
        except:
            print("⚠️  PyAudio otomatik kurulamadı")
            print("Manuel kurulum için:")
            print("  1. https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
            print("  2. Python versiyonunuza uygun .whl dosyasını indirin")
            print("  3. pip install dosya_adi.whl")


def create_env_file():
    """İlk .env dosyasını oluştur"""
    print_header("⚙️ Yapılandırma")
    
    if os.path.exists('.env'):
        print("✅ .env dosyası mevcut")
        return
    
    print("📝 .env dosyası oluşturuluyor...\n")
    
    print("Google Gemini API Key'inizi alın:")
    print("👉 https://makersuite.google.com/app/apikey")
    print()
    
    api_key = input("Google API Key: ").strip()
    
    print("\nTercihiniz hangisi?")
    print("1. Google TTS (Ücretsiz, doğal ses, internet gerekli)")
    print("2. Azure TTS (Premium kalite, API key gerekli)")
    print("3. Offline TTS (Internet gerektirmez, robotic ses)")
    
    tts_choice = input("\nSeçim (1-3) [1]: ").strip() or "1"
    
    tts_engine = {
        "1": "google",
        "2": "azure",
        "3": "pyttsx3"
    }.get(tts_choice, "google")
    
    azure_key = ""
    azure_region = ""
    
    if tts_engine == "azure":
        print("\nAzure Speech bilgilerinizi girin:")
        azure_key = input("Azure Speech Key: ").strip()
        azure_region = input("Azure Region [westeurope]: ").strip() or "westeurope"
    
    # .env oluştur
    with open('.env', 'w') as f:
        f.write(f"# Google Gemini AI\n")
        f.write(f"GOOGLE_API_KEY={api_key}\n\n")
        
        f.write(f"# Wake Word\n")
        f.write(f"WAKE_WORD=virtus\n\n")
        
        f.write(f"# Dil ve Ses\n")
        f.write(f"LANGUAGE=tr-TR\n")
        f.write(f"VOICE_RATE=165\n\n")
        
        f.write(f"# TTS Motor\n")
        f.write(f"TTS_ENGINE={tts_engine}\n")
        
        if tts_engine == "azure":
            f.write(f"AZURE_SPEECH_KEY={azure_key}\n")
            f.write(f"AZURE_SPEECH_REGION={azure_region}\n")
            f.write(f"AZURE_VOICE_NAME=tr-TR-AhmetNeural\n")
    
    print("\n✅ .env dosyası oluşturuldu!")


def create_directories():
    """Gerekli klasörleri oluştur"""
    print_header("📁 Klasörler")
    
    dirs = ['data', 'logs']
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}/")


def test_microphone():
    """Mikrofon testi"""
    print_header("🎤 Mikrofon Testi")
    
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        
        # Mikrofonları listele
        print("\nMevcut mikrofonlar:")
        mics = sr.Microphone.list_microphone_names()
        
        if not mics:
            print("❌ Hiç mikrofon bulunamadı!")
            return False
        
        for i, name in enumerate(mics[:5]):
            print(f"  [{i}] {name}")
        
        # Mikrofon testi
        print("\n🔊 Mikrofon testi yapılıyor...")
        print("2 saniye içinde bir şeyler söyleyin:\n")
        
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
        
        text = recognizer.recognize_google(audio, language='tr-TR')
        
        print(f"✅ Başarılı! Algılanan: '{text}'")
        return True
        
    except ImportError:
        print("❌ SpeechRecognition veya PyAudio kurulu değil!")
        print("\nKurulum:")
        print("  pip install SpeechRecognition")
        print("  pip install pipwin")
        print("  python -m pipwin install pyaudio")
        return False
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False


def test_tts():
    """Text-to-Speech testi"""
    print_header("🔊 Text-to-Speech Testi")
    
    try:
        from modules.advanced_tts import AdvancedTTS
        
        print("TTS motoru başlatılıyor...")
        tts = AdvancedTTS()
        
        print(f"Motor: {tts.engine_type}")
        print("\n🔊 Test mesajı çalınıyor...\n")
        
        test_msg = "Merhaba! Ben Virtus, sizin kişisel yapay zeka asistanınızım."
        tts.speak(test_msg)
        
        print("✅ TTS çalışıyor!")
        return True
        
    except Exception as e:
        print(f"❌ TTS hatası: {e}")
        return False


def test_ai():
    """AI entegrasyonu testi"""
    print_header("🧠 AI Testi")
    
    try:
        from core.ai_brain import AIBrain
        
        print("AI Brain başlatılıyor...")
        ai = AIBrain()
        
        print("Test komutu gönderiliyor...\n")
        
        result = ai.process_command("Chrome'u aç")
        
        print(f"Intent: {result.get('intent')}")
        print(f"Action: {result.get('action')}")
        print(f"Response: {result.get('response')}")
        
        print("\n✅ AI çalışıyor!")
        return True
        
    except Exception as e:
        print(f"❌ AI hatası: {e}")
        print("\nGoogle API Key'inizi kontrol edin:")
        print("  .env dosyasındaki GOOGLE_API_KEY değerini kontrol edin")
        return False


def test_applications():
    """Uygulama tarayıcıyı test et"""
    print_header("📱 Uygulama Tarayıcı Testi")
    
    try:
        from plugins.application_master import ApplicationMaster
        
        print("Uygulamalar taranıyor...")
        app_master = ApplicationMaster()
        
        print(f"\n✅ {len(app_master.app_database)} uygulama bulundu")
        print(f"🎮 {len(app_master.steam_games)} Steam oyunu")
        
        # Örnek aramalar
        test_apps = ['chrome', 'steam', 'calculator']
        print("\n🔍 Test aramaları:")
        
        for app in test_apps:
            result = app_master.find_application(app)
            if result:
                print(f"  ✅ {app}")
            else:
                print(f"  ⚠️  {app} bulunamadı")
        
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False


def main():
    """Ana kurulum fonksiyonu"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║              VIRTUS AI ASISTAN KURULUM                   ║
    ║                  Gelişmiş Versiyon                       ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # 1. Python versiyonu
    if not check_python_version():
        return
    
    # 2. Bağımlılıklar
    response = input("\nBağımlılıkları yüklemek ister misiniz? (e/h): ")
    if response.lower() == 'e':
        install_dependencies()
    
    # 3. Yapılandırma
    create_env_file()
    
    # 4. Klasörler
    create_directories()
    
    # 5. Testler
    print("\n" + "=" * 60)
    print("  🧪 TESTLER")
    print("=" * 60)
    
    results = {
        "Mikrofon": test_microphone(),
        "TTS": test_tts(),
        "AI": test_ai(),
        "Uygulamalar": test_applications()
    }
    
    # Sonuçlar
    print_header("📊 SONUÇLAR")
    
    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✨ TÜM TESTLER BAŞARILI!")
        print("\nVirtus'u başlatmak için:")
        print("  python main_new.py")
    else:
        print("⚠️  BAZUM TESTLER BAŞARISIZ")
        print("\nSorunları çözüp tekrar deneyin.")
        print("Yardım için KURULUM.md dosyasına bakın.")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()