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
class Pizza(db.Model):
    __tablename__ = 'Pizzas'  # table name is plural, class name is singular

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=True, nullable=False) #_name
    _pizza = db.Column(db.String(255), unique=False, nullable=False) #_uid
    _size = db.Column(db.String(255), unique=False, nullable=False) # _password
    _price = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, name, pizza, size, price):
        self._name = name
        self._pizza = pizza
        self._size = size
        self._price = price

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    def is_name(self, name):
        return self._name == name
    
    @property
    def pizza(self):
        return self._pizza
    
    @pizza.setter
    def pizza(self, pizza):
        self._pizza = pizza
    
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        self._size = size

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        self._price = price
    
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
            "name": self.name,
            "pizza": self.pizza,
            "size": self.size,
            "price": self.price
        }

    def update(self, name="", pizza="", size="", price=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(pizza) > 0:
            self.pizza = pizza
        if len(size) > 0:
            self.size = size
        if len(price) > 0:
            self.price = price
        db.session.commit()
        db.session.add(self)
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def initPizzas():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        p1 = Pizza(name='Luka', pizza='Cheese', size='Small', price='9.99')
        p2 = Pizza(name='James', pizza='Cheese', size='Medium', price='11.99')
        p3 = Pizza(name='Finn', pizza='Cheese', size='Large', price='13.99')
        p4 = Pizza(name='Edwin', pizza='Pepperoni', size='Small', price='9.99')
        p5 = Pizza(name='Gene', pizza='Pepperoni', size='Medium', price='11.99')
        p6 = Pizza(name='Kush', pizza='Pepperoni', size='Large', price='13.99')
        p7 = Pizza(name='Zeen', pizza='Vegetarian', size='Large', price='13.99')


        pizzas = [p1, p2, p3, p4, p5, p6, p7]

        """Builds sample user/note(s) data"""
        for pizza in pizzas:
            try:
                '''add user to table'''
                object = pizza.create()
                print(f"Created new uid {object.name}")
            except:
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {pizza.name}, or error.")
                
initPizzas()

def find_by_name(name):
    with app.app_context():
        order = Pizza.query.filter_by(_name=name).first()
    return order

def create():
    name = input("Enter the name of the person who made this pizza: ")
    pizza = input("Enter the pizza: ")
    size = input("Enter the price of the pizza: ")
    price = input("Enter the price of this pizza: ")

    order = Pizza(name=name, 
                pizza=pizza, 
                size=size,
                price=price
                )
        
    with app.app_context():
            try:
                object = order.create()
                print("Created\n", object.read())
            except:
                print("Unknown error uid {uid}")

def read():
    with app.app_context():
        table = Pizza.query.all()
    json_ready = [order.read() for order in table]
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