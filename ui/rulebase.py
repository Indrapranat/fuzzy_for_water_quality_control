"""
ui/rulebase.py
==============
Halaman Rule Base.

Menampilkan 27 aturan (rules) Fuzzy Mamdani dalam bentuk tabel interaktif
yang dapat difilter berdasarkan Suhu, pH, dan TDS.
Mengambil data langsung dari modul fuzzy.rules.
"""

import streamlit as st
import pandas as pd

from fuzzy.rules import get_rules


# Peta warna per kategori output (untuk highlight baris)
_HIGHLIGHT_COLOR = {
    "Perawatan Ringan":   "background-color: #d1fae5; color: #065f46; font-weight: 600;",
    "Perawatan Sedang":   "background-color: #fef9c3; color: #854d0e; font-weight: 600;",
    "Perawatan Intensif": "background-color: #fee2e2; color: #991b1b; font-weight: 600;",
}

_ICON_OUTPUT = {
    "Perawatan Ringan":   "🟢",
    "Perawatan Sedang":   "🟡",
    "Perawatan Intensif": "🔴",
}


def _style_output(val: str) -> str:
    """Kembalikan CSS style untuk kolom output."""
    return _HIGHLIGHT_COLOR.get(val, "")


def render_rulebase() -> None:
    """Merender konten halaman Rule Base."""

    # ── Header ──────────────────────────────────────────────────────────────
    st.markdown(
        """
        <h2 style="margin-bottom:0.2rem;">
            <span class="material-symbols-rounded" style="vertical-align:middle; font-size:2rem; color:#0f4c81;">format_list_numbered</span>
            &nbsp;Rule Base Mamdani
        </h2>
        <p style="color:#64748b; margin-top:0.2rem;">
            Daftar lengkap <b>27 Aturan IF-THEN</b> yang digunakan oleh Engine Fuzzy Mamdani.<br>
            Dibentuk dari kombinasi <b>3 Suhu × 3 pH × 3 TDS = 27 kombinasi unik</b>.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Ambil semua rules ────────────────────────────────────────────────────
    rules = get_rules()
    total = len(rules)

    # ── Statistik ringkas ────────────────────────────────────────────────────
    jml_ringan   = sum(1 for r in rules if r["output"] == "Perawatan Ringan")
    jml_sedang   = sum(1 for r in rules if r["output"] == "Perawatan Sedang")
    jml_intensif = sum(1 for r in rules if r["output"] == "Perawatan Intensif")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📋 Total Rule",             total)
    c2.metric("🟢 Perawatan Ringan",   jml_ringan)
    c3.metric("🟡 Perawatan Sedang",   jml_sedang)
    c4.metric("🔴 Perawatan Intensif", jml_intensif)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filter ───────────────────────────────────────────────────────────────
    st.markdown("#### :material/filter_alt: Filter Rule")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        f_suhu = st.selectbox(
            "🌡️ Suhu",
            ["Semua", "Dingin", "Normal", "Panas"],
            key="rb_suhu"
        )
    with col2:
        f_ph = st.selectbox(
            "🧪 pH",
            ["Semua", "Asam", "Netral", "Basa"],
            key="rb_ph"
        )
    with col3:
        f_tds = st.selectbox(
            "💧 TDS",
            ["Semua", "Rendah", "Sedang", "Tinggi"],
            key="rb_tds"
        )
    with col4:
        f_output = st.selectbox(
            "✅ Strategi Output",
            ["Semua", "Perawatan Ringan", "Perawatan Sedang", "Perawatan Intensif"],
            key="rb_output"
        )

    # ── Terapkan filter ──────────────────────────────────────────────────────
    filtered = rules[:]
    if f_suhu   != "Semua":
        filtered = [r for r in filtered if r["suhu"]   == f_suhu]
    if f_ph     != "Semua":
        filtered = [r for r in filtered if r["ph"]     == f_ph]
    if f_tds    != "Semua":
        filtered = [r for r in filtered if r["tds"]    == f_tds]
    if f_output != "Semua":
        filtered = [r for r in filtered if r["output"] == f_output]

    # ── Build DataFrame ──────────────────────────────────────────────────────
    # Lookup nomor rule asli dari posisi di list penuh
    rule_to_no = {
        (r["suhu"], r["ph"], r["tds"]): i + 1
        for i, r in enumerate(rules)
    }

    st.markdown(
        f"Menampilkan **{len(filtered)}** dari **{total}** rule."
    )
    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered:
        st.warning("Tidak ada rule yang cocok dengan filter yang dipilih.")
        return

    df_display = pd.DataFrame([
        {
            "No Rule":                      f"R{rule_to_no.get((r['suhu'], r['ph'], r['tds']), '?')}",
            "🌡️ Suhu (IF)":                r["suhu"],
            "🧪 pH (AND)":                 r["ph"],
            "💧 TDS (AND)":                r["tds"],
            "✅ Strategi Perawatan (THEN)": f"{_ICON_OUTPUT.get(r['output'], '')} {r['output']}",
        }
        for r in filtered
    ])

    st.dataframe(
        df_display,
        use_container_width=True,
        height=min(50 + len(filtered) * 37, 700),
        hide_index=True,
    )

    # ── Keterangan Kategori ──────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("ℹ️ Keterangan Kategori Parameter & Output", expanded=False):
        col_a, col_b, col_c, col_d = st.columns(4)

        with col_a:
            st.markdown("**🌡️ Suhu Air (°C)**")
            st.markdown("""
| Kategori | Rentang |
|----------|---------|
| Dingin   | 0 – 24 °C |
| Normal   | 24 – 30 °C |
| Panas    | 30 – 50 °C |
""")

        with col_b:
            st.markdown("**🧪 pH Air**")
            st.markdown("""
| Kategori | Rentang |
|----------|---------|
| Asam   | 0 – 6.5 |
| Netral | 6.5 – 7.5 |
| Basa   | 7.5 – 14 |
""")

        with col_c:
            st.markdown("**💧 TDS Air (ppm)**")
            st.markdown("""
| Kategori | Rentang |
|----------|---------|
| Rendah | 0 – 200 ppm |
| Sedang | 200 – 500 ppm |
| Tinggi | 500 – 1000 ppm |
""")

        with col_d:
            st.markdown("**✅ Strategi Perawatan**")
            st.markdown("""
| Output | Centroid |
|--------|---------|
| 🟢 Ringan   | 0 – 37.5 |
| 🟡 Sedang   | 37.5 – 62.5 |
| 🔴 Intensif | 62.5 – 100 |
""")

    # ── Logika Penentuan Rule ────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📖 Logika Penentuan Rule Base", expanded=False):
        st.markdown("""
        **Dasar penentuan output setiap rule:**

        - **Normal + Netral + Rendah** → kondisi ideal → 🟢 **Perawatan Ringan** (hanya 1 rule)
        - **Satu parameter menyimpang** (misal suhu dingin/panas, atau pH asam/basa, atau TDS sedang) → 🟡 **Perawatan Sedang**
        - **Dua atau lebih parameter bermasalah**, atau satu parameter **sangat ekstrem** (TDS Tinggi dengan suhu/pH bermasalah) → 🔴 **Perawatan Intensif**

        Sistem menggunakan operator **AND = MIN** untuk inferensi dan **MAX** untuk agregasi output.
        Defuzzifikasi menggunakan metode **Centroid (Center of Gravity)**.
        """)
