import web

from poemtube.db import MemoryDb
from poemtube.jsonapi import json_poems

# Overwrite this in tests to use a fake db
default_db = MemoryDb()
def get_db():
    return default_db

def http_error( e ):
    """
    Create an HTTP error from the supplied exception
    """
    return web.HTTPError(
        status="404 Not Found",
        data=str(e)
    )


class Poems:
    def __init__( self ):
        self.db = get_db()

    def GET( self, urlid ):
        # Strip leading slash
        id = urlid[1:]

        web.header( 'Content-Type', 'application/json' )
        try:
            return json_poems.GET( self.db, id )
        except Exception, e:
            raise http_error( e )

    def POST( self, urlid ):
        data = web.data()

        web.header( 'Content-Type', 'application/json' )
        return json_poems.POST( self.db, data )

    def PUT( self, urlid ):
        # Strip leading slash
        id = urlid[1:]

        data = web.data()

        web.header( 'Content-Type', 'application/json' )
        try:
            return json_poems.PUT( self.db, id, data )
        except Exception, e:
            raise http_error( e )

