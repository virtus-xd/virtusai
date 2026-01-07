"""
VIRTUS AI ASISTAN - Yeni Ana Giriş Noktası
Tamamen yeniden yapılandırılmış sistem

Kullanım:
    python main_new.py              # Sesli mod (wake word ile)
    python main_new.py --no-wake    # Sesli mod (wake word olmadan)
    python main_new.py --test       # Test modu (klavyeden komut)
    python main_new.py --setup      # Kurulum ve testler
"""
import sys
import os

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
from pathlib import Path

# Logging yapılandırması
log_file = Path('data/virtus.log')
log_file.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def print_banner():
    """Hoş geldin banner'ı"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║                  VIRTUS AI ASISTAN                       ║
    ║              Powered by Google Gemini 2.0                ║
    ║                                                          ║
    ║              🎤 Sesli Komut Sistemi                      ║
    ║              🧠 Gelişmiş AI İşleme                       ║
    ║              📱 Geniş Uygulama Desteği                   ║
    ║              🔊 Doğal Türkçe Ses                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)


def run_voice_mode(with_wake_word=True):
    """Sesli mod - ana kullanım"""
    try:
        from core.virtus_fixed import VirtusFixed
        from config import settings
        
        print_banner()
        
        # Wake word ayarını geçici olarak değiştir
        if not with_wake_word:
            settings.ENABLE_WAKE_WORD = False
        
        # Virtus'u başlat
        virtus = VirtusFixed()
        virtus.start()
        
    except ImportError as e:
        print(f"\n❌ Modül yükleme hatası: {e}")
        print("\nEksik bağımlılıklar olabilir. Kurulum için:")
        print("  python setup_complete.py")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Kritik Hata: {e}")


def run_test_mode():
    """Test modu - klavyeden komut"""
    try:
        from core.virtus_fixed import VirtusFixed
        
        print_banner()
        print("🧪 TEST MODU - Klavyeden komut girin\n")
        print("Örnek komutlar:")
        print("  - Chrome'u aç")
        print("  - Ses seviyesini 50 yap")
        print("  - YouTube'da Python tutorial ara")
        print("  - 15 çarpı 23 kaç eder?")
        print("\nÇıkmak için 'exit' veya 'çıkış' yazın\n")
        print("=" * 60 + "\n")
        
        # Virtus'u başlat (ama start() çağırma)
        virtus = VirtusFixed()
        
        # Test döngüsü
        while True:
            try:
                command = input("💬 Komut: ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['exit', 'quit', 'çıkış', 'kapat']:
                    virtus.speak("Görüşürüz!")
                    print("\n👋 Görüşürüz!\n")
                    break
                
                # Manuel komut çalıştır
                virtus.manual_command(command)
                
            except KeyboardInterrupt:
                print("\n\n👋 Görüşürüz!\n")
                break
                
    except Exception as e:
        logger.error(f"Test mode error: {e}")
        print(f"\n❌ Hata: {e}")


def run_setup():
    """Kurulum ve test scripti"""
    try:
        from setup_complete import main as setup_main
        setup_main()
    except ImportError:
        print("❌ setup_complete.py bulunamadı!")


def show_help():
    """Yardım mesajı"""
    print("""
    VIRTUS AI ASISTAN - Kullanım Kılavuzu
    
    🎤 SESLI MOD (Önerilen):
    
        python main_new.py
        
        Wake word ile çalışır. "Virtus" diyerek uyandırın,
        ardından komutunuzu söyleyin.
    
    
    🎤 SESLI MOD (Wake Word Olmadan):
    
        python main_new.py --no-wake
        
        Sürekli dinler, wake word gerektirmez.
        Direkt komutlarınızı söyleyebilirsiniz.
    
    
    ⌨️  TEST MODU:
    
        python main_new.py --test
        
        Klavyeden komut yazarak test edin.
        Mikrofonla ilgili sorun varsa bu modu kullanın.
    
    
    ⚙️  KURULUM & TEST:
    
        python main_new.py --setup
        
        Bağımlılık kontrolü, yapılandırma ve testler.
        İlk kurulumda veya sorun yaşıyorsanız çalıştırın.
    
    
    📝 ÖRNEK KOMUTLAR:
    
        "Chrome'u aç"
        "Spotify'ı çalıştır"
        "Counter-Strike oyununu başlat"
        "Ses seviyesini 70 yap"
        "YouTube'da Python tutorial ara"
        "Ekranı kilitle"
        "5 çarpı 7 kaç eder?"
        "Ankara'nın nüfusu kaç?"
        "Kapat" / "Çıkış" (asistanı kapatmak için)
    
    
    🔧 SORUN GİDERME:
    
        Mikrofon çalışmıyor:
          → python main_new.py --setup
          → Mikrofon izinlerini kontrol edin
          → PyAudio kurulumunu kontrol edin
        
        Ses çıkmıyor:
          → .env dosyasında TTS_ENGINE ayarını kontrol edin
          → Hoparlör bağlantısını kontrol edin
        
        AI yanıt vermiyor:
          → .env dosyasında GOOGLE_API_KEY kontrolü
          → Internet bağlantısı
        
        Uygulama açmıyor:
          → Uygulama cache'ini yenileyin (ilk çalıştırmada otomatik)
          → Uygulama adını tam söyleyin
    
    
    📚 DAHA FAZLA BİLGİ:
    
        README.md         - Genel bilgi
        KURULUM.md        - Detaylı kurulum
        QUICK_START.md    - Hızlı başlangıç
    
    
    💡 İPUCU:
    
        Asistanı her açtığınızda "Merhaba" der ve sizi dinlemeye
        başlar. Wake word modu aktifse "Virtus" demeniz gerekir.
    """)


def main():
    """Ana fonksiyon - komut satırı argümanlarını işle"""
    
    # Argüman kontrolü
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h', 'help']:
            show_help()
            
        elif arg in ['--test', '-t', 'test']:
            run_test_mode()
            
        elif arg in ['--setup', '-s', 'setup']:
            run_setup()
            
        elif arg in ['--no-wake', '--continuous', '-c']:
            run_voice_mode(with_wake_word=False)
            
        else:
            print(f"❌ Bilinmeyen argüman: {arg}")
            print("Yardım için: python main_new.py --help")
    
    else:
        # Varsayılan: Sesli mod (wake word ile)
        run_voice_mode(with_wake_word=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Görüşürüz!\n")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        print(f"\n❌ Beklenmeyen Hata: {e}")
        print("Detaylar için data/virtus.log dosyasına bakın\n")