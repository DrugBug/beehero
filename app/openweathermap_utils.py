import os
import requests
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

API_KEY = os.environ['OPENWEATHERMAP_API_KEY']
NUM_OF_FORECASTS_PER_DAY = 8


def get_location_coordinates(location: str, limit: int = 1) -> Dict[str, Any]:
    """ Return coordinates for a location using 'openweathermap' geocoding API """
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit={limit}&appid={API_KEY}"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    assert 0 < len(data) <= limit, f"No result found for location: '{location}'"

    return {
        "name": data[0]["name"],
        "latitude": data[0]["lat"],
        "longitude": data[0]["lon"]
    }


def get_location_forecasts(latitude: float, longitude: float) -> List[Dict]:
    """ Return '5 day / 3-hour forecast' for a location using 'openweathermap' data API """
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()

    response = []
    for forecast in data.get("list", []):
        response.append({
            "dt": forecast["dt"],
            "temp": forecast["main"]["temp"],
            "humidity": forecast["main"]["humidity"],
            "feels_like": forecast["main"]["feels_like"]
        })

    return response
