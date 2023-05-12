from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from testusers import getUser, getName

LeaderboardAPI = Blueprint('LeaderboardAPI.i', __name__, url_prefix='/api/leaderboard')
api = Api(LeaderboardAPI)

# example leaderboard data
leaderboard = {
    'players': [
        {'name': 'John', 'score': 10},
        {'name': 'Emily', 'score': 8},
        {'name': 'Michael', 'score': 6},
        {'name': 'Jane', 'score': 4},
        {'name': 'David', 'score': 2}
    ]
}

class LeaderboardAPI:
    class _Read(Resource):
        def get(self):
            return leaderboard

    class _AddScore(Resource):
        def post(self):
            # read data from json body
            body = request.get_json()
            name = body.get('name')
            score = body.get('score')

            # check if name and score are present in request
            if not name or not score:
                return {'message': 'Please provide a name and a score'}, 400
            
            # check if score is valid (must be a positive integer)
            try:
                score = int(score)
                if score < 0:
                    raise ValueError
            except ValueError:
                return {'message': 'Score must be a positive integer'}, 400
            
            # add player to leaderboard
            leaderboard['players'].append({'name': name, 'score': score})
            
            # sort leaderboard by score in descending order
            leaderboard['players'] = sorted(leaderboard['players'], key=lambda p: p['score'], reverse=True)
            
            return {'message': f'{name} added to leaderboard'}, 201

    # building RESTapi endpoint
    api.add_resource(LeaderboardAPI._Read, '/')
    api.add_resource(LeaderboardAPI._AddScore, '/add_score')

