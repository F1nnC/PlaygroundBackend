from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from users import test
from __init__ import db, app
user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _Create(Resource):
        def post(self):
            
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            username = body.get('username')
            password = body.get('password')
            gender = body.get('gender')
            dob = body.get('dob')
            ''' #1: Key code block, setup USER OBJECT '''
            uo = test(username=username, 
                      password=password, 
                      gender= gender,
                      dob=dob)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {username}, either a format error or User ID {username} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            users = test.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    class _findUsername(Resource):
        def get(self):
            usernames = []
            users = test.query.all()
            username = [user.read() for user in users]
            for i in range(len(username)):
                usernames.append({"username": username[i]['username'], "password": username[i]['password'],"dob": username[i]['dob']})
            return jsonify(usernames)
    class _Security(Resource):

        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            ''' Get Data '''
            username = body.get('username')
            if username is None:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            password = body.get('password')
            ''' Find user '''
            user = test.query.filter_by(_username=username).first()
            if user is None or not user.is_password(password):
                return {'message': f"Invalid user id or password"}, 400  
            ''' authenticated user '''
            return jsonify(user.read())


    # class _Calender_tuesday(Resource):
    #     def post(self):
    #         body = request.get_json()
    #         username = body.get('username')
    #         tuesday = body.get('tuesday')
    #         if username is None:
    #             return {'message': f'User ID is missing'}, 400
    #         if tuesday is None:
    #             return {'message': f'Tuesday is missing'}, 400   
    #         user = test.query.filter_by(_username=username).first()
    #         user.tuesday += " " + tuesday
    #         db.session.commit()
    #         return jsonify(user.read())
    
    # class _update_password(Resource):
    #     def post(self):
    #         body = request.get_json()
    #         username = body.get('username')
    #         password = body.get('password')
    #         dob = body.get('dob')
    #         if username is None:
    #             return {'message': f'User ID is missing'}, 400
    #         if password is None:
    #             return {'message': f'password is missing'}, 400
            
    #         user = test.query.filter_by(_username=username).first()
    #         if dob != user.dob:
    #             return {'message': f'birthday is not matched'}, 400
    #         user.password = password
    #         db.session.commit()
    #         return jsonify(user.read())
    # class _delete_user(Resource):
    #     def post(self):
    #         body = request.get_json()
    #         username = body.get('username')
    #         password = body.get('password')
    #         if username is None:
    #             return {'message': f'User ID is missing'}, 400
    #         if password is None:
    #             return {'message': f'password is missing'}, 400
    #         user = test.query.filter_by(_username=username).first()
    #         if user is None or not user.is_password(password):
    #             return {'message': f"Invalid user id or password"}, 400  
    #         user.delete()
    #         db.session.commit()
    #         return jsonify(user.read())
        
        
        
    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Security, '/match')
    api.add_resource(_findUsername, '/username')