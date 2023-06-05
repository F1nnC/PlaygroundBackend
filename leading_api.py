from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db, app
from leading_model import Student

student_api = Blueprint('student_api', __name__,
                   url_prefix='/api/student/')

api = Api(student_api)

class StudentAPI(Resource):        
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            studentID = body.get('studentID')
            if studentID is None or len(studentID) < 2 or len(studentID) > 30:
                return {'message': f'Student ID is missing, or is less than 2 characters, or is more than 30 characters'}, 210
            name = body.get('name')
            if name is None or len(name) < 2 or len(name) > 800:
                return {'message': f'Text is missing, or is less than 2 characters, or is more than 800 characters'}, 210
            gpa = body.get('GPA')
            if gpa is None or len(gpa) < 2 or len(gpa) > 800:
                return {'message': f'GPA is missing, or is less than 2 characters, or is more than 800 characters'}, 210
            percentage = body.get('percen')
            if percentage is None or len(percentage) < 2 or len(percentage) > 800:
                return {'message': f'Text is missing, or is less than 2 characters, or is more than 800 characters'}, 210
           
            ''' Create FdPost instance '''
            uo = Student(studentID=studentID, name=name, gpa=gpa, percentage=percentage)
            
            post = uo.create()
            if post:
                return jsonify(post.read())
            return {'message': f'Processed {name}, format error'}, 210

    class _Read(Resource):
        def get(self):
            students = Student.query.all()
            json_ready = [student.read() for student in students]
            return jsonify(json_ready)

    class _Delete(Resource):
        def delete(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            phone = Student.query.filter_by(id=id).first()
            if phone is None:
                return {'message': f'post not found'}, 404

            phone.delete()
            return {'message': f'Deleted'}, 200
        
    class _Update(Resource):
        def put(self):
            id = request.args.get('id')
            if id is None:
                return {'message': f'id {id} is missing'}, 400
        
            post = Student.query.filter_by(id=id).first()
            if post is None:
                return {'message': f'post not found'}, 404
            
            body = request.get_json()
            imageURL = body.get('imageURL')
            if imageURL is None:
                return {'message': f'no like change (imageURL) request found'}, 404

            post.update(imageURL)
            return {'message': f'Updated'}, 200
        
    api.add_resource(_Create, '/post') # Create post
    api.add_resource(_Read, '/') # Read post
    api.add_resource(_Delete, '/delete') # Delete post
    api.add_resource(_Update, '/update') # Update post