import os
import json
from flask_login import UserMixin
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from __init__ import db, app

class Menu(UserMixin, db.Model):
    __tablename__ = 'PizzaMenu'
    id = db.Column(db.Integer, primary_key=True)
    pizza = db.Column(db.String(255), unique=False, nullable=False)
    price = db.Column(db.String(255), unique=False, nullable=False)
    size = db.Column(db.String(255), unique=False, nullable=False)
    uid = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, pizza="", uid=None, price="", size=""):
        self.uid = uid if uid is not None else make_id() 
        self.pizza = pizza
        self.price = price
        self.size = size


    def __repr__(self):
        return f"Menu({self.uid}, {self.pizza}, {self.price}, {self.size})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        return {
            "uid": self.uid,
            "pizza": self.pizza,
            "price": self.price,
            "size": self.size
        }

    def update(self, pizza="", price="", size=""):
        if pizza:
            self.pizza = pizza
        if price:
            self.price = price
        if size:
            self.size = size
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def getUser(uid):
    user = Menu.query.filter_by(uid=uid).first()
    if user:
        return user
    return "Invalid user"

def getName(pizza):
    user = Menu.query.filter_by(pizza=pizza).first()
    if user:
        return user
    return None

def make_id():
    users = Menu.query.all()
    uid = 0
    for user in users:
        if user.uid > uid:
            uid = user.uid
    if uid < 100:
        return 100
    return uid + 1

def getPrice(price):
    user = Menu.query.filter_by(price=price).first()
    if user:
        return user
    return None

def getSize(size):
    user = Menu.query.filter_by(size=size).first()
    if user:
        return user
    return None

def CreateMenuData():
    with app.app_context():
        db.create_all()
        u1 = Menu(pizza="cheese", price="10.99", size="medium", uid = 2)
        try:
            u1.create()
        except IntegrityError:
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {u1.uid}")

if __name__ == "__main__":
    CreateMenuData()
