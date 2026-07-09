"""
fuzzy/rules.py
==============
Basis Aturan (Rule Base) Sistem Fuzzy Mamdani Aquascape.

Berisi 27 aturan IF-THEN yang dibentuk dari kombinasi:
  - 3 kategori Suhu × 3 kategori pH × 3 kategori TDS

Format setiap rule adalah dictionary:
  {
      "suhu":   str,  # Kategori Suhu (Dingin | Normal | Panas)
      "ph":     str,  # Kategori pH   (Asam   | Netral | Basa )
      "tds":    str,  # Kategori TDS  (Rendah | Sedang | Tinggi)
      "output": str,  # Kategori Output (Perawatan Ringan | Sedang | Intensif)
  }

Logika penentuan rule didasarkan pada:
  - Suhu Normal + pH Netral + TDS Rendah → kondisi terbaik → Ringan
  - Salah satu parameter menyimpang → Sedang
  - Dua atau lebih parameter bermasalah, atau satu parameter ekstrem → Intensif

Daftar Rule (27 rule):
"""

from typing import List, Dict

# ---------------------------------------------------------------------------
# RULE BASE — 27 ATURAN FUZZY MAMDANI
# ---------------------------------------------------------------------------
# Urutan: Suhu × pH × TDS (3×3×3 = 27 kombinasi)

RULES: List[Dict[str, str]] = [
    # ===== SUHU: DINGIN =====

    # R1: Dingin + Asam + TDS Rendah → 2 masalah (suhu & pH) → Intensif
    {"suhu": "Dingin", "ph": "Asam",   "tds": "Rendah", "output": "Perawatan Intensif"},

    # R2: Dingin + Asam + TDS Sedang → 3 masalah → Intensif
    {"suhu": "Dingin", "ph": "Asam",   "tds": "Sedang", "output": "Perawatan Intensif"},

    # R3: Dingin + Asam + TDS Tinggi → semua masalah → Intensif
    {"suhu": "Dingin", "ph": "Asam",   "tds": "Tinggi", "output": "Perawatan Intensif"},

    # R4: Dingin + Netral + TDS Rendah → hanya suhu bermasalah → Sedang
    {"suhu": "Dingin", "ph": "Netral", "tds": "Rendah", "output": "Perawatan Sedang"},

    # R5: Dingin + Netral + TDS Sedang → suhu + TDS → Sedang
    {"suhu": "Dingin", "ph": "Netral", "tds": "Sedang", "output": "Perawatan Sedang"},

    # R6: Dingin + Netral + TDS Tinggi → suhu ok tapi TDS tinggi → Intensif
    {"suhu": "Dingin", "ph": "Netral", "tds": "Tinggi", "output": "Perawatan Intensif"},

    # R7: Dingin + Basa + TDS Rendah → 2 masalah (suhu & pH) → Intensif
    {"suhu": "Dingin", "ph": "Basa",   "tds": "Rendah", "output": "Perawatan Intensif"},

    # R8: Dingin + Basa + TDS Sedang → 3 masalah → Intensif
    {"suhu": "Dingin", "ph": "Basa",   "tds": "Sedang", "output": "Perawatan Intensif"},

    # R9: Dingin + Basa + TDS Tinggi → semua bermasalah → Intensif
    {"suhu": "Dingin", "ph": "Basa",   "tds": "Tinggi", "output": "Perawatan Intensif"},

    # ===== SUHU: NORMAL =====

    # R10: Normal + Asam + TDS Rendah → hanya pH bermasalah → Sedang
    {"suhu": "Normal", "ph": "Asam",   "tds": "Rendah", "output": "Perawatan Sedang"},

    # R11: Normal + Asam + TDS Sedang → pH + TDS → Intensif
    {"suhu": "Normal", "ph": "Asam",   "tds": "Sedang", "output": "Perawatan Intensif"},

    # R12: Normal + Asam + TDS Tinggi → pH buruk + TDS tinggi → Intensif
    {"suhu": "Normal", "ph": "Asam",   "tds": "Tinggi", "output": "Perawatan Intensif"},

    # R13: Normal + Netral + TDS Rendah → kondisi ideal → Ringan
    {"suhu": "Normal", "ph": "Netral", "tds": "Rendah", "output": "Perawatan Ringan"},

    # R14: Normal + Netral + TDS Sedang → hanya TDS agak tinggi → Sedang
    {"suhu": "Normal", "ph": "Netral", "tds": "Sedang", "output": "Perawatan Sedang"},

    # R15: Normal + Netral + TDS Tinggi → suhu & pH bagus tapi TDS tinggi → Sedang
    {"suhu": "Normal", "ph": "Netral", "tds": "Tinggi", "output": "Perawatan Sedang"},

    # R16: Normal + Basa + TDS Rendah → hanya pH bermasalah → Sedang
    {"suhu": "Normal", "ph": "Basa",   "tds": "Rendah", "output": "Perawatan Sedang"},

    # R17: Normal + Basa + TDS Sedang → pH + TDS → Intensif
    {"suhu": "Normal", "ph": "Basa",   "tds": "Sedang", "output": "Perawatan Intensif"},

    # R18: Normal + Basa + TDS Tinggi → pH buruk + TDS tinggi → Intensif
    {"suhu": "Normal", "ph": "Basa",   "tds": "Tinggi", "output": "Perawatan Intensif"},

    # ===== SUHU: PANAS =====

    # R19: Panas + Asam + TDS Rendah → 2 masalah (suhu & pH) → Intensif
    {"suhu": "Panas",  "ph": "Asam",   "tds": "Rendah", "output": "Perawatan Intensif"},

    # R20: Panas + Asam + TDS Sedang → 3 masalah → Intensif
    {"suhu": "Panas",  "ph": "Asam",   "tds": "Sedang", "output": "Perawatan Intensif"},

    # R21: Panas + Asam + TDS Tinggi → semua bermasalah → Intensif
    {"suhu": "Panas",  "ph": "Asam",   "tds": "Tinggi", "output": "Perawatan Intensif"},

    # R22: Panas + Netral + TDS Rendah → hanya suhu bermasalah → Sedang
    {"suhu": "Panas",  "ph": "Netral", "tds": "Rendah", "output": "Perawatan Sedang"},

    # R23: Panas + Netral + TDS Sedang → suhu + TDS → Intensif
    {"suhu": "Panas",  "ph": "Netral", "tds": "Sedang", "output": "Perawatan Intensif"},

    # R24: Panas + Netral + TDS Tinggi → suhu buruk + TDS tinggi → Intensif
    {"suhu": "Panas",  "ph": "Netral", "tds": "Tinggi", "output": "Perawatan Intensif"},

    # R25: Panas + Basa + TDS Rendah → 2 masalah (suhu & pH) → Intensif
    {"suhu": "Panas",  "ph": "Basa",   "tds": "Rendah", "output": "Perawatan Intensif"},

    # R26: Panas + Basa + TDS Sedang → 3 masalah → Intensif
    {"suhu": "Panas",  "ph": "Basa",   "tds": "Sedang", "output": "Perawatan Intensif"},

    # R27: Panas + Basa + TDS Tinggi → semua bermasalah → Intensif
    {"suhu": "Panas",  "ph": "Basa",   "tds": "Tinggi", "output": "Perawatan Intensif"},
]


def get_rules() -> List[Dict[str, str]]:
    """Mengembalikan seluruh rule base fuzzy Mamdani.

    Returns:
        List berisi 27 rule dalam format dictionary.
    """
    return RULES


def print_rules() -> None:
    """Mencetak seluruh rule ke konsol dalam format yang mudah dibaca."""
    print("=" * 70)
    print(f"{'RULE BASE — SISTEM FUZZY MAMDANI AQUASCAPE':^70}")
    print(f"{'Total: 27 Aturan Fuzzy':^70}")
    print("=" * 70)
    for i, rule in enumerate(RULES, start=1):
        print(
            f"R{i:>2}. IF Suhu={rule['suhu']:<7} "
            f"AND pH={rule['ph']:<7} "
            f"AND TDS={rule['tds']:<7} "
            f"THEN {rule['output']}"
        )
    print("=" * 70)
