import server
import requests

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
    expected_return = server.connHeader + server.defaultHtml
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_default_path():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = server.connHeader + server.defaultHtml
   
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_content_path():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = server.connHeader + server.contentHtml
   
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_file_path():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = server.connHeader + server.fileHtml
   
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_image_path():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = server.connHeader + server.imageHtml
   
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")

    expected_return = "hello world" 
   
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


