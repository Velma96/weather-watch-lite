# seed.py
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
    
    print("Seeding users...")
    users = []
    for _ in range(15):
        #Use generate_password_hash for proper password hashing
        user = User(
            username=faker.user_name(),
            email=faker.email(),
            password_hash=generate_password_hash(faker.password(length=10))
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()
    
    print("Seeding saved locations and weather data...")
    saved_locations = []
    for user in users:
        for _ in range(random.randint(1, 3)):
            location = SavedLocation(
                user_id=user.id,
                location_name=faker.city()
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
    
    print("Seeding search records...")
    for user in users:
        user_locations = [loc for loc in saved_locations if loc.user_id == user.id]
        for _ in range(random.randint(2, 4)):
            query = f"{faker.city()} weather"
            search = SearchRecord(
                user_id=user.id,
                query=query
            )
            db.session.add(search)
            db.session.commit()  
            
            
            if user_locations: 
                linked_locations = random.sample(user_locations, min(len(user_locations), random.randint(1, 2)))
                for loc in linked_locations:
                    db.session.execute(search_records_locations.insert().values(
                        search_record_id=search.id,
                        saved_location_id=loc.id
                    ))
    
    db.session.commit()
    print("Seeding complete.")