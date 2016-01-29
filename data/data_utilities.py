"""
Utilities specifically for the data processing scripts and data interfaces.
"""
import os
from datetime import date

THIS_FILE_PATH = os.path.dirname(__file__)
CURRENT_YEAR = date.today().year
CURRENT_MONTH = date.today().month

DEFAULT_RAW_REVIEWS_FILE_NAME = 'yelp_academic_dataset_review.json'
DEFAULT_RAW_USERS_FILE_NAME = 'yelp_academic_dataset_user.json'

DEFAULT_BASIC_ATTRIBUTES_FILE_NAME = 'user_basic_attributes.txt'
DEFAULT_REVIEW_LENGTHS_FILE_NAME = 'user_average_review_lengths.txt'
DEFAULT_READING_LEVELS_FILE_NAME = 'user_reading_levels.txt'
DEFAULT_PAGERANKS_FILE_NAME = 'user_pageranks.txt'
DEFAULT_COMBINED_USERS_FILE_NAME = 'combined_users.txt'

DEFAULT_D3_GRAPH_FILE_NAME = 'users_D3_graph.json'

# List of (attribute name, function that returns attribute value, given a raw user dictionary)
BASIC_USER_ATTRIBUTES_AND_EXTRACTORS = [
	( 'ID', lambda raw_user: raw_user['user_id'] ),
	( 'review_count', lambda raw_user: raw_user['review_count'] ),
	( 'average_stars', lambda raw_user: raw_user['average_stars'] ),
	( 'funny_vote_count', lambda raw_user: raw_user['votes']['funny'] ),
	( 'useful_vote_count', lambda raw_user: raw_user['votes']['useful'] ),
	( 'cool_vote_count', lambda raw_user: raw_user['votes']['cool'] ),
	( 'friend_count', lambda raw_user: len(raw_user['friends']) ),
	( 'years_elite', lambda raw_user: len(raw_user['elite']) ),
	( 'months_member', lambda raw_user: _months_since_year_and_month(raw_user['yelping_since']) ),
	( 'fan_count', lambda raw_user: raw_user['fans'] ),
]

# Attributes that can be extracted solely from the raw Yelp user file
BASIC_USER_ATTRIBUTES = list(zip(*BASIC_USER_ATTRIBUTES_AND_EXTRACTORS)[0])

# All user attributes available (across all dataset files and after all processing)
ALL_USER_ATTRIBUTES = list(BASIC_USER_ATTRIBUTES) + [
	'average_review_length',
	'average_reading_level',
	'pagerank',
]

# User attributes typically desired for training models
_EXCLUDE_FROM_DEFAULT_USER_ATTRIBUTES = set(['funny_vote_count', 'useful_vote_count', 'cool_vote_count', 'friend_count', 'fan_count'])
DEFAULT_USER_ATTRIBUTES = [attribute for attribute in ALL_USER_ATTRIBUTES if attribute not in _EXCLUDE_FROM_DEFAULT_USER_ATTRIBUTES]


def _months_since_year_and_month(year_month_string):
	"""Returns the number of months' difference between now and a month formatted as YYYY-MM."""
	year, month = map(int, year_month_string.split('-'))
	return 12 * (CURRENT_YEAR - year) - month + CURRENT_MONTH


def _raw_data_absolute_path(relative_path):
	"""Given the name of a raw data file, returns its absolute path."""
	return os.path.join(THIS_FILE_PATH, 'raw_data/' + relative_path)


def _processed_data_absolute_path(relative_path):
	"""Given the name of a processed data file, returns its absolute path."""
	return os.path.join(THIS_FILE_PATH, 'processed_data/' + relative_path)


# TODO: Cast numerical attribute values to floats, ints, etc.
def _read_single_user_attribute(input_file_name):
	"""
	Given a processed user attribute file of the form
		user_1_ID user_1_attribute_value
			.
			.
			.
		user_N_ID user_N_attribute_value
	
	returns a dictionary:
		{ user_1_ID: user_1_attribute_value, ..., user_N_ID: user_N_attribute_value }
	"""
	attribute_for_user = {}

	with open(_processed_data_absolute_path(input_file_name)) as attribute_file:

		for user_line in attribute_file:
			user_ID, attribute_value = user_line.split()
			attribute_for_user[user_ID] = attribute_value

	return attribute_for_user


def _write_single_user_attribute(attribute_for_user, output_file_name):
	"""
	Given a dictionary
		{ user_1_ID: user_1_attribute_value, ..., user_N_ID: user_N_attribute_value }

	writes a file of the form
		user_1_ID user_1_attribute_value
			.
			.
			.
		user_N_ID user_N_attribute_value
	"""
	with open(_processed_data_absolute_path(output_file_name), 'w') as attribute_file: # Write mode; overwrite old file if it exists
		
		for user_ID, attribute in attribute_for_user.iteritems():
			attribute_file.write(user_ID + ' ' + str(attribute) + '\n')


# TODO: Cast numerical attribute values to floats, ints, etc.
def _read_multiple_user_attributes(input_file_name, attributes):
	"""
	Given a processed user attributes file of the form
		attribute_1_name ... attribute_K_name
		user_1_attribute_1_value ... user_1_attribute_K_value
			.
			.
			.
		user_N_attribute_1_value ... user_N_attribute_K_value

	and a list of desired attributes, returns a list of user dictionaries:
		[
			{attribute_1_name: user_1_attribute_1_value, ..., attribute_k_name: user_1_attribute_k_value},
				.
				.
				.
			{attribute_1_name: user_N_attribute_1_value, ..., attribute_k_name: user_N_attribute_k_value}
		]
	where the user dictionaries include only the k <= K desired attributes.
	"""
	attributes_set = set(attributes)
	users = []

	with open(_raw_data_absolute_path(input_file_name)) as attributes_file:

		# Row 1: attribute names
		attributes_in_file = attributes_file.readline().split()

		# Rows 2,...,N: users' attribute values written in the same order
		for user_line in attributes_file:
			user_attribute_values = user_line.split()
			users += [ { attribute_name: user_attribute_values[i] for i, attribute_name in enumerate(attributes_in_file) if attribute_name in attributes_set } ]

	return users


def _write_multiple_user_attributes(users, attributes, output_file_name):
	"""
	Given a list of (or iterator over) user dictionaries and a list of user attributes, writes a
	file of the form
		attribute_1_name ... attribute_K_name
		user_1_attribute_1_value ... user_1_attribute_K_value
			.
			.
			.
		user_N_attribute_1_value ... user_N_attribute_K_value
	"""
	with open(_processed_data_absolute_path(output_file_name), 'w') as user_attributes_file: # Write mode; overwrite old file if it exists

		# Row 1: attribute names
		user_attributes_file.write( ' '.join(attributes) + '\n' )

		# Rows 2,...,N: users' attribute values written in the same order
		for user in users:
			user_attributes_file.write( ' '.join([str(user[attribute]) for attribute in attributes]) + '\n' )




