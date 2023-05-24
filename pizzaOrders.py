import os, json
from __init__ import db, app
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from flask import Blueprint, request, jsonify
from flask import jsonify

class Order(UserMixin, db.Model):
    __tablename__ = 'PizzaOrders'
    id = db.Column(db.Integer, primary_key=True)
    _orderName = db.Column(db.String(255), unique=False, nullable=False)
    _pizzaType = db.Column(db.String(255), unique=False, nullable=False)
    _address = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, orderName="", uid="0", pizzaType="", address=""):
        self._uid = uid
        self._orderName = orderName
        self._pizzaType = pizzaType
        self._address = address

    def __repr__(self):
        return f"Order({self._uid}, {self._orderName}, {self._pizzaType}, {self._address})"

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
            "uid": self._uid,
            "name": self._orderName,
            "pizzaType": self._pizzaType,
            "address": self._address
        }

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

    def update(self, orderName="", pizzaType="", address=""):
        if orderName:
            self._orderName = orderName
        if pizzaType:
            self._pizzaType = pizzaType
        if address:
            self._address = address
        db.session.commit()
        db.session.add(self)
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    def get_id(self):
        return self._uid

    def get_name(self):
        return self._orderName

    def get_type(self):
        return self._pizzaType

    def get_address(self):
        return self._address


def getUser(uid):
    users = Order.query.all()
    for user in users:
        if user.get_id() == uid:
            return user
    return "Invalid user"


def getName(orderName):
    users = Order.query.all()
    for user in users:
        if user.get_name() == orderName:
            return user
    return None


def make_id():
    users = Order.query.all()
    uid = 0
    for user in users:
        if user.get_id() > uid:
            uid = user.get_id()
    if uid < 100:
        return 100
    return uid + 1

def getType(pizzaType):
    users = Order.query.all()
    for user in users:
        if(user.get_type() == pizzaType):
            return user
    else: 
        return None


def getAddress(address):
    users = Order.query.all()
    for user in users:
        if(user.get_address() == address):
            return user
    else: 
        return None

def createTestingData1():
    with app.app_context():
        db.create_all()
        u1 = Order(orderName ="Balls", uid="100", pizzaType = "Cheese", address = "2305 Nighthawk lane")  
        try:
            '''add user/note data to table'''
            u1.create()
            # u5.create()
            # u6.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {u1.uid}")



if __name__ == "__main__":
    createTestingData1()
