from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Initialize extensions without app
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()