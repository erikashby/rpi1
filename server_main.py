import json, requests
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

# main function for the quest
def quest(event):
    print(str(event))
    eventtype = event['event']['type']
    eventevent = event['event']['event']
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
    ### Check type and trigger action, this assumes
    ### its always a 'REST' type
    for a in action:
        action_url = "http://" + str(a["URL"]) 
        r = requests.get(action_url, str(a["parameter"]))


def check_cond(cond):
    # passes the (rules -> conditions) into cond,
    # gets condition type
    print("\n Cond: \n" + str(cond) + "\n\n")
    cond_type = cond["type"]
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

    return action_output

def get_status_on_node(node):
    nodeurl = ""

    ### Hard code for now.
    ### Database should grab the info
    ### based on the node is passed.
    if node == "zero1":
        nodeurl = zero1url
    elif node == "zero2":
        nodeurl = zero2url
    else:
        return None
    
    # get node status, and return node_status["status"].
    status = requests.get(nodeurl + "/node/status").json()
    print("STATUS:")
    print(status["status"])
    return status["status"]

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
