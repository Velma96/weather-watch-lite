from flask_restful import Resource
from flask import request
from models import User, SavedLocation, SearchRecord, WeatherData
from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash
import random

weather_conditions = ['Sunny', 'Rainy', 'Cloudy', 'Stormy', 'Snowy', 'Foggy']

def generate_mock_forecast():
    """Generate a 7-day mock forecast."""
    return [
        {
            "day": i + 1,
            "temperature": round(random.uniform(-10, 35), 1),
            "humidity": random.randint(20, 100),
            "condition": random.choice(weather_conditions)
        } for i in range(7)
    ]

class UserResource(Resource):
    def get(self, id=None):
        try:
            if id:
                user = User.query.get(id)
                if not user:
                    return {"error": "User not found"}, 404
                return {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "updated_at": user.updated_at.isoformat() if user.updated_at else None
                }, 200
            users = User.query.all()
            return [{
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            } for user in users], 200
        except Exception as e:
            return {"error": f"Server error: {str(e)}"}, 500

    def post(self):
        try:
            data = request.get_json()
            if not all(key in data for key in ['username', 'email', 'password']):
                return {"error": "Missing required fields (username, email, password)"}, 400
            if User.query.filter_by(username=data['username']).first():
                return {"error": "Username already exists"}, 409
            if User.query.filter_by(email=data['email']).first():
                return {"error": "Email already exists"}, 409
            user = User(
                username=data['username'],
                email=data['email'],
                password_hash=generate_password_hash(data['password'])
            )
            db.session.add(user)
            db.session.commit()
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "message": "User created successfully"
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to create user: {str(e)}"}, 400

class SavedLocationResource(Resource):
    def get(self, id=None):
        try:
            if id:
                location = SavedLocation.query.get(id)
                if not location:
                    return {"error": "Saved location not found"}, 404
                return {
                    "id": location.id,
                    "user_id": location.user_id,
                    "location_name": location.location_name,
                    "created_at": location.created_at.isoformat() if location.created_at else None,
                    "updated_at": location.updated_at.isoformat() if location.updated_at else None,
                    "weather_data": [{
                        "id": wd.id,
                        "current_temperature": wd.current_temperature,
                        "weather_condition": wd.weather_condition
                    } for wd in location.weather_data]
                }, 200
            locations = SavedLocation.query.all()
            return [{
                "id": loc.id,
                "user_id": loc.user_id,
                "location_name": loc.location_name,
                "created_at": loc.created_at.isoformat() if loc.created_at else None
            } for loc in locations], 200
        except Exception as e:
            return {"error": f"Server error: {str(e)}"}, 500

    def post(self):
        try:
            data = request.get_json()
            if not all(key in data for key in ['location_name']):
                return {"error": "Missing required field (location_name)"}, 400
            location = SavedLocation(user_id=1, location_name=data['location_name'])
            db.session.add(location)
            db.session.commit()

            # Generate and save mock weather data
            weather = WeatherData(
                location_id=location.id,
                current_temperature=round(random.uniform(-10, 35), 1),
                current_humidity=random.randint(20, 100),
                current_wind_speed=round(random.uniform(0, 60), 1),
                weather_condition=random.choice(weather_conditions),
                forecast_data=generate_mock_forecast()
            )
            db.session.add(weather)
            db.session.commit()

            return {
                "id": location.id,
                "user_id": location.user_id,
                "location_name": location.location_name,
                "message": "Location and weather data saved successfully"
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to save location: {str(e)}"}, 400

    def delete(self, id):
        try:
            location = SavedLocation.query.get(id)
            if not location:
                return {"error": "Saved location not found"}, 404
            
            # Delete associated weather data
            WeatherData.query.filter_by(location_id=id).delete()
            
            # Delete the location
            db.session.delete(location)
            db.session.commit()
            
            return {
                "id": id,
                "message": "Location deleted successfully"
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to delete location: {str(e)}"}, 400
class SearchRecordResource(Resource):
    def get(self, id=None):
        try:
            if id:
                record = SearchRecord.query.get(id)
                if not record:
                    return {"error": "Search record not found"}, 404
                return {
                    "id": record.id,
                    "user_id": record.user_id,
                    "query": record.query,
                    "created_at": record.created_at.isoformat(),
                    "saved_locations": [{"id": loc.id, "location_name": loc.location_name} for loc in record.saved_locations]
                }, 200
            records = SearchRecord.query.all()
            return [{
                "id": rec.id,
                "user_id": rec.user_id,
                "query": rec.query,
                "created_at": rec.created_at.isoformat(),
                "location_count": len(rec.saved_locations)
            } for rec in records], 200
        except Exception as e:
            return {"error": f"Server error: {str(e)}"}, 500

    def post(self):
        try:
            data = request.get_json()
            if not all(key in data for key in ['query']):
                return {"error": "Missing required field (query)"}, 400
            record = SearchRecord(user_id=1, query=data['query'])
            db.session.add(record)
            db.session.commit()
            return {
                "id": record.id,
                "user_id": record.user_id,
                "query": record.query,
                "location_count": len(record.saved_locations),
                "message": "Search record created successfully"
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to create search record: {str(e)}"}, 400

class WeatherDataResource(Resource):
    def get(self, id=None):
        try:
            if id:
                weather = WeatherData.query.get(id)
                if not weather:
                    return {"error": "Weather data not found"}, 404
                return {
                    "id": weather.id,
                    "location_id": weather.location_id,
                    "location_name": weather.location.location_name,
                    "current_temperature": weather.current_temperature,
                    "current_humidity": weather.current_humidity,
                    "current_wind_speed": weather.current_wind_speed,
                    "weather_condition": weather.weather_condition,
                    "forecast_data": weather.forecast_data,
                    "created_at": weather.created_at.isoformat(),
                    "updated_at": weather.updated_at.isoformat() if weather.updated_at else None
                }, 200
            
            location_name = request.args.get('location')
            if location_name:
                location = SavedLocation.query.filter_by(location_name=location_name).first()
                if not location:
                    location = SavedLocation(user_id=1, location_name=location_name)
                    db.session.add(location)
                    db.session.commit()
                    weather = WeatherData(
                        location_id=location.id,
                        current_temperature=round(random.uniform(-10, 35), 1),
                        current_humidity=random.randint(20, 100),
                        current_wind_speed=round(random.uniform(0, 60), 1),
                        weather_condition=random.choice(weather_conditions),
                        forecast_data=generate_mock_forecast()
                    )
                    db.session.add(weather)
                    db.session.commit()
                else:
                    weather = WeatherData.query.filter_by(location_id=location.id).first()
                    if not weather:
                        weather = WeatherData(
                            location_id=location.id,
                            current_temperature=round(random.uniform(-10, 35), 1),
                            current_humidity=random.randint(20, 100),
                            current_wind_speed=round(random.uniform(0, 60), 1),
                            weather_condition=random.choice(weather_conditions),
                            forecast_data=generate_mock_forecast()
                        )
                        db.session.add(weather)
                        db.session.commit()
                return {
                    "id": weather.id,
                    "location_id": weather.location_id,
                    "location_name": weather.location.location_name,
                    "current_temperature": weather.current_temperature,
                    "current_humidity": weather.current_humidity,
                    "current_wind_speed": weather.current_wind_speed,
                    "weather_condition": weather.weather_condition,
                    "forecast_data": weather.forecast_data,
                    "created_at": weather.created_at.isoformat(),
                    "updated_at": weather.updated_at.isoformat() if weather.updated_at else None
                }, 200
            
            weather_data = WeatherData.query.all()
            return [{
                "id": wd.id,
                "location_id": wd.location_id,
                "location_name": wd.location.location_name,
                "current_temperature": wd.current_temperature,
                "weather_condition": wd.weather_condition,
                "created_at": wd.created_at.isoformat()
            } for wd in weather_data], 200
        except Exception as e:
            return {"error": f"Server error: {str(e)}"}, 500

    def post(self):
        try:
            data = request.get_json()
            required_fields = ['location_id', 'current_temperature', 'current_humidity', 'current_wind_speed', 'weather_condition']
            if not all(key in data for key in required_fields):
                return {"error": f"Missing required fields: {required_fields}"}, 400
            location = SavedLocation.query.get(data['location_id'])
            if not location:
                return {"error": "Location not found"}, 404
            weather = WeatherData(
                location_id=data['location_id'],
                current_temperature=data['current_temperature'],
                current_humidity=data['current_humidity'],
                current_wind_speed=data['current_wind_speed'],
                weather_condition=data['weather_condition'],
                forecast_data=data.get('forecast_data', [])
            )
            db.session.add(weather)
            db.session.commit()
            return {
                "id": weather.id,
                "location_id": weather.location_id,
                "message": "Weather data created successfully"
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to create weather data: {str(e)}"}, 400