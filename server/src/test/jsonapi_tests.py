
from nose.tools import *
import json

from fakedb import FakeDb

from poemtube.jsonapi import json_poems
from poemtube.jsonapi.json_errors import JsonInvalidRequest

def Can_list_poems__test():
    # This is what we are testing
    j = json_poems.GET( FakeDb(), "" )

    # Parse it and sort the answer
    lst = json.loads( j )
    lst.sort()

    assert_equal(
        ["id1", "id2", "id3"],
        lst
    )

def Can_list_n_poems__test():
    # This is what we are testing
    j = json_poems.GET( FakeDb(), "", { "count": "2" } )

    # We got back the number we asked for
    lst = json.loads( j )
    assert_equal( 2, len( lst ) )

def Nonnumeric_count_is_an_error__test():
    caught_exception = None
    try:
        json_poems.GET( FakeDb(), "", { "count": "2foo" } )
    except JsonInvalidRequest, e:
        caught_exception = e

    assert_is_not_none( caught_exception )

    assert_equal(
        { 'error': '"2foo" is an invalid value for count.' },
        json.loads( str( caught_exception ) )
    )

    assert_equal( 400, caught_exception.suggested_code )

def Negative_count_is_an_error__test():
    caught_exception = None
    try:
        json_poems.GET( FakeDb(), "", { "count": "-2" } )
    except JsonInvalidRequest, e:
        caught_exception = e

    assert_is_not_none( caught_exception )

    assert_equal(
        { 'error': '"-2" is an invalid value for count.' },
        json.loads( str( caught_exception ) )
    )

    assert_equal( 400, caught_exception.suggested_code )

def Can_get_single_poem__test():
    # This is what we are testing
    j = json_poems.GET( FakeDb(), "id3" )

    # Parse the answer - should be valid JSON
    ans = json.loads( j )

    assert_equal( "id3",     ans["id"] )
    assert_equal( "title3",  ans["title"] )
    assert_equal( "author3", ans["author"] )
    assert_equal( "text3",   ans["text"] )

def Getting_a_nonexistent_poem_is_an_error__test():
    caught_exception = None
    try:
        json_poems.GET( FakeDb(), "nonexistid" )
    except JsonInvalidRequest, e:
        caught_exception = e

    assert_is_not_none( caught_exception )

    assert_equal(
        { 'error': '"nonexistid" is not the ID of an existing poem.' },
        json.loads( str( caught_exception ) )
    )

    assert_equal( 404, caught_exception.suggested_code )


def Can_add_a_new_poem__test():
    db = FakeDb()
    newpoem = {
        "title"  : "A Poem",
        "author" : "Andy Balaam",
        "text"   : "Sometimes, sometimes\nSometimes.\n"
    }
    j = json_poems.POST( db, json.dumps( newpoem ) )

    id = json.loads( j )
    assert_equals( "a-poem", id )

    assert_equals(
        "A Poem",
        db.poems[id]["title"]
    )

    assert_equals(
        "Andy Balaam",
        db.poems[id]["author"]
    )

    assert_equals(
        "Sometimes, sometimes\nSometimes.\n",
        db.poems[id]["text"]
    )


def Can_replace_an_existing_poem__test():
    db = FakeDb()

    # Sanity - poem exists
    assert_equal( "title3", db.poems["id3"]["title"] )

    newpoem = {
        "title"  : "A Poem",
        "author" : "Andy Balaam",
        "text"   : "Sometimes, sometimes\nSometimes.\n"
    }

    # This is what we are testing
    json_poems.PUT( db, "id3", json.dumps( newpoem ) )

    # The poem was replaced with what we supplied
    assert_equal( newpoem, db.poems.data["id3"] )


def Replacing_an_invalid_id_is_an_error__test():
    db = FakeDb()

    newpoem = {
        "title"  : "A Poem",
        "author" : "Andy Balaam",
        "text"   : "Sometimes, sometimes\nSometimes.\n"
    }
    caught_exception = None
    try:
        json_poems.PUT( db, "nonexistid", json.dumps( newpoem ) )
    except JsonInvalidRequest, e:
        caught_exception = e

    assert_is_not_none( caught_exception )

    assert_equal(
        { 'error': '"nonexistid" is not the ID of an existing poem.' },
        json.loads( str( caught_exception ) )
    )

    assert_equal( 404, caught_exception.suggested_code )


def Can_delete_an_existing_poem__test():
    db = FakeDb()

    # Sanity - poem exists
    assert_equal( "title1", db.poems["id1"]["title"] )

    # This is what we are testing
    json_poems.DELETE( db, "id1" )

    # It no longer exists
    assert_false( "id1" in db.poems )


def Deleting_an_invalid_id_is_an_error__test():
    caught_exception = None
    try:
        json_poems.DELETE( FakeDb(), "nonexistid" )
    except JsonInvalidRequest, e:
        caught_exception = e

    assert_is_not_none( caught_exception )

    assert_equal(
        { 'error': '"nonexistid" is not the ID of an existing poem.' },
        json.loads( str( caught_exception ) )
    )

    assert_equal( 404, caught_exception.suggested_code )


def Can_amend_an_existing_poem__test():
    db = FakeDb()

    # Sanity
    assert_equal( "title1", db.poems["id1"]["title"] )

    mods = {
        "title"  : "A Poem",
        "text"   : "Sometimes, sometimes\nSometimes.\n"
    }

    # This is what we are testing
    json_poems.PATCH( db, "id1", json.dumps( mods ) )

    # The poem was replaced with what we supplied
    assert_equal(
        {
            "title"  : "A Poem",
            "author" : "author1",
            "text"   : "Sometimes, sometimes\nSometimes.\n"
        },
        db.poems.data["id1"]
    )


def Amending_with_invalid_properties_is_an_error__test():
    db = FakeDb()

    newprops = {
        "foo" : "Andy Balaam"
    }

    caught_exception = None
    try:
        json_poems.PATCH( db, "id3", json.dumps( newprops ) )
    except JsonInvalidRequest, e:
        caught_exception = e

    assert_is_not_none( caught_exception )

    assert_equal(
        { 'error': '"foo" is not a valid property of a poem.' },
        json.loads( str( caught_exception ) )
    )

    assert_equal( 400, caught_exception.suggested_code )


def Amending_an_invalid_id_is_an_error__test():
    db = FakeDb()

    newpoem = {
        "title"  : "A Poem"
    }
    caught_exception = None
    try:
        json_poems.PATCH( db, "nonexistid", json.dumps( newpoem ) )
    except JsonInvalidRequest, e:
        caught_exception = e

    assert_is_not_none( caught_exception )

    assert_equal(
        { 'error': '"nonexistid" is not the ID of an existing poem.' },
        json.loads( str( caught_exception ) )
    )

    assert_equal( 404, caught_exception.suggested_code )



