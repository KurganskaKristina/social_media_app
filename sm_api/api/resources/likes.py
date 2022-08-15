from datetime import datetime


from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from sm_api.api.app import app
from sm_api.models.users import UsersModel as um
from sm_api.models.posts import PostsModel as pm
from sm_api.models.likes import LikesModel as lm


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
