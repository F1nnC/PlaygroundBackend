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