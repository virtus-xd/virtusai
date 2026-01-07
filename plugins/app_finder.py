"""
Dinamik Uygulama Bulucu - Registry ve Start Menu'den uygulamaları tarar
"""
import os
import logging
import winreg
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class AppFinder:
    """Windows uygulamalarını dinamik olarak bulur"""
    
    def __init__(self):
        self.app_cache = {}
        self.steam_games = {}
        self._scan_applications()
    
    def _scan_applications(self):
        """Kurulu uygulamaları tara"""
        logger.info("🔍 Uygulamalar taranıyor...")
        
        # 1. Start Menu
        self._scan_start_menu()
        
        # 2. Yaygın uygulamalar
        self._add_common_apps()
        
        # 3. Steam oyunları
        self._scan_steam_games()
        
        logger.info(f"✅ {len(self.app_cache)} uygulama bulundu")
    
    def _scan_start_menu(self):
        """Start Menu'deki kısayolları tara"""
        start_menu_paths = [
            os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
            os.path.join(os.environ['PROGRAMDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
        ]
        
        for base_path in start_menu_paths:
            if not os.path.exists(base_path):
                continue
            
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.endswith('.lnk'):
                        app_name = file.replace('.lnk', '').lower()
                        full_path = os.path.join(root, file)
                        self.app_cache[app_name] = full_path
    
    def _add_common_apps(self):
        """Yaygın uygulamaları ekle"""
        common_apps = {
            # Browsers
            'chrome': 'chrome.exe',
            'google chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe',
            'microsoft edge': 'msedge.exe',
            'opera': 'opera.exe',
            'brave': 'brave.exe',
            
            # Communication
            'discord': 'discord.exe',
            'telegram': 'telegram.exe',
            'whatsapp': 'whatsapp.exe',
            'slack': 'slack.exe',
            'teams': 'teams.exe',
            'zoom': 'zoom.exe',
            'skype': 'skype.exe',
            
            # Development
            'vscode': 'code.exe',
            'visual studio code': 'code.exe',
            'visual studio': 'devenv.exe',
            'pycharm': 'pycharm64.exe',
            'android studio': 'studio64.exe',
            'sublime': 'sublime_text.exe',
            'notepad++': 'notepad++.exe',
            'atom': 'atom.exe',
            'git bash': 'git-bash.exe',
            
            # Office
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'powerpoint': 'powerpnt.exe',
            'outlook': 'outlook.exe',
            'onenote': 'onenote.exe',
            
            # Media
            'spotify': 'spotify.exe',
            'vlc': 'vlc.exe',
            'itunes': 'itunes.exe',
            'windows media player': 'wmplayer.exe',
            'photoshop': 'photoshop.exe',
            'premiere': 'adobe premiere pro.exe',
            'obs': 'obs64.exe',
            'obs studio': 'obs64.exe',
            
            # Gaming
            'steam': 'steam.exe',
            'epic games': 'epicgameslauncher.exe',
            'origin': 'origin.exe',
            'uplay': 'uplay.exe',
            'battle.net': 'battle.net.exe',
            'gog galaxy': 'galaxyclient.exe',
            
            # System
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'hesap makinesi': 'calc.exe',
            'paint': 'mspaint.exe',
            'command prompt': 'cmd.exe',
            'powershell': 'powershell.exe',
            'task manager': 'taskmgr.exe',
            'control panel': 'control.exe',
            'settings': 'ms-settings:',
            
            # Utilities
            'winrar': 'winrar.exe',
            '7zip': '7zFM.exe',
            'ccleaner': 'ccleaner64.exe',
            'malwarebytes': 'mbam.exe',
        }
        
        for name, exe in common_apps.items():
            if name not in self.app_cache:
                self.app_cache[name] = exe
    
    def _scan_steam_games(self):
        """Steam oyunlarını tara"""
        try:
            # Steam path
            steam_paths = [
                r"C:\Program Files (x86)\Steam",
                r"C:\Program Files\Steam",
                os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Steam'),
            ]
            
            for steam_path in steam_paths:
                if not os.path.exists(steam_path):
                    continue
                
                # Steam apps klasörü
                apps_path = os.path.join(steam_path, 'steamapps', 'common')
                if os.path.exists(apps_path):
                    for game_folder in os.listdir(apps_path):
                        game_name = game_folder.lower()
                        game_path = os.path.join(apps_path, game_folder)
                        
                        # Oyun exe'sini bul
                        for file in os.listdir(game_path):
                            if file.endswith('.exe') and not file.startswith('Uninstall'):
                                full_path = os.path.join(game_path, file)
                                self.steam_games[game_name] = full_path
                                self.app_cache[game_name] = full_path
                                break
                    
                    logger.info(f"🎮 {len(self.steam_games)} Steam oyunu bulundu")
                break
                
        except Exception as e:
            logger.warning(f"Steam oyunları taranamadı: {e}")
    
    def find_app(self, app_name):
        """
        Uygulama bul
        
        Args:
            app_name (str): Uygulama adı
            
        Returns:
            str: Uygulama yolu veya komutu
        """
        app_name = app_name.lower().strip()
        
        # Direkt eşleşme
        if app_name in self.app_cache:
            return self.app_cache[app_name]
        
        # Kısmi eşleşme
        for name, path in self.app_cache.items():
            if app_name in name or name in app_name:
                return path
        
        # Bulunamadı
        logger.warning(f"Uygulama bulunamadı: {app_name}")
        return None
    
    def launch_app(self, app_name):
        """Uygulamayı başlat"""
        app_path = self.find_app(app_name)
        
        if not app_path:
            return False
        
        try:
            # .lnk kısayolu
            if app_path.endswith('.lnk'):
                os.startfile(app_path)
            # Exe dosyası
            elif app_path.endswith('.exe'):
                subprocess.Popen(app_path)
            # ms-settings: gibi protokoller
            elif ':' in app_path:
                os.startfile(app_path)
            # Sadece exe adı
            else:
                os.startfile(app_path)
            
            logger.info(f"✅ {app_name} açıldı")
            return True
            
        except Exception as e:
            logger.error(f"Uygulama açılamadı: {e}")
            return False
    
    def close_app(self, app_name):
        """Uygulamayı kapat"""
        app_path = self.find_app(app_name)
        
        if not app_path:
            return False
        
        try:
            # Exe adını al
            if app_path.endswith('.exe'):
                exe_name = os.path.basename(app_path)
            else:
                exe_name = app_path
            
            subprocess.run(['taskkill', '/IM', exe_name, '/F'], 
                         capture_output=True, 
                         timeout=5)
            
            logger.info(f"✅ {app_name} kapatıldı")
            return True
            
        except Exception as e:
            logger.error(f"Uygulama kapatılamadı: {e}")
            return False
    
    def list_apps(self):
        """Tüm uygulamaları listele"""
        return sorted(self.app_cache.keys())
    
    def list_games(self):
        """Steam oyunlarını listele"""
        return sorted(self.steam_games.keys())
