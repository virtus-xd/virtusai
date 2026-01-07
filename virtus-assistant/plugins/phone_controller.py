"""
Telefon Kontrolü - Android entegrasyonu
Kivy + Plyer kullanarak Android fonksiyonları
"""
import logging

logger = logging.getLogger(__name__)

try:
    # Android için
    from plyer import call, sms, notification, vibrator
    PHONE_AVAILABLE = True
except ImportError:
    PHONE_AVAILABLE = False
    logger.warning("Plyer modülü bulunamadı - telefon özellikleri devre dışı")


class PhoneController:
    """Telefon işlemleri kontrolcüsü"""
    
    def __init__(self):
        self.available = PHONE_AVAILABLE
    
    def make_call(self, phone_number):
        """Telefon araması yap"""
        if not self.available:
            logger.error("Telefon özellikleri kullanılamıyor")
            return False
        
        try:
            call.makecall(tel=phone_number)
            logger.info(f"📞 Arama yapılıyor: {phone_number}")
            return True
        except Exception as e:
            logger.error(f"Arama hatası: {e}")
            return False
    
    def send_sms(self, phone_number, message):
        """SMS gönder"""
        if not self.available:
            logger.error("Telefon özellikleri kullanılamıyor")
            return False
        
        try:
            sms.send(recipient=phone_number, message=message)
            logger.info(f"📱 SMS gönderildi: {phone_number}")
            return True
        except Exception as e:
            logger.error(f"SMS hatası: {e}")
            return False
    
    def show_notification(self, title, message):
        """Bildirim göster"""
        if not self.available:
            logger.error("Telefon özellikleri kullanılamıyor")
            return False
        
        try:
            notification.notify(
                title=title,
                message=message,
                app_name='Virtus',
                timeout=10
            )
            return True
        except Exception as e:
            logger.error(f"Bildirim hatası: {e}")
            return False
    
    def vibrate(self, duration=0.5):
        """Telefonu titret"""
        if not self.available:
            return False
        
        try:
            vibrator.vibrate(time=duration)
            return True
        except Exception as e:
            logger.error(f"Titreşim hatası: {e}")
            return False


# PC için alternatif - ADB kullanarak Android kontrolü
class ADBPhoneController:
    """
    ADB (Android Debug Bridge) kullanarak telefon kontrolü
    Telefon USB ile bağlı veya WiFi üzerinden bağlanabilir
    """
    
    def __init__(self):
        self.adb_available = self._check_adb()
    
    def _check_adb(self):
        """ADB kurulu mu kontrol et"""
        import subprocess
        try:
            result = subprocess.run(['adb', 'version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=2)
            return result.returncode == 0
        except:
            return False
    
    def make_call(self, phone_number):
        """ADB ile arama yap"""
        if not self.adb_available:
            return False
        
        try:
            import subprocess
            cmd = f'adb shell am start -a android.intent.action.CALL -d tel:{phone_number}'
            subprocess.run(cmd.split(), timeout=5)
            logger.info(f"📞 ADB ile arama: {phone_number}")
            return True
        except Exception as e:
            logger.error(f"ADB arama hatası: {e}")
            return False
    
    def send_sms(self, phone_number, message):
        """ADB ile SMS gönder"""
        if not self.adb_available:
            return False
        
        try:
            import subprocess
            cmd = f'adb shell service call isms 5 i32 0 s16 "com.android.mms" s16 "{phone_number}" s16 "null" s16 "{message}" s16 "null" s16 "null"'
            subprocess.run(cmd, shell=True, timeout=5)
            logger.info(f"📱 ADB ile SMS: {phone_number}")
            return True
        except Exception as e:
            logger.error(f"ADB SMS hatası: {e}")
            return False
    
    def open_app(self, package_name):
        """Android uygulaması aç"""
        if not self.adb_available:
            return False
        
        try:
            import subprocess
            cmd = f'adb shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1'
            subprocess.run(cmd.split(), timeout=5)
            return True
        except Exception as e:
            logger.error(f"Uygulama açma hatası: {e}")
            return False


# Contacts veritabanı
class ContactManager:
    """Kişi yönetimi - isimden telefon numarası bul"""
    
    def __init__(self):
        self.contacts = self._load_contacts()
    
    def _load_contacts(self):
        """Kişileri yükle (basit JSON dosyası)"""
        import json
        import os
        
        contacts_file = 'data/contacts.json'
        
        if os.path.exists(contacts_file):
            try:
                with open(contacts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        
        # Varsayılan boş
        return {}
    
    def save_contacts(self):
        """Kişileri kaydet"""
        import json
        import os
        
        os.makedirs('data', exist_ok=True)
        
        with open('data/contacts.json', 'w', encoding='utf-8') as f:
            json.dump(self.contacts, f, ensure_ascii=False, indent=2)
    
    def find_contact(self, name):
        """İsimden kişi bul"""
        # Büyük/küçük harf duyarsız arama
        name_lower = name.lower()
        
        for contact_name, contact_data in self.contacts.items():
            if name_lower in contact_name.lower():
                return contact_data
        
        return None
    
    def add_contact(self, name, phone_number, email=None):
        """Yeni kişi ekle"""
        self.contacts[name] = {
            'phone': phone_number,
            'email': email
        }
        self.save_contacts()
    
    def get_phone_number(self, name):
        """İsimden telefon numarası al"""
        contact = self.find_contact(name)
        if contact:
            return contact.get('phone')
        return None
