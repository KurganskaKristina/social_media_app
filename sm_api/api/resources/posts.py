from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from sm_api.api.app import app
from sm_api.models.users import UsersModel as um
from sm_api.models.posts import PostsModel as pm


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
