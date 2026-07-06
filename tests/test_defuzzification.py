"""
tests/test_defuzzification.py
==============================
Unit test untuk modul fuzzy/defuzzification.py.

Menguji metode centroid defuzzification dan kategorisasi output
dengan berbagai kondisi fungsi agregasi.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from fuzzy.defuzzification import centroid, tentukan_kategori
from fuzzy.inference import jalankan_inferensi


# ---------------------------------------------------------------------------
# TEST: Fungsi centroid
# ---------------------------------------------------------------------------

class TestCentroid:
    """Test suite untuk fungsi defuzzifikasi centroid."""

    def test_centroid_array_nol_mengembalikan_nol(self):
        """Jika semua mu_agregasi = 0, centroid harus = 0."""
        x = np.linspace(0, 100, 100)
        mu = np.zeros_like(x)
        nilai, _ = centroid(x, mu)
        assert nilai == pytest.approx(0.0)

    def test_centroid_spike_di_kiri(self):
        """Spike di sisi kiri universe harus menghasilkan centroid mendekati kiri."""
        x = np.linspace(0, 100, 1000)
        mu = np.zeros_like(x)
        # Buat spike tipis di sekitar x=10
        mu[(x >= 8) & (x <= 12)] = 1.0
        nilai, _ = centroid(x, mu)
        assert nilai == pytest.approx(10.0, abs=1.0)

    def test_centroid_spike_di_kanan(self):
        """Spike di sisi kanan universe harus menghasilkan centroid mendekati kanan."""
        x = np.linspace(0, 100, 1000)
        mu = np.zeros_like(x)
        # Buat spike tipis di sekitar x=90
        mu[(x >= 88) & (x <= 92)] = 1.0
        nilai, _ = centroid(x, mu)
        assert nilai == pytest.approx(90.0, abs=1.0)

    def test_centroid_simetris_di_tengah(self):
        """Distribusi simetris harus menghasilkan centroid di tengah (≈50)."""
        x = np.linspace(0, 100, 1000)
        mu = np.zeros_like(x)
        # Buat trapezoid simetris di tengah (40-60)
        mu[(x >= 40) & (x <= 60)] = 1.0
        nilai, _ = centroid(x, mu)
        assert nilai == pytest.approx(50.0, abs=0.5)

    def test_centroid_dimensi_tidak_sama_raise_error(self):
        """Dimensi x dan mu yang berbeda harus melempar ValueError."""
        x = np.linspace(0, 100, 100)
        mu = np.zeros(50)  # Dimensi berbeda
        with pytest.raises(ValueError):
            centroid(x, mu)

    def test_output_dalam_rentang_universe(self):
        """Nilai centroid harus selalu berada di dalam rentang universe [0, 100]."""
        x = np.linspace(0, 100, 1000)
        # Gunakan pipeline inferensi untuk menghasilkan mu_agregasi nyata
        for suhu, ph, kekeruhan in [(27.0, 7.0, 0.0), (35.0, 4.0, 90.0), (15.0, 8.5, 50.0)]:
            hasil = jalankan_inferensi(suhu, ph, kekeruhan)
            nilai, _ = centroid(hasil["x_output"], hasil["mu_agregasi"])
            assert 0.0 <= nilai <= 100.0, f"Centroid={nilai} di luar [0, 100]"

    def test_centroid_mengembalikan_tuple(self):
        """centroid harus mengembalikan tuple (float, str)."""
        x = np.linspace(0, 100, 100)
        mu = np.zeros_like(x)
        mu[40:60] = 0.5
        hasil = centroid(x, mu)
        assert isinstance(hasil, tuple)
        assert len(hasil) == 2
        assert isinstance(hasil[0], float)
        assert isinstance(hasil[1], str)


# ---------------------------------------------------------------------------
# TEST: Fungsi tentukan_kategori
# ---------------------------------------------------------------------------

class TestTentukanKategori:
    """Test suite untuk fungsi kategorisasi output."""

    def test_nilai_nol_adalah_ringan(self):
        """Nilai 0 harus dikategorikan Perawatan Ringan."""
        assert tentukan_kategori(0.0) == "Perawatan Ringan"

    def test_nilai_37_adalah_ringan(self):
        """Nilai 37 (di bawah threshold 37.5) harus Ringan."""
        assert tentukan_kategori(37.0) == "Perawatan Ringan"

    def test_nilai_50_adalah_sedang(self):
        """Nilai 50 harus dikategorikan Perawatan Sedang."""
        assert tentukan_kategori(50.0) == "Perawatan Sedang"

    def test_nilai_62_adalah_sedang(self):
        """Nilai 62 (di bawah threshold 62.5) harus Sedang."""
        assert tentukan_kategori(62.0) == "Perawatan Sedang"

    def test_nilai_63_adalah_intensif(self):
        """Nilai 63 (di atas threshold 62.5) harus Intensif."""
        assert tentukan_kategori(63.0) == "Perawatan Intensif"

    def test_nilai_100_adalah_intensif(self):
        """Nilai 100 harus dikategorikan Perawatan Intensif."""
        assert tentukan_kategori(100.0) == "Perawatan Intensif"

    def test_ketiga_kategori_dapat_dihasilkan(self):
        """Ketiga kategori output harus dapat dihasilkan."""
        kategori_set = {
            tentukan_kategori(10.0),
            tentukan_kategori(50.0),
            tentukan_kategori(80.0),
        }
        assert kategori_set == {"Perawatan Ringan", "Perawatan Sedang", "Perawatan Intensif"}


# ---------------------------------------------------------------------------
# TEST: Integrasi Inferensi + Defuzzifikasi
# ---------------------------------------------------------------------------

class TestIntegrasiInferensiDefuzz:
    """Test integrasi antara inferensi dan defuzzifikasi."""

    def test_kondisi_ideal_menghasilkan_ringan(self):
        """Input ideal (Normal+Netral+Jernih) harus menghasilkan Perawatan Ringan."""
        hasil = jalankan_inferensi(27.0, 7.0, 0.0)
        nilai_c, kategori = centroid(hasil["x_output"], hasil["mu_agregasi"])
        assert kategori == "Perawatan Ringan", (
            f"Diharapkan 'Perawatan Ringan', diperoleh '{kategori}' (centroid={nilai_c:.2f})"
        )

    def test_kondisi_buruk_menghasilkan_intensif(self):
        """Input buruk (Panas+Asam+Keruh) harus menghasilkan Perawatan Intensif."""
        hasil = jalankan_inferensi(45.0, 3.0, 95.0)
        nilai_c, kategori = centroid(hasil["x_output"], hasil["mu_agregasi"])
        assert kategori == "Perawatan Intensif", (
            f"Diharapkan 'Perawatan Intensif', diperoleh '{kategori}' (centroid={nilai_c:.2f})"
        )
