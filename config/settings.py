"""
Virtus Asistan - Ayarlar
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY', '')

# Asistan Ayarları
ASSISTANT_NAME = "Virtus"
WAKE_WORD = os.getenv('WAKE_WORD', 'virtus')
LANGUAGE = os.getenv('LANGUAGE', 'tr-TR')

# Ses Ayarları
VOICE_RATE = int(os.getenv('VOICE_RATE', 150))
VOICE_VOLUME = 1.0

# Mikrofon Ayarları
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024

# Timeout Ayarları
LISTENING_TIMEOUT = 5  # Komut bekleme süresi (saniye)
PHRASE_TIMEOUT = 2

# Log Ayarları
LOG_LEVEL = 'INFO'
LOG_FILE = 'data/virtus.log'

# Platform
import platform
PLATFORM = platform.system()  # Windows, Linux, Darwin (macOS)
