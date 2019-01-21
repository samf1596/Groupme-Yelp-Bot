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
          'text'   : str(msg),
         }
  requests.post(url, data = data)

def get_rec(term=None, location=None, data=None):
    header = {"Authorization": "Bearer "+ os.getenv("YELP_KEY")}
    params = {
        "term":term,
        "location":location
    }
    return requests.get(url='https://api.yelp.com/v3/businesses/search', params=params, headers=header)

def get_message():
    params = {
        "limit":1,
        "token":os.getenv('GROUPME_TOKEN'),
    }
    res = requests.get(url='https://api.groupme.com/v3/groups/42030640/messages', params=params)
    print(res.json())
    return res

@app.route('/', methods=['POST'])
def hook():
    data = request.get_json()

    if data['name'] != 'Yelp' and ("hello" in data['text'].lower() or "hi" in data['text'].lower() or "yo" in data['text'].lower()):
        msg = "Hello, " + data['name'] + ". What would you like to search for? Food? Activities?"
        send_message(msg)

    if data['name'] != 'Yelp' and ("food" in data['text'].lower()):
        send_message("Where would like like to search for food? (city/zip/state/combo)")
        bot = True
        print(bot==True)
        print("in food")
        while bot==True:
            res = get_message().json()
            location = res["response"]["messages"][0]["text"]
            print("in loop")
            if res["response"]["messages"][0]["name"] != "Yelp":
                bot = False

        rec = get_rec(term="food", location=location).json()
        print(rec)
        count = 0
        for i in rec['businesses']:
            send_message("\nName: " + str(i['name']) + "\nPrice: " + str(i['price']) + "\nPhone: " + str(i['phone']) + "\n")
            count = count + 1
            if count >= 5:
                break

    return "ok", 200
