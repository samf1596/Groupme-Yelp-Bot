import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests
from flask import Flask, request

app = Flask(__name__)

def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post'

  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  requests.post(url, data = data)
  #json = urlopen(request).read().decode()

def get_rec(msg, data):
    header = {"Authorizaion": "Bearer "+ os.getenv("YELP_KEY")}
    params = {
        "term":"food",
        "latitude": data["lat"],
        "longitude": data["lng"]
    }
    return requests.get(url='https://api.yelp.com/v3/businesses/search', params=params, header=header)


@app.route('/', methods=['POST'])
def hook():
    data = request.get_json()
    # We don't want to reply to ourselves!
    #print(data)
    #recs = get_rec(data["text"], data)
    #print(recs["businesses"])

    if data['name'] != 'Yelp' and ("hello" in data['text'].lower() or "hi" in data['text'].lower() or "yo" in data['text'].lower()):
        msg = "Hello, " + data['name'] + ". What would you like to search for? Food? Activities?"
        send_message(msg)

    return "ok", 200
