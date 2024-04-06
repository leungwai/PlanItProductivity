from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class Config:
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:productive@productive.ck04jav5vuqu.us-east-1.rds.amazonaws.com/productive'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 100, 'pool_recycle': 280}
