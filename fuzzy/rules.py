"""
fuzzy/rules.py
==============
Basis Aturan (Rule Base) Sistem Fuzzy Mamdani Aquascape.

Berisi 27 aturan IF-THEN yang dibentuk dari kombinasi:
  - 3 kategori Suhu × 3 kategori pH × 3 kategori Kekeruhan

Format setiap rule adalah dictionary:
  {
      "suhu":      str,   # Kategori Suhu (Dingin | Normal | Panas)
      "ph":        str,   # Kategori pH   (Asam   | Netral | Basa )
      "kekeruhan": str,   # Kategori Kekeruhan (Jernih | Sedang | Keruh)
      "output":    str,   # Kategori Output    (Perawatan Ringan | Sedang | Intensif)
  }

Logika penentuan rule didasarkan pada:
  - Suhu Normal + pH Netral + Kekeruhan Jernih → kondisi terbaik → Ringan
  - Salah satu parameter menyimpang → Sedang
  - Dua atau lebih parameter bermasalah, atau satu parameter ekstrem → Intensif

Daftar Rule (27 rule):
"""

from typing import List, Dict

# ---------------------------------------------------------------------------
# RULE BASE — 27 ATURAN FUZZY MAMDANI
# ---------------------------------------------------------------------------
# Urutan: Suhu × pH × Kekeruhan (3×3×3 = 27 kombinasi)

RULES: List[Dict[str, str]] = [
    # ===== SUHU: DINGIN =====

    # R1: Dingin + Asam + Jernih → 2 masalah (suhu & pH) → Intensif
    {"suhu": "Dingin", "ph": "Asam",   "kekeruhan": "Jernih", "output": "Perawatan Intensif"},

    # R2: Dingin + Asam + Sedang → 3 masalah → Intensif
    {"suhu": "Dingin", "ph": "Asam",   "kekeruhan": "Sedang", "output": "Perawatan Intensif"},

    # R3: Dingin + Asam + Keruh → semua masalah → Intensif
    {"suhu": "Dingin", "ph": "Asam",   "kekeruhan": "Keruh",  "output": "Perawatan Intensif"},

    # R4: Dingin + Netral + Jernih → hanya suhu bermasalah → Sedang
    {"suhu": "Dingin", "ph": "Netral", "kekeruhan": "Jernih", "output": "Perawatan Sedang"},

    # R5: Dingin + Netral + Sedang → suhu + kekeruhan → Sedang
    {"suhu": "Dingin", "ph": "Netral", "kekeruhan": "Sedang", "output": "Perawatan Sedang"},

    # R6: Dingin + Netral + Keruh → suhu ok tapi keruh → Intensif
    {"suhu": "Dingin", "ph": "Netral", "kekeruhan": "Keruh",  "output": "Perawatan Intensif"},

    # R7: Dingin + Basa + Jernih → 2 masalah (suhu & pH) → Intensif
    {"suhu": "Dingin", "ph": "Basa",   "kekeruhan": "Jernih", "output": "Perawatan Intensif"},

    # R8: Dingin + Basa + Sedang → 3 masalah → Intensif
    {"suhu": "Dingin", "ph": "Basa",   "kekeruhan": "Sedang", "output": "Perawatan Intensif"},

    # R9: Dingin + Basa + Keruh → semua bermasalah → Intensif
    {"suhu": "Dingin", "ph": "Basa",   "kekeruhan": "Keruh",  "output": "Perawatan Intensif"},

    # ===== SUHU: NORMAL =====

    # R10: Normal + Asam + Jernih → hanya pH bermasalah → Sedang
    {"suhu": "Normal", "ph": "Asam",   "kekeruhan": "Jernih", "output": "Perawatan Sedang"},

    # R11: Normal + Asam + Sedang → pH + kekeruhan → Intensif
    {"suhu": "Normal", "ph": "Asam",   "kekeruhan": "Sedang", "output": "Perawatan Intensif"},

    # R12: Normal + Asam + Keruh → pH buruk + keruh → Intensif
    {"suhu": "Normal", "ph": "Asam",   "kekeruhan": "Keruh",  "output": "Perawatan Intensif"},

    # R13: Normal + Netral + Jernih → kondisi ideal → Ringan
    {"suhu": "Normal", "ph": "Netral", "kekeruhan": "Jernih", "output": "Perawatan Ringan"},

    # R14: Normal + Netral + Sedang → hanya kekeruhan agak keruh → Sedang
    {"suhu": "Normal", "ph": "Netral", "kekeruhan": "Sedang", "output": "Perawatan Sedang"},

    # R15: Normal + Netral + Keruh → suhu & pH bagus tapi keruh → Sedang
    {"suhu": "Normal", "ph": "Netral", "kekeruhan": "Keruh",  "output": "Perawatan Sedang"},

    # R16: Normal + Basa + Jernih → hanya pH bermasalah → Sedang
    {"suhu": "Normal", "ph": "Basa",   "kekeruhan": "Jernih", "output": "Perawatan Sedang"},

    # R17: Normal + Basa + Sedang → pH + kekeruhan → Intensif
    {"suhu": "Normal", "ph": "Basa",   "kekeruhan": "Sedang", "output": "Perawatan Intensif"},

    # R18: Normal + Basa + Keruh → pH buruk + keruh → Intensif
    {"suhu": "Normal", "ph": "Basa",   "kekeruhan": "Keruh",  "output": "Perawatan Intensif"},

    # ===== SUHU: PANAS =====

    # R19: Panas + Asam + Jernih → 2 masalah (suhu & pH) → Intensif
    {"suhu": "Panas",  "ph": "Asam",   "kekeruhan": "Jernih", "output": "Perawatan Intensif"},

    # R20: Panas + Asam + Sedang → 3 masalah → Intensif
    {"suhu": "Panas",  "ph": "Asam",   "kekeruhan": "Sedang", "output": "Perawatan Intensif"},

    # R21: Panas + Asam + Keruh → semua bermasalah → Intensif
    {"suhu": "Panas",  "ph": "Asam",   "kekeruhan": "Keruh",  "output": "Perawatan Intensif"},

    # R22: Panas + Netral + Jernih → hanya suhu bermasalah → Sedang
    {"suhu": "Panas",  "ph": "Netral", "kekeruhan": "Jernih", "output": "Perawatan Sedang"},

    # R23: Panas + Netral + Sedang → suhu + kekeruhan → Intensif
    {"suhu": "Panas",  "ph": "Netral", "kekeruhan": "Sedang", "output": "Perawatan Intensif"},

    # R24: Panas + Netral + Keruh → suhu buruk + keruh → Intensif
    {"suhu": "Panas",  "ph": "Netral", "kekeruhan": "Keruh",  "output": "Perawatan Intensif"},

    # R25: Panas + Basa + Jernih → 2 masalah (suhu & pH) → Intensif
    {"suhu": "Panas",  "ph": "Basa",   "kekeruhan": "Jernih", "output": "Perawatan Intensif"},

    # R26: Panas + Basa + Sedang → 3 masalah → Intensif
    {"suhu": "Panas",  "ph": "Basa",   "kekeruhan": "Sedang", "output": "Perawatan Intensif"},

    # R27: Panas + Basa + Keruh → semua bermasalah → Intensif
    {"suhu": "Panas",  "ph": "Basa",   "kekeruhan": "Keruh",  "output": "Perawatan Intensif"},
]


def get_rules() -> List[Dict[str, str]]:
    """Mengembalikan seluruh rule base fuzzy Mamdani.

    Returns:
        List berisi 27 rule dalam format dictionary.
    """
    return RULES


def print_rules() -> None:
    """Mencetak seluruh rule ke konsol dalam format yang mudah dibaca.

    Digunakan untuk dokumentasi dan verifikasi rule base.
    """
    print("=" * 70)
    print(f"{'RULE BASE — SISTEM FUZZY MAMDANI AQUASCAPE':^70}")
    print(f"{'Total: 27 Aturan Fuzzy':^70}")
    print("=" * 70)
    for i, rule in enumerate(RULES, start=1):
        print(
            f"R{i:>2}. IF Suhu={rule['suhu']:<7} "
            f"AND pH={rule['ph']:<7} "
            f"AND Kekeruhan={rule['kekeruhan']:<7} "
            f"THEN {rule['output']}"
        )
    print("=" * 70)
