from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from testusers import getName, PizzaUsers


NameAPI = Blueprint('NameAPI', __name__, url_prefix='/api/leaderboards/')

api = Api(NameAPI)


def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

class Login(Resource):
    def post(self):
        body = request.get_json(force=True)
        name = body.get('name')
        if name is None or len(name) < 2:
            return {'message': f'name is missing'}
        password = body.get('password')
        user = getName(name)

        if user is None:
            return {'message': f"invalid username"}

        isPass = user.is_password_match(password)

        if not isPass:
            return {'message': f"wrong password"}
        
        user.score = 0
        user.update()

        response = jsonify(user.read())
        return response

api.add_resource(Login, '/', methods=['GET', 'POST'])
