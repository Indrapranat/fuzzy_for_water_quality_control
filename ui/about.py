"""
ui/about.py
===========
Halaman Tentang Penelitian.

Menampilkan informasi metadata tentang penelitian skripsi,
tujuan, diagram, dan informasi pendukung lainnya.
"""

import streamlit as st
from ui.components import render_header

def render_about() -> None:
    """Merender konten halaman Tentang Penelitian."""
    render_header(
        title="ℹ️ Tentang Penelitian",
        subtitle="Informasi Skripsi dan Pengembangan Sistem"
    )

    with st.container():
        st.markdown("### 🎓 Judul Skripsi")
        st.info(
            "**Model Logika Fuzzy Mamdani dalam Menentukan Strategi Perawatan "
            "Akuarium Aquascape Berdasarkan Fluktuasi Parameter Kualitas Air**"
        )
        
        st.markdown("### 🎯 Tujuan Penelitian")
        st.write(
            "Penelitian ini bertujuan untuk merancang dan membangun model komputasi "
            "berbasis Logika Fuzzy Mamdani guna menentukan strategi perawatan "
            "akuarium aquascape secara akurat dan responsif. Model ini dievaluasi "
            "kemampuannya dalam menangani ketidakpastian (ambiguitas) dari fluktuasi "
            "suhu, pH, dan kekeruhan air yang dapat memengaruhi ekosistem flora dan fauna "
            "di dalamnya."
        )
        
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📥 Variabel Input")
            st.markdown(
                """
                1. **Suhu Air (°C)**
                   - Dingin (0 - 26)
                   - Normal (24 - 30)
                   - Panas (28 - 60)
                2. **pH Air**
                   - Asam (0 - 7)
                   - Netral (6 - 8)
                   - Basa (7 - 14)
                3. **Kekeruhan (NTU)**
                   - Jernih (0 - 40)
                   - Sedang (20 - 70)
                   - Keruh (50 - 150)
                """
            )
        
        with c2:
            st.markdown("### 📤 Variabel Output")
            st.markdown(
                """
                - **Strategi Perawatan (0 - 100)**
                  - Perawatan Ringan (0 - 37.5)
                  - Perawatan Sedang (25 - 75)
                  - Perawatan Intensif (62.5 - 100)
                """
            )
            
        st.markdown("---")
        
        st.markdown("### 🛠️ Spesifikasi Sistem & Library")
        st.write("Sistem ini dibangun menggunakan ekosistem Python murni tanpa bergantung pada library fuzzy black-box (seperti scikit-fuzzy) untuk memastikan transparansi algoritma (white-box).")
        
        libs = {
            "Python": "Bahasa Pemrograman Utama (v3.9+)",
            "Streamlit": "Pembuatan Antarmuka Pengguna (UI)",
            "NumPy": "Komputasi Matriks dan Array Multidimensi",
            "Pandas": "Manipulasi Dataframe (Riwayat & Rule)",
            "Matplotlib": "Pembangkitan Visualisasi Grafik MF",
            "OpenPyXL": "Engine Pembaca/Penulis File Excel"
        }
        
        for lib, desc in libs.items():
            st.markdown(f"- **{lib}**: {desc}")
