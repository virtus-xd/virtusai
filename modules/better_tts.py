"""
İyileştirilmiş Text-to-Speech - Daha doğal erkek sesi
"""
import os
import logging
from gtts import gTTS
import tempfile
import platform

logger = logging.getLogger(__name__)

# Ses çalma için platform kontrolü
if platform.system() == 'Windows':
    import winsound
    AUDIO_PLAYER = 'winsound'
else:
    try:
        from playsound import playsound
        AUDIO_PLAYER = 'playsound'
    except:
        import pygame
        pygame.mixer.init()
        AUDIO_PLAYER = 'pygame'


class BetterTTS:
    """Google TTS ile daha doğal ses"""
    
    def __init__(self, language='tr', slow=False):
        self.language = language
        self.slow = slow
        self.temp_dir = tempfile.gettempdir()
        logger.info("✅ Google TTS hazır (doğal ses)")
    
    def speak(self, text):
        """Metni doğal sesle seslendir"""
        if not text:
            return
        
        try:
            logger.info(f"🔊 Konuşuyor: {text}")
            
            # Geçici dosya oluştur
            temp_file = os.path.join(self.temp_dir, 'virtus_speech.mp3')
            
            # Google TTS ile oluştur
            tts = gTTS(text=text, lang=self.language, slow=self.slow)
            tts.save(temp_file)
            
            # Oynat
            self._play_audio(temp_file)
            
            # Temizle
            try:
                os.remove(temp_file)
            except:
                pass
            
        except Exception as e:
            logger.error(f"TTS hatası: {e}")
    
    def _play_audio(self, file_path):
        """Ses dosyasını oynat"""
        try:
            if AUDIO_PLAYER == 'winsound':
                # Windows için
                import subprocess
                subprocess.run(['powershell', '-c', 
                              f'(New-Object Media.SoundPlayer "{file_path}").PlaySync()'],
                             timeout=30)
            
            elif AUDIO_PLAYER == 'playsound':
                from playsound import playsound
                playsound(file_path)
            
            elif AUDIO_PLAYER == 'pygame':
                import pygame
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            
        except Exception as e:
            logger.error(f"Ses çalma hatası: {e}")


# Fallback: pyttsx3 ile offline ses (internet yoksa)
class OfflineTTS:
    """Offline TTS - pyttsx3 ile"""
    
    def __init__(self):
        import pyttsx3
        self.engine = pyttsx3.init()
        self._configure()
    
    def _configure(self):
        """Türkçe erkek sesi seç"""
        try:
            self.engine.setProperty('rate', 160)  # Biraz hızlı
            self.engine.setProperty('volume', 1.0)
            
            # Türkçe erkek ses bul
            voices = self.engine.getProperty('voices')
            
            # Önce Türkçe erkek ara
            for voice in voices:
                if 'turkish' in voice.name.lower() and 'male' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    logger.info(f"Ses: {voice.name}")
                    return
            
            # Türkçe herhangi biri
            for voice in voices:
                if 'turkish' in voice.name.lower() or 'tr' in voice.id.lower():
                    self.engine.setProperty('voice', voice.id)
                    logger.info(f"Ses: {voice.name}")
                    return
            
            # Hiçbiri yoksa varsayılan
            logger.warning("Türkçe ses bulunamadı, varsayılan kullanılıyor")
            
        except Exception as e:
            logger.error(f"TTS konfigürasyon hatası: {e}")
    
    def speak(self, text):
        """Offline konuş"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS hatası: {e}")


# Ana TTS sınıfı - otomatik seçim
class SmartTTS:
    """Akıllı TTS - internet varsa Google, yoksa offline"""
    
    def __init__(self):
        self.online_available = self._check_internet()
        
        if self.online_available:
            logger.info("🌐 Online TTS (Google) kullanılıyor")
            self.tts = BetterTTS()
        else:
            logger.info("💾 Offline TTS kullanılıyor")
            self.tts = OfflineTTS()
    
    def _check_internet(self):
        """Internet bağlantısı var mı?"""
        try:
            import requests
            requests.get('https://www.google.com', timeout=2)
            return True
        except:
            return False
    
    def speak(self, text):
        """Konuş (otomatik online/offline)"""
        self.tts.speak(text)
