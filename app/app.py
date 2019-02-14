from flask import Flask

from app.extensions import db, migrate
from app import user

from werkzeug.contrib.fixers import ProxyFix

def create_app():
    app = Flask(__name__)
    register_blueprint(app)

    app.wsgi_app = ProxyFix(app.wsgi_app)
    return app

#def register_logger(app):


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app)

def register_blueprint(app_par):
    app_par.register_blueprint(user.view.bp, url_prefix="/user")

#def register_shell_context(app):
        
#def register_error_handler(app):
        
