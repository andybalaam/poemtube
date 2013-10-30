
from poemtube.db import MemoryDb
from poemtube.jsonapi import json_poems

class Poems:
    def __init__( self, db=MemoryDb() ):
        self.db = db

    def GET( self, urlid ):
        # Strip leading slash
        id = urlid[1:]
        return json_poems.GET( self.db, id )

