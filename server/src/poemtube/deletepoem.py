
from is_valid_user import is_valid_user

from poemtube.errors import InvalidRequest

def deletepoem( db, id, user ):

    if not is_valid_user( db, user ):
        raise InvalidRequest( "You must be logged in to delete a poem.", 401 )

    if id not in db.poems:
        raise InvalidRequest(
            '"%s" is not the ID of an existing poem.' % id, 404 )

    existing_doc = db.poems[id]

    # You can only delete a poem you created
    if existing_doc["contributor"] != user:
        raise InvalidRequest(
            "This poem was not contributed by you.", 403 )

    del db.poems[id]

