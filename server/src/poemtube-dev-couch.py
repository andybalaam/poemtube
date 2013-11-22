#!/usr/bin/env python

# Launch poemtube server against a real local couch database

import os
import sys
import web

from poemtube import urls
from poemtube.db import ExtCouchDb

import poemtube.db.which_db

poemtube.db.which_db.db = ExtCouchDb()

app = web.application( urls, globals() )

if __name__ == "__main__":
	app.run()


