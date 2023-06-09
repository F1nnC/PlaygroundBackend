from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db, app
from edwin_model import Phone

# Blueprint and API runtime url
phone_api = Blueprint('phone_api', __name__,
                   url_prefix='/api/edwin/')

api = Api(phone_api)
# This is what makes the class and is called in main.py
class PhoneAPI(Resource):        
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Checking the length of each variable
            model = body.get('model')
            if model is None or len(model) < 2 or len(model) > 30:
                return {'message': f'Model is missing, or is less than 2 characters, or is more than 30 characters'}, 210
            company = body.get('company')
            if company is None or len(company) < 2 or len(company) > 800:
                return {'message': f'Text is missing, or is less than 2 characters, or is more than 800 characters'}, 210
            price = body.get('price')
            if price is None or len(price) < 2 or len(price) > 800:
                return {'message': f'Price is missing, or is less than 2 characters, or is more than 800 characters'}, 210
           
            ''' Create FdPost instance '''
            uo = Phone(model=model, company=company, price=price)
            
            post = uo.create()
            if post:
                return jsonify(post.read())
            return {'message': f'Processed {model}, format error'}, 210
    # Read all the values in the list and in the table
    class _Read(Resource):
        def get(self):
            phones = Phone.query.all()
            json_ready = [phone.read() for phone in phones]
            return jsonify(json_ready)
    # This is the code to delete and send to /website/create
    class _Delete(Resource):
        def delete(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            phone = Phone.query.filter_by(id=id).first()
            if phone is None:
                return {'message': f'post not found'}, 404

            phone.delete()
            return {'message': f'Deleted'}, 200
    # Update the data for each user based on the ID #
    class _Update(Resource):
        def put(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            post = Phone.query.filter_by(id=id).first()
            if post is None:
                return {'message': f'post not found'}, 404
            
            body = request.get_json()
            imageURL = body.get('imageURL')
            if imageURL is None:
                return {'message': f'no like change (imageURL) request found'}, 404

            post.update(imageURL)
            return {'message': f'Updated'}, 200
        
    api.add_resource(_Create, '/post') # Create phone
    api.add_resource(_Read, '/') # Read phone
    api.add_resource(_Delete, '/delete') # Delete phone
    api.add_resource(_Update, '/update') # Update phone