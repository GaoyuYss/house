from utils.settings import DATABASE
from flask import session, redirect, url_for
from functools import wraps

def get_sqlalchemy_uri(BATABASE):
    user = DATABASE['USER']
    password = DATABASE['PASSWORD']
    host = DATABASE['HOST']
    port = DATABASE['PORT']
    name = DATABASE['NAME']
    engine = DATABASE['ENGINE']
    driver = DATABASE['DRIVER']
    return '%s+%s://%s:%s@%s:%s/%s' %(engine,driver,user,password,host,port,name)


def login(func):
    @wraps(func)
    def check(*args,**kwargs):
        if session['user_id']:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('user.login'))
    return check