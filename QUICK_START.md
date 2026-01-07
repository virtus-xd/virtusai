# 🚀 VIRTUS - Hızlı Başlangıç

## ⚡ 5 Dakikada Başla

### 1️⃣ Kurulum (İlk Kez)

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Kurulum scriptini çalıştır
python setup.py
```

Google API Key'inizi girmeniz istenecek:
- https://makersuite.google.com/app/apikey
- "Create API Key" → Kopyala → Yapıştır

### 2️⃣ Test Et

```bash
# Klavyeden komut yazarak test et
python main.py --test
```

Örnek komutlar:
```
Chrome'u aç
Mehmet'i ara
ses seviyesini 75 yap
5+7 kaç eder?
```

### 3️⃣ Canlı Kullan

```bash
# Wake word ile çalıştır
python main.py
```

**"Virtus"** diyerek uyandırın, sonra komutunuzu verin!

---

## 📱 Telefon İçin

### Windows PC'den Android Kontrolü (ADB)

```bash
# 1. ADB kur
# https://developer.android.com/studio/releases/platform-tools

# 2. Telefonunuzu USB ile bağla

# 3. USB Debugging'i aç
# Ayarlar > Geliştirici Seçenekleri > USB Debugging

# 4. Test et
adb devices

# 5. Virtus'u çalıştır - artık arama yapabilir!
```

### Kişi Ekle

`data/contacts.json`:
```json
{
  "Annem": {
    "phone": "+905551234567"
  }
}
```

---

## 🎯 Komut Örnekleri

### 💻 Uygulama Kontrolü
```
Virtus, Chrome'u aç
Virtus, Calculator'ı aç
Virtus, Spotify'ı çalıştır
```

### 📞 Arama
```
Virtus, Mehmet'i ara
Virtus, annem'i ara
```

### 🔧 Sistem Kontrolü
```
Virtus, ses seviyesini 50 yap
Virtus, sesi kapat
Virtus, ekranı kilitle
Virtus, bilgisayarı kapat
```

### 🔍 Web Araması
```
Virtus, Python tutorial ara
Virtus, YouTube'da müzik aç
```

### 🧮 Hesaplama
```
Virtus, 15 çarpı 23 kaç eder?
Virtus, 100'ün yüzde 15'i ne kadar?
```

### 💬 Sohbet
```
Virtus, hava durumu nasıl?
Virtus, Türkiye'nin başkenti neresi?
Virtus, bir şaka anlat
```

---

## ⚙️ Ayarlar

### Konuşma Hızını Değiştir

`.env` dosyasında:
```env
VOICE_RATE=150  # Varsayılan
VOICE_RATE=120  # Yavaş
VOICE_RATE=180  # Hızlı
```

### Wake Word Değiştir

`.env` dosyasında:
```env
WAKE_WORD=jarvis
# veya
WAKE_WORD=hey virtus
```

---

## 🐛 Sorun mu var?

### Mikrofon çalışmıyor
```bash
# Test et
python setup.py
```

### API hatası
```bash
# .env dosyasını kontrol et
notepad .env

# API key'i yeniden gir
GOOGLE_API_KEY=your_key_here
```

### PyAudio kurulmuyor
```bash
pip install pipwin
pipwin install pyaudio
```

---

## 🎨 Özelleştir

### Yeni Uygulama Ekle

`core/action_executor.py`:
```python
self.app_mappings = {
    'vscode': 'code.exe',
    'photoshop': 'photoshop.exe',
    # Yeni uygulamalarınızı buraya
}
```

### Yeni Komut Ekle

Virtus zaten akıllı! Gemini API sayesinde doğal dille yeni komutları anlayabilir.

Sadece söyleyin:
```
Virtus, yarın saat 9'da beni uyandır
Virtus, masaüstünde yeni klasör oluştur
Virtus, bu şarkının adı ne?
```

---

## 🌟 Pro İpuçları

1. **Daha hızlı yanıt** için `VOICE_RATE`'i artırın
2. **Gürültülü ortamda** mikrofon sensitivitesini ayarlayın
3. **Offline çalışma** için local Whisper kullanın
4. **Custom wake word** için Porcupine Console'u kullanın

---

## 📚 Daha Fazlası

- `KURULUM.md` - Detaylı kurulum
- `README.md` - Proje hakkında
- `main.py --help` - Komut satırı yardımı

---

## 💡 Fikir & Öneri?

Bu sizin asistanınız! Özgürce geliştirin ve paylaşın.

**Keyifli kullanımlar! 🚀**
