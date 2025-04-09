from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api

# Initialize extensions without app
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
api = Api()  # This may not be used if we create a new Api instance in app.py