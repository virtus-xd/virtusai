"""
Gelişmiş Text-to-Speech Sistemi
- Google TTS (doğal, akıcı erkek sesi)
- Azure TTS (en kaliteli, opsiyonel)
- Offline fallback (pyttsx3)
"""
import os
import logging
import tempfile
import time
from pathlib import Path
from config.settings import (
    TTS_ENGINE, VOICE_RATE, AZURE_SPEECH_KEY, 
    AZURE_SPEECH_REGION, AZURE_VOICE_NAME
)

logger = logging.getLogger(__name__)


class AdvancedTTS:
    """Akıllı TTS Sistemi - En iyi ses kalitesi"""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.engine_type = TTS_ENGINE
        self.engine = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """En uygun TTS motorunu başlat"""
        
        # 1. Öncelik: Azure TTS (en iyi kalite)
        if self.engine_type == 'azure' and AZURE_SPEECH_KEY:
            if self._init_azure():
                logger.info("✅ Azure TTS hazır (premium kalite)")
                return
        
        # 2. İkinci seçenek: Google TTS (iyi kalite, ücretsiz)
        if self.engine_type == 'google' or not AZURE_SPEECH_KEY:
            if self._init_google():
                logger.info("✅ Google TTS hazır (doğal ses)")
                return
        
        # 3. Fallback: pyttsx3 (offline ama robotic)
        self._init_pyttsx3()
        logger.info("✅ Offline TTS hazır (internet gerektirmez)")
    
    def _init_azure(self):
        """Azure Cognitive Services TTS"""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            speech_config = speechsdk.SpeechConfig(
                subscription=AZURE_SPEECH_KEY,
                region=AZURE_SPEECH_REGION
            )
            
            # Türkçe erkek sesi - çok doğal
            speech_config.speech_synthesis_voice_name = AZURE_VOICE_NAME
            
            # Konuşma hızı ayarı
            speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
            )
            
            self.engine = speechsdk.SpeechSynthesizer(speech_config=speech_config)
            self.engine_type = 'azure'
            return True
            
        except ImportError:
            logger.warning("Azure Speech SDK kurulu değil: pip install azure-cognitiveservices-speech")
            return False
        except Exception as e:
            logger.warning(f"Azure TTS başlatılamadı: {e}")
            return False
    
    def _init_google(self):
        """Google TTS - Ücretsiz ve kaliteli"""
        try:
            from gtts import gTTS
            self.engine_type = 'google'
            return True
        except ImportError:
            logger.warning("gTTS kurulu değil: pip install gtts")
            return False
    
    def _init_pyttsx3(self):
        """Offline TTS - Fallback"""
        try:
            import pyttsx3
            
            self.engine = pyttsx3.init()
            
            # Türkçe erkek sesi seç
            voices = self.engine.getProperty('voices')
            
            # Türkçe erkek ses ara
            for voice in voices:
                name_lower = voice.name.lower()
                if 'turkish' in name_lower or 'tr-tr' in voice.id.lower():
                    if 'male' in name_lower or 'erkek' in name_lower:
                        self.engine.setProperty('voice', voice.id)
                        logger.info(f"Türkçe erkek ses bulundu: {voice.name}")
                        break
            
            # Konuşma hızı ve ses seviyesi
            self.engine.setProperty('rate', VOICE_RATE)
            self.engine.setProperty('volume', 0.95)
            
            self.engine_type = 'pyttsx3'
            return True
            
        except Exception as e:
            logger.error(f"pyttsx3 başlatılamadı: {e}")
            return False
    
    def speak(self, text, blocking=True):
        """
        Metni akıcı erkek sesiyle seslendir
        
        Args:
            text: Söylenecek metin
            blocking: True ise konuşma bitene kadar bekle
        """
        if not text or not text.strip():
            return
        
        text = text.strip()
        logger.info(f"🔊 Konuşuyor: {text[:50]}...")
        
        try:
            if self.engine_type == 'azure':
                self._speak_azure(text, blocking)
            elif self.engine_type == 'google':
                self._speak_google(text, blocking)
            else:
                self._speak_pyttsx3(text, blocking)
                
        except Exception as e:
            logger.error(f"TTS hatası: {e}")
            # Fallback dene
            if self.engine_type != 'pyttsx3':
                logger.info("Offline TTS'ye geçiliyor...")
                self._init_pyttsx3()
                self._speak_pyttsx3(text, blocking)
    
    def _speak_azure(self, text, blocking):
        """Azure ile konuş"""
        if blocking:
            result = self.engine.speak_text_async(text).get()
            if result.reason != 0:  # Success
                logger.warning(f"Azure TTS uyarısı: {result.reason}")
        else:
            self.engine.speak_text_async(text)
    
    def _speak_google(self, text, blocking):
        """Google TTS ile konuş - Doğal ses"""
        from gtts import gTTS
        
        # Geçici MP3 dosyası
        temp_file = os.path.join(self.temp_dir, f'virtus_{int(time.time())}.mp3')
        
        try:
            # Google TTS ile oluştur - erkek sesi için tld kullanıyoruz
            tts = gTTS(text=text, lang='tr', slow=False, tld='com.tr')
            tts.save(temp_file)
            
            # Oynat
            self._play_audio_file(temp_file, blocking)
            
        finally:
            # Temizle
            try:
                if os.path.exists(temp_file):
                    time.sleep(0.1)  # Dosya açık olabilir
                    os.remove(temp_file)
            except:
                pass
    
    def _speak_pyttsx3(self, text, blocking):
        """Offline TTS ile konuş"""
        if blocking:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            self.engine.say(text)
            self.engine.startLoop(False)
            self.engine.iterate()
            self.engine.endLoop()
    
    def _play_audio_file(self, filepath, blocking=True):
        """Ses dosyasını oynat - Platform bağımsız"""
        # Öncelik 1: pygame (en güvenilir, cross-platform)
        try:
            import pygame
            
            # pygame mixer'ı başlat (eğer başlatılmamışsa)
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            
            if blocking:
                # Çalma bitene kadar bekle
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            
            return
            
        except ImportError:
            logger.warning("pygame kurulu değil, alternatif yöntem deneniyor...")
        except Exception as e:
            logger.warning(f"pygame hatası: {e}, alternatif yöntem deneniyor...")
        
        # Öncelik 2: Windows winsound (sadece WAV)
        if os.name == 'nt':
            try:
                # MP3'ü WAV'a çevirmeye gerek yok, PowerShell kullan
                import subprocess
                ps_command = f'''
                $player = New-Object System.Media.SoundPlayer
                $player.SoundLocation = "{filepath}"
                $player.PlaySync()
                '''
                
                if blocking:
                    subprocess.run(['powershell', '-Command', ps_command], 
                                 capture_output=True, timeout=30)
                else:
                    ps_command = ps_command.replace('PlaySync', 'Play')
                    subprocess.Popen(['powershell', '-Command', ps_command],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                return
                
            except Exception as e:
                logger.warning(f"PowerShell hatası: {e}")
        
        # Öncelik 3: ffplay (Linux/Mac)
        try:
            import subprocess
            if blocking:
                subprocess.run(['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', filepath], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL,
                             timeout=30)
            else:
                subprocess.Popen(['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', filepath],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            return
            
        except (FileNotFoundError, Exception) as e:
            logger.warning(f"ffplay hatası: {e}")
        
        # Son çare: Browser açma (Windows için)
        if os.name == 'nt':
            try:
                os.startfile(filepath)
            except Exception as e:
                logger.error(f"Ses oynatılamadı: {e}")
    
    def stop(self):
        """Konuşmayı durdur"""
        try:
            if self.engine_type == 'pyttsx3' and self.engine:
                self.engine.stop()
        except:
            pass
    
    def test_voice(self):
        """Ses testisi yap"""
        test_messages = [
            "Merhaba! Ben Virtus, sizin kişisel yapay zeka asistanınızım.",
            "Ses kalitemi test ediyorum. Beni net duyabiliyor musunuz?",
            "Chrome'u açıyorum, ses seviyesini ayarlıyorum, veya hesaplama yapabilirim."
        ]
        
        print("\n🔊 TTS Test Başlıyor...")
        print(f"Motor: {self.engine_type}")
        print("-" * 50)
        
        for i, msg in enumerate(test_messages, 1):
            print(f"\n[{i}/{len(test_messages)}] {msg}")
            self.speak(msg, blocking=True)
            time.sleep(0.5)
        
        print("\n✅ Test tamamlandı!")


# Test kodu
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("""
    ╔═══════════════════════════════════════════╗
    ║         VIRTUS TTS TEST                   ║
    ╚═══════════════════════════════════════════╝
    """)
    
    tts = AdvancedTTS()
    tts.test_voice()