"""
ui/main_page.py
===============
Mengatur tiga halaman utama: INPUT, PROSES, OUTPUT.
"""

import streamlit as st
import pandas as pd
from io import BytesIO
import config
from fuzzy.validator import ValidationError, validasi_baris, validasi_dataframe
from fuzzy.inference import jalankan_inferensi
from fuzzy.defuzzification import centroid


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────

DESKRIPSI_REKOMENDASI = {
    "Perawatan Ringan": {
        "emoji": "🟢",
        "warna_class": "result-ringan",
        "warna_hex": "#10b981",
        "ringkasan": "Kondisi air aquascape Anda dalam keadaan sangat baik dan stabil.",
        "detail": [
            "**Penggantian air:** Cukup lakukan pergantian air sebesar 10–20% dari total volume akuarium setiap 1–2 minggu sekali. Kondisi air saat ini masih sangat mendukung kehidupan ikan dan tanaman.",
            "**Filter & sirkulasi:** Bersihkan media filter biologis secara ringan (bilas dengan air akuarium, jangan gunakan air keran) setiap 2–4 minggu. Pastikan aliran air tetap lancar.",
            "**Pemupukan:** Berikan pupuk cair mikro dan makro sesuai dosis standar. Tanaman dalam kondisi baik akan menyerap nutrisi secara optimal.",
            "**Pencahayaan:** Pertahankan jadwal pencahayaan 8–10 jam per hari. Tidak ada penyesuaian khusus yang diperlukan.",
            "**Pemantauan:** Lanjutkan pemantauan rutin 1x seminggu untuk memastikan parameter tetap stabil. Catat setiap perubahan sebagai data historis.",
            "**Ikan & tanaman:** Kondisi ini ideal untuk pertumbuhan tanaman dan kesehatan ikan. Anda dapat mempertimbangkan penambahan stok tanaman atau ikan jika kapasitas akuarium memungkinkan.",
        ]
    },
    "Perawatan Sedang": {
        "emoji": "🟡",
        "warna_class": "result-sedang",
        "warna_hex": "#f59e0b",
        "ringkasan": "Kondisi air aquascape memerlukan perhatian. Tindakan korektif diperlukan segera.",
        "detail": [
            "**Penggantian air segera:** Lakukan pergantian air sebesar 25–40% dalam waktu 24–48 jam ke depan untuk mengembalikan keseimbangan parameter. Gunakan air yang sudah dikondisikan (dechlorinated).",
            "**Periksa dan bersihkan filter:** Bersihkan atau ganti media filter mekanik (kapas filter) yang mungkin sudah tersumbat dan menjadi sumber polutan. Jangan ganti semua media biologis sekaligus.",
            "**Cek sumber masalah:** Identifikasi penyebab penurunan kualitas air — apakah dari overfeeding (kelebihan pakan), kepadatan ikan, tanaman mati membusuk, atau kurangnya sirkulasi.",
            "**Penyesuaian pH:** Jika pH terlalu asam atau basa, gunakan produk penyeimbang pH secara bertahap (jangan ubah drastis dalam satu waktu untuk menghindari syok pada ikan).",
            "**Kurangi pemberian pakan:** Sementara kurangi frekuensi makan ikan menjadi 1x sehari dan pastikan tidak ada sisa pakan yang mengendap di dasar akuarium.",
            "**Pemantauan intensif:** Ukur ulang parameter (suhu, pH, kekeruhan) setiap hari selama 5–7 hari ke depan hingga nilai kembali ke rentang normal.",
        ]
    },
    "Perawatan Intensif": {
        "emoji": "🔴",
        "warna_class": "result-intensif",
        "warna_hex": "#ef4444",
        "ringkasan": "Kondisi air aquascape dalam keadaan KRITIS. Tindakan penanganan segera sangat diperlukan untuk menyelamatkan ekosistem.",
        "detail": [
            "**Penggantian air darurat:** Segera lakukan pergantian air sebesar 50–70% dari total volume akuarium. Lakukan secara bertahap (30% dulu, tunggu 1 jam, lalu 30% lagi) untuk menghindari syok osmotik pada ikan.",
            "**Isolasi ikan (jika perlu):** Jika ikan menunjukkan tanda-tanda stres (megap-megap di permukaan, diam di dasar, warna pucat, sisik berdiri), segera pindahkan ke akuarium karantina sementara.",
            "**Bersihkan total substrat:** Gunakan siphon/selang untuk menyedot kotoran dan detritus yang mengendap di dasar. Substrat kotor adalah sumber utama polutan amonia dan nitrit.",
            "**Ganti media filter mekanik:** Ganti kapas filter dan semua media mekanik yang sudah jenuh. Pertahankan sebagian media biologis untuk menjaga bakteri nitrifikasi yang berguna.",
            "**Aerasi tambahan:** Tambahkan aerator (batu udara) sementara untuk meningkatkan kadar oksigen terlarut yang kemungkinan sangat rendah saat ini.",
            "**Hentikan pemberian pakan:** Puasakan ikan selama 2–3 hari untuk meminimalkan produksi limbah organik selama proses pemulihan. Ikan dapat bertahan tanpa makan hingga 1 minggu.",
            "**Evaluasi ulang sistem:** Setelah kondisi stabil (3–5 hari), evaluasi kembali kepadatan ikan, kapasitas filter, dan jadwal perawatan rutin untuk mencegah kejadian serupa terulang.",
        ]
    }
}


def _render_proses_satu_data(no, suhu, ph, kekeruhan, hasil, nilai_centroid, kategori):
    """Merender detail proses fuzzy untuk satu data dalam expander."""
    label = f"Data #{no} — Suhu: {suhu}°C | pH: {ph} | Kekeruhan: {kekeruhan} NTU → {kategori}"
    with st.expander(label, expanded=(no == 1)):
        mu_suhu = hasil["mu_suhu"]
        mu_ph = hasil["mu_ph"]
        mu_kekeruhan = hasil["mu_kekeruhan"]
        rules_aktif = hasil["rules_aktif"]
        x_out = hasil["x_output"]
        mu_ag = hasil["mu_agregasi"]

        # ── STEP 1: FUZZIFIKASI ──────────────────────────────────────────
        st.markdown("#### 1️⃣ Fuzzifikasi")
        st.markdown(
            """
            <div class="formula-box">
            Rumus Triangular Membership Function (MF):<br>
            &nbsp;&nbsp;μ(x) = 0,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; jika x ≤ a atau x ≥ c<br>
            &nbsp;&nbsp;μ(x) = (x − a) / (b − a),&nbsp; jika a < x ≤ b<br>
            &nbsp;&nbsp;μ(x) = (c − x) / (c − b),&nbsp; jika b < x < c<br>
            &nbsp;&nbsp;μ(x) = 1,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; jika x = b
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**🌡️ Suhu Air**")
            for kat, (a, b, c) in config.SUHU_MF.items():
                mu = mu_suhu[kat]
                x = suhu
                if x <= b:
                    rumus = f"({x} − {a}) / ({b} − {a}) = **{mu:.4f}**" if a != b else f"1.0 (shoulder kiri)"
                else:
                    rumus = f"({c} − {x}) / ({c} − {b}) = **{mu:.4f}**" if b != c else f"1.0 (shoulder kanan)"
                if mu == 0:
                    st.markdown(f"- μ_{kat}: `0.0000` *(di luar rentang)*")
                else:
                    st.markdown(f"- μ_{kat}: {rumus}")

        with col2:
            st.markdown("**🧪 pH Air**")
            for kat, (a, b, c) in config.PH_MF.items():
                mu = mu_ph[kat]
                x = ph
                if x <= b:
                    rumus = f"({x} − {a}) / ({b} − {a}) = **{mu:.4f}**" if a != b else "1.0 (shoulder kiri)"
                else:
                    rumus = f"({c} − {x}) / ({c} − {b}) = **{mu:.4f}**" if b != c else "1.0 (shoulder kanan)"
                if mu == 0:
                    st.markdown(f"- μ_{kat}: `0.0000` *(di luar rentang)*")
                else:
                    st.markdown(f"- μ_{kat}: {rumus}")

        with col3:
            st.markdown("**💧 Kekeruhan**")
            for kat, (a, b, c) in config.KEKERUHAN_MF.items():
                mu = mu_kekeruhan[kat]
                x = kekeruhan
                if x <= b:
                    rumus = f"({x} − {a}) / ({b} − {a}) = **{mu:.4f}**" if a != b else "1.0 (shoulder kiri)"
                else:
                    rumus = f"({c} − {x}) / ({c} − {b}) = **{mu:.4f}**" if b != c else "1.0 (shoulder kanan)"
                if mu == 0:
                    st.markdown(f"- μ_{kat}: `0.0000` *(di luar rentang)*")
                else:
                    st.markdown(f"- μ_{kat}: {rumus}")

        st.markdown("---")

        # ── STEP 2: EVALUASI RULE ────────────────────────────────────────
        st.markdown("#### 2️⃣ Evaluasi Rule & Implikasi (Operator AND = MIN)")
        st.markdown(
            """
            <div class="formula-box">
            α_i = MIN(μ_suhu, μ_ph, μ_kekeruhan)<br>
            Rule aktif jika α_i > 0. Output rule dipotong (clipping) pada nilai α_i.
            </div>
            """,
            unsafe_allow_html=True
        )
        if rules_aktif:
            data_rules = []
            for r in rules_aktif:
                data_rules.append({
                    "Rule": f"R{r['rule_no']}",
                    "IF Suhu": r["suhu"],
                    "AND pH": r["ph"],
                    "AND Kekeruhan": r["kekeruhan"],
                    "THEN Output": r["output"],
                    "α (Fire Strength)": f"{r['fire_strength']:.4f}"
                })
            df_rules = pd.DataFrame(data_rules)
            st.dataframe(df_rules, use_container_width=True, hide_index=True)
        else:
            st.warning("Tidak ada rule yang aktif untuk input ini.")

        st.markdown("---")

        # ── STEP 3: AGREGASI ─────────────────────────────────────────────
        st.markdown("#### 3️⃣ Agregasi Output (Operator MAX)")
        st.markdown(
            """
            <div class="formula-box">
            μ_agregasi(x) = MAX(μ_clip_R1(x), μ_clip_R2(x), ..., μ_clip_RN(x))<br>
            Semua output rule yang aktif digabungkan menggunakan fungsi MAX.
            </div>
            """,
            unsafe_allow_html=True
        )
        mu_max = float(mu_ag.max())
        st.markdown(f"Nilai puncak agregasi: **{mu_max:.4f}** (dari {len(rules_aktif)} rule aktif)")

        st.markdown("---")

        # ── STEP 4: DEFUZZIFIKASI ────────────────────────────────────────
        st.markdown("#### 4️⃣ Defuzzifikasi (Metode Centroid / Center of Gravity)")
        import numpy as np
        numerator = float(np.sum(x_out * mu_ag))
        denominator = float(np.sum(mu_ag))
        st.markdown(
            f"""
            <div class="formula-box">
            z* = Σ[x_i × μ(x_i)] / Σ[μ(x_i)]<br><br>
            Numerator &nbsp;= Σ[x_i × μ(x_i)] = {numerator:.4f}<br>
            Denominator = Σ[μ(x_i)]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = {denominator:.4f}<br>
            <br>
            <b>z* = {numerator:.4f} / {denominator:.4f} = {nilai_centroid:.4f}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Kategorisasi
        if nilai_centroid < 37.5:
            kategori_label = "Perawatan Ringan (0 – 37.5)"
        elif nilai_centroid < 62.5:
            kategori_label = "Perawatan Sedang (37.5 – 62.5)"
        else:
            kategori_label = "Perawatan Intensif (62.5 – 100)"

        st.markdown(f"**Nilai z* = {nilai_centroid:.4f}** → masuk kategori **{kategori_label}**")


def _render_output_satu(kategori, nilai_centroid):
    """Merender kartu output rekomendasi."""
    info = DESKRIPSI_REKOMENDASI[kategori]
    st.markdown(
        f"""
        <div class="{info['warna_class']}">
            <div style="font-size:3rem;">{info['emoji']}</div>
            <div class="result-title" style="color:{info['warna_hex']};">{kategori}</div>
            <p style="font-size:1.05rem; color:#374151; margin-top:0.5rem;">{info['ringkasan']}</p>
            <p style="color:#64748b; font-size:0.9rem;">Nilai Centroid (z*): <b>{nilai_centroid:.4f}</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 Panduan Tindakan")
    for poin in info["detail"]:
        st.markdown(f"- {poin}")


# ─────────────────────────────────────────────
# HALAMAN INPUT
# ─────────────────────────────────────────────

def render_input():
    st.markdown("## 📥 Input Data")
    st.markdown("Pilih cara memasukkan data parameter kualitas air aquascape Anda:")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="large")

    # ── INPUT MANUAL ─────────────────────────────────────────────────────
    with col_left:
        st.markdown(
            """
            <div class="section-card">
                <h3 style="color:#0f4c81; margin-top:0;">💧 Input Manual (Harian)</h3>
                <p style="color:#64748b;">Masukkan nilai yang Anda ukur hari ini secara langsung.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        suhu = st.number_input("🌡️ Suhu Air (°C)", min_value=0.0, max_value=50.0, value=27.0, step=0.5,
                               help="Rentang valid: 0 – 50 °C")
        ph = st.number_input("🧪 pH Air", min_value=0.0, max_value=14.0, value=7.0, step=0.1,
                             help="Rentang valid: 0 – 14")
        kekeruhan = st.number_input("💧 Kekeruhan (NTU)", min_value=0.0, max_value=100.0, value=10.0, step=1.0,
                                    help="Rentang valid: 0 – 100 NTU")

        if st.button("🔍 Analisis Sekarang", use_container_width=True):
            try:
                validasi_baris(1, suhu, ph, kekeruhan)
                hasil = jalankan_inferensi(suhu, ph, kekeruhan)
                nilai_centroid, kategori = centroid(hasil["x_output"], hasil["mu_agregasi"])
                st.session_state["mode"] = "manual"
                st.session_state["hasil_manual"] = {
                    "no": 1, "suhu": suhu, "ph": ph, "kekeruhan": kekeruhan,
                    "hasil": hasil, "centroid": nilai_centroid, "kategori": kategori
                }
                st.session_state["page_goto"] = "proses"
                st.success("✅ Data berhasil dianalisis! Pindah ke halaman **PROSES** atau **OUTPUT** di sidebar.")
            except ValidationError as e:
                st.error(f"Validasi gagal: {e.pesan}")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

    # ── UPLOAD EXCEL ─────────────────────────────────────────────────────
    with col_right:
        st.markdown(
            """
            <div class="section-card">
                <h3 style="color:#0f4c81; margin-top:0;">📁 Upload Excel (Banyak Data)</h3>
                <p style="color:#64748b;">Upload file Excel berisi banyak data untuk diproses sekaligus.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            **Format kolom yang wajib ada di file Excel:**
            | No | Suhu | pH | Kekeruhan |
            |----|------|----|-----------|
            | 1  | 27.0 | 7.0 | 10.0   |
            | 2  | 30.5 | 6.5 | 45.0   |
            """
        )
        uploaded = st.file_uploader("📂 Klik di sini untuk pilih file Excel (.xlsx)", type=["xlsx"])

        if uploaded:
            try:
                df_raw = pd.read_excel(uploaded, engine="openpyxl")
                st.success(f"File berhasil dibaca: **{len(df_raw)} baris** data ditemukan.")
                st.dataframe(df_raw.head(5), use_container_width=True)

                if st.button("🚀 Proses Semua Data", use_container_width=True):
                    df_valid, errors = validasi_dataframe(df_raw)
                    if errors:
                        for e in errors:
                            st.warning(e)
                    if df_valid.empty:
                        st.error("Tidak ada data valid yang bisa diproses.")
                    else:
                        hasil_list = []
                        bar = st.progress(0)
                        total = len(df_valid)
                        for i, (_, row) in enumerate(df_valid.iterrows()):
                            no = int(row["No"])
                            s = float(row["Suhu"])
                            p = float(row["pH"])
                            k = float(row["Kekeruhan"])
                            h = jalankan_inferensi(s, p, k)
                            nc, kat = centroid(h["x_output"], h["mu_agregasi"])
                            hasil_list.append({
                                "no": no, "suhu": s, "ph": p, "kekeruhan": k,
                                "hasil": h, "centroid": nc, "kategori": kat
                            })
                            bar.progress((i + 1) / total)
                        st.session_state["mode"] = "excel"
                        st.session_state["hasil_excel"] = hasil_list
                        st.success(f"✅ {total} data berhasil diproses! Pindah ke halaman **PROSES** atau **OUTPUT** di sidebar.")
            except Exception as e:
                st.error(f"Gagal membaca file: {e}")


# ─────────────────────────────────────────────
# HALAMAN PROSES
# ─────────────────────────────────────────────

def render_proses():
    st.markdown("## ⚙️ Detail Proses Perhitungan Fuzzy")
    st.markdown("Berikut adalah penjabaran lengkap setiap tahap perhitungan Logika Fuzzy Mamdani.")
    st.markdown("---")

    mode = st.session_state.get("mode")

    if mode == "manual":
        d = st.session_state["hasil_manual"]
        _render_proses_satu_data(d["no"], d["suhu"], d["ph"], d["kekeruhan"],
                                  d["hasil"], d["centroid"], d["kategori"])

    elif mode == "excel":
        hasil_list = st.session_state["hasil_excel"]
        st.info(f"Menampilkan detail perhitungan untuk **{len(hasil_list)} data**. Klik setiap baris untuk membuka detail.")
        for d in hasil_list:
            _render_proses_satu_data(d["no"], d["suhu"], d["ph"], d["kekeruhan"],
                                      d["hasil"], d["centroid"], d["kategori"])
    else:
        st.info("Belum ada data yang dianalisis. Silakan masukkan data di halaman **📥 INPUT** terlebih dahulu.")


# ─────────────────────────────────────────────
# HALAMAN OUTPUT
# ─────────────────────────────────────────────

def render_output():
    st.markdown("## 📤 Rekomendasi Strategi Perawatan")
    st.markdown("---")

    mode = st.session_state.get("mode")

    if mode == "manual":
        d = st.session_state["hasil_manual"]
        st.markdown(f"**Data:** Suhu {d['suhu']}°C | pH {d['ph']} | Kekeruhan {d['kekeruhan']} NTU")
        st.markdown("<br>", unsafe_allow_html=True)
        _render_output_satu(d["kategori"], d["centroid"])

    elif mode == "excel":
        hasil_list = st.session_state["hasil_excel"]
        st.markdown(f"Total data diproses: **{len(hasil_list)} baris**")

        # Ringkasan distribusi
        from collections import Counter
        dist = Counter(d["kategori"] for d in hasil_list)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("🟢 Perawatan Ringan", dist.get("Perawatan Ringan", 0))
        with c2:
            st.metric("🟡 Perawatan Sedang", dist.get("Perawatan Sedang", 0))
        with c3:
            st.metric("🔴 Perawatan Intensif", dist.get("Perawatan Intensif", 0))

        st.markdown("---")

        # Tabel hasil + download
        df_out = pd.DataFrame([{
            "No": d["no"], "Suhu (°C)": d["suhu"], "pH": d["ph"],
            "Kekeruhan (NTU)": d["kekeruhan"],
            "Centroid (z*)": round(d["centroid"], 4),
            "Rekomendasi": d["kategori"]
        } for d in hasil_list])
        st.dataframe(df_out, use_container_width=True, hide_index=True)

        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_out.to_excel(w, index=False, sheet_name="Hasil Analisis")
        st.download_button("📥 Download Hasil Excel", buf.getvalue(),
                           "hasil_analisis_aquascape.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

        st.markdown("---")
        st.markdown("### Panduan Tindakan per Kategori")

        # Tampilkan panduan untuk setiap kategori yang muncul
        for kat in ["Perawatan Ringan", "Perawatan Sedang", "Perawatan Intensif"]:
            if dist.get(kat, 0) > 0:
                with st.expander(f"{DESKRIPSI_REKOMENDASI[kat]['emoji']} {kat} ({dist[kat]} data)", expanded=False):
                    _render_output_satu(kat, next(d["centroid"] for d in hasil_list if d["kategori"] == kat))

    else:
        st.info("Belum ada data yang dianalisis. Silakan masukkan data di halaman **📥 INPUT** terlebih dahulu.")


# ─────────────────────────────────────────────
# ROUTER UTAMA
# ─────────────────────────────────────────────

def render_main(page: str):
    if "📥" in page:
        render_input()
    elif "⚙️" in page:
        render_proses()
    elif "📤" in page:
        render_output()
