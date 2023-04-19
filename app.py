from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Player %r>' % self.name


@app.route('/api/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    if request.method == 'POST':
        data = request.json
        name = data['name']
        level = data['level']

        player = Player(name=name, level=level)
        db.session.add(player)
        db.session.commit()

        return jsonify({'message': 'Player added successfully!'})

    elif request.method == 'GET':
        players = Player.query.all()
        result = []
        for player in players:
            player_data = {}
            player_data['name'] = player.name
            player_data['level'] = player.level
            result.append(player_data)

        return jsonify(result)

@app.route('/api/leaderboard', methods=['POST'])
def add_player():
    data = request.json
    player = Player(name=data['name'])
    db.session.add(player)
    db.session.commit()
    return jsonify({'message': 'Player added to leaderboard.'}), 201
@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    players = Player.query.order_by(Player.id).all()
    leaderboard = [{'name': player.name, 'level': player.level} for player in players]
    return jsonify(leaderboard), 200

if __name__ == '__main__':
    app.run(debug=True)

