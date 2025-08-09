import simplekml
from typing import List, Tuple, Optional

# Mantém a função antiga (compatibilidade)
def geojson_line_to_kmz(coords_lonlat: List[Tuple[float, float]], output_path: str, name: str = "Rota", 
                         description: Optional[str] = None) -> str:
    kml = simplekml.Kml()
    ls = kml.newlinestring(name=name, description=description)
    # coords_lonlat já está como [(lon,lat), ...]
    ls.coords = [(lon, lat) for lon, lat in coords_lonlat]
    ls.extrude = 0
    ls.tessellate = 1
    ls.altitudemode = simplekml.AltitudeMode.clamptoground
    kml.savekmz(output_path)
    return output_path

# Nova função com marcadores de origem/destino
def geojson_line_with_markers_to_kmz(
    coords_lonlat: List[Tuple[float, float]],
    start_latlon: Tuple[float, float],
    end_latlon: Tuple[float, float],
    output_path: str,
    route_name: str = "Rota",
    start_name: str = "Origem",
    end_name: str = "Destino",
    description: Optional[str] = None,
) -> str:
    """
    Gera um KMZ contendo:
      - a rota (LineString) a partir de coords [lon, lat]
      - um marcador para a origem (start_latlon = [lat, lon])
      - um marcador para o destino (end_latlon = [lat, lon])
    """
    kml = simplekml.Kml()

    # Linha da rota
    ls = kml.newlinestring(name=route_name, description=description)
    ls.coords = [(lon, lat) for lon, lat in coords_lonlat]
    ls.tessellate = 1
    ls.altitudemode = simplekml.AltitudeMode.clamptoground

    # Marcador de origem
    s_lat, s_lon = start_latlon
    p_start = kml.newpoint(name=start_name, coords=[(s_lon, s_lat)])

    # Marcador de destino
    e_lat, e_lon = end_latlon
    p_end = kml.newpoint(name=end_name, coords=[(e_lon, e_lat)])

    # (Opcional) estilos de ícones/cores podem ser definidos aqui

    kml.savekmz(output_path)
    return output_path
