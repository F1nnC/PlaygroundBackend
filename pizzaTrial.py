from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
database = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy()
db.init_app(app)


import datetime
from datetime import datetime
import json

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class Pizza(db.Model):
    __tablename__ = 'PizzaMenus'

    id = db.Column(db.Integer, primary_key=True)
    _pizza = db.Column(db.String(255), unique=False, nullable=False) #_name
    _pizzaPrice = db.Column(db.String(255), unique=True, nullable=False) #_uid
    _pizzaSize = db.Column(db.String(255), unique=False, nullable=False) # _password
    def __init__(self, pizza, pizzaPrice, pizzaSize):
        self._pizza = pizza
        self._pizzaPrice= pizzaPrice
        self._pizzaSize = pizzaSize

    @property
    def pizza(self):
        return self._pizza
    
    @pizza.setter
    def pizza(self, pizza):
        self._pizza = pizza
    
    @property
    def pizzaSize(self):
        return self._pizzaSize
    
    @pizzaSize.setter
    def pizzaSize(self, pizzaSize):
        self._pizzaSize = pizzaSize

    def is_pizzaSize(self, pizzaSize):
        return self._pizzaSize == pizzaSize
    
    @property
    def pizzaPrice(self):
        return self._pizzaPrice
    
    @pizzaPrice.setter
    def price(self, pizzaPrice):
        self._pizzaPrice = pizzaPrice
        
    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()  
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "pizza": self.pizza,
            "pizzaPrice": self.pizzaPrice,
            "pizzaSize": self.pizzaSize,
        }

    def update(self, pizza="", pizzaPrice="", pizzaSize=""):
        """only updates values with length"""
        if len(pizza) > 0:
            self.pizza = pizza
        if len(pizzaPrice) > 0:
            self.pizzaPrice = pizzaPrice
        if len(pizzaSize) > 0:
            self.pizzaSize = pizzaSize
        db.session.commit()
        db.session.add(self)
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
def initPizzas():
    with app.app_context():
        db.create_all()
        p1 = Pizza(pizza='Cheese', pizzaPrice='10.99', pizzaSize='Small')
        p2 = Pizza(pizza='Cheese', pizzaPrice='12.99', pizzaSize='Medium')
        p3 = Pizza(pizza='Cheese', pizzaPrice='14.99', pizzaSize='Large')
        p4 = Pizza(pizza='Pepperoni', pizzaPrice='10.99', pizzaSize='Small')
        p5 = Pizza(pizza='Pepperoni', pizzaPrice='12.99', pizzaSize='Medium')
        p6 = Pizza(pizza='Pepperoni', pizzaPrice='14.99', pizzaSize='Large')
        p7 = Pizza(pizza='Barbecue', pizzaPrice='10.99', pizzaSize='Small')
        p8 = Pizza(pizza='Barbecue', pizzaPrice='12.99', pizzaSize='Medium')
        p9 = Pizza(pizza='Barbecue', pizzaPrice='14.99', pizzaSize='Large')
        p10 = Pizza(pizza='Vegetarian', pizzaPrice='10.99', pizzaSize='Small')
        p11 = Pizza(pizza='Vegetarian', pizzaPrice='12.99', pizzaSize='Medium')
        p12 = Pizza(pizza='Vegetarian', pizzaPrice='14.99', pizzaSize='Large')
        p13 = Pizza(pizza='Hawaiian', pizzaPrice='10.99', pizzaSize='Small')
        p14 = Pizza(pizza='Hawaiian', pizzaPrice='12.99', pizzaSize='Medium')
        p15 = Pizza(pizza='Hawaiian', pizzaPrice='14.99', pizzaSize='Large')

        pizzas = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15]

        for item in pizzas:
            try:
                object = item.create()
                print(f"Created new uid {object.pizza}")
            except:  # error raised if object nit created
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {item.pizza}, or error.")
                
initPizzas()