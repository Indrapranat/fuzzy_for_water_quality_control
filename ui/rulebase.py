"""
ui/rulebase.py
==============
Halaman Rule Base.

Menampilkan 27 aturan (rules) dalam bentuk DataFrame yang dapat dicari/filter.
Mengambil data langsung dari modul fuzzy.rules.
"""

import streamlit as st
import pandas as pd

from fuzzy.rules import get_rules
from ui.components import render_header

def render_rulebase() -> None:
    """Merender konten halaman Rule Base."""
    render_header(
        title="<span class='material-symbols-rounded' style='vertical-align: middle; font-size: 2.5rem;'>format_list_numbered</span> Rule Base Mamdani",
        subtitle="Daftar lengkap 27 Aturan yang digunakan oleh Engine Fuzzy"
    )

    st.markdown(
        "Sistem menggunakan 27 rule yang dibentuk dari kombinasi seluruh "
        "kategori (3 Suhu × 3 pH × 3 Kekeruhan)."
    )

    # Ambil rules dari engine
    rules = get_rules()
    
    # Konversi ke DataFrame untuk kemudahan display
    df_rules = pd.DataFrame(rules)
    df_rules.index = df_rules.index + 1  # 1-indexed
    df_rules.index.name = "Rule No"
    
    # Ubah nama kolom agar lebih rapi
    df_rules = df_rules.rename(columns={
        "suhu": "Suhu (IF)",
        "ph": "pH (AND)",
        "kekeruhan": "Kekeruhan (AND)",
        "output": "Strategi Perawatan (THEN)"
    })

    # Fitur Pencarian & Filter
    st.markdown("### :material/search: Cari / Filter Rule")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        f_suhu = st.selectbox("Filter Suhu", ["Semua", "Dingin", "Normal", "Panas"])
    with col2:
        f_ph = st.selectbox("Filter pH", ["Semua", "Asam", "Netral", "Basa"])
    with col3:
        f_kek = st.selectbox("Filter Kekeruhan", ["Semua", "Jernih", "Sedang", "Keruh"])

    # Terapkan filter
    df_filtered = df_rules.copy()
    if f_suhu != "Semua":
        df_filtered = df_filtered[df_filtered["Suhu (IF)"] == f_suhu]
    if f_ph != "Semua":
        df_filtered = df_filtered[df_filtered["pH (AND)"] == f_ph]
    if f_kek != "Semua":
        df_filtered = df_filtered[df_filtered["Kekeruhan (AND)"] == f_kek]

    st.markdown(f"Menampilkan **{len(df_filtered)}** dari 27 rule.")
    
    # Tampilkan DataFrame
    st.dataframe(
        df_filtered,
        use_container_width=True,
        height=500
    )
