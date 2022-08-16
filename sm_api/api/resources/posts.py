from datetime import datetime

from flask import jsonify, request, json
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
    data = json.loads(request.data)
    user = um.get_user(login=user_login)
    um.modify_user(user["id"], last_request=datetime.now())
    pm.add_post(data["title"], data["text"], user["id"])
    return jsonify(message="You added a post"), 201
