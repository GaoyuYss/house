from flask import Blueprint, request, render_template, session, jsonify
import random
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import os
from utils.settings import MEDIA_DIR
from re import fullmatch

user_blue = Blueprint('user',__name__)


@user_blue.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        phone = request.form.get('phone')
        code = request.form.get('code')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        user = User.query.filter(User.phone==phone).first()
        se_code = session.get('code')
        if user:
            return jsonify({'code':10002,'msg':'该手机号已注册'})
        if se_code != code:
            return jsonify({'code':10001,'msg':'验证码校验失败'})
        if all([password,password2]):
            if password == password2 :
                new_password = generate_password_hash(password)
                user = User()
                user.phone = phone
                user.pwd_hash = new_password
                user.add_update()
                return jsonify({'code':200,'msg':'注册成功'})
            else:
                return jsonify({'code':10000,'msg':'两次密码不相同'})



@user_blue.route('/img_code/')
def img_code():
    if request.method == 'GET':
        code = ''
        str = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        for i in range(4):
            code += random.choice(str)
        session['code'] = code
        return jsonify({'code':200,'msg':'请求成功','data': code})


@user_blue.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        if not all([phone,password]):
            return jsonify({'code':10001,'msg':'请输入完整信息'})
        user = User.query.filter(User.phone==phone).first()
        if not user:
            return jsonify({'code':10002,'msg':'该手机号没有注册'})
        if not check_password_hash(user.pwd_hash,password):
            return jsonify({'code':10003,'msg':'密码错误'})
        session['user_id'] = user.id
        request.user = user
        return jsonify({'code':200,'msg':'请求成功'})


@user_blue.route('/my/',methods=['GET'])
def my():
    if request.method == 'GET':

        return render_template('my.html')


@user_blue.route('/my_info/',methods=['GET'])
def my_info():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    phone = user.phone
    name = user.name
    if not name:
        name = '无'
    return jsonify({'code':200,'msg':'请求成功','name':name,'phone':phone})


@user_blue.route('/profile/',methods = ['GET'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')


@user_blue.route('/update_info/',methods=['GET'])
def update_info():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        name = user.name
        icon = user.avatar
        return jsonify({'code':200,'msg':'请求成功','name':name,'icon':icon})


@user_blue.route('/update_name/',methods=['POST'])
def update_name():
    if request.method == 'POST':
        name = request.form.get('name')
        user = User.query.filter(User.name==name).first()
        if user :
            return jsonify({'code':201,'msg':'该用户名已存在'})
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        user.name = name
        user.add_update()
        return jsonify({'code':200,'msg':'请求成功'})


@user_blue.route('/update_icon/',methods=['POST'])
def update_icon():
    if request.method == 'POST':
        # 1.获取图片
        icon = request.files.get('avatar')
        # 2.保存图片
        path = os.path.join(MEDIA_DIR,icon.filename)
        icon.save(path)
        # 3.修改图片
        user = User.query.get(session.get('user_id'))
        avatar = '/static/media/' + icon.filename
        user.avatar = avatar
        user.add_update()
        return jsonify({'code':200,'msg':'请求成功','avatar':avatar})


@user_blue.route('/auth/',methods=['GET'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html')


@user_blue.route('/real/', methods=['POST'])
def real():
    if request.method == 'POST':
        id_name = request.form.get('id_name')
        id_card = request.form.get('id_card')
        if not all([id_card,id_name]):
            return jsonify({'code':10001,'msg':'请输入完整信息'})
        re_name = r'([\u4e00-\u9fa5]{1,5})'
        re_card = r'^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$|^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$'
        result = fullmatch(re_name,id_name)
        if not result:
            return jsonify({'code':10002,'msg':'请输入正确姓名'})
        result1 = fullmatch(re_card,id_card)
        if not result1:
            return jsonify({'code':10002,'msg':'请输入正确身份证号'})
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        user.id_name = id_name
        user.id_card = id_card
        user.add_update()
        return jsonify({'code':200,'msg':'保存成功'})


@user_blue.route('/real_push/',methods = ['GET'])
def real_push():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        id_name = user.id_name
        id_card = user.id_card
        if all([id_name,id_card]):
            return jsonify({'code':200,'msg':'刷新成功','id_name':id_name,'id_card':id_card})
        else:
            return jsonify({'code':10002,'msg':'没有身份信息'})


@user_blue.route('/logout/',methods=['GET'])
def logout():
    if request.method == 'GET':
        del session['user_id']
        return jsonify({'code':200,'msg':'退出成功'})