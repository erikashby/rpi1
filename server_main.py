import json
from datetime import datetime
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, users!'

@app.route('/testput', methods=["PUT"])
def test_put():
    event = request.json
    print("got req")
    return "<h1>TEST<h1>"
