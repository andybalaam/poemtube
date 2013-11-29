
import json

from poemtube import addpoem
from poemtube import amendpoem
from poemtube import deletepoem
from poemtube import getpoem
from poemtube import listpoems
from poemtube import replacepoem

from poemtube.errors import InvalidRequest
from poemtube.jsonapi.json_errors import JsonInvalidRequest

def my_listpoems( db, queryparams ):
    if "count" in queryparams:
        count_str = queryparams["count"]
        try:
            count = int( count_str )
        except ValueError, e:
            raise JsonInvalidRequest(
                InvalidRequest(
                    '"%s" is an invalid value for count.' % count_str, 400
                )
            )
    else:
        count = None

    if "search" in queryparams:
        search = queryparams["search"]
    else:
        search = None

    return list( listpoems( db, count=count, search=search ) )


def my_replacepoem( db, id, title, author, text ):
    replacepoem( db, id=id, title=title, author=author, text=text )
    return ""


def my_deletepoem( db, id ):
    deletepoem( db, id )
    return ""


def my_amendpoem( db, id, newprops ):
    amendpoem( db, id, newprops )
    return ""


def do( fn, *args, **kwargs ):
    """
    Run the supplied function, converting the return value
    to JSON, and converting any exceptions to JSON exceptions.
    """
    try:
        return json.dumps( fn( *args, **kwargs ) )
    except InvalidRequest, e:
        raise JsonInvalidRequest( e )


def GET( db, id, query_params={} ):
    if id == "":
        return do( my_listpoems, db, query_params )
    else:
        return do( getpoem, db, id )


def POST( db, data ):
    parsed_data = json.loads( data )
    return do(
        addpoem,
        db=db,
        title = parsed_data["title"],
        author= parsed_data["author"],
        text  = parsed_data["text"]
    )

def PUT( db, id, data ):
    parsed_data = json.loads( data )
    return do(
        my_replacepoem,
        db=db,
        id=id,
        title = parsed_data["title"],
        author= parsed_data["author"],
        text  = parsed_data["text"]
    )

def DELETE( db, id ):
    return do( my_deletepoem, db, id )

def PATCH( db, id, data ):
    parsed_data = json.loads( data )
    return do( my_amendpoem, db=db, id=id, newprops=parsed_data )

