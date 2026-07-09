"""
config.py
=========
Konfigurasi terpusat untuk seluruh project AquascapeFuzzy.

Berisi parameter fungsi keanggotaan, path file, dan pengaturan output.
Digunakan oleh seluruh modul agar tidak ada nilai magic number yang tersebar.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# PATH KONFIGURASI
# ---------------------------------------------------------------------------

BASE_DIR: Path = Path(__file__).parent.resolve()
DATA_DIR: Path = BASE_DIR / "data"
OUTPUT_DIR: Path = BASE_DIR / "output"
GRAPHS_DIR: Path = OUTPUT_DIR / "graphs"

INPUT_FILE: Path = DATA_DIR / "data.xlsx"
OUTPUT_FILE: Path = OUTPUT_DIR / "hasil.xlsx"
SUMMARY_FILE: Path = OUTPUT_DIR / "summary.txt"

# ---------------------------------------------------------------------------
# PARAMETER FUNGSI KEANGGOTAAN — INPUT 1: SUHU (°C)
# ---------------------------------------------------------------------------
# Format triangular: (a, b, c) → titik kiri, puncak, titik kanan

SUHU_MF = {
    "Dingin": (0.0, 0.0, 26.0),    # Dingin: 0 - 0 - 26
    "Normal": (24.0, 27.0, 30.0),  # Normal: 24 - 27 - 30
    "Panas": (28.0, 50.0, 50.0),   # Panas: 28 - 50 - 50
}

# Batas validasi suhu
SUHU_MIN: float = 0.0
SUHU_MAX: float = 50.0

# ---------------------------------------------------------------------------
# PARAMETER FUNGSI KEANGGOTAAN — INPUT 2: pH
# ---------------------------------------------------------------------------

PH_MF = {
    "Asam": (0.0, 0.0, 7.0),       # Asam: 0 - 0 - 7
    "Netral": (6.0, 7.0, 8.0),     # Netral: 6 - 7 - 8
    "Basa": (7.0, 14.0, 14.0),     # Basa: 7 - 14 - 14
}

# Batas validasi pH
PH_MIN: float = 0.0
PH_MAX: float = 14.0

# ---------------------------------------------------------------------------
# PARAMETER FUNGSI KEANGGOTAAN — INPUT 3: TDS (ppm)
# ---------------------------------------------------------------------------

TDS_MF = {
    "Rendah": (0.0, 0.0, 200.0),      # Rendah: 0 - 0 - 200
    "Sedang": (100.0, 300.0, 500.0),  # Sedang: 100 - 300 - 500
    "Tinggi": (400.0, 1000.0, 1000.0), # Tinggi: 400 - 1000 - 1000
}

# Alias backward-compatible
KEKERUHAN_MF = TDS_MF

# Batas validasi TDS
TDS_MIN: float = 0.0
TDS_MAX: float = 1000.0
KEKERUHAN_MIN: float = TDS_MIN
KEKERUHAN_MAX: float = TDS_MAX

# ---------------------------------------------------------------------------
# PARAMETER FUNGSI KEANGGOTAAN — OUTPUT: STRATEGI PERAWATAN
# ---------------------------------------------------------------------------

OUTPUT_MF = {
    "Perawatan Ringan": (0.0, 0.0, 50.0),     # Ringan: 0 - 0 - 50
    "Perawatan Sedang": (25.0, 50.0, 75.0),   # Sedang: 25 - 50 - 75
    "Perawatan Intensif": (50.0, 100.0, 100.0), # Intensif: 50 - 100 - 100
}

# Range universe of discourse untuk output defuzzifikasi
OUTPUT_MIN: float = 0.0
OUTPUT_MAX: float = 100.0
OUTPUT_RESOLUTION: int = 1000  # Jumlah titik diskritisasi

# ---------------------------------------------------------------------------
# PENGATURAN GRAFIK
# ---------------------------------------------------------------------------

GRAPH_DPI: int = 300
GRAPH_FORMAT: str = "png"
GRAPH_STYLE: str = "seaborn-v0_8-whitegrid"

# Warna untuk setiap kategori membership function
COLOR_PALETTE = {
    # Suhu
    "Dingin": "#4FC3F7",
    "Normal": "#66BB6A",
    "Panas": "#EF5350",
    # pH
    "Asam": "#FF7043",
    "Netral": "#26C6DA",
    "Basa": "#7E57C2",
    # TDS
    "Rendah": "#29B6F6",
    "Sedang": "#FFA726",
    "Tinggi": "#8D6E63",
    # Output
    "Perawatan Ringan": "#66BB6A",
    "Perawatan Sedang": "#FFA726",
    "Perawatan Intensif": "#EF5350",
}

# ---------------------------------------------------------------------------
# PENGATURAN LOGGING
# ---------------------------------------------------------------------------

LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
