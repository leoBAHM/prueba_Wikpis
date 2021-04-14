from flask import Flask, jsonify

from .database import db
from .extensions import mars, migrate


def create_app(settings_module):
    app = Flask(__name__) # Created flask application 
    app.config.from_object(settings_module) # Get config into config.py

    from API.Users import models

    # Add db application
    db.init_app(app)
    mars.init_app(app)
    migrate.init_app(app, db)

    #Register blueprint
    from .Users import user_bp
    app.register_blueprint(user_bp)

    #Error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    @app.errorhandler(500)
    def base_error_handler(e):
        return jsonify({'msg': 'Internal error server', 'status': 500}), 500
    @app.errorhandler(404)
    def error_404_handler(e):
        return jsonify({'msg':'Page not found', 'status': 404}), 404