"""
utils/excel.py
==============
Modul untuk operasi baca/tulis file Excel menggunakan pandas dan openpyxl.

Bertanggung jawab atas:
1. Membaca data input dari data/data.xlsx.
2. Menulis hasil analisis ke output/hasil.xlsx.
3. Menulis summary ke output/summary.txt.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

import pandas as pd

import config

logger = logging.getLogger(__name__)


def baca_data(path: Path = config.INPUT_FILE) -> pd.DataFrame:
    """Membaca file Excel data input.

    Args:
        path: Path ke file Excel input. Default: config.INPUT_FILE.

    Returns:
        DataFrame berisi kolom No, Suhu, pH, Kekeruhan.

    Raises:
        FileNotFoundError: Jika file tidak ditemukan pada path yang diberikan.
        ValueError: Jika file Excel tidak dapat dibaca (format salah).
    """
    if not path.exists():
        raise FileNotFoundError(
            f"File data tidak ditemukan: {path}\n"
            f"Pastikan file 'data.xlsx' ada di folder 'data/'."
        )

    try:
        df = pd.read_excel(path, engine="openpyxl")
        logger.info("Data berhasil dibaca dari: %s (%d baris)", path, len(df))
        return df
    except Exception as exc:
        raise ValueError(
            f"Gagal membaca file Excel '{path}': {exc}"
        ) from exc


def tulis_hasil(
    hasil_list: List[Dict[str, Any]],
    path: Path = config.OUTPUT_FILE,
) -> None:
    """Menulis hasil analisis fuzzy ke file Excel output.

    Format output yang dihasilkan:
        No | Suhu | pH | Kekeruhan | Nilai Centroid | Kategori

    Args:
        hasil_list: List dictionary berisi hasil setiap data.
            Setiap dictionary wajib memiliki kunci:
            no, suhu, ph, kekeruhan, centroid, kategori.
        path: Path ke file Excel output. Default: config.OUTPUT_FILE.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    records = []
    for h in hasil_list:
        records.append({
            "No":             h["no"],
            "Suhu (°C)":      h["suhu"],
            "pH":             h["ph"],
            "Kekeruhan (NTU)": h["kekeruhan"],
            "Nilai Centroid": round(h["centroid"], 4),
            "Kategori":       h["kategori"],
        })

    df_output = pd.DataFrame(records)

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df_output.to_excel(writer, index=False, sheet_name="Hasil Analisis")

    logger.info("Hasil analisis disimpan ke: %s", path)


def tulis_summary(
    hasil_list: List[Dict[str, Any]],
    path: Path = config.SUMMARY_FILE,
) -> None:
    """Menulis ringkasan analisis ke file summary.txt.

    Berisi statistik keseluruhan proses analisis fuzzy.

    Args:
        hasil_list: List dictionary hasil analisis per baris.
        path: Path ke file summary. Default: config.SUMMARY_FILE.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    jumlah_data = len(hasil_list)
    centroid_values = [h["centroid"] for h in hasil_list]
    rata_centroid = sum(centroid_values) / jumlah_data if jumlah_data > 0 else 0.0

    jumlah_ringan = sum(1 for h in hasil_list if h["kategori"] == "Perawatan Ringan")
    jumlah_sedang = sum(1 for h in hasil_list if h["kategori"] == "Perawatan Sedang")
    jumlah_intensif = sum(1 for h in hasil_list if h["kategori"] == "Perawatan Intensif")

    tanggal_proses = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sep = "=" * 60
    konten = (
        f"{sep}\n"
        "  RINGKASAN ANALISIS FUZZY MAMDANI AQUASCAPE\n"
        "  Model Logika Fuzzy Mamdani dalam Menentukan\n"
        "  Strategi Perawatan Akuarium Aquascape\n"
        f"{sep}\n\n"
        f"  Tanggal Proses       : {tanggal_proses}\n\n"
        f"  Jumlah Data          : {jumlah_data} record\n"
        f"  Rata-rata Centroid   : {rata_centroid:.4f}\n\n"
        f"  Perawatan Ringan     : {jumlah_ringan} record\n"
        f"  Perawatan Sedang     : {jumlah_sedang} record\n"
        f"  Perawatan Intensif   : {jumlah_intensif} record\n\n"
        f"{sep}\n"
    )

    path.write_text(konten, encoding="utf-8")
    logger.info("Summary disimpan ke: %s", path)
