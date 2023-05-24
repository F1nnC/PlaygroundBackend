from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from testusers import getUser, getName, PizzaUsers



chess_user_api = Blueprint('pizza_user_api', __name__,
                   url_prefix='/api/pizza_users')