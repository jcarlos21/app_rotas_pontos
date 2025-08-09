import os
import io
import folium
import streamlit as st
import pandas as pd
from typing import Tuple, List

from streamlit_folium import st_folium

from osrm_client import OSRMClient
from kmz_utils import geojson_line_with_markers_to_kmz
from parsers import parse_csv_xlsx, parse_kml_bytes, parse_kmz

st.set_page_config(page_title="OSRM + KMZ – Rotas por Pontos", layout="wide")

st.title("🗺️ Rotas por Pontos (OSRM + KMZ)")
st.caption(
    "Envie CSV/XLSX/KML/KMZ com NOME, LATITUDE, LONGITUDE **ou** digite duas coordenadas. "
    "Gera rota urbana (ruas/avenidas/BR via OSRM), mostra no mapa e exporta KMZ."
)

# ---------------- Sidebar (OSRM) ----------------
with st.sidebar:
    st.header("Configurações OSRM")
    base_url = st.text_input("URL do OSRM", value="https://router.project-osrm.org")
    profile = st.selectbox("Perfil", options=["driving", "cycling", "foot"], index=0)
    client = OSRMClient(base_url=base_url, profile=profile)

# ---------------- Entrada: arquivo ou 2 coords ----------------
mode = st.radio(
    "Como deseja fornecer as coordenadas?",
    ["Arquivo (múltiplos pontos)", "Digitar 2 coordenadas"],
    index=0,
)

coords_latlon: List[Tuple[float, float]] = []
labels: List[str] = []

if mode == "Arquivo (múltiplos pontos)":
    up = st.file_uploader(
        "Envie um arquivo .csv, .xlsx, .kml ou .kmz",
        type=["csv", "xlsx", "kml", "kmz"],
    )
    if up is not None:
        ext = f".{up.name.split('.')[-1].lower()}"
        data = up.read()
        try:
            if ext in (".csv", ".xlsx"):
                df = parse_csv_xlsx(data, ext)
            elif ext == ".kml":
                df = parse_kml_bytes(data)
            else:
                df = parse_kmz(data)

            st.success(f"{len(df)} ponto(s) carregado(s). A **ordem do arquivo** será respeitada.")
            labels = df["NOME"].astype(str).tolist()
            coords_latlon = list(
                zip(df["LATITUDE"].astype(float), df["LONGITUDE"].astype(float))
            )
        except Exception as e:
            st.error(f"Erro ao ler arquivo: {e}")

else:
    st.write(
        "Forneça as duas coordenadas no formato `lat, lon` (ex.: `-5.8484, -35.8393`)."
    )
    c1, c2 = st.columns(2)
    with c1:
        s1 = st.text_input("Coordenada A (lat, lon)", value="-5.79448, -35.21100")
    with c2:
        s2 = st.text_input("Coordenada B (lat, lon)", value="-5.81290, -35.23740")

    def _parse_latlon(s: str) -> Tuple[float, float]:
        parts = s.split(",")
        if len(parts) != 2:
            raise ValueError("Use o formato lat, lon")
        lat = float(parts[0].strip())
        lon = float(parts[1].strip())
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError("Faixa inválida de latitude/longitude")
        return (lat, lon)

    try:
        a = _parse_latlon(s1)
        b = _parse_latlon(s2)
        coords_latlon = [a, b]
        labels = ["A", "B"]
    except Exception as e:
        if s1 or s2:
            st.warning(f"Coordenadas inválidas: {e}")

# ---------------- Ação ----------------
run = st.button("Calcular rota")

if run:
    if len(coords_latlon) < 2:
        st.error("É necessário ao menos 2 pontos.")
    else:
        try:
            route = client.route_multi(coords_latlon, overview="full")
            distance_m = route["distance"]
            duration_s = route["duration"]
            coords = route["geometry"]["coordinates"]  # [[lon, lat], ...]

            st.success(
                f"Distância: {distance_m/1000:.2f} km | Duração: {duration_s/60:.1f} min | Pontos: {len(coords_latlon)}"
            )

            # --------- Mapa (grandão) com streamlit-folium ---------
            mid_lat, mid_lon = coords_latlon[0]
            m = folium.Map(location=[mid_lat, mid_lon], zoom_start=13, control_scale=True)

            for (lat, lon), name in zip(coords_latlon, labels):
                folium.Marker([lat, lon], tooltip=name).add_to(m)

            folium.PolyLine([(lat, lon) for lon, lat in coords], weight=5).add_to(m)

            st_folium(m, width=None, height=820)

            # --------- Exportar KMZ com marcadores ----------
            origem_latlon = coords_latlon[0]
            destino_latlon = coords_latlon[-1]
            nome_origem = (labels[0] if labels else "Origem")
            nome_destino = (labels[-1] if labels else "Destino")

            kmz_bytes = io.BytesIO()
            tmp_path = "rota_osrm_temp.kmz"
            geojson_line_with_markers_to_kmz(
                coords,                      # lista [lon,lat] da rota (OSRM)
                origem_latlon,               # (lat, lon)
                destino_latlon,              # (lat, lon)
                tmp_path,
                route_name="Rota OSRM",
                start_name=nome_origem,
                end_name=nome_destino,
                description=f"{profile} – {distance_m/1000:.2f} km",
            )
            with open(tmp_path, "rb") as f:
                kmz_bytes.write(f.read())
            kmz_bytes.seek(0)
            kmz_data = kmz_bytes.getvalue()
            os.remove(tmp_path)

            st.session_state["kmz_data"] = kmz_data

            st.download_button(
                label="📥 Baixar KMZ",
                data=kmz_data,
                file_name="rota_osrm.kmz",
                mime="application/vnd.google-earth.kmz",
            )

        except Exception as e:
            st.error(f"Falha ao obter rota: {e}")

if "kmz_data" in st.session_state:
    st.download_button(
        label="📥 Baixar KMZ (última rota)",
        data=st.session_state["kmz_data"],
        file_name="rota_osrm.kmz",
        mime="application/vnd.google-earth.kmz",
    )