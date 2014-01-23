#!/usr/bin/env python
import random
import socket
import time


connHeader = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"
defaultHtml = "<ul><li><a href='/content'>content</a></li><li><a href='/file'>file</a></li><li><a href='/image'>image</a></li></ul>" 
contentHtml = "<h1>Hello, world.</h1>This is shadikjo\'s content path."
fileHtml = "<h1>Hello, world.</h1>This is shadikjo\'s file path."
imageHtml = "<h1>Hello, world.</h1>This is shadikjo\'s image path."


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


def handle_connection(c):
    received = c.recv(1000)
    received = received.split(" ", 2)
    # print received[0]
    type = received[0]

    if type == "POST":
        c.send("hello world")
        c.close()
        return

    if len(received) < 2:
        return 
    path = received[1] 
    # print path
    if path == "/content":
        c.send(connHeader)
        c.send(contentHtml)
    elif path == "/file":
        c.send(connHeader)
        c.send(fileHtml)
    elif path == "/image":
        c.send(connHeader)
        c.send(imageHtml)
    else:
        c.send(connHeader)
        c.send(defaultHtml)

    c.close()


if __name__ == '__main__':
    main()
