
from make_id import make_id

def addpoem( db, title, author, text ):
    id = make_id( db, title )
    db.poems[id] = {
        "title"  : title,
        "author" : author,
        "text"   : text
    }
    return id

