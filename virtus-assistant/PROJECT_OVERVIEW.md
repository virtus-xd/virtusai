# VIRTUS AI ASISTAN - Proje Genel Bakış

## 📋 Proje Özeti

**VIRTUS**, JARVIS tarzı, çok platformlu bir AI asistanıdır. Google Gemini AI ile güçlendirilmiş, doğal dil işleme yeteneklerine sahip, bilgisayar, telefon ve akıllı saat üzerinde çalışabilen bir sistemdir.

## 🎯 Temel Özellikler

### ✅ Şu An Çalışan

- ✅ Wake word detection ("Virtus" ile aktivasyon)
- ✅ Türkçe ses tanıma (Speech Recognition)
- ✅ Google Gemini AI entegrasyonu
- ✅ Doğal dil komut işleme
- ✅ Text-to-Speech yanıtlar
- ✅ Windows uygulama kontrolü
- ✅ Web araması
- ✅ Hesaplama ve bilgi sorgulama
- ✅ Sistem kontrolü (ses, ekran, güç)
- ✅ Kişi yönetimi

### 🚧 Geliştirme Aşamasında

- 🚧 Android telefon entegrasyonu (ADB ile)
- 🚧 Custom wake word modeli
- 🚧 Dosya işlemleri
- 🚧 E-posta gönderme
- 🚧 Hatırlatıcılar ve zamanlayıcılar
- 🚧 Müzik kontrolü

### 📱 Gelecek Özellikler

- 📱 Native Android app (Kivy)
- 📱 iOS desteği
- ⌚ Akıllı saat entegrasyonu
- 🏠 Smart home kontrolü
- 🌐 Multi-device senkronizasyon
- 🎨 GUI arayüzü
- 🔐 Sesli kimlik doğrulama

## 🏗️ Mimari

```
┌─────────────────────────────────────────────┐
│             VIRTUS MAIN SYSTEM              │
└─────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼────┐   ┌────▼────┐  ┌────▼────┐
   │  WAKE   │   │ SPEECH  │  │   TTS   │
   │  WORD   │   │  RECOG  │  │ ENGINE  │
   └─────────┘   └─────────┘  └─────────┘
                      │
                 ┌────▼────┐
                 │   AI    │
                 │ BRAIN   │◄──── Google Gemini
                 │ (NLP)   │
                 └────┬────┘
                      │
              ┌───────┴───────┐
              │               │
         ┌────▼────┐    ┌────▼────┐
         │ ACTION  │    │ PLUGINS │
         │EXECUTOR │    │ SYSTEM  │
         └────┬────┘    └────┬────┘
              │               │
    ┌─────────┼───────────────┼─────────┐
    │         │               │         │
┌───▼───┐ ┌──▼───┐      ┌────▼────┐ ┌──▼───┐
│  PC   │ │Phone │      │ Windows │ │ Web  │
│  Apps │ │ Call │      │ Control │ │Search│
└───────┘ └──────┘      └─────────┘ └──────┘
```

## 📂 Dosya Yapısı

```
virtus-assistant/
│
├── main.py                 # Ana giriş noktası
├── setup.py                # Kurulum scripti
├── demo.py                 # Demo ve test
├── mobile_app.py           # Mobil uygulama (Kivy)
│
├── config/
│   └── settings.py         # Tüm ayarlar
│
├── core/
│   ├── virtus.py           # Ana asistan sınıfı
│   ├── ai_brain.py         # Gemini AI entegrasyonu
│   └── action_executor.py  # Komutları çalıştırır
│
├── modules/
│   ├── wake_word_detector.py      # Wake word
│   ├── speech_recognition_module.py # STT
│   └── text_to_speech.py          # TTS
│
├── plugins/
│   ├── phone_controller.py        # Telefon kontrolü
│   └── windows_controller.py      # Windows sistem kontrolü
│
└── data/
    └── contacts.json       # Kişiler veritabanı
```

## 🔧 Teknolojiler

### Backend
- **Python 3.8+** - Ana dil
- **Google Gemini AI** - Doğal dil işleme
- **SpeechRecognition** - Ses tanıma
- **pyttsx3** - Text-to-Speech
- **Porcupine** - Wake word detection (opsiyonel)

### Platform Entegrasyonları
- **pywin32** - Windows API
- **pycaw** - Windows ses kontrolü
- **pyautogui** - GUI otomasyon
- **ADB** - Android kontrolü
- **Kivy** - Cross-platform mobil app

### AI & NLP
- **Google Generative AI** - Intent recognition
- **JSON** - Komut yapılandırması

## 🚀 Kullanım Senaryoları

### 1. Ofis Çalışması
```
"Virtus, Word'ü aç"
"Virtus, ekranı yakınlaştır"
"Virtus, bu metni Mehmet'e mail at"
```

### 2. Ev Otomasyonu
```
"Virtus, ışıkları kapat"  (smart home ile)
"Virtus, müziği aç"
"Virtus, saat 7'de alarm kur"
```

### 3. Telefon Kontrolü
```
"Virtus, annem'i ara"
"Virtus, Ahmet'e mesaj gönder"
"Virtus, son mesajları oku"
```

### 4. Bilgi Asistanı
```
"Virtus, bugün hava nasıl?"
"Virtus, en yakın restoran nerede?"
"Virtus, 150 euro kaç TL?"
```

## 🔐 Güvenlik & Gizlilik

- ✅ API keyleri `.env` dosyasında (git'e dahil değil)
- ✅ Ses kaydı saklanmıyor
- ✅ Konuşma geçmişi lokal
- ⚠️  Gemini API'ye internet üzerinden gidiyor
- 🔜 Offline mod (local LLM ile)

## 📊 Performans

- **Wake word latency**: ~100ms
- **Speech recognition**: 1-2 saniye
- **AI processing**: 0.5-2 saniye
- **Action execution**: Anında
- **Total response time**: ~3-5 saniye

## 🎓 Öğrenme Kaynakları

### Dokümantasyon
- `README.md` - Proje açıklaması
- `KURULUM.md` - Detaylı kurulum
- `QUICK_START.md` - Hızlı başlangıç

### API Dokümantasyonları
- [Google Gemini API](https://ai.google.dev/)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [Kivy](https://kivy.org/doc/stable/)

## 🛠️ Geliştirme Roadmap

### Faz 1: Temel Sistem ✅
- [x] Wake word detection
- [x] Speech recognition
- [x] AI integration
- [x] Basic commands

### Faz 2: Platform Entegrasyonları 🚧
- [x] Windows control
- [ ] Android full integration
- [ ] iOS support
- [ ] Linux support

### Faz 3: Gelişmiş Özellikler 📋
- [ ] Context-aware conversations
- [ ] Learning from user habits
- [ ] Multi-language support
- [ ] Voice authentication

### Faz 4: IoT & Smart Home 🔮
- [ ] Smart home devices
- [ ] Car integration
- [ ] Wearable devices
- [ ] Cloud sync

## 🤝 Katkıda Bulunma

Bu bir kişisel proje ama fikirlerinizi paylaşabilirsiniz:

1. Fork edin
2. Feature branch oluşturun
3. Commit edin
4. Pull request gönderin

## 📄 Lisans

MIT License - Özgürce kullanın ve geliştirin!

## 👨‍💻 Geliştirici Notları

### Eklenmesi Gerekenler
- [ ] Hata yönetimi iyileştirmesi
- [ ] Unit testler
- [ ] CI/CD pipeline
- [ ] Docker container
- [ ] Web dashboard
- [ ] API endpoint'leri

### Bilinen Sorunlar
- PyAudio bazen kurulumda sorun çıkarıyor → pipwin kullanın
- Custom wake word için Porcupine key gerekli
- Android call permission sorunları olabilir

### Optimizasyon Fırsatları
- Gemini yerine local LLM (Ollama)
- Speech recognition için Whisper
- Wake word için custom model training
- Async işlemler için aiohttp

## 📞 İletişim & Destek

Bu bir öğrenim projesi. Sorularınız için:
- Issue açın
- Dokümantasyonu kontrol edin
- Demo'ları çalıştırın

---

**Virtus ile keyifli asistan deneyimi! 🚀🤖**
