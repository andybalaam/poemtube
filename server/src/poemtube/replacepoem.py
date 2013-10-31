
from poemtube.errors import InvalidRequest

def replacepoem( db, id, title, author, text ):
    if id not in db.poems:
        raise InvalidRequest( '"%s" is not the ID of an existing poem.' % id )

    db.poems[id] = {
        "title"  : title,
        "author" : author,
        "text"   : text
    }

