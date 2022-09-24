from flask import Flask
from flask_cors import CORS

# Flask Injector
from flask_injector import FlaskInjector

# extensions
from ticketeer.extensions import custom_injector, db, migrate

# config loading
from ticketeer.config import load_config

# Dependency Injection config
from ticketeer.dependencies import configure

# Blueprints
from ticketeer.endpoint.ticket_endpoint import ticket
from ticketeer.endpoint.user_endpoint import user
from ticketeer.security.authentication import authentication
from ticketeer.error.error_handlers import error_handlers


def create_app(test_config=None, injector_module=None) -> Flask:

    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(load_config())
    else:
        app.config.from_mapping(test_config)
    print(app.debug)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db) 

    app.register_blueprint(ticket, url_prefix='/ticket')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(authentication, url_prefix='/auth')
    app.register_blueprint(error_handlers)

    modules = [configure]
    if injector_module:
        modules.append(injector_module)

    FlaskInjector(app=app, modules=modules, injector=custom_injector)
    
    with app.app_context():
        db.create_all()
        return app
