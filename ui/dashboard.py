"""
ui/dashboard.py
===============
Halaman Dashboard (Beranda) aplikasi.

Menampilkan informasi umum mengenai penelitian, judul, metode,
dan diagram alur sederhana dari proses fuzzy Mamdani.
"""

import streamlit as st
from ui.components import render_header


def render_dashboard() -> None:
    """Merender konten halaman Dashboard."""
    render_header(
        title="🏠 Dashboard",
        subtitle="Sistem Inferensi Fuzzy Mamdani untuk Perawatan Aquascape"
    )

    st.markdown("### Judul Penelitian")
    st.info(
        "**Model Logika Fuzzy Mamdani dalam Menentukan Strategi Perawatan "
        "Akuarium Aquascape Berdasarkan Fluktuasi Parameter Kualitas Air**"
    )

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Metode", value="Fuzzy Mamdani")
    with col2:
        st.metric(label="Jumlah Rule", value="27 Rule")
    with col3:
        st.metric(label="Parameter Input", value="3 Parameter")

    st.markdown("---")
    
    st.markdown("### Deskripsi Sistem")
    st.write(
        "Sistem ini dikembangkan untuk membantu dalam menentukan strategi perawatan "
        "akuarium aquascape secara otomatis berdasarkan tiga parameter kualitas air: "
        "**Suhu Air (°C)**, **pH**, dan **Kekeruhan (NTU)**. Dengan menggunakan logika "
        "fuzzy Mamdani, sistem dapat mengakomodasi ketidakpastian kondisi air dan "
        "memberikan rekomendasi perawatan yang proporsional."
    )

    st.markdown("### Diagram Alur Inferensi Fuzzy")
    
    # Membuat diagram alur menggunakan container dan styling CSS sederhana
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; gap: 10px; margin-top: 20px;">
            <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 10px 30px; border-radius: 8px; font-weight: bold; color: #1e3a8a; width: 300px; text-align: center;">1. Input (Suhu, pH, Kekeruhan)</div>
            <div style="color: #94a3b8; font-size: 24px;">&#8595;</div>
            <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 10px 30px; border-radius: 8px; font-weight: bold; color: #166534; width: 300px; text-align: center;">2. Fuzzifikasi</div>
            <div style="color: #94a3b8; font-size: 24px;">&#8595;</div>
            <div style="background-color: #fffbeb; border: 1px solid #fde68a; padding: 10px 30px; border-radius: 8px; font-weight: bold; color: #92400e; width: 300px; text-align: center;">3. Inferensi Mamdani (Evaluasi Rule)</div>
            <div style="color: #94a3b8; font-size: 24px;">&#8595;</div>
            <div style="background-color: #fdf2f8; border: 1px solid #fbcfe8; padding: 10px 30px; border-radius: 8px; font-weight: bold; color: #9d174d; width: 300px; text-align: center;">4. Defuzzifikasi (Centroid)</div>
            <div style="color: #94a3b8; font-size: 24px;">&#8595;</div>
            <div style="background-color: #f8fafc; border: 2px solid #334155; padding: 10px 30px; border-radius: 8px; font-weight: bold; color: #0f172a; width: 300px; text-align: center;">5. Output (Strategi Perawatan)</div>
        </div>
        """,
        unsafe_allow_html=True
    )
