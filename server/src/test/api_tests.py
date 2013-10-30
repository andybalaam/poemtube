
from nose.tools import *
import json

from fakedb import FakeDb

from poemtube.api.v1 import Poems

def Can_list_poems_in_json__test():
    handler = Poems( FakeDb() )

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

def Can_list_poems_in_json_with_slash_in_url__test():
    handler = Poems( FakeDb() )

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

def Can_get_single_poem_in_json__test():
    handler = Poems( FakeDb() )

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


