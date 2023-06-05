
import json
from flask_sqlalchemy import SQLAlchemy
from __init__ import db, app
from sqlalchemy.exc import IntegrityError

class test(db.Model):
    __tablename__ = 'chess'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _white = db.Column(db.String(255), unique=True, nullable=False)
    _black = db.Column(db.String(255), unique=False, nullable=False)
    _chess_id = db.Column(db.String, unique=False, nullable=False)
    _move = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, white, black, chess_id, move):
        self._white = white
        self._black = black
        self._chess_id = chess_id
        self._move = move

 # a getter method, extracts email from object
    @property
    def white(self):
        return self._white
    
    # a setter function, allows name to be updated after initial object creation
    @white.setter
    def white(self, white):
        self._white = white
        
    # check if uid parameter matches user id in object, return boole
    def is_white(self, white):
        return self._white == white

# a name getter method, extracts name from object
    @property
    def black(self):
        return self._black
    
    # a setter function, allows name to be updated after initial object creation
    @black.setter
    def black(self, black):
        self._black = black
    
    def is_black(self, black):
        return self._black == black

    @property
    def chess_id(self):
        return self._chess_id
    
    # a setter function, allows name to be updated after initial object creation
    @chess_id.setter
    def chess_id(self, chess_id):
        self._chess_id = chess_id

    @property
    def move(self):
        return self._move
    
    # a setter function, allows name to be updated after initial object creation
    @move.setter
    def move(self, move):
        self._move = move



    
 # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
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
            "white": self.white,
            "black": self.black,
            "chess_id": self.chess_id,
            "move": self.move
        }



# CRUD update: updates user name, password, phone
    # returns self
    def update(self, white="", black = "", chess_id = "", move = ""):
        """only updates values with length"""
        if len(white) > 0:
            self.white = white
        if len(black) > 0:
            self.black = black
        if len(chess_id) >= 0:
            self.chess_id = chess_id
        if len(move) >= 0:
            self.move = move
        db.session.commit()
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

def initChess():
    with app.app_context():
        """Create database and tables"""

        db.create_all()
        """Tester data for table"""
        u2 = test(white="Ja", black="Jeong", chess_id="whita", move="w")


        
        try:
            print("hello") 
            u2.create()
            print("Created\n", u2.read())
            print("success")
        except IntegrityError:
            db.session.remove()
            print("error")
            print(f"Records exist, duplicate email, or error: {u2.white} and {u2.black}")
initChess()