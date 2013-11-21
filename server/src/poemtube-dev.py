#!/usr/bin/env python

import os
import sys
import web

from poemtube import urls

app = web.application( urls, globals() )

if __name__ == "__main__":
	app.run()


