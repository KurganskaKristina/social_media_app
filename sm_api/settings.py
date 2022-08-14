from os import environ
from datetime import timedelta

from sm_api.config import Config

config_path = environ.get("CONFIG_PATH") or '/home/kristina/PycharmProjects/social_media_app/config.json'
config = Config(config_path).read()

JWT_SECRET = config["jwt_secret"]
ACCESS_EXPIRES = timedelta(hours=1)

DATABASE = {
    'drivername': config["database"]['drivername'],
    'host': config["database"]["host"],
    'port': config["database"]['port'],
    'username': config["database"]['username'],
    'password': config["database"]['password'],
    'database': config["database"]['database']
}
