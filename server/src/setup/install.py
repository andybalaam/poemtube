#!/usr/bin/env python

import argparse
import sys

from couchdb import PreconditionFailed, ResourceNotFound
from couchdb.client import Server

def delete_and_create_db( server, a, dbname ):
    dbn = a.prefix + dbname

    if a.delete:
        try:
            server.delete( dbn )
            print "Deleted database %s" % dbn
        except ResourceNotFound:
            pass

    try:
        server.create( dbn )
    except PreconditionFailed:
        sys.stderr.write(
            ( "Database %s already exists - run with " +
            "--delete to delete and recreate.\n" )
                % dbn
        )
        sys.exit( 1 )

    print "Created database %s" % dbn

parser = argparse.ArgumentParser()
parser.add_argument( "--prefix", default="" )
parser.add_argument( "--delete", default=False, action="store_true" )

a = parser.parse_args( sys.argv[1:] )

server = Server()

delete_and_create_db( server, a, "poems" )
delete_and_create_db( server, a, "tokens" )


