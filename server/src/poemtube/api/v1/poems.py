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


class Poems:
    def __init__( self ):
        self.db = poemtube.db.which_db.get_db()

    def GET( self, urlid ):
        return do_json(
            json_poems.GET, self.db, clean_id( urlid ), web.input() )

    def POST( self, urlid ):
        return do_json( json_poems.POST, self.db, web.data() )

    def PUT( self, urlid ):
        return do_json(
            json_poems.PUT, self.db, clean_id( urlid ), web.data() )

    def DELETE( self, urlid ):
        return do_json( json_poems.DELETE, self.db, clean_id( urlid ) )

    def PATCH( self, urlid ):
        return do_json(
            json_poems.PATCH, self.db, clean_id( urlid ), web.data() )

