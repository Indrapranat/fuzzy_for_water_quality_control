"""
utils/plotting.py
=================
Modul pembuatan grafik berkualitas tinggi menggunakan Matplotlib.

Menghasilkan 6 jenis grafik yang disimpan di output/graphs/:

1. mf_suhu.png         — Fungsi keanggotaan Suhu
2. mf_ph.png           — Fungsi keanggotaan pH
3. mf_kekeruhan.png    — Fungsi keanggotaan Kekeruhan
4. mf_output.png       — Fungsi keanggotaan Output
5. agregasi_N.png      — Grafik agregasi per data (N = nomor data)
6. defuzzifikasi_N.png — Grafik defuzzifikasi per data dengan garis centroid
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend untuk batch processing
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from typing import Dict, List, Any
import logging

import config
from fuzzy.membership import triangular_mf_array

logger = logging.getLogger(__name__)


def _setup_style() -> None:
    """Mengaktifkan style matplotlib untuk grafik yang konsisten."""
    try:
        plt.style.use(config.GRAPH_STYLE)
    except OSError:
        plt.style.use("seaborn-v0_8-whitegrid")


def plot_membership_function(
    variabel: str,
    universe: np.ndarray,
    mf_params: Dict[str, tuple],
    xlabel: str,
    judul: str,
    path_simpan: Path,
) -> None:
    """Membuat dan menyimpan grafik fungsi keanggotaan triangular.

    Args:
        variabel: Nama variabel ('suhu', 'ph', 'kekeruhan', 'output').
        universe: Array titik diskrit universe of discourse.
        mf_params: Dictionary parameter MF {kategori: (a, b, c)}.
        xlabel: Label sumbu x.
        judul: Judul grafik.
        path_simpan: Path untuk menyimpan file PNG.
    """
    _setup_style()
    fig, ax = plt.subplots(figsize=(10, 5))

    for kategori, (a, b, c) in mf_params.items():
        warna = config.COLOR_PALETTE.get(kategori, "#888888")
        mu_array = triangular_mf_array(universe, a, b, c)
        ax.plot(
            universe,
            mu_array,
            label=kategori,
            color=warna,
            linewidth=2.5,
        )
        ax.fill_between(universe, mu_array, alpha=0.15, color=warna)

        # Tandai titik puncak (b)
        if a <= b <= c:
            mu_puncak = triangular_mf_array(np.array([b]), a, b, c)[0]
            ax.annotate(
                f"({b}, {mu_puncak:.0f})",
                xy=(b, mu_puncak),
                xytext=(b, mu_puncak + 0.07),
                ha="center",
                fontsize=8,
                color=warna,
                fontweight="bold",
            )

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel("Derajat Keanggotaan μ(x)", fontsize=12)
    ax.set_title(judul, fontsize=14, fontweight="bold", pad=15)
    ax.set_ylim(-0.05, 1.15)
    ax.legend(loc="upper right", fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.4)

    fig.tight_layout()
    path_simpan.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path_simpan, dpi=config.GRAPH_DPI, format=config.GRAPH_FORMAT, bbox_inches="tight")
    plt.close(fig)
    logger.info("Grafik MF '%s' disimpan: %s", variabel, path_simpan)


def buat_grafik_mf_suhu(graphs_dir: Path) -> None:
    """Membuat grafik fungsi keanggotaan Suhu Air.

    Args:
        graphs_dir: Direktori output untuk menyimpan grafik.
    """
    universe = np.linspace(config.SUHU_MIN, config.SUHU_MAX, 500)
    plot_membership_function(
        variabel="suhu",
        universe=universe,
        mf_params=config.SUHU_MF,
        xlabel="Suhu Air (°C)",
        judul="Fungsi Keanggotaan — Suhu Air (°C)",
        path_simpan=graphs_dir / "mf_suhu.png",
    )


def buat_grafik_mf_ph(graphs_dir: Path) -> None:
    """Membuat grafik fungsi keanggotaan pH Air.

    Args:
        graphs_dir: Direktori output untuk menyimpan grafik.
    """
    universe = np.linspace(config.PH_MIN, config.PH_MAX, 500)
    plot_membership_function(
        variabel="ph",
        universe=universe,
        mf_params=config.PH_MF,
        xlabel="pH Air",
        judul="Fungsi Keanggotaan — pH Air",
        path_simpan=graphs_dir / "mf_ph.png",
    )


def buat_grafik_mf_tds(graphs_dir: Path) -> None:
    """Membuat grafik fungsi keanggotaan TDS Air.

    Args:
        graphs_dir: Direktori output untuk menyimpan grafik.
    """
    universe = np.linspace(config.TDS_MIN, config.TDS_MAX, 500)
    plot_membership_function(
        variabel="tds",
        universe=universe,
        mf_params=config.TDS_MF,
        xlabel="TDS Air (ppm)",
        judul="Fungsi Keanggotaan — TDS Air (ppm)",
        path_simpan=graphs_dir / "mf_tds.png",
    )


# Alias backward-compatible
def buat_grafik_mf_kekeruhan(graphs_dir: Path) -> None:
    """Alias untuk buat_grafik_mf_tds (backward-compatible)."""
    buat_grafik_mf_tds(graphs_dir)


def buat_grafik_mf_output(graphs_dir: Path) -> None:
    """Membuat grafik fungsi keanggotaan Strategi Perawatan (Output).

    Args:
        graphs_dir: Direktori output untuk menyimpan grafik.
    """
    universe = np.linspace(config.OUTPUT_MIN, config.OUTPUT_MAX, 500)
    plot_membership_function(
        variabel="output",
        universe=universe,
        mf_params=config.OUTPUT_MF,
        xlabel="Strategi Perawatan (Skor)",
        judul="Fungsi Keanggotaan — Strategi Perawatan (Output)",
        path_simpan=graphs_dir / "mf_output.png",
    )


def buat_grafik_agregasi(
    no: int,
    x_output: np.ndarray,
    mu_agregasi: np.ndarray,
    graphs_dir: Path,
) -> None:
    """Membuat grafik hasil agregasi MAX untuk satu data.

    Menampilkan kurva agregasi yang merupakan gabungan (union)
    dari seluruh fungsi keanggotaan output yang ter-clip.

    Args:
        no: Nomor data.
        x_output: Array universe output.
        mu_agregasi: Array derajat keanggotaan hasil agregasi MAX.
        graphs_dir: Direktori output untuk menyimpan grafik.
    """
    _setup_style()
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x_output, mu_agregasi, color="#3F51B5", linewidth=2.5, label="Agregasi MAX")
    ax.fill_between(x_output, mu_agregasi, alpha=0.3, color="#3F51B5")

    ax.set_xlabel("Universe Output — Strategi Perawatan", fontsize=12)
    ax.set_ylabel("Derajat Keanggotaan μ(x)", fontsize=12)
    ax.set_title(
        f"Hasil Agregasi MAX — Data #{no}",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax.set_ylim(-0.05, 1.15)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, alpha=0.4)

    fig.tight_layout()
    path_simpan = graphs_dir / f"agregasi_{no:03d}.png"
    fig.savefig(path_simpan, dpi=config.GRAPH_DPI, format=config.GRAPH_FORMAT, bbox_inches="tight")
    plt.close(fig)
    logger.debug("Grafik agregasi Data #%d disimpan: %s", no, path_simpan)


def buat_grafik_defuzzifikasi(
    no: int,
    x_output: np.ndarray,
    mu_agregasi: np.ndarray,
    nilai_centroid: float,
    kategori: str,
    graphs_dir: Path,
) -> None:
    """Membuat grafik defuzzifikasi dengan garis centroid untuk satu data.

    Menampilkan kurva agregasi beserta garis vertikal merah
    yang menunjukkan posisi nilai centroid (z*).

    Args:
        no: Nomor data.
        x_output: Array universe output.
        mu_agregasi: Array derajat keanggotaan hasil agregasi MAX.
        nilai_centroid: Nilai crisp hasil defuzzifikasi centroid.
        kategori: Label kategori strategi perawatan.
        graphs_dir: Direktori output untuk menyimpan grafik.
    """
    _setup_style()
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x_output, mu_agregasi, color="#3F51B5", linewidth=2.5, label="Agregasi MAX")
    ax.fill_between(x_output, mu_agregasi, alpha=0.25, color="#3F51B5")

    # Garis vertikal pada nilai centroid
    ax.axvline(
        x=nilai_centroid,
        color="#E53935",
        linewidth=2.5,
        linestyle="--",
        label=f"Centroid z* = {nilai_centroid:.4f}",
    )

    # Anotasi teks nilai centroid
    mu_at_centroid = float(np.interp(nilai_centroid, x_output, mu_agregasi))
    ax.annotate(
        f"z* = {nilai_centroid:.2f}\n({kategori})",
        xy=(nilai_centroid, mu_at_centroid),
        xytext=(nilai_centroid + 4, mu_at_centroid + 0.1),
        arrowprops={"arrowstyle": "->", "color": "#E53935"},
        fontsize=10,
        color="#E53935",
        fontweight="bold",
    )

    ax.set_xlabel("Universe Output — Strategi Perawatan", fontsize=12)
    ax.set_ylabel("Derajat Keanggotaan μ(x)", fontsize=12)
    ax.set_title(
        f"Defuzzifikasi Centroid — Data #{no}  |  {kategori}",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax.set_ylim(-0.05, 1.15)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, alpha=0.4)

    fig.tight_layout()
    path_simpan = graphs_dir / f"defuzzifikasi_{no:03d}.png"
    fig.savefig(path_simpan, dpi=config.GRAPH_DPI, format=config.GRAPH_FORMAT, bbox_inches="tight")
    plt.close(fig)
    logger.debug("Grafik defuzzifikasi Data #%d disimpan: %s", no, path_simpan)


def buat_semua_mf(graphs_dir: Path) -> None:
    """Membuat seluruh grafik fungsi keanggotaan (4 grafik).

    Args:
        graphs_dir: Direktori output untuk menyimpan grafik.
    """
    buat_grafik_mf_suhu(graphs_dir)
    buat_grafik_mf_ph(graphs_dir)
    buat_grafik_mf_tds(graphs_dir)
    buat_grafik_mf_output(graphs_dir)
    logger.info("Semua grafik fungsi keanggotaan berhasil dibuat.")
