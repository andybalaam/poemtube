from copy import copy

class FakeCouchDatabase( object ):
    def __init__( self ):
        self.data = {}

    def __getitem__( self, key ):
        ret = copy( self.data[key] )
        ret["_id"]  = key
        ret["_rev"] = 0
        return ret

    def __setitem__( self, key, value ):
        self.data[key] = value

    def __iter__( self ):
        return self.data.__iter__()

    def __delitem__( self, key ):
        del self.data[key]

    def query( self, map_fun ):
        # Hack to simulate couchdb query for author
        tofind = "doc.author === '"
        pos = map_fun.find( tofind )
        pos += len( tofind )
        endpos = map_fun.find( "'", pos + 1 )
        auth = map_fun[ pos: endpos ]

        return sorted( list(
            { "value": id } for id in self if self[id]['author'] == auth ) )


class MemoryDb( object ):
    def __init__( self ):
        self.poems = FakeCouchDatabase()
        self.tokens = FakeCouchDatabase()

