import simplekml

def geojson_line_with_markers_to_kmz(coords_lonlat, start_latlon, end_latlon, output_path,
                                     route_name="Rota", start_name="Início", end_name="Fim", description=""):
    """
    Cria um arquivo KMZ contendo:
      - Linha da rota (verde, espessura 4.0)
      - Marcador de início
      - Marcador de fim
    """
    kml = simplekml.Kml()

    # Linha da rota
    ls = kml.newlinestring(name=route_name, description=description)
    ls.coords = [(lon, lat) for lon, lat in coords_lonlat]
    ls.style.linestyle.color = simplekml.Color.rgb(0, 255, 0)  # Verde
    ls.style.linestyle.width = 4.0

    # Marcador de início
    p_start = kml.newpoint(name=start_name, coords=[(start_latlon[1], start_latlon[0])])
    p_start.style.iconstyle.color = simplekml.Color.yellow

    # Marcador de fim
    p_end = kml.newpoint(name=end_name, coords=[(end_latlon[1], end_latlon[0])])
    p_end.style.iconstyle.color = simplekml.Color.yellow

    # Salvar KMZ
    kml.savekmz(output_path)
