from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from testusers import PizzaUsers
from testusers import getName, getUser, getScore 
from flask_sqlalchemy import SQLAlchemy

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

from __init__ import db, app

pizza_user_api = Blueprint('pizza_user_api', __name__,
                   url_prefix='/api/users/')

                   

# API docs https://flask-restful.readthedocs.io/en/latest/api.html

api = Api(pizza_user_api)

class UserAPI:
    
    class _Create(Resource):
        def put(self):
            # Retrieve JSON data from the request body
            body = request.get_json(force=True)
            name = body.get('name')
            score = 1  # Increase the score by 1
            
            # Query PizzaUsers table for users with names 'Toby' or 'Gene'
            users = PizzaUsers.query.filter(PizzaUsers.name.in_(['Toby', 'Gene'])).all()
            
            # Get user by name
            user = getName(name)
            
            if user:
                for user in users:
                    # Update the user's score
                    updated_score = user.update_score(score)
                return {'message': f'Score updated to {updated_score}'}
            else:
                return {'message': f'User {name} not found'}, 404
        
        def post(self):
            ''' Read data from JSON body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            
            # Validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing or is less than 2 characters'}, 210
            
            # Validate uid
            # uid = body.get('uid')
            # if uid is None or len(uid) < 2:
            #     return {'message': f'User ID is missing or is less than 2 characters'}, 210
            
            # Look for password and dob
            password = body.get('password')
            dob = body.get('dob')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = PizzaUsers(name=name)
            
            ''' Additional garbage error checking '''
            
            # Set password if provided
            if password is not None:
                uo.set_password(password)
            
            # Convert dob to date type
            if dob is not None:
                try:
                    uo.dob = dob
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 210
            
            # Create user in the database
            user = uo.create()
            
            # Success returns JSON of user
            if user:
                return jsonify(uo.read())
            
            # Failure returns error
            return {'message': f'{name} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            # Get all users from the PizzaUsers table
            users = PizzaUsers.query.all()
            
            # Bubble sort users based on score (descending order)
            n = len(users)
            for i in range(n - 1):
                for j in range(0, n - i - 1):
                    if users[j].score < users[j + 1].score:
                        users[j], users[j + 1] = users[j + 1], users[j]
            
            # Prepare users in JSON format
            json_ready = [user.read() for user in users]
            
            return jsonify(json_ready)

    class _DeleteGame(Resource):
        def post(self):
            body = request.get_json(force=True)
            name = body.get('name')
            date = body.get('date')
            
            # Get user by name
            user = getName(name)
            
            return user.deleteGame(date)

    class _UpdateScore(Resource):
        def put(self, uid):
            # Get user by uid
            user = getUser(uid)
            
            if user != "Invalid user":
                # Update the user's score
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
            
            # Get user by name
            user = getName(name)
            
            if user and user.is_password_match(password):
                # Update the user's score
                updated_score = user.update_score(score)
                return {'message': f'Score updated to {updated_score}'}
            elif not user:
                # Create a new user if the user doesn't exist
                uo = PizzaUsers(name=name, password=password, score=score)
                created_user = uo.create()
                
                if created_user:
                    return {'message': 'New user created successfully'}
                else:
                    return {'message': 'Failed to create a new user'}, 500
            else:
                return {'message': 'Invalid password'}, 401
        
    class _DeleteUser(Resource):
        def delete(self, username, password):
        # Get user by name
            user = getName(username)

            if user and user.is_password_match(password):
            # Delete the user
                user.delete()
                return {'message': f'User {username} deleted successfully'}
            elif not user:
                return {'message': f'User {username} not found'}, 404
            else:
                return {'message': 'Invalid password'}, 401


    # Building REST API endpoints
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_DeleteUser, "/delete_user/<string:username>/<string:password>")
    api.add_resource(_UpdateScore, "/update_score/<int:uid>")
    api.add_resource(_Win, '/win')

if __name__ == "__main__":
    app.run()

