import json
import os

import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hook():
    data = request.json()
    print(data)
    return "ok", 200


if __name__ == '__main__':
    app.run(port=3000)