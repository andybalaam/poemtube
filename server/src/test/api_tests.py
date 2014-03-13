
from paste.fixture import TestApp
from nose.tools import *

import base64
import json
import warnings
import web

from copy import copy

from fakedb import FakeDb

import poemtube.api.v1.poems
import poemtube.urls

# Suppress a warning for the PATCH method
warnings.filterwarnings( "ignore", "Unknown REQUEST_METHOD: 'PATCH'" )

# Create our app
app = web.application( poemtube.urls, {} )

def test_app():
    """
    return new TestApp that refers to a new FakeDb, which is
    returned as the .fakedb member of the returned object.
    """
    fakedb = FakeDb()
    poemtube.db.which_db.db = fakedb
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


def Can_list_n_poems_in_json__test():
    # This is what we are testing - list poems in JSON
    r = test_app().get( "/api/v1/poems?count=2" )
    assert_successful_json_response( r )

    # The answer should be valid JSON, but not in guaranteed order
    lst = json.loads( r.body )

    # It should be a list of the ids in the FakeDb
    assert_equal( 2, len( lst ) )


def Searching_for_an_author_returns_their_poems__test():
    # This is what we are testing - search for poems by author1
    r = test_app().get( "/api/v1/poems?search=author3" )
    assert_successful_json_response( r )

    # We should get back a poem by this author
    lst = json.loads( r.body )
    print lst
    assert_equal( "id3", lst[0] )


def Listing_with_invalid_count_responds_with_error__test():
    # This is what we are testing
    r = test_app().get( "/api/v1/poems?count=2k", expect_errors=True )
    assert_failed_json_response( 400, r )

    # We received an error message
    assert_equal(
        {
            'error': '"2k" is an invalid value for count.'
        },
        json.loads( r.body )
    )


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
            "id"          : "id1",
            "title"       : "title1",
            "author"      : "author1",
            "text"        : "text1",
            "contributor" : "user1",
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


def auth_header( user, pw ):
    info = base64.encodestring( "%s:%s" % ( user, pw ) )
    return {
        "Authorization": "Basic " + info
    }


def Can_add_new_poem_in_json__test():
    poem = {
        "title"  : "My New Poem",
        "author" : "Frank Black",
        "text"   : "Soda spoke\n  softly\nSoda\n"
    }

    # This is what we are testing - add a poem
    app = test_app()
    r = app.post(
        "/api/v1/poems",
        params=json.dumps( poem ),
        headers=auth_header( "user1", "pass1" )
    )
    assert_successful_json_response( r )

    # We should have responded with the id of the new poem
    newid = json.loads( r.body )
    assert_equal( "my-new-poem", newid )

    # And the database should have the poem added
    expected = copy( poem )
    expected["contributor"] = "user1"
    assert_equal( expected, app.fakedb.poems.data[newid] )


def Bad_password_prevents_add__test():
    r = test_app().post(
        "/api/v1/poems",
        params=json.dumps( { "title": "x" } ),
        headers=auth_header( "user1", "bad password" ),
        expect_errors=True
    )
    assert_equal( 401, r.status )


def No_login_prevents_add__test():
    r = test_app().post(
        "/api/v1/poems",
        params=json.dumps( { "title": "x" } ),
        headers={},
        expect_errors=True
    )
    assert_equal( 401, r.status )


def Can_replace_existing_poem_in_json__test():
    poem = {
        "title"   : "modtitle2",
        "author"  : "modauthor2",
        "text"    : "modtext2"
    }

    app = test_app()

    # Sanity - the original poem exists
    assert_equal( "title2", app.fakedb.poems.data["id2"]["title"] )

    # This is what we are testing - modify an existing poem
    r = app.put(
        "/api/v1/poems/id2",
        params=json.dumps( poem ),
        headers=auth_header( "user2", "pass2" )
    )
    assert_successful_json_response( r )

    # The response is empty
    assert_equal( "", json.loads( r.body ) )

    # The database should have new version of the poem
    expected = copy( poem )
    expected["contributor"] = "user2"
    assert_equal( expected, app.fakedb.poems.data["id2"] )


def Wrong_user_prevents_replace__test():
    r = test_app().put(
        "/api/v1/poems/id1",
        params=json.dumps( { "title": "x", "author": "x", "text": "x" } ),
        headers=auth_header( "user2", "pass2" ),
        expect_errors=True
    )
    print r
    assert_equal( 403, r.status )


def Bad_password_prevents_replace__test():
    r = test_app().put(
        "/api/v1/poems/id1",
        params=json.dumps( { "title": "x" } ),
        headers=auth_header( "user1", "bad password" ),
        expect_errors=True
    )
    assert_equal( 401, r.status )


def No_login_prevents_replace__test():
    r = test_app().put(
        "/api/v1/poems/id1",
        params=json.dumps( { "title": "x" } ),
        headers={},
        expect_errors=True
    )
    assert_equal( 401, r.status )


def Replacing_a_nonexistent_poem_returns_error_response__test():
    poem = { "title":"t", "author":"a", "text": "x" }

    # This is what we are testing
    r = test_app().put(
        "/api/v1/poems/nonexistentid",
        params=json.dumps( poem ),
        headers=auth_header( "user2", "pass2" ),
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
    r = app.delete(
        "/api/v1/poems/id3", headers=auth_header( "user3", "pass3" ) )

    assert_successful_json_response( r )

    # The response is empty
    assert_equal( "", json.loads( r.body ) )

    # The poem is gone
    assert_false( "id3" in app.fakedb.poems )


def Wrong_user_prevents_delete__test():
    r = test_app().delete(
        "/api/v1/poems/id1",
        headers=auth_header( "user2", "pass2" ),
        expect_errors=True
    )
    assert_equal( 403, r.status )


def Bad_password_prevents_delete__test():
    r = test_app().delete(
        "/api/v1/poems/id1",
        headers=auth_header( "user1", "bad password" ),
        expect_errors=True
    )
    assert_equal( 401, r.status )


def No_login_prevents_delete__test():
    r = test_app().delete(
        "/api/v1/poems/id1",
        headers={},
        expect_errors=True
    )
    assert_equal( 401, r.status )


def Deleting_a_nonexistent_poem_returns_error_response__test():
    # This is what we are testing
    r = test_app().delete(
        "/api/v1/poems/nonexistentid",
        headers=auth_header( "user2", "pass2" ),
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


def patch( app, url, params, headers, expect_errors=False ):
    return app.post(
        url,
        extra_environ={ "REQUEST_METHOD": "PATCH" },
        params=params,
        headers=headers,
        expect_errors=expect_errors
    )


def Can_amend_an_existing_poem__test():
    newprops = {
        "author": "Me",
        "text"  : "my peom\nis    misspelt.\n"
    }

    app = test_app()

    # This is what we are testing
    r = patch(
        app,
        "/api/v1/poems/id2",
        params=json.dumps( newprops ),
        headers=auth_header( "user2", "pass2" )
    )
    assert_successful_json_response( r )

    assert_equal(
        {
            "title"       : "title2",
            "author"      : "Me",
            "text"        : "my peom\nis    misspelt.\n",
            "contributor" : "user2",
        },
        app.fakedb.poems.data["id2"]
    )

def Amending_a_nonexistent_poem_returns_an_error__test():
    poem = { "title":"t" }

    # This is what we are testing
    r = patch(
        test_app(),
        "/api/v1/poems/nonexistentid",
        params=json.dumps( poem ),
        headers=auth_header( "user2", "pass2" ),
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


def Amending_with_a_bad_property_returns_an_error__test():
    poem = { "notaprop":"t" }

    # This is what we are testing
    r = patch(
        test_app(),
        "/api/v1/poems/id2",
        params=json.dumps( poem ),
        headers=auth_header( "user2", "pass2" ),
        expect_errors=True
    )

    # The request failed
    assert_failed_json_response( 400, r )

    # We received an error message
    assert_equal(
        {
            'error': '"notaprop" is not a valid property of a poem.'
        },
        json.loads( r.body )
    )


def Wrong_user_prevents_amend__test():
    r = patch(
        test_app(),
        "/api/v1/poems/id1",
        params=json.dumps( { "title": "x" } ),
        headers=auth_header( "user2", "pass2" ),
        expect_errors=True
    )
    assert_equal( 403, r.status )


def Bad_password_prevents_amend__test():
    r = patch(
        test_app(),
        "/api/v1/poems/id1",
        params=json.dumps( { "title": "x" } ),
        headers=auth_header( "user1", "bad password" ),
        expect_errors=True
    )
    assert_equal( 401, r.status )


def No_login_prevents_amend__test():
    r = patch(
        test_app(),
        "/api/v1/poems/id1",
        params=json.dumps( { "title": "x" } ),
        headers={},
        expect_errors=True
    )
    assert_equal( 401, r.status )


def No_login_prevents_logging_in__test():
    # This is what we are testing - try to log in,
    # but we fail because we provided no auth header
    app = test_app()
    r = app.get( "/api/v1/login", expect_errors=True )
    assert_equal( 401, r.status )


def Incorrect_login_prevents_logging_in__test():
    # This is what we are testing - try to log in,
    # but we fail because password is wrong.
    app = test_app()
    r = app.get(
        "/api/v1/login",
        headers=auth_header( "user1", "bad password" ),
        expect_errors=True,
    )
    assert_equal( 401, r.status )


def Correct_login_sets_a_cookie__test():
    # This is what we are testing - try to log in,
    # but we fail because password is wrong.
    app = test_app()
    r = app.get(
        "/api/v1/login",
        headers=auth_header( "user1", "pass1" )
    )
    assert_equal( 204, r.status )
    assert_true( "authentication_token" in r.cookies_set )


# TODO: error conditions:
#   - missing id for PUT/PATCH
#   - any id for POST
#   - non-JSON for POST/PUT/PATCH
#   - missing attributes for POST/PUT
#   - invalid/extra attributes for POST/PUT/PATCH

# TODO: features:
#   - avoid overwriting an old poem when posting a new one



