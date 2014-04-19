import sqlite3

# connect to the already existing database
db = sqlite3.connect('images.sqlite')

# configure to allow binary insertions
db.text_factory = bytes


def insert(image_data, image_name, image_description):
	# insert!
	db.execute('INSERT INTO image_store (image, name, description) VALUES (?, ?, ?)', (image_data, image_name, image_description))
	db.commit()

def retrieve(key):
	# get a query handle (or "cursor")
	c = db.cursor()

	# select all of the images
	c.execute('SELECT i, image, name, description FROM image_store  WHERE i=key ORDER BY i ASC LIMIT 1')
	#          ^      ^             ^           ^
	#          ^      ^             ^           ^----- details of ordering/limits
	#          ^      ^             ^
	#          ^      ^             ^--- table from which you want to extract
	#          ^      ^
	#          ^      ^---- choose the columns that you want to extract
	#          ^
	#          ^----- pick zero or more rows from the database


	# grab the first result (this will fail if no results!)
	i, image, name, description = c.fetchone()

	return i, image, name, description

	# write 'image' data out to sys.argv[1]
	# print 'writing image', i
	# open(sys.argv[1], 'w').write(image)

def retrieve_all_keys():
	c = db.cursor()
	c.execute('SELECT i FROM image_store ORDER BY i ASC')

	return c.fetchall()


def retrieve_all():
	c = db.cursor()
	c.execute('SELECT i, image, name, description FROM image_store ORDER BY i ASC')

	return c.fetchall()	

def retrieve_latest():
	c = db.cursor()

	# select all of the images
	c.execute('SELECT i, image, name, description FROM image_store ORDER BY i DESC LIMIT 1')
	#          ^      ^             ^           ^
	#          ^      ^             ^           ^----- details of ordering/limits
	#          ^      ^             ^
	#          ^      ^             ^--- table from which you want to extract
	#          ^      ^
	#          ^      ^---- choose the columns that you want to extract
	#          ^
	#          ^----- pick zero or more rows from the database


	# grab the first result (this will fail if no results!)
	i, image, name, description = c.fetchone()

	return i, image, name, description