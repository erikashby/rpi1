import json, requests
from datetime import datetime
from flask import Flask, request
app = Flask(__name__)

rules = json.load("rules.json")

def quest(event):
    '''
    'name' = 'nodename' << required >>
    'type' = 'node' << required: type of device sending event >>
    'version' = '0.1' << optional: version of aoftware sending event >>
    'source ip' = '192.168.1.204' << optional >>
    'event' = {
        'datetime' = '(datetime)'   << Optiona: The date/time the event was sent.  If no datetime is included the current server datetme will be assume as the event datetime >>
        'type' = 'button'  << Required: Type of event 'button', 'triger' etc.>>
        'ID' = 'id'  << Optional: ID associated with the event >>
        'event' = '(event name)'  << Required: One of the supported events for the specific type >>
        'meta' = {(additional meta data)} << Optional: Additional meta data in json format >>
    }
    status =  << Optional status when event is sent from a node>> 
    {  
        'datetime' = 'datetime',
        'light_status' : [ {'id'= 'led0','state'=0 },{'id'= 'led1','state'=0 }...]
    }
    '''
    print(rules)
    type = event['event']['type']
    eventId = event['event']['ID']
    eventevent = event['event']['event']




@app.route('/')
def hello_world():
    return 'Hello, users!'

@app.route('/event', methods=['PUT'])
def event():
    response = request.json
    quest(response)
    return "200"

@app.route('/testput', methods=["PUT"])
def test_put():
    get_ip = '1'
    get_state = '0'
    action = 'on'
    event = request.json
    for i in event:
        if i == 'source ip':
            get_ip = event[i]
    
    status_url = "http://" + get_ip + ":5000/node/status"
    status = requests.get(status_url).json()

    get_state = status['status']['light_status'][0]['state']

    if get_state == 0:
        action = 'on'
    elif get_state == 1:
        action = 'off'

    toggle_url = "http://" + get_ip + ":5000/node/light?id=led0&action=" + action

    toggle = requests.get(toggle_url)

    return "<h1>TEST<h1>"


@app.route('/testprint', methods=["PUT"])
def test_print():
    response = request.json
    print(response)

    '''
    'name' = 'nodename' << required >>
    'type' = 'node' << required: type of device sending event >>
    'version' = '0.1' << optional: version of aoftware sending event >>
    'source ip' = '192.168.1.204' << optional >>
    'event' = {
        'datetime' = '(datetime)'   << Optiona: The date/time the event was sent.  If no datetime is included the current server datetme will be assume as the event datetime >>
        'type' = 'button'  << Required: Type of event 'button', 'triger' etc.>>
        'ID' = 'id'  << Optional: ID associated with the event >>
        'event' = '(event name)'  << Required: One of the supported events for the specific type >>
        'meta' = {(additional meta data)} << Optional: Additional meta data in json format >>
    }
    status =  << Optional status when event is sent from a node>> 
    {  
        'datetime' = 'datetime',
        'light_status' : [ {'id'= 'led0','state'=0 },{'id'= 'led1','state'=0 }...]
    }
    '''

    print('my name is ' + response['name'])
    print('my type is ' + response['type'])
    print('on version v' + response['version'])
    print('my ip is ' + response['source ip'])
    print('current time in "event": ' + response['event']['datetime'])
    print('my event type is ' + response['event']['type'])
    print('my event ID is ' + response['event']['ID'])
    print('the ' + response['event']['event'] + ' has been made.')
    print('my status datetime is ' + response['status']['datetime'])
    for i in response['status']['light_status']:
        print('id: ' + i['id'] + ' with state ' + str(i['state']))

    
    return "<h1>test<h1>"
