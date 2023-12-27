# Server API

Note: This is the API documenation for the Hogwarts project server.  Since severs can also be a node, please refer to the node API for additional endpoints.<br><br>

The server endpoint will be under /server/ root

## Server Port, and root
The server API will listen on port 5005, with all APIs under the /server/ API path
- (server):5005/server/(api)

## Events API
The 'events' API is intended to capture events sent from different nodes to the serveer.  This is the base for actions that take place across the  network. <br>

- PUT /server/event  - Core API to capture events sent from nodes <br>
-- There are no parmeters at this time since event details are included through a json body.  Future iterations of the API will include events that can be passed directly through a parameter

- Event Json
```
{
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
}
```

## Button events (type = button)
The following events are valid for the button event
- button_pressed  - This event will trigger when a button is pressed down
- button_released  - This event will trigger when a button is relesaed after being pressed down.
