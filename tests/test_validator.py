"""
tests/test_validator.py
=======================
Unit test untuk modul fuzzy/validator.py.

Menguji validasi nilai suhu, pH, kekeruhan, dan seluruh DataFrame
termasuk kasus batas atas, batas bawah, nilai tidak valid, dan
deteksi kolom yang hilang.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from fuzzy.validator import (
    ValidationError,
    validasi_suhu,
    validasi_ph,
    validasi_kekeruhan,
    validasi_baris,
    validasi_dataframe,
)


# ---------------------------------------------------------------------------
# TEST: Validasi Suhu
# ---------------------------------------------------------------------------

class TestValidasiSuhu:
    """Test suite untuk validasi variabel Suhu."""

    def test_suhu_batas_bawah_valid(self):
        """Suhu 0°C (batas bawah) harus lolos validasi."""
        validasi_suhu(0.0, baris=1)

    def test_suhu_batas_atas_valid(self):
        """Suhu 50°C (batas atas) harus lolos validasi."""
        validasi_suhu(50.0, baris=1)

    def test_suhu_tengah_valid(self):
        """Suhu 27°C harus lolos validasi."""
        validasi_suhu(27.0, baris=1)

    def test_suhu_negatif_tidak_valid(self):
        """Suhu negatif harus melempar ValidationError."""
        with pytest.raises(ValidationError):
            validasi_suhu(-1.0, baris=1)

    def test_suhu_terlalu_panas_tidak_valid(self):
        """Suhu > 50°C harus melempar ValidationError."""
        with pytest.raises(ValidationError):
            validasi_suhu(51.0, baris=1)

    def test_suhu_string_tidak_valid(self):
        """Suhu berupa string harus melempar ValidationError."""
        with pytest.raises(ValidationError):
            validasi_suhu("panas", baris=1)  # type: ignore

    def test_error_menyebut_nomor_baris(self):
        """Pesan error harus menyebutkan nomor baris yang bermasalah."""
        with pytest.raises(ValidationError) as exc_info:
            validasi_suhu(999.0, baris=5)
        assert "5" in str(exc_info.value)


# ---------------------------------------------------------------------------
# TEST: Validasi pH
# ---------------------------------------------------------------------------

class TestValidasiPH:
    """Test suite untuk validasi variabel pH."""

    def test_ph_nol_valid(self):
        """pH 0 (batas bawah) harus lolos."""
        validasi_ph(0.0, baris=1)

    def test_ph_empat_belas_valid(self):
        """pH 14 (batas atas) harus lolos."""
        validasi_ph(14.0, baris=1)

    def test_ph_tujuh_valid(self):
        """pH 7 (netral) harus lolos."""
        validasi_ph(7.0, baris=1)

    def test_ph_negatif_tidak_valid(self):
        """pH negatif harus melempar ValidationError."""
        with pytest.raises(ValidationError):
            validasi_ph(-0.1, baris=1)

    def test_ph_lebih_dari_empat_belas_tidak_valid(self):
        """pH > 14 harus melempar ValidationError."""
        with pytest.raises(ValidationError):
            validasi_ph(14.1, baris=1)


# ---------------------------------------------------------------------------
# TEST: Validasi Kekeruhan
# ---------------------------------------------------------------------------

class TestValidasiKekeruhan:
    """Test suite untuk validasi variabel Kekeruhan."""

    def test_kekeruhan_nol_valid(self):
        """Kekeruhan 0 NTU (batas bawah) harus lolos."""
        validasi_kekeruhan(0.0, baris=1)

    def test_kekeruhan_seratus_valid(self):
        """Kekeruhan 100 NTU (batas atas) harus lolos."""
        validasi_kekeruhan(100.0, baris=1)

    def test_kekeruhan_lima_puluh_valid(self):
        """Kekeruhan 50 NTU harus lolos."""
        validasi_kekeruhan(50.0, baris=1)

    def test_kekeruhan_negatif_tidak_valid(self):
        """Kekeruhan negatif harus melempar ValidationError."""
        with pytest.raises(ValidationError):
            validasi_kekeruhan(-1.0, baris=1)

    def test_kekeruhan_lebih_dari_seratus_tidak_valid(self):
        """Kekeruhan > 100 NTU harus melempar ValidationError."""
        with pytest.raises(ValidationError):
            validasi_kekeruhan(101.0, baris=1)


# ---------------------------------------------------------------------------
# TEST: Validasi DataFrame
# ---------------------------------------------------------------------------

class TestValidasiDataframe:
    """Test suite untuk validasi DataFrame penuh."""

    def _buat_df_valid(self) -> pd.DataFrame:
        """Membuat DataFrame valid untuk pengujian."""
        return pd.DataFrame({
            "No":        [1, 2, 3],
            "Suhu":      [27.0, 30.0, 24.0],
            "pH":        [7.0, 6.5, 7.5],
            "Kekeruhan": [10.0, 50.0, 80.0],
        })

    def test_dataframe_valid_tidak_ada_error(self):
        """DataFrame valid harus tidak menghasilkan error apapun."""
        df, errors = validasi_dataframe(self._buat_df_valid())
        assert len(errors) == 0
        assert len(df) == 3

    def test_dataframe_dengan_baris_tidak_valid(self):
        """Baris tidak valid harus dibuang, bukan seluruh DataFrame."""
        df = pd.DataFrame({
            "No":        [1, 2, 3],
            "Suhu":      [27.0, 999.0, 25.0],  # baris 2 tidak valid
            "pH":        [7.0, 7.0, 7.0],
            "Kekeruhan": [10.0, 10.0, 10.0],
        })
        df_valid, errors = validasi_dataframe(df)
        assert len(df_valid) == 2
        assert len(errors) == 1

    def test_kolom_hilang_raise_error(self):
        """DataFrame tanpa kolom wajib harus melempar ValueError."""
        df = pd.DataFrame({
            "No":  [1, 2],
            "Suhu": [27.0, 28.0],
            # pH dan Kekeruhan hilang
        })
        with pytest.raises(ValueError, match="Kolom wajib tidak ditemukan"):
            validasi_dataframe(df)

    def test_semua_baris_tidak_valid_mengembalikan_df_kosong(self):
        """Jika semua baris tidak valid, DataFrame hasil harus kosong."""
        df = pd.DataFrame({
            "No":        [1, 2],
            "Suhu":      [999.0, -100.0],
            "pH":        [99.0, -1.0],
            "Kekeruhan": [999.0, -5.0],
        })
        df_valid, errors = validasi_dataframe(df)
        assert df_valid.empty
        assert len(errors) == 2
