from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from model.pizzaMenus import Menu

menu_api = Blueprint('menu_api', __name__,
                   url_prefix='/api/pizzaMenus')

api = Api(menu_api)

class MenuAPI(Resource):        
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            pizza = body.get('pizza')
            if pizza is None or len(pizza) < 2 or len(pizza) > 30:
                return {'message': f'Model is missing, or is less than 2 characters, or is more than 30 characters'}, 210
            price = body.get('price')
            if price is None or len(price) < 2 or len(price) > 800:
                return {'message': f'Text is missing, or is less than 2 characters, or is more than 800 characters'}, 210
            size = body.get('size')
            if size is None or len(size) < 2 or len(size) > 800:
                return {'message': f'Price is missing, or is less than 2 characters, or is more than 800 characters'}, 210
           
            ''' Create FdPost instance '''
            uo = Menu(pizza=pizza, price=price, size=size)
            
            post = uo.create()
            if post:
                return jsonify(post.read())
            return {'message': f'Processed {pizza}, format error'}, 210

    class _Read(Resource):
        def get(self):
            Menu = Menu.query.all()
            json_ready = [phone.read() for phone in menus]
            return jsonify(json_ready)

    class _Delete(Resource):
        def delete(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            menu = Menu.query.filter_by(id=id).first()
            if menu is None:
                return {'message': f'post not found'}, 404

            phone.delete()
            return {'message': f'Deleted'}, 200
        
    class _Update(Resource):
        def put(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            post = Phone.query.filter_by(id=id).first()
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