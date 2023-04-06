import os
import urllib.request
import ssl
import json
from pprint import pprint
from json2html import *
from bs4 import BeautifulSoup
from justwatch import JustWatch
from service_codes import service_codes
import csv

class StreamingServices():
	def __init__(self, providers='../data/providers.json')
		if os.path.exists(providers)
			with open(providers) as fp:
				providers = json.load(fp)
		if services:
			self.subscriptionServices = services
		services = {p['short_name']:p['clear_name'] for p in providers}

		free_services = {p['short_name']:p['clear_name'] for p in providers \
					if 'buy' not in p['monetization_types'] and \
					'rent' not in p['monetization_types'] and \
					'flatrate' not in p['monetization_types']}
		self.allProviders = self.Providers(providers if providers else None)


	def Providers(self, file='../data/providers.json'):
		if providers and os.path.exists(providersJson)
				with open(providers) as fp:
					providers = json.load(fp)

	def loadUserServices(file=None):
		if file and os.path.exists(file):
			with open(file) as fp:
				jdict = json.load(fp)
				return jdict
		else:
			return None

	def saveUserServices(services=None, file=None)
		if services and file:
			with open(file, 'w') as fp:
				json_data = json.dumps(services, indent=4)
				fp.write(json_data)
			return save_file
		else:
			return None

	def userProviders(providers=None):
		if providers:
			return providers


		template = {"Title":'',"Year":None, v:'' for k, v in service_names.items() if k in streamers}

	just_watch = JustWatch(country=country)
	print(results)
	for movie in watchlist_titles:
		offers = []
		movie_found = just_watch.search_for_item(
				query=movie, 
				monetization_types=['flatrate', 'free', 'ads'])
		if len(movie_found['items']) > 0 and movie_found['items'][0]['title'] == movie:
			movie_year = movie_found['items'][0]['original_release_year']
			offer = [o['package_short_name'] for o in movie_found['items'][0]['offers'] \
						if o['monetization_type'] != 'buy' and o['monetization_type'] != 'rent']
			offer = [s for s in offer if s in streamers]
			offer = [*set(offer)]
			offer_lookup = [service_codes[k] for o in offer for k in service_codes.keys() if o == k]
			if offer_lookup != []:
				results[movie] = offer_lookup
			else:
				not_available.append(movie)
			rscsv["Title"] = movie
			rscsv["Year"] 	= movie_year
			{service_codes[s]:"True" if s in offer else servcice_codes[s]:"False" for s in streamers}
			results_json_list.append()
			results_list.append()
	return results