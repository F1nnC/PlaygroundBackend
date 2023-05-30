from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from pizzaOrdersFinal import Order
from flask import Flask

from __init__ import db, app
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
pizza_api_redux = Blueprint('pizza_api_redux', __name__, url_prefix='/api/pizzaorders/')
api = Api(pizza_api_redux)

class PizzaAPI:
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            orderName = body.get('orderName')
            uid = body.get('uid')
            pizzaType = body.get('pizzaType')
            address = body.get('address')
            
            new_order = Order(orderName=orderName, uid=uid, pizzaType=pizzaType, address=address)
            created_order = new_order.create()

            if created_order:
                return jsonify(created_order.read())
            else:
                return {'message': 'Failed to create a new order'}, 500

    class _Read(Resource):
        def get(self):
            orders = Order.query.all()
            json_ready = [order.read() for order in orders]
            return jsonify(json_ready)

    class _Update(Resource):
        def put(self, uid):
            body = request.get_json()
            order = Order.query.get(uid)

            if order:
                order.update(
                    orderName=body.get('orderName', order.orderName),
                    pizzaType=body.get('pizzaType', order.pizzaType),
                    address=body.get('address', order.address)
                )
                return jsonify(order.read())
            else:
                return {'message': 'Order not found'}, 404

    class _Delete(Resource):
        def delete(self, uid):
            order = Order.query.get(uid)

            if order:
                order.delete()
                return {'message': 'Order deleted successfully'}
            else:
                return {'message': 'Order not found'}, 404


    api.add_resource(_Create, '/')
    api.add_resource(_Read, '/')
    api.add_resource(_Update, '/<int:uid>')
    api.add_resource(_Delete, '/<int:uid>')

if __name__ == "__main__":
    app.run()
    CORS(app)