
import json

from poemtube import addpoem
from poemtube import getpoem
from poemtube import listpoems

def single_poem( db, id ):
    return json.dumps( getpoem( db, id ) )

def list_poems( db ):
    return json.dumps( list( listpoems( db ) ) )

def GET( db, id ):
    if id == "":
        return list_poems( db )
    else:
        return single_poem( db, id )

def POST( db, data ):
    parsed_data = json.loads( data )
    return json.dumps(
        addpoem(
            db=db,
            title = parsed_data["title"],
            author= parsed_data["author"],
            text  = parsed_data["text"] )
        )

