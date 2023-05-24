from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from archive.pizzaTrial import Pizza

pizza_api = Blueprint('pizza_api', __name__, url_prefix='/api/pizza/')
api = Api(pizza_api)

class PizzaAPI:
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            pizza = body.get('pizza')
            pizzaPrice = body.get('pizzaPrice')
            pizzaSize = body.get('pizzaSize')

            new_pizza = Pizza(pizza=pizza, pizzaPrice=pizzaPrice, pizzaSize=pizzaSize)
            created_pizza = new_pizza.create()

            if created_pizza:
                return jsonify(created_pizza.read())
            else:
                return {'message': 'Failed to create a new pizza'}, 500

    class _Read(Resource):
        def get(self):
            pizzas = Pizza.query.all()
            json_ready = [pizza.read() for pizza in pizzas]
            return jsonify(json_ready)

    class _Update(Resource):
        def put(self, pizza_id):
            body = request.get_json()
            pizza = Pizza.query.get(pizza_id)

            if pizza:
                pizza.update(
                    pizza=body.get('pizza', pizza.pizza),
                    pizzaPrice=body.get('pizzaPrice', pizza.pizzaPrice),
                    pizzaSize=body.get('pizzaSize', pizza.pizzaSize)
                )
                return jsonify(pizza.read())
            else:
                return {'message': 'Pizza not found'}, 404

    class _Delete(Resource):
        def delete(self, pizza_id):
            pizza = Pizza.query.get(pizza_id)

            if pizza:
                pizza.delete()
                return {'message': 'Pizza deleted successfully'}
            else:
                return {'message': 'Pizza not found'}, 404

    api.add_resource(_Create, '/')
    api.add_resource(_Read, '/')
    api.add_resource(_Update, '/<int:pizza_id>')
    api.add_resource(_Delete, '/<int:pizza_id>')
