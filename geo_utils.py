from geopy.distance import geodesic
from typing import Tuple

def haversine_m(latlon_a: Tuple[float, float], latlon_b: Tuple[float, float]) -> float:
    return geodesic(latlon_a, latlon_b).meters
