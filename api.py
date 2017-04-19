
def login(username, password):
	""" 
	verifies username password combination and returns user type

	@return string
	"Official"
	"Scientist"
	"Admin"
	"Invalid"
	"""
	return "Official" #Fixme: change this

def add_user(username, password, email, user_type, type_args):
	""" 
	registers user in the database

	@return int error_code: FIXME: maybe not the best way to do this
	0: no error
	1: duplicate username
	2: duplicate email
	"""
	return 0

def add_datapoint(location, timedate, data_type, data_value):
	"""
	adds a datapoint to the database and returns an error code

	@param array timedate [year, month, day, hour, min, sec] 

	@return int error_code 
	0: success
	"""
	return 0

def add_poi(name, city, state, zip):
	"""
	adds a POI to the database

	@return int error_code
	0: success

	"""
	return 0

def get_cities(): #fixme: does this need to deend on state
	"""
	returns list of valid cities in the database

	@return array city_list
	"""
	return ["Atlanta", "Macon", "Savanna"]


def get_states():
	"""
	returns list of valid states in the database

	@return array state_list
	"""
	return ["GA", "TN", "NY"]

def get_poi_names():
	"""
	returns a list of POI names

	@return array poi_names
	"""
	return ["Little 5 Points", "Georgia Tech", "Macon Mall"]

def get_pending_datapoints():
	return

def get_pending_officials():
	return

def get_datapoints(filters):
	"""
	@param dictionary filters 
	pending
	location_name
	city
	state
	zip
	flagged
	date_flagged_start
	date_flagged_end
	"""
	# for k in filters.keys

