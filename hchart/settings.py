from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SECRET_KEY = env.str("SECRET_KEY")
MAX_CONTENT_LENGTH = 204800 # max allowed file size is 200 kb (200 * 1024)
