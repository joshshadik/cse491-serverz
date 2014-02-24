#!/usr/bin/env python 
import random
import socket
import time
from urlparse import urlparse, parse_qs
import cgi
from StringIO import StringIO

from app import make_app

import quixote
# from quixote.demo import create_publisher
# from quixote.demo.mini_demo import create_publisher
from quixote.demo.altdemo import create_publisher

_the_app = None

##def make_app():
##    global _the_app
##
##    if _the_app is None:
##        p = create_publisher()
##        _the_app = quixote.get_wsgi_app()
##
##    return _the_app


def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port 
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()

        print 'Got connection from', client_host, client_port

        handle_connection(c)

def handle_connection(conn):
    received = ""

    while True:
        received = received + conn.recv(1)
        if received[-4:] == "\r\n\r\n":
            break

    request, data = received.split("\r\n", 1)

    url = urlparse(request.split(" ", 2)[1])

    headers = {}

    buf = StringIO(data)
    line = buf.readline()
    while line != '\r\n':
        kv = line.split(': ', 1)
        headers[kv[0].lower()] = kv[1].strip('\r\n')
        line = buf.readline()

    environ = {}

    environ['REQUEST_METHOD'] = request.split(' ', 1)[0]
    environ['PATH_INFO'] = url.path
    environ['QUERY_STRING'] = url.query
    environ['SCRIPT_NAME'] = ''

    
    content = ''
    if environ['REQUEST_METHOD'] == "POST":
        environ['CONTENT_TYPE'] = headers['content-type']
        environ['CONTENT_LENGTH'] = headers['content-length']
        while len(content) < int(headers['content-length']):
            content += conn.recv(1)
    else:
        environ['CONTENT_LENGTH'] = '0'


    environ['wsgi.input'] = StringIO(content)
    response_status = ""
    response_headers = {}
    
    def start_response(status, headers, exc_info=None):
        response_status = status
        response_headers = headers
            

    app = make_app()
    server_response = app(environ, start_response)


    conn.send("HTTP/1.0 {0}\r\n".format(response_status))
    for header in response_headers:
        conn.send("{0}: {1}\r\n".format(header[0], header[1]))
    conn.send("\r\n")
    for data in server_response:
        conn.send(data)
    conn.close()


if __name__ == '__main__':
    main()

