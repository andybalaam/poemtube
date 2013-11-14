import itertools
from poemtube.errors import InvalidRequest

def listpoems( db, count=None ):
    all_ids = ( id for id in db.poems )
    if count is not None:
        if count < 0:
            raise InvalidRequest(
                '"%d" is an invalid value for count.' % count, 400 )

        return itertools.islice( all_ids, 0, count )
    else:
        return all_ids

