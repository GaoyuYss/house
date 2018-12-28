from flask import Blueprint,request, render_template, jsonify, session
from dateutil.parser import parse
from app.models import House,Order
from utils.function import login

order_blue = Blueprint('order',__name__)



@order_blue.route('/booking/',methods=['GET'])
def booking():
    if request.method == 'GET':
        return render_template('booking.html')


@order_blue.route('/house_info/<int:house_id>',methods=['GET'])
def house_info(house_id):
    if request.method == 'GET':
        house = House.query.get(house_id)
        index_image =house.index_image_url
        price = house.price
        title = house.title
        return jsonify({'code':200,'msg':'请求成功','index_image':index_image,'price':price,'title':title})


@order_blue.route('/make_order/',methods=['POST'])
def make_order():
    if request.method == 'POST':
        house_id = request.form.get('house_id')
        begin_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        if not all([begin_date,end_date]):
            return jsonify({'code':10001,'msg':'日期不能为空'})
        user_id = session.get('user_id')
        days = (parse(end_date)-parse(begin_date)).days+1
        house_price = House.query.get(house_id).price
        amount = house_price*days
        order = Order()
        order.user_id = user_id
        order.house_id = house_id
        order.begin_date = begin_date
        order.end_date = end_date
        order.house_price = house_price
        order.days = days
        order.amount = amount
        order.add_update()
        house = House.query.get(house_id)
        count = house.order_count
        house.order_count = int(count)+1
        house.add_update()
        return jsonify({'code':200,'msg':'提交成功'})


@order_blue.route('/orders/',methods=['GET'])
def orders():
    if request.method == 'GET':
        return render_template('orders.html')


@order_blue.route('/my_orders/',methods=['GET'])
def my_orders():
    if request.method == 'GET':
        user_id = session.get('user_id')
        orders = Order.query.filter(Order.user_id==user_id).all()
        data = []
        for order in orders:
            data.append(order.to_dict())
        return jsonify({'code':200,'msg':'请求成功','data':data})


@order_blue.route('/lorders/',methods=['GET'])
def lorders():
    if request.method == 'GET':
        return render_template('lorders.html')


@order_blue.route('/lorders_list/',methods=['GET'])
def lorders_list():
    if request.method == 'GET':
        user_id = session.get('user_id')
        houses = House.query.filter(House.user_id==user_id).all()
        house_id = [house.id for house in  houses]
        orders = Order.query.filter(Order.house_id.in_(house_id)).all()
        data = []
        for order in orders:
            info = order.to_dict()
            data.append(info)
        return jsonify({'code':200,'msg':'请求成功','data':data})


@order_blue.route('/comment/',methods=['POST'])
def comment():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        comment = request.form.get('comment')
        order = Order.query.get(order_id)
        order.comment = comment
        order.status = 'COMPLETE'
        order.add_update()
        return jsonify({'code':200,'msg':'添加成功'})
