import flask
from imageappflask import app
import image
import io
 
@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/image_raw/')
@app.route('/image_raw/<image_id>')
def image_raw(image_id=None):
    if image_id == None:
	    img_data = image.get_latest_image()
    else:
        img_data = image.get_image(image_id)

    response = flask.make_response(img_data[0])
    # print img_data[3]
    response.headers['Content-Type'] = img_data[3]

    return response

@app.route('/jquery/')
def jquery():
	return flask.send_file('jquery-1.3.2.min.js')

@app.route('/upload/')
def upload():
	return flask.render_template('upload.html')

@app.route('/upload_receive', methods=['GET', 'POST'])
def upload_receive():

    file_obj = flask.request.files['file']
    name = flask.request.form['image_name']
    description = flask.request.form["image_description"]
    mimetype =  file_obj.mimetype

    data = file_obj.read(int(1e9))
    image.add_image(data, name, description, mimetype)

    return flask.redirect(flask.url_for('index'))

@app.route('/upload2/')
def upload2():
    return flask.render_template('upload2.html')

@app.route('/upload2_receive', methods=['GET', 'POST'])
def upload2_receive():
    file_obj = flask.request.files['file']

    data = file_obj.read(int(1e9))
    image.add_image(data, "image_name", "image description")

    return flask.render_template('upload2_received.html')

@app.route('/upload_temp', methods=['GET', 'POST'])
def upload_temp():
    file_obj = flask.request.files['file']
    cookie_info = flask.request.environ.get('HTTP_COOKIE', "")
    print cookie_info
    data = file_obj.read(int(1e9))
    image.add_temp(data, file_obj.mimetype)
    return 'OK'

@app.route('/image_temp/')
def image_temp():
    print "viewing temp"
    img_data = image.get_temp()

    response = flask.make_response(img_data[0])
    response.headers['Content-Type'] = img_data[1]
    return response

@app.route('/img/')
@app.route('/img/<image_id>')
def img(image_id=None):

    if image_id == None:
        img_response = image.get_latest_image()
        image_id =''
    else:
    	img_response = image.get_image(image_id)

    return flask.render_template('image.html', image_id=image_id, image_name=img_response[1], image_description=img_response[2])

@app.route('/all_imgs/')
def all_imgs():
    imgs = image.get_all_images()

    return flask.render_template('list_images.html', images=imgs)