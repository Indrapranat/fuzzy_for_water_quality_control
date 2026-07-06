"""
fuzzy/defuzzification.py
========================
Implementasi Defuzzifikasi menggunakan Metode Centroid (Center of Gravity).

Metode Centroid mengubah fungsi keanggotaan agregasi (yang merupakan
sebuah kurva) menjadi satu nilai crisp tunggal yang merepresentasikan
strategi perawatan yang direkomendasikan.

Rumus Centroid (Center of Gravity):
                    Σ [x_i × μ(x_i)]
    z* = ─────────────────────────────────
                      Σ μ(x_i)

Keterangan:
    z*      = Nilai crisp output (nilai defuzzifikasi)
    x_i     = Titik ke-i pada universe of discourse output
    μ(x_i)  = Derajat keanggotaan agregasi pada titik x_i
    Σ       = Penjumlahan atas seluruh titik diskrit

Semakin banyak titik diskritisasi, semakin akurat hasil centroid.
Dalam project ini digunakan OUTPUT_RESOLUTION = 1000 titik (lihat config.py).
"""

import numpy as np
from typing import Tuple
import logging

import config

logger = logging.getLogger(__name__)


def centroid(
    x_output: np.ndarray,
    mu_agregasi: np.ndarray,
) -> Tuple[float, str]:
    """Menghitung nilai defuzzifikasi menggunakan metode Centroid.

    Mengimplementasikan rumus Center of Gravity secara manual dengan
    NumPy agar seluruh perhitungan transparan dan dapat ditelusuri.

    Args:
        x_output: Array titik diskrit universe of discourse output [0, 100].
        mu_agregasi: Array derajat keanggotaan hasil agregasi MAX.

    Returns:
        Tuple berisi:
        - nilai_centroid (float): Nilai crisp hasil defuzzifikasi [0, 100].
          Jika denominator = 0 (tidak ada rule aktif), dikembalikan 0.0.
        - kategori (str): Label strategi perawatan berdasarkan threshold.

    Raises:
        ValueError: Jika dimensi x_output dan mu_agregasi tidak sama.
    """
    if x_output.shape != mu_agregasi.shape:
        raise ValueError(
            f"Dimensi x_output ({x_output.shape}) dan "
            f"mu_agregasi ({mu_agregasi.shape}) harus sama."
        )

    # -----------------------------------------------------------------------
    # HITUNG CENTROID
    #
    # Pembilang (Numerator):   Σ [x_i × μ(x_i)]
    # Penyebut  (Denominator): Σ μ(x_i)
    # -----------------------------------------------------------------------
    numerator: float = float(np.sum(x_output * mu_agregasi))
    denominator: float = float(np.sum(mu_agregasi))

    if denominator == 0.0:
        logger.warning(
            "Denominator centroid = 0. Tidak ada rule yang aktif. "
            "Nilai centroid dikembalikan sebagai 0.0."
        )
        nilai_centroid = 0.0
    else:
        # Rumus centroid: z* = Σ(x_i × μ(x_i)) / Σ(μ(x_i))
        nilai_centroid = numerator / denominator

    logger.debug(
        "Centroid → Numerator=%.4f, Denominator=%.4f, z*=%.4f",
        numerator,
        denominator,
        nilai_centroid,
    )

    kategori = tentukan_kategori(nilai_centroid)
    return nilai_centroid, kategori


def tentukan_kategori(nilai_centroid: float) -> str:
    """Menentukan label kategori strategi perawatan dari nilai centroid.

    Pembagian threshold berdasarkan titik persimpangan fungsi keanggotaan
    output yang telah didefinisikan di config.OUTPUT_MF:
        - Perawatan Ringan  : 0  – 37.5 (centroid dominan di sisi Ringan)
        - Perawatan Sedang  : 37.5 – 62.5 (centroid di tengah)
        - Perawatan Intensif: 62.5 – 100 (centroid dominan di sisi Intensif)

    Args:
        nilai_centroid: Nilai crisp hasil defuzzifikasi [0, 100].

    Returns:
        Label kategori strategi perawatan sebagai string.
    """
    if nilai_centroid < 37.5:
        return "Perawatan Ringan"
    elif nilai_centroid < 62.5:
        return "Perawatan Sedang"
    else:
        return "Perawatan Intensif"
