#!/usr/bin/env python

import requests
import sys
import urllib

base_url = "http://0.0.0.0:8080/api/v1/"

id = sys.argv[1]

r = requests.get( base_url + "poems/" + urllib.quote( id ) )

poem = r.json

print( poem['title'] )
print( "=" * len( poem['title'] ) )
print( "by %s" % poem['author'] )
print

print( poem['text'] )

