# from http://docs.python.org/2/library/wsgiref.html

from wsgiref.util import setup_testing_defaults
from urlparse import urlparse, parse_qs
import cgi
import StringIO
import jinja2
from wsgiref.validate import validator

HEADER = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n"
HEADER_404 = "HTTP/1.0 404 Not Found \r\nContent-type: text/html\r\n\r\n"

TemplateDir = "./templates"


jLdr = jinja2.FileSystemLoader(TemplateDir)
jEnv = jinja2.Environment(loader=jLdr)
    

def simple_app(environ, start_response):

        
    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    if environ['REQUEST_METHOD'] == "POST":
        ret = handle_post(environ, headers)
    elif environ['REQUEST_METHOD'] == "GET":
        ret, headers = handle_get(environ)
        ret = str(ret)

    start_response(status, headers)

    return [ret]

def make_app():
    return validator(simple_app)


def handle_get(environ):
    path = environ["PATH_INFO"]
    path = path.lstrip('/')

    headers = [('Content-type', 'text/html')]
    
    formData = parse_qs(environ["QUERY_STRING"])

    if "firstname" not in formData.keys():
        formData["firstname"] = ["",]
        
    if "lastname" not in formData.keys():
        formData["lastname"] = ["",]

    if path == "":
        path = "index"

    if path == "image":
        headers = [('Content-type', 'image/jpeg')]
        fp = open("image.jpg", "rb")
        ret = fp.read()
        fp.close()
    elif path == "file":
        headers = [('Content-type', 'text/plain')]
        fp = open("file.txt", "rb")
        ret = fp.read()
        fp.close()       
    else:
        path += ".html"
        
        try:
            ret = jEnv.get_template(path).render(formData)
        except jinja2.exceptions.TemplateNotFound:
            ret = error404(environ)

    return ret, headers

def handle_post(environ, headers):
    path = environ["PATH_INFO"]
    path = path.lstrip('/')

    post_data = {}

    formData =  cgi.FieldStorage(fp = environ['wsgi.input'], headers=headers, environ=environ)

    if "firstname" not in formData.keys():
        post_data["firstname"] = ["",]
        
    if "lastname" not in formData.keys():
        post_data["lastname"] = ["",]
        
    for key in formData.keys():
        post_data[key] = formData[key].value.split()

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
