from flask import Flask
from flask_jwt_extended import JWTManager

from sm_api.settings import JWT_SECRET

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET
jwt = JWTManager(app)

from sm_api.api.resources import users, posts, likes, analytics

if __name__ == '__main__':
    app.run()
