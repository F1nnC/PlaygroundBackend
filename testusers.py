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
    score = db.Column(db.Integer, nullable=False)
    games = db.Column(db.String(255), unique = False, nullable=False)


    def __init__(self, name='', uid="0", score=0):
        self.uid = make_id()
        self.name = name
        self.games = ""

    def __repr__(self):
        return "Users(" + str(self.uid) + "," + self.name + "," + self.score +  str(self.games) + ")"


    def create(self):
        try:
            db.session.add(self)  
            db.session.commit()  
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def update(self, name="", uid="", score = ""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(score) > 0:
            self.score = score
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

def getScore(score):
    users = PizzaUsers.query.all() 
    score = 0 
    for user in users: 
        if(user.get_id() == score):
            return score


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
        u1 = PizzaUsers(name='F1nnc', uid="12", score = "10")
        u2 = PizzaUsers(name='Gene', uid="123", score = "5" )
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

def win(uid):
    user = PizzaUsers.query.filter_by(uid=uid).first()
    if user:
        user.score += 1
        db.session.commit()
    else:
        print("Invalid user")


if __name__ == "__main__":
    createTestingData()