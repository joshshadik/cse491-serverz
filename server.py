#!/usr/bin/env python 
import random
import socket
import time
from urlparse import urlparse, parse_qs
import cgi
import StringIO

from app import simple_app


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

    buf = StringIO.StringIO(data)
    line = buf.readline()
    while line != '\r\n':
        kv = line.split(': ', 1)
        headers[kv[0].lower()] = kv[1].strip('\r\n')
        line = buf.readline()

    environ = {}

    environ['REQUEST_METHOD'] = request.split(' ', 1)[0]
    environ['PATH_INFO'] = url.path
    environ['QUERY_STRING'] = url.query

    if environ['REQUEST_METHOD'] == "POST":
        environ['CONTENT_TYPE'] = headers['content-type']
        environ['CONTENT_LENGTH'] = headers['content-length']
        post_content = conn.recv(int(headers['content-length']))
        print post_content
        post_content = StringIO.StringIO(post_content)
        environ['wsgi.input'] = cgi.FieldStorage(fp = post_content, headers=headers, environ=environ)
    else:
        environ['CONTENT_LENGTH'] = '0'


    response_status = ""
    response_headers = {}
    
    def start_response(status, headers, exc_info=None):
        response_status = status
        response_headers = headers
            
        
    server_response = simple_app(environ, start_response)


    conn.send("HTTP/1.0 {0}\r\n".format(response_status))
    for header in response_headers:
        conn.send("{0}: {1}\r\n".format(header[0], header[1]))
    conn.send("\r\n")
    conn.send(server_response)
    conn.close()


if __name__ == '__main__':
    main()

