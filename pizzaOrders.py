import os
import json
from flask_login import UserMixin
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from __init__ import db, app

class Order(UserMixin, db.Model):
    __tablename__ = 'PizzaOrders'
    id = db.Column(db.Integer, primary_key=True)
    orderName = db.Column(db.String(255), unique=False, nullable=False)
    pizzaType = db.Column(db.String(255), unique=False, nullable=False)
    address = db.Column(db.String(255), unique=False, nullable=False)
    uid = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, orderName="", uid=None, pizzaType="", address=""):
        self.uid = uid if uid is not None else make_id() 
        self.orderName = orderName
        self.pizzaType = pizzaType
        self.address = address


    def __repr__(self):
        return f"Order({self.uid}, {self.orderName}, {self.pizzaType}, {self.address})"

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
            "name": self.orderName,
            "pizzaType": self.pizzaType,
            "address": self.address
        }

    def update(self, orderName="", pizzaType="", address=""):
        if orderName:
            self.orderName = orderName
        if pizzaType:
            self.pizzaType = pizzaType
        if address:
            self.address = address
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def getUser(uid):
    user = Order.query.filter_by(uid=uid).first()
    if user:
        return user
    return "Invalid user"

def getName(orderName):
    user = Order.query.filter_by(orderName=orderName).first()
    if user:
        return user
    return None

def make_id():
    users = Order.query.all()
    uid = 0
    for user in users:
        if user.uid > uid:
            uid = user.uid
    if uid < 100:
        return 100
    return uid + 1

def getType(pizzaType):
    user = Order.query.filter_by(pizzaType=pizzaType).first()
    if user:
        return user
    return None

def getAddress(address):
    user = Order.query.filter_by(address=address).first()
    if user:
        return user
    return None

def createTestingData1():
    with app.app_context():
        db.create_all()
        u1 = Order(orderName="hehehaw", pizzaType="Cheese", address="2305 Nighthawk lane", uid = 2)
        try:
            u1.create()
        except IntegrityError:
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {u1.uid}")

if __name__ == "__main__":
    createTestingData1()
