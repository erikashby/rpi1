import json, requests
from datetime import datetime
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, users!'

@app.route('/testput', methods=["PUT"])
def test_put():
    get_ip = '1'
    get_action = 'on'
    event = request.json
    for i in event:
        if i == 'source ip':
            get_ip = event[i]
    
    status_url = "http://" + get_ip + ":5000/node/status"
    status = requests.get(status_url).json()

    get_action = status['status']['light_status'][0]['state']
    print(get_action)
    send_toggle = "http://" + get_ip + ":5000/node/light?id=led0&action="

    return "<h1>TEST<h1>"

