"""
tests/test_membership.py
========================
Unit test untuk modul fuzzy/membership.py.

Menguji fungsi triangular_mf dan seluruh fungsi fuzzifikasi
dengan berbagai kasus uji termasuk nilai batas, nilai dalam range,
dan nilai di luar range.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from fuzzy.membership import (
    triangular_mf,
    triangular_mf_array,
    fuzzifikasi_suhu,
    fuzzifikasi_ph,
    fuzzifikasi_kekeruhan,
)


# ---------------------------------------------------------------------------
# TEST: triangular_mf — fungsi dasar
# ---------------------------------------------------------------------------

class TestTriangularMF:
    """Test suite untuk fungsi triangular_mf dasar."""

    def test_titik_puncak_mengembalikan_satu(self):
        """Titik puncak b harus menghasilkan derajat keanggotaan = 1."""
        assert triangular_mf(27.0, 24.0, 27.0, 30.0) == pytest.approx(1.0)

    def test_titik_kaki_kiri_mengembalikan_nol(self):
        """Titik kaki kiri a harus menghasilkan derajat keanggotaan = 0."""
        assert triangular_mf(24.0, 24.0, 27.0, 30.0) == pytest.approx(0.0)

    def test_titik_kaki_kanan_mengembalikan_nol(self):
        """Titik kaki kanan c harus menghasilkan derajat keanggotaan = 0."""
        assert triangular_mf(30.0, 24.0, 27.0, 30.0) == pytest.approx(0.0)

    def test_nilai_di_luar_kiri(self):
        """Nilai di bawah a harus mengembalikan 0."""
        assert triangular_mf(20.0, 24.0, 27.0, 30.0) == pytest.approx(0.0)

    def test_nilai_di_luar_kanan(self):
        """Nilai di atas c harus mengembalikan 0."""
        assert triangular_mf(35.0, 24.0, 27.0, 30.0) == pytest.approx(0.0)

    def test_sisi_naik_tengah(self):
        """Nilai tepat di tengah sisi naik harus = 0.5."""
        # a=24, b=27, c=30 → x=25.5 → (25.5-24)/(27-24) = 1.5/3 = 0.5
        assert triangular_mf(25.5, 24.0, 27.0, 30.0) == pytest.approx(0.5)

    def test_sisi_turun_tengah(self):
        """Nilai tepat di tengah sisi turun harus = 0.5."""
        # a=24, b=27, c=30 → x=28.5 → (30-28.5)/(30-27) = 1.5/3 = 0.5
        assert triangular_mf(28.5, 24.0, 27.0, 30.0) == pytest.approx(0.5)

    def test_shoulder_kiri_nilai_satu(self):
        """Shoulder kiri (a==b): nilai x = a (puncak shoulder) harus = 1."""
        # a=0, b=0, c=26 -> x=0 -> shoulder kiri: return (26-0)/(26-0) = 1
        assert triangular_mf(0.0, 0.0, 0.0, 26.0) == pytest.approx(1.0)

    def test_shoulder_kanan_nilai_satu(self):
        """Shoulder kanan (b==c): nilai x = b (puncak) harus = 1."""
        # a=28, b=50, c=50 -> x=50 -> shoulder kanan: x<=b -> (50-28)/(50-28) = 1
        assert triangular_mf(50.0, 28.0, 50.0, 50.0) == pytest.approx(1.0)

    def test_parameter_tidak_valid_raise_error(self):
        """Parameter tidak valid (a > b) harus melempar ValueError."""
        with pytest.raises(ValueError):
            triangular_mf(5.0, 10.0, 5.0, 15.0)

    def test_rentang_output_selalu_nol_sampai_satu(self):
        """Semua output harus berada di rentang [0, 1]."""
        for x in np.linspace(0, 50, 100):
            mu = triangular_mf(x, 24.0, 27.0, 30.0)
            assert 0.0 <= mu <= 1.0, f"Nilai mu={mu} untuk x={x} di luar [0,1]"


class TestTriangularMFArray:
    """Test suite untuk versi array dari triangular_mf."""

    def test_output_shape_sama_dengan_input(self):
        """Shape output harus sama dengan shape input."""
        x = np.linspace(0, 50, 200)
        mu = triangular_mf_array(x, 24.0, 27.0, 30.0)
        assert mu.shape == x.shape

    def test_puncak_adalah_satu(self):
        """Nilai pada titik puncak harus = 1 dalam array."""
        x = np.array([27.0])
        mu = triangular_mf_array(x, 24.0, 27.0, 30.0)
        assert mu[0] == pytest.approx(1.0)

    def test_semua_nilai_dalam_rentang(self):
        """Semua nilai output array harus berada di [0, 1]."""
        x = np.linspace(0, 50, 500)
        mu = triangular_mf_array(x, 24.0, 27.0, 30.0)
        assert np.all(mu >= 0.0) and np.all(mu <= 1.0)


# ---------------------------------------------------------------------------
# TEST: Fuzzifikasi Suhu
# ---------------------------------------------------------------------------

class TestFuzzifikasiSuhu:
    """Test suite untuk fuzzifikasi variabel Suhu."""

    def test_kunci_output_lengkap(self):
        """Output harus memiliki semua kategori Suhu."""
        hasil = fuzzifikasi_suhu(27.0)
        assert set(hasil.keys()) == {"Dingin", "Normal", "Panas"}

    def test_suhu_normal_ideal(self):
        """Suhu 27°C (titik puncak Normal) harus memiliki μ_Normal = 1."""
        hasil = fuzzifikasi_suhu(27.0)
        assert hasil["Normal"] == pytest.approx(1.0)
        assert hasil["Dingin"] == pytest.approx(0.0)
        assert hasil["Panas"] == pytest.approx(0.0)

    def test_suhu_sangat_dingin(self):
        """Suhu 0°C harus penuh Dingin."""
        hasil = fuzzifikasi_suhu(0.0)
        assert hasil["Dingin"] == pytest.approx(1.0)

    def test_suhu_sangat_panas(self):
        """Suhu 50°C harus penuh Panas."""
        hasil = fuzzifikasi_suhu(50.0)
        assert hasil["Panas"] == pytest.approx(1.0)

    def test_semua_nilai_dalam_rentang(self):
        """Semua derajat keanggotaan harus dalam [0, 1]."""
        for suhu in np.linspace(0, 50, 50):
            hasil = fuzzifikasi_suhu(float(suhu))
            for v in hasil.values():
                assert 0.0 <= v <= 1.0


# ---------------------------------------------------------------------------
# TEST: Fuzzifikasi pH
# ---------------------------------------------------------------------------

class TestFuzzifikasiPH:
    """Test suite untuk fuzzifikasi variabel pH."""

    def test_kunci_output_lengkap(self):
        """Output harus memiliki semua kategori pH."""
        hasil = fuzzifikasi_ph(7.0)
        assert set(hasil.keys()) == {"Asam", "Netral", "Basa"}

    def test_ph_netral_ideal(self):
        """pH 7.0 (titik puncak Netral) harus memiliki μ_Netral = 1."""
        hasil = fuzzifikasi_ph(7.0)
        assert hasil["Netral"] == pytest.approx(1.0)

    def test_ph_sangat_asam(self):
        """pH 0 harus penuh Asam."""
        hasil = fuzzifikasi_ph(0.0)
        assert hasil["Asam"] == pytest.approx(1.0)

    def test_ph_sangat_basa(self):
        """pH 14 harus penuh Basa."""
        hasil = fuzzifikasi_ph(14.0)
        assert hasil["Basa"] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# TEST: Fuzzifikasi Kekeruhan
# ---------------------------------------------------------------------------

class TestFuzzifikasiKekeruhan:
    """Test suite untuk fuzzifikasi variabel Kekeruhan."""

    def test_kunci_output_lengkap(self):
        """Output harus memiliki semua kategori Kekeruhan."""
        hasil = fuzzifikasi_kekeruhan(0.0)
        assert set(hasil.keys()) == {"Jernih", "Sedang", "Keruh"}

    def test_kekeruhan_jernih(self):
        """Kekeruhan 0 NTU harus penuh Jernih."""
        hasil = fuzzifikasi_kekeruhan(0.0)
        assert hasil["Jernih"] == pytest.approx(1.0)

    def test_kekeruhan_sedang_ideal(self):
        """Kekeruhan 50 NTU (puncak Sedang) harus μ_Sedang = 1."""
        hasil = fuzzifikasi_kekeruhan(50.0)
        assert hasil["Sedang"] == pytest.approx(1.0)

    def test_kekeruhan_keruh(self):
        """Kekeruhan 100 NTU harus penuh Keruh."""
        hasil = fuzzifikasi_kekeruhan(100.0)
        assert hasil["Keruh"] == pytest.approx(1.0)
