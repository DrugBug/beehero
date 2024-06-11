import logging
from datetime import datetime
from typing import Dict, List
from sqlalchemy import asc
from app import db
from app.models import Forecast, Location

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def persist_location_forecasts(location: Location, forecasts: List[Dict]):
    """ Add new location forecasts to the database """
    logger.info("Persisting Forecast objects")
    db.session.add_all(
            [Forecast(
                temperature=forecast["temp"],
                humidity=forecast["humidity"],
                feels_like=forecast["feels_like"],
                date_time=datetime.fromtimestamp(forecast["dt"]),
                location=location
            ) for forecast in forecasts]
        )

    try:
        db.session.commit()
        logger.info("Forecasts committed")

    except Exception as e:
        logger.error(f"Failed to persist {len(forecasts)} Forecasts for location {location}: {e}")
        db.session.rollback()
        raise


def persist_location(location_name: str) -> Location:
    """ Add new Location to the database """
    logger.info(f"Persist location {location_name}")
    location = Location(name=location_name)
    db.session.add(location)
    try:
        db.session.commit()
        logger.info("Location committed")

    except Exception as e:
        logger.error(f"Failed to persist location {location_name}: {e}")
        db.session.rollback()
        raise

    return location


def get_locations() -> List[Location]:
    """ Fetch all locations from the database """
    locations = Location.query.all()
    return locations


def get_minimum_humidity_forecast() -> Forecast:
    """ Get the forecast with the lowest humidity """
    min_humid_forcast = db.session.query(Forecast).order_by(asc(Forecast.humidity)).limit(1)
    return min_humid_forcast.first()
