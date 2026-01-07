"""
Virtus Asistan - Ayarlar
Tüm yapılandırma burada
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# API KEYS
# ============================================
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY', '')

# Azure TTS (Opsiyonel - Premium)
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY', '')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION', 'westeurope')
AZURE_VOICE_NAME = os.getenv('AZURE_VOICE_NAME', 'tr-TR-AhmetNeural')

# ============================================
# ASİSTAN AYARLARI
# ============================================
ASSISTANT_NAME = "Virtus"
WAKE_WORD = os.getenv('WAKE_WORD', 'virtus')
LANGUAGE = os.getenv('LANGUAGE', 'tr-TR')

# ============================================
# SES AYARLARI (TTS)
# ============================================
VOICE_RATE = int(os.getenv('VOICE_RATE', 165))  # Konuşma hızı
VOICE_VOLUME = 0.95

# TTS Motor Seçimi
# 'google' = gTTS (en iyi, ücretsiz, internet gerekli)
# 'azure' = Azure TTS (premium, API key gerekli)
# 'pyttsx3' = Offline (internet gerektirmez)
TTS_ENGINE = os.getenv('TTS_ENGINE', 'google')

# ============================================
# MİKROFON AYARLARI
# ============================================
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
ENERGY_THRESHOLD = 1500  # DÜŞÜRÜLDÜ - daha hassas (eski: 3000)
DYNAMIC_ENERGY = True    # Otomatik ayarlama
PAUSE_THRESHOLD = 0.8    # Konuşma duraklaması

# Mikrofon kazancı (1.0 = normal, 2.0 = 2x hassas)
MICROPHONE_GAIN = float(os.getenv('MICROPHONE_GAIN', 1.5))

# ============================================
# TIMEOUT AYARLARI
# ============================================
LISTENING_TIMEOUT = 5      # Komut bekleme süresi (saniye)
PHRASE_TIMEOUT = 10        # Maksimum konuşma süresi
WAKE_WORD_TIMEOUT = 1      # Wake word bekleme

# ============================================
# UYGULAMA TARAMA
# ============================================
SCAN_STEAM_GAMES = True
SCAN_EPIC_GAMES = True
SCAN_START_MENU = True
SCAN_REGISTRY = True
APP_CACHE_REFRESH = 3600   # Cache yenileme (saniye)

# ============================================
# LOG AYARLARI
# ============================================
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = 'data/virtus.log'
ENABLE_DEBUG = os.getenv('ENABLE_DEBUG', 'False').lower() == 'true'

# ============================================
# PLATFORM
# ============================================
import platform
PLATFORM = platform.system()  # Windows, Linux, Darwin (macOS)

# ============================================
# ÖZELLİK TOGGLE'LARI
# ============================================
ENABLE_WAKE_WORD = os.getenv('ENABLE_WAKE_WORD', 'True').lower() == 'true'
ENABLE_CONTINUOUS_LISTENING = True
ENABLE_CONTEXT_AWARENESS = True
ENABLE_LEARNING = False  # Gelecek özellik

# ============================================
# PERFORMANS
# ============================================
MAX_CONVERSATION_HISTORY = 10
AI_RESPONSE_TIMEOUT = 10

# ============================================
# GELİŞMİŞ AYARLAR
# ============================================
# Ses tanıma backend'i
# 'google' = Google Speech Recognition (ücretsiz)
# 'whisper' = OpenAI Whisper (offline, yavaş)
SPEECH_BACKEND = os.getenv('SPEECH_BACKEND', 'google')

# AI Model
# 'gemini-2.0-flash-exp' = Yeni model (hızlı)
# 'gemini-pro' = Eski model (stabil)
AI_MODEL = os.getenv('AI_MODEL', 'gemini-2.0-flash-exp')

# ============================================
# AYAR KONTROLÜ
# ============================================
def check_settings():
    """Kritik ayarları kontrol et"""
    issues = []
    
    if not GOOGLE_API_KEY:
        issues.append("❌ GOOGLE_API_KEY eksik!")
    
    if TTS_ENGINE == 'azure' and not AZURE_SPEECH_KEY:
        issues.append("⚠️  Azure TTS seçili ama AZURE_SPEECH_KEY yok")
    
    if issues:
        print("\n⚠️  Yapılandırma Uyarıları:")
        for issue in issues:
            print(f"   {issue}")
        print()
    
    return len(issues) == 0


# Başlangıçta kontrol et
if __name__ == "__main__":
    print("Virtus Ayarları:")
    print(f"  - Asistan: {ASSISTANT_NAME}")
    print(f"  - Wake Word: {WAKE_WORD}")
    print(f"  - Dil: {LANGUAGE}")
    print(f"  - TTS Motor: {TTS_ENGINE}")
    print(f"  - Platform: {PLATFORM}")
    print(f"  - API Key: {'✓' if GOOGLE_API_KEY else '✗'}")
    
    check_settings()