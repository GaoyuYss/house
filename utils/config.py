from utils.function import get_sqlalchemy_uri
from utils.settings import DATABASE
import redis


class Conf():
    SQLALCHEMY_DATABASE_URI = get_sqlalchemy_uri(DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 这个配置表示无论如何都将执行teardown
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SECRET_KEY = '1212'
    # 配置redis库
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379)