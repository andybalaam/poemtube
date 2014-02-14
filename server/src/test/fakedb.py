from poemtube.db import MemoryDb

class FakeDb( MemoryDb ):
    def __init__( self ):
        MemoryDb.__init__( self )
        self.poems.data = {
            "id1" : {
                "author"      : "author1",
                "title"       : "title1",
                "text"        : "text1",
                "contributor" : "user1"
            },
            "id2" : {
                "author"      : "author2",
                "title"       : "title2",
                "text"        : "text2",
                "contributor" : "user2"
            },
            "id3" : {
                "author"      : "author3",
                "title"       : "title3",
                "text"        : "text3",
                "contributor" : "user3"
            }
        }

