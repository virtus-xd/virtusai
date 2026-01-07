"""
Action Executor - AI'dan gelen komutları çalıştırır
"""
import logging
import webbrowser
import subprocess
import os
from config.settings import PLATFORM

# Platform-specific controllers
try:
    from plugins.phone_controller import ContactManager, ADBPhoneController
    from plugins.windows_controller import WindowsController
    PLUGINS_AVAILABLE = True
except ImportError:
    PLUGINS_AVAILABLE = False

logger = logging.getLogger(__name__)


class ActionExecutor:
    def __init__(self):
        self.platform = PLATFORM
        self.app_mappings = self._get_app_mappings()
        
        # Controller'ları başlat
        if PLUGINS_AVAILABLE:
            self.contact_manager = ContactManager()
            self.phone_controller = ADBPhoneController()
            
            if self.platform == 'Windows':
                self.windows_controller = WindowsController()
            else:
                self.windows_controller = None
        else:
            self.contact_manager = None
            self.phone_controller = None
            self.windows_controller = None
    
    def _get_app_mappings(self):
        """Platform-specific uygulama yolları"""
        if self.platform == 'Windows':
            return {
                'chrome': 'chrome.exe',
                'firefox': 'firefox.exe',
                'edge': 'msedge.exe',
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'paint': 'mspaint.exe',
                'word': 'winword.exe',
                'excel': 'excel.exe',
                'spotify': 'spotify.exe',
                'discord': 'discord.exe',
                'telegram': 'telegram.exe',
                'whatsapp': 'whatsapp.exe'
            }
        # Linux/Mac için başka mappings eklenebilir
        return {}
    
    def execute(self, intent_data):
        """
        Intent'e göre aksiyonu çalıştır
        
        Args:
            intent_data (dict): AI'dan gelen intent verisi
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            intent = intent_data.get('intent', '')
            action = intent_data.get('action', '')
            params = intent_data.get('parameters', {})
            
            logger.info(f"⚡ Executing: {intent} -> {action}")
            
            # Intent'e göre yönlendir
            if intent == 'call':
                return self._make_call(params)
            
            elif intent == 'open_app':
                return self._open_application(params)
            
            elif intent == 'close_app':
                return self._close_application(params)
            
            elif intent == 'search':
                return self._web_search(params)
            
            elif intent == 'system_control':
                return self._system_control(params)
            
            elif intent == 'file_operation':
                return self._file_operation(params)
            
            elif intent == 'calculation':
                return True  # Hesaplama AI tarafından yapılır
            
            elif intent == 'information':
                return True  # Bilgi AI tarafından verilir
            
            elif intent == 'chat':
                return True  # Sohbet, yanıt zaten AI'dan gelir
            
            else:
                logger.warning(f"Bilinmeyen intent: {intent}")
                return False
                
        except Exception as e:
            logger.error(f"Action execution error: {e}")
            return False
    
    def _make_call(self, params):
        """Telefon araması yap"""
        contact = params.get('contact', '')
        phone_number = params.get('phone_number', '')
        
        # Eğer isim verilmişse, numarayı bul
        if contact and not phone_number and self.contact_manager:
            phone_number = self.contact_manager.get_phone_number(contact)
            
            if not phone_number:
                logger.warning(f"Kişi bulunamadı: {contact}")
                return False
        
        if phone_number and self.phone_controller:
            return self.phone_controller.make_call(phone_number)
        else:
            logger.warning("Telefon kontrolcüsü kullanılamıyor")
            return False
    
    def _open_application(self, params):
        """Uygulama aç"""
        app_name = params.get('app_name', '').lower()
        
        if app_name in self.app_mappings:
            try:
                if self.platform == 'Windows':
                    os.startfile(self.app_mappings[app_name])
                else:
                    subprocess.Popen([self.app_mappings[app_name]])
                
                logger.info(f"✅ {app_name} açıldı")
                return True
            except Exception as e:
                logger.error(f"Uygulama açılamadı: {e}")
                return False
        else:
            logger.warning(f"Uygulama bulunamadı: {app_name}")
            return False
    
    def _close_application(self, params):
        """Uygulama kapat"""
        app_name = params.get('app_name', '').lower()
        
        try:
            if self.platform == 'Windows':
                subprocess.run(['taskkill', '/IM', self.app_mappings.get(app_name, app_name), '/F'])
            else:
                subprocess.run(['killall', app_name])
            
            logger.info(f"✅ {app_name} kapatıldı")
            return True
        except Exception as e:
            logger.error(f"Uygulama kapatılamadı: {e}")
            return False
    
    def _web_search(self, params):
        """Web'de arama yap"""
        query = params.get('query', '')
        search_engine = params.get('engine', 'google')
        
        if search_engine == 'google':
            url = f"https://www.google.com/search?q={query}"
        elif search_engine == 'youtube':
            url = f"https://www.youtube.com/results?search_query={query}"
        else:
            url = f"https://www.google.com/search?q={query}"
        
        webbrowser.open(url)
        logger.info(f"🔍 Arama yapıldı: {query}")
        return True
    
    def _system_control(self, params):
        """Sistem kontrolü (ses, parlaklık, vb.)"""
        control_type = params.get('type', '').lower()
        value = params.get('value', '')
        
        logger.info(f"🔧 Sistem kontrolü: {control_type} = {value}")
        
        if not self.windows_controller and self.platform == 'Windows':
            logger.warning("Windows kontrolcüsü kullanılamıyor")
            return False
        
        try:
            if control_type == 'volume' or control_type == 'ses':
                if isinstance(value, str) and value.lower() in ['kapat', 'mute', 'sessiz']:
                    return self.windows_controller.mute()
                elif isinstance(value, str) and value.lower() in ['aç', 'unmute']:
                    return self.windows_controller.unmute()
                else:
                    level = int(value)
                    return self.windows_controller.set_volume(level)
            
            elif control_type == 'brightness' or control_type == 'parlaklık':
                level = int(value)
                return self.windows_controller.set_brightness(level)
            
            elif control_type == 'shutdown' or control_type == 'kapat':
                delay = int(value) if value else 60
                return self.windows_controller.shutdown(delay)
            
            elif control_type == 'restart' or control_type == 'yeniden başlat':
                delay = int(value) if value else 60
                return self.windows_controller.restart(delay)
            
            elif control_type == 'lock' or control_type == 'kilitle':
                return self.windows_controller.lock_screen()
            
            elif control_type == 'sleep' or control_type == 'uyku':
                return self.windows_controller.sleep()
            
            else:
                logger.warning(f"Bilinmeyen sistem kontrolü: {control_type}")
                return False
                
        except Exception as e:
            logger.error(f"Sistem kontrolü hatası: {e}")
            return False
    
    def _file_operation(self, params):
        """Dosya işlemleri"""
        operation = params.get('operation', '')
        path = params.get('path', '')
        
        logger.info(f"📁 Dosya işlemi: {operation} - {path}")
        
        # TODO: Dosya işlemleri implementasyonu
        
        return True
