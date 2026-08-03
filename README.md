# ⚽ FIFA World Cup 2026 — Player Performance Analysis

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=flat-square&logo=jupyter)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=flat-square&logo=plotly)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Seaborn-11557c?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> Exploratory Data Analysis (EDA) lengkap dari dataset performa pemain FIFA World Cup 2026, mencakup analisis ofensif, defensif, fisik, tim, dan lebih banyak lagi — tersedia dalam format **Jupyter Notebook** (static) dan **Streamlit Dashboard** (interactive).

---

## 📋 Daftar Isi

- [Overview](#-overview)
- [Dataset](#-dataset)
- [Struktur Analisis (Notebook)](#-struktur-analisis-notebook)
- [Interactive Dashboard (Streamlit)](#-interactive-dashboard-streamlit)
- [Key Insights](#-key-insights)
- [Cara Menjalankan](#-cara-menjalankan)
- [Dependensi](#-dependensi)
- [Struktur Folder](#-struktur-folder)
- [Tools & Library](#️-tools--library)

---

## 🌍 Overview

Proyek ini merupakan analisis data eksploratif (EDA) menyeluruh dari dataset performa pemain pada ajang **FIFA World Cup 2026**. Analisis ini bertujuan untuk:

- Mengungkap **pola performa** pemain terbaik di turnamen
- Membandingkan **efisiensi ofensif** (Goals vs xG) antar pemain dan posisi
- Menganalisis **tren performa** sepanjang tahapan turnamen dari Group Stage hingga Final
- Mengidentifikasi **tim terkuat** berdasarkan win rate dan produktivitas gol
- Menemukan pemain dengan **value-for-money terbaik** berdasarkan nilai pasar vs performa

---

## 📊 Dataset

| Atribut | Detail |
|---|---|
| **File** | `fifa_world_cup_2026_player_performance.csv` |
| **Ukuran** | ~17 MB |
| **Total Baris** | 54,601 |
| **Total Kolom** | 75 |

### Kolom Utama

```
Identitas     : player_id, player_name, age, nationality, team, position, club_name
Match Info    : match_id, match_date, stadium, tournament_stage, match_result
Ofensif       : goals, assists, shots, shots_on_target, expected_goals_xg, expected_assists_xa
Passing       : successful_passes, total_passes, pass_accuracy, key_passes
Dribbling     : dribbles_attempted, successful_dribbles
Defensif      : tackles, interceptions, clearances, blocks, aerial_duels_won
Fisik         : distance_covered_km, sprint_distance_km, top_speed_kmh, stamina_score
Rating        : player_rating, performance_score, offensive_contribution, defensive_contribution
Kiper         : saves, save_percentage, clean_sheet, goals_conceded
```

---

## 🧩 Struktur Analisis (Notebook)

Notebook `Analysis/fifa2026_analysis.ipynb` terdiri dari **12 seksi analisis** dengan 30+ visualisasi static bertema dark premium:

| # | Seksi | Deskripsi |
|---|-------|-----------|
| 1 | **Setup & Data Loading** | Import library, konfigurasi tema visual, load dataset |
| 2 | **Data Overview & Quality** | Cek missing values, tipe data, statistik deskriptif |
| 3 | **Tournament Overview** | Ringkasan turnamen, jumlah laga per tahap |
| 4 | **Player Demographics** | Distribusi usia, posisi, kaki dominan, tinggi badan, nasionalitas |
| 5 | **Attacking Performance** | Top scorers, xG vs actual goals, shot conversion rate, top assisters |
| 6 | **Passing & Creativity** | Pass accuracy per posisi, creativity index, analisis dribbling |
| 7 | **Defensive Performance** | Top defenders, intensitas defensif per tahap, rekam kartu |
| 8 | **Physical & Stamina** | Top speed, distribusi jarak per posisi, stamina vs distance |
| 9 | **Overall Player Ratings** | KDE + box plot rating, top 15 pemain, radar chart top 5 |
| 10 | **Team Analysis** | Win rate, goals per game, bubble chart gol dicetak vs kebobolan |
| 11 | **Advanced Insights** | Correlation heatmap, performa berdasarkan hasil laga, tren per tahap, market value |
| 12 | **Key Findings & Summary** | Ringkasan insight utama + final dashboard (`fifa2026_dashboard.png`) |

---

## 🚀 Interactive Dashboard (Streamlit)

Selain notebook, proyek ini juga dilengkapi dengan **dashboard interaktif** berbasis Streamlit dengan tema dark premium dan semua chart menggunakan Plotly (zoom, hover, pan).

### Fitur Dashboard

| Halaman | Fitur Utama |
|---------|-------------|
| 🏠 **Overview** | 6 KPI cards (teams, players, matches, goals, assists, rating), charts per stage, top leaders |
| 👤 **Player Explorer** | Tabel filterable + Radar Chart komparasi hingga 5 pemain secara bersamaan |
| ⚽ **Attacking** | Top scorers, scatter xG overperformers, shot conversion rate, assists analysis |
| 🛡️ **Defensive** | Top defenders (stacked bar), intensitas per stage (line chart), rekam kartu |
| 💪 **Physical** | Speed ranking, violin plot distribusi kecepatan, stamina vs distance + OLS trendline |
| 🌍 **Teams** | Win rate ranking, goals chart, radar comparator tim, bubble chart gol |

### Global Filters (Sidebar)
- Filter **Tournament Stage** (Group Stage → Final)
- Filter **Posisi Pemain** (Goalkeeper, Defender, Midfielder, Forward)
- Slider **minimum menit bermain** untuk menyaring pemain aktif

### Menjalankan Dashboard

```bash
cd Dashboard
streamlit run app.py
```

Buka browser dan akses: **http://localhost:8501**

---

## 💡 Key Insights

### 🥇 Individu
- **Top Scorer** memiliki selisih **Goals vs xG positif** yang signifikan — mengindikasikan pemain yang "overperform" ekspektasi statistik
- **Pemain kreatif** (key passes + assists + xA) didominasi oleh **gelandang** dengan akurasi umpan tertinggi
- **Kecepatan puncak rata-rata** pemain: ~30 km/h; **jarak tempuh rata-rata** per laga: ~9–10 km

### 🛡️ Defensif
- Intensitas defensif (tackles & interceptions) **meningkat secara konsisten** di babak knockout dibandingkan group stage
- Jumlah kartu kuning dan merah juga **memuncak di babak eliminasi**

### 🌍 Tim
- Tim dengan **win rate tertinggi** menunjukkan keseimbangan antara ofensif produktif dan pertahanan solid (selisih gol positif)
- Hubungan antara **nilai pasar pemain** dan skor performa tidak selalu linier — beberapa pemain bernilai rendah tampil luar biasa

### 📈 Korelasi
- **`performance_score`** berkorelasi kuat dengan `player_rating`, `goals`, dan `expected_goals_xg`
- **`stamina_score`** berkorelasi positif dengan `distance_covered_km`

---

## 🚀 Cara Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/username/fifa-world-cup-2026-analysis.git
cd fifa-world-cup-2026-analysis
```

### 2. Install Dependensi

```bash
# Untuk Notebook
pip install pandas numpy matplotlib seaborn jupyter

# Untuk Streamlit Dashboard
pip install -r Dashboard/requirements.txt
```

### 3A. Jalankan Notebook (Static Analysis)

```bash
cd Analysis
jupyter notebook fifa2026_analysis.ipynb
```

> Jalankan seluruh cell dari atas ke bawah dengan **Kernel → Restart & Run All**.

### 3B. Jalankan Dashboard (Interactive)

```bash
cd Dashboard
streamlit run app.py
```

> Buka browser di **http://localhost:8501**

---

## 📦 Dependensi

### Notebook
```txt
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
jupyter>=1.0.0
```

### Streamlit Dashboard
```txt
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.23.0
plotly>=5.15.0
```

---

## 📁 Struktur Folder

```
FIFA World Cup 2026 Player Performance Dataset/
│
├── 📄 README.md                          # Dokumentasi proyek ini
│
├── 📂 Analysis/
│   ├── 📓 fifa2026_analysis.ipynb        # Notebook EDA utama (12 seksi, 30+ charts)
│   ├── 📊 fifa_world_cup_2026_player_performance.csv  # Dataset utama (~17 MB)
│   └── 🖼️  fifa2026_dashboard.png         # Output dashboard static (auto-generated)
│
└── 📂 Dashboard/
    ├── 🐍 app.py                         # Streamlit interactive dashboard (6 halaman)
    └── 📋 requirements.txt               # Dependensi dashboard
```

---

## 🛠️ Tools & Library

| Tool | Kegunaan |
|------|----------|
| `pandas` | Manipulasi dan agregasi data |
| `numpy` | Operasi numerik dan array |
| `matplotlib` | Visualisasi static (bar, scatter, radar, dll.) |
| `seaborn` | Heatmap dan distribusi statistik |
| `plotly` | Visualisasi interaktif pada Streamlit dashboard |
| `streamlit` | Framework interactive web dashboard |
| `Jupyter Notebook` | Lingkungan analisis eksploratif |

---

## 📝 Lisensi

Proyek ini dibuat untuk keperluan **portofolio data analysis**. Dataset bersifat publik/simulasi untuk tujuan edukasi.

---

## 👤 Author

**[Nama Anda]**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat-square&logo=github&logoColor=white)](https://github.com/username)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/username)

---

> ⭐ Jika proyek ini bermanfaat, jangan lupa berikan **star** di GitHub!
