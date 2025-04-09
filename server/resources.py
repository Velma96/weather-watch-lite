from flask_restful import Resource
from flask import request
from models import User, SavedLocation, SearchRecord, WeatherData
from extensions import db
from datetime import datetime

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
            
            # Validate required fields
            if not all(key in data for key in ['username', 'email', 'password']):
                return {"error": "Missing required fields (username, email, password)"}, 400
            
            # Check if username or email already exists
            if User.query.filter_by(username=data['username']).first():
                return {"error": "Username already exists"}, 409
            if User.query.filter_by(email=data['email']).first():
                return {"error": "Email already exists"}, 409
            
            user = User(
                username=data['username'],
                email=data['email'],
                password_hash=data['password']  # In production, hash this properly
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

    def put(self, id):
        try:
            user = User.query.get(id)
            if not user:
                return {"error": "User not found"}, 404
                
            data = request.get_json()
            
            # Validate at least one field to update
            if not any(key in data for key in ['username', 'email', 'password']):
                return {"error": "No valid fields provided for update"}, 400
            
            # Check for duplicate username
            if 'username' in data and data['username'] != user.username:
                if User.query.filter_by(username=data['username']).first():
                    return {"error": "Username already exists"}, 409
                user.username = data['username']
            
            # Check for duplicate email
            if 'email' in data and data['email'] != user.email:
                if User.query.filter_by(email=data['email']).first():
                    return {"error": "Email already exists"}, 409
                user.email = data['email']
            
            if 'password' in data:
                user.password_hash = data['password']  # Hash this in production
                
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "message": "User updated successfully"
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to update user: {str(e)}"}, 400

    def delete(self, id):
        try:
            user = User.query.get(id)
            if not user:
                return {"error": "User not found"}, 404
                
            db.session.delete(user)
            db.session.commit()
            
            return {"message": "User deleted successfully"}, 200
            
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to delete user: {str(e)}"}, 400


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
            
            # Get all saved locations with basic info
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
            
            # Validate required fields
            if not all(key in data for key in ['user_id', 'location_name']):
                return {"error": "Missing required fields (user_id, location_name)"}, 400
            
            # Verify user exists
            if not User.query.get(data['user_id']):
                return {"error": "User not found"}, 404
            
            # Check for duplicate location for this user
            if SavedLocation.query.filter_by(
                user_id=data['user_id'],
                location_name=data['location_name']
            ).first():
                return {"error": "Location already saved for this user"}, 409
            
            location = SavedLocation(
                user_id=data['user_id'],
                location_name=data['location_name']
            )
            
            db.session.add(location)
            db.session.commit()
            
            return {
                "id": location.id,
                "user_id": location.user_id,
                "location_name": location.location_name,
                "message": "Location saved successfully"
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to save location: {str(e)}"}, 400

    def put(self, id):
        try:
            location = SavedLocation.query.get(id)
            if not location:
                return {"error": "Saved location not found"}, 404
                
            data = request.get_json()
            
            # Validate at least one field to update
            if 'location_name' not in data:
                return {"error": "No valid fields provided for update"}, 400
            
            # Check for duplicate location name for this user
            if 'location_name' in data and data['location_name'] != location.location_name:
                if SavedLocation.query.filter_by(
                    user_id=location.user_id,
                    location_name=data['location_name']
                ).first():
                    return {"error": "Location name already exists for this user"}, 409
                
                location.location_name = data['location_name']
            
            location.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {
                "id": location.id,
                "user_id": location.user_id,
                "location_name": location.location_name,
                "message": "Location updated successfully"
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to update location: {str(e)}"}, 400

    def delete(self, id):
        try:
            location = SavedLocation.query.get(id)
            if not location:
                return {"error": "Saved location not found"}, 404
                
            # Delete associated weather data first
            WeatherData.query.filter_by(location_id=id).delete()
            
            db.session.delete(location)
            db.session.commit()
            
            return {"message": "Location and associated weather data deleted successfully"}, 200
            
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
                    "saved_locations": [{
                        "id": loc.id,
                        "location_name": loc.location_name
                    } for loc in record.saved_locations]
                }, 200
            
            # Get all search records with basic info
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
            
            # Validate required fields
            if not all(key in data for key in ['user_id', 'query']):
                return {"error": "Missing required fields (user_id, query)"}, 400
            
            # Verify user exists
            if not User.query.get(data['user_id']):
                return {"error": "User not found"}, 404
            
            # Check for location_ids if provided
            location_ids = data.get('location_ids', [])
            valid_locations = []
            if location_ids:
                valid_locations = SavedLocation.query.filter(
                    SavedLocation.id.in_(location_ids),
                    SavedLocation.user_id == data['user_id']
                ).all()
                if len(valid_locations) != len(location_ids):
                    return {"error": "One or more locations not found or don't belong to user"}, 404
            
            record = SearchRecord(
                user_id=data['user_id'],
                query=data['query']
            )
            
            db.session.add(record)
            db.session.commit()
            
            # Associate locations if provided
            if valid_locations:
                for location in valid_locations:
                    record.saved_locations.append(location)
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

    def put(self, id):
        try:
            record = SearchRecord.query.get(id)
            if not record:
                return {"error": "Search record not found"}, 404
                
            data = request.get_json()
            
            # Validate at least one field to update
            if not any(key in data for key in ['query', 'location_ids']):
                return {"error": "No valid fields provided for update"}, 400
            
            if 'query' in data:
                record.query = data['query']
            
            if 'location_ids' in data:
                # Clear existing associations
                record.saved_locations = []
                
                # Add new associations
                location_ids = data['location_ids']
                valid_locations = SavedLocation.query.filter(
                    SavedLocation.id.in_(location_ids),
                    SavedLocation.user_id == record.user_id
                ).all()
                
                if len(valid_locations) != len(location_ids):
                    db.session.rollback()
                    return {"error": "One or more locations not found or don't belong to user"}, 404
                
                for location in valid_locations:
                    record.saved_locations.append(location)
            
            db.session.commit()
            
            return {
                "id": record.id,
                "user_id": record.user_id,
                "query": record.query,
                "location_count": len(record.saved_locations),
                "message": "Search record updated successfully"
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to update search record: {str(e)}"}, 400

    def delete(self, id):
        try:
            record = SearchRecord.query.get(id)
            if not record:
                return {"error": "Search record not found"}, 404
                
            # The association table records will be deleted automatically due to cascade
            db.session.delete(record)
            db.session.commit()
            
            return {"message": "Search record deleted successfully"}, 200
            
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to delete search record: {str(e)}"}, 400


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
            
            # Get by location name if provided
            location_name = request.args.get('location')
            if location_name:
                location = SavedLocation.query.filter_by(location_name=location_name).first()
                if not location:
                    return {"error": "Location not found"}, 404
                
                weather = WeatherData.query.filter_by(location_id=location.id).first()
                if not weather:
                    return {"error": "No weather data available for this location"}, 404
                
                return weather.to_dict(), 200
            
            # Get all weather data with basic info
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
            
            # Validate required fields
            required_fields = [
                'location_id', 'current_temperature', 
                'current_humidity', 'current_wind_speed',
                'weather_condition', 'forecast_data'
            ]
            if not all(key in data for key in required_fields):
                return {"error": f"Missing required fields: {required_fields}"}, 400
            
            # Verify location exists
            location = SavedLocation.query.get(data['location_id'])
            if not location:
                return {"error": "Location not found"}, 404
            
            # Validate weather condition
            valid_conditions = ['sunny', 'rainy', 'cloudy', 'stormy', 'snowy', 'foggy']
            if data['weather_condition'] not in valid_conditions:
                return {"error": f"Invalid weather condition. Must be one of: {valid_conditions}"}, 400
            
            # Validate numerical values
            if not (-100 <= data['current_temperature'] <= 100):
                return {"error": "Temperature must be between -100 and 100°C"}, 400
            if not (0 <= data['current_humidity'] <= 100):
                return {"error": "Humidity must be between 0 and 100%"}, 400
            if not (0 <= data['current_wind_speed'] <= 500):
                return {"error": "Wind speed must be between 0 and 500 km/h"}, 400
            
            weather = WeatherData(
                location_id=data['location_id'],
                current_temperature=data['current_temperature'],
                current_humidity=data['current_humidity'],
                current_wind_speed=data['current_wind_speed'],
                weather_condition=data['weather_condition'],
                forecast_data=data['forecast_data']
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

    def put(self, id):
        try:
            weather = WeatherData.query.get(id)
            if not weather:
                return {"error": "Weather data not found"}, 404
                
            data = request.get_json()
            
            # Validate at least one field to update
            updatable_fields = [
                'current_temperature', 'current_humidity',
                'current_wind_speed', 'weather_condition',
                'forecast_data'
            ]
            if not any(key in data for key in updatable_fields):
                return {"error": f"No valid fields provided for update. Updatable fields: {updatable_fields}"}, 400
            
            # Validate updates
            if 'current_temperature' in data:
                if not (-100 <= data['current_temperature'] <= 100):
                    return {"error": "Temperature must be between -100 and 100°C"}, 400
                weather.current_temperature = data['current_temperature']
            
            if 'current_humidity' in data:
                if not (0 <= data['current_humidity'] <= 100):
                    return {"error": "Humidity must be between 0 and 100%"}, 400
                weather.current_humidity = data['current_humidity']
            
            if 'current_wind_speed' in data:
                if not (0 <= data['current_wind_speed'] <= 500):
                    return {"error": "Wind speed must be between 0 and 500 km/h"}, 400
                weather.current_wind_speed = data['current_wind_speed']
            
            if 'weather_condition' in data:
                valid_conditions = ['sunny', 'rainy', 'cloudy', 'stormy', 'snowy', 'foggy']
                if data['weather_condition'] not in valid_conditions:
                    return {"error": f"Invalid weather condition. Must be one of: {valid_conditions}"}, 400
                weather.weather_condition = data['weather_condition']
            
            if 'forecast_data' in data:
                weather.forecast_data = data['forecast_data']
            
            weather.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {
                "id": weather.id,
                "location_id": weather.location_id,
                "message": "Weather data updated successfully"
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to update weather data: {str(e)}"}, 400

    def delete(self, id):
        try:
            weather = WeatherData.query.get(id)
            if not weather:
                return {"error": "Weather data not found"}, 404
                
            db.session.delete(weather)
            db.session.commit()
            
            return {"message": "Weather data deleted successfully"}, 200
            
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to delete weather data: {str(e)}"}, 400