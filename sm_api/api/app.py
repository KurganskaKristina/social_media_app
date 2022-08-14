from datetime import datetime

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from sm_api.models.users import UsersModel as um
from sm_api.models.posts import PostsModel as pm
from sm_api.models.likes import LikesModel as lm
from sm_api.settings import JWT_SECRET

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET
jwt = JWTManager(app)


@app.route('/api/register', methods=['POST'])
def register_user():
    login = request.json['login']
    user = um.select().where(um.login == login).dicts().first()
    if user:
        um.modify_user(user["id"], last_request=datetime.now())
        return jsonify(message="The login already exists."), 409
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    password = request.json['password']
    res_id = um.add_user(first_name, last_name, login, password)
    um.modify_user(res_id, last_request=datetime.now())
    return jsonify(message="User registered successfully."), 201


@app.route('/api/login', methods=['POST'])
def login_user():
    login = request.json['login']
    password = request.json['password']

    user = um.select(um.id).where(um.login == login, um.password == password).dicts().first()

    if user:
        additional_claims = {"user_id": user["id"]}
        access_token = create_access_token(identity=login, additional_claims=additional_claims)
        um.modify_user(user["id"], last_login=datetime.now())
        um.modify_user(user["id"], last_request=datetime.now())
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


@app.route('/api/posts', methods=['GET'])
def get_posts():
    user_id = request.args.get('user_id')
    posts = pm.get_posts(user_id)
    return jsonify(posts), 200


@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_login = get_jwt_identity()
    title = request.json["title"]
    text = request.json["text"]
    user = um.select(um.id).where(um.login == user_login).dicts().first()
    um.modify_user(user["id"], last_request=datetime.now())
    pm.add_post(title, text, user["id"])
    return jsonify(message="You added a post"), 201


@app.route('/api/likes', methods=['GET'])
def get_likes():
    user_id = request.args.get('user_id')
    likes = lm.get_likes(user_id)
    return jsonify(likes), 200


@app.route('/api/like/<int:post_id>', methods=['POST'])
@jwt_required()
def like_post(post_id: int):
    user_login = get_jwt_identity()
    user = um.select(um.id).where(um.login == user_login).dicts().first()
    post = pm.select(pm.id).where(pm.id == post_id).first()
    um.modify_user(user["id"], last_request=datetime.now())
    if user and post:
        lm.add_like(user["id"], post_id)
        return jsonify(message=f"You liked a post #{post_id}"), 201
    return jsonify(message=f"You can't like a post"), 400


@app.route('/api/unlike/<int:post_id>', methods=['DELETE'])
@jwt_required()
def unlike_post(post_id: int):
    user_login = get_jwt_identity()
    user = um.select(um.id).where(um.login == user_login).dicts().first()
    um.modify_user(user["id"], last_request=datetime.now())
    lm.delete_like(user["id"], post_id)
    return jsonify(message=f"You unliked a post #{post_id}"), 201


@app.route('/api/analytics', methods=["GET"])
def get_analytics():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    if not (date_from and date_to):
        return jsonify(message=f"Input a period"), 400

    date_from_datetime = datetime.strptime(date_from, '%m/%d/%y')
    date_to_datetime = datetime.strptime(date_to, '%m/%d/%y')

    res_data = lm.get_likes_for_period(date_from_datetime, date_to_datetime)
    return jsonify(res_data), 200


if __name__ == '__main__':
    app.run()
