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
    key, image = image_store.retrieve_latest()
    return image

def get_all_images():
	images = image_store.retrieve_all()
	return images
