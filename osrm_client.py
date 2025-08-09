import requests
from typing import List, Tuple, Literal

OSRMProfile = Literal["driving", "cycling", "foot"]

class OSRMClient:
    def __init__(self, base_url: str = "https://router.project-osrm.org", profile: OSRMProfile = "driving"):
        self.base_url = base_url.rstrip("/")
        self.profile = profile

    def set_profile(self, profile: OSRMProfile):
        self.profile = profile

    def route_multi(self, coords_latlon: List[Tuple[float, float]], overview: str = "full") -> dict:
        """Rota por TODOS os pontos, na ordem fornecida (waypoints)."""
        if len(coords_latlon) < 2:
            raise ValueError("Forneça pelo menos 2 coordenadas.")
        coord_str = ";".join([f"{lon},{lat}" for (lat, lon) in coords_latlon])
        url = (
            f"{self.base_url}/route/v1/{self.profile}/" +
            coord_str +
            f"?overview={overview}&geometries=geojson&annotations=distance,duration"
        )
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()
        if data.get("code") != "Ok" or not data.get("routes"):
            raise RuntimeError(f"OSRM error: {data}")
        return data["routes"][0]