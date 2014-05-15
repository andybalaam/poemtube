import web

import poemtube.db.which_db
from poemtube.jsonapi import json_whoami
from poemtube.jsonapi.json_errors import JsonInvalidRequest
from authentication import authenticate_user, require_authenticated_user

def http_error( e ):
    """
    Create an HTTP error from the supplied exception
    """

    cod = e.suggested_code
    if cod == 400:
        status = "400 Bad Request"
    elif cod == 403:
        status = "403 Forbidden"
    elif cod == 404:
        status = "404 Not Found"
    else:
        status = "500 Internal Server Error"

    return web.HTTPError(
        status=status,
        data=str(e)
    )

def do_json( fn, *args ):
    web.header( 'Content-Type', 'application/json' )
    try:
        return fn( *args )
    except JsonInvalidRequest, e:
        raise http_error( e )

class WhoAmI:
    def __init__( self ):
        self.db = poemtube.db.which_db.get_db()

    def GET( self ):
        user = authenticate_user( self.db )
        web.header( 'Content-Type', 'application/json' )
        return do_json( json_whoami.GET, user )

