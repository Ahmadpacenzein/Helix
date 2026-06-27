# HELIX - Global Natural Disaster Monitor

HELIX adalah aplikasi dashboard berbasis web (Single Page Application) yang didesain khusus untuk memantau data bencana alam global secara real-time menggunakan data dari **NASA EONET API**.

Proyek ini mendemonstrasikan implementasi NoSQL Data Modeling menggunakan MongoDB, termasuk perancangan skema berbasis query, denormalisasi data, pembuatan indeks, pipeline agregasi, serta sinkronisasi data terjadwal di latar belakang (*background scheduler*).

---

##  Fitur Utama
1. **Peta Interaktif (MapLibre GL)**: Visualisasi lokasi bencana dengan penanda dinamis berkode warna berdasarkan kategori hazard.
2. **Dashboard Summary Cards**: Menampilkan metrik total bencana, status aktif, jumlah kategori, dan negara terdampak.
3. **Penyaring Kategori & Waktu**: Memfilter sebaran peta secara langsung tanpa memuat ulang halaman (*No Page Reload*).
4. **Pencarian Terdebounce**: Fitur pencarian nama bencana, negara, atau kategori dengan optimasi *debounce* 300ms untuk meminimalkan beban API.
5. **Visualisasi Analisis (Chart.js)**: Menyajikan data dalam bentuk Category Distribution (Pie Chart), Country Statistics (Bar Chart), dan Daily Trend (Line Chart).
6. **Background Scheduler**: Mengambil data NASA EONET dan melakukan agregasi secara berkala di latar belakang (interval dapat dikonfigurasi).

---

##  Tech Stack
* **Frontend**: HTML5, Vanilla CSS (Glassmorphism design system), Bootstrap 5, Vanilla JavaScript, MapLibre GL JS, Chart.js.
* **Backend**: Python 3.12, Flask, APScheduler (Background Scheduler), PyMongo, Requests.
* **Database**: MongoDB Community Edition.

---

##  Dokumentasi & Screenshots

Berikut adalah seluruh visualisasi dan dokumentasi antarmuka serta sistem database aplikasi HELIX:

### 1. Dashboard Utama
Menampilkan visualisasi glassmorphism premium dengan tema gelap (dark theme), ringkasan kartu metrik, peta interaktif, daftar live feed, filter kategori, dan grafik analisis.
![Dashboard Utama](screenshots/Dashboard%20penuh.png)

### 2. Peta Interaktif & Live Feed
Menampilkan titik-titik bencana menggunakan MapLibre GL dengan penanda dinamis berkode warna berdasarkan kategori hazard (misal: Merah untuk Kebakaran Hutan, Biru untuk Badai, Hijau untuk Gempa/Gunung Berapi).
![Peta Utama](screenshots/Peta%20dengan%20marker.png)

### 3. Grafik Analisis & Chart
Visualisasi distribusi kategori bencana (Pie Chart), top 5 negara terdampak (Bar Chart), serta tren bencana harian (Line Chart).
![Grafik Analisis](screenshots/Analytics%20chart.png)

### 4. Pencarian Terdebounce
Pencarian real-time dengan penundaan (*debounce*) 300ms yang langsung menyaring peta dan feed data tanpa membebani browser atau backend.
![Hasil Pencarian](screenshots/Search%20yang%20berhasil.png)

### 5. Log Status Sinkronisasi (Synchronization Status)
Menampilkan metadata sinkronisasi data terakhir, seperti status keberhasilan, waktu sinkronisasi, jumlah data baru yang diimpor, dan jumlah data yang diperbarui.
![Status Sinkronisasi](screenshots/Synchronization%20Status%20(Success).png)

### 6. Terminal Proses Scheduler
Tampilan console/terminal saat background scheduler berjalan secara otomatis untuk mengunduh data dari EONET API, melakukan *reverse geocoding* nama negara, dan memperbarui database.
![Proses Terminal](screenshots/Terminal%20saat%20scheduler%20berhasil%20sinkronisasi.png)

### 7. Struktur Database di MongoDB Compass
Struktur penyimpanan koleksi dokumen pada database `helix` di MongoDB Compass.
![Struktur MongoDB](screenshots/MongoDB%20Compass%20(helix%20terbuka).png)

### 8. Koleksi Dokumen `events`
Contoh dokumen data bencana yang disimpan di dalam koleksi `events`. Setiap dokumen menyimpan informasi lengkap bencana alam beserta koordinat dan negara yang berhasil diidentifikasi.
![Koleksi Events](screenshots/Collection%20events.png)

### 9. Koleksi Dokumen `dashboard_summary`
Hasil kompilasi dan agregasi data yang siap disajikan ke frontend, memisahkan statistik berdasarkan kategori, negara terdampak, dan tren harian.
![Koleksi Summary](screenshots/Collection%20dashboard_summary.png)

---

##  Panduan Instalasi & Penggunaan

### 1. Prasyarat
Sebelum memulai, pastikan perangkat Anda memiliki:
* **Python 3.11** atau versi lebih baru.
* **MongoDB Community Edition** terpasang dan berjalan di alamat default `localhost:27017`.

---

### 2. Langkah Instalasi

1. Clone atau ekstrak repositori proyek ke komputer Anda.
2. Buka terminal (atau PowerShell/Command Prompt di Windows) pada direktori proyek.
3. Buat dan aktifkan virtual environment Python:
   * **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   * **Windows (Command Prompt)**:
     ```cmd
     python -m venv venv
     .\venv\Scripts\activate.bat
     ```
   * **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
4. Pasang seluruh pustaka (dependencies) yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```
5. Salin dan konfigurasikan file environtment `.env`:
   ```bash
   # Windows (PowerShell/CMD) atau macOS/Linux
   cp .env.example .env
   ```
   Secara default, konfigurasi dalam `.env` adalah sebagai berikut:
   ```env
   PORT=5000
   MONGO_URI=mongodb://localhost:27017/
   MONGO_DB=helix
   FETCH_INTERVAL=2
   ```
   *Catatan: `FETCH_INTERVAL=2` berarti background scheduler akan menyinkronkan data ke NASA EONET setiap 2 menit sekali.*

---

### 3. Menjalankan Uji Coba & Database Seeding

#### A. Memasukkan Data Simulasi (Seeding)
Guna memudahkan pengujian tampilan dashboard secara instan tanpa menunggu proses sinkronisasi NASA EONET yang lama, masukkan 15 data tiruan bencana alam yang bervariasi dengan menjalankan script berikut:
```bash
# Di Windows (PowerShell)
$env:PYTHONPATH="."
python scripts/seed_data.py

# Di macOS/Linux atau CMD
PYTHONPATH=. python scripts/seed_data.py
```

#### B. Menjalankan Sinkronisasi Manual secara Langsung (Live Sync)
Apabila Anda ingin langsung menarik data bencana riil terbaru yang aktif dari server NASA EONET API ke database lokal, jalankan perintah ini:
```bash
# Di Windows (PowerShell)
$env:PYTHONPATH="."
python scripts/sync_now.py

# Di macOS/Linux atau CMD
PYTHONPATH=. python scripts/sync_now.py
```

#### C. Menjalankan Perbaikan Data Negara (Fix Country offline)
Untuk memperbarui kolom nama negara pada data bencana lama yang terdaftar sebagai "Unknown Country" secara otomatis berdasarkan pencocokan koordinat geografis:
```bash
# Di Windows (PowerShell)
$env:PYTHONPATH="."
python scripts/fix_countries.py

# Di macOS/Linux atau CMD
PYTHONPATH=. python scripts/fix_countries.py
```

---

### 4. Menjalankan Pengujian Sistem (Unit & Integration Tests)

Untuk memverifikasi fungsionalitas backend, database, parsing API EONET, serta kalkulasi agregasi data:
```bash
# Menjalankan semua modul tes sekaligus
python -m unittest discover -s tests -p "test_*.py"

# Atau menjalankan tes secara individual
python tests/test_database.py
python tests/test_dashboard.py
python tests/test_transformer.py
python tests/test_api.py
python tests/test_fetcher.py
```

---

### 5. Menjalankan Aplikasi

Jalankan server Flask utama dengan perintah:
```bash
python app.py
```
Setelah server aktif, buka browser Anda dan kunjungi tautan berikut:
```text
http://localhost:5000
```

Dashboard interaktif HELIX siap digunakan untuk memantau aktivitas bencana alam global secara real-time!
