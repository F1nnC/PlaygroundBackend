from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Setup of key Flask object (app)
app = Flask(__name__)
database = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy()

# This belongs in place where it runs once per project
db.init_app(app)

""" database dependencies to support sqlite examples """
import datetime
from datetime import datetime
import json

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into a Python shell and follow along '''
class Orders(db.Model):
    __tablename__ = 'Orderings'
    id = db.Column(db.Integer, primary_key=True)
    _orderName = db.Column(db.String(255), unique=True, nullable=False) #_name
    _pizzaType = db.Column(db.String(255), unique=False, nullable=False) #_uid
    _address = db.Column(db.String(255), unique=False, nullable=False) # _password

    def __init__(self, orderName, pizzaType, address):
        self._orderName = orderName
        self._pizzaType = pizzaType
        self._address = address

    @property
    def orderName(self):
        return self._orderName
    
    @orderName.setter
    def orderName(self, orderName):
        self._orderName = orderName
    
    @property
    def pizzaType(self):
        return self._pizzaType
    
    @pizzaType.setter
    def pizzaType(self, pizzaType):
        self._pizzaType = pizzaType
        
    def is_pizzaType(self, pizzaType):
        return self._pizzaType == pizzaType
    
    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, address):
        self._address = address

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
            "orderName": self.orderName,
            "pizzaType": self.pizzaType,
            "address": self.address,
        }

    def update(self, orderName="", pizzaType="", address=""):
        """only updates values with length"""
        if len(orderName) > 0:
            self.orderName = orderName
        if len(pizzaType) > 0:
            self.pizzaType = pizzaType
        if len(address) > 0:
            self.address = address
        db.session.commit()
        db.session.add(self)
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

# Builds working data for testing
def initPizzaing():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        p1 = Orders(orderName='James', pizzaType='Cheese', address='799')
        p2 = Orders(orderName='Finn', pizzaType='Pepperoni', address='999')

        orders = [p1, p2]
        
        """Builds sample user/note(s) data"""
        for order in orders:
            try:
                '''add user to table'''
                object = order.create()
                print(f"Created new uid {object.orderName}")
            except:  # error raised if object nit created
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {order.orderName}, or error.")
                
initPizzaing()

def find_by_name(orderName):
    with app.app_context():
        name = Orders.query.filter_by(_orderName=orderName).first()
    return name # returns user object

# Inputs, Try/Except, and SQLAlchemy work together to build a valid database object
def create():
    # optimize user time to see if uid exists
    pizzaType = input("Enter your pizza: ")
    orderName = input("Enter your name: ")
    address = input("Enter your address: ")
    
    # Initialize User object before date
    order = Orders(orderName=orderName, 
                pizzaType=pizzaType, 
                address=address,
                )

    # write object to database
    with app.app_context():
        try:
            object = order.create()
            print("Created\n", object.read())
        except:  # error raised if object not created
            print("Unknown error uid {uid}")
        
# create()

def read():
    with app.app_context():
        table = Orders.query.all()
    json_ready = [order.read() for order in table] # each user adds user.read() to list
    return json_ready

# read()

def delete_by_company(): # makes a new function called delete_by_uid
    orderName = input("Enter uid of user to be deleted ") # prompts the user to enter the uid
    user = find_by_name(orderName)  # using previous function to locate user by inputted id
    with app.app_context():
        try:
            object = user.delete() 
            print(f"User with uid {orderName} has been deleted")
        except:  # error raised if object not found
           (f"No user with uid {orderName} was found")
        
delete_by_company()
