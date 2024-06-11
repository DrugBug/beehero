from app.api import app
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CITIES = ["Jerusalem", "Haifa", "Tel Aviv", "Eilat", "Tiberias"]


def init_db_data():
    from app.db_utils import persist_location, persist_location_forecasts
    from app.openweathermap_utils import get_location_coordinates, get_location_forecasts

    for city in CITIES:
        try:
            location = persist_location(city)
            coordinates = get_location_coordinates(location.name)
            forecasts = get_location_forecasts(latitude=coordinates["latitude"], longitude=coordinates["longitude"])
            persist_location_forecasts(location, forecasts)

        except Exception as e:
            logger.error(f"Failed to initiate data: {e}")
            raise


if __name__ == '__main__':
    init_db_data()
    app.run(debug=True, host="0.0.0.0", port=5000)

