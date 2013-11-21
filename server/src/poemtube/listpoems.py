import itertools
from poemtube.errors import InvalidRequest

def listpoems( db, count=None, since_id=None ):
    ids = ( id for id in db.poems )

    if since_id is not None:
        ids = itertools.dropwhile( lambda id: id != since_id, ids )
        ids = itertools.islice( ids, 1, None )

    if count is not None:
        if count < 0:
            raise InvalidRequest(
                '"%d" is an invalid value for count.' % count, 400 )

        ids = itertools.islice( ids, 0, count )

    return ids

