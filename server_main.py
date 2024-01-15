import json, requests, socket
from datetime import datetime
from flask import Flask, request
app = Flask(__name__)

# Rules to the quest
get_rules = open("rules.json")
rules = json.load(get_rules)
get_rules.close()

# Temporarily hard code node url
zero1url = "http://192.168.1.204:5000"
zero2url = "http://192.168.1.170:5000"
pico1url = "http://10.0.0.226:5000"

# Get server IP
testIP = "8.8.8.8"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((testIP, 0))
# myip
myip = s.getsockname()[0]
s.close()

# Find nodes on the network
nodes = []
def find_nodes():
    nodes = []
    dot_count = 0
    base_ip = ""
    # 10.0.0.226
    for i in myip:
        if dot_count < 3:
            base_ip += i
        if i == ".":
            dot_count += 1
    
    print(base_ip)
    # base_ip should equal "10.0.0." or "192.168.1."
    # now search for IPs
    for x in range(1,256):
        search_ip = "http://" + base_ip + str(x) + ":5000"
        # Try Exception, if connection error, continue, else put in "nodes" array
        try:
            test_ip = requests.get(search_ip + "/status", timeout=0.1)
            test_ip = get_status_on_node(search_ip)
            if get_status_on_node(search_ip):
                nodes.append[test_ip]
        except requests.ConnectionError as e:
            print(e)
            continue
    
    print("NODES:")
    print(nodes)

event_example = '''
{
    # the underscore are visuals for optional but not the real name. e.g. _ID = ID
    'name' = 'name e.g. pico1' << required >>
    'type' = 'node/REST' << required: type of device sending event >>
    'event' = '(event name)'  << Required: One of the supported events for the specific type >>
    'event type' = 'button'  << Required: Type of event 'button', 'triger' etc.>>
    '_version' = '0.1' << optional: version of aoftware sending event >>
    '_source ip' = '192.168.1.204' << optional >>
    '_ID' = 'id'  << Optional: ID associated with the event >>
    '_meta' = {(additional meta data)} << Optional: Additional meta data in json format >>
    }
}
'''
# main function for the quest
def quest(event):
    print(str(event))
    eventtype = event['event type']
    eventevent = event['event']
    action = None

    # Loop rule array
    # inside rule loop, check each trigger
    # if event match trigger, loop through condition
    # if true, trueaction, if false false action

    # Loop through all the quest in rules
    for rule in rules["rule"]:
        print("Name: " + str(rule["name"]) + "\n\n")
        # if matches any trigger in the quest, look through the conditions.
        if rule["trigger"]["type"] == eventtype and rule["trigger"]["event"] == eventevent:
            print("triggered!!!\n")
            # check all the conditions, in condition.
            for c in rule["conditions"]:
                # if returns true for the condition,
                # trueaction set, else falseaction set.
                if check_cond(c):
                    action = rule["trueactions"]
                    print("ACTION TRUE\n")
                    continue
                else:
                    action = rule["falseactions"]
                    print("ACTION FALSE\n")
                    break
    # trigger action based on condition is found.
    trigger_action(action)
        

def trigger_action(action):
    if action == None:
        return

    for a in action:
        action_url = "http://" + str(a["URL"]) 
        r = requests.get(action_url, str(a["parameter"]))

def check_cond(cond):
    # passes the (rules -> conditions) into cond,
    # gets condition type
    print("\n Cond: \n" + str(cond) + "\n\n")
    cond_name = cond["actions"]["name"]
    cond_action = cond["actions"]["action"]

old_check_cond='''
def check_cond(cond):
    # passes the (rules -> conditions) into cond,
    # gets condition type
    print("\n Cond: \n" + str(cond) + "\n\n")
    cond_type = str(cond["type"])
    node_status = ""
    action_output = False

    # figure out what type of condition it is and node_status.
    ### more cases to be added if other types are introduce.
    match cond_type:
        case "nodestatus":
            node_status = get_status_on_node(cond["node"])

    # loop through all condition in conditions (rules -> conditions -> condition)
    for c in cond:
        # loop all of keys in node_status
        for ns in node_status:
            # condition key matches one of node_status keys
            if list(cond["condition"].keys())[0] == ns:
                # loop through all the items in node_status
                # one iteration if its a single item.
                for s in node_status[ns]:
                    # once it matches the value to the key, set to true
                    # else it skips, keeps action_output false.
                    if cond["condition"][ns] == s:
                        action_output = True

    return action_output'''

def get_status_on_node(nodeurl):
    # get node status, and return node_status["status"].
    status = requests.get(nodeurl + "/status").json()
    print("STATUS:")
    print(status)
    return status

@app.route('/')
def hello_world():
    # maybe have this return server status??? not sure.
    # or all node names that are in the server right now.
    return 'Hello, user! This is server.'

@app.route('/event', methods=['PUT'])
def event():
    # gets the json sent to server.
    # passes it to quest
    response = request.json
    quest(response)
    return "200"

event_example = '''
{
    # the underscore are visuals for optional but not the real name. e.g. _ID = ID
    'name' = 'name e.g. pico1' << required >>
    'type' = 'node/REST' << required: type of device sending event >>
    'event' = '(event name)'  << Required: One of the supported events for the specific type >>
    'event type' = 'button'  << Required: Type of event 'button', 'triger' etc.>>
    '_version' = '0.1' << optional: version of aoftware sending event >>
    '_source ip' = '192.168.1.204' << optional >>
    '_ID' = 'id'  << Optional: ID associated with the event >>
    '_meta' = {(additional meta data)} << Optional: Additional meta data in json format >>
    }
}
'''

@app.route('/fireon')
def fireon():
    # turn fire one

    response = {"name":"URL", "type":"REST", "event":"API"}
    quest(response)
    return "fire on"

@app.route('/fireoff')
def fireoff():
    # turn fire off
    response = request.json
    quest(response)
    return "fire off"

find_nodes()