from random import randrange
from datetime import date
import json
from flask_sqlalchemy import SQLAlchemy
from __init__ import db, app
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash



class test(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _gender = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)
    def __init__(self, username, password, gender, dob = date.today()):
        self._username = username
        self._password = password
        self._gender = gender
        self._dob = dob
 # a getter method, extracts email from object
    @property
    def username(self):
        return self._username
    
    # a setter function, allows name to be updated after initial object creation
    @username.setter
    def username(self, username):
        self._username = username
        
    # check if uid parameter matches user id in object, return boolean
    def is_username(self, username):
        return self._username == username

# a name getter method, extracts name from object
    @property
    def password(self):
        return self._password
    
    # a setter function, allows name to be updated after initial object creation
    @password.setter
    def password(self, password):
        self._password = password
    
    def is_password(self, password):
        return self._password == password

    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    @property
    def age(self):
        today = date.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))
 
    @property
    def gender(self):
        return self._gender
    
    # a setter function, allows name to be updated after initial object creation
    @gender.setter
    def gender(self, gender):
        self._gender = gender
 # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "dob": self.dob,
            "age": self.age,
            "gender": self.gender
        }



# CRUD update: updates user name, password, phone
    # returns self
    def update(self, username="", password = "", dob="", gender=""):
        """only updates values with length"""
        if len(username) > 0:
            self.username = username
        if len(password) > 0:
            self.password = password
        if len(password) > 0:
            self.password = password
        if len(dob) > 0:
            self.dob = dob
        if gender == "male" | gender == "female":
            self.gender = gender
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
        """Tester data for table"""
        u1 = test(username="James", password="1234", gender = "male", dob=date(1847, 2, 11))
        users = [u1]


        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.username}")