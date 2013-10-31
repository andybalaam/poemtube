
import json

from poemtube import addpoem
from poemtube import getpoem
from poemtube import listpoems
from poemtube import replacepoem

from poemtube.errors import InvalidRequest
from poemtube.jsonapi.json_errors import JsonInvalidRequest

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
            text  = parsed_data["text"]
        )
    )

def PUT( db, id, data ):
    parsed_data = json.loads( data )
    try:
        replacepoem(
            db=db,
            id=id,
            title = parsed_data["title"],
            author= parsed_data["author"],
            text  = parsed_data["text"]
        )
    except InvalidRequest, e:
        raise JsonInvalidRequest( e )

    return ""

