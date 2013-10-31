
from nose.tools import *

from fakedb import FakeDb

import poemtube.listpoems
from poemtube.errors import InvalidRequest

def Can_list_all_poems__test():
    answer = poemtube.listpoems( FakeDb() )
    assert_equal(
        set( ( "id1", "id2", "id3" ) ),
        set( answer )
    )

def Can_get_an_individual_poem__test():
    answer = poemtube.getpoem( FakeDb(), "id2" )

    assert_equal( "id2",     answer["id"] )
    assert_equal( "author2", answer["author"] )
    assert_equal( "title2",  answer["title"] )
    assert_equal( "text2",   answer["text"] )

def Can_add_a_new_poem__test():
    db = FakeDb()
    id = poemtube.addpoem(
        db, title="title X", author="author X", text="text X" )

    assert_equal( "title-x", id )

    newentry = db.poems[id]

    assert_equal( "title X", newentry["title"] )
    assert_equal( "author X", newentry["author"] )
    assert_equal( "text X", newentry["text"] )

def Id_is_all_lower_case__test():
    assert_equal(
                                    "hello",
        poemtube.make_id( FakeDb(), "HEllO" )
    )

def Id_replaces_spaces_with_dashes__test():
    assert_equal(
                                    "hello-world",
        poemtube.make_id( FakeDb(), "hello world" )
    )

def Id_replaces_nonalphanum_with_dashes__test():
    assert_equal(
                                      "hello-world----------------------------",
        poemtube.make_id( FakeDb(), """hello world?:{}[]"'+=-_)(*&^%$"!.,<>/@~""" )
    )

def Can_replace_an_existing_poem__test():
    db = FakeDb()
    poemtube.modifypoem(
        db, "id1", title="title X", author="author X", text="text X" )

    modentry = db.poems["id1"]

    assert_equal( "title X",  modentry["title"] )
    assert_equal( "author X", modentry["author"] )
    assert_equal( "text X",   modentry["text"] )

@raises( InvalidRequest )
def Replacing_a_nonexistent_poem_is_an_error__test():
    db = FakeDb()
    poemtube.modifypoem(
        db, "nonexistid", title="title X", author="author X", text="text X" )

