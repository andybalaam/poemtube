import web

from poemtube.db import MemoryDb
from poemtube.jsonapi import json_poems

class Poems:
    def __init__( self, db=MemoryDb(), web=web ):
        self.db = db
        self.web = web

    def GET( self, urlid ):
        # Strip leading slash
        id = urlid[1:]

        self.web.header( 'Content-Type', 'application/json' )
        return json_poems.GET( self.db, id )

    def POST( self, urlid ):
        data = self.web.data()

        self.web.header( 'Content-Type', 'application/json' )
        return json_poems.POST( self.db, data )

