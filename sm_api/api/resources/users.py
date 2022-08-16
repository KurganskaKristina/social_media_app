from datetime import datetime

from flask import jsonify, request, json
from flask_jwt_extended import create_access_token

from sm_api.api.app import app
from sm_api.api.utils import check_dict_attr
from sm_api.api.validators import UserRegisterDataValidator, UserLoginDataValidator
from sm_api.models.users import UsersModel as um


@app.route('/api/register', methods=['POST'])
def register_user():
    data = json.loads(request.data)
    valid_data = check_dict_attr(UserRegisterDataValidator, data, "Invalid data to register a user")
    user = um.get_user(login=valid_data.login)

    if user is not None:
        return jsonify(message="The login already exists."), 409

    um.add_user(valid_data.first_name, valid_data.last_name, valid_data.login, valid_data.password)

    return jsonify(message="User registered successfully."), 201


@app.route('/api/login', methods=['POST'])
def login_user():
    data = json.loads(request.data)
    valid_data = check_dict_attr(UserLoginDataValidator, data, "Invalid data to login a user")
    user = um.get_registered_user(valid_data.login, valid_data.password)

    if user:
        um.modify_user(user["id"], last_login=datetime.now(), last_request=datetime.now())
        access_token = create_access_token(identity=data['login'], additional_claims={"user_id": user["id"]})
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        amount = request.args.get('amount')
        users = um.get_users(amount)
        return jsonify(users), 200
    except ValueError:
        return jsonify(message="Wrong query parameters data."), 400


@app.route('/api/users/<int:user_id>/activity', methods=['GET'])
def get_user_activity(user_id: int):
    users = um.get_user_activity(user_id)
    if users:
        return jsonify(users), 200
    return jsonify(message="User can't be found"), 400
