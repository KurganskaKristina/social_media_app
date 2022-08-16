from datetime import datetime

from flask import jsonify, request, json
from flask_jwt_extended import create_access_token

from sm_api.api.app import app
from sm_api.models.users import UsersModel as um


@app.route('/api/register', methods=['POST'])
def register_user():
    login = request.json['login']
    user = um.get_user(login=login)

    if user is not None:
        return jsonify(message="The login already exists."), 409

    data = json.loads(request.data)
    um.add_user(data['first_name'], data['last_name'], login, data['password'])

    return jsonify(message="User registered successfully."), 201


@app.route('/api/login', methods=['POST'])
def login_user():
    data = json.loads(request.data)
    user = um.get_registered_user(data['login'], data['password'])

    if user:
        um.modify_user(user["id"], last_login=datetime.now(), last_request=datetime.now())
        access_token = create_access_token(identity=data['login'], additional_claims={"user_id": user["id"]})
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
