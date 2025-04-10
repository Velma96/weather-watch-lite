from flask import Flask, jsonify, request
from extensions import db, migrate, cors, api
from flask_restful import Api  # Import Api class explicitly

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    # Create a new Api instance bound to this app
    api_instance = Api(app)
    
    # Import resources here to avoid circular imports
    from resources import UserResource, SavedLocationResource, SearchRecordResource, WeatherDataResource
    
    # Register resources with the api instance
    api_instance.add_resource(UserResource, '/users', '/users/<int:id>')
    api_instance.add_resource(SavedLocationResource, '/saved-locations', '/saved-locations/<int:id>')
    api_instance.add_resource(SearchRecordResource, '/search-records', '/search-records/<int:id>')
    api_instance.add_resource(WeatherDataResource, '/weather-data', '/weather-data/<int:id>')
    
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Weather API!"})
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)