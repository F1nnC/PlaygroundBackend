from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)

@app.route('/api/leaderboard/', methods=['POST'])
def add_player():
    data = request.json
    player = Player(name=data['name'], level=data['level'])
    db.session.add(player)
    db.session.commit()
    return jsonify({'message': 'Player added successfully.'})


def createTestingData():
    with app.app_context():
        db.init_app(app)
        db.create_all()
        u1 = Player(name='gene', level='2')
        try:
            '''add user/note data to table'''
            u1.create()

        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {u1.uid}")
if __name__ == '__main__':
    app.run()
    createTestingData()