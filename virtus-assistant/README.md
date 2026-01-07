# VIRTUS - AI Asistan Sistemi

JARVIS tarzı, çoklu platform destekli akıllı asistan.

## Özellikler

- 🎤 Wake Word Detection: "Virtus" komutu ile aktivasyon
- 🗣️ Sesli Komut Tanıma
- 🧠 Google Gemini AI Entegrasyonu
- 📱 Multi-Platform: PC, Telefon, Akıllı Saat
- ⚡ Sistem Kontrolü: Arama, uygulama yönetimi, dosya işlemleri
- 🔊 Text-to-Speech yanıtlar

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

```bash
python main.py
```

## Yapı

```
virtus-assistant/
├── core/           # Ana sistem bileşenleri
├── modules/        # Wake word, STT, TTS modülleri
├── plugins/        # Platform-specific işlevler
├── config/         # Ayarlar
└── data/           # Model ve veri dosyaları
```

## API Keys

`.env` dosyası oluşturup API anahtarlarınızı ekleyin:
```
GOOGLE_API_KEY=your_gemini_api_key
```
