import requests

url = "https://spotify81.p.rapidapi.com/top_200_tracks"

headers = {
	"X-RapidAPI-Key": "56cf0d9c39msh90ab47fd56c02e6p1d2792jsn0f4dfaa46b90",
	"X-RapidAPI-Host": "spotify81.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
response = response.json()
from contextlib import nullcontext
from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import requests  # used for testing 
import time

# Blueprints enable python code to be organized in multiple files and directories https://flask.palletsprojects.com/en/2.2.x/blueprints/
song_api = Blueprint('song_api', __name__,
                   url_prefix='/api/songs')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(song_api)

"""Time Keeper
Returns:
    Boolean: is it time to update?
"""
def updateTime():
    global last_run  # the last_run global is preserved between calls to function
    try: last_run
    except: last_run = None
    
    # initialize last_run data
    if last_run is None:
        last_run = time.time()
        return True
    
    # calculate time since last update
    elapsed = time.time() - last_run
    if elapsed > 86400:  # update every 24 hours
        last_run = time.time()
        return True
    
    return False
def getSongsAPI():
    global songs_data  # the covid_data global is preserved between calls to function
    try: songs_data
    except: songs_data = None

    """
    Preserve Service usage / speed time with a Reasonable refresh delay
    """
    if updateTime(): # request Covid data
        """
        RapidAPI is the world's largest API Marketplace. 
        Developers use Rapid API to discover and connect to thousands of APIs. 
        """
        url = "https://spotify81.p.rapidapi.com/top_200_tracks"

        headers = {
            "X-RapidAPI-Key": "56cf0d9c39msh90ab47fd56c02e6p1d2792jsn0f4dfaa46b90",
            "X-RapidAPI-Host": "spotify81.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        songs_data = response
    else:  # Request Covid Data
        response = songs_data

    return response


"""API with Country Filter
Returns:
    String: Filter of API response
"""   
def getSpotify(filter):
    # Request Covid Data
    response = getSongsAPI()
    # Look for Country    
    songs = response.json().get()
    for country in songs:  # countries is a list
        if country[""].lower() == filter.lower():  # this filters for country
            return country
    
    return {"message": filter + " not found"}


"""Defines API Resources 
  URLs are defined with api.add_resource
"""   
class CovidAPI:
    """API Method to GET all Covid Data"""
    class _Read(Resource):
        def get(self):
            return getSongsAPI().json()
        
    """API Method to GET Covid Data for a Specific Country"""
    class _ReadSongs(Resource):
        def get(self, filter):
            return jsonify(getSpotify(filter))
    
    # resource is called an endpoint: base usr + prefix + endpoint
    api.add_resource(_Read, '/')
    api.add_resource(_ReadSongs, '/<string:filter>')


"""Main or Tester Condition 
  This code only runs when this file is "played" directly
"""        
if __name__ == "__main__": 
    """
    Using this test code is how I built the backend logic around this API.  
    There were at least 10 debugging session, on handling updateTime.
    """
    
    print("-"*30) # cosmetic separator

    # This code looks for "world data"
    response = getSongsAPI()
    world = response.json().get()  # turn response to json() so we can extract "world_total"
    for key, value in world.items():  # this finds key, value pairs in country
        print(key, value)

    print("-"*30)

  
