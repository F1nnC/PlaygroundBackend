from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    players = Player.query.order_by(Player.id).all()
    leaderboard = []
    for player in players:
        leaderboard.append({'id': player.id, 'name': player.name, 'level': player.level})
    return jsonify({'leaderboard': leaderboard})

@app.route('/api/leaderboard', methods=['POST'])
def add_player():
    player_data = request.get_json()
    new_player = Player(name=player_data['name'], level=player_data['level'])
    db.session.add(new_player)
    db.session.commit()
    return 'Player added to the leaderboard'
