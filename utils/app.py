from flask import Flask
from utils.settings import TEMPLATE_DIR, STATIC_DIR
from utils.config import Conf
from app.house import house_blue
from app.user import user_blue
from app.order import order_blue
from app.models import db
from flask_session import Session


def create_app():
    app = Flask(__name__,static_folder=STATIC_DIR,template_folder=TEMPLATE_DIR)
    app.config.from_object(Conf)
    app.register_blueprint(blueprint=user_blue,url_prefix='/user')
    app.register_blueprint(blueprint=house_blue,url_prefix='/house')
    app.register_blueprint(blueprint=order_blue,url_prefix='/order')

    se = Session()
    se.init_app(app)

    db.init_app(app)

    return app

