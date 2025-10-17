# 🎙️ Profesyonel Ses Asistanı

Modern yapay zeka destekli metin okuma, konuşma tanıma ve ses klonlama uygulaması.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## ✨ Özellikler

- 🔊 **Text-to-Speech:** İnsan gibi doğal ses ile metin okuma
- 🎤 **Speech-to-Text:** Konuşmayı metne çevirme
- 🎭 **Ses Klonlama:** Kendi sesinizi kullanın (5-10 saniye yeterli)
- 🌍 **Çok Dilli:** Türkçe ve İngilizce desteği
- 🖥️ **Modern Arayüz:** Kullanıcı dostu web arayüzü
- 💻 **Offline:** İnternet bağlantısı gerektirmez

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler
- Python 3.8 veya üzeri
- FFmpeg

### 2. Kurulum

```bash
# Projeyi klonla
git clone https://github.com/kullanici/ses-asistani.git
cd ses-asistani

# Virtual environment oluştur
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Kütüphaneleri yükle
pip install coqui-tts openai-whisper gradio torch sounddevice soundfile numpy ffmpeg-python
```

### 3. FFmpeg Kurulumu

**Windows:**
```bash
choco install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### 4. Çalıştır

```bash
python ses_asistani_gui.py
```

Tarayıcıda otomatik açılır: `http://127.0.0.1:7860`

## 📖 Kullanım

### Text-to-Speech (Metin Okuma)
1. "Text-to-Speech" sekmesine git
2. Metni yaz
3. Dil seç (Türkçe/English)
4. "Oku" butonuna tıkla

### Speech-to-Text (Konuşma Tanıma)
1. "Speech-to-Text" sekmesine git
2. Mikrofona konuş veya ses dosyası yükle
3. "Metne Çevir" butonuna tıkla

### Ses Klonlama
1. "Ses Klonlama" sekmesine git
2. 5-10 saniye net konuş
3. "Sesi Klonla" butonuna tıkla
4. Artık TTS'de kendi sesinle konuşabilirsin

## 🛠️ Kullanılan Teknolojiler

- **Coqui TTS (XTTS-v2):** İnsan benzeri ses sentezi
- **OpenAI Whisper:** Konuşma tanıma
- **Gradio:** Web arayüzü
- **PyTorch:** Derin öğrenme altyapısı

## 📊 Sistem Gereksinimleri

**Minimum:**
- RAM: 4 GB
- Disk: 2 GB boş alan
- CPU: Intel i3 veya eşdeğeri

**Önerilen:**
- RAM: 8 GB
- GPU: NVIDIA (CUDA destekli)
- SSD

## 🐛 Sorun Giderme

### "FFmpeg bulunamadı" hatası
FFmpeg'i sistem PATH'ine ekleyin veya manuel kurun.

### "TTS motoru hazır değil" hatası
İlk çalıştırmada modeller indiriliyor, lütfen bekleyin (~500MB).

### Mikrofon çalışmıyor
Windows Ayarlar → Gizlilik → Mikrofon → İzin ver

## 📝 Lisans

Bu proje açık kaynaklıdır. Kişisel ve eğitim amaçlı kullanım için ücretsizdir.

**Kullanılan Kütüphaneler:**
- Coqui TTS: CPML (Kişisel kullanım ücretsiz)
- OpenAI Whisper: MIT License
- Gradio: Apache 2.0

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Commit yapın (`git commit -m 'Yeni özellik eklendi'`)
4. Push edin (`git push origin feature/yeniOzellik`)
5. Pull Request açın

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

## 🙏 Teşekkürler

- [Coqui AI](https://github.com/coqui-ai/TTS)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Gradio](https://gradio.app/)

---

⭐ Beğendiyseniz yıldız vermeyi unutmayın!