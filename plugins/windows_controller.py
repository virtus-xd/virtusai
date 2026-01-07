"""
Windows Sistem Kontrolü
"""
import logging
import subprocess
import os

logger = logging.getLogger(__name__)

try:
    import win32api
    import win32con
    import win32gui
    WINDOWS_API_AVAILABLE = True
except ImportError:
    WINDOWS_API_AVAILABLE = False
    logger.warning("pywin32 bulunamadı - bazı Windows özellikleri devre dışı")


class WindowsController:
    """Windows sistem kontrolü"""
    
    def __init__(self):
        self.available = WINDOWS_API_AVAILABLE
    
    def set_volume(self, level):
        """Ses seviyesini ayarla (0-100)"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # 0.0 - 1.0 arası
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            logger.info(f"🔊 Ses seviyesi: {level}%")
            return True
            
        except Exception as e:
            logger.error(f"Ses ayarlama hatası: {e}")
            return False
    
    def get_volume(self):
        """Mevcut ses seviyesini al"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            current_volume = volume.GetMasterVolumeLevelScalar()
            return int(current_volume * 100)
            
        except Exception as e:
            logger.error(f"Ses okuma hatası: {e}")
            return None
    
    def mute(self):
        """Sesi kapat"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            volume.SetMute(1, None)
            logger.info("🔇 Ses kapatıldı")
            return True
            
        except Exception as e:
            logger.error(f"Mute hatası: {e}")
            return False
    
    def unmute(self):
        """Sesi aç"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            volume.SetMute(0, None)
            logger.info("🔊 Ses açıldı")
            return True
            
        except Exception as e:
            logger.error(f"Unmute hatası: {e}")
            return False
    
    def set_brightness(self, level):
        """Ekran parlaklığını ayarla (0-100)"""
        try:
            # Windows WMI kullanarak
            import wmi
            c = wmi.WMI(namespace='wmi')
            methods = c.WmiMonitorBrightnessMethods()[0]
            methods.WmiSetBrightness(level, 0)
            logger.info(f"💡 Parlaklık: {level}%")
            return True
        except Exception as e:
            logger.error(f"Parlaklık ayarlama hatası: {e}")
            return False
    
    def shutdown(self, delay_seconds=60):
        """Bilgisayarı kapat"""
        try:
            subprocess.run(['shutdown', '/s', '/t', str(delay_seconds)])
            logger.info(f"💤 Kapatma başlatıldı ({delay_seconds}s)")
            return True
        except Exception as e:
            logger.error(f"Kapatma hatası: {e}")
            return False
    
    def restart(self, delay_seconds=60):
        """Bilgisayarı yeniden başlat"""
        try:
            subprocess.run(['shutdown', '/r', '/t', str(delay_seconds)])
            logger.info(f"🔄 Yeniden başlatma ({delay_seconds}s)")
            return True
        except Exception as e:
            logger.error(f"Yeniden başlatma hatası: {e}")
            return False
    
    def cancel_shutdown(self):
        """Kapatma/yeniden başlatmayı iptal et"""
        try:
            subprocess.run(['shutdown', '/a'])
            logger.info("✅ Kapatma iptal edildi")
            return True
        except Exception as e:
            logger.error(f"İptal hatası: {e}")
            return False
    
    def lock_screen(self):
        """Ekranı kilitle"""
        try:
            subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
            logger.info("🔒 Ekran kilitlendi")
            return True
        except Exception as e:
            logger.error(f"Kilitleme hatası: {e}")
            return False
    
    def sleep(self):
        """Uyku moduna geç"""
        try:
            subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'])
            logger.info("😴 Uyku modu")
            return True
        except Exception as e:
            logger.error(f"Uyku modu hatası: {e}")
            return False
    
    def get_active_window_title(self):
        """Aktif pencere başlığını al"""
        if not self.available:
            return None
        
        try:
            window = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(window)
            return title
        except Exception as e:
            logger.error(f"Pencere başlığı hatası: {e}")
            return None
    
    def minimize_all_windows(self):
        """Tüm pencereleri minimize et (Win+D)"""
        try:
            import pyautogui
            pyautogui.hotkey('win', 'd')
            logger.info("📊 Masaüstü gösteriliyor")
            return True
        except Exception as e:
            logger.error(f"Minimize hatası: {e}")
            return False
