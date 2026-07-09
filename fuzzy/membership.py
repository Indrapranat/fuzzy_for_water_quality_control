"""
fuzzy/membership.py
===================
Implementasi Fungsi Keanggotaan Triangular (Triangular Membership Function).

Modul ini berisi fungsi-fungsi murni (pure functions) untuk menghitung
derajat keanggotaan setiap variabel fuzzy menggunakan representasi
fungsi segitiga (triangular).

Rumus Triangular MF:
    Untuk x terhadap segitiga (a, b, c):

        μ(x) = 0,                      jika x <= a atau x >= c
        μ(x) = (x - a) / (b - a),     jika a < x <= b
        μ(x) = (c - x) / (c - b),     jika b < x < c
        μ(x) = 1,                      jika x == b
"""

import numpy as np
from typing import Dict, Tuple
import config


def triangular_mf(x: float, a: float, b: float, c: float) -> float:
    """Menghitung derajat keanggotaan dengan fungsi triangular.

    Args:
        x: Nilai crisp yang akan difuzzifikasi.
        a: Titik kaki kiri segitiga (μ = 0 saat x <= a).
        b: Titik puncak segitiga (μ = 1 saat x == b).
        c: Titik kaki kanan segitiga (μ = 0 saat x >= c).

    Returns:
        Derajat keanggotaan dalam rentang [0, 1].

    Raises:
        ValueError: Jika a > b atau b > c (parameter tidak valid).

    Examples:
        >>> triangular_mf(27.0, 24.0, 27.0, 30.0)
        1.0
        >>> triangular_mf(25.5, 24.0, 27.0, 30.0)
        0.5
    """
    if a > b or b > c:
        raise ValueError(
            f"Parameter segitiga tidak valid: a={a}, b={b}, c={c}. "
            f"Wajib memenuhi a <= b <= c."
        )

    # Shoulder kiri: a == b → kurva dimulai dari 1 di titik a dan turun ke c
    # Shoulder kanan: b == c → kurva naik dari a ke b dan tetap 1 di b=c
    # Handle titik tepat di a atau c

    # Nilai di luar range kiri (tapi hanya jika bukan shoulder kiri)
    if x < a:
        return 0.0

    # Nilai di luar range kanan (tapi hanya jika bukan shoulder kanan)
    if x > c:
        return 0.0

    # Shoulder kiri (a == b): seluruh area dari a hingga c = 1
    if a == b:
        # Sisi turun: dari b menuju c
        if x < c:
            if c == b:
                return 1.0
            return float((c - x) / (c - b))
        return 0.0  # x == c

    # Shoulder kanan (b == c): seluruh area dari a ke b = 1
    if b == c:
        # Sisi naik: dari a menuju b
        if x <= b:
            if b == a:
                return 1.0
            return float((x - a) / (b - a))
        return 0.0  # x > c tidak mungkin sudah ditangani di atas

    # Triangular biasa: a < b < c
    if x == a or x >= c:
        return 0.0

    # Sisi naik: dari a menuju puncak b
    if a < x <= b:
        return float((x - a) / (b - a))

    # Sisi turun: dari puncak b menuju c
    if b < x < c:
        return float((c - x) / (c - b))

    return 0.0


def triangular_mf_array(
    x_array: np.ndarray, a: float, b: float, c: float
) -> np.ndarray:
    """Menghitung derajat keanggotaan triangular untuk array NumPy.

    Versi vektorisasi dari triangular_mf untuk keperluan plotting
    dan perhitungan agregasi pada universe of discourse.

    Args:
        x_array: Array nilai crisp (numpy array).
        a: Titik kaki kiri segitiga.
        b: Titik puncak segitiga.
        c: Titik kaki kanan segitiga.

    Returns:
        Array derajat keanggotaan dengan dimensi sama seperti x_array.
    """
    mu = np.zeros_like(x_array, dtype=float)

    # Sisi naik: a < x <= b
    mask_naik = (x_array > a) & (x_array <= b)
    if b != a:
        mu[mask_naik] = (x_array[mask_naik] - a) / (b - a)
    else:
        mu[mask_naik] = 1.0

    # Sisi turun: b < x < c
    mask_turun = (x_array > b) & (x_array < c)
    if c != b:
        mu[mask_turun] = (c - x_array[mask_turun]) / (c - b)
    else:
        mu[mask_turun] = 1.0

    return mu


# ---------------------------------------------------------------------------
# FUZZIFIKASI VARIABEL INPUT
# ---------------------------------------------------------------------------

def fuzzifikasi_suhu(nilai_suhu: float) -> Dict[str, float]:
    """Menghitung derajat keanggotaan untuk variabel Suhu.

    Menggunakan parameter fungsi keanggotaan dari config.SUHU_MF.

    Args:
        nilai_suhu: Nilai suhu dalam derajat Celsius.

    Returns:
        Dictionary dengan kunci nama kategori dan nilai derajat keanggotaan.
        Contoh: {"Dingin": 0.0, "Normal": 1.0, "Panas": 0.0}
    """
    hasil: Dict[str, float] = {}
    for kategori, (a, b, c) in config.SUHU_MF.items():
        hasil[kategori] = triangular_mf(nilai_suhu, a, b, c)
    return hasil


def fuzzifikasi_ph(nilai_ph: float) -> Dict[str, float]:
    """Menghitung derajat keanggotaan untuk variabel pH.

    Menggunakan parameter fungsi keanggotaan dari config.PH_MF.

    Args:
        nilai_ph: Nilai pH air.

    Returns:
        Dictionary dengan kunci nama kategori dan nilai derajat keanggotaan.
        Contoh: {"Asam": 0.0, "Netral": 1.0, "Basa": 0.0}
    """
    hasil: Dict[str, float] = {}
    for kategori, (a, b, c) in config.PH_MF.items():
        hasil[kategori] = triangular_mf(nilai_ph, a, b, c)
    return hasil


def fuzzifikasi_tds(nilai_tds: float) -> Dict[str, float]:
    """Menghitung derajat keanggotaan untuk variabel TDS.

    Menggunakan parameter fungsi keanggotaan dari config.TDS_MF.

    Args:
        nilai_tds: Nilai TDS dalam satuan ppm.

    Returns:
        Dictionary dengan kunci nama kategori dan nilai derajat keanggotaan.
        Contoh: {"Rendah": 1.0, "Sedang": 0.0, "Tinggi": 0.0}
    """
    hasil: Dict[str, float] = {}
    for kategori, (a, b, c) in config.TDS_MF.items():
        hasil[kategori] = triangular_mf(nilai_tds, a, b, c)
    return hasil


# Alias backward-compatible
def fuzzifikasi_kekeruhan(nilai_kekeruhan: float) -> Dict[str, float]:
    """Alias untuk fuzzifikasi_tds (backward-compatible)."""
    return fuzzifikasi_tds(nilai_kekeruhan)


def get_output_mf_array(
    x_array: np.ndarray,
) -> Dict[str, np.ndarray]:
    """Menghitung array fungsi keanggotaan untuk semua kategori output.

    Digunakan dalam proses defuzzifikasi untuk membangun
    universe of discourse output.

    Args:
        x_array: Array titik diskrit pada universe output [0, 100].

    Returns:
        Dictionary berisi array keanggotaan untuk setiap kategori output.
    """
    hasil: Dict[str, np.ndarray] = {}
    for kategori, (a, b, c) in config.OUTPUT_MF.items():
        hasil[kategori] = triangular_mf_array(x_array, a, b, c)
    return hasil
