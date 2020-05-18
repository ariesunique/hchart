from environs import Env

env = Env()
env.read_env()

ENV = "development"
DEBUG = True
TESTING = True
SECRET_KEY = "secret"
WTF_CSRF_ENABLED = False
