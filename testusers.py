from flask_login import UserMixin
from flask import Blueprint, request, jsonify
import os, json
from __init__ import db, app
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class PizzaUsers(UserMixin, db.Model):
    __tablename__ = 'chess_users'
    
    # Define the Users schema
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    score = db.Column(db.String(255), unique=True, nullable=False)
    games = db.Column(db.String(255), unique = False, nullable=False)
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    # notes = db.relationship("Notes", cascade='all, delete', backref='users', lazy=True)


    def __init__(self, name='', uid="0", password="null", dob="11-11-1111", games=""):
        self.uid = make_id()
        self.name = name
        self.dob = dob
        self.games = ""
        self.set_password(password)
        
    def __repr__(self):
        return "Users(" + str(self.uid) + "," + self.name + "," + str(self.dob) +  str(self.games) + ")"


    def create(self):
        try:
            db.session.add(self)  
            db.session.commit()  
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def update(self, name="", uid="", password="", dob=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if len(dob) > 0:
            self.dob = dob
        db.session.commit()
        return self


def make_id():
    users = PizzaUsers.query.all()
    uid = 0
    for user in users:
        if(user.get_id() > uid):
            uid = user.get_id()
    if (uid < 100):
        return 100
    return uid + 1


def getUser(uid):
    users = PizzaUsers.query.all()
    for user in users:
        if(user.get_id() == uid):
            return user
    else:
        return "Invalid user"

def createTestingData():
    with app.app_context():
        db.init_app(app)
        db.create_all()
        u1 = PizzaUsers(name='F1nnc', password="123", uid="12")
        u2 = PizzaUsers(name='Gene', password="123", uid="123")
        try:
            '''add user/note data to table'''
            u1.create()
            u2.create()
            #u5.create()
            #u6.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {u1.uid}")



if __name__ == "__main__":
    createTestingData()