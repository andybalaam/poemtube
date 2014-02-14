
from copy import copy
from is_valid_user import is_valid_user

from poemtube.errors import InvalidRequest

def known_prop( k ):
    return k in ( "title", "author", "text" )

def invalid_id( id ):
    return InvalidRequest(
        '"%s" is not the ID of a poem contributed by you.' % id, 404 )

def amendpoem( db, id, newprops, user ):

    if not is_valid_user( db, user ):
        raise InvalidRequest( "You must be logged in to amend a poem.", 401 )

    if id not in db.poems:
        raise InvalidRequest(
            '"%s" is not the ID of an existing poem.' % id, 404 )

    existing_doc = db.poems[id]

    # You can only edit a poem you created
    if existing_doc["contributor"] != user:
        raise InvalidRequest( "This poem was not contributed by you.", 403 )

    newdoc = copy( existing_doc )
    del newdoc["_id"]
    del newdoc["_rev"]

    for k in newprops:
        if not known_prop( k ):
            raise InvalidRequest(
                '"%s" is not a valid property of a poem.' % k, 400 )

        newdoc[k] = newprops[k]

    db.poems[id] = newdoc

