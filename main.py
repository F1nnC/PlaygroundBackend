from app import Player, player_leaderboard_api, app
from flask import render_template
from app import db


# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)




@app.errorhandler(404)  
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  
def index():
    return render_template("index.html")

@app.route('/stub/') 
def stub():
    return render_template("stub.html")


if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port=5000)

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)
