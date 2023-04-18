from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'https://playgroundproject.duckdns.org/'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User(name='{self.name}', level={self.level})"

with app.app_context():
    db.create_all()

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    level = request.form.get('level')
    if name and level:
        user = User(name=name, level=level)
        db.session.add(user)
        db.session.commit()
        return "User added to leaderboard."
    else:
        return "Invalid input. Please provide both name and level."


if __name__ == '__main__':
    app.run()

@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.level.desc()).all()
    return render_template('leaderboard.html', users=users)
