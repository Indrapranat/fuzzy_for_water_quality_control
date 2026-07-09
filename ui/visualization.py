"""
ui/visualization.py
===================
Halaman Visualisasi.

Menampilkan grafik-grafik yang telah di-generate oleh Engine (Matplotlib).
Tidak menghitung ulang, murni memuat gambar dari output/graphs/.
"""

import streamlit as st
from pathlib import Path
from PIL import Image

import config
from ui.components import render_header

def render_visualization() -> None:
    """Merender konten halaman Visualisasi Membership."""
    render_header(
        title="<span class='material-symbols-rounded' style='vertical-align: middle; font-size: 2.5rem;'>show_chart</span> Visualisasi Membership",
        subtitle="Grafik Fungsi Keanggotaan Logika Fuzzy Mamdani"
    )

    st.markdown(
        "Halaman ini menampilkan representasi visual dari fungsi keanggotaan "
        "yang digunakan dalam engine Fuzzy Mamdani. Grafik digenerate secara otomatis "
        "saat engine dijalankan."
    )

    graphs_dir = config.GRAPHS_DIR
    
    # 1. Grafik Input
    st.markdown("### Variabel Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        path_suhu = graphs_dir / "mf_suhu.png"
        if path_suhu.exists():
            st.image(Image.open(path_suhu), caption="Fungsi Keanggotaan Suhu Air")
        else:
            st.warning("Grafik MF Suhu belum dibuat. Jalankan main.py terlebih dahulu.")
            
        path_ph = graphs_dir / "mf_ph.png"
        if path_ph.exists():
            st.image(Image.open(path_ph), caption="Fungsi Keanggotaan pH Air")
        else:
            st.warning("Grafik MF pH belum dibuat.")
            
    with col2:
        path_kekeruhan = graphs_dir / "mf_kekeruhan.png"
        if path_kekeruhan.exists():
            st.image(Image.open(path_kekeruhan), caption="Fungsi Keanggotaan Kekeruhan")
        else:
            st.warning("Grafik MF Kekeruhan belum dibuat.")

    st.markdown("---")
    
    # 2. Grafik Output
    st.markdown("### Variabel Output")
    
    path_output = graphs_dir / "mf_output.png"
    if path_output.exists():
        st.image(Image.open(path_output), caption="Fungsi Keanggotaan Strategi Perawatan", use_container_width=True)
    else:
        st.warning("Grafik MF Output belum dibuat.")
        
    st.markdown("---")
    
    # 3. Grafik Hasil Proses (Agregasi & Defuzzifikasi untuk Data Terakhir)
    st.markdown("### Contoh Hasil Agregasi & Defuzzifikasi (Data Terakhir)")
    
    # Mencari grafik terakhir di folder graphs
    if graphs_dir.exists():
        agregasi_files = sorted(list(graphs_dir.glob("agregasi_*.png")))
        defuz_files = sorted(list(graphs_dir.glob("defuzzifikasi_*.png")))
        
        if agregasi_files and defuz_files:
            c1, c2 = st.columns(2)
            with c1:
                st.image(Image.open(agregasi_files[-1]), caption=f"Agregasi ({agregasi_files[-1].name})")
            with c2:
                st.image(Image.open(defuz_files[-1]), caption=f"Defuzzifikasi ({defuz_files[-1].name})")
        else:
            st.info("Belum ada grafik hasil analisis data per baris.")
