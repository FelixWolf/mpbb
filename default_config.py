from app import app
import os.path
rootdir = os.path.dirname(os.path.realpath(__file__))+"/"
class Config(object):
    ROOT_DIR = rootdir
    CACHE_DIR = "./.cache"
    SQLALCHEMY_DATABASE_URI = "sqlite://{}/database.sqlite".format(rootdir)
    SQLALCHEMY_TRACK_MODIFICATIONS = app.debug
