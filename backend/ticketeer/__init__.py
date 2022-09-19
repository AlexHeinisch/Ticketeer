from flask import Flask
from flask_cors import CORS
import json

# Flask Injector
import injector
from .dependencies import configure
from flask_injector import FlaskInjector

# Blueprints
from .endpoint.ticket_endpoint import ticket
from .endpoint.user_endpoint import user

from .security.authentication import authentication

from .error.error_handlers import error_handlers

custom_injector = injector.Injector()

def create_app(test_config=None, injector_module=None) -> Flask:

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_file('config.json', load=json.load)
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(ticket, url_prefix='/ticket')
    app.register_blueprint(user, url_prefix='/user')

    app.register_blueprint(authentication, url_prefix='/auth')

    app.register_blueprint(error_handlers)

    modules = [configure]
    if injector_module:
        modules.append(injector_module)

    FlaskInjector(app=app, modules=modules, injector=custom_injector)

    return app
