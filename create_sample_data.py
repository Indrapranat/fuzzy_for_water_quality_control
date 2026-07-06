"""
Script untuk membuat file data/data.xlsx dengan data sampel.

Jalankan sekali saja:
    python create_sample_data.py
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 20 data sampel yang bervariasi untuk pengujian
data = {
    "No": list(range(1, 21)),
    "Suhu": [
        27.0, 30.5, 22.0, 28.0, 35.0,
        26.0, 24.5, 31.0, 20.0, 27.5,
        29.0, 23.0, 33.0, 27.0, 19.0,
        28.5, 26.5, 32.0, 25.0, 27.0,
    ],
    "pH": [
        7.0, 6.5, 8.2, 7.0, 4.5,
        7.2, 6.8, 8.5, 7.0, 7.0,
        6.0, 7.5, 5.5, 7.0, 7.8,
        6.2, 7.1, 8.0, 6.9, 7.0,
    ],
    "Kekeruhan": [
        10.0, 45.0, 80.0, 20.0, 90.0,
        5.0, 35.0, 70.0, 15.0, 25.0,
        60.0, 10.0, 85.0, 0.0, 50.0,
        30.0, 8.0, 75.0, 40.0, 55.0,
    ],
}

df = pd.DataFrame(data)
output_path = DATA_DIR / "data.xlsx"
df.to_excel(output_path, index=False, engine="openpyxl")
print(f"[OK] File data sampel berhasil dibuat: {output_path}")
print(f"   Total: {len(df)} baris data")
