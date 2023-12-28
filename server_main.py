import json, requests
from datetime import datetime
from flask import Flask, request
app = Flask(__name__)

get_rules = open("rules.json")
rules = json.load(get_rules)
get_rules.close()

zero1url = "http://192.168.1.204:5000"
zero2url = "http://192.168.1.170:5000"

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

def quest(event):
    # Each event name, type, id, and event
    print(event)
    eventname = event['name']
    eventtype = event['event']['type']
    eventId = event['event']['ID']
    eventevent = event['event']['event']
    action = None

    # Loop rule array
    # inside rule loop, check each trigger
    # if event match trigger, loop through condition
    # if true, trueaction, if false false action

    for rule in rules["rule"]:
        print(rule["name"])
        #print(str(rule["trigger"]["from"]) + "\n\n")
        if rule["trigger"]["from"] == eventname and rule["trigger"]["type"] == eventtype and rule["trigger"]["event"] == eventevent and rule["trigger"]["id"] == eventId:
            print("triggered!!!\n")
            for c in rule["conditions"]:
                if check_cond(c):
                    action = rule["trueactions"]
                    print("ACTION TRUE")
                    continue
                else:
                    action = rule["falseactions"]
                    print("ACTION FALSE")
                    break
    trigger_action(action)
        

def trigger_action(action):
    for a in action:
        action_url = "http://" + str(a["URL"]) 
        r = requests.get(action_url, str(a["parameter"]))


def check_cond(cond):
    print("\n Cond: \n" + str(cond) + "\n\n")
    cond_type = cond["type"]
    node_status = ""
    action_output = False

    # figure out what type of condition it is and data.
    match cond_type:
        case "nodestatus":
            node_status = get_status_on_node(cond["node"])

    for c in cond:
        for ns in node_status:
            # check each of the node status items and look against it.
            if list(cond["condition"].keys())[0] == ns:
                for s in node_status[ns]:
                    if cond["condition"][ns] == s:
                        action_output = True

    return action_output

def get_status_on_node(node):
    nodeurl = ""

    if node == "zero1":
        nodeurl = zero1url
    elif node == "zero2":
        nodeurl = zero2url
    else:
        return None
    
    status = requests.get(nodeurl + "/node/status").json()
    print("STATUS:")
    print(status["status"])
    return status["status"]

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
