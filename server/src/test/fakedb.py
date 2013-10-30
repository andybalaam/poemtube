

class FakeDb( object ):
    def __init__( self ):
        self.poems = {
            "id1" : {
                "author" : "author1",
                "title"  : "title1",
                "text"   : "text1",
            },
            "id2" : {
                "author" : "author2",
                "title"  : "title2",
                "text"   : "text2",
            },
            "id3" : {
                "author" : "author3",
                "title"  : "title3",
                "text"   : "text3",
            }
        }

