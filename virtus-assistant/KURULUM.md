# VIRTUS Kurulum Rehberi

## 1. Gereksinimler

- Python 3.8 veya üzeri
- Mikrofon (ses girişi için)
- İnternet bağlantısı (Gemini API için)
- Windows 10/11 (şu an için)

## 2. Kurulum Adımları

### Adım 1: Repository'yi klonlayın veya indirin

```bash
cd virtus-assistant
```

### Adım 2: Virtual environment oluşturun (önerilen)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### Adım 3: Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

**Not:** PyAudio kurulumu sorun çıkarırsa:
```bash
pip install pipwin
pipwin install pyaudio
```

### Adım 4: Google Gemini API Key alın

1. https://makersuite.google.com/app/apikey adresine gidin
2. "Create API Key" butonuna tıklayın
3. API key'i kopyalayın

### Adım 5: Kurulum scriptini çalıştırın

```bash
python setup.py
```

Bu script:
- `.env` dosyasını oluşturur
- Bağımlılıkları kontrol eder
- Mikrofon ve TTS testleri yapar

### Adım 6: `.env` dosyasını düzenleyin

```env
GOOGLE_API_KEY=sizin_api_keyiniz
PORCUPINE_ACCESS_KEY=  # Opsiyonel
WAKE_WORD=virtus
LANGUAGE=tr-TR
VOICE_RATE=150
```

## 3. Çalıştırma

### Normal Mod (Wake Word ile)

```bash
python main.py
```

"Virtus" diyerek asistanı uyandırın ve komutunuzu verin.

### Test Modu (Manuel)

```bash
python main.py --test
```

Komutları klavyeden yazarak test edin.

## 4. Örnek Komutlar

```
Virtus, Chrome'u aç
Virtus, Mehmet'i ara
Virtus, ses seviyesini 50 yap
Virtus, ekranı kilitle
Virtus, 5+7 kaç eder?
Virtus, hava durumu nasıl?
Virtus, YouTube'da müzik aç
```

## 5. Telefon Entegrasyonu (Android)

### ADB Kurulumu (PC'den telefon kontrolü için)

1. Android SDK Platform Tools'u indirin:
   https://developer.android.com/studio/releases/platform-tools

2. PATH'e ekleyin

3. Telefonunuzda USB Debugging'i açın:
   - Ayarlar > Telefon Hakkında > Yapı Numarası'na 7 kez dokunun
   - Geliştirici Seçenekleri > USB Debugging'i açın

4. Telefonu USB ile bağlayın ve test edin:
   ```bash
   adb devices
   ```

### Kişi Ekleme

`data/contacts.json` dosyasını düzenleyin:

```json
{
  "Mehmet": {
    "phone": "+905551234567",
    "email": "mehmet@example.com"
  }
}
```

## 6. Android App (Gelecek Özellik)

Kivy ile cross-platform mobil uygulama yapılabilir:

```bash
pip install kivy plyer buildozer
```

## 7. Akıllı Saat Entegrasyonu

- Wear OS için Google Assistant API kullanılabilir
- Bluetooth üzerinden bildirim ve komut alışverişi

## 8. Sorun Giderme

### Mikrofon çalışmıyor
- Mikrofon izinlerini kontrol edin
- Varsayılan mikrofonu Windows ayarlarından seçin

### TTS sesi yok
- Ses sürücülerini güncelleyin
- Türkçe ses paketi yükleyin (Windows TTS)

### API hatası
- Internet bağlantınızı kontrol edin
- Google API key'in geçerli olduğundan emin olun
- API kotanızı kontrol edin

### PyAudio kurulum hatası
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# Linux
sudo apt-get install portaudio19-dev python3-pyaudio

# Mac
brew install portaudio
pip install pyaudio
```

## 9. Gelişmiş Özellikler

### Custom Wake Word

Picovoice Console'dan custom wake word oluşturun:
1. https://console.picovoice.ai/
2. "Virtus" kelimesi için .ppn dosyası oluşturun
3. `data/` klasörüne kaydedin
4. `wake_word_detector.py`'yi güncelleyin

### Ses Tanıma İyileştirme

Daha iyi sonuç için OpenAI Whisper kullanabilirsiniz:

```bash
pip install openai-whisper
```

## 10. Katkıda Bulunma

Bu bir kişisel proje, dilediğiniz gibi özelleştirin!

## 11. Lisans

MIT License - Özgürce kullanın ve geliştirin!
