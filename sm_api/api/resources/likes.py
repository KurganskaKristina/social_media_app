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
    user = um.get_user(login=user_login)
    post = pm.get_post(post_id)
    um.modify_user(user["id"], last_request=datetime.now())
    if user and post:
        like_id = lm.add_like(user["id"], post_id)
        if like_id:
            return jsonify(message=f"You liked a post #{post_id}"), 201
        else:
            return jsonify(message=f"You have already liked a post #{post_id} before"), 400
    return jsonify(message=f"You can't like a post"), 400


@app.route('/api/unlike/<int:post_id>', methods=['DELETE'])
@jwt_required()
def unlike_post(post_id: int):
    user_login = get_jwt_identity()
    user = um.get_user(login=user_login)
    um.modify_user(user["id"], last_request=datetime.now())
    if lm.delete_like(user["id"], post_id):
        return jsonify(message=f"You unliked a post #{post_id}"), 201
    else:
        return jsonify(message=f"You have already unliked a post #{post_id} before"), 400
