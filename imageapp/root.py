import quixote
from quixote.directory import Directory, export, subdir
from quixote.util import StaticFile
from quixote.session import SessionManager, Session
import os.path

from . import html, image

class RootDirectory(Directory):
    _q_exports = []


    @export(name='')                    # this makes it public.
    def index(self):
        
        # if not self.sessionManager.has_session_cookie():            
        #     session = self.sessionManager.new_session(self.sessionManager._make_session_id())
        #     self.sessionManager.maintain_session(session)
        #     self.sessionManager.set_session_cookie(session.id)
        #     print "creating session"
        # else:
        #     session = self.sessionManager.get_session()
        #     print "has session already"

        session = quixote.get_session()

        # self.sessionManager.get_session()
        # session = self.sessionManager.get_session()
        # self.sessionManager.maintain_session(session)
        # session = self.sessionManager.get_session()
        if session is not None:
            print session.id

        return html.render('index.html')

    @export(name="jquery")
    def jquery(self):
        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname,"")
        jquery_path = os.path.join(dirname,'jquery-1.3.2.min.js')
        return open(jquery_path).read()

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        name = request.form["image_name"]
        description = request.form["image_description"]

        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image.add_image(data, name, description)

        # return quixote.redirect('./image')

        return html.render('image.html', {'image_name' : image.get_latest_image()[1], 'image_description' : image.get_latest_image()[2]})

    @export(name='upload_temp')
    def upload_temp(self):
        request = quixote.get_request()

        the_file = request.form['file']
        data = the_file.read(int(1e9))

        image.add_temp(data)

        return 


    @export(name='upload2')
    def upload2(self):
        return html.render('upload2.html')

    @export(name='upload2_receive')
    def upload2_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image.add_image(data, "image name", "image description")

        return html.render('upload2_received.html')

    @export(name='image')
    def image(self):
        return html.render('image.html', {'image_name' : image.get_latest_image()[1], 'image_description' : image.get_latest_image()[2]})

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        response.set_content_type('image/png')
        img = image.get_latest_image()[0]
        return img

    @export(name='image_temp')
    def image_temp(self):
        response = quixote.get_response()
        response.set_content_type('image/png')
        img = image.get_temp()
        return img
