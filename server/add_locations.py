from app import create_app
from models import db, SavedLocation
from datetime import datetime

app = create_app()

locations = [
    'New York', 'London', 'Lagos', 'Paris', 'Kampala',
    'Kisumu', 'Washington DC', 'Dallas', 'Toronto', 'Rio de Janeiro'
]

with app.app_context():
    for loc in locations:
        # Check if location exists first
        if not SavedLocation.query.filter_by(location_name=loc).first():
            new_loc = SavedLocation(
                user_id=1,  # Change to appropriate user ID
                location_name=loc,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_loc)
    
    db.session.commit()
    print(f"Added {len(locations)} new locations")