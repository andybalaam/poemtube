#!/usr/bin/env python

import sys
import web

from poemtube import urls, args

app = web.application( urls, globals() )

args.process( sys.argv[1:] )

if __name__ == "__main__":
	app.run()


