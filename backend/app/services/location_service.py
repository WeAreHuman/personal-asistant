from typing import Optional

from geopy.distance import geodesic
from geopy.geocoders import Nominatim

COMMON_LOCATIONS = {
    "food_bank": "Second Harvest Food Bank",
    "campus": "University Campus",
    "dining_hall": "Campus Dining Hall",
    "bus_stop": "Main Street Bus Stop",
}

_geolocator = Nominatim(user_agent="personal-assistant-ai")


def calculate_distance(origin: str, destination: str) -> float:
    """Calculate distance in miles between two locations using geocoding."""
    try:
        origin_loc = _geolocator.geocode(origin)
        dest_loc = _geolocator.geocode(destination)
        if not origin_loc or not dest_loc:
            return 0.0
        origin_coords = (origin_loc.latitude, origin_loc.longitude)
        dest_coords = (dest_loc.latitude, dest_loc.longitude)
        return geodesic(origin_coords, dest_coords).miles
    except Exception:
        return 0.0


def get_travel_time_estimate(distance_miles: float, mode: str = "walking") -> int:
    """Estimate travel time in minutes."""
    speeds = {
        "walking": 3.0,
        "cycling": 12.0,
        "driving": 30.0,
        "transit": 15.0,
    }
    speed = speeds.get(mode, 3.0)
    if distance_miles <= 0:
        return 0
    return max(1, int((distance_miles / speed) * 60))


def resolve_location(name: str) -> Optional[str]:
    """Resolve a common location alias to its full name."""
    return COMMON_LOCATIONS.get(name.lower(), name)
