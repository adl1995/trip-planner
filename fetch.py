#!/usr/bin/env python
import csv
import json
import pathlib
import operator
import requests
import argparse
import configparser

import wikipedia

# TODO
# option to specify number of sentences

# Read the API key form the configuration.
config = configparser.ConfigParser()
config.read('secrets.ini')

API_KEY = config['API_KEYS']['GOOGLE_MAPS']
PLACES_TYPES = ['park', 'point_of_interest', 'establishment', 'museum', 'library', 'church', 'art_gallery', 'political']
# Search query operators.
OPERATORS = {
	'and': operator.and_,
	'or': operator.or_
}

def fetch_place_detail(place_id):
	place_raw = requests.get(f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={API_KEY}')
	try:
		return json.loads(place_raw.text)['result']
	except KeyError:
		raise KeyError('Index \'result\' does not exist')

# Add parameters for the search query.
parser = argparse.ArgumentParser()
parser.add_argument('--query', type=str, help='Search query for Google Maps API')
parser.add_argument('--directory', type=str, help='Output directory')
parser.add_argument('--rating', type=float, help='Minimum rating of the place(s)')
parser.add_argument('--reviews', type=int, help='Minimum review count of the place(s)')
parser.add_argument('--operator', default='and', choices=OPERATORS.keys(), type=str,
								  help='Operation to perform between ratings and reviews count.')
parser.add_argument('--exclude', '-e', choices=PLACES_TYPES, nargs='+', type=str,
									   help='Exclude the places from the query result')
parser.add_argument('--language', default='en', choices=['en', 'fr', 'de'], type=str,
								  help='Language of the Wikipedia link')

args = parser.parse_args()

# Fetch the data.
places = requests.get(f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={args.query}&language=en&key={API_KEY}')
# Convert the response to a JSON object.
places = json.loads(places.text)['results']
if not places:
	raise Exception(f'No results found for query: {args.query}')

# Create the directory if it doesn't exist.
pathlib.Path(args.directory).mkdir(parents=True, exist_ok=True)
# Make the filename more readable, as this will appear as the layer title in Google My Maps.
query = args.query.split(' ')
filename = ' '.join([q.capitalize() for q in query])
# Set Wikipedia language.
wikipedia.set_lang(args.language)

columns = ['name', 'coordinates', 'types', 'rating', 'formatted address', 'summary', 'url', 'reviews']
with open(args.directory + f'/{filename}.csv', 'w') as out_file:
	writer = csv.writer(out_file, delimiter=',')
	writer.writerow(columns)
	for place in places:
		name = place['name']
		formatted_address = place['formatted_address']
		types = place['types']
		try:
			reviews = place['user_ratings_total']
		except:
			continue

		try:
			wiki_page = wikipedia.page(name)
			url = wiki_page.url
			summary = wiki_page.summary.replace('\n', '')
		except:
			url, summary = '', ''

		if args.exclude and 'rating' in place and (args.rating and args.reviews):
			rating = place['rating']
			if OPERATORS[args.operator](rating >= args.rating, reviews >= args.reviews):
				# If item type is from the exlude list, skip it.
				if list(set(args.exclude) & set(types)):
					continue

		lat, lng = place['geometry']['location']['lat'], place['geometry']['location']['lng']
		data = [name, (lat, lng), ', '.join(types), place['rating'], formatted_address, summary, url, reviews]
		print(f'{filename} -> {data}')
		writer.writerow(data)
		# print(json.dumps(place, indent=4, sort_keys=True))

		# else:
		# 	rating = -1
		# types = ', '.join(place['types'])
		# lat, lng = place['geometry']['location']['lat'], place['geometry']['location']['lng']
		# data = [name, (lat, lng), types, rating, formatted_address, icon]
		# print(f'{filename} -> {data}')
		# writer.writerow(data)
