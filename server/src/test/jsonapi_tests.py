
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

def Can_get_single_poem__test():
    # This is what we are testing
    j = json_poems.GET( FakeDb(), "id3" )

    # Parse the answer - should be valid JSON
    ans = json.loads( j )

    assert_equal( "id3",     ans["id"] )
    assert_equal( "title3",  ans["title"] )
    assert_equal( "author3", ans["author"] )
    assert_equal( "text3",   ans["text"] )

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

    newpoem = {
        "title"  : "A Poem",
        "author" : "Andy Balaam",
        "text"   : "Sometimes, sometimes\nSometimes.\n"
    }
    json_poems.PUT( db, "id3", json.dumps( newpoem ) )

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




