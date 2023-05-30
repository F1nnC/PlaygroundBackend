from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
import json
from sqlalchemy.exc import IntegrityError

"""
These object and definitions are used throughout the Jupyter Notebook.
"""

app = Flask(__name__)
database = 'sqlite:///sqlite.db'  # path and filename of databaseapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = 'SECRET_KEY'
db = SQLAlchemy()


db.init_app(app)

''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into a Python shell and follow along '''
class Phone(db.Model):
    __tablename__ = 'Phones'  # table name is plural, class name is singular

    id = db.Column(db.Integer, primary_key=True)
    _company = db.Column(db.String(255), unique=False, nullable=False) #_name
    _model = db.Column(db.String(255), unique=True, nullable=False) #_uid
    _price = db.Column(db.String(255), unique=False, nullable=False) # _password
    _dob = db.Column(db.Date) #_dob

    def __init__(self, company, model, price, dob=datetime.today()):
        self._company = company
        self._model = model
        self._price = price

    @property
    def company(self):
        return self._company
    
    @company.setter
    def company(self, company):
        self._company = company
    
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, model):
        self._model = model
        
    def is_model(self, model):
        return self._model == model
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        self._price = price
    
    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "company": self.company,
            "model": self.model,
            "price": self.price,
        }

    def update(self, company="", model="", price=""):
        """only updates values with length"""
        if len(company) > 0:
            self.company = company
        if len(model) > 0:
            self.model = model
        if len(price) > 0:
            self.price = price
        db.session.commit()
        db.session.add(self)
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def initPhones():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        p1 = Phone(company='Apple', model='iPhone 14', price='799')
        p2 = Phone(company='Apple', model='iPhone 14 Pro', price='999')
        p3 = Phone(company='Samsung', model='Galaxy S23', price='799')
        p4 = Phone(company='LG', model='Wing', price='999')
        p5 = Phone(company='Motorola', model='Razr', price='1399')
        p6 = Phone(company='Google', model='Pixel 7', price='599')

        phones = [p1, p2, p3, p4, p5, p6]

        """Builds sample user/note(s) data"""
        for phone in phones:
            try:
                '''add user to table'''
                object = phone.create()
                print(f"Created new uid {object.model}")
            except:
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {phone.model}, or error.")
                
initPhones()

def find_by_company(company):
    with app.app_context():
        name = Phone.query.filter_by(_company=company).first()
    return name

def create():
    phone = input("Enter the Phone: ")
    company = input("Enter the manufacturer: ")
    price = input("Enter the Price: ")

    phone = Phone(phone=phone, 
                company=company, 
                price=price,
                )
        
    with app.app_context():
            try:
                object = phone.create()
                print("Created\n", object.read())
            except:
                print("Unknown error uid {uid}")

def read():
    with app.app_context():
        table = Phone.query.all()
    json_ready = [phone.read() for phone in table]
    return json_ready

# def delete_by_phone():
#     orderName = input("Enter uid of user to be deleted ")
#     user = find_by_company(orderName)
#     with app.app_context():
#         try:
#             object = user.delete() 
#             print(f"User with uid {orderName} has been deleted")
#         except:
#            (f"No user with uid {orderName} was found")
        
# delete_by_phone()