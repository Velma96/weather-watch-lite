from extensions import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from datetime import datetime

##User model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    saved_locations = relationship('SavedLocation', back_populates='user', cascade="all, delete-orphan")
    search_records = relationship('SearchRecord', back_populates='user', cascade="all, delete-orphan")

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3 or len(username) > 25:
            raise ValueError("Username must be between 3 and 25 characters long.")
        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError("Email must be of a valid format.")
        return email           

    @validates('password_hash')
    def validate_password(self, key, password_hash):
        if len(password_hash) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        return password_hash   

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }     

##Association table for many-to-many relationship between SavedLocation and SearchRecord
search_records_locations = db.Table(
    'search_records_locations',
    db.Column('search_record_id', db.Integer, db.ForeignKey('search_records.id'), primary_key=True),
    db.Column('saved_location_id', db.Integer, db.ForeignKey('saved_locations.id'), primary_key=True)
)        

##Saved location model
class SavedLocation(db.Model, SerializerMixin):
    __tablename__ = 'saved_locations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='saved_locations')
    search_records = relationship('SearchRecord', secondary=search_records_locations, back_populates='saved_locations')
    weather_data = relationship('WeatherData', back_populates='location', cascade="all, delete-orphan")

    @validates('location_name')
    def validate_location_name(self, key, location_name):
        if len(location_name) < 3 or len(location_name) > 80:
            raise ValueError("Location name must be between 3 and 80 characters long.")
        return location_name        

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "location_name": self.location_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }    

##Search record model
class SearchRecord(db.Model, SerializerMixin):
    __tablename__ = 'search_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='search_records')
    saved_locations = relationship('SavedLocation', secondary=search_records_locations, back_populates='search_records')

    @validates('query')
    def validate_query(self, key, query):
        if len(query) < 3 or len(query) > 80:
            raise ValueError("Query must be between 3 and 80 characters long.")
        return query

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "query": self.query,
            "created_at": self.created_at
        }

##Weather data model
class WeatherData(db.Model, SerializerMixin):
    __tablename__ = 'weather_data'

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('saved_locations.id'), nullable=False)
    current_temperature = db.Column(db.Float, nullable=False)
    current_humidity = db.Column(db.Float, nullable=False)
    current_wind_speed = db.Column(db.Float, nullable=False)
    weather_condition = db.Column(db.String(50), nullable=False)
    forecast_data = db.Column(db.JSON, nullable=False)  # Store the 7-day forecast data in JSON format
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with SavedLocation to get the location details
    location = relationship('SavedLocation', back_populates='weather_data')

    @validates('current_temperature')
    def validate_temperature(self, key, current_temperature):
        if current_temperature < -100 or current_temperature > 100:
            raise ValueError('Temperature should be between -100°C and 100°C.')
        return current_temperature

    @validates('current_humidity')
    def validate_humidity(self, key, current_humidity):
        if current_humidity < 0 or current_humidity > 100:
            raise ValueError('Humidity should be between 0 and 100%.')
        return current_humidity

    @validates('current_wind_speed')
    def validate_wind_speed(self, key, current_wind_speed):
        if current_wind_speed < 0 or current_wind_speed > 500:
            raise ValueError('Wind speed should be between 0 and 500 km/h.')
        return current_wind_speed

    @validates('weather_condition')
    def validate_weather_condition(self, key, weather_condition):
        valid_conditions = ['sunny', 'rainy', 'cloudy', 'stormy', 'snowy', 'foggy']
        if weather_condition not in valid_conditions:
            raise ValueError('Invalid weather condition.')
        return weather_condition

    def to_dict(self):
        return {
            "id": self.id,
            "location_id": self.location_id,
            "current_temperature": self.current_temperature,
            "current_humidity": self.current_humidity,
            "current_wind_speed": self.current_wind_speed,
            "weather_condition": self.weather_condition,
            "forecast_data": self.forecast_data,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }