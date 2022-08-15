from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import create_access_token

from sm_api.api.app import app
from sm_api.models.users import UsersModel as um


@app.route('/api/register', methods=['POST'])
def register_user():
    login = request.json['login']
    user = um.select().where(um.login == login).first()
    if user:
        um.modify_user(user["id"], last_request=datetime.now())
        return jsonify(message="The login already exists."), 409
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    password = request.json['password']
    um.add_user(first_name, last_name, login, password)
    return jsonify(message="User registered successfully."), 201


@app.route('/api/login', methods=['POST'])
def login_user():
    login = request.json['login']
    password = request.json['password']
    user = um.select(um.id).where(um.login == login, um.password == password).dicts().first()

    if user:
        um.modify_user(user["id"], last_login=datetime.now(), last_request=datetime.now())
        additional_claims = {"user_id": user["id"]}
        access_token = create_access_token(identity=login, additional_claims=additional_claims)
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


@app.route('/api/users', methods=['GET'])
def get_users():
    amount = request.args.get('amount')
    users = um.get_users(amount)
    return jsonify(users), 200


@app.route('/api/users/<int:user_id>/activity', methods=['GET'])
def get_user_activity(user_id: int):
    users = um.get_user_activity(user_id)
    return jsonify(users), 200
