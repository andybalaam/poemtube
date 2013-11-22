#!/usr/bin/env python

# Launch poemtube server with an in-memory database that is
# populated with some sample data every time we launch
# (i.e. any poems you add will be lost when this process stops.)

import os
import sys
import web

from poemtube import urls
from poemtube.db import MemoryDb

import poemtube.db.which_db
import poemtube.sampledata

poemtube.db.which_db.db = MemoryDb()
poemtube.sampledata.insert()

app = web.application( urls, globals() )

if __name__ == "__main__":
	app.run()


