
class MemoryDb( object ):
    def __init__( self ):
        self.poems = {}
        self.add_sample_data()

    def add_sample_data( self ):
        self.poems[ "a-question" ] = {
            "title": "A Question",
            "text":
                "A voice said, Look me in the stars\n" +
                "And tell me truly, men of earth,\n" +
                "If all the soul-and-body scars\n" +
                "Were not too much to pay for birth.\n",
            "author" : "Robert Frost"
        }

        self.poems[ "this-is-a-photo" ] = {
            "title": "This Is A Photograph Of Me",
            "text":
                "It was taken some time ago.\n" +
                "At first it seems to be\n" +
                "a smeared\n" +
                "print: blurred lines and grey flecks\n" +
                "blended with the paper;\n" +
                "\n" +
                "then, as you scan\n" +
                "it, you see in the left-hand corner\n" +
                "a thing that is like a branch: part of a tree\n" +
                "(balsam or spruce) emerging\n" +
                "and, to the right, halfway up\n" +
                "what ought to be a gentle\n" +
                "slope, a small frame house.\n" +
                "\n" +
                "In the background there is a lake,\n" +
                "and beyond that, some low hills.\n" +
                "\n" +
                "(The photograph was taken\n" +
                "the day after I drowned.\n" +
                "\n" +
                "I am in the lake, in the center\n" +
                "of the picture, just under the surface.\n" +
                "\n" +
                "It is difficult to say where\n" +
                "precisely, or to say\n" +
                "how large or small I am:\n" +
                "the effect of water\n" +
                "on light is a distortion\n" +
                "\n" +
                "but if you look long enough,\n" +
                "eventually\n" +
                "you will be able to see me.)\n",
            "author": "Margaret Atwood"
        }

