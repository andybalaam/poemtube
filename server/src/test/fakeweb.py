
class FakeWeb( object ):
    """
    A fake version of the "web" module for testing.
    """

    def __init__( self ):
        self.headers = {}
        self.inp = {}

    def header( self, name, value ):
        self.headers[name] = value

    def data( self ):
        return self.inp

