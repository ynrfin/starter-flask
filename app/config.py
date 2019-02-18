import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY = os.environ.get('SECRET_KEY') or "heythereprettyladies"

class DevConfig(Config):
    EXPLAIN_TEMPLATE_LOADING = True
    DEBUG =True
