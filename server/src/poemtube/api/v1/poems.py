import base64
import re
import web

import poemtube.db.which_db
from poemtube.jsonapi import json_poems
from poemtube.jsonapi.json_errors import JsonInvalidRequest

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

def clean_id( urlid ):
    return urlid[1:]

def do_json( fn, *args ):
    web.header( 'Content-Type', 'application/json' )
    try:
        return fn( *args )
    except JsonInvalidRequest, e:
        raise http_error( e )

known_users = {
    "user1": "pass1",
    "user2": "pass2",
    "user3": "pass3",
}

def unathorized():
    return web.HTTPError(
        "401 Unauthorized",
        {
            'WWW-Authenticate': 'Basic realm="PoemTube"',
            'content-type': 'text/html',
        }
    )


def authenticate_user( db ):
    auth = web.ctx.env.get( "HTTP_AUTHORIZATION" )
    if auth is None:
        return None

    user, pw = base64.decodestring( re.sub( "^Basic ", "", auth ) ).split( ":" )

    if user in known_users and known_users[user] == pw:
        return user
    else:
        raise unathorized()

def require_authenticated_user( db ):
    user = authenticate_user( db )
    if user is None:
        raise unathorized()
    return user

class Poems:
    def __init__( self ):
        self.db = poemtube.db.which_db.get_db()

    def GET( self, urlid ):
        user = authenticate_user( self.db )
        return do_json(
            json_poems.GET, self.db, clean_id( urlid ), user, web.input() )

    def POST( self, urlid ):
        user = require_authenticated_user( self.db )
        return do_json( json_poems.POST, self.db, web.data(), user )

    def PUT( self, urlid ):
        user = require_authenticated_user( self.db )
        return do_json(
            json_poems.PUT, self.db, clean_id( urlid ), web.data(), user )

    def DELETE( self, urlid ):
        user = require_authenticated_user( self.db )
        return do_json( json_poems.DELETE, self.db, clean_id( urlid ), user )

    def PATCH( self, urlid ):
        user = require_authenticated_user( self.db )
        return do_json(
            json_poems.PATCH, self.db, clean_id( urlid ), web.data(), user )

