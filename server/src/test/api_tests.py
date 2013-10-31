
from nose.tools import *
import json

from fakedb import FakeDb
from fakeweb import FakeWeb

from poemtube.api.v1 import Poems

def Can_list_poems_in_json__test():
    fakeweb = FakeWeb()
    handler = Poems( FakeDb(), fakeweb )

    # This is what we are testing - list poems in JSON
    answer = handler.GET( "" )

    # The answer should be valid JSON
    lst = json.loads( answer )

    # But not in a guaranteed order
    lst.sort()

    # It should be a list of ids
    assert_equal(
        ["id1", "id2", "id3"],
        lst
    )

    # We set the content type correctly
    assert_equal(
        "application/json",
        fakeweb.headers["Content-Type"]
    )


def Can_list_poems_in_json_with_slash_in_url__test():
    fakeweb = FakeWeb()
    handler = Poems( FakeDb(), fakeweb )

    # This is what we are testing - list poems in JSON
    answer = handler.GET( "/" )

    # The answer should be valid JSON
    lst = json.loads( answer )

    # But not in a guaranteed order
    lst.sort()

    # It should be a list of ids
    assert_equal(
        ["id1", "id2", "id3"],
        lst
    )

    # We set the content type correctly
    assert_equal(
        "application/json",
        fakeweb.headers["Content-Type"]
    )

def Can_get_single_poem_in_json__test():
    fakeweb = FakeWeb()
    handler = Poems( FakeDb(), fakeweb )

    # This is what we are testing - get a poem
    jans = handler.GET( "/id1" )

    # The answer should be valid JSON
    ans = json.loads( jans )

    # It should be a list of ids
    assert_equal(
        {
            "id"     : "id1",
            "title"  : "title1",
            "author" : "author1",
            "text"   : "text1",
        },
        ans
    )

    assert_equal(
        "application/json",
        fakeweb.headers["Content-Type"]
    )

def Can_add_new_poem_in_json__test():
    fakeweb = FakeWeb()
    fakedb = FakeDb()
    handler = Poems( fakedb, fakeweb )

    poem = {
        "title"  : "My New Poem",
        "author" : "Frank Black",
        "text"   : "Soda spoke\n  softly\nSoda\n"
    }

    fakeweb.inp = json.dumps( poem )

    # This is what we are testing - add a poem
    jans = handler.POST( "/" )

    # The answer should be valid JSON
    ans = json.loads( jans )

    # It should be the id of the new poem
    assert_equal( "my-new-poem", ans )

    # And the database should have the poem added
    assert_equal( poem, fakedb.poems[ans] )


# TODO: error conditions:
#   - bad id for GET/PUT/PATCH
#   - missing id for PUT/PATCH
#   - any id for POST
#   - non-JSON for POST/PUT/PATCH
#   - missing attributes for POST/PUT
#   - invalid/extra attributes for POST/PUT/PATCH

# TODO: features:
#   - avoid overwriting an old poem when posting a new one



