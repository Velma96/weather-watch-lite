from extensions import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from datetime import datetime

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-saved_locations.user', '-search_records.user')
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)  # Stores hashed password
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    saved_locations = relationship('SavedLocation', back_populates='user', cascade="all, delete-orphan")
    search_records = relationship('SearchRecord', back_populates='user', cascade="all, delete-orphan")

    def to_dict(self):
        data = super().to_dict()
        if 'created_at' in data:
            data['created_at'] = data['created_at'].isoformat() if data['created_at'] else None
        if 'updated_at' in data:
            data['updated_at'] = data['updated_at'].isoformat() if data['updated_at'] else None
        return data

# Association table
search_records_locations = db.Table(
    'search_records_locations',
    db.Column('search_record_id', db.Integer, db.ForeignKey('search_records.id'), primary_key=True),
    db.Column('saved_location_id', db.Integer, db.ForeignKey('saved_locations.id'), primary_key=True)
)

class SavedLocation(db.Model, SerializerMixin):
    __tablename__ = 'saved_locations'
    serialize_rules = ('-user.saved_locations', '-search_records.saved_locations', '-weather_data.location')
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='saved_locations')
    search_records = relationship('SearchRecord', secondary=search_records_locations, back_populates='saved_locations')
    weather_data = relationship('WeatherData', back_populates='location', cascade="all, delete-orphan")

    def to_dict(self):
        data = super().to_dict()
        if 'created_at' in data:
            data['created_at'] = data['created_at'].isoformat() if data['created_at'] else None
        if 'updated_at' in data:
            data['updated_at'] = data['updated_at'].isoformat() if data['updated_at'] else None
        return data

class SearchRecord(db.Model, SerializerMixin):
    __tablename__ = 'search_records'
    serialize_rules = ('-user.search_records', '-saved_locations.search_records')
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    search_term = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='search_records')
    saved_locations = relationship('SavedLocation', secondary=search_records_locations, back_populates='search_records')

    def to_dict(self):
        data = super().to_dict()
        if 'created_at' in data:
            data['created_at'] = data['created_at'].isoformat() if data['created_at'] else None
        return data

class WeatherData(db.Model, SerializerMixin):
    __tablename__ = 'weather_data'
    serialize_rules = ('-location.weather_data',)
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('saved_locations.id'), nullable=False)
    current_temperature = db.Column(db.Float, nullable=False)
    current_humidity = db.Column(db.Float, nullable=False)
    current_wind_speed = db.Column(db.Float, nullable=False)
    weather_condition = db.Column(db.String(50), nullable=False)
    forecast_data = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    location = relationship('SavedLocation', back_populates='weather_data')

    def to_dict(self):
        data = super().to_dict()
        if 'created_at' in data:
            data['created_at'] = data['created_at'].isoformat() if data['created_at'] else None
        if 'updated_at' in data:
            data['updated_at'] = data['updated_at'].isoformat() if data['updated_at'] else None
        return data