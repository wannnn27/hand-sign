# Hand Sign Voice Recognition 👋🗣️

Aplikasi pengenalan gestur tangan berbasis AI menggunakan **MediaPipe** dan **OpenCV**, yang menerjemahkan gerakan tangan menjadi suara (Text-to-Speech) dalam Bahasa Indonesia.

## 📋 Fitur
- **Deteksi Tangan Real-time**: Menggunakan webcam untuk mendeteksi jari dan gestur.
- **Text-to-Speech (TTS)**: Mengubah gestur menjadi suara menggunakan Google TTS (`gTTS`).
- **Caching Suara**: Menyimpan file audio agar respon lebih cepat dan hemat data.
- **Audio Playback Stabil**: Menggunakan `pygame` untuk pemutaran audio tanpa blocking.

## 🛠️ Instalasi

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/wannnn27/hand-sign.git
   cd hand-sign
   ```

2. **Install dependencies:**
   Pastikan Anda menggunakan Python 3.10 atau versi yang kompatibel.
   ```bash
   pip install -r requirements.txt
   ```
   > **Catatan:** Jika terjadi error pada tampilan kamera, pastikan `opencv-python-headless` tidak terinstall. Jalankan `pip uninstall opencv-python-headless` jika perlu.

## 🚀 Cara Menjalankan

Jalankan script utama:
```bash
python gesture.py
```
Arahkan tangan kanan Anda ke kamera.

## ✌️ Daftar Gestur

Berikut adalah gestur yang dikenali:

| Gestur | Jari Terbuka | Output Suara |
| :--- | :--- | :--- |
| **FIVE** (5) | Semua jari | *"Halo!"* |
| **TWO** (2) | Telunjuk & Tengah | *"Perkenalkan"* |
| **ONE** (1) | Telunjuk saja | *"Saya Adi Arwan Syah"* |
| **ROCK** 🤘 | Telunjuk & Kelingking* | *"Dari prodi Sistem Informasi"* |
| **THUMB** 👍 | Jempol saja | *"Terima kasih"* |

*(Gestur ROCK disesuaikan dengan logika pada kode: Jempol + Kelingking atau sesuai implementasi)*

## 📄 Lisensi
Project ini dilisensikan di bawah **MIT License**. Lihat file [LICENSE](LICENSE) untuk detailnya.

---
**Created by Adi Arwan Syah**
