from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
import json
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
"""
These object and definitions are used throughout the Jupyter Notebook.
"""


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into a Python shell and follow along '''
class Student(db.Model):
    __tablename__ = 'GPAs'  # table name is plural, class name is singular

    id = db.Column(db.Integer, primary_key=True)
    _studentID = db.Column(db.String(255), unique=False, nullable=False) #_name
    _name = db.Column(db.String(255), unique=True, nullable=False) #_uid
    _GPA = db.Column(db.Integer)
    _percentage = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, studentID, name, GPA, percentage):
        self._studentID = studentID
        self._name = name
        self._GPA = GPA
        self._percentage = percentage

    @property
    def studentID(self):
        return self._studentID
    
    @studentID.setter
    def studentID(self, studentID):
        self._studentID = studentID
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
        
    def is_name(self, name):
        return self._name == name
    
    @property
    def GPA(self):
        return self._GPA
    
    @GPA.setter
    def GPA(self, GPA):
        self._GPA = GPA

    @property
    def percentage(self):
        return self._percentage
    
    @percentage.setter
    def percentage(self, percentage):
        self._percentage = percentage
    
    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "studentID": self.studentID,
            "name": self.name,
            "GPA": self.GPA,
            "percentage": self.percentage
        }

    def update(self, studentID="", name="", GPA="", percentage=""):
        """only updates values with length"""
        if len(studentID) > 0:
            self.studentID = studentID
        if len(name) > 0:
            self.name = name
        if len(percentage) > 0:
            self.percentage = percentage
        db.session.commit()
        db.session.add(self)
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def initStudents():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        s1 = Student(studentID='1924520', name='Dillon Lee', GPA='3.5', percentage='85%')
        s2 = Student(studentID='1820352', name='Steven', GPA='3.8', percentage='92%')
        s3 = Student(studentID='1923509', name='Noor', GPA='3.2', percentage='98%')
        s4 = Student(studentID='1812350', name='Lucas', GPA='3.9', percentage='75%')

        students = [s1, s2, s3, s4]

        """Builds sample user/note(s) data"""
        for student in students:
            try:
                '''add user to table'''
                object = student.create()
                print(f"Created new uid {object.name}")
            except:
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {student.name}, or error.")
                
initStudents()

def find_by_name(name):
    with app.app_context():
        name = Student.query.filter_by(_name=name).first()
    return name

def create():
    studentID = input("Enter the student ID: ")
    name = input("Enter your name: ")
    gpa = input("Enter your GPA: ")
    percentage = input("Enter your percentage: ")


    student = Student(studentID=studentID, 
                name=name, 
                GPA=gpa,
                percentage=percentage
                )
        
    with app.app_context():
            try:
                object = student.create()
                print("Created\n", object.read())
            except:
                print("Unknown error uid {uid}")

def read():
    with app.app_context():
        table = Student.query.all()
    json_ready = [student.read() for student in table]
    return json_ready

# def delete_by_phone():
#     orderName = input("Enter uid of user to be deleted ")
#     user = find_by_company(orderName)
#     with app.app_context():
#         try:
#             object = user.delete() 
#             print(f"User with uid {orderName} has been deleted")
#         except:
#            (f"No user with uid {orderName} was found")
        
# delete_by_phone()