import simplekml
from typing import List, Tuple, Optional

def geojson_line_to_kmz(coords_lonlat: List[Tuple[float, float]], output_path: str, name: str = "Rota", 
                         description: Optional[str] = None) -> str:
    kml = simplekml.Kml()
    ls = kml.newlinestring(name=name, description=description)
    latlon = [(lat, lon) for lon, lat in coords_lonlat]
    ls.coords = [(lon, lat) for lat, lon in latlon]
    ls.extrude = 0
    ls.tessellate = 1
    ls.altitudemode = simplekml.AltitudeMode.clamptoground
    kml.savekmz(output_path)
    return output_path