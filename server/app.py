import os
from flask import Flask, jsonify, request
from extensions import db, migrate, cors
from flask_restful import Api
from decouple import config

def create_app():
    app = Flask(__name__)
    
    # Load configurations from .env
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL', default='sqlite:///weather.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_ORIGINS'] = config('FRONTEND_URL', default='http://localhost:5173,https://weather-watch-lite-1-5aa2.onrender.com').split(',')
    app.json.compact = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    
    # Create API instance
    api_instance = Api(app)
    
    # Import resources
    from resources import UserResource, SavedLocationResource, SearchRecordResource, WeatherDataResource
    
    # Register resources
    api_instance.add_resource(UserResource, '/users', '/users/<int:id>')
    api_instance.add_resource(SavedLocationResource, '/saved-locations', '/saved-locations/<int:id>')
    api_instance.add_resource(SearchRecordResource, '/search-records', '/search-records/<int:id>')
    api_instance.add_resource(WeatherDataResource, '/weather-data', '/weather-data/<int:id>')
    
    # Newsletter signup endpoint
    @app.route('/newsletter', methods=['POST'])
    def newsletter_signup():
        try:
            data = request.get_json()
            if not data or not data.get('email'):
                return jsonify({"error": "Email is required"}), 400
            
            from models import User  # We'll reuse User model for simplicity
            if User.query.filter_by(email=data['email']).first():
                return jsonify({"error": "Email already subscribed"}), 409
            
            # Store email without password/username since it's just for newsletter
            subscriber = User(
                username=f"subscriber_{data['email'].split('@')[0]}",  # Dummy username
                email=data['email'],
                password_hash=''  # No password needed
            )
            db.session.add(subscriber)
            db.session.commit()
            return jsonify({"message": "Successfully subscribed to newsletter", "email": data['email']}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Subscription failed: {str(e)}"}), 500
    
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Weather API!"})
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5555))
    app.run(host="0.0.0.0", port=port)