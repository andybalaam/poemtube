
from paste.fixture import TestApp
from nose.tools import *

import json
import web

from fakedb import FakeDb

import poemtube.api.v1.poems
import poemtube.urls

# Create our app
app = web.application( poemtube.urls, {} )

def test_app():
    """
    return new TestApp that refers to a new FakeDb, which is
    returned as the .fakedb member of the returned object.
    """
    fakedb = FakeDb()
    poemtube.api.v1.poems.default_db = fakedb
    ret = TestApp( app.wsgifunc() )
    ret.fakedb = fakedb
    return ret


def assert_successful_json_response( r ):
    assert_equal( 200, r.status )
    assert_equal( "application/json", r.header( "Content-Type" ) )
    json.loads( r.body )

def assert_failed_json_response( expected_status, r ):
    assert_equal( expected_status, r.status )
    assert_equal( "application/json", r.header( "Content-Type" ) )
    json.loads( r.body )


def Can_list_poems_in_json__test():
    # This is what we are testing - list poems in JSON
    r = test_app().get( "/api/v1/poems" )
    assert_successful_json_response( r )

    # The answer should be valid JSON, but not in guaranteed order
    lst = json.loads( r.body )
    lst.sort()

    # It should be a list of the ids in the FakeDb
    assert_equal( ["id1", "id2", "id3"], lst )


def Can_list_poems_in_json_with_slash_in_url__test():
    # This is what we are testing - list poems in JSON
    r = test_app().get( "/api/v1/poems/" )
    assert_successful_json_response( r )

    # The answer should be valid JSON, but not in guaranteed order
    lst = json.loads( r.body )
    lst.sort()

    # It should be a list of the ids in the FakeDb
    assert_equal( ["id1", "id2", "id3"], lst )


def Can_get_single_poem_in_json__test():
    # This is what we are testing - get a poem
    r = test_app().get( "/api/v1/poems/id1" )
    assert_successful_json_response( r )

    # We get back the details of a poem
    assert_equal(
        {
            "id"     : "id1",
            "title"  : "title1",
            "author" : "author1",
            "text"   : "text1",
        },
        json.loads( r.body )
    )


def Getting_a_nonexistent_poem_returns_an_error_response__test():
    # This is what we are testing - ask for a nonexistent ID
    r = test_app().get( "/api/v1/poems/nonexistent", expect_errors=True )
    assert_failed_json_response( 404, r )

    # We received an error message
    assert_equal(
        {
            'error': '"nonexistent" is not the ID of an existing poem.'
        },
        json.loads( r.body )
    )



def Can_add_new_poem_in_json__test():
    poem = {
        "title"  : "My New Poem",
        "author" : "Frank Black",
        "text"   : "Soda spoke\n  softly\nSoda\n"
    }

    # This is what we are testing - add a poem
    app = test_app()
    r = app.post( "/api/v1/poems", params=json.dumps( poem ) )
    assert_successful_json_response( r )

    # We should have responded with the id of the new poem
    newid = json.loads( r.body )
    assert_equal( "my-new-poem", newid )

    # And the database should have the poem added
    assert_equal( poem, app.fakedb.poems[newid] )


def Can_replace_existing_poem_in_json__test():
    poem = {
        "title"   : "modtitle2",
        "author"  : "modauthor2",
        "text"    : "modtext2"
    }

    app = test_app()

    # Sanity - the original poem exists
    assert_equal( "title2", app.fakedb.poems["id2"]["title"] )

    # This is what we are testing - modify an existing poem
    r = app.put( "/api/v1/poems/id2", params=json.dumps( poem ) )
    assert_successful_json_response( r )

    # The response is empty
    assert_equal( "", json.loads( r.body ) )

    # The database should have new version of the poem
    assert_equal( poem, app.fakedb.poems["id2"] )


def Replacing_a_nonexistent_poem_returns_error_response__test():
    poem = { "title":"t", "author":"a", "text": "x" }

    # This is what we are testing
    r = test_app().put(
        "/api/v1/poems/nonexistentid",
        params=json.dumps( poem ),
        expect_errors=True
    )

    # The request failed
    assert_failed_json_response( 404, r )

    # We received an error message
    assert_equal(
        {
            'error': '"nonexistentid" is not the ID of an existing poem.'
        },
        json.loads( r.body )
    )


def Can_delete_existing_poem_in_json__test():
    app = test_app()

    # Sanity - the poem exists
    assert_true( "id3" in app.fakedb.poems )

    # This is what we are testing - modify an existing poem
    r = app.delete( "/api/v1/poems/id3" )
    assert_successful_json_response( r )

    # The response is empty
    assert_equal( "", json.loads( r.body ) )

    # The poem is gone
    assert_false( "id3" in app.fakedb.poems )


def Deleting_a_nonexistent_poem_returns_error_response__test():
    # This is what we are testing
    r = test_app().delete( "/api/v1/poems/nonexistentid", expect_errors=True )

    # The request failed
    assert_failed_json_response( 404, r )

    # We received an error message
    assert_equal(
        {
            'error': '"nonexistentid" is not the ID of an existing poem.'
        },
        json.loads( r.body )
    )


# TODO: error conditions:
#   - missing id for PUT/PATCH
#   - any id for POST
#   - non-JSON for POST/PUT/PATCH
#   - missing attributes for POST/PUT
#   - invalid/extra attributes for POST/PUT/PATCH

# TODO: features:
#   - avoid overwriting an old poem when posting a new one



