# image handling API

images = {}

temp_images = {}


def add_image(data, name, description):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
        
    images[image_num] = [data, name, description]
    return image_num

def add_temp(data):
	temp_images[0] = data
	return

def get_temp():
	return temp_images[0]

def get_image(num):
    return images[num][0]

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]
