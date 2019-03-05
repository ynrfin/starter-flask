import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY = os.environ.get('SECRET_KEY') or "heythereprettyladies"
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "localhost"
    MAIL_PORT = os.environ.get('MAIL_PORT') or 8025

class DevConfig(Config):
    EXPLAIN_TEMPLATE_LOADING = True
    DEBUG =True
