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
        return self.stock
    
    @pizzaPrice.setter
        def pizzaPrice(self, pizzaPrice):
        self.pizzaPrice = pizzaPrice
    

    def __str__(self):
        return json.dumps(self,read())
    
    def create(self):
        try:
            db.session.ass(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
    def read(self):
        return {
            "pizza": self.pizza,
            "pizzaPrice": self.pizzaPrice,
        }
    def update(self, pizza="", pizzaPrice=""):
        