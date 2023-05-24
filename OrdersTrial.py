"""
These imports define the key objects
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""
These object and definitions are used throughout the Jupyter Notebook.
"""

# Setup of key Flask object (app)
app = Flask(__name__)
# Setup SQLAlchemy object and properties for the database (db)
database = 'sqlite:///sqlite.db'  # path and filename of databaseapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy()


import json
from sqlalchemy.exc import IntegrityError


class Pizza(db.Model):
    __tablename__ = 'Orders'

    id = db.Column(db.Integer, primary_key=True)
    _orderName = db.Column(db.String(255), unique=False, nullable=False) #_name
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
    def address(self):
        return self._address
    
    @address.setter
    def address(self, address):
        self._address = address
        
    def is_address(self, address):
        return self._address == address
    
    @property
    def pizzaType(self):
        return self._pizzaType
    
    @pizzaType.setter
    def pizzaType(self, pizzaType):
        self._pizzaType = pizzaType
    
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


def initPizzaOrders():
    with app.app_context():
        db.create_all()
        p1 = Pizza(orderName='Apple', pizzaType='Cheese', address='799')
        p2 = Pizza(orderName='Samsung', pizzaType='Cheese', address='799')

        orders = [p1, p2]

        """Builds sample user/note(s) data"""
        for order in orders:
            try:
                existing_order = Pizza.query.filter_by(orderName=order.orderName).first()
                if existing_order:
                    db.session.delete(existing_order)
                    db.session.commit()
                    print(f"Deleted existing order: {existing_order.orderName}")
                new_order = order.create()
                print(f"Created new order: {new_order.orderName}")
            except Exception as e:
                print(f"Failed to create order: {order.orderName}. Error: {str(e)}")

initPizzaOrders()


def find_by_name(orderName):
    with app.app_context():
        name = Pizza.query.filter_by(_orderName=orderName).first()
    return name # returns user object

# def find_by_name(orderName):
#     with app.app_context():
#         name = Pizza.query.filter_by(_orderName=orderName).first()
#     return name # returns user object


# def create():
#     orderName = input("Enter your name: ")
#     order = find_by_name(orderName)
#     try:
#         print("Found\n", order.read())
#         return
#     except:
#         pass # keep going
    
#     pizzaType = input("Enter the pizza type: ")
#     address = input("Enter your address: ")
    
#     # Initialize User object before date
#     phone = Pizza(orderName=orderName, 
#                 pizzaType=pizzaType, 
#                 address=address,
#                 )
    
#     with app.app_context():
#         try:
#             object = phone.create()
#             print("Created\n", object.read())
#         except:  # error raised if object not created
#             print("Unknown error uid {uid}")
        
# create()