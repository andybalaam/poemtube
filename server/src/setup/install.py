#!/usr/bin/env python

import argparse
import sys

from couchdb import PreconditionFailed, ResourceNotFound
from couchdb.client import Server

parser = argparse.ArgumentParser()
parser.add_argument( "--prefix", default="" )
parser.add_argument( "--delete", default=False, action="store_true" )

a = parser.parse_args( sys.argv[1:] )

poemsdbname = a.prefix + "poems"

server = Server()

if a.delete:
    try:
        server.delete( poemsdbname )
        print "Deleted database %s" % poemsdbname
    except ResourceNotFound:
        pass

try:
    server.create( poemsdbname )
except PreconditionFailed:
    sys.stderr.write(
        ( "Database %s already exists - run with " +
        "--delete to delete and recreate.\n" )
            % poemsdbname
    )
    sys.exit( 1 )

print "Created database %s" % poemsdbname

