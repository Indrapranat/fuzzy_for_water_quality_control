"""
fuzzy/validator.py
==================
Modul Validasi Data Input.

Memastikan setiap nilai input berada dalam rentang universe of discourse
yang telah ditetapkan dalam penelitian. Data yang tidak valid akan
ditolak sebelum memasuki proses fuzzifikasi.

Rentang validasi:
    - Suhu : 0 – 50 °C
    - pH   : 0 – 14
    - TDS  : 0 – 1000 ppm
"""

from typing import List, Tuple, Optional
import pandas as pd
import logging

import config

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Exception khusus untuk kesalahan validasi data input.

    Attributes:
        baris: Nomor baris data yang bermasalah (1-indexed).
        pesan: Pesan kesalahan detail.
    """

    def __init__(self, baris: int, pesan: str) -> None:
        """Inisialisasi ValidationError.

        Args:
            baris: Nomor baris data yang bermasalah.
            pesan: Pesan kesalahan detail.
        """
        self.baris = baris
        self.pesan = pesan
        super().__init__(f"[Baris {baris}] {pesan}")


def validasi_suhu(nilai: float, baris: int) -> None:
    """Memvalidasi nilai suhu.

    Args:
        nilai: Nilai suhu dalam derajat Celsius.
        baris: Nomor baris data (untuk pesan error).

    Raises:
        ValidationError: Jika nilai suhu di luar rentang [0, 50].
        ValidationError: Jika nilai suhu bukan tipe numerik.
    """
    if not isinstance(nilai, (int, float)):
        raise ValidationError(
            baris,
            f"Suhu harus berupa angka, ditemukan: {type(nilai).__name__} = '{nilai}'"
        )
    if pd.isna(nilai):
        raise ValidationError(baris, "Nilai Suhu tidak boleh kosong (NaN).")
    if not (config.SUHU_MIN <= nilai <= config.SUHU_MAX):
        raise ValidationError(
            baris,
            f"Suhu={nilai}°C di luar rentang valid "
            f"[{config.SUHU_MIN}, {config.SUHU_MAX}]°C."
        )


def validasi_ph(nilai: float, baris: int) -> None:
    """Memvalidasi nilai pH.

    Args:
        nilai: Nilai pH air.
        baris: Nomor baris data (untuk pesan error).

    Raises:
        ValidationError: Jika nilai pH di luar rentang [0, 14].
        ValidationError: Jika nilai pH bukan tipe numerik.
    """
    if not isinstance(nilai, (int, float)):
        raise ValidationError(
            baris,
            f"pH harus berupa angka, ditemukan: {type(nilai).__name__} = '{nilai}'"
        )
    if pd.isna(nilai):
        raise ValidationError(baris, "Nilai pH tidak boleh kosong (NaN).")
    if not (config.PH_MIN <= nilai <= config.PH_MAX):
        raise ValidationError(
            baris,
            f"pH={nilai} di luar rentang valid "
            f"[{config.PH_MIN}, {config.PH_MAX}]."
        )


def validasi_tds(nilai: float, baris: int) -> None:
    """Memvalidasi nilai TDS.

    Args:
        nilai: Nilai TDS dalam satuan ppm.
        baris: Nomor baris data (untuk pesan error).

    Raises:
        ValidationError: Jika nilai TDS di luar rentang [0, 1000].
        ValidationError: Jika nilai TDS bukan tipe numerik.
    """
    if not isinstance(nilai, (int, float)):
        raise ValidationError(
            baris,
            f"TDS harus berupa angka, ditemukan: {type(nilai).__name__} = '{nilai}'"
        )
    if pd.isna(nilai):
        raise ValidationError(baris, "Nilai TDS tidak boleh kosong (NaN).")
    if not (config.TDS_MIN <= nilai <= config.TDS_MAX):
        raise ValidationError(
            baris,
            f"TDS={nilai} ppm di luar rentang valid "
            f"[{config.TDS_MIN}, {config.TDS_MAX}] ppm."
        )


# Alias backward-compatible
validasi_kekeruhan = validasi_tds


def validasi_baris(
    no: int,
    suhu: float,
    ph: float,
    tds: float,
) -> None:
    """Memvalidasi satu baris data input secara lengkap.

    Args:
        no: Nomor urut data.
        suhu: Nilai suhu (°C).
        ph: Nilai pH.
        tds: Nilai TDS (ppm).

    Raises:
        ValidationError: Jika salah satu nilai tidak valid.
    """
    validasi_suhu(suhu, no)
    validasi_ph(ph, no)
    validasi_tds(tds, no)
    logger.debug("Validasi baris %d: OK (Suhu=%.2f, pH=%.2f, TDS=%.2f)", no, suhu, ph, tds)


def validasi_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """Memvalidasi seluruh DataFrame input.

    Memeriksa:
    1. Keberadaan kolom wajib: No, Suhu, pH, Kekeruhan.
    2. Setiap nilai pada kolom Suhu, pH, Kekeruhan.

    Args:
        df: DataFrame yang dibaca dari data/data.xlsx.

    Returns:
        Tuple berisi:
        - DataFrame yang sudah divalidasi (baris tidak valid dibuang).
        - List pesan error untuk setiap baris yang tidak valid.

    Raises:
        ValueError: Jika kolom wajib tidak ditemukan di file Excel.
    """
    kolom_wajib = ["No", "Suhu", "pH", "TDS"]
    kolom_hilang = [k for k in kolom_wajib if k not in df.columns]
    if kolom_hilang:
        # Cek juga kolom lama 'Kekeruhan' untuk kompatibilitas
        if "Kekeruhan" in df.columns and "TDS" not in df.columns:
            df = df.rename(columns={"Kekeruhan": "TDS"})
            kolom_hilang = []
        else:
            raise ValueError(
                f"Kolom wajib tidak ditemukan: {kolom_hilang}. "
                f"Kolom yang tersedia: {list(df.columns)}"
            )

    baris_valid: List[int] = []
    pesan_error: List[str] = []

    for idx, row in df.iterrows():
        no = int(row["No"])
        try:
            suhu = float(row["Suhu"])
            ph = float(row["pH"])
            tds = float(row["TDS"])
            validasi_baris(no, suhu, ph, tds)
            baris_valid.append(idx)  # type: ignore[arg-type]
        except ValidationError as e:
            pesan = str(e)
            pesan_error.append(pesan)
            logger.warning("Data tidak valid: %s", pesan)
        except (ValueError, TypeError) as e:
            pesan = f"[Baris {no}] Konversi tipe data gagal: {e}"
            pesan_error.append(pesan)
            logger.warning("Data tidak valid: %s", pesan)

    df_valid = df.loc[baris_valid].reset_index(drop=True)

    if pesan_error:
        logger.warning(
            "%d baris data tidak valid dan dilewati.", len(pesan_error)
        )
    else:
        logger.info("Semua %d baris data valid.", len(df_valid))

    return df_valid, pesan_error
