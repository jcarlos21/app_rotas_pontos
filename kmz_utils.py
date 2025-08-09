from fastkml import kml
from shapely.geometry import LineString, Point
import zipfile
import os

def geojson_line_with_markers_to_kmz(coords, origem_latlon, destino_latlon, kmz_path, route_name="Rota", start_name="Origem", end_name="Destino", description=""):
    # coords vem como [[lon, lat], ...] do OSRM
    line = LineString([(lon, lat) for lon, lat in coords])
    start_point = Point(origem_latlon[1], origem_latlon[0])
    end_point = Point(destino_latlon[1], destino_latlon[0])

    ns = "{http://www.opengis.net/kml/2.2}"
    k = kml.KML()
    d = kml.Document(ns, 'docid', route_name, description)
    f = kml.Folder(ns, 'fid', route_name)

    # Estilo da linha (verde e espessura 4.0)
    style_id = "routeStyle"
    style = kml.Style(
        ns,
        style_id,
        LineStyle=kml.LineStyle(ns, color="ff00ff00", width=4.0)  # ff00ff00 = verde
    )
    d.append_style(style)

    # Placemark da rota
    placemark_route = kml.Placemark(ns, 'route', route_name, description)
    placemark_route.append_styleUrl(f"#{style_id}")
    placemark_route.geometry = line
    f.append(placemark_route)

    # Placemark origem
    placemark_start = kml.Placemark(ns, 'start', start_name)
    placemark_start.geometry = start_point
    f.append(placemark_start)

    # Placemark destino
    placemark_end = kml.Placemark(ns, 'end', end_name)
    placemark_end.geometry = end_point
    f.append(placemark_end)

    d.append(f)
    k.append(d)

    # Salvar como KML temporário
    kml_temp_path = kmz_path.replace(".kmz", ".kml")
    with open(kml_temp_path, 'w', encoding='utf-8') as f_out:
        f_out.write(k.to_string(prettyprint=True))

    # Compactar em KMZ
    with zipfile.ZipFile(kmz_path, 'w', compression=zipfile.ZIP_DEFLATED) as kmz:
        kmz.write(kml_temp_path, arcname=os.path.basename(kml_temp_path))

    os.remove(kml_temp_path)
