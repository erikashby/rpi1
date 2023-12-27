import json
from datetime import datetime
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, users!'

@app.route('/testput', methods=["PUT"])
def test_put():
    get_ip = '1'
    get_action = 'toggle'
    event = request.json
    for i in event:
        if i == 'source ip':
            get_ip = event[i]
        if i == 'action':
            get_action = event[i]
    
    print("source ip = " + get_ip)

    send_toggle = "http://" + get_ip + ":5000/node/light?id=led0&action=" + get_action

    return "<h1>TEST<h1>"

