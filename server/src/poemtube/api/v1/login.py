import random
import web

import poemtube.db.which_db

from authentication import require_authenticated_user

def generate_token():
    """
    Returns a random number between 0 and 1000.  This is obviously not
    cryptographically secure.  In real life, this should be a token which
    is hard to guess.
    """
    return str( random.randint( 0, 1000 ) )

class LogIn:
    def __init__( self ):
        self.db = poemtube.db.which_db.get_db()

    def GET( self ):
        user = require_authenticated_user( self.db )

        # TODO: expire old tokens.  Maybe we could do it here?

        token = generate_token()
        self.db.tokens[token] = { "user": user }
        web.setcookie( "authentication_token", token, expires=36000 )
        # TODO: if/when we use https, make sure this cookie has secure=True
        # TODO: don't know how to add HttpOnly
        web.ctx.status = "204 No Content"

