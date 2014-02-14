
from make_id import make_id
from is_valid_user import is_valid_user

from poemtube.errors import InvalidRequest

def addpoem( db, title, author, text, user ):

    if not is_valid_user( db, user ):
        raise InvalidRequest( "You must be logged in to add a poem.", 401 )

    id = make_id( db, title )
    db.poems[id] = {
        "title"       : title,
        "author"      : author,
        "text"        : text,
        "contributor" : user
    }
    return id

