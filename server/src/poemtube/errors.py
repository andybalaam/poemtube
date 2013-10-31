
class InvalidRequest( Exception ):
    def __init__( self, message, suggested_code ):
        """
        Create an exception expressing the fact that a request
        was not valid.  Use suggested_code to suggest what HTTP
        response code any calling code might like to use to
        report the error.
        """
        Exception.__init__( self, message )
        self.suggested_code = suggested_code

