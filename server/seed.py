<<<<<<< HEAD
=======
from faker import Faker
import random
from app import app
from extensions import db
from models import User, SavedLocation, SearchRecord, WeatherData, search_records_locations
from werkzeug.security import generate_password_hash

faker = Faker()
weather_conditions = ['sunny', 'rainy', 'cloudy', 'stormy', 'snowy', 'foggy']

with app.app_context():
    print("Clearing the database")
    db.drop_all()
    db.create_all()
    
    print("Seeding default user...")
    default_user = User(
        username="default",
        email="default@example.com",
        password_hash=generate_password_hash("default")
    )
    db.session.add(default_user)
    db.session.commit()
    
    print("Seeding saved locations and weather data...")
    saved_locations = []
    test_locations = ['New York', 'London', 'Tokyo']
    for loc_name in test_locations:
        location = SavedLocation(
            user_id=default_user.id,
            location_name=loc_name
        )
        db.session.add(location)
        saved_locations.append(location)
    db.session.commit()
    
    for location in saved_locations:
        forecast_data = []
        for i in range(7):
            forecast_data.append({
                "day": i + 1,
                "temperature": round(random.uniform(-10, 35), 1),
                "humidity": random.randint(20, 100),
                "condition": random.choice(weather_conditions)
            })
        weather = WeatherData(
            location_id=location.id,
            current_temperature=round(random.uniform(-10, 35), 1),
            current_humidity=random.randint(20, 100),
            current_wind_speed=round(random.uniform(0, 60), 1),
            weather_condition=random.choice(weather_conditions),
            forecast_data=forecast_data
        )
        db.session.add(weather)
    db.session.commit()
    
    print("Seeding complete.")
>>>>>>> dd07df84e4b1a2d353aebfcd4f9814b8aeabf834
