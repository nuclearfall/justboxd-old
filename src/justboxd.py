import urllib.request
import ssl
import json
from json2html import *
from bs4 import BeautifulSoup
from justwatch import JustWatch
from service_codes import service_codes

# create a dictionary of all service codes 
with open('../providers.json') as fn:
	providers = json.load(fn)

service_names = {p['short_name']:p['clear_name'] for p in providers}
service_codes_short = [k for k in service_names.keys()]
free_services = {p['short_name']:p['clear_name'] for p in providers \
					if 'buy' not in p['monetization_types'] and \
					'rent' not in p['monetization_types'] and \
					'flatrate' not in p['monetization_types']}
subscription_services = {p['short_name']:p['clear_name'] for p in providers if 'flatrate' in p['monetization_types']}


def get_watchlist_titles (letterboxd_username='default', 
			list_name='watchlist', sort_by='popular', pages=10):
	titles = []
	url_string = 'https://letterboxd.com/' + letterboxd_username + '/'
	url_postfix = "/by/" + sort_by + "/page/"
	if list_name != "watchlist":
		list_name = ''.join(["-" if char == " " else "" if char == "'" else char for char in list_name]).lower()
		list_name = "list/" + list_name
	url_string += list_name + url_postfix
	ssl._create_default_https_context = ssl._create_unverified_context
	html_str = ''

	for i in range(pages):
		fp = urllib.request.urlopen(url_string + str(i+1))
		html_str += fp.read().decode("utf8")
		fp.close()

	soup = BeautifulSoup(html_str, 'html.parser')
	html_objects = soup.findAll('li', {'class': 'poster-container'})
	for html_object in html_objects:
		object_str = str(html_object).replace('&amp;','&')
		print(object_str)
		start_index = object_str.index('<img alt="')+10
		end_index = object_str.index('"', start_index)
		movie_name = object_str[start_index:end_index]
		print(movie_name)
		titles.append(movie_name)
	return titles

# get list of streaming services for list of titles.
def get_streamers(watchlist_titles, streamers, country='US'):
	just_watch = JustWatch(country=country)
	results = {}
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
				full_key = movie + " " + "(" + str(movie_year) + ")"
				results[full_key] = offer_lookup
	return results

def save_json_to_html(titles_dict, fn='streaming.html'):
	json_data = json.dumps(titles_dict, indent=4)
	jhtml = json2html.convert(json = json_data)
	with open(fn, 'w') as fp:
		fp.write(jhtml)
	return fn



