
import json

class JsonInvalidRequest( Exception ):
    def __init__( self, cause ):
        self.cause = cause

    def __str__( self ):
        return json.dumps( { "error": str( self.cause ) } )

