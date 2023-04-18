from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

from superCoolFile import getUser, getName

from superCoolFile import Users

game_currency_api = Blueprint('game_currency_api', __name__,
                   url_prefix='/api/game-currency')

api = Api(game_currency_api)

class UserAPI:
        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate password
            password = body.get('password')
            if password is None or len(password) < 2:
                return {'message': f'Password is missing, or is less than 2 characters'}, 400
            # look for email
            email = body.get('email')
            if email is None or len(email) < 5:
                return {'message': f'Email is missing, or is less than 5 characters'}, 400
            
            ''' #1: Key code block, setup USER OBJECT '''
            uo = Users(name=name, email=email)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(uo.read())
            # failure returns error
            return {'message': f'{name} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            users = Users.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)

    class _GetUser(Resource):
        def get(self, uid):
            user = getUser(uid)
            if user:
                return jsonify(user.read())
            return {'message': f'User with uid {uid} not found'}, 404

    class _UpdateCurrency(Resource):
        def post(self):
            body = request.get_json(force=True)
            uid = body.get('uid')
            currency = body.get('currency')
            user = getUser(uid)
            if user:
                user.update_currency(currency)
                return jsonify(user.read())
            return {'message': f'User with uid {uid} not found'}, 404

    class _DeleteUser(Resource):
        def delete(self, uid):
            user = getUser(uid)
            if user:
                user.delete()
                return {'message': f'User with uid {uid} deleted successfully'}
            return {'message': f'User with uid {uid} not found'}, 404

    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_GetUser, '/<int:uid>')
    api.add_resource(_UpdateCurrency, '/update_currency')
    api.add_resource(_DeleteUser, '/<int:uid>')
