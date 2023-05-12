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

class Order(db.Model):
    __tablename__ = 'PizzaOrders'

    id = db.Column(db.Integer, primary_key=True)
    _orderName = db.Column(db.String(255), unique=False, nullable=False) #_name
    _pizzaType = db.Column(db.String(255), unique=False, nullable=False) #_type
    _address = db.Column(db.String(255), unique=False, nullable=False) # _address
    def __init__(self, orderName, pizzaType, address):
        self._orderName = orderName
        self._pizzaType = pizzaType
        self._address = address

    @property
    def orderName(self):
        return self._orderName
    
    @orderName.setter
    def orderName(self, orderName):
        self.orderName = orderName
    
    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, address):
        self._address = address

    def is_address(self, address):
        return self._address == address
    
    @property
    def pizzaPrice(self):
        return self._pizzaPrice
    
    @pizzaType.setter
    def pizzaType(self, pizzaType):
        self._pizzaType = pizzaType
        
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
            "orderName": self.orderName,
            "pizzaType": self.pizzaType,
            "address": self.address,
        }

    def update(self, orderName="", pizzaType="", address=""):
        """only updates values with length"""
        if len(orderName) > 0:
            self.pizza = orderName
        if len(pizzaType) > 0:
            self.pizzaType = pizzaType
        if len(address) > 0:
            self.address = address
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
        p1 = Order(orderName='Joe', pizzaType='cheese', address='1313 Disneyland Dr, Anaheim, CA 92802')
        p2 = Order(orderName='Bill', pizzaType='pepperoni', address='1600 Pennsylvania Avenue NW, Washington, DC 20500')


        orders = [p1, p2]

        for item in Orders:
            try:
                object = item.create()
                print(f"Created new uid {object.order}")
            except:  # error raised if object nit created
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {item.order}, or error.")
                
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
    cursor.execute('''CREATE TABLE PizzaOrders(
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