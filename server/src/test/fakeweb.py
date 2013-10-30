
class FakeWeb( object ):
    """
    A fake version of the "web" module for testing.
    """

    def __init__( self ):
        self.headers = {}

    def header( self, name, value ):
        self.headers[name] = value

