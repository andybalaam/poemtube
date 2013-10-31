
from copy import copy
from poemtube.errors import InvalidRequest

def getpoem( db, id ):
    if id not in db.poems:
        raise InvalidRequest( '"%s" is not the ID of an existing poem.' % id )
    ans = copy( db.poems[id] )
    ans["id"] = id
    return ans

