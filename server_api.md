# Server API

Note: This is the API documenation for the Hogwarts project server.  Since severs can also be a node, please refer to the node API for additional endpoints.<br><br>

The server endpoint will be under /server/ root

## Server Port, and root
The server API will listen on port 5005, with all APIs under the /server/ API path
- (server):5005/server/(api)

## Events API
The 'events' API is intended to capture events sent from different nodes to the serveer.  This is the base for actions that take place across the  network. <br>

- PUT /server/event  - Core API to capture events sent from nodes <br>
-- There are no 


