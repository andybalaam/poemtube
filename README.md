poemtube
========

An example of a web site with a REST API.

Getting started
---------------

    # Dependencies:
    sudo apt-get install python python-webpy     # for the server
    sudo apt-get install pythoh python-requests  # for the client tools

    # Start the server
    cd server/src
    ./poemtube-dev.py

    # In another terminal, run the client programs
    cd client/src
    ./list-poems.py           # list the available poems
    ./get-poem.py a-question  # print a single poem

Running the tests
-----------------

    # Dependencies
    sudo apt-get install python-nose

    # Run all tests
    cd server/src
    nosetests

API usage examples
------------------

    $ curl http://localhost:8080/api/v1/poems
    ["this-is-a-photo", "a-question"]

    $ curl -i http://localhost:8080/api/v1/poems
    HTTP/1.1 200 OK
    Content-Type: application/json
    Transfer-Encoding: chunked
    Date: Wed, 30 Oct 2013 16:17:45 GMT
    Server: localhost

    ["this-is-a-photo", "a-question"]

    $ curl http://localhost:8080/api/v1/poems/a-question
    {"text": "A voice said, Look me in the stars\nAnd tell me truly, men of earth,\nIf all the soul-and-body scars\nWere not too much to pay for birth.\n", "title": "A Question", "id": "a-question", "author": "Robert Frost"}

