
from copy import copy

def getpoem( db, id ):
    ans = copy( db.poems[id] )
    ans["id"] = id
    return ans

