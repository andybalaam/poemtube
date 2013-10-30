
from nose.tools import *

from fakedb import FakeDb

import poemtube.listpoems

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

