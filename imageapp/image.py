# image handling API
import image_store

images = {}

temp_images = {}


def add_image(data, name, description):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
        
    images[image_num] = [data, name, description]

    image_store.insert(data, name, description)
    
    return image_num

def add_temp(data):
	temp_images[0] = data
	return

def get_temp():
	return temp_images[0]

def get_image(num):
    return images[num][0]

def get_latest_image():
    key, image_data, name, description = image_store.retrieve_latest()
    image = [image_data, name, description]
    images[key] = image
    return image
    # image_num = max(images.keys())
    # return images[image_num]


def load_database():
    image_rows = image_store.retrieve_all()

    for row in image_rows:
        images['%d' % row[0]] = [row[1], row[2], row[3]] 

    print len(images)