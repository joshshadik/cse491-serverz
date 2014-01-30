#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs

connHeader = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"
error404 = "HTTP/1.0 404 Not Found \r\nContent-type: text/html\r\n\r\n 404 Error. Page Not Found."
defaultHtml = "<ul><li><a href='/content'>content</a></li><li><a href='/file'>file</a></li><li><a href='/image'>image</a></li><li><a href='/form'>form</a></li></ul>"
contentHtml = "<h1>Hello, world.</h1>This is shadikjo\'s content path."
fileHtml = "<h1>Hello, world.</h1>This is shadikjo\'s file path."
imageHtml = "<h1>Hello, world.</h1>This is shadikjo\'s image path."
formHtml = """<form action='/submit' method='POST'>
<input type='text' name='firstname'>
<input type='text' name='lastname'>
<input type='submit'>
</form>"""
submitHtml = "Hello, Mr. %s %s."

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
    rcvData = c.recv(1000)
    received = rcvData.split(" ", 2)
    type = received[0]

    if len(received) < 2:
        return


    if type == "POST":
        handle_post(c, rcvData)
    else:
        handle_get(c, rcvData)

    c.close()

def handle_get(c, rcvData):
    data = urlparse(rcvData.split(" ", 2)[1])
    path = data.path
    formData = parse_qs(data.query)

    print rcvData.split(" ", 2)[1]

    if path == "/content":
        content(c, formData) 
    elif path == "/file":
        file(c, formData) 
    elif path == "/image":
        image(c, formData)        
    elif path == "/":
        index(c, formData) 
    elif path == "/form":
        form(c, formData)
    elif path == "/submit":
        submit(c, formData)
    else:
        c.send(error404)

def handle_post(c, rcvData):
    path = urlparse(rcvData.split(" ", 2)[1]).path

    print rcvData 

    if path == "/submit":
        formData = parse_qs(rcvData.split('\n')[-1])
        submit(c, formData)

def index(c, formData):
    c.send(connHeader)
    c.send(defaultHtml)

def content(c, formData):
    c.send(connHeader)
    c.send(contentHtml)

def file(c, formData):
    c.send(connHeader)
    c.send(fileHtml)

def image(c, formData):
    c.send(connHeader)
    c.send(imageHtml)

def form(c, formData):
    c.send(connHeader)
    c.send(formHtml)

def submit(c, formData):
    c.send(connHeader)
    c.send(submitHtml % (formData["firstname"][0], formData["lastname"][0]))

if __name__ == '__main__':
    main()

