"""
fuzzy/inference.py
==================
Implementasi Mesin Inferensi Mamdani.

Modul ini mengeksekusi proses inferensi Mamdani secara lengkap:

Tahap 1 — Fuzzifikasi:
    Mengubah nilai crisp input menjadi derajat keanggotaan menggunakan
    fungsi keanggotaan triangular yang telah didefinisikan di membership.py.

Tahap 2 — Evaluasi Rule (Operator AND → MIN):
    Setiap rule dievaluasi dengan operator AND menggunakan fungsi MIN.
    Fire Strength = MIN(μ_suhu, μ_ph, μ_tds)

Tahap 3 — Implikasi:
    Setiap rule yang aktif (fire strength > 0) menghasilkan potongan
    (clipping) pada fungsi keanggotaan output.
    μ_output_clip(x) = MIN(fire_strength, μ_output(x))

Tahap 4 — Agregasi (Operator MAX):
    Seluruh fungsi output yang telah di-clip digabungkan menggunakan
    operator MAX pada setiap titik x:
    μ_agregasi(x) = MAX(μ_clip_rule1(x), μ_clip_rule2(x), ...)
"""

import numpy as np
from typing import Dict, List, Any
import logging

from fuzzy.membership import (
    fuzzifikasi_suhu,
    fuzzifikasi_ph,
    fuzzifikasi_tds,
    triangular_mf_array,
)
from fuzzy.rules import RULES
import config

logger = logging.getLogger(__name__)


def evaluasi_rule(
    mu_suhu: Dict[str, float],
    mu_ph: Dict[str, float],
    mu_tds: Dict[str, float],
) -> List[Dict[str, Any]]:
    """Mengevaluasi seluruh rule fuzzy dengan operator AND (MIN).

    Untuk setiap rule, fire strength dihitung sebagai:
        α_i = MIN(μ_suhu[kategori], μ_ph[kategori], μ_tds[kategori])

    Rule dikatakan aktif jika α_i > 0.

    Args:
        mu_suhu: Derajat keanggotaan Suhu untuk setiap kategori.
        mu_ph: Derajat keanggotaan pH untuk setiap kategori.
        mu_tds: Derajat keanggotaan TDS untuk setiap kategori.

    Returns:
        List dictionary berisi informasi setiap rule yang aktif:
        {
            "rule_no":       int,    # Nomor rule (1-27)
            "suhu":          str,    # Kategori suhu
            "ph":            str,    # Kategori pH
            "tds":           str,    # Kategori TDS
            "output":        str,    # Kategori output
            "mu_suhu":       float,  # Derajat keanggotaan suhu
            "mu_ph":         float,  # Derajat keanggotaan pH
            "mu_tds":        float,  # Derajat keanggotaan TDS
            "fire_strength": float,  # MIN(mu_suhu, mu_ph, mu_tds)
            "aktif":         bool,   # True jika fire_strength > 0
        }
    """
    hasil_evaluasi: List[Dict[str, Any]] = []

    for i, rule in enumerate(RULES, start=1):
        mu_s = mu_suhu.get(rule["suhu"], 0.0)
        mu_p = mu_ph.get(rule["ph"], 0.0)
        mu_t = mu_tds.get(rule["tds"], 0.0)

        fire_strength = min(mu_s, mu_p, mu_t)
        aktif = fire_strength > 0.0

        hasil_evaluasi.append({
            "rule_no":       i,
            "suhu":          rule["suhu"],
            "ph":            rule["ph"],
            "tds":           rule["tds"],
            "output":        rule["output"],
            "mu_suhu":       mu_s,
            "mu_ph":         mu_p,
            "mu_tds":        mu_t,
            "fire_strength": fire_strength,
            "aktif":         aktif,
        })

    return hasil_evaluasi


def agregasi_max(
    hasil_evaluasi: List[Dict[str, Any]],
    x_output: np.ndarray,
) -> np.ndarray:
    """Menggabungkan seluruh output rule yang aktif menggunakan operator MAX.

    Proses:
    1. Untuk setiap rule aktif, hitung fungsi keanggotaan output yang di-clip:
       μ_clip(x) = MIN(fire_strength, μ_output(x))
    2. Gabungkan semua μ_clip dengan operator MAX:
       μ_agregasi(x) = MAX(μ_clip_rule1(x), μ_clip_rule2(x), ...)

    Args:
        hasil_evaluasi: Output dari fungsi evaluasi_rule.
        x_output: Array titik diskrit pada universe output.

    Returns:
        Array numpy berisi derajat keanggotaan hasil agregasi MAX
        pada setiap titik di x_output.
    """
    # Inisialisasi agregasi dengan nol
    mu_agregasi = np.zeros_like(x_output, dtype=float)

    for rule_data in hasil_evaluasi:
        if not rule_data["aktif"]:
            continue

        kategori_output = rule_data["output"]
        fire_strength = rule_data["fire_strength"]

        # Ambil parameter segitiga untuk kategori output ini
        a, b, c = config.OUTPUT_MF[kategori_output]

        # Hitung fungsi keanggotaan output pada seluruh universe
        mu_output_penuh = triangular_mf_array(x_output, a, b, c)

        # Implikasi MIN: potong (clip) pada fire_strength
        mu_clip = np.minimum(fire_strength, mu_output_penuh)

        # Agregasi MAX: ambil nilai maksimum dari semua rule
        mu_agregasi = np.maximum(mu_agregasi, mu_clip)

    return mu_agregasi


def jalankan_inferensi(
    suhu: float,
    ph: float,
    tds: float,
) -> Dict[str, Any]:
    """Menjalankan seluruh proses inferensi Mamdani untuk satu data input.

    Args:
        suhu: Nilai suhu air (°C).
        ph: Nilai pH air.
        tds: Nilai TDS air (ppm).

    Returns:
        Dictionary berisi hasil lengkap inferensi:
        {
            "input":          dict,       # Nilai input crisp
            "mu_suhu":        dict,       # Derajat keanggotaan Suhu
            "mu_ph":          dict,       # Derajat keanggotaan pH
            "mu_tds":         dict,       # Derajat keanggotaan TDS
            "hasil_evaluasi": list,       # Hasil evaluasi 27 rule
            "rules_aktif":    list,       # Hanya rule yang aktif
            "x_output":       np.ndarray, # Universe output
            "mu_agregasi":    np.ndarray, # Fungsi agregasi MAX
        }
    """
    logger.debug(
        "Memulai inferensi: Suhu=%.2f°C, pH=%.2f, TDS=%.2f ppm",
        suhu, ph, tds,
    )

    # TAHAP 1: FUZZIFIKASI
    mu_suhu = fuzzifikasi_suhu(suhu)
    mu_ph = fuzzifikasi_ph(ph)
    mu_tds = fuzzifikasi_tds(tds)

    logger.debug("Fuzzifikasi Suhu: %s", mu_suhu)
    logger.debug("Fuzzifikasi pH: %s", mu_ph)
    logger.debug("Fuzzifikasi TDS: %s", mu_tds)

    # TAHAP 2 & 3: EVALUASI RULE + IMPLIKASI MIN
    hasil_evaluasi = evaluasi_rule(mu_suhu, mu_ph, mu_tds)

    rules_aktif = [r for r in hasil_evaluasi if r["aktif"]]
    logger.debug("Rule aktif: %d dari %d rule", len(rules_aktif), len(hasil_evaluasi))

    # TAHAP 4: AGREGASI MAX
    x_output = np.linspace(
        config.OUTPUT_MIN,
        config.OUTPUT_MAX,
        config.OUTPUT_RESOLUTION,
    )
    mu_agregasi = agregasi_max(hasil_evaluasi, x_output)

    return {
        "input": {"suhu": suhu, "ph": ph, "tds": tds},
        "mu_suhu": mu_suhu,
        "mu_ph": mu_ph,
        "mu_tds": mu_tds,
        "hasil_evaluasi": hasil_evaluasi,
        "rules_aktif": rules_aktif,
        "x_output": x_output,
        "mu_agregasi": mu_agregasi,
    }
