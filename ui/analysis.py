"""
ui/analysis.py
==============
Halaman utama analisis.

Mengambil input dari user, memvalidasi, memanggil Engine Fuzzy,
dan menampilkan hasil dalam UI card dan expander detail.
Mendukung input manual harian dan upload Excel untuk banyak data.
"""

import streamlit as st
import pandas as pd
import time
from io import BytesIO
from typing import Dict, Any

from fuzzy.validator import ValidationError, validasi_baris, validasi_dataframe
from fuzzy.inference import jalankan_inferensi
from fuzzy.defuzzification import centroid
from ui.components import render_header, render_card, get_status_indicator
import config


def render_analysis() -> None:
    """Merender konten halaman Analisis Data."""
    render_header(
        title="📊 Analisis Kualitas Air",
        subtitle="Analisis strategi perawatan aquascape melalui input manual atau upload data Excel."
    )

    tab1, tab2 = st.tabs(["💧 Input Manual (Harian)", "📁 Upload Excel (Banyak Data)"])

    with tab1:
        st.markdown("### Parameter Input Harian")
        st.info("Gunakan opsi ini jika Anda hanya ingin mengecek kualitas air untuk hari ini.")
        
        with st.container():
            col1, col2, col3 = st.columns(3)
            
            with col1:
                suhu = st.number_input(
                    "Suhu Air (°C)", 
                    min_value=-10.0, 
                    max_value=60.0, 
                    value=27.0, 
                    step=0.5,
                    help=f"Rentang valid: {config.SUHU_MIN} - {config.SUHU_MAX} °C"
                )
            with col2:
                ph = st.number_input(
                    "pH Air", 
                    min_value=-2.0, 
                    max_value=16.0, 
                    value=7.0, 
                    step=0.1,
                    help=f"Rentang valid: {config.PH_MIN} - {config.PH_MAX}"
                )
            with col3:
                kekeruhan = st.number_input(
                    "Kekeruhan (NTU)", 
                    min_value=-10.0, 
                    max_value=150.0, 
                    value=10.0, 
                    step=1.0,
                    help=f"Rentang valid: {config.KEKERUHAN_MIN} - {config.KEKERUHAN_MAX} NTU"
                )

        st.markdown("<br>", unsafe_allow_html=True)
        
        kolom_tombol, _ = st.columns([1, 4])
        with kolom_tombol:
            analisis_btn = st.button("🔍 Analisis Data Harian", use_container_width=True)
            
        st.markdown("---")

        if analisis_btn:
            try:
                # 1. Validasi Input
                validasi_baris(1, suhu, ph, kekeruhan)
                
                # 2. Loading Spinner
                with st.spinner('Menjalankan Engine Fuzzy Mamdani...'):
                    time.sleep(0.5) # Sedikit delay agar spinner terlihat (UX)
                    
                    # 3. Panggil Engine Fuzzy
                    hasil_inferensi = jalankan_inferensi(suhu, ph, kekeruhan)
                    nilai_centroid, kategori = centroid(
                        hasil_inferensi["x_output"],
                        hasil_inferensi["mu_agregasi"],
                    )
                    rules_aktif = hasil_inferensi["rules_aktif"]
                    
                st.success("Analisis berhasil diselesaikan!")
                
                # Tampilkan Hasil di Cards
                st.markdown("### Hasil Analisis")
                
                warna, icon_status, teks_status = get_status_indicator(nilai_centroid)
                
                c1, c2 = st.columns(2)
                c3, c4 = st.columns(2)
                
                with c1:
                    render_card("Nilai Centroid (z*)", f"{nilai_centroid:.4f}", "🎯")
                with c2:
                    render_card("Strategi Perawatan", kategori, "📋")
                with c3:
                    render_card("Jumlah Rule Aktif", f"{len(rules_aktif)} dari 27", "⚡")
                with c4:
                    render_card("Status Kondisi Air", f"{icon_status} {teks_status}", "")
                    
                # Detail Hasil dalam Expander
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("Lihat Detail Perhitungan (Tahap demi Tahap)", expanded=False):
                    st.markdown("#### 1. Fuzzifikasi (Derajat Keanggotaan)")
                    
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.write("**Suhu:**")
                        for k, v in hasil_inferensi['mu_suhu'].items():
                            st.write(f"- μ_{k}: `{v:.4f}`")
                    with m2:
                        st.write("**pH:**")
                        for k, v in hasil_inferensi['mu_ph'].items():
                            st.write(f"- μ_{k}: `{v:.4f}`")
                    with m3:
                        st.write("**Kekeruhan:**")
                        for k, v in hasil_inferensi['mu_kekeruhan'].items():
                            st.write(f"- μ_{k}: `{v:.4f}`")
                    
                    st.divider()
                    
                    st.markdown("#### 2. Evaluasi Rule & Implikasi (MIN)")
                    if rules_aktif:
                        for r in rules_aktif:
                            st.markdown(
                                f"**R{r['rule_no']}**: IF Suhu={r['suhu']} AND pH={r['ph']} AND Kekeruhan={r['kekeruhan']} "
                                f"**THEN** {r['output']} (Fire Strength α = `{r['fire_strength']:.4f}`)"
                            )
                    else:
                        st.warning("Tidak ada rule yang aktif (semua fire strength = 0).")
                        
                    st.divider()
                    
                    st.markdown("#### 3. Agregasi (MAX) & Defuzzifikasi")
                    st.write(f"Nilai **Centroid (Center of Gravity)** dihitung dan menghasilkan z* = `{nilai_centroid:.4f}`.")
                    st.write(f"Berdasarkan nilai tersebut, sistem merekomendasikan **{kategori}**.")

            except ValidationError as e:
                st.error(f"**Validasi Gagal:** {e.pesan}")
            except Exception as e:
                st.error(f"**Terjadi Kesalahan Internal:** {str(e)}")

    with tab2:
        st.markdown("### Upload Data Excel")
        st.info("Gunakan opsi ini jika Anda memiliki banyak data pengujian yang ingin diproses sekaligus. Kolom wajib: **No, Suhu, pH, Kekeruhan**.")
        
        uploaded_file = st.file_uploader("Pilih file Excel (.xlsx)", type=["xlsx"])
        
        if uploaded_file is not None:
            try:
                df_raw = pd.read_excel(uploaded_file, engine="openpyxl")
                
                with st.expander("Preview Data Excel yang Diupload", expanded=True):
                    st.dataframe(df_raw.head(10))
                
                if st.button("🚀 Proses Semua Data Excel", use_container_width=True):
                    with st.spinner("Memvalidasi dan memproses data..."):
                        df_valid, pesan_error = validasi_dataframe(df_raw)
                        
                        if pesan_error:
                            st.warning("Ditemukan baris data tidak valid (baris ini akan diabaikan):")
                            for p in pesan_error:
                                st.write(f"- {p}")
                                
                        if df_valid.empty:
                            st.error("Tidak ada data valid yang bisa diproses. Pastikan format kolom sesuai dengan template.")
                        else:
                            hasil_list = []
                            progress_bar = st.progress(0)
                            total_data = len(df_valid)
                            
                            # Gunakan enumerate karena index DataFrame bisa jadi terpotong/tidak berurutan
                            for i, (_, row) in enumerate(df_valid.iterrows()):
                                no = int(row["No"])
                                suhu = float(row["Suhu"])
                                ph = float(row["pH"])
                                kekeruhan = float(row["Kekeruhan"])
                                
                                # Inferensi
                                hasil_inferensi = jalankan_inferensi(suhu, ph, kekeruhan)
                                nilai_centroid, kategori = centroid(
                                    hasil_inferensi["x_output"],
                                    hasil_inferensi["mu_agregasi"]
                                )
                                
                                hasil_list.append({
                                    "No": no,
                                    "Suhu": suhu,
                                    "pH": ph,
                                    "Kekeruhan": kekeruhan,
                                    "Centroid": round(nilai_centroid, 4),
                                    "Kategori": kategori
                                })
                                
                                progress_bar.progress((i + 1) / total_data)
                                
                            df_hasil = pd.DataFrame(hasil_list)
                            st.success(f"✅ Berhasil memproses {total_data} baris data!")
                            
                            st.write("### Preview Hasil Analisis")
                            st.dataframe(df_hasil, use_container_width=True)
                            
                            # Siapkan file excel untuk didownload
                            excel_buffer = BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                                df_hasil.to_excel(writer, index=False, sheet_name="Hasil Analisis")
                            
                            st.markdown("#### Unduh Hasil")
                            st.download_button(
                                label="📥 Download File Hasil (Excel)",
                                data=excel_buffer.getvalue(),
                                file_name="hasil_analisis_aquascape.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                            
            except Exception as e:
                st.error(f"Gagal memproses file Excel. Pastikan file valid dan tidak rusak. Error: {e}")
