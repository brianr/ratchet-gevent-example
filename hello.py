"""
Sample Gevent application with Ratchet integration.
"""

import sys
import logging

from gevent.pywsgi import WSGIServer
import ratchet
import webob


# configure logging so that ratchet's log messages will appear
logging.basicConfig()


def application(environ, start_response):
    request = webob.Request(environ)
    status = '200 OK'

    headers = [('Content-Type', 'text/html')]

    start_response(status, headers)
    
    yield '<p>Hello world</p>'

    try:
        # will raise a NameError about 'bar' not being defined
        foo = bar
    except:
        # report full exception info
        ratchet.report_exc_info(sys.exc_info(), request)
        
        # and/or, just send a string message with a level
        ratchet.report_message("Here's a message", 'info', request)
    
        yield '<p>Caught an exception</p>'


# initialize ratchet with an access token and environment name
ratchet.init('YOUR_ACCESS_TOKEN', 'development')

# now start the wsgi server
WSGIServer(('', 8000), application).serve_forever()
