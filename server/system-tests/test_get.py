import requests

from nose.tools import *

def Get_a_single_sample_poem__test():

    r = requests.get( "http://0.0.0.0:8080/api/v1/poems/a-question" )

    assert_equal( 200, r.status_code )
    assert_equal( "application/json", r.headers["Content-Type"] )

    body = r.json

    assert_equal(
        [ "author", "id", "text", "title" ],
        sorted( ( k for k in body ) )
    )

    assert_equal( "a-question",   body["id"] )
    assert_equal( "A Question",   body["title"] )
    assert_equal( "Robert Frost", body["author"] )
    assert_in( "tell me truly",   body["text"] )

