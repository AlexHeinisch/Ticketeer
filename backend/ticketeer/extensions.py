from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import injector


db = SQLAlchemy()
migrate = Migrate()
custom_injector = injector.Injector()
