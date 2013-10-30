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


