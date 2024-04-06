from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

jwt = JWTManager()
db = SQLAlchemy()


"""Construct the core application."""
app = Flask(__name__, instance_relative_config=False)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:productive@productive.ck04jav5vuqu.us-east-1.rds.amazonaws.com/productive'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:productive@productivityapp.ck04jav5vuqu.us-east-1.rds.amazonaws.com/productivityapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100, 'pool_recycle': 280}
app.config['SECRET_KEY'] = 'testing'
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True

db.init_app(app)
jwt.init_app(app)


with app.app_context():
    CORS(app, resources={r'/*': {'origins': '*'}})
  # Create sql tables for our data models


from productivityapp.auth import app_auth
app.register_blueprint(app_auth)


from productivityapp.routes import app_routes
app.register_blueprint(app_routes)