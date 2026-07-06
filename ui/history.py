"""
ui/history.py
=============
Halaman Riwayat Analisis.

Membaca file output/hasil.xlsx dan menampilkannya sebagai DataFrame interaktif
dengan fitur unduh (download) dan filter.
"""

import streamlit as st
import pandas as pd
from io import BytesIO

import config
from ui.components import render_header

def render_history() -> None:
    """Merender konten halaman Riwayat Analisis."""
    render_header(
        title="📁 Riwayat Analisis",
        subtitle="Data hasil analisis sebelumnya yang tersimpan di sistem."
    )

    path_hasil = config.OUTPUT_FILE
    
    if not path_hasil.exists():
        st.info("Belum ada riwayat analisis. Silakan jalankan program utama atau gunakan menu Analisis Data.")
        return

    try:
        # Membaca file Excel
        df = pd.read_excel(path_hasil, engine="openpyxl")
        
        st.markdown(f"Ditemukan **{len(df)}** data riwayat analisis.")
        
        # Fitur download
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Riwayat")
        
        st.download_button(
            label="📥 Download Data (Excel)",
            data=excel_buffer.getvalue(),
            file_name="riwayat_analisis_aquascape.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Fitur filter Kategori
        kategori_filter = st.multiselect(
            "Filter berdasarkan Kategori Strategi Perawatan:",
            options=df["Kategori"].unique(),
            default=df["Kategori"].unique()
        )
        
        if kategori_filter:
            df_filtered = df[df["Kategori"].isin(kategori_filter)]
        else:
            df_filtered = df

        # Tampilkan DataFrame
        st.dataframe(
            df_filtered,
            use_container_width=True,
            height=600
        )
        
    except Exception as e:
        st.error(f"Gagal membaca file riwayat: {e}")
