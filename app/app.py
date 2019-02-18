from flask import Flask

from app.extensions import db, migrate, login_manager
from app import user
from app.config import DevConfig
from app.user.models import User

from werkzeug.contrib.fixers import ProxyFix

def create_app():
    app = Flask(__name__)
    register_config(app)
    register_extensions(app)
    register_blueprint(app)

    register_shell_context(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    return app

def register_config(app):
    app.config.from_object(DevConfig)
#def register_logger(app):


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

def register_blueprint(app_par):
    app_par.register_blueprint(user.view.bp, url_prefix="/user")

def register_shell_context(app):
    def shell_context():
        return {
            'db' : db,
            'User' : User
        }
    app.shell_context_processor(shell_context)
#def register_error_handler(app):

