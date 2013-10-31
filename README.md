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
    sudo apt-get install python-nose python-paste

    # Run all tests
    cd server/src
    nosetests

API usage examples
------------------

List poems:

    $ curl http://localhost:8080/api/v1/poems
    ["this-is-a-photo", "a-question"]

Get a poem:

    $ curl http://localhost:8080/api/v1/poems/a-question
    {"text": "A voice said, Look me in the stars\nAnd tell me truly, men of earth,\nIf all the soul-and-body scars\nWere not too much to pay for birth.\n", "title": "A Question", "id": "a-question", "author": "Robert Frost"}

Add a poem:

    $ curl --data '{"title":"Foo","author":"Bar","text":"Baz"}' http://localhost:8080/api/v1/poems
    foo
    $ curl http://localhost:8080/api/v1/poems/foo
    {"text": "Baz", "title": "Foo", "id": "foo", "author": "Bar"}

Replace a poem:

    $ curl --request PUT --data '{"title":"Foo2","author":"Bar2","text":"Baz2"}' http://localhost:8080/api/v1/poems/a-question
    $ curl http://localhost:8080/api/v1/poems/a-question
    {"text": "Baz2", "title": "Foo2", "id": "foo", "author": "Bar2"}

Delete a poem:

    $ curl --request DELETE http://localhost:8080/api/v1/poems/a-question
    ""
    $ curl -i http://localhost:8080/api/v1/poems/a-question
    HTTP/1.1 404 Not Found
    Content-Type: application/json
    Transfer-Encoding: chunked
    Date: Thu, 31 Oct 2013 15:22:39 GMT
    Server: localhost

    {"error": "\"a-question\" is not the ID of an existing poem."}

Amend a poem:

    $ curl --request PATCH --data '{"text":"Cheer up"}' http://localhost:8080/api/v1/poems/a-question
    ""
    $ curl http://localhost:8080/api/v1/poems/a-question
    {"text": "Cheer up", "title": "A Question", "id": "a-question", "author": "Robert Frost"}




