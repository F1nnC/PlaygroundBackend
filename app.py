from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)

@app.route('/api/leaderboard', methods=['POST'])
def add_player():
    data = request.json
    player = Player(name=data['name'], level=data['level'])
    db.session.add(player)
    db.session.commit()
    return jsonify({'message': 'Player added successfully.'})

if __name__ == '__main__':
    app.run()

