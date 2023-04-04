from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError



class Pizzas(db.Model):
    __tablename__ = 'pizzas' # table plural

    id = db.Column(db.Integer, primary_key=True)
    pizza = db.column(db.String(255), unique=False, nullable=False)
    pizzaPrice = db.column(db.string(255), unique=False, nullable=False)
    pizzaSize = db.column(db.string(255), unique=False, nullable=False)


    def __init__(self, pizza, pizzaPrice):

        self.pizza = pizza
        self.pizzaPrice = pizzaPrice


    @property
    def pizza(self):
        return self.pizza
    
    @pizza.setter
    def pizza(self, pizza):
        self.pizza = pizza

    
    @property
    def pizzaPrice(self):
        return self.pizzaPrice
    
    @pizzaPrice.setter
    def pizzaPrice(self, pizzaPrice):
            self.pizzaPrice = pizzaPrice
    
    @property
    def pizzaSize(self):
        return self.pizzaSize
    
    @pizzaSize.setter
    def pizzaSize(self, pizzaSize):
        self.pizzasize = pizzaSize
    

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
            "pizza": self.pizza,
            "pizzaPrice": self.pizzaPrice,
            "pizzaSize": self.pizzaSize
        }
    def update(self, pizza="", pizzaPrice="", pizzaSize=""):
       """only updates values with length"""
       if len(pizza) > 2:
           self.pizza = pizza
       if len(pizzaPrice) > 0:
           self.pizzaPrice = pizzaPrice
       if len(pizzaSize) > 0:
           self.pizzaSize = pizzaSize
       db.session.commit()
       return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    # end of crud

def initPizzas():
    with app.app_context():
        db.create_all()

        # Test data
        u1 = Pizzas(pizza='Cheese pizza', pizzaPrice='14.99', pizzaSize='Large')
        u2 = Pizzas(pizza='Cheese pizza', pizzaPrice='12.99', pizzaSize='Medium')
        u3 = Pizzas(pizza='Cheese pizza', pizzaPrice='10.99', pizzaSize='Small')
        

pizza = [u1, u2, u3]

for pizza in Pizzas:
    try:
        pizza.create()
    except IntegrityError:
        db.session.remove()
        print(f"This is a duplicate")