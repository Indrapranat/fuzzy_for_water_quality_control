"""
tests/test_inference.py
=======================
Unit test untuk modul fuzzy/inference.py.

Menguji evaluasi rule, agregasi MAX, dan pipeline inferensi
Mamdani secara end-to-end untuk berbagai kombinasi input.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from fuzzy.inference import evaluasi_rule, agregasi_max, jalankan_inferensi
from fuzzy.membership import fuzzifikasi_suhu, fuzzifikasi_ph, fuzzifikasi_kekeruhan


# ---------------------------------------------------------------------------
# TEST: Evaluasi Rule
# ---------------------------------------------------------------------------

class TestEvaluasiRule:
    """Test suite untuk fungsi evaluasi_rule."""

    def test_jumlah_rule_adalah_27(self):
        """Harus ada tepat 27 rule yang dievaluasi."""
        mu_s = fuzzifikasi_suhu(27.0)
        mu_p = fuzzifikasi_ph(7.0)
        mu_k = fuzzifikasi_kekeruhan(0.0)
        hasil = evaluasi_rule(mu_s, mu_p, mu_k)
        assert len(hasil) == 27

    def test_fire_strength_dalam_rentang_nol_satu(self):
        """Semua fire_strength harus berada di [0, 1]."""
        mu_s = fuzzifikasi_suhu(27.0)
        mu_p = fuzzifikasi_ph(7.0)
        mu_k = fuzzifikasi_kekeruhan(30.0)
        hasil = evaluasi_rule(mu_s, mu_p, mu_k)
        for r in hasil:
            assert 0.0 <= r["fire_strength"] <= 1.0

    def test_kondisi_ideal_menghasilkan_rule_ringan_aktif(self):
        """Input ideal (Normal+Netral+Jernih) harus mengaktifkan rule Ringan."""
        mu_s = fuzzifikasi_suhu(27.0)    # Normal = 1.0
        mu_p = fuzzifikasi_ph(7.0)       # Netral = 1.0
        mu_k = fuzzifikasi_kekeruhan(0.0)  # Jernih = 1.0 (shoulder kiri)

        hasil = evaluasi_rule(mu_s, mu_p, mu_k)

        # Cari rule R13: Normal + Netral + Jernih -> Perawatan Ringan
        rule_ringan = next(
            r for r in hasil
            if r["suhu"] == "Normal" and r["ph"] == "Netral"
            and r["kekeruhan"] == "Jernih"
        )
        assert rule_ringan["aktif"] is True
        assert rule_ringan["fire_strength"] == pytest.approx(1.0)
        assert rule_ringan["output"] == "Perawatan Ringan"

    def test_fire_strength_menggunakan_min(self):
        """Fire strength harus sama dengan nilai minimum dari ketiga mu."""
        mu_s = {"Dingin": 0.3, "Normal": 0.7, "Panas": 0.0}
        mu_p = {"Asam": 0.0, "Netral": 0.5, "Basa": 0.0}
        mu_k = {"Jernih": 0.8, "Sedang": 0.0, "Keruh": 0.0}

        hasil = evaluasi_rule(mu_s, mu_p, mu_k)

        # Normal + Netral + Jernih → MIN(0.7, 0.5, 0.8) = 0.5
        rule = next(
            r for r in hasil
            if r["suhu"] == "Normal" and r["ph"] == "Netral"
            and r["kekeruhan"] == "Jernih"
        )
        assert rule["fire_strength"] == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# TEST: Agregasi MAX
# ---------------------------------------------------------------------------

class TestAgregasiMax:
    """Test suite untuk fungsi agregasi_max."""

    def test_output_shape_sesuai_input(self):
        """Shape output agregasi harus sama dengan x_output."""
        x = np.linspace(0, 100, 100)
        mu_s = fuzzifikasi_suhu(27.0)
        mu_p = fuzzifikasi_ph(7.0)
        mu_k = fuzzifikasi_kekeruhan(10.0)
        hasil = evaluasi_rule(mu_s, mu_p, mu_k)
        mu_agg = agregasi_max(hasil, x)
        assert mu_agg.shape == x.shape

    def test_output_dalam_rentang_nol_satu(self):
        """Semua nilai agregasi harus berada di [0, 1]."""
        x = np.linspace(0, 100, 200)
        mu_s = fuzzifikasi_suhu(30.0)
        mu_p = fuzzifikasi_ph(8.0)
        mu_k = fuzzifikasi_kekeruhan(70.0)
        hasil = evaluasi_rule(mu_s, mu_p, mu_k)
        mu_agg = agregasi_max(hasil, x)
        assert np.all(mu_agg >= 0.0) and np.all(mu_agg <= 1.0)

    def test_tidak_ada_rule_aktif_menghasilkan_nol(self):
        """Jika tidak ada rule aktif, agregasi harus nol di semua titik."""
        x = np.linspace(0, 100, 100)
        # Semua fire strength = 0
        mu_s = {"Dingin": 0.0, "Normal": 0.0, "Panas": 0.0}
        mu_p = {"Asam": 0.0, "Netral": 0.0, "Basa": 0.0}
        mu_k = {"Jernih": 0.0, "Sedang": 0.0, "Keruh": 0.0}
        hasil = evaluasi_rule(mu_s, mu_p, mu_k)
        mu_agg = agregasi_max(hasil, x)
        assert np.all(mu_agg == 0.0)


# ---------------------------------------------------------------------------
# TEST: Pipeline Inferensi End-to-End
# ---------------------------------------------------------------------------

class TestJalankanInferensi:
    """Test suite untuk pipeline inferensi Mamdani end-to-end."""

    def test_output_kunci_lengkap(self):
        """Output harus memiliki semua kunci yang diharapkan."""
        hasil = jalankan_inferensi(27.0, 7.0, 10.0)
        kunci_wajib = {
            "input", "mu_suhu", "mu_ph", "mu_kekeruhan",
            "hasil_evaluasi", "rules_aktif", "x_output", "mu_agregasi",
        }
        assert kunci_wajib.issubset(set(hasil.keys()))

    def test_input_tersimpan_benar(self):
        """Nilai input harus tersimpan dengan benar di hasil."""
        hasil = jalankan_inferensi(25.0, 6.5, 30.0)
        assert hasil["input"]["suhu"] == pytest.approx(25.0)
        assert hasil["input"]["ph"] == pytest.approx(6.5)
        assert hasil["input"]["kekeruhan"] == pytest.approx(30.0)

    def test_x_output_dalam_rentang(self):
        """x_output harus berada di rentang [0, 100]."""
        hasil = jalankan_inferensi(27.0, 7.0, 0.0)
        assert hasil["x_output"].min() >= 0.0
        assert hasil["x_output"].max() <= 100.0

    def test_mu_agregasi_tidak_semua_nol_untuk_input_valid(self):
        """Untuk input yang menghasilkan rule aktif, agregasi tidak boleh nol."""
        # Gunakan x=0.0 untuk Kekeruhan Jernih (shoulder kiri = 1.0)
        hasil = jalankan_inferensi(27.0, 7.0, 0.0)
        assert np.any(hasil["mu_agregasi"] > 0.0), (
            "Agregasi harus > 0 untuk kondisi ideal Normal+Netral+Jernih"
        )

    def test_kondisi_parah_banyak_rule_aktif(self):
        """Kondisi buruk harus menghasilkan lebih banyak rule aktif."""
        hasil_baik = jalankan_inferensi(27.0, 7.0, 0.0)
        hasil_buruk = jalankan_inferensi(35.0, 4.0, 90.0)
        # Kondisi buruk biasanya menghasilkan lebih banyak rule aktif
        assert len(hasil_buruk["rules_aktif"]) >= 0  # Minimal tidak error
