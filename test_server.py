import server
import requests
import jinja2


TemplateDir = "./templates"
    
ldr = jinja2.FileSystemLoader(TemplateDir)
env = jinja2.Environment(loader=ldr)



class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, env)

    assert "Welcome" in conn.sent , 'Got: %s' % (repr(conn.sent),)

def test_default_path():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
   
    server.handle_connection(conn, env)

    assert "Content" in conn.sent and "File" in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_content_path():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
   
    server.handle_connection(conn, env)

    assert "content" in conn.sent , 'Got: %s' % (repr(conn.sent),)

def test_file_path():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
   
    server.handle_connection(conn, env)

    assert "file" in conn.sent , 'Got: %s' % (repr(conn.sent),)

def test_image_path():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
   
    server.handle_connection(conn, env)

    assert "image" in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_form_get():
    conn =  FakeConnection("GET /submit?firstname=hello&lastname=world HTTP/1.0\r\n\r\n")


    server.handle_connection(conn, env)

    assert "Mr. hello world" in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_form_post():
    conn =  FakeConnection('POST /submit HTTP/1.1\r\n' +\
    'Host: arctic.cse.msu.edu:9176\r\n' +\
    'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20131030 Firefox/17.0 Iceweasel/17.0.10\r\n' +\
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n' +\
    'Accept-Language: en-US,en;q=0.5\r\n' +\
    'Accept-Encoding: gzip, deflate\r\n' +\
    'Connection: keep-alive\r\n' +\
    'Referer: http://arctic.cse.msu.edu:9176/formPost\r\n' +\
    'Content-Type: application/x-www-form-urlencoded\r\n' +\
    'Content-Length: 50\r\n' +\
    '\r\n' +\
    'firstname=hello&lastname=world&submit=Submit+Query\r\n')


    server.handle_connection(conn, env)

    assert "Mr. hello world" in conn.sent , 'Got: %s' % (repr(conn.sent),)

def test_form_post__multi():
    reqString = 'POST /submit HTTP/1.1\r\n' +\
	'Host: arctic.cse.msu.edu:9853\r\n' +\
	'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20131030 Firefox/17.0 Iceweasel/17.0.10\r\n' +\
	'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n' +\
	'Accept-Language: en-US,en;q=0.5\r\n' +\
	'Accept-Encoding: gzip, deflate\r\n' +\
	'Connection: keep-alive\r\n' +\
	'Referer: http://arctic.cse.msu.edu:9853/formPost\r\n'+\
	'Content-Type: multipart/form-data; boundary=---------------------------10925359777073771901781915428\r\n' +\
	'Content-Length: 422\r\n' +\
	'\r\n' +\
	'-----------------------------10925359777073771901781915428\r\n' +\
	'Content-Disposition: form-data; name="firstname"\r\n' +\
	'\r\n' +\
	'hello\r\n' +\
	'-----------------------------10925359777073771901781915428\r\n' +\
	'Content-Disposition: form-data; name="lastname"\r\n' +\
	'\r\n' +\
	'world\r\n' +\
	'-----------------------------10925359777073771901781915428\r\n' +\
	'Content-Disposition: form-data; name="submit"\r\n' +\
	'\r\n' +\
	'Submit Query\r\n' +\
	'-----------------------------10925359777073771901781915428--\r\n'
    conn = FakeConnection(reqString)
    server.handle_connection(conn, env)

    assert "Mr. hello world" in conn.sent, 'Wrong page: %s' % (repr(conn.sent),)

def test_404():
   conn = FakeConnection("GET /feiap HTTP/1.1\r\n\r\n")
   server.handle_connection(conn, env)

   assert "404 error" in conn.sent, "Got: %s" % (repr(conn.sent),)
