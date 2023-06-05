from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db, app
from luka_model import Pizza

menu_api = Blueprint('menu_api', __name__,
                   url_prefix='/api/menu/')

api = Api(menu_api)

class MenuAPI(Resource):        
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            name = body.get('name')
            if name is None or len(name) < 2 or len(name) > 30:
                return {'message': f'Name is missing, or is less than 2 characters, or is more than 30 characters'}, 210
            pizza = body.get('pizza')
            if pizza is None or len(pizza) < 2 or len(pizza) > 800:
                return {'message': f'Pizza is missing, or is less than 2 characters, or is more than 800 characters'}, 210
            size = body.get('size')
            if size is None or len(size) < 2 or len(size) > 800:
                return {'message': f'GPA is missing, or is less than 2 characters, or is more than 800 characters'}, 210
            price = body.get('price')
            if price is None or len(price) < 2 or len(price) > 800:
                return {'message': f'Price is missing, or is less than 2 characters, or is more than 800 characters'}, 210
           
            uo = Pizza(name=name, pizza=pizza, size=size, price=price)
            
            post = uo.create()
            if post:
                return jsonify(post.read())
            return {'message': f'Processed {name}, format error'}, 210

    class _Read(Resource):
        def get(self):
            orders = Pizza.query.all()
            json_ready = [order.read() for order in orders]
            return jsonify(json_ready)

    class _Delete(Resource):
        def delete(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            order = Pizza.query.filter_by(id=id).first()
            if order is None:
                return {'message': f'post not found'}, 404

            order.delete()
            return {'message': f'Deleted'}, 200
        
    class _Update(Resource):
        def put(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            post = Pizza.query.filter_by(id=id).first()
            if post is None:
                return {'message': f'post not found'}, 404
            
            body = request.get_json()
            imageURL = body.get('imageURL')
            if imageURL is None:
                return {'message': f'no like change (imageURL) request found'}, 404

            post.update(imageURL)
            return {'message': f'Updated'}, 200
        
    api.add_resource(_Create, '/post') # Create post
    api.add_resource(_Read, '/') # Read post
    api.add_resource(_Delete, '/delete') # Delete post
    api.add_resource(_Update, '/update') # Update post