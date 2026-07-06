"""
main.py
=======
Entry point utama — Sistem Fuzzy Mamdani Aquascape.

Mengorkestrasi seluruh alur proses:
    1. Inisialisasi logging
    2. Baca data dari Excel
    3. Validasi data
    4. Proses Fuzzy Mamdani per baris (Fuzzifikasi → Inferensi → Defuzzifikasi)
    5. Cetak hasil detail ke konsol
    6. Simpan hasil ke Excel
    7. Simpan summary ke TXT
    8. Buat seluruh grafik

Cara menjalankan:
    python main.py

Pastikan file data/data.xlsx sudah ada sebelum menjalankan program.
"""

import sys
import io
import logging
from pathlib import Path
from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# Konfigurasi encoding UTF-8 untuk konsol Windows
# ---------------------------------------------------------------------------
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Tambahkan root directory ke sys.path agar import lintas modul berjalan
sys.path.insert(0, str(Path(__file__).parent.resolve()))

import config
from utils.logger import setup_logger
from utils.excel import baca_data, tulis_hasil, tulis_summary
from utils.plotting import (
    buat_semua_mf,
    buat_grafik_agregasi,
    buat_grafik_defuzzifikasi,
)
from fuzzy.validator import validasi_dataframe
from fuzzy.inference import jalankan_inferensi
from fuzzy.defuzzification import centroid


def cetak_header() -> None:
    """Mencetak header informasi project ke konsol."""
    print("\n" + "=" * 70)
    print("  SISTEM FUZZY MAMDANI - STRATEGI PERAWATAN AQUASCAPE")
    print("  Model Logika Fuzzy Mamdani dalam Menentukan Strategi Perawatan")
    print("  Akuarium Aquascape Berdasarkan Fluktuasi Parameter Kualitas Air")
    print("=" * 70 + "\n")


def cetak_hasil_detail(
    no: int,
    hasil_inferensi: Dict[str, Any],
    nilai_centroid: float,
    kategori: str,
) -> None:
    """Mencetak detail hasil analisis satu baris data ke konsol.

    Args:
        no: Nomor urut data.
        hasil_inferensi: Dictionary hasil dari jalankan_inferensi().
        nilai_centroid: Nilai defuzzifikasi centroid.
        kategori: Label kategori strategi perawatan.
    """
    inp = hasil_inferensi["input"]
    mu_s = hasil_inferensi["mu_suhu"]
    mu_p = hasil_inferensi["mu_ph"]
    mu_k = hasil_inferensi["mu_kekeruhan"]
    rules_aktif = hasil_inferensi["rules_aktif"]

    print(f"\n" + "-" * 70)
    print(f"  DATA #{no}")
    print("-" * 70)
    print(f"  INPUT:")
    print(f"    Suhu      = {inp['suhu']:.2f} °C")
    print(f"    pH        = {inp['ph']:.2f}")
    print(f"    Kekeruhan = {inp['kekeruhan']:.2f} NTU")

    print(f"\n  NILAI MEMBERSHIP:")
    print(f"    Suhu:")
    for k, v in mu_s.items():
        print(f"      μ_{k:<8} = {v:.4f}")
    print(f"    pH:")
    for k, v in mu_p.items():
        print(f"      μ_{k:<8} = {v:.4f}")
    print(f"    Kekeruhan:")
    for k, v in mu_k.items():
        print(f"      μ_{k:<8} = {v:.4f}")

    print(f"\n  RULE YANG AKTIF ({len(rules_aktif)} dari 27 rule):")
    if rules_aktif:
        for r in rules_aktif:
            print(
                f"    R{r['rule_no']:>2}. IF Suhu={r['suhu']:<7} "
                f"AND pH={r['ph']:<7} AND Kekeruhan={r['kekeruhan']:<7} "
                f"=> {r['output']:<22} | alpha = {r['fire_strength']:.4f}"
            )
    else:
        print("    (Tidak ada rule aktif - semua fire strength = 0)")

    print(f"\n  HASIL DEFUZZIFIKASI:")
    print(f"    Nilai Centroid (z*) = {nilai_centroid:.4f}")
    print(f"    Strategi Perawatan  = ** {kategori} **")


def proses_semua_data() -> List[Dict[str, Any]]:
    """Memproses seluruh data dari Excel secara sequential.

    Returns:
        List dictionary berisi hasil analisis setiap baris data.
    """
    logger = logging.getLogger(__name__)

    # -----------------------------------------------------------------------
    # LANGKAH 1: BACA DATA
    # -----------------------------------------------------------------------
    logger.info("Membaca data dari: %s", config.INPUT_FILE)
    df_raw = baca_data(config.INPUT_FILE)

    # -----------------------------------------------------------------------
    # LANGKAH 2: VALIDASI DATA
    # -----------------------------------------------------------------------
    logger.info("Memvalidasi data...")
    df_valid, pesan_error = validasi_dataframe(df_raw)

    if pesan_error:
        print("\n[!] PERINGATAN — DATA TIDAK VALID:")
        for pesan in pesan_error:
            print(f"   [X] {pesan}")

    if df_valid.empty:
        logger.error("Tidak ada data valid yang dapat diproses. Program berhenti.")
        sys.exit(1)

    logger.info("Data valid: %d baris siap diproses.", len(df_valid))

    # -----------------------------------------------------------------------
    # LANGKAH 3: BUAT GRAFIK MEMBERSHIP FUNCTION (sekali saja)
    # -----------------------------------------------------------------------
    logger.info("Membuat grafik fungsi keanggotaan...")
    config.GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    buat_semua_mf(config.GRAPHS_DIR)

    # -----------------------------------------------------------------------
    # LANGKAH 4: PROSES FUZZY MAMDANI PER BARIS
    # -----------------------------------------------------------------------
    hasil_list: List[Dict[str, Any]] = []

    print(f"\n{'=' * 70}")
    print(f"  PROSES ANALISIS FUZZY MAMDANI")
    print(f"  Total Data: {len(df_valid)} baris")
    print(f"{'=' * 70}")

    for _, row in df_valid.iterrows():
        no = int(row["No"])
        suhu = float(row["Suhu"])
        ph = float(row["pH"])
        kekeruhan = float(row["Kekeruhan"])

        # Inferensi Mamdani (Fuzzifikasi + Evaluasi Rule + Agregasi MAX)
        hasil_inferensi = jalankan_inferensi(suhu, ph, kekeruhan)

        # Defuzzifikasi Centroid
        nilai_centroid, kategori = centroid(
            hasil_inferensi["x_output"],
            hasil_inferensi["mu_agregasi"],
        )

        # Cetak detail ke konsol
        cetak_hasil_detail(no, hasil_inferensi, nilai_centroid, kategori)

        # Simpan data hasil untuk output Excel
        hasil_list.append({
            "no":        no,
            "suhu":      suhu,
            "ph":        ph,
            "kekeruhan": kekeruhan,
            "centroid":  nilai_centroid,
            "kategori":  kategori,
        })

        # Buat grafik agregasi dan defuzzifikasi untuk data ini
        buat_grafik_agregasi(
            no,
            hasil_inferensi["x_output"],
            hasil_inferensi["mu_agregasi"],
            config.GRAPHS_DIR,
        )
        buat_grafik_defuzzifikasi(
            no,
            hasil_inferensi["x_output"],
            hasil_inferensi["mu_agregasi"],
            nilai_centroid,
            kategori,
            config.GRAPHS_DIR,
        )

        logger.info(
            "Data #%d selesai: Suhu=%.2f°C, pH=%.2f, Kekeruhan=%.2f NTU "
            "→ Centroid=%.4f → %s",
            no, suhu, ph, kekeruhan, nilai_centroid, kategori,
        )

    return hasil_list


def main() -> None:
    """Fungsi utama yang menjalankan seluruh pipeline analisis."""
    # Setup logging (konsol + file)
    setup_logger(
        log_file=config.OUTPUT_DIR / "run.log",
        level=config.LOG_LEVEL,
    )
    logger = logging.getLogger(__name__)

    cetak_header()
    logger.info("=== AquascapeFuzzy dimulai ===")

    try:
        hasil_list = proses_semua_data()

        # -------------------------------------------------------------------
        # LANGKAH 5: SIMPAN HASIL KE EXCEL
        # -------------------------------------------------------------------
        logger.info("Menyimpan hasil ke Excel...")
        tulis_hasil(hasil_list, config.OUTPUT_FILE)

        # -------------------------------------------------------------------
        # LANGKAH 6: SIMPAN SUMMARY
        # -------------------------------------------------------------------
        logger.info("Menyimpan summary...")
        tulis_summary(hasil_list, config.SUMMARY_FILE)

        # -------------------------------------------------------------------
        # CETAK RINGKASAN AKHIR
        # -------------------------------------------------------------------
        jumlah_ringan = sum(1 for h in hasil_list if h["kategori"] == "Perawatan Ringan")
        jumlah_sedang = sum(1 for h in hasil_list if h["kategori"] == "Perawatan Sedang")
        jumlah_intensif = sum(1 for h in hasil_list if h["kategori"] == "Perawatan Intensif")
        rata_centroid = sum(h["centroid"] for h in hasil_list) / len(hasil_list)

        print(f"\n{'=' * 70}")
        print("  RINGKASAN HASIL ANALISIS")
        print("-" * 70)
        print(f"  Total Data Diproses   : {len(hasil_list)} baris")
        print(f"  Rata-rata Centroid    : {rata_centroid:.4f}")
        print(f"  Perawatan Ringan      : {jumlah_ringan} data")
        print(f"  Perawatan Sedang      : {jumlah_sedang} data")
        print(f"  Perawatan Intensif    : {jumlah_intensif} data")
        print(f"{'─' * 70}")
        print(f"  Output Excel          : {config.OUTPUT_FILE}")
        print(f"  Summary               : {config.SUMMARY_FILE}")
        print(f"  Grafik                : {config.GRAPHS_DIR}")
        print(f"{'=' * 70}\n")

        logger.info("=== AquascapeFuzzy selesai dengan sukses ===")

    except FileNotFoundError as exc:
        logger.error("File tidak ditemukan: %s", exc)
        print(f"\n[ERROR]: {exc}")
        sys.exit(1)
    except ValueError as exc:
        logger.error("Kesalahan data: %s", exc)
        print(f"\n[ERROR]: {exc}")
        sys.exit(1)
    except Exception as exc:
        logger.exception("Kesalahan tidak terduga: %s", exc)
        print(f"\n[ERROR TIDAK TERDUGA]: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
