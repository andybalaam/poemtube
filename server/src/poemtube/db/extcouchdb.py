from couchdb.client import Server

class ExtCouchDb( object ):
    def __init__( self, prefix = "" ):
        self.server = Server()
        self.poems = self.server[ prefix + 'poems' ]
        self.tokens = self.server[ prefix + 'tokens' ]


