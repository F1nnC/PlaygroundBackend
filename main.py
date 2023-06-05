from app import app
import threading

# import "packages" from flask
from flask import render_template

# import "packages" from "this" project
from testusers import createTestingData
from __init__ import db, app
# setup APIs
from server import server
from superCoolFile import pizza_user_api
# setup App pages
from projects.projects import app_projects
from login import NameAPI

from pizzaOrdersFinal import createTestingData2
from songs import song_api
from chess_api import chess_api
# Edwin's Database
from edwin_model import initPhones # CHANGE
from edwin_api import phone_api # CHANGE
from flask import Flask, render_template
from flask_cors import CORS
from pizzamethods import pizza_api_redux
from chess_model import initChess
app.register_blueprint(pizza_api_redux)
app.register_blueprint(pizza_user_api)
# EDWIN
app.register_blueprint(phone_api)
app.register_blueprint(song_api)
app.register_blueprint(server)
app.register_blueprint(app_projects)
app.register_blueprint(NameAPI)
app.register_blueprint(chess_api)
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
    createTestingData2()
    initPhones() # CHANGE
    initChess()
    # createBattleshipTable()

if __name__ == "__main__":
    from flask_cors import CORS
    cors = CORS(app)
    app.run(debug=True, host="0.0.0.0", port=5000)
