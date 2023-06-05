from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from chess_model import test
from __init__ import db, app
chess_api = Blueprint('chess_api', __name__,
                   url_prefix='/api/chess')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(chess_api)

class ChessAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            white = body.get('white')
            black = body.get('black')
            chess_id = body.get('chess_id')
            move = body.get('move')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = test(white=white, 
                      black=black, 
                      chess_id=chess_id,
                      move=move)
            
            ''' Additional garbage error checking '''
            # set password if provided
            ''' #2: Key Code block to add user to database '''
            # create user in database
            chess_user = uo.create()
            # success returns json of user
            if chess_user:
                return jsonify(chess_user.read())
            # failure returns error
            return {'message': f'Processed {white}, either a format error or User ID {white}are duplicate'}, 210

    class _Read(Resource):
        def get(self):
            users = test.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    # class _Security(Resource):
    #     def post(self):
    #         ''' Read data for json body '''
    #         body = request.get_json()
    #         ''' Get Data '''
    #         white = body.get('white')
    #         if white is None:
    #             return {'message': f'User ID is missing, or is less than 2 characters'}, 400
    #         black = body.get('black')
    #         if black is None:
    #             return {'message': f'User ID is missing, or is less than 2 characters'}, 400
    #         ''' Find user '''
    #         user = test.query.filter_by(_white=white).first()
    #         if user is None or not user.is_black(black):
    #             return {'message': f"Invalid user id or password"}, 400  
    #         ''' authenticated user '''
    #         return jsonify(user.read())

        
        
        
    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    # api.add_resource(_Security, '/match')
    