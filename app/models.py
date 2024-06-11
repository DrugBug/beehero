import uuid
from sqlalchemy.orm import backref
from app import db


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Uuid(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.name


class Forecast(db.Model):
    __tablename__ = "forecasts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    feels_like = db.Column(db.Float, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    location_id = db.Column(db.Uuid(as_uuid=True), db.ForeignKey('locations.id'))
    location = db.relationship("Location", backref=backref("forecasts", order_by='Forecast.date_time.desc()'))

    def __str__(self):
        return f"{self.location} - {self.date_time}"
