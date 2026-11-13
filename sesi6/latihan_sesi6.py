# sesi6/latihan_sesi6.py — Latihan mandiri Sesi 6 no. 1–4
#   1. bar horizontal churn rate per payment_method, terurut, + garis vertikal rata-rata (add_vline)
#   2. scatter diubah menjadi bubble chart: size="support_calls"
#   3. sunburst region -> segmen -> kontrak (jumlah pelanggan) + cara membacanya
#   4. gauge go.Indicator(mode="gauge+number") churn rate keseluruhan
# Jalankan: python sesi6/latihan_sesi6.py
#   -> menyimpan 4 chart HTML di sesi6/output_latihan/ lalu membuka aplikasi Dash di port 8052
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc

ROOT = Path(__file__).resolve().parents[1]
STATUS = {"Bertahan": "#2a78d6", "Churn": "#eb6834"}
KATEGORI = ["#2a78d6", "#1baf7a", "#eda100", "#4a3aa7", "#e87ba4"]
KONTRAK = ["Bulanan", "Tahunan", "Dua Tahun"]

df = pd.read_csv(ROOT / "data" / "customer_churn.csv", parse_dates=["signup_date"])
df["status"] = df["churn"].map({0: "Bertahan", 1: "Churn"})
df["tagihan_ribu"] = df["monthly_charges"] / 1000
rata2 = df.churn.mean()

fig = {}

# 1. Bar horizontal terurut + garis rata-rata nasional
pm = df.groupby("payment_method", as_index=False)["churn"].mean().sort_values("churn")
f = px.bar(pm, x="churn", y="payment_method", orientation="h", text_auto=".1%",
           color_discrete_sequence=["#eb6834"],
           labels={"churn": "Churn rate", "payment_method": "Metode pembayaran"},
           title="Transfer Bank memiliki churn rate tertinggi")
f.add_vline(x=rata2, line_dash="dot", annotation_text=f"rata-rata {rata2:.1%}",
            annotation_position="top")
f.update_xaxes(tickformat=".0%", range=[0, 0.45])
fig["L1_bar_payment"] = f

# 2. Bubble chart: ukuran titik = jumlah panggilan ke CS
f = px.scatter(df, x="tenure_months", y="tagihan_ribu", color="status", size="support_calls",
               size_max=18, opacity=0.5, color_discrete_map=STATUS,
               hover_name="customer_id",
               hover_data={"contract_type": True, "support_calls": True, "tagihan_ribu": ":.0f"},
               labels={"tenure_months": "Tenure (bulan)", "tagihan_ribu": "Tagihan (ribu Rp)",
                       "support_calls": "Panggilan CS"},
               title="Bubble: titik besar (sering menghubungi CS) banyak yang churn di tenure pendek")
fig["L2_bubble"] = f

# 3. Sunburst: lingkar dalam = region, tengah = segmen, luar = kontrak
cnt = df.groupby(["region", "segment", "contract_type"]).size().reset_index(name="pelanggan")
f = px.sunburst(cnt, path=["region", "segment", "contract_type"], values="pelanggan",
                color="region", color_discrete_sequence=KATEGORI,
                title="Sunburst: region → segmen → kontrak (jumlah pelanggan)")
f.update_traces(insidetextorientation="radial",
                hovertemplate="%{label}<br>%{value} pelanggan<br>"
                              "%{percentParent:.1%} dari %{parent}<extra></extra>")
fig["L3_sunburst"] = f

# 4. Gauge churn rate keseluruhan
f = go.Figure(go.Indicator(
    mode="gauge+number", value=rata2 * 100, number={"suffix": "%", "valueformat": ".1f"},
    title={"text": "Churn rate keseluruhan"},
    gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#eb6834"},
           "steps": [{"range": [0, 30], "color": "#e3f4ec"},
                     {"range": [30, 60], "color": "#fdf1d6"},
                     {"range": [60, 100], "color": "#fbe1e1"}]}))
fig["L4_gauge"] = f

for f in fig.values():
    f.update_layout(template="plotly_white")

CARA_BACA = [
    html.H4("Cara membaca sunburst (latihan no. 3)"),
    html.Ul([
        html.Li("Lingkar dalam = region, lingkar tengah = segmen, lingkar luar = jenis kontrak."),
        html.Li("Lebar sudut setiap irisan sebanding dengan jumlah pelanggan. Jawa adalah irisan "
                f"terbesar ({(df.region == 'Jawa').mean():.0%} pelanggan)."),
        html.Li("Baca dari dalam ke luar: setiap irisan luar adalah bagian dari irisan di dalamnya, "
                "misalnya Jawa → Retail → Bulanan."),
        html.Li("Arahkan kursor untuk melihat jumlah dan persentase terhadap induknya. Klik satu irisan "
                "untuk memperbesar cabang itu; klik bagian tengah untuk kembali."),
        html.Li("Sunburst menunjukkan komposisi (berapa banyak), bukan churn rate. Untuk membandingkan "
                "churn antar-kelompok, pakai bar chart atau heatmap."),
    ]),
]

app = Dash(__name__, title="Latihan Sesi 6")
app.layout = html.Div(style={"maxWidth": "1150px", "margin": "auto", "fontFamily": "Arial",
                             "padding": "0 16px"}, children=[
    html.H1("Latihan Sesi 6 — Plotly"),
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "12px"}, children=[
        dcc.Graph(figure=fig["L1_bar_payment"]), dcc.Graph(figure=fig["L4_gauge"])]),
    dcc.Graph(figure=fig["L2_bubble"]),
    html.Div(style={"display": "grid", "gridTemplateColumns": "3fr 2fr", "gap": "12px",
                    "alignItems": "center"}, children=[
        dcc.Graph(figure=fig["L3_sunburst"].update_layout(height=520)), html.Div(CARA_BACA)]),
])

if __name__ == "__main__":
    OUT = ROOT / "sesi6" / "output_latihan"; OUT.mkdir(exist_ok=True)
    for nama, f in fig.items():
        f.write_html(OUT / f"{nama}.html", include_plotlyjs="cdn")
    print(f"{len(fig)} chart HTML tersimpan di", OUT)
    app.run(debug=False, port=8052)
