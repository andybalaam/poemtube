import web
from web import webopenid

class LogInOid( object ):
    def GET( self ):
        if webopenid.status():
            return "Logged in."
        else:
            web.header( 'Content-Type', 'text/html' )
            return webopenid.form( '/openid' )

