#!/usr/bin/env python

import requests

base_url = "http://0.0.0.0:8080/api/v1/"

r = requests.get( base_url + "poems/" )

fmt = "%-20s %-20s %s"

print( fmt % ( "ID", "AUTHOR", "TITLE" ) )
print( "=" * 80 )

for poem in r.json:
    print( fmt % ( poem['id'], poem['author'], poem['title'] ) )


