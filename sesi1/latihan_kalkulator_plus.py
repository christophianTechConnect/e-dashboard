# sesi1/latihan_kalkulator_plus.py — Latihan mandiri Sesi 1 no. 1, 2, dan 4
import streamlit as st

st.set_page_config(page_title="Kalkulator Tagihan Plus", page_icon="🧾")
st.title("🧾 Kalkulator Estimasi Tagihan Internet")
st.write("Masukkan paket dan durasi berlangganan untuk melihat estimasi biaya.")

# No. 1 — tambah layanan "Satelit" Rp550.000
HARGA = {"DSL": 260_000, "Fiber": 420_000, "Mobile Broadband": 310_000, "Satelit": 550_000}
DISKON = {"Bulanan": 0.00, "Tahunan": 0.10, "Dua Tahun": 0.18}

layanan = st.selectbox("Jenis layanan", list(HARGA))
kontrak = st.radio("Jenis kontrak", list(DISKON), horizontal=True)
bulan = st.number_input("Durasi (bulan)", min_value=1, max_value=72, value=12, step=1)

# No. 2 — slider diskon promosi tambahan 0–20%
promo = st.slider("Diskon promosi tambahan (%)", 0, 20, 0)

ppn = st.checkbox("Tambahkan PPN 11%", value=True)

# No. 4 — penghitung klik dengan session_state (nilainya bertahan antar-rerun)
if "jumlah_klik" not in st.session_state:
    st.session_state.jumlah_klik = 0

if st.button("Hitung", type="primary"):
    st.session_state.jumlah_klik += 1

    per_bulan = HARGA[layanan] * (1 - DISKON[kontrak]) * (1 - promo / 100)
    total = per_bulan * bulan * (1.11 if ppn else 1)

    st.metric("Biaya per bulan", f"Rp{per_bulan:,.0f}".replace(",", "."))
    hemat = 1 - (1 - DISKON[kontrak]) * (1 - promo / 100)
    st.metric("Total estimasi", f"Rp{total:,.0f}".replace(",", "."),
              delta=f"hemat {hemat:.0%}" if hemat else None)
    st.caption("Estimasi bersifat ilustratif untuk latihan.")

st.caption(f"Tombol Hitung sudah diklik {st.session_state.jumlah_klik} kali.")
