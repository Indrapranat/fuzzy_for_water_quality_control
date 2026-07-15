"""
app.py
======
Entry point utama untuk aplikasi Streamlit.
Memiliki 4 halaman: Input, Proses, Output, Rule Base.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.resolve()))

from ui.styles import apply_custom_styles
from ui.main_page import render_main
from ui.rulebase import render_rulebase


def main():
    st.set_page_config(
        page_title="Aquascape Fuzzy Mamdani",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    apply_custom_styles()

    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; padding: 1.5rem 0 1rem 0;">
                <div style="font-size: 2.5rem;"><span class="material-symbols-rounded" style="font-size: 3rem; color: #60a5fa;">water_ec</span></div>
                <h2 style="color:#0f4c81; margin:0; font-size:1.3rem; font-weight:700;">Aquascape Fuzzy</h2>
                <p style="color:#64748b; font-size:0.82rem; margin-top:0.3rem;">Sistem Perawatan Cerdas</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

        page = st.radio(
            "Navigasi",
            options=[
                ":material/input: INPUT",
                ":material/settings: PROSES",
                ":material/output: OUTPUT",
                ":material/format_list_numbered: RULE BASE",
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown(
            """
            <div style="font-size:0.78rem; color:#94a3b8; text-align:center; line-height:1.6;">
                <b>Alur Kerja:</b><br>
                <span class="material-symbols-rounded" style="font-size: 0.9rem;">looks_one</span> <b>INPUT</b> — Masukkan data<br>
                <span class="material-symbols-rounded" style="font-size: 0.9rem;">looks_two</span> <b>PROSES</b> — Lihat perhitungan<br>
                <span class="material-symbols-rounded" style="font-size: 0.9rem;">looks_3</span> <b>OUTPUT</b> — Baca rekomendasi<br>
                <span class="material-symbols-rounded" style="font-size: 0.9rem;">looks_4</span> <b>RULE BASE</b> — 27 Aturan Fuzzy
            </div>
            """,
            unsafe_allow_html=True
        )

    if "RULE BASE" in page:
        render_rulebase()
    else:
        render_main(page)


if __name__ == "__main__":
    main()
