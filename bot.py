import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests
from flask import Flask, request

app = Flask(__name__)

def send_message(msg):
  url  = 'https://api.groupme.com/v3/bo ts/post'

  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  request = requests.post(url, data = data)
  #json = urlopen(request).read().decode()

@app.route('/', methods=['POST'])
def hook():
    data = request.get_json()
      # We don't want to reply to ourselves!
    if data['name'] != 'Yelp':
        msg = '{}, you sent "{}".'.format(data['name'], data['text'])
        send_message(msg)

    return "ok", 200
