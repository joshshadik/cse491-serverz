# image handling API

images = {}


def add_image(data, name, description):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
        
    images[image_num] = [data, name, description]
    return image_num

def get_image(num):
    return images[num][0]

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num][0]
