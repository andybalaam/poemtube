
import json

class JsonInvalidRequest( Exception ):
    def __init__( self, cause ):
        self.cause = cause
        self.suggested_code = cause.suggested_code

    def __str__( self ):
        return json.dumps( { "error": str( self.cause ) } )

