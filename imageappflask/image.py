# image handling API
import image_store

temp_images = {}

def add_image(data, name, description, mimetype):
    image_id = image_store.insert(data, name, description, mimetype)
    return image_id

def add_temp(data, mimetype):
    temp_images[0] = [data, mimetype]
    return

def get_temp():
    return temp_images[0]

def get_image(image_id):
    return image_store.retrieve(image_id)

def get_latest_image():
    key = image_store.retrieve_latest()
    return key 

def get_all_images():
    images = image_store.retrieve_all()
    print "got images"
    return images

def get_by_query(query):
    images = image_store.search(query)
    return images

def add_comment(image_id, comment):
    row_id = image_store.add_comment(image_id, comment)
    return row_id

def get_comments(image_id):
    comments = image_store.get_comments(image_id)
    return comments
