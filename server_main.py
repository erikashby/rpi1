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
    event = request.json
    for i in event:
        if i == 'source ip':
            get_ip = event[i]
    
    return "<h1>TEST<h1>"
