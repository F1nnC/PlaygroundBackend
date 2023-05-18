from app import Player, player_leaderboard_api, app
import threading

# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries

# import "packages" from "this" project
from __init__ import app  # Definitions initialization
from model_chess import createTestingData

# setup APIs

from superCoolFile import pizza_user_api
# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition
from login import NameAPI
from testusers import createTestingData
from testusers import db
# register URIs


app.register_blueprint(pizza_user_api)
app.register_blueprint()
app.register_blueprint(app_projects) # register app pages
app.register_blueprint(NameAPI)


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
