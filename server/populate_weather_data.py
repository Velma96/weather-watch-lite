from app import app
from extensions import db
from models import WeatherData, SavedLocation
from datetime import datetime
import random


weather_conditions = ['Sunny', 'Rainy', 'Cloudy', 'Snowy', 'Foggy']

with app.app_context():
    for loc in SavedLocation.query.all():
        if not WeatherData.query.filter_by(location_id=loc.id).first():
            forecast_data = {
                'days': [
                    {
                        'day': i,
                        'temp': round(random.uniform(10, 30), 1),
                        'condition': random.choice(weather_conditions)
                    }
                    for i in range(1, 6)
                ]
            }

            db.session.add(WeatherData(
                location_id=loc.id,
                current_temperature=round(random.uniform(10, 30), 1),
                current_humidity=random.randint(30, 90),
                current_wind_speed=round(random.uniform(0, 20), 1),
                weather_condition=random.choice(weather_conditions),
                forecast_data=forecast_data,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ))

    db.session.commit()
    print("✅ Weather data added successfully!")
