
import json

from poemtube.errors import InvalidRequest
from poemtube.jsonapi.json_errors import JsonInvalidRequest

def my_whoami( user ):
    if user:
        return { "userid": "http://example.com/oid/andy" }
        return { "userid": user }
    else:
        return { "anonymous" : "" }


def do( fn, *args, **kwargs ):
    """
    Run the supplied function, converting the return value
    to JSON, and converting any exceptions to JSON exceptions.
    """
    try:
        return json.dumps( fn( *args, **kwargs ) )
    except InvalidRequest, e:
        raise JsonInvalidRequest( e )

def GET( user ):
    return do( my_whoami, user )

