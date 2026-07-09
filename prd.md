# PRD — AquascapeFuzzy
## Product Requirements Document

**Nama Proyek:** AquascapeFuzzy  
**Versi:** 1.1.0  
**Tanggal:** 7 Juli 2026  
**Status:** Final — Revisi Variabel Input ke-3: TDS  

---

## 1. Ringkasan Eksekutif

**AquascapeFuzzy** adalah sistem komputasi berbasis Python yang mengimplementasikan **Logika Fuzzy Mamdani** secara manual (tanpa library fuzzy pihak ketiga) untuk menganalisis data kualitas air akuarium aquascape dan menghasilkan rekomendasi strategi perawatan.

Judul penelitian:

> *"Model Logika Fuzzy Mamdani dalam Menentukan Strategi Perawatan Akuarium Aquascape Berdasarkan Fluktuasi Parameter Kualitas Air"*

Seluruh perhitungan diimplementasikan menggunakan NumPy agar proses dapat ditelusuri dan dijelaskan secara akademis.

---

## 2. Latar Belakang & Permasalahan

Akuarium aquascape membutuhkan pemantauan kualitas air yang konsisten. Tiga parameter utama yang digunakan adalah **Suhu**, **pH**, dan **Total Dissolved Solids (TDS)**. TDS mengukur jumlah zat padat terlarut dalam air (mineral, garam, organik terlarut) dalam satuan ppm (*parts per million*). Nilai TDS yang terlalu tinggi mengindikasikan penumpukan limbah, garam berlebih, atau mineral yang dapat mengganggu osmoregulasi ikan dan pertumbuhan tanaman aquascape.

**Masalah yang dipecahkan:**
- Penentuan strategi perawatan bersifat subjektif dan tidak terstandarisasi
- Tidak ada sistem otomatis yang transparan dan dapat diaudit secara akademis
- Kurangnya alat visualisasi proses inferensi fuzzy yang edukatif

---

## 3. Tujuan & Sasaran

| # | Tujuan | Indikator Keberhasilan |
|---|--------|------------------------|
| 1 | Implementasi inferensi Mamdani manual | Semua tahap berjalan tanpa library fuzzy |
| 2 | Menghasilkan rekomendasi perawatan | Output: nilai centroid + kategori per data |
| 3 | Antarmuka web edukatif | UI Streamlit 3 halaman berjalan lancar |
| 4 | Input batch dari Excel | Batch processing menghasilkan `hasil.xlsx` |
| 5 | Visualisasi grafik | Grafik MF, agregasi, defuzzifikasi di `output/graphs/` |

---

## 4. Pengguna Target

| Tipe Pengguna | Kebutuhan Utama |
|---------------|-----------------|
| Peneliti / Mahasiswa | Alat komputasi untuk data skripsi |
| Dosen Pembimbing | Memeriksa transparansi algoritma fuzzy |
| Penghobi Aquascape | Rekomendasi perawatan berdasarkan parameter air |

---

## 5. Spesifikasi Teknis — Metode Fuzzy Mamdani

### 5.1 Variabel Input

#### Input 1: Suhu Air (°C) — Universe [0, 50]

| Himpunan Fuzzy | Tipe | Parameter (a, b, c) | Keterangan |
|----------------|------|---------------------|------------|
| Dingin | Shoulder kiri | (0, 0, 26) | Suhu rendah berbahaya |
| Normal | Triangular | (24, 27, 30) | Kondisi ideal |
| Panas | Shoulder kanan | (28, 50, 50) | Suhu tinggi berbahaya |

#### Input 2: pH Air — Universe [0, 14]

| Himpunan Fuzzy | Tipe | Parameter (a, b, c) | Keterangan |
|----------------|------|---------------------|------------|
| Asam | Shoulder kiri | (0, 0, 7) | pH rendah merusak biota |
| Netral | Triangular | (6, 7, 8) | pH ideal |
| Basa | Shoulder kanan | (7, 14, 14) | pH tinggi merusak biota |

#### Input 3: Total Dissolved Solids / TDS (ppm) — Universe [0, 1000]

TDS mengukur jumlah total zat padat terlarut dalam air. Nilai TDS yang rendah menandakan air bersih dan mineral seimbang, sedangkan TDS tinggi menandakan akumulasi limbah, garam, atau mineral berlebih yang membahayakan ekosistem aquascape.

| Himpunan Fuzzy | Tipe | Parameter (a, b, c) | Keterangan |
|----------------|------|---------------------|------------|
| Rendah | Shoulder kiri | (0, 0, 200) | TDS rendah — air bersih |
| Sedang | Triangular | (100, 300, 500) | TDS sedang |
| Tinggi | Shoulder kanan | (400, 1000, 1000) | TDS tinggi — air kotor |

---

### 5.2 Variabel Output: Strategi Perawatan — Universe [0, 100]

| Himpunan Fuzzy | Tipe | Parameter (a, b, c) | Threshold Centroid |
|----------------|------|---------------------|--------------------|
| Perawatan Ringan | Shoulder kiri | (0, 0, 50) | z* < 37.5 |
| Perawatan Sedang | Triangular | (25, 50, 75) | 37.5 ≤ z* < 62.5 |
| Perawatan Intensif | Shoulder kanan | (50, 100, 100) | z* ≥ 62.5 |

Universe of discourse output didiskritisasi menjadi **1000 titik**.

---

### 5.3 Fungsi Keanggotaan Triangular (Triangular MF)

Rumus:

```
μ(x) = 0,                    jika x ≤ a atau x ≥ c
μ(x) = (x - a) / (b - a),   jika a < x ≤ b
μ(x) = (c - x) / (c - b),   jika b < x < c
μ(x) = 1,                    jika x = b
```

**Kasus shoulder:**
- **Shoulder kiri** (a = b): nilai 1 di titik a, turun linear menuju c
- **Shoulder kanan** (b = c): naik linear dari a, nilai 1 di titik b=c

---

### 5.4 Basis Aturan — 27 Aturan Fuzzy IF-THEN

Dibangun dari kombinasi penuh **3 × 3 × 3 = 27 kombinasi** anteseden.

**Logika penetapan output:**
- **Ringan** → semua parameter ideal (Normal + Netral + TDS Rendah)
- **Sedang** → satu parameter menyimpang
- **Intensif** → dua atau lebih parameter bermasalah, atau satu parameter ekstrem

| Rule | Suhu | pH | TDS | Output |
|------|------|----|-----|--------|
| R1 | Dingin | Asam | Rendah | Perawatan Intensif |
| R2 | Dingin | Asam | Sedang | Perawatan Intensif |
| R3 | Dingin | Asam | Tinggi | Perawatan Intensif |
| R4 | Dingin | Netral | Rendah | Perawatan Sedang |
| R5 | Dingin | Netral | Sedang | Perawatan Sedang |
| R6 | Dingin | Netral | Tinggi | Perawatan Intensif |
| R7 | Dingin | Basa | Rendah | Perawatan Intensif |
| R8 | Dingin | Basa | Sedang | Perawatan Intensif |
| R9 | Dingin | Basa | Tinggi | Perawatan Intensif |
| R10 | Normal | Asam | Rendah | Perawatan Sedang |
| R11 | Normal | Asam | Sedang | Perawatan Intensif |
| R12 | Normal | Asam | Tinggi | Perawatan Intensif |
| **R13** | **Normal** | **Netral** | **Rendah** | **Perawatan Ringan** |
| R14 | Normal | Netral | Sedang | Perawatan Sedang |
| R15 | Normal | Netral | Tinggi | Perawatan Sedang |
| R16 | Normal | Basa | Rendah | Perawatan Sedang |
| R17 | Normal | Basa | Sedang | Perawatan Intensif |
| R18 | Normal | Basa | Tinggi | Perawatan Intensif |
| R19 | Panas | Asam | Rendah | Perawatan Intensif |
| R20 | Panas | Asam | Sedang | Perawatan Intensif |
| R21 | Panas | Asam | Tinggi | Perawatan Intensif |
| R22 | Panas | Netral | Rendah | Perawatan Sedang |
| R23 | Panas | Netral | Sedang | Perawatan Intensif |
| R24 | Panas | Netral | Tinggi | Perawatan Intensif |
| R25 | Panas | Basa | Rendah | Perawatan Intensif |
| R26 | Panas | Basa | Sedang | Perawatan Intensif |
| R27 | Panas | Basa | Tinggi | Perawatan Intensif |

> Distribusi output: **1 Ringan** — **8 Sedang** — **18 Intensif**

---

### 5.5 Alur 4 Tahap Inferensi Mamdani

```
Input Crisp (Suhu, pH, TDS)
        │
        ▼
┌───────────────────────────────────┐
│  TAHAP 1: FUZZIFIKASI             │
│  Hitung μ(x) setiap kategori      │
│  menggunakan Triangular MF        │
└───────────────────┬───────────────┘
                    │
                    ▼
┌───────────────────────────────────┐
│  TAHAP 2: EVALUASI RULE           │
│  Operator AND = MIN               │
│  α_i = MIN(μ_suhu, μ_ph, μ_tds)  │
│  Rule aktif jika α_i > 0          │
└───────────────────┬───────────────┘
                    │
                    ▼
┌───────────────────────────────────┐
│  TAHAP 3: IMPLIKASI (CLIPPING)    │
│  μ_clip(x) = MIN(α_i, μ_output(x))│
└───────────────────┬───────────────┘
                    │
                    ▼
┌───────────────────────────────────┐
│  TAHAP 4: AGREGASI MAX            │
│  μ_agg(x) = MAX semua μ_clip(x)   │
└───────────────────┬───────────────┘
                    │
                    ▼
┌───────────────────────────────────┐
│  DEFUZZIFIKASI: CENTROID          │
│  z* = Σ(x·μ(x)) / Σ(μ(x))        │
│  → Nilai crisp [0, 100]           │
│  → Label kategori perawatan       │
└───────────────────────────────────┘
```

---

### 5.6 Defuzzifikasi — Metode Centroid (Center of Gravity)

**Rumus:**

```
         Σ [x_i × μ_agregasi(x_i)]
z* = ──────────────────────────────────
              Σ μ_agregasi(x_i)
```

- `z*` = nilai crisp output ∈ [0, 100]
- `x_i` = titik ke-i pada universe (1000 titik diskrit)
- `μ_agregasi(x_i)` = derajat keanggotaan hasil agregasi MAX
- Jika denominator = 0 → z* = 0.0

**Kategorisasi hasil centroid:**

| Rentang z* | Strategi Perawatan |
|------------|-------------------|
| 0 – 37.5 | Perawatan Ringan |
| 37.5 – 62.5 | Perawatan Sedang |
| 62.5 – 100 | Perawatan Intensif |

---

## 6. Arsitektur Sistem

```
AquascapeFuzzy/
├── app.py                    ← Entry point Streamlit (3 halaman)
├── main.py                   ← Entry point CLI (batch processing)
├── config.py                 ← Konfigurasi terpusat (semua parameter MF)
├── fuzzy/
│   ├── membership.py         ← Triangular MF + fuzzifikasi_tds()
│   ├── rules.py              ← 27 rule base (kolom: suhu, ph, tds)
│   ├── inference.py          ← Mesin inferensi (fuzzifikasi → agregasi)
│   ├── defuzzification.py    ← Centroid + kategorisasi
│   └── validator.py          ← Validasi range input (termasuk TDS 0–1000 ppm)
├── utils/
│   ├── excel.py              ← Baca/tulis Excel (kolom TDS)
│   ├── plotting.py           ← Grafik MF (termasuk mf_tds.png)
│   └── logger.py             ← Konfigurasi logging
├── ui/
│   ├── main_page.py          ← Router halaman Streamlit (input TDS)
│   └── styles.py             ← Custom CSS
├── tests/                    ← Unit test (pytest)
├── data/data.xlsx            ← File input (kolom: No, Suhu, pH, TDS)
└── output/                   ← Hasil analisis (auto-generated)
```

---

## 7. Spesifikasi Fitur

### 7.1 Mode CLI (main.py)

| Fitur | Deskripsi |
|-------|-----------|
| Baca Excel | Membaca `data/data.xlsx` (kolom: No, Suhu, pH, TDS) |
| Validasi Input | Memeriksa range valid (TDS: 0–1000 ppm) |
| Batch Inferensi | Inferensi Mamdani untuk setiap baris data |
| Output Excel | Hasil (No, Suhu, pH, TDS (ppm), Centroid, Kategori) → `hasil.xlsx` |
| Ringkasan | Total data, rata-rata centroid, distribusi kategori → `summary.txt` |
| Grafik MF | 4 PNG grafik fungsi keanggotaan (termasuk `mf_tds.png`) |
| Grafik Agregasi | PNG grafik agregasi MAX per data |
| Grafik Defuzzifikasi | PNG grafik centroid per data |
| Logging | Log lengkap → `run.log` |

### 7.2 Mode Web UI — Streamlit (3 Halaman)

#### Halaman 1: INPUT
- Form input manual: Suhu (°C), pH, TDS (ppm)
- Upload Excel untuk input batch (kolom: No, Suhu, pH, TDS)
- Validasi real-time rentang parameter
- Tombol "Jalankan Analisis"

#### Halaman 2: PROSES
- Tampilan transparan 4 tahap inferensi Mamdani:
  - Tabel derajat keanggotaan (fuzzifikasi Suhu, pH, TDS)
  - Tabel 27 rule + fire strength (kolom: IF Suhu, AND pH, AND TDS, THEN Output)
  - Highlight rule aktif (fire strength > 0)
  - Visualisasi kurva agregasi MAX
- Formula matematis ditampilkan tiap tahap

#### Halaman 3: OUTPUT
- Nilai centroid (z*) dengan indikator visual
- Label strategi perawatan
- Grafik defuzzifikasi
- Rekomendasi tindakan perawatan
- Tabel riwayat analisis (kolom TDS ppm)
- Ekspor hasil ke Excel

---

## 8. Validasi Input

| Parameter | Minimum | Maksimum | Satuan |
|-----------|---------|----------|--------|
| Suhu | 0.0 | 50.0 | °C |
| pH | 0.0 | 14.0 | — |
| TDS | 0.0 | 1000.0 | ppm |

Input di luar rentang menghasilkan pesan error yang informatif dan proses dihentikan.

---

## 9. Format Data Input Excel

| No | Suhu | pH | TDS |
|----|------|----|-----|
| 1 | 27.0 | 7.0 | 150 |
| 2 | 30.5 | 6.5 | 450 |
| 3 | 22.0 | 8.2 | 750 |

- Baris header wajib ada
- Nilai numerik (float/int) untuk ketiga parameter
- Kolom `Kekeruhan` lama akan otomatis di-rename ke `TDS` untuk kompatibilitas

---

## 10. Dependensi Teknis

| Library | Versi Min | Kegunaan |
|---------|-----------|----------|
| Python | 3.9+ | Runtime |
| numpy | 1.24.0 | Array, centroid, agregasi |
| pandas | 2.0.0 | Baca/tulis Excel |
| matplotlib | 3.7.0 | Grafik MF dan inferensi |
| openpyxl | 3.1.0 | Engine Excel |
| scipy | 1.10.0 | Operasi saintifik |
| streamlit | latest | UI web |
| pytest | 7.4.0 | Unit testing |

> **Tidak menggunakan `scikit-fuzzy`.** Seluruh perhitungan fuzzy diimplementasikan manual.

---

## 11. Pengujian (Unit Testing)

| File | Cakupan |
|------|---------|
| `test_membership.py` | Triangular MF, shoulder, fuzzifikasi_tds |
| `test_validator.py` | Validasi range TDS 0–1000 ppm |
| `test_inference.py` | Evaluasi rule (kolom tds), fire strength, agregasi |
| `test_defuzzification.py` | Centroid, kategorisasi threshold |

```bash
pytest tests/ -v --cov=fuzzy --cov-report=term-missing
```

---

## 12. Output yang Dihasilkan

| File | Deskripsi |
|------|-----------|
| `output/hasil.xlsx` | Tabel: No, Suhu, pH, TDS (ppm), Centroid, Kategori |
| `output/summary.txt` | Total data, rata-rata centroid, distribusi kategori |
| `output/run.log` | Log lengkap eksekusi |
| `output/graphs/mf_suhu.png` | Grafik MF Suhu |
| `output/graphs/mf_ph.png` | Grafik MF pH |
| `output/graphs/mf_tds.png` | Grafik MF TDS |
| `output/graphs/mf_output.png` | Grafik MF Output |
| `output/graphs/agregasi_NNN.png` | Grafik agregasi data #NNN |
| `output/graphs/defuzzifikasi_NNN.png` | Grafik defuzzifikasi data #NNN |

---

## 13. Kriteria Penerimaan

- [ ] 27 rule terdefinisi dengan kolom `tds` (Rendah / Sedang / Tinggi)
- [ ] `fuzzifikasi_tds()` menghasilkan nilai ∈ [0, 1] untuk semua input valid
- [ ] Triangular MF benar untuk TDS universe [0, 1000] ppm
- [ ] Fire strength menggunakan operator MIN (AND)
- [ ] Agregasi menggunakan operator MAX
- [ ] Defuzzifikasi menggunakan Centroid (Center of Gravity)
- [ ] Diskritisasi: 1000 titik pada universe [0, 100]
- [ ] Kategorisasi: Ringan < 37.5 ≤ Sedang < 62.5 ≤ Intensif
- [ ] Validasi TDS: tolak nilai di luar [0, 1000] ppm
- [ ] Semua unit test lulus (`pytest tests/ -v`)
- [ ] UI Streamlit menampilkan input TDS (ppm) dan label kolom yang benar
- [ ] Grafik `mf_tds.png` dihasilkan di `output/graphs/`

---

## 14. Cara Menjalankan

```bash
# Mode CLI (batch dari Excel)
python main.py

# Mode Web UI (Streamlit)
streamlit run app.py

# Unit Testing
pytest tests/ -v
```

---

*Dokumen ini merupakan spesifikasi resmi proyek AquascapeFuzzy v1.1.0 — Revisi: Kekeruhan (NTU) → TDS (ppm)*
