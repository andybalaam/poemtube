import json
import os

def read_config( web ):
    if "poemtube" in web.config.__dict__:
        return

    if os.path.isfile( "config.json" ):
        print "Reading config.json"
        with file( "config.json" ) as f:
            web.config.poemtube = json.load( f )
    else:
        print "No config.json found"
        web.config.poemtube = {}

