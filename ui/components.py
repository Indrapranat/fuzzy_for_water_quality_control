"""
ui/components.py
================
Modul ini berisi komponen antarmuka yang dapat digunakan kembali (reusable components).

Digunakan untuk menjaga konsistensi tampilan antar halaman dan
mengurangi duplikasi kode.
"""

import streamlit as st


def render_header(title: str, subtitle: str = "") -> None:
    """Merender header halaman dengan gaya yang konsisten.

    Args:
        title: Judul utama halaman.
        subtitle: Subjudul opsional.
    """
    st.markdown(
        f"""
        <div style="padding-bottom: 1rem; border-bottom: 2px solid #e5e7eb; margin-bottom: 2rem;">
            <h1 style="color: #1f2937; margin-bottom: 0;">{title}</h1>
            <p style="color: #6b7280; font-size: 1.1rem; margin-top: 0.5rem;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Merender footer di bagian bawah halaman."""
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #9ca3af; font-size: 0.9rem; padding: 1rem 0;">
            <p><strong>Sistem Inferensi Fuzzy Mamdani</strong><br>
            Dikembangkan menggunakan Python & Streamlit &copy; 2026</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(title: str, content: str, icon: str = "") -> None:
    """Merender sebuah card sederhana menggunakan HTML/CSS.

    Args:
        title: Judul card.
        content: Isi teks atau nilai dari card.
        icon: Nama material icon (contoh: 'analytics').
    """
    icon_html = f"<span class='material-symbols-rounded' style='vertical-align: middle; margin-right: 0.3rem; font-size: 1.3rem;'>{icon}</span>" if icon else ""
    st.markdown(
        f"""
        <div class="custom-card">
            <h4 style="color: #4b5563; margin-top: 0; font-size: 1.1rem; display: flex; align-items: center;">{icon_html} {title}</h4>
            <p style="color: #111827; font-size: 1.5rem; font-weight: 600; margin-bottom: 0;">{content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_status_indicator(centroid: float) -> tuple:
    """Menentukan indikator status (warna dan icon) berdasarkan nilai centroid.

    Args:
        centroid: Nilai hasil defuzzifikasi (0-100).

    Returns:
        Tuple berisi (warna_hex, icon, status_text).
    """
    if centroid < 37.5:
        return ("#10b981", "<span class='material-symbols-rounded' style='color:#10b981; vertical-align:middle;'>check_circle</span>", "Sangat Baik (Perawatan Ringan)")
    elif centroid < 62.5:
        return ("#f59e0b", "<span class='material-symbols-rounded' style='color:#f59e0b; vertical-align:middle;'>warning</span>", "Perlu Perhatian (Perawatan Sedang)")
    else:
        return ("#ef4444", "<span class='material-symbols-rounded' style='color:#ef4444; vertical-align:middle;'>error</span>", "Kritis (Perawatan Intensif)")
