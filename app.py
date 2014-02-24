# from http://docs.python.org/2/library/wsgiref.html

from wsgiref.util import setup_testing_defaults
from urlparse import urlparse, parse_qs
import cgi
import StringIO
import jinja2

HEADER = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"
HEADER_404 = "HTTP/1.0 404 Not Found \r\nContent-type: text/html\r\n\r\n"

TemplateDir = "./templates"


jLdr = jinja2.FileSystemLoader(TemplateDir)
jEnv = jinja2.Environment(loader=jLdr)
    

def simple_app(environ, start_response):
##    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    
    if environ['REQUEST_METHOD'] == "POST":
##        ret = ["%s: %s\n" % (key, value)
##               for key, value in environ.iteritems()]
##        ret.insert(0, "This is your environ.  Hello, world!\n\n")
        ret = handle_post(environ, headers)
    elif environ['REQUEST_METHOD'] == "GET":
        ret = handle_get(environ)
        ret = str(ret)

    return ret

def make_app():
    return simple_app


def handle_get(environ):
    path = environ["PATH_INFO"]
    path = path.lstrip('/')

    formData = parse_qs(environ["QUERY_STRING"])

    if path == "":
        path = "index"

    path += ".html"
    
    try:
        ret = jEnv.get_template(path).render(formData)
    except jinja2.exceptions.TemplateNotFound:
        ret = error404(environ)

    return ret

def handle_post(environ, headers):
    path = environ["PATH_INFO"]
    path = path.lstrip('/')

    post_data = {}

    for key in environ["wsgi.input"].keys():
        post_data[key] = environ["wsgi.input"][key].value.split()        

    path += ".html"

    try:
        ret = jEnv.get_template(path).render(post_data)
    except jinja2.exceptions.TemplateNotFound:
        ret = error404(environ)

    return ret
    

def error404(environ):
    ret = jEnv.get_template("404.html").render()
    return ret

if __name__ == '__main__':
    main()
