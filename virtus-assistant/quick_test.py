"""
Hızlı Modül Testi - Tüm yeni modülleri test eder
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("""
╔══════════════════════════════════════════════════════════╗
║              VIRTUS HIZLI MODÜL TESTİ                    ║
╚══════════════════════════════════════════════════════════╝
""")

results = {}

# 1. Config Test
print("\n[1/5] Config modülü test ediliyor...")
try:
    from config import settings
    print(f"✅ Config yüklendi")
    print(f"   - API Key: {'✓' if settings.GOOGLE_API_KEY else '✗ EKSİK!'}")
    print(f"   - TTS Engine: {settings.TTS_ENGINE}")
    print(f"   - Wake Word: {settings.WAKE_WORD}")
    results['config'] = True
except Exception as e:
    print(f"❌ Config hatası: {e}")
    results['config'] = False

# 2. TTS Test
print("\n[2/5] TTS modülü test ediliyor...")
try:
    from modules.advanced_tts import AdvancedTTS
    
    tts = AdvancedTTS()
    print(f"✅ TTS yüklendi (Motor: {tts.engine_type})")
    
    # Kısa test
    print("🔊 Test sesi çalınıyor...")
    tts.speak("Merhaba! TTS sistemi çalışıyor.", blocking=True)
    print("✅ TTS çalıştı!")
    
    results['tts'] = True
except Exception as e:
    print(f"❌ TTS hatası: {e}")
    results['tts'] = False

# 3. Speech Recognition Test
print("\n[3/5] Speech Recognition test ediliyor...")
try:
    from modules.advanced_speech_recognition import AdvancedSpeechRecognition
    
    speech = AdvancedSpeechRecognition()
    print(f"✅ Speech Recognition yüklendi")
    print(f"   - Mikrofon: {'✓' if speech.is_available() else '✗'}")
    print(f"   - Kalibre: {'✓' if speech.is_calibrated else '✗'}")
    
    results['speech'] = True
except Exception as e:
    print(f"❌ Speech Recognition hatası: {e}")
    print("   PyAudio kurulu olmayabilir!")
    results['speech'] = False

# 4. AI Brain Test
print("\n[4/5] AI Brain test ediliyor...")
try:
    from core.ai_brain import AIBrain
    
    ai = AIBrain()
    print(f"✅ AI Brain yüklendi")
    
    # Basit test
    result = ai.process_command("Test komutu")
    print(f"   - Yanıt: {result.get('response', 'N/A')[:50]}...")
    
    results['ai'] = True
except Exception as e:
    print(f"❌ AI Brain hatası: {e}")
    print("   Google API Key kontrolü yapın!")
    results['ai'] = False

# 5. Application Master Test
print("\n[5/5] Application Master test ediliyor...")
try:
    from plugins.application_master import ApplicationMaster
    
    apps = ApplicationMaster()
    print(f"✅ Application Master yüklendi")
    print(f"   - Toplam uygulama: {len(apps.app_database)}")
    print(f"   - Steam oyunları: {len(apps.steam_games)}")
    
    # Chrome testi
    chrome = apps.find_application('chrome')
    print(f"   - Chrome bulundu: {'✓' if chrome else '✗'}")
    
    results['apps'] = True
except Exception as e:
    print(f"❌ Application Master hatası: {e}")
    results['apps'] = False

# Sonuçlar
print("\n" + "=" * 60)
print("SONUÇLAR:")
print("=" * 60)

for module, status in results.items():
    symbol = "✅" if status else "❌"
    print(f"{symbol} {module.upper()}")

all_passed = all(results.values())

print("\n" + "=" * 60)
if all_passed:
    print("✨ TÜM MODÜLLER ÇALIŞIYOR!")
    print("\nVirtus'u başlatmak için:")
    print("  python main_new.py")
    print("\nVeya test modu için:")
    print("  python main_new.py --test")
else:
    print("⚠️ BAZI MODÜLLER ÇALIŞMIYOR")
    print("\nEksik modüller için:")
    
    if not results.get('speech'):
        print("\n🎤 PyAudio kurulumu:")
        print("  pip install pipwin")
        print("  python -m pipwin install pyaudio")
    
    if not results.get('ai'):
        print("\n🧠 Google API Key:")
        print("  .env dosyasında GOOGLE_API_KEY ayarlayın")
    
    if not results.get('tts'):
        print("\n🔊 TTS kurulumu:")
        print("  pip install gtts pyttsx3")

print("=" * 60 + "\n")
