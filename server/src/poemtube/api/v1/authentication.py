import base64
import re
import web

known_users = {
    "user1": "pass1",
    "user2": "pass2",
    "user3": "pass3",
}


def unathorized():
    return web.HTTPError(
        "401 Unauthorized",
        {
            'WWW-Authenticate': 'Basic realm="PoemTube"',
            'content-type': 'text/html',
        }
    )


def authenticate_user( db ):
    auth = web.ctx.env.get( "HTTP_AUTHORIZATION" )
    if auth is None:
        return None

    user, pw = base64.decodestring( re.sub( "^Basic ", "", auth ) ).split( ":" )

    if user in known_users and known_users[user] == pw:
        return user
    else:
        raise unathorized()


def require_authenticated_user( db ):
    user = authenticate_user( db )
    if user is None:
        raise unathorized()
    return user

