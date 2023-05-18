from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource 
import requests   
import ast
import json as JSON

# Blueprints allow this code to be procedurally abstracted from main.py, meaning code is not all in one place
server = Blueprint('server', __name__,
                   url_prefix='/api/server')  # endpoint prefix 

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(server)

data = []

# Function for JSON conversion, apparently there's a better way to do this, but I didn't know about it so this was my solution.
def changeToJSON(bad):
    good = ''
    for i in bad:
        if i != "'":
            good = good + i
        elif i == "'":
            good = good + '"'
    return JSON.loads(good)
class ChessAPI:

    # Reads the api 
    class _get(Resource):
        def get(self):
            return data

    # Pushes directly to the api (unused)
    class _push(Resource):
        def post(self):
            global data
            body = request.get_data(..., True).replace("[", "{").replace("]", "}")
            data.append(body)
            return data 
    
    # Starts a new game instance within the api. The format below is the json format which data should be sent through in.
    class _start(Resource):
        def post(self):
            # request body format: {'gid' : {'uid1' : 1234, 'uid2' : 1234, 'move1' : 'move1', 'move2' : 'move2'}}
            global data
            body = request.get_data(..., True).replace("[", "{").replace("]", "}")
            body = changeToJSON(body)
            data.append(body)
            return data
        