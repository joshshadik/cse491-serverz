#!/usr/bin/env python 
import random
import socket
import time
from urlparse import urlparse, parse_qs
import cgi
import StringIO
import jinja2

HEADER = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"
HEADER_404 = "HTTP/1.0 404 Not Found \r\nContent-type: text/html\r\n\r\n"

TemplateDir = "./templates"


def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    ldr = jinja2.FileSystemLoader(TemplateDir)
    env = jinja2.Environment(loader=ldr)

    print 'Starting server on', host, port 
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()

        print 'Got connection from', client_host, client_port

        handle_connection(c)

def signal_handler(signum, frame):
    raise Exception("Timed out")

def handle_connection(conn):
    rcvData = ""

    while True:
        rcvData = rcvData + c.recv(1)
        if rcvData[-4:] == "\r\n\r\n":
            break


    received = rcvData.split(" ", 2)
    type = received[0]

    if len(received) < 2:
        return


    if type == "POST":
        srvRsp = handle_post(rcvData, env, c)
    else:
        srvRsp = handle_get(rcvData, env)

    c.send(srvRsp)
    c.close()

def handle_get(rcvData, env):
    data = urlparse(rcvData.split(" ", 2)[1])
    path = data.path
    path = path.lstrip('/')

    formData = parse_qs(data.query)

    if path == "":
        path = "index"
    elif path =="submit":
        return submitGet(formData, env)

    path += ".html"
   
    print path

    try:
        srvRsp = HEADER + env.get_template(path).render()
    except jinja2.exceptions.TemplateNotFound:
        srvRsp = error404(env)

    return srvRsp

def handle_post(rcvData, env, c):
    path = urlparse(rcvData.split(" ", 2)[1]).path
    path = path.lstrip('/')

    reqFS = createPostFS(rcvData, c)


    path += "Post.html"

    try:
        srvRsp = HEADER + env.get_template(path).render(reqFS)
    except jinja2.exceptions.TemplateNotFound:
        srvRsp = error404( env)

    return srvRsp



# initialize field storage object based on request data
# specialized for post method
def createPostFS(reqData, c): # credit to Minh Pham
    buf = StringIO.StringIO(reqData)

    headers = {}

    buf.readline()
    line = buf.readline()

    while line != '\r\n':
        print line.split(': ', 1)
        kv = line.split(': ', 1)
        headers[kv[0].lower()] = kv[1].strip('\r\n')
        line = buf.readline()

    if 'content-length' in headers.keys():
        buf  = StringIO.StringIO(c.recv(int(headers['content-length'])))
   
    env = {}

    env['REQUEST_METHOD'] = 'POST'

    # credit to Maxwell Brown and Xavier Durand-Hollis
    formFS = cgi.FieldStorage(fp = buf, headers=headers, environ=env)

    return formFS
    

def submitGet(formData, env):
    srvRsp = HEADER + env.get_template("submit.html").render(formData)
    return srvRsp

def error404(env):
    srvRsp = HEADER_404 + env.get_template("404.html").render()
    return srvRsp

if __name__ == '__main__':
    main()

