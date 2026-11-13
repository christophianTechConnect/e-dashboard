# sesi7/app_sapa.py — 7.2 Contoh callback paling sederhana (jalankan: python sesi7/app_sapa.py)
from dash import Dash, html, dcc, Input, Output, callback

app = Dash(__name__)
app.layout = html.Div([
    dcc.Input(id="nama", value="", placeholder="Ketik nama"),
    html.H3(id="sapaan"),
])


@callback(Output("sapaan", "children"), Input("nama", "value"))
def sapa(nama):
    return f"Halo, {nama}!" if nama else "Silakan isi nama."


if __name__ == "__main__":
    app.run(debug=True)
