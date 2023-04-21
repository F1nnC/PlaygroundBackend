from flask import Blueprint, jsonify, request, Flask, render_template
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

player_leaderboard_api = Blueprint('player_leaderboard_api', __name__, url_prefix='/api')
api = Api(player_leaderboard_api)

class PlayerAPI(Resource):
    def post(self):
        data = request.json
        player = Player(name=data['name'], level=data['level'])
        db.session.add(player)
        db.session.commit()
        return jsonify({'message': 'Player added successfully.'})

api.add_resource(PlayerAPI, '/', endpoint='leaderboard')

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

@app.route('/view-db')
def view_db():
    players = Player.query.all()
    result = []
    for player in players:
        player_data = {'name': player.name, 'level': player.level}
        result.append(player_data)
    return jsonify(result)

app.register_blueprint(player_leaderboard_api, url_prefix='/api')

if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port=5000)

