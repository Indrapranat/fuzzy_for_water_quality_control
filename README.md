# AquascapeFuzzy

![Screenshot Aplikasi](assets/app_preview.png)

> **Model Logika Fuzzy Mamdani dalam Menentukan Strategi Perawatan Akuarium Aquascape Berdasarkan Fluktuasi Parameter Kualitas Air**

Sistem komputasi berbasis Python yang mengimplementasikan **Logika Fuzzy Mamdani** secara manual (tanpa library fuzzy pihak ketiga) untuk menganalisis data kualitas air akuarium aquascape dan menghasilkan rekomendasi strategi perawatan.

---

## Daftar Isi

- [Cara Install](#cara-install)
- [Cara Menjalankan](#cara-menjalankan)
- [Struktur Folder](#struktur-folder)
- [Format Data Input](#format-data-input)
- [Variabel Fuzzy](#variabel-fuzzy)
- [Cara Mengganti Rule](#cara-mengganti-rule)
- [Cara Mengganti Membership Function](#cara-mengganti-membership-function)
- [Cara Kerja Inferensi Mamdani](#cara-kerja-inferensi-mamdani)
- [Cara Kerja Defuzzifikasi Centroid](#cara-kerja-defuzzifikasi-centroid)
- [Menjalankan Unit Test](#menjalankan-unit-test)
- [Output yang Dihasilkan](#output-yang-dihasilkan)

---

## Cara Install

### Prasyarat

- Python 3.9 atau lebih baru
- pip (biasanya sudah terinstall bersama Python)

### Langkah Instalasi

```bash
# 1. Masuk ke direktori project
cd AquascapeFuzzy

# 2. (Opsional) Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install seluruh dependensi
pip install -r requirements.txt
```

---

## Cara Menjalankan

```bash
# Pastikan file data/data.xlsx sudah ada
python main.py
```

Program akan:
1. Membaca `data/data.xlsx`
2. Memvalidasi setiap nilai input
3. Menjalankan inferensi Fuzzy Mamdani untuk setiap baris
4. Menampilkan detail proses ke konsol
5. Menyimpan hasil ke `output/hasil.xlsx`
6. Menyimpan ringkasan ke `output/summary.txt`
7. Menghasilkan 4 grafik MF + grafik per-data di `output/graphs/`

### Menjalankan Antarmuka Pengguna (UI)

Sistem ini juga dilengkapi dengan antarmuka web modern berbasis Streamlit untuk keperluan demonstrasi visual.

```bash
streamlit run app.py
```

Antarmuka ini memuat fitur-fitur berikut:
- **Dashboard**: Gambaran umum dan alur proses logika fuzzy.
- **Analisis Data**: Input manual untuk evaluasi interaktif dan melihat perhitungan detil (fuzzifikasi hingga centroid).
- **Visualisasi Membership**: Pratinjau representasi grafis *membership function* (Suhu, pH, Kekeruhan, dan Output) beserta contoh hasil grafik inferensi.
- **Rule Base**: Daftar 27 tabel aturan berbasis interaktif lengkap dengan fitur pemfilteran.
- **Riwayat Analisis**: Tabel riwayat analisis dan fitur ekspor ke Excel.
- **Tentang Penelitian**: Penjelasan singkat perihal riset dan parameter input.

---

## Struktur Folder

```
AquascapeFuzzy/
├── data/
│   └── data.xlsx              ← File data input (wajib dibuat)
│
├── output/
│   ├── hasil.xlsx             ← Hasil analisis (auto-generated)
│   ├── summary.txt            ← Ringkasan statistik (auto-generated)
│   ├── run.log                ← Log eksekusi (auto-generated)
│   └── graphs/
│       ├── mf_suhu.png        ← Grafik MF Suhu
│       ├── mf_ph.png          ← Grafik MF pH
│       ├── mf_kekeruhan.png   ← Grafik MF Kekeruhan
│       ├── mf_output.png      ← Grafik MF Output
│       ├── agregasi_001.png   ← Agregasi Data #1
│       └── defuzzifikasi_001.png ← Defuzzifikasi Data #1
│
├── fuzzy/
│   ├── __init__.py
│   ├── membership.py          ← Fungsi keanggotaan triangular
│   ├── rules.py               ← 27 Rule Fuzzy Mamdani
│   ├── inference.py           ← Mesin inferensi Mamdani
│   ├── defuzzification.py     ← Defuzzifikasi Centroid
│   └── validator.py           ← Validasi data input
│
├── utils/
│   ├── __init__.py
│   ├── excel.py               ← Baca/tulis Excel
│   ├── plotting.py            ← Pembuatan grafik
│   └── logger.py              ← Konfigurasi logging
│
├── tests/
│   ├── __init__.py
│   ├── test_membership.py     ← Test fungsi keanggotaan
│   ├── test_validator.py      ← Test validasi
│   ├── test_inference.py      ← Test inferensi
│   └── test_defuzzification.py ← Test defuzzifikasi centroid
│
├── config.py                  ← Konfigurasi terpusat
├── main.py                    ← Entry point utama
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Format Data Input

Buat file `data/data.xlsx` dengan format berikut:

| No | Suhu | pH  | Kekeruhan |
|----|------|-----|-----------|
| 1  | 27.0 | 7.0 | 10.0      |
| 2  | 30.5 | 6.5 | 45.0      |
| 3  | 22.0 | 8.2 | 80.0      |

**Rentang Valid:**
| Parameter | Min | Max | Satuan |
|-----------|-----|-----|--------|
| Suhu      | 0   | 50  | °C     |
| pH        | 0   | 14  | —      |
| Kekeruhan | 0   | 100 | NTU    |

---

## Variabel Fuzzy

### Input 1: Suhu Air (°C)

| Kategori | a     | b     | c     |
|----------|-------|-------|-------|
| Dingin   | 0     | 0     | 26    |
| Normal   | 24    | 27    | 30    |
| Panas    | 28    | 50    | 50    |

### Input 2: pH Air

| Kategori | a | b  | c  |
|----------|---|----|----|
| Asam     | 0 | 0  | 7  |
| Netral   | 6 | 7  | 8  |
| Basa     | 7 | 14 | 14 |

### Input 3: Kekeruhan (NTU)

| Kategori | a  | b   | c   |
|----------|----|-----|-----|
| Jernih   | 0  | 0   | 40  |
| Sedang   | 20 | 50  | 80  |
| Keruh    | 60 | 100 | 100 |

### Output: Strategi Perawatan

| Kategori            | a  | b   | c   |
|---------------------|----|-----|-----|
| Perawatan Ringan    | 0  | 0   | 50  |
| Perawatan Sedang    | 25 | 50  | 75  |
| Perawatan Intensif  | 50 | 100 | 100 |

---

## Cara Mengganti Rule

Seluruh rule tersimpan di `fuzzy/rules.py` dalam variabel `RULES`.

Setiap rule adalah dictionary dengan format:

```python
{
    "suhu":      "Normal",            # Dingin | Normal | Panas
    "ph":        "Netral",            # Asam | Netral | Basa
    "kekeruhan": "Jernih",            # Jernih | Sedang | Keruh
    "output":    "Perawatan Ringan",  # Perawatan Ringan | Sedang | Intensif
}
```

**Contoh menambah atau mengubah rule:**

```python
# Di fuzzy/rules.py, ubah elemen dalam list RULES
RULES[12] = {
    "suhu":      "Normal",
    "ph":        "Netral",
    "kekeruhan": "Jernih",
    "output":    "Perawatan Ringan",  # Ubah output di sini
}
```

Tidak ada kode lain yang perlu diubah — sistem akan otomatis menggunakan rule terbaru.

---

## Cara Mengganti Membership Function

Seluruh parameter MF tersimpan di `config.py`.

**Contoh mengubah parameter Suhu:**

```python
# Di config.py
SUHU_MF = {
    "Dingin": (0.0, 0.0, 25.0),   # Ubah titik c dari 26 → 25
    "Normal": (23.0, 27.0, 31.0), # Geser rentang Normal
    "Panas":  (29.0, 50.0, 50.0), # Geser titik a dari 28 → 29
}
```

**Format parameter:** `(a, b, c)` di mana:
- `a` = titik kaki kiri (μ = 0 saat x ≤ a)
- `b` = titik puncak (μ = 1 saat x = b)
- `c` = titik kaki kanan (μ = 0 saat x ≥ c)

Tidak perlu mengubah file lain setelah mengubah `config.py`.

---

## Cara Kerja Inferensi Mamdani

Sistem menggunakan **Metode Mamdani** dengan alur sebagai berikut:

### Tahap 1: Fuzzifikasi

Mengubah nilai crisp (terukur) menjadi derajat keanggotaan fuzzy menggunakan **Triangular Membership Function**:

```
       μ(x) = 0,                   jika x ≤ a atau x ≥ c
       μ(x) = (x - a) / (b - a),  jika a < x ≤ b
       μ(x) = (c - x) / (c - b),  jika b < x < c
```

Contoh: Suhu = 25.5°C → μ_Normal = (25.5 - 24) / (27 - 24) = **0.5**

### Tahap 2: Evaluasi Rule (Operator AND = MIN)

Setiap rule dievaluasi dengan **fungsi MIN** sebagai operator AND:

```
α_i = MIN(μ_suhu, μ_ph, μ_kekeruhan)
```

Rule dikatakan **aktif** jika `α_i > 0`.

### Tahap 3: Implikasi (Clipping)

Output setiap rule aktif dipotong pada nilai fire strength:

```
μ_clip(x) = MIN(α_i, μ_output(x))
```

### Tahap 4: Agregasi (Operator MAX)

Seluruh output rule digabungkan menggunakan **fungsi MAX**:

```
μ_agregasi(x) = MAX(μ_clip_r1(x), μ_clip_r2(x), ..., μ_clip_rN(x))
```

---

## Cara Kerja Defuzzifikasi Centroid

Metode **Centroid** (Center of Gravity) mengubah kurva agregasi menjadi nilai crisp tunggal:

```
           Σ [x_i × μ(x_i)]
z* = ─────────────────────────────
              Σ μ(x_i)
```

Keterangan:
- `z*` = nilai defuzzifikasi (output akhir) dalam rentang [0, 100]
- `x_i` = titik ke-i pada universe of discourse
- `μ(x_i)` = derajat keanggotaan agregasi pada titik x_i

**Kategorisasi hasil centroid:**

| Rentang z*       | Strategi Perawatan  |
|------------------|---------------------|
| 0 – 37.5         | Perawatan Ringan    |
| 37.5 – 62.5      | Perawatan Sedang    |
| 62.5 – 100       | Perawatan Intensif  |

---

## Menjalankan Unit Test

```bash
# Jalankan semua test
pytest tests/ -v

# Jalankan dengan laporan cakupan kode
pytest tests/ -v --cov=fuzzy --cov-report=term-missing

# Jalankan test untuk modul tertentu
pytest tests/test_membership.py -v
pytest tests/test_validator.py -v
pytest tests/test_inference.py -v
pytest tests/test_defuzzification.py -v
```

---

## Output yang Dihasilkan

| File | Deskripsi |
|------|-----------|
| `output/hasil.xlsx` | Tabel hasil: No, Suhu, pH, Kekeruhan, Centroid, Kategori |
| `output/summary.txt` | Ringkasan: total data, rata-rata centroid, distribusi kategori |
| `output/run.log` | Log lengkap proses eksekusi |
| `output/graphs/mf_suhu.png` | Grafik fungsi keanggotaan Suhu |
| `output/graphs/mf_ph.png` | Grafik fungsi keanggotaan pH |
| `output/graphs/mf_kekeruhan.png` | Grafik fungsi keanggotaan Kekeruhan |
| `output/graphs/mf_output.png` | Grafik fungsi keanggotaan Output |
| `output/graphs/agregasi_NNN.png` | Grafik agregasi MAX untuk data #NNN |
| `output/graphs/defuzzifikasi_NNN.png` | Grafik defuzzifikasi untuk data #NNN |

---

## Dependensi

| Library | Versi Minimum | Kegunaan |
|---------|---------------|----------|
| numpy | 1.24.0 | Operasi array numerik |
| pandas | 2.0.0 | Baca/tulis Excel dan DataFrame |
| matplotlib | 3.7.0 | Pembuatan grafik |
| openpyxl | 3.1.0 | Engine Excel untuk pandas |
| scipy | 1.10.0 | Operasi saintifik tambahan |
| pytest | 7.4.0 | Framework unit test |

> **Catatan:** Project ini **tidak** menggunakan `scikit-fuzzy` (skfuzzy). Seluruh perhitungan fuzzy diimplementasikan manual menggunakan NumPy agar proses dapat dipahami dan dijelaskan secara akademis pada Bab IV skripsi.
