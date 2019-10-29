#!/usr/bin/env python
import csv
import json
import pathlib
import operator
import requests
import argparse
import configparser

import wikipedia

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
parser.add_argument('--summary-length', type=int,
										help='Limit the number of sentences in place summary.')

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
with open(args.directory + f'/{filename}.csv', 'w', encoding='utf-8') as out_file:
	writer = csv.writer(out_file, delimiter='|')
	writer.writerow(columns)
	for place in places:
		name = place['name']
		formatted_address = place['formatted_address']
		types = place['types']
		if 'user_ratings_total' in place:
			reviews = place['user_ratings_total']
		else:
			reviews = -1

		if 'rating' in place:
			rating = place['rating']
		else:
			rating = -1

		try:
			if args.summary_length:
				wiki_page = wikipedia.page(name, sentences=args.summary_length)
			else:
				wiki_page = wikipedia.page(name)
			url = wiki_page.url
			summary = wiki_page.summary.replace('\n', '')
		except KeyboardInterrupt:
			exit(-1)
		except:
			url, summary = '', ''

		# If item type is from the exlude list, skip it.
		if args.exclude:
			if list(set(args.exclude) & set(types)):
				continue

		# If an item doesn't satify the rating and review count criteria, skip it.
		if args.rating and args.reviews:
			rating = place['rating']
			if not OPERATORS[args.operator](rating >= args.rating, reviews >= args.reviews):
				continue
		elif args.rating:
			if not rating >= args.rating:
				continue
		elif args.reviews:
			if not reviews >= args.reviews:
				continue

		lat, lng = place['geometry']['location']['lat'], place['geometry']['location']['lng']
		data = [name, (lat, lng), ', '.join(types), rating, formatted_address, summary, url, reviews]
		print(f'{filename} -> {data}')
		writer.writerow(data)
