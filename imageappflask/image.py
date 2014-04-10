# image handling API
import image_store

temp_images = {}

def add_image(data, name, description):
    image_id = image_store.insert(data, name, description)
    return image_id

def add_temp(data):
	temp_images[0] = data
	return

def get_temp():
	return temp_images[0]

def get_image(image_id):
    return image_store.retrieve(image_id)

def get_latest_image():
    key, image_data, name, description = image_store.retrieve_latest()
    image = [image_data, name, description]
    return image
