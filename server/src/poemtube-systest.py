#!/usr/bin/env python

# Launch poemtube server against a real local Couch DB, but
# with a table prefix set to avoid overwriting real data.
# Insert some sample data to facilitate testing.

import os
import sys
import web

from poemtube import urls
from poemtube.db import ExtCouchDb

import poemtube.db.which_db
import poemtube.sampledata

poemtube.db.which_db.db = ExtCouchDb( prefix="systest-" )
poemtube.sampledata.insert()

app = web.application( urls, globals() )

if __name__ == "__main__":
	app.run()


