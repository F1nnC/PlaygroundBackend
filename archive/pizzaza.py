from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from pizzaing import Orders
from flask import Flask
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource 


orders_api = Blueprint('orders_api', __name__,
                   url_prefix='/api/orders/')
api = Api(orders_api)


class OrdersAPI:
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            orderName = body.get('orderName')
            if orderName is None or len(orderName) < 2 or len(orderName) > 30:
                return {'message': f'Name is missing, or is less than 2 characters, or is more than 30 characters'}, 210
            # validate uid
            pizzaType = body.get('pizzaType')
            if pizzaType is None or len(pizzaType) < 2 or len(pizzaType) > 800:
                return {'message': f'pizzaType is missing, or is less than 2 characters, or is more than 800 characters'}, 210
            # validate address
            address = body.get('address')
            if address is None:
                return {'message': f'address is missing'}, 210
           
            ''' Create FdPost instance '''
            uo = Orders(orderName=orderName, pizzaType=pizzaType, address=address)
            
            ''' Additional input error checking '''

            
            ''' Create post in database '''
            # create post in database
            post = uo.create()
            # success returns json of post
            if post:
                return jsonify(post.read())
            # failure returns error
            return {'message': f'Processed {orderName}, format error'}, 210

    class _Read(Resource):
        def get(self):
            posts = Orders.query.all()    # read/extract all posts from database
            json_ready = [post.read() for post in posts]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    class _Delete(Resource):
        def delete(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            post = Orders.query.filter_by(id=id).first()
            if post is None:
                return {'message': f'post not found'}, 404

            post.delete()
            return {'message': f'Deleted'}, 200
        
    class _Update(Resource):
        def put(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            post = Orders.query.filter_by(id=id).first()
            if post is None:
                return {'message': f'post not found'}, 404
            
            body = request.get_json()
            address = body.get('address')
            if address is None:
                return {'message': f'no like change (address) request found'}, 404

            post.update(address)
            return {'message': f'Updated'}, 200
        
    # Building REST api endpoints
    api.add_resource(_Create, '/post') # Create post
    api.add_resource(_Read, '/') # Read post
    api.add_resource(_Delete, '/delete') # Delete post
    api.add_resource(_Update, '/update') # Update post