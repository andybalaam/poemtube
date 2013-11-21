import web

from poemtube.config import read_config
from poemtube.db import ExtCouchDb, MemoryDb

read_config( web )

def _lookup( cfg, key, default ):
    if key in cfg:
        return cfg[key]
    else:
        return default

def _choose_db( cfg ):
    dbtype = _lookup( cfg, "db", "memory" )
    if dbtype == "memory":
        print "Using in-memory db"
        return MemoryDb()
    elif dbtype == "couch":
        prefix = _lookup( cfg, "prefix", "" )
        print "Using couchdb with prefix %s" % prefix
        return ExtCouchDb( prefix )
    else:
        raise Exception( "Unknown db type '%s'." % dbtype )

db = _choose_db( web.config.poemtube )

def get_db():
    global db

    if db is None:
        raise Exception( "No db set!" )

    return db

