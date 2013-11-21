
import argparse

from poemtube.db import ExtCouchDb, MemoryDb
from poemtube.db import which_db

parser = argparse.ArgumentParser()
parser.add_argument( 'ip', default="8080" )
parser.add_argument( '--db', default="couch" )
parser.add_argument( '--prefix', default="" )

def process( argv ):
    args = parser.parse_args( argv )

    dbarg = args.db
    if dbarg == "couch":
        which_db.db = ExtCouchDb( args.prefix )
    elif dbarg == "memory":
        which_db.db = MemoryDb()
    else:
        raise Exception( "Unknown db type '%s'." % dbarg )


