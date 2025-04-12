from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS

from config import Config

db = SQLAlchemy()
migrate = Migrate()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    CORS(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5555, debug=True)
