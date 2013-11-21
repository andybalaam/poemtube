import json
import requests

from nose.tools import *

sample_data = [

    {
        "title": "A Question",
        "text":
            "A voice said, Look me in the stars\n" +
            "And tell me truly, men of earth,\n" +
            "If all the soul-and-body scars\n" +
            "Were not too much to pay for birth.\n",
        "author" : "Robert Frost"
    },

    {
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
]

def insert_sample_data():

    for doc in sample_data:
        r = requests.post(
            "http://0.0.0.0:8080/api/v1/poems",
            json.dumps( doc )
        )

        assert_equal( 200, r.status_code )

