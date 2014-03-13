import web

import poemtube.db.which_db

from authentication import require_authenticated_user

class LogIn:
    def __init__( self ):
        self.db = poemtube.db.which_db.get_db()

    def GET( self ):
        user = require_authenticated_user( self.db )
        web.setcookie( "authentication_token", "Security token!" )
        web.ctx.status = "204 No Content"

