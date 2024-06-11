import inspect
from collections import defaultdict
from http import HTTPStatus
from app.openweathermap_utils import NUM_OF_FORECASTS_PER_DAY
from flask import request
from app.db_utils import *
from app import create_app

app = create_app()
ENDPOINTS_CACHE = {}


@app.route('/average-temp', methods=['GET'])
def average_temperature():
    """
    Return the average temperature of each day for every location in the following format:
    {
        "location_1": [
            {
                "avg_temp": float,
                "day": "YYYY-mm-dd"
            },
            {
                "avg_temp": float,
                "day": "YYYY-mm-dd"
            },
            . . .
        ],
        "location_2": [. . .]
    }
    """
    global ENDPOINTS_CACHE
    f_name = inspect.stack()[0][3]

    if f_name in ENDPOINTS_CACHE:
        logger.info(f"Endpoint {f_name} response is cached, getting from cache")
        return ENDPOINTS_CACHE[f_name], HTTPStatus.OK

    logger.info(f"Endpoint {f_name} response is not cached, preforming logic")
    response = {}
    for location in get_locations():
        response[location.name] = []

        group_by_date = defaultdict(int)    # TODO: should be on DB level
        for forecast in location.forecasts:
            group_by_date[forecast.date_time.strftime('%Y-%m-%d')] += forecast.temperature

        for day, sum_temps_per_day in group_by_date.items():
            response[location.name].append(
                {
                    "day": day,
                    "avg_temp": round(sum_temps_per_day / NUM_OF_FORECASTS_PER_DAY, 1)
                }
            )

    ENDPOINTS_CACHE[f_name] = response

    return response, HTTPStatus.OK


@app.route('/global-lowest-humidity', methods=['GET'])
def global_lowest_humidity_point():
    """ Return the location and time of the forecast with the lowest humidity recorded """
    global ENDPOINTS_CACHE
    f_name = inspect.stack()[0][3]

    if f_name in ENDPOINTS_CACHE:
        logger.info(f"Endpoint {f_name} response is cached, getting from cache")
        return ENDPOINTS_CACHE[f_name], HTTPStatus.OK

    logger.info(f"Endpoint {f_name} response is not cached, preforming logic")
    forecast = get_minimum_humidity_forecast()
    response = {
        "location": str(forecast.location),
        "time": str(forecast.date_time)
    }

    ENDPOINTS_CACHE[f_name] = response

    return response, HTTPStatus.OK


@app.route('/how-it-feels-like', methods=['GET'])
def feels_like_location_ranking():
    """ Return ordered locations with their latest 'feels_like' temperature """
    global ENDPOINTS_CACHE
    f_name = inspect.stack()[0][3]

    if f_name in ENDPOINTS_CACHE:
        logger.info(f"Endpoint {f_name} calculation is cached, getting from cache")
        data = ENDPOINTS_CACHE[f_name]
    else:
        logger.info(f"Endpoint {f_name} calculation is not cached, preforming logic")
        # location.forecasts[0] usage: Model 'Forecast.location' backref has order_by='Forecast.date_time.desc()'
        data = {location.name: location.forecasts[0].feels_like for location in get_locations()}
        ENDPOINTS_CACHE[f_name] = data

    order = request.args.get('order')
    if order not in ('asc', 'desc'):
        order = 'asc'

    # TODO: should be on DB level (using 'Rank')
    response = [{k[0]: k[1]} for k in sorted(data.items(), key=lambda item: item[1], reverse=order == 'desc')]

    return response, HTTPStatus.OK
