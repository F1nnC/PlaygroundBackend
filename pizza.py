from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from pizzas import pizzas
from __init__ import db, app

pizza_api = Blueprint('pizza_api', __name__,
                   url_prefix='/pizzas')

api = Api(pizza_api)

class PizzaAPI:
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
                        
            ''' Avoid garbage in, error checking '''
            # validate name
            pizzaType = body.get('pizzaType')
            pizzaSize = body.get('pizzaSize')
            pizzaPrice = body.get('pizzaPrice')

            if pizzaType is None or len(pizzaType) < 2:
                return {'message': f'Pizzatype is missing or too short'}, 210
            
            uo = Pizzas(pizza=pizza,
                    pizzaSize=pizzaSize,
                    pizzaPrice=pizzaPrice)
            
            pizza = uo.create()
            if pizza:
                return jsonify(pizza.read())
            return {'message': f'Processed {pizza}, either format issue or pizza is duplicate'}, 210
    class _Read(Resource):
        def get(selfcreate):
            pizzas = Pizzas.query.all()
            json_ready = [pizza.read() for pizza in pizzas]
            return jsonify(json_ready)

api.add_resource(_Create, '/create')
api.add_resource(_Read, '/')