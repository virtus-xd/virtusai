"""
Gelişmiş Uygulama Yönetim Sistemi
- Windows Registry tarama
- Start Menu tarama
- Steam, Epic, GOG oyunları
- Dinamik uygulama bulma
- Akıllı eşleştirme
"""
import os
import logging
import winreg
import subprocess
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class ApplicationMaster:
    """Tüm uygulamaları bulan ve yöneten master sınıf"""
    
    def __init__(self):
        self.app_database = {}
        self.steam_games = {}
        self.epic_games = {}
        self.gog_games = {}
        
        # Cache dosyası
        self.cache_file = Path('data/app_cache.json')
        
        # Uygulamaları yükle veya tara
        if self.cache_file.exists():
            self._load_cache()
        else:
            self.scan_all_applications()
    
    def scan_all_applications(self):
        """Tüm uygulamaları kapsamlı tara"""
        logger.info("🔍 Uygulama taraması başlıyor...")
        
        # 1. Manuel bilinen uygulamalar
        self._add_common_applications()
        
        # 2. Start Menu
        self._scan_start_menu()
        
        # 3. Windows Registry
        self._scan_registry()
        
        # 4. Program Files
        self._scan_program_files()
        
        # 5. Gaming platforms
        self._scan_steam()
        self._scan_epic_games()
        self._scan_gog()
        
        # 6. Kısayolları ekle
        self._add_shortcuts()
        
        logger.info(f"✅ {len(self.app_database)} uygulama bulundu")
        logger.info(f"✅ {len(self.steam_games)} Steam oyunu")
        logger.info(f"✅ {len(self.epic_games)} Epic oyunu")
        
        # Cache'e kaydet
        self._save_cache()
    
    def _add_common_applications(self):
        """Yaygın uygulamalar - garantili liste"""
        common_apps = {
            # Browsers
            'chrome': {'exe': 'chrome.exe', 'names': ['chrome', 'google chrome']},
            'firefox': {'exe': 'firefox.exe', 'names': ['firefox', 'mozilla firefox']},
            'edge': {'exe': 'msedge.exe', 'names': ['edge', 'microsoft edge']},
            'opera': {'exe': 'opera.exe', 'names': ['opera']},
            'brave': {'exe': 'brave.exe', 'names': ['brave']},
            
            # Communication
            'discord': {'exe': 'Discord.exe', 'names': ['discord']},
            'telegram': {'exe': 'Telegram.exe', 'names': ['telegram']},
            'whatsapp': {'exe': 'WhatsApp.exe', 'names': ['whatsapp']},
            'slack': {'exe': 'slack.exe', 'names': ['slack']},
            'teams': {'exe': 'Teams.exe', 'names': ['teams', 'microsoft teams']},
            'zoom': {'exe': 'Zoom.exe', 'names': ['zoom']},
            'skype': {'exe': 'Skype.exe', 'names': ['skype']},
            
            # Development
            'vscode': {'exe': 'Code.exe', 'names': ['vscode', 'visual studio code', 'code']},
            'visual studio': {'exe': 'devenv.exe', 'names': ['visual studio']},
            'pycharm': {'exe': 'pycharm64.exe', 'names': ['pycharm']},
            'intellij': {'exe': 'idea64.exe', 'names': ['intellij', 'intellij idea']},
            'android studio': {'exe': 'studio64.exe', 'names': ['android studio']},
            'sublime': {'exe': 'sublime_text.exe', 'names': ['sublime', 'sublime text']},
            'notepad++': {'exe': 'notepad++.exe', 'names': ['notepad++', 'notepad plus']},
            'atom': {'exe': 'atom.exe', 'names': ['atom']},
            'git bash': {'exe': 'git-bash.exe', 'names': ['git bash', 'git']},
            'github desktop': {'exe': 'GitHubDesktop.exe', 'names': ['github desktop', 'github']},
            
            # Office
            'word': {'exe': 'WINWORD.EXE', 'names': ['word', 'microsoft word']},
            'excel': {'exe': 'EXCEL.EXE', 'names': ['excel', 'microsoft excel']},
            'powerpoint': {'exe': 'POWERPNT.EXE', 'names': ['powerpoint', 'microsoft powerpoint']},
            'outlook': {'exe': 'OUTLOOK.EXE', 'names': ['outlook', 'microsoft outlook']},
            'onenote': {'exe': 'ONENOTE.EXE', 'names': ['onenote', 'microsoft onenote']},
            
            # Media & Creative
            'spotify': {'exe': 'Spotify.exe', 'names': ['spotify']},
            'vlc': {'exe': 'vlc.exe', 'names': ['vlc', 'vlc media player']},
            'itunes': {'exe': 'iTunes.exe', 'names': ['itunes']},
            'photoshop': {'exe': 'Photoshop.exe', 'names': ['photoshop', 'adobe photoshop']},
            'premiere': {'exe': 'Adobe Premiere Pro.exe', 'names': ['premiere', 'adobe premiere']},
            'after effects': {'exe': 'AfterFX.exe', 'names': ['after effects', 'adobe after effects']},
            'illustrator': {'exe': 'Illustrator.exe', 'names': ['illustrator', 'adobe illustrator']},
            'obs': {'exe': 'obs64.exe', 'names': ['obs', 'obs studio']},
            'audacity': {'exe': 'audacity.exe', 'names': ['audacity']},
            'gimp': {'exe': 'gimp-2.10.exe', 'names': ['gimp']},
            
            # Gaming Platforms
            'steam': {'exe': 'steam.exe', 'names': ['steam']},
            'epic games': {'exe': 'EpicGamesLauncher.exe', 'names': ['epic', 'epic games']},
            'origin': {'exe': 'Origin.exe', 'names': ['origin']},
            'uplay': {'exe': 'uplay.exe', 'names': ['uplay', 'ubisoft connect']},
            'battle.net': {'exe': 'Battle.net.exe', 'names': ['battle.net', 'battlenet', 'blizzard']},
            'gog galaxy': {'exe': 'GalaxyClient.exe', 'names': ['gog', 'gog galaxy']},
            'ea app': {'exe': 'EADesktop.exe', 'names': ['ea app', 'ea']},
            
            # System Tools
            'notepad': {'exe': 'notepad.exe', 'names': ['notepad', 'not defteri']},
            'calculator': {'exe': 'calc.exe', 'names': ['calculator', 'hesap makinesi']},
            'paint': {'exe': 'mspaint.exe', 'names': ['paint', 'resim']},
            'cmd': {'exe': 'cmd.exe', 'names': ['cmd', 'command prompt', 'komut istemi']},
            'powershell': {'exe': 'powershell.exe', 'names': ['powershell']},
            'task manager': {'exe': 'taskmgr.exe', 'names': ['task manager', 'görev yöneticisi']},
            'control panel': {'exe': 'control.exe', 'names': ['control panel', 'denetim masası']},
            'settings': {'exe': 'ms-settings:', 'names': ['settings', 'ayarlar']},
            'explorer': {'exe': 'explorer.exe', 'names': ['explorer', 'dosya gezgini', 'file explorer']},
            
            # Utilities
            'winrar': {'exe': 'WinRAR.exe', 'names': ['winrar']},
            '7zip': {'exe': '7zFM.exe', 'names': ['7zip', '7-zip']},
            'ccleaner': {'exe': 'CCleaner64.exe', 'names': ['ccleaner']},
            'malwarebytes': {'exe': 'mbam.exe', 'names': ['malwarebytes']},
            'vmware': {'exe': 'vmware.exe', 'names': ['vmware']},
            'virtualbox': {'exe': 'VirtualBox.exe', 'names': ['virtualbox']},
            'anydesk': {'exe': 'AnyDesk.exe', 'names': ['anydesk']},
            'teamviewer': {'exe': 'TeamViewer.exe', 'names': ['teamviewer']},
        }
        
        for app_id, data in common_apps.items():
            self.app_database[app_id] = {
                'exe': data['exe'],
                'names': data['names'],
                'type': 'common'
            }
    
    def _scan_start_menu(self):
        """Start Menu kısayollarını tara"""
        start_paths = [
            Path(os.environ['APPDATA']) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs',
            Path(os.environ['PROGRAMDATA']) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs'
        ]
        
        for base_path in start_paths:
            if not base_path.exists():
                continue
            
            for lnk_file in base_path.rglob('*.lnk'):
                app_name = lnk_file.stem.lower()
                
                # Gereksiz kısayolları atla
                skip_keywords = ['uninstall', 'readme', 'help', 'documentation']
                if any(kw in app_name for kw in skip_keywords):
                    continue
                
                self.app_database[app_name] = {
                    'exe': str(lnk_file),
                    'names': [app_name],
                    'type': 'shortcut'
                }
    
    def _scan_registry(self):
        """Windows Registry'den uygulamaları oku"""
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'),
            (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'),
        ]
        
        for hkey, subkey_path in registry_paths:
            try:
                with winreg.OpenKey(hkey, subkey_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                                
                                # Exe yolunu bul
                                try:
                                    install_location = winreg.QueryValueEx(subkey, 'InstallLocation')[0]
                                    if install_location:
                                        app_id = name.lower()
                                        self.app_database[app_id] = {
                                            'exe': install_location,
                                            'names': [app_id],
                                            'type': 'registry'
                                        }
                                except:
                                    pass
                        except:
                            continue
            except Exception as e:
                logger.debug(f"Registry okuma hatası: {e}")
    
    def _scan_program_files(self):
        """Program Files klasörlerini tara"""
        program_dirs = [
            Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')),
            Path(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'))
        ]
        
        for base_dir in program_dirs:
            if not base_dir.exists():
                continue
            
            for app_dir in base_dir.iterdir():
                if not app_dir.is_dir():
                    continue
                
                # Exe dosyalarını ara
                for exe_file in app_dir.rglob('*.exe'):
                    # Ana exe olabilecekleri seç
                    if exe_file.parent == app_dir or 'bin' in exe_file.parts:
                        app_name = app_dir.name.lower()
                        
                        if app_name not in self.app_database:
                            self.app_database[app_name] = {
                                'exe': str(exe_file),
                                'names': [app_name],
                                'type': 'program_files'
                            }
                        break
    
    def _scan_steam(self):
        """Steam oyunlarını tara"""
        steam_paths = [
            Path('C:/Program Files (x86)/Steam'),
            Path('C:/Program Files/Steam'),
            Path(os.environ.get('PROGRAMFILES(X86)', '')) / 'Steam',
        ]
        
        for steam_path in steam_paths:
            if not steam_path.exists():
                continue
            
            steamapps = steam_path / 'steamapps' / 'common'
            if not steamapps.exists():
                continue
            
            for game_dir in steamapps.iterdir():
                if not game_dir.is_dir():
                    continue
                
                game_name = game_dir.name.lower()
                
                # Exe bul
                for exe_file in game_dir.rglob('*.exe'):
                    # Uninstall değilse
                    if 'unins' not in exe_file.name.lower():
                        self.steam_games[game_name] = str(exe_file)
                        self.app_database[f"steam_{game_name}"] = {
                            'exe': str(exe_file),
                            'names': [game_name, f"steam {game_name}"],
                            'type': 'steam_game'
                        }
                        break
            
            logger.info(f"🎮 {len(self.steam_games)} Steam oyunu bulundu")
            break
    
    def _scan_epic_games(self):
        """Epic Games oyunlarını tara"""
        epic_path = Path(os.environ['PROGRAMDATA']) / 'Epic' / 'EpicGamesLauncher' / 'Data' / 'Manifests'
        
        if not epic_path.exists():
            return
        
        for manifest_file in epic_path.glob('*.item'):
            try:
                import json
                with open(manifest_file, 'r') as f:
                    data = json.load(f)
                    game_name = data.get('DisplayName', '').lower()
                    install_location = data.get('InstallLocation', '')
                    
                    if game_name and install_location:
                        self.epic_games[game_name] = install_location
                        self.app_database[f"epic_{game_name}"] = {
                            'exe': install_location,
                            'names': [game_name, f"epic {game_name}"],
                            'type': 'epic_game'
                        }
            except:
                continue
        
        if self.epic_games:
            logger.info(f"🎮 {len(self.epic_games)} Epic oyunu bulundu")
    
    def _scan_gog(self):
        """GOG oyunlarını tara"""
        gog_path = Path(os.environ['PROGRAMDATA']) / 'GOG.com' / 'Galaxy' / 'storage'
        
        if not gog_path.exists():
            return
        
        # GOG tarama mantığı buraya eklenebilir
        pass
    
    def _add_shortcuts(self):
        """Özel kısayollar ekle"""
        shortcuts = {
            'youtube': {'exe': 'https://www.youtube.com', 'names': ['youtube']},
            'gmail': {'exe': 'https://mail.google.com', 'names': ['gmail', 'mail']},
            'drive': {'exe': 'https://drive.google.com', 'names': ['drive', 'google drive']},
            'twitter': {'exe': 'https://twitter.com', 'names': ['twitter', 'x']},
            'instagram': {'exe': 'https://instagram.com', 'names': ['instagram']},
            'facebook': {'exe': 'https://facebook.com', 'names': ['facebook']},
            'netflix': {'exe': 'https://netflix.com', 'names': ['netflix']},
        }
        
        for app_id, data in shortcuts.items():
            self.app_database[app_id] = {
                'exe': data['exe'],
                'names': data['names'],
                'type': 'web'
            }
    
    def find_application(self, query):
        """
        Uygulamayı akıllı şekilde bul
        
        Args:
            query: Aranacak uygulama adı
            
        Returns:
            dict: Uygulama bilgisi veya None
        """
        query = query.lower().strip()
        
        # 1. Tam eşleşme
        if query in self.app_database:
            return self.app_database[query]
        
        # 2. İsim eşleşmesi
        for app_id, app_data in self.app_database.items():
            if query in app_data['names']:
                return app_data
        
        # 3. Kısmi eşleşme
        for app_id, app_data in self.app_database.items():
            # Query, app isminin içinde mi?
            if query in app_id:
                return app_data
            
            # Query, alternatif isimlerin içinde mi?
            for name in app_data['names']:
                if query in name or name in query:
                    return app_data
        
        # 4. Fuzzy matching (benzer isimler)
        best_match = None
        best_score = 0
        
        for app_id, app_data in self.app_database.items():
            score = self._fuzzy_match(query, app_id)
            if score > best_score and score > 0.7:
                best_score = score
                best_match = app_data
        
        return best_match
    
    def _fuzzy_match(self, query, target):
        """Basit fuzzy matching"""
        query = query.lower()
        target = target.lower()
        
        # Aynıysa
        if query == target:
            return 1.0
        
        # İçeriyorsa
        if query in target or target in query:
            return 0.9
        
        # Karakter benzerliği
        common_chars = sum(1 for c in query if c in target)
        similarity = common_chars / max(len(query), len(target))
        
        return similarity
    
    def launch_application(self, query):
        """
        Uygulamayı başlat
        
        Args:
            query: Uygulama adı
            
        Returns:
            bool: Başarılı ise True
        """
        app_data = self.find_application(query)
        
        if not app_data:
            logger.warning(f"Uygulama bulunamadı: {query}")
            return False
        
        exe_path = app_data['exe']
        
        try:
            if exe_path.startswith('http'):
                # Web URL
                import webbrowser
                webbrowser.open(exe_path)
            elif exe_path.endswith('.lnk'):
                # Kısayol
                os.startfile(exe_path)
            elif exe_path.startswith('ms-'):
                # MS protokol
                os.startfile(exe_path)
            else:
                # Normal exe
                subprocess.Popen(exe_path)
            
            logger.info(f"✅ Başlatıldı: {query}")
            return True
            
        except Exception as e:
            logger.error(f"Başlatma hatası: {e}")
            return False
    
    def close_application(self, query):
        """Uygulamayı kapat"""
        app_data = self.find_application(query)
        
        if not app_data:
            return False
        
        exe_path = app_data['exe']
        exe_name = Path(exe_path).name if not exe_path.startswith('http') else None
        
        if not exe_name:
            return False
        
        try:
            subprocess.run(['taskkill', '/IM', exe_name, '/F'], 
                         capture_output=True, timeout=5)
            logger.info(f"✅ Kapatıldı: {query}")
            return True
        except:
            return False
    
    def _save_cache(self):
        """Cache'e kaydet"""
        try:
            os.makedirs('data', exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'apps': self.app_database,
                    'steam': self.steam_games,
                    'epic': self.epic_games
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Cache kaydetme hatası: {e}")
    
    def _load_cache(self):
        """Cache'den yükle"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.app_database = data.get('apps', {})
                self.steam_games = data.get('steam', {})
                self.epic_games = data.get('epic', {})
            
            logger.info(f"✅ Cache yüklendi: {len(self.app_database)} uygulama")
        except Exception as e:
            logger.error(f"Cache yükleme hatası: {e}")
            self.scan_all_applications()


# Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🔍 Uygulama taraması başlıyor...")
    master = ApplicationMaster()
    
    print(f"\n✅ Toplam {len(master.app_database)} uygulama bulundu")
    print(f"🎮 Steam: {len(master.steam_games)} oyun")
    
    # Örnekler
    test_apps = ['chrome', 'steam', 'discord', 'vscode', 'counter-strike']
    
    print("\n🧪 Test Aramaları:")
    for app in test_apps:
        result = master.find_application(app)
        if result:
            print(f"  ✅ {app}: {result['exe']}")
        else:
            print(f"  ❌ {app}: Bulunamadı")