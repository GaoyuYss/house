import os
from utils.settings import MEDIA_DIR
from flask import Blueprint, request, render_template, session, jsonify
from app.models import User, Area, Facility, House, HouseImage, Order
from dateutil.parser import parse
from datetime import datetime


house_blue = Blueprint('house',__name__)


@house_blue.route('/index/',methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@house_blue.route('/index_info/',methods=['GET'])
def index_info():
    if request.method == 'GET':
        user_id = session.get('user_id')
        name = ''
        user = User.query.filter(User.id==user_id).first()
        if user:
            if user.name:
                name = user.name
            else:
                name = user.phone
        houses = House.query.all()[0:3]
        houses_data = []
        for house in houses:
            houses_info = house.to_dict()
            houses_data.append(houses_info)
        areas = Area.query.all()
        areas_data = []
        for area in areas:
            area_info = area.to_dict()
            areas_data.append(area_info)
        return jsonify({'code':200,'msg':'请求成功','name':name,'houses_data':houses_data,'areas_data':areas_data})


@house_blue.route('/my_house/',methods=['GET'])
def my_house():
    if request.method == 'GET':
        return render_template('myhouse.html')


@house_blue.route('/is_real/',methods=['GET'])
def is_real():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    id_name = user.id_name
    id_card = user.id_card
    if all([id_name, id_card]):
        return jsonify({'code': 200,'msg':'已经验证身份'})
    else:
        return jsonify({'code': 10002, 'msg': '未验证身份'})


@house_blue.route('/new_house/',methods=['GET'])
def new_house():
    if request.method == 'GET':
        areas = Area.query.all()
        facilits = Facility.query.all()
        return render_template('newhouse.html',areas=areas,facilits=facilits)


@house_blue.route('/push_new_house/',methods=['PATCH'])
def push_new_house():
    if request.method == 'PATCH':
        user_id = session.get('user_id')
        title = request.form.get('title')
        price = request.form.get('price')
        area_id = int(request.form.get('area_id'))
        address = request.form.get('address')
        room_count = request.form.get('room_count')
        acreage = request.form.get('acreage')
        unit = request.form.get('unit')
        capacity = request.form.get('capacity')
        beds = request.form.get('beds')
        deposit = request.form.get('deposit')
        min_days = request.form.get('min_days')
        max_days = request.form.get('max_days')
        facility = request.form.getlist('facility')
        if not all([user_id,title,price,area_id,address,room_count,acreage,unit,capacity,beds,deposit,min_days,max_days,facility]):
            return jsonify({'code':10002,'msg':'请填写完整信息'})
        house = House()
        house.user_id = user_id
        house.title = title
        house.price = price
        house.area_id = area_id
        house.address = address
        house.room_count = room_count
        house.acreage = acreage
        house.unit = unit
        house.capacity = capacity
        house.beds = beds
        house.deposit = deposit
        house.min_days = min_days
        house.max_days = max_days
        for i in facility:
            faci = Facility.query.get(i)
            house.facilities.append(faci)
        house.add_update()
        house_id = house.id
        return jsonify({'code':200,'msg':'添加成功','house_id':house_id})


@house_blue.route('/push_house_image/',methods=['PATCH'])
def push_house_image():
    if request.method == 'PATCH':
        image = request.files.get('house_image')
        if not image:
            return jsonify({'code':10002,'msg':'请添加图片'})
        path = os.path.join(MEDIA_DIR,image.filename)
        image.save(path)
        house_id = request.form.get('house_id')
        house_image = HouseImage()
        house_image.house_id = house_id
        url = '/static/media/' + image.filename
        house_image.url = url
        house_image.add_update()
        index_url = HouseImage.query.filter(HouseImage.house_id==house_id).first().url
        house = House.query.get(house_id)
        house.index_image_url = index_url
        house.add_update()
        return jsonify({'code':200,'msg':'添加成功','url':url})


@house_blue.route('/house_info/',methods=['GET'])
def house_info():
    if request.method == 'GET':
        user_id = session.get('user_id')
        houses = House.query.filter(House.user_id == user_id).all()
        if not houses:
            return jsonify({'code':10001,'msg':'请求成功'})
        data = []
        for house in houses:
            info = house.to_dict()
            data.append(info)
        return jsonify({'code':200,'msg':'请求成功','data':data})


@house_blue.route('/detail/',methods=['GET'])
def detail():
    if request.method == 'GET':
        return render_template('detail.html')


@house_blue.route('/detail_image/<int:id>/',methods=['GET'])
def detail_image(id):
    if request.method == 'GET':
        house = House.query.get(id)
        data = house.to_full_dict()
        return jsonify({'code':200,'msg':'请求成功','data':data})


@house_blue.route('/detail_info/<int:id>/',methods=['GET'])
def detail_info(id):
    if request.method == 'GET':
        house = House.query.get(id)
        data = house.to_full_dict()
        user_id = session.get('user_id')
        booking = 0
        if user_id:
            if user_id == house.user_id:
                booking=1
        return jsonify({'code':200,'msg':'请求成功','data':data,'booking':booking})


@house_blue.route('/search/',methods=['GET'])
def search():
    if request.method == 'GET':
        return render_template('search.html')


@house_blue.route('/house_first/',methods=['POST'])
def house_first():
    if request.method == 'POST':
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')
        sd = datetime.strptime(start_date,'%Y-%m-%d')
        ed = datetime.strptime(end_date, '%Y-%m-%d')
        aid = request.form.get('aid')
        houses = House.query.filter(House.area_id==aid)
        house_id = [house.id for house in houses]
        # 拿到所有这个区的房间的订单
        orders = Order.query.filter(Order.house_id.in_(house_id))
        # 拿到不同不符合条件下的订单
        orders1 = orders.filter(sd<Order.begin_date,Order.begin_date<ed).all()
        orders2 = orders.filter(Order.begin_date < sd, ed < Order.begin_date).all()
        orders3 = orders.filter(sd<Order.end_date ,Order.end_date<ed).all()
        # 将所有不符合条件的订单合在一起
        no_orders = orders1+orders2+orders3
        house_no_id = []
        # 遍历拿到所有不符合条件的订单所对应的房间id
        for order in set(no_orders):
            house_no_id.append(order.house_id)
        # 用所有这个区的房间的id中去除不符合条件的房间id
        new_house_id = set(house_id)-set(house_no_id)
        # 拿到所有符合条件的房间
        new_houses = House.query.filter(House.id.in_(new_house_id)).all()
        house_data = []
        for i in new_houses:
            house_data.append(i.to_full_dict())

        areas = Area.query.all()
        areas_data = []
        for i in areas:
            areas_data.append(i.to_dict())
        return jsonify({'code':200,'msg':'请求成功','house_data':house_data,'areas_data':areas_data})


@house_blue.route('/update_search/',methods=['POST'])
def update_search():
    if request.method == 'POST':
        aid = request.form.get('aid')
        sd1 = request.form.get('sd')
        ed1 = request.form.get('ed')
        sd = datetime.strptime(sd1, '%Y-%m-%d')
        ed =  datetime.strptime(ed1, '%Y-%m-%d')
        sk = request.form.get('sk')
        p = request.form.get('p')
        houses = House.query.filter(House.area_id==aid).all()
        house_id = [house.id for house in houses]
        orders = Order.query.filter(Order.house_id.in_(house_id))
        orders1 = orders.filter(sd<Order.begin_date,Order.begin_date<ed).all()
        orders4 = orders.filter(sd==Order.begin_date).all()
        orders2 = orders.filter(Order.begin_date < sd, ed < Order.begin_date).all()
        orders3 = orders.filter(sd<Order.end_date,Order.end_date<ed).all()
        no_orders = orders1+orders2+orders3+orders4
        house_no_id = []
        for order in set(no_orders):
            house_no_id.append(order.house_id)
        new_house_id = set(house_id)-set(house_no_id)
        new_houses = House.query.filter(House.id.in_(new_house_id))
        if sk == 'new':
            new_houses = new_houses.order_by('id desc').all()
        elif sk == 'booking':
            new_houses = new_houses.order_by('order_count desc').all()
        elif sk == 'price-inc':
            new_houses = new_houses.order_by('price').all()
        elif sk == 'price-des':
            new_houses = new_houses.order_by('price desc').all()
        house_data = []
        for i in new_houses:
            house_data.append(i.to_full_dict())
        return jsonify({'code':200,'msg':'更新成功','house_data':house_data})
