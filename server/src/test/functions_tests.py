
from nose.tools import *

from fakedb import FakeDb

import poemtube
from poemtube.errors import InvalidRequest

def Can_list_all_poems__test():
    answer = poemtube.listpoems( FakeDb() )
    assert_equal(
        set( ( "id1", "id2", "id3" ) ),
        set( answer )
    )

def Can_list_a_specified_number_of_poems__test():
    answer = poemtube.listpoems( FakeDb(), count=2 )
    assert_equal( 2, len( list( answer ) ) )

    answer = poemtube.listpoems( FakeDb(), count=1 )
    assert_equal( 1, len( list( answer ) ) )

def Listing_asking_for_too_many_returns_all__test():
    answer = poemtube.listpoems( FakeDb(), count=200 )
    assert_equal( 3, len( list( answer ) ) )

def Can_list_starting_after_an_id__test():
    answer = list( poemtube.listpoems( FakeDb(), since_id="id2" ) )
    # We don't know what order they will come back in, but even
    # if id2 is first, we'll get one less
    assert_true( len( answer ) < 3 )
    print answer
    assert_true( "id2" not in answer )


def Listing_asking_for_too_many_returns_all__test():
    answer = poemtube.listpoems( FakeDb(), count=200 )
    assert_equal( 3, len( list( answer ) ) )

@raises( InvalidRequest )
def Listing_asking_for_negative_is_an_error__test():
    poemtube.listpoems( FakeDb(), count=-1 )


def Searching_for_an_author_returns_their_poems__test():
    db = FakeDb()
    id1 = poemtube.addpoem(
        db, title="t1", author="fred 1", text="t1", user="user1" )
    id2 = poemtube.addpoem(
        db, title="t2", author="fred 2", text="t2", user="user1" )
    id3 = poemtube.addpoem(
        db, title="t3", author="fred 1", text="t3", user="user1" )
    id4 = poemtube.addpoem(
        db, title="t4", author="fred 3", text="t4", user="user1" )
    id5 = poemtube.addpoem(
        db, title="t5", author="fred 1", text="t5", user="user1" )

    # This is what we are testing
    answer = poemtube.listpoems( db, search="fred 1" )

    # Take the first 3 - theoretically there might be others
    first_3 = list( answer )[:3]

    # We got back the 3 poems by this author
    assert_equal( id1, first_3[0] )
    assert_equal( id3, first_3[1] )
    assert_equal( id5, first_3[2] )



def Can_get_an_individual_poem__test():
    answer = poemtube.getpoem( FakeDb(), "id2" )

    assert_equal( "id2",     answer["id"] )
    assert_equal( "author2", answer["author"] )
    assert_equal( "title2",  answer["title"] )
    assert_equal( "text2",   answer["text"] )

@raises( InvalidRequest )
def Getting_a_nonexistent_poem_is_an_error__test():
    poemtube.getpoem( FakeDb(), "nonexistentid" )

def Can_add_a_new_poem__test():
    db = FakeDb()
    id = poemtube.addpoem(
        db,
        title="title X",
        author="author X",
        text="text X",
        user="user1"
    )

    assert_equal( "title-x", id )

    newentry = db.poems.data[id]

    assert_equal( "title X", newentry["title"] )
    assert_equal( "author X", newentry["author"] )
    assert_equal( "text X", newentry["text"] )

@raises( InvalidRequest )
def Adding_a_poem_not_logged_in_is_an_error__test():
    db = FakeDb()
    poemtube.addpoem( db, "X", "X", "X", user=None )

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
    poemtube.replacepoem(
        db,
        "id1",
        title="title X",
        author="author X",
        text="text X",
        user="user1"
    )

    modentry = db.poems.data["id1"]

    assert_equal( "title X",  modentry["title"] )
    assert_equal( "author X", modentry["author"] )
    assert_equal( "text X",   modentry["text"] )
    assert_equal( "user1",    modentry["contributor"] )

@raises( InvalidRequest )
def Replacing_a_poem_contributed_by_someone_else_is_an_error():
    db = FakeDb()
    poemtube.replacepoem(
        db, "id1", title="X", author="X", text="X", user="user2" )

@raises( InvalidRequest )
def Replacing_a_poem_not_logged_in_is_an_error():
    db = FakeDb()
    poemtube.replacepoem(
        db, "id1", title="X", author="X", text="X", user=None )

@raises( InvalidRequest )
def Replacing_a_nonexistent_poem_is_an_error__test():
    db = FakeDb()
    poemtube.replacepoem(
        db,
        "nonexistid",
        title="title X",
        author="author X",
        text="text X",
        user="user1"
    )

def Can_delete_a_poem__test():
    db = FakeDb()

    # Sanity - id1 exists
    assert_true( "id1" in db.poems )

    # This is what we are testing - delete the item
    poemtube.deletepoem( db, "id1", user="user1" )

    # It has gone
    assert_false( "id1" in db.poems )

@raises( InvalidRequest )
def Deleting_a_poem_not_contributed_by_you_is_an_error__test():
    db = FakeDb()
    poemtube.deletepoem( db, "id1", user="user2" )

@raises( InvalidRequest )
def Deleting_a_nonexistent_poem_is_an_error__test():
    db = FakeDb()
    poemtube.deletepoem( db, "nonexistid", user="user1" )

def Can_amend_a_poem_title__test():
    db = FakeDb()

    # Sanity - before modifying
    assert_equal(
        {
            "title"       : "title1",
            "author"      : "author1",
            "text"        : "text1",
            "contributor" : "user1"
        },
        db.poems.data["id1"]
    )

    # This is what we are testing
    poemtube.amendpoem( db, "id1", { "title": "title X" }, user="user1" )

    # Title changed
    assert_equal(
        {
            "title"       : "title X",
            "author"      : "author1",
            "text"        : "text1",
            "contributor" : "user1"
        },
        db.poems.data["id1"]
    )

def Can_amend_a_poem_author__test():
    db = FakeDb()

    # This is what we are testing
    poemtube.amendpoem( db, "id1", { "author": "author X" }, user="user1" )

    # Title changed
    assert_equal(
        {
            "title"       : "title1",
            "author"      : "author X",
            "text"        : "text1",
            "contributor" : "user1"
        },
        db.poems.data["id1"]
    )

def Can_amend_a_poem_text__test():
    db = FakeDb()

    # This is what we are testing
    poemtube.amendpoem( db, "id2", { "text": "text X" }, user="user2" )

    # Title changed
    assert_equal(
        {
            "title"       : "title2",
            "author"      : "author2",
            "text"        : "text X",
            "contributor" : "user2"
        },
        db.poems.data["id2"]
    )


def Can_amend_a_poem_multiple__test():
    db = FakeDb()

    # This is what we are testing
    poemtube.amendpoem(
        db, "id1", { "text": "text X", "author": "author X" }, user="user1" )

    # Title changed
    assert_equal(
        {
            "title"       : "title1",
            "author"      : "author X",
            "text"        : "text X",
            "contributor" : "user1"
        },
        db.poems.data["id1"]
    )


@raises( InvalidRequest )
def Attempting_to_change_contributor_is_an_error__test():
    poemtube.amendpoem(
        FakeDb(), "id1", { "text": "t", "contributor": "foo" }, user="user1" )

@raises( InvalidRequest )
def Amending_using_unknown_property_is_an_error__test():
    poemtube.amendpoem(
        FakeDb(), "id1", { "text": "t", "badprop": "foo" }, user="user1" )


@raises( InvalidRequest )
def Amending_an_unknown_id_is_an_error__test():
    poemtube.amendpoem( FakeDb(), "unknown", { "text": "t" }, user="user1" )


@raises( InvalidRequest )
def Amending_someone_elses_poem_is_an_error__test():
    poemtube.amendpoem( FakeDb(), "id1", { "text": "t" }, user="user2" )


@raises( InvalidRequest )
def Amending_not_logged_in_is_an_error__test():
    poemtube.amendpoem( FakeDb(), "id1", { "text": "t" }, user=None )

