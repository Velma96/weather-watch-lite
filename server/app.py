from flask import Flask, jsonify, request
from extensions import db, migrate, cors, api
from flask_restful import Resource

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False
    

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    api.init_app(app)
    
    
    from models import User, SavedLocation, SearchRecord, WeatherData
    
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Weather API!"})
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)