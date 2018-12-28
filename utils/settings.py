import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# static路径
STATIC_DIR = os.path.join(BASE_DIR,'static')
# media路径
MEDIA_DIR = os.path.join(STATIC_DIR,'media')
# templates路径
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')


DATABASE={
    'USER': 'root',
    'PASSWORD': '123456',
    'NAME': 'ihome',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'ENGINE': 'mysql',
    'DRIVER': 'pymysql'
}