"""
VIRTUS AI Asistan - Ana Giriş Noktası
"""
import sys
import os

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.virtus import Virtus
import logging

logger = logging.getLogger(__name__)


def main():
    """Ana fonksiyon"""
    print("""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║            VIRTUS AI ASISTAN              ║
    ║         Powered by Google Gemini          ║
    ║                                           ║
    ║    "Virtus" diyerek beni uyandırın!      ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    """)
    
    try:
        # Virtus'u başlat
        virtus = Virtus()
        
        # Komut satırı argümanları kontrol et
        if len(sys.argv) > 1:
            if sys.argv[1] == '--test':
                # Test modu
                print("\n🧪 TEST MODU - Manuel komut girin (çıkmak için 'exit'):\n")
                while True:
                    cmd = input("Komut: ")
                    if cmd.lower() in ['exit', 'quit', 'çıkış']:
                        break
                    virtus.manual_command(cmd)
            elif sys.argv[1] == '--help':
                print("""
Kullanım:
    python main.py              # Normal mod (wake word ile)
    python main.py --test       # Test modu (manuel komut)
    python main.py --help       # Yardım
                """)
        else:
            # Normal mod - wake word ile çalış
            virtus.start()
            
    except KeyboardInterrupt:
        print("\n\n👋 Görüşürüz!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Hata: {e}")


if __name__ == "__main__":
    main()
