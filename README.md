### INSTALLATION INSTRUCTIONS ###
This assignment was built using Python 3.10 (Flask, SQLAlchemy + Postgres).
1. Clone this repository.
2. Enter the main directory (where the `docker-compose.yml` is found) and run `docker-compose up` to build and run the services.
4. You can now access the API by browsing/CURLing the following urls:
- http://localhost:5000/average-temp
- http://localhost:5000/global-lowest-humidity
- http://localhost:5000/how-it-feels-like?order={asc|desc}

