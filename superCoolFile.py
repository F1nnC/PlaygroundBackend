from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from testusers import PizzaUsers
from testusers import getName, getUser, getScore 
from flask_sqlalchemy import SQLAlchemy

pizza_user_api = Blueprint('pizza_user_api', __name__,
                   url_prefix='/api/users/')

                   

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(pizza_user_api)
class UserAPI:        
    class _Create(Resource):
        def put(self):
            body = request.get_json(force=True)
            name = body.get('name')
            score = 1  # Increase the score by 1
            users = PizzaUsers.query.filter(PizzaUsers.name.in_(['Toby', 'Gene'])).all()
            user = getName(name)
            if user:
                for user in users:
                    updated_score = user.update_score(score)
                return {'message': f'Score updated to {updated_score}'}
            else:
                return {'message': f'User {name} not found'}, 404
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid
            # uid = body.get('uid')
            # if uid is None or len(uid) < 2:
            #     return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            # look for password and dob
            password = body.get('password')
            dob = body.get('dob')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = PizzaUsers(name=name)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            if dob is not None:
                try:
                    uo.dob = dob
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 210
            
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(uo.read())
            # failure returns error
            return {'message': f'{name} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            users = PizzaUsers.query.all()
            
            # Bubble sort yay!!!!!!!
            n = len(users)
            for i in range(n - 1):
                for j in range(0, n - i - 1):
                    if users[j].score < users[j + 1].score:
                        users[j], users[j + 1] = users[j + 1], users[j]
            
            json_ready = [user.read() for user in users]
            return jsonify(json_ready)



    class _DeleteGame(Resource):
        def post(self):
            body = request.get_json(force=True)
            name = body.get('name')
            date = body.get('date')
            user = getName(name)
            return user.deleteGame(date)

    class _UpdateScore(Resource):
        def put(self, uid):
            user = getUser(uid)
            if user != "Invalid user":
                user.score += 1
                return {'message': 'Score updated successfully'}
            else:
                return {'message': 'Invalid user'}, 404

    class _Win(Resource):
        def post(self):
            body = request.get_json(force=True)
            name = body.get('name')
            password = body.get('password')
            score = 1  
            user = getName(name)
            if user and user.is_password_match(password):
                updated_score = user.update_score(score)
                return {'message': f'Score updated to {updated_score}'}
            elif not user:
                uo = PizzaUsers(name=name, password=password, score=score)
                created_user = uo.create()
                if created_user:
                    return {'message': 'New user created successfully'}
                else:
                    return {'message': 'Failed to create a new user'}, 500
            else:
                return {'message': 'Invalid password'}, 401
        
    class _DeleteUser(Resource):
        def delete(self):
            body = request.get_json(force=True)
            names = body.get('names', [])
            deleted_users = []
            for name in names:
                user = getName(name)
                if user:
                    user.delete()
                    deleted_users.append(name)
            return {'message': 'Deleted users', 'deleted_users': deleted_users}


    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_DeleteGame, '/delete_game')
    api.add_resource(_DeleteUser, "/delete_user/<int:uid>")
    api.add_resource(_UpdateScore, "/update_score/<int:uid>")
    api.add_resource(_Win, '/win')