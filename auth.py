from flask import Blueprint
from flask import request, jsonify
import json
from .app import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    jwt_required,
    get_current_user,
    get_jwt_identity,)
from .models import User

app_auth = Blueprint('auth', __name__, url_prefix="/auth")


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify(err="Token has expired"), 401


@app_auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    name = data['name']
    username = data['username']
    email = data['email']
    password = data['password']

    user = User.query.filter_by(username=username).one_or_none()
    print(user)
    if user is None:
        user = User(
            name=name,
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        print('creating user')
        created_user = user.add()
        if created_user:
            access_token = create_access_token(identity=user.user_id)
            refresh_token = create_refresh_token(identity=user.user_id)

            response = jsonify()
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            # response.headers.add('Access-Control-Allow-Origin', '*')

            return response, 201
    return jsonify(
        {
            "message": "Unable to create user."
        }
    ), 400


@app_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        print("60")
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id)

        response = jsonify({"message": f"{username} logged in."})
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 201
    return jsonify(
        {
            "message": "Invalid user details!"
        }
    ), 401


@app_auth.route('/logout', methods=['POST'])

def logout():
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200


@app_auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first()
    access_token = create_access_token(identity=user.user_id)

    response = jsonify()
    set_access_cookies(response, access_token)
    return response, 201


@app_auth.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user = get_current_user()
    user_has_tokens = get_jwt_identity() is not None
    response = jsonify({"user": current_user.user_id, "isLoggedIn": user_has_tokens})
    return response, 201
