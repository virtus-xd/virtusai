"""
Text-to-Speech - Metni sese çevirir
"""
import pyttsx3
import logging
from config.settings import VOICE_RATE, VOICE_VOLUME, LANGUAGE

logger = logging.getLogger(__name__)


class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._configure_voice()
    
    def _configure_voice(self):
        """Ses ayarlarını yapılandır"""
        try:
            # Konuşma hızı
            self.engine.setProperty('rate', VOICE_RATE)
            
            # Ses seviyesi
            self.engine.setProperty('volume', VOICE_VOLUME)
            
            # Türkçe ses seç (varsa)
            voices = self.engine.getProperty('voices')
            
            # Windows'ta Türkçe ses ara
            for voice in voices:
                if 'turkish' in voice.name.lower() or 'tr' in voice.id.lower():
                    self.engine.setProperty('voice', voice.id)
                    logger.info(f"Türkçe ses bulundu: {voice.name}")
                    break
            else:
                # Türkçe bulunamazsa varsayılanı kullan
                logger.warning("Türkçe ses bulunamadı, varsayılan ses kullanılıyor")
                
        except Exception as e:
            logger.error(f"TTS konfigürasyon hatası: {e}")
    
    def speak(self, text):
        """Metni seslendir"""
        try:
            logger.info(f"🔊 Konuşuyor: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            logger.error(f"TTS hatası: {e}")
    
    def speak_async(self, text):
        """Metni asenkron seslendir (bloke etmez)"""
        try:
            logger.info(f"🔊 Konuşuyor (async): {text}")
            self.engine.say(text)
            self.engine.startLoop(False)
            self.engine.iterate()
            self.engine.endLoop()
            
        except Exception as e:
            logger.error(f"TTS async hatası: {e}")
    
    def stop(self):
        """Konuşmayı durdur"""
        try:
            self.engine.stop()
        except:
            pass


# Alternatif: gTTS kullanımı (internet gerektirir ama daha iyi ses kalitesi)
"""
from gtts import gTTS
import os
import pygame

def speak_gtts(text, lang='tr'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save('temp_speech.mp3')
        
        pygame.mixer.init()
        pygame.mixer.music.load('temp_speech.mp3')
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        os.remove('temp_speech.mp3')
    except Exception as e:
        logger.error(f"gTTS error: {e}")
"""
