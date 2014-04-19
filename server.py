#!/usr/bin/env python 
import random
import socket
import time
from urlparse import urlparse, parse_qs
import cgi
from StringIO import StringIO

import argparse

from app import make_app
import quixote
# from quixote.demo import create_publisher
# from quixote.demo.mini_demo import create_publisher
from quixote.demo.altdemo import create_publisher
import imageapp
import imageappflask
from quotes.apps import QuotesApp 
from chat.apps import ChatApp 
import cookieapp

apps = ['image', 'altdemo', 'myapp', 'quotes', 'chat', 'flask', 'cookie']

_the_app = None


def make_imageapp():
    imageapp.setup()
    p = imageapp.create_publisher()
    return quixote.get_wsgi_app() 

def make_altdemo():
    create_publisher()
    return quixote.get_wsgi_app()

def make_flask():
    return imageappflask.get_wsgi_app()

def main():
    global _the_app
    parser = argparse.ArgumentParser()
    parser.add_argument('-A', default = apps[0], choices = apps, help = 'Select app to run.')
    parser.add_argument('-p', default=10000, type=int, help = 'Select a port to run on.')
    args = parser.parse_args()

    if args.A == 'image':
        _the_app = make_imageapp()
    elif args.A == 'altdemo':
        _the_app = make_altdemo()
    elif args.A == 'myapp':
        _the_app = make_app()
    elif args.A == 'quotes':
        _the_app = QuotesApp('quotes/quotes.txt', './quotes/html')
    elif args.A == 'chat':
        _the_app = ChatApp('./chat/html')
    elif args.A == 'flask':
        _the_app = make_flask()
    elif args.A == 'cookie':
        _the_app = cookieapp.wsgi_app


    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
   
    if args.p == 10000:
        port = random.randint(8000, 9999)
    else:
        port = args.p

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

    received = conn.recv(1)

    if len(received) == 0:
        return
 
    # print received

    while '\r\n\r\n' not in received:
        received += conn.recv(1)

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
    environ['SERVER_NAME'] = "{0}".format(conn.getsockname()[0])
    environ['SERVER_PORT'] = "{0}".format(conn.getsockname()[1])
    environ['CONTENT_TYPE'] = 'text/html'
    environ['wsgi.version'] = ('',)
    environ['wsgi.errors'] = StringIO()
    environ['wsgi.multithread'] = 0
    environ['wsgi.multiprocess'] = 0
    environ['wsgi.run_once'] = 0
    environ['wsgi.url_scheme'] = 'http'

    
    content = ''
    if environ['REQUEST_METHOD'] == "POST":
        environ['CONTENT_TYPE'] = headers['content-type']
        environ['CONTENT_LENGTH'] = headers['content-length']
        while len(content) < int(headers['content-length']):
            content += conn.recv(1)
    else:
        environ['CONTENT_LENGTH'] = '0'

    if 'cookie' in headers.keys():
        environ['HTTP_COOKIE'] = headers['cookie']

    environ['wsgi.input'] = StringIO(content)

    
    def start_response(status, headers, exc_info=None):
        conn.send("HTTP/1.0 {0}\r\n".format(status))
        for header in headers:
            conn.send("{0}: {1}\r\n".format(header[0], header[1]))
        conn.send("\r\n")


            
    if _the_app is not None:
        app = _the_app 
    else:
        app = make_app()
    server_response = app(environ, start_response)



    for data in server_response:
        conn.send(data)
    conn.close()


if __name__ == '__main__':
    main()

