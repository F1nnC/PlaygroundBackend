from app import Player, player_leaderboard_api, app
import threading

# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries

# import "packages" from "this" project
from __init__ import app 
from testusers import createTestingData

# setup APIs
from server import server
from testApi import server2
from superCoolFile import pizza_user_api
# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition
from login import NameAPI
from pizzatestcode import pizza_api
from testusers import db
# register URIs

app.register_blueprint(pizza_api)
app.register_blueprint(pizza_user_api)
app.register_blueprint(server)
app.register_blueprint(server2)
app.register_blueprint(app_projects) # register app pages
app.register_blueprint(NameAPI)


@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/stub/')  # connects /stub/ URL to stub() function
def stub():
    return render_template("stub.html")

@app.before_first_request
def activate_job():
    createTestingData()
    # createBattleshipTable()


if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port=8095)

# Initialize the SQLAlchemy object to work with the Flask app instance

