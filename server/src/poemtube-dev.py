#!/usr/bin/env python

import sys
import web

from poemtube.urls import urls

app = web.application( urls, globals() )

if __name__ == "__main__":
	app.run()


