from flask_sqlalchemy import SQLAlchemy
import injector

custom_injector = injector.Injector()
db = SQLAlchemy()
