from flask import Flask
from flask_cors import CORS

from .models import db, migrate
from .routes import api


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api, url_prefix='/api/products/')

    return app
