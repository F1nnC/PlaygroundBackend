from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
import os
if not os.path.exists('sqlite.db'):
    open('sqlite.db', 'w').close()

database = 'sqlite:///sqlite.db'
database2 = 'instance/sqlite.db'
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
    _pizzaPrice = db.Column(db.String(255), unique=False, nullable=False) #_uid
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

import sqlite3

def schema():
    # Connecting to the database
    conn = sqlite3.connect(database2)

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Dropping PizzaMenus table if already exists.
    cursor.execute("DROP TABLE IF EXISTS PizzaMenus")

    # Creating table
    cursor.execute('''CREATE TABLE PizzaMenus(
                      pizza TEXT NOT NULL,
                      pizzaPrice REAL NOT NULL,
                      pizzaSize TEXT NOT NULL)''')

    # Commit the changes
    conn.commit()

    # Close the database connection
    conn.close()


    #"Records inserted...""
schema()

#CREATE
import sqlite3

def create():
    pizza = input("Enter your pizza name:")
    pizzaPrice = input("Enter your pizzaPrice:")
    pizzaSize = input("Enter your pizzaSize:")
    
    # Connect to the database file
    conn = sqlite3.connect(database2)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    try:
        # Execute an SQL command to insert data into a table
        cursor.execute("INSERT INTO PizzaMenus (PIZZA, PIZZAPRICE, pizzaSize) VALUES (?, ?, ?)", (pizza, pizzaPrice, pizzaSize))
        
        # Commit the changes to the database
        conn.commit()
        print(f"A new user record {pizzaPrice} has been created")
                
    except sqlite3.Error as error:
        print("Error while executing the INSERT:", error)


    # Close the cursor and connection objects
    cursor.close()
    conn.close()


#READ
import sqlite3

def read():
    # Connect to the database file
    conn = sqlite3.connect(database2)

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    
    # Execute a SELECT statement to retrieve data from a table
    results = cursor.execute('SELECT * FROM PizzaMenus').fetchall()

    # Print the results
    if len(results) == 0:
        print("Table is empty")
    else:
        for row in results:
            print(row)

    # Close the cursor and connection objects
    cursor.close()
    conn.close()
    
read()

def update():
    pizzaPrice = input("Enter pizzaPrice to update")
    pizzaSize = input("Enter updated pizzaSize")
    if len(pizzaSize) < 2:
        message = "Playground"
        pizzaSize = 'playground'
    else:
        message = "successfully updated"

    # Connect to the database file
    conn = sqlite3.connect(database2)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    try:
        # Execute an SQL command to update data in a table
        cursor.execute("UPDATE PizzaMenus SET pizzaSize = ? WHERE pizzaPrice = ?", (pizzaSize, pizzaPrice))
        if cursor.rowcount == 0:
            # The pizzaPrice was not found in the table
            print(f"No pizzaPrice {pizzaPrice} was not found in the playground table")
        else:
            print(f"The row with pizzaPrice {pizzaPrice} the pizzaSize has been {message}")
            conn.commit()                                                   
    except sqlite3.Error as error:
        print("Error while executing the UPDATE:", error)
        
    
    # Close the cursor and connection objects
    cursor.close()
    conn.close()

import sqlite3

#DELETE
def delete():
    pizzaPrice = input("Enter pizzaPrice to delete")

    # Connect to the database file
    conn = sqlite3.connect(database2)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM PizzaMenus WHERE pizzaPrice = ?", (pizzaPrice,))
        # get the number of rows affected.
        cursor.execute("SELECT changes()").fetchone()[0]
        
        conn.commit()
    except sqlite3.Error as error:
        print("Error while executing the DELETE:", error)
        
    # Close the cursor and connection objects
    cursor.close()
    conn.close()

def menu():
    print()
    operation = input("Enter: (C)reate (R)ead (U)pdate or (D)elete or (S)chema")
    if operation.lower() == 'c':
        create()
    elif operation.lower() == 'r':
        read()
    elif operation.lower() == 'u':
        update()
    elif operation.lower() == 'd':
        delete()
    elif operation.lower() == 's':
        schema()
    elif len(operation)==0: # Escape Key
        return
    else:
        print("Please enter c, r, u, or d") 
    menu() # recursion, repeat menu
        
try:
    menu() # start menu
except:
    print("Perform Jupyter 'Run All' prior to starting menu")