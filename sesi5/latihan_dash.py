# sesi5/latihan_dash.py — Latihan mandiri Sesi 5 no. 1–4 (jalankan: python sesi5/latihan_dash.py)
# Pengembangan dari app_dash_dasar.py:
#   1. KPI card kelima: rata-rata jumlah keluhan
#   2. grafik kedua (churn rate per region), dua grafik berdampingan dengan CSS grid
#   3. DataTable dengan sorting (sort_action="native") dan paging (page_size=5)
#   4. gaya dipindahkan ke sesi5/assets/style.css, komponen memakai className
from pathlib import Path
import pandas as pd
from dash import Dash, html, dcc, dash_table

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "customer_churn.csv", parse_dates=["signup_date"])


def churn_per(kolom):
    out = (df.groupby(kolom)
             .agg(pelanggan=("customer_id", "count"), churn_rate=("churn", "mean"))
             .reset_index())
    out["churn_rate"] = (out["churn_rate"] * 100).round(1)
    return out


ringkas = churn_per("contract_type")
per_region = churn_per("region").sort_values("churn_rate", ascending=False)
# Tabel detail region x kontrak (15 baris) agar paging 5 baris per halaman benar-benar terlihat
detail = churn_per(["region", "contract_type"])

app = Dash(__name__, title="Dash Dasar — Latihan")


# No. 4 — tidak ada lagi dict gaya; kartu memakai className dari assets/style.css
def kartu(judul, nilai):
    return html.Div([html.P(judul, className="kartu-judul"),
                     html.H2(nilai, className="kartu-nilai")], className="kartu")


def grafik_bar(data, x, judul, warna):
    return dcc.Graph(figure={
        "data": [{"type": "bar", "x": data[x], "y": data["churn_rate"],
                  "marker": {"color": warna},
                  "text": [f"{v:.1f}%" for v in data["churn_rate"]], "textposition": "outside"}],
        "layout": {"title": {"text": judul}, "yaxis": {"title": "Churn rate (%)"},
                   "height": 350, "margin": {"t": 50, "b": 40, "l": 50, "r": 10}},
    })


app.layout = html.Div(className="halaman", children=[
    html.H1("Dashboard Churn — Versi Dash"),
    html.P("Latihan Sesi 5: lima KPI, dua grafik berdampingan, tabel dengan sorting & paging.",
           className="subjudul"),

    # No. 1 — KPI kelima
    html.Div(className="kartu-baris", children=[
        kartu("Total pelanggan", f"{len(df):,}"),
        kartu("Churn rate", f"{df.churn.mean():.1%}"),
        kartu("Rata-rata tenure", f"{df.tenure_months.mean():.1f} bln"),
        kartu("Region", df.region.nunique()),
        kartu("Rata-rata keluhan", f"{df.num_complaints.mean():.2f}"),
    ]),

    # No. 2 — dua grafik berdampingan dengan CSS grid (class .grid-2)
    html.Div(className="grid-2", children=[
        grafik_bar(ringkas, "contract_type", "Churn rate per jenis kontrak", "#C44E52"),
        grafik_bar(per_region, "region", "Churn rate per region", "#2a78d6"),
    ]),

    # No. 3 — sorting & paging; klik judul kolom untuk mengurutkan
    html.H3("Ringkasan per region × kontrak"),
    dash_table.DataTable(data=detail.to_dict("records"),
                         columns=[{"name": c, "id": c} for c in detail.columns],
                         sort_action="native", page_size=5,
                         style_cell={"padding": "6px", "textAlign": "left"},
                         style_header={"fontWeight": "bold", "background": "#E9EDF5"}),

    html.Hr(),
    html.Small("Sumber: data latihan sintetis customer_churn.csv", className="sumber"),
])

if __name__ == "__main__":
    app.run(debug=True, port=8051)      # port 8051 agar bisa berjalan bersamaan dengan app_dash_dasar
