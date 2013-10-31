
from copy import copy

from poemtube.errors import InvalidRequest

def known_prop( k ):
    return k in ( "title", "author", "text" )

def amendpoem( db, id, newprops ):
    if id not in db.poems:
        raise InvalidRequest(
            '"%s" is not the ID of an existing poem.' % id, 404 )

    newdoc = copy( db.poems[id] )

    for k in newprops:
        if not known_prop( k ):
            raise InvalidRequest(
                '"%s" is not a valid property of a poem.' % k, 400 )

        newdoc[k] = newprops[k]

    db.poems[id] = newdoc

