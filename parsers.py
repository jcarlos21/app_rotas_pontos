from typing import Tuple, List
import pandas as pd
import zipfile
from fastkml import kml

ExpectedCols = ["NOME", "LATITUDE", "LONGITUDE"]

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Normaliza cabeçalhos ignorando acentos/caixa e removendo espaços
    df2 = df.copy()
    mapper = {}
    for c in df2.columns:
        c_norm = (
            str(c)
            .strip()
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
            .upper()
        )
        mapper[c] = c_norm
    df2.rename(columns=mapper, inplace=True)
    # Mapas comuns
    rename_back = {}
    for c in df2.columns:
        if c in ("NOME", "NAME"): rename_back[c] = "NOME"
        if c in ("LATITUDE", "LAT", "Y"): rename_back[c] = "LATITUDE"
        if c in ("LONGITUDE", "LON", "LONG", "X"): rename_back[c] = "LONGITUDE"
    df2.rename(columns=rename_back, inplace=True)
    missing = [c for c in ExpectedCols if c not in df2.columns]
    if missing:
        raise ValueError(f"Colunas ausentes: {missing}. Esperado: {ExpectedCols}")
    return df2[ExpectedCols]

def parse_csv_xlsx(file_bytes: bytes, suffix: str) -> pd.DataFrame:
    if suffix == ".csv":
        df = pd.read_csv(pd.io.common.BytesIO(file_bytes))
    else:
        df = pd.read_excel(pd.io.common.BytesIO(file_bytes))
    return _normalize_columns(df)

def parse_kml_bytes(kml_bytes: bytes) -> pd.DataFrame:
    from shapely.geometry import Point
    k = kml.KML()
    k.from_string(kml_bytes)
    placemarks = []
    def _walk(feats):
        for f in feats:
            if hasattr(f, 'features') and f.features:
                yield from _walk(f.features())
            else:
                yield f
    for f in _walk(k.features()):
        try:
            if hasattr(f, 'geometry') and isinstance(f.geometry, Point):
                lon, lat = f.geometry.coords[0]
                name = getattr(f, 'name', None) or "Sem Nome"
                placemarks.append({"NOME": name, "LATITUDE": lat, "LONGITUDE": lon})
        except Exception:
            continue
    if not placemarks:
        raise ValueError("Nenhum Point encontrado no KML.")
    return _normalize_columns(pd.DataFrame(placemarks))

def parse_kmz(file_bytes: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(pd.io.common.BytesIO(file_bytes)) as z:
        # Procura o primeiro .kml
        kml_name = next((n for n in z.namelist() if n.lower().endswith('.kml')), None)
        if not kml_name:
            raise ValueError("KMZ inválido: não contém KML.")
        with z.open(kml_name) as f:
            kml_bytes = f.read()
    return parse_kml_bytes(kml_bytes)
