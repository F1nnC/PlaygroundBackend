from flask import Blueprint, jsonify, request, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)

player_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(player_api)

class PlayerAPI(Resource):
    def post(self):
        data = request.json
        player = Player(name=data['name'], level=data['level'])
        db.session.add(player)
        db.session.commit()
        return jsonify({'message': 'Player added successfully.'})

api.add_resource(PlayerAPI, '/leaderboard')

def create_testing_data():
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database: {e}")
            return
        u1 = Player(name='gene', level=2)
        try:
            db.session.add(u1)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(f"Records exist, duplicate email, or error: {u1.id}")

@app.before_first_request
def activate_job():
    create_testing_data()

player_api.register(api)

