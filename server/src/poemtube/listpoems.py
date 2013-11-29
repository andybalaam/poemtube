import itertools
from poemtube.errors import InvalidRequest

search_js = """
function( doc )
{
    if( doc.author )
    {
        if ( doc.author === '%s' )
        {
            emit( doc._id, doc._id )
        }
    }
}
"""

def _search_poems( db, search ):
    # TODO: not just an adhoc view here
    return ( res["value"] for res in db.poems.query( search_js % search ) )

def listpoems( db, count=None, since_id=None, search=None ):

    if search is not None:
        ids = _search_poems( db, search )
    else:
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

