import os
import urllib.request
import ssl
import json
from json2html import *
from bs4 import BeautifulSoup
from justwatch import JustWatch
from service_codes import service_codes
import csv

# create a dictionary of all service codes 
with open('../providers.json') as fp:
	providers = json.load(fp)

service_names = {p['short_name']:p['clear_name'] for p in providers}
service_codes_short = [k for k in service_names.keys()]
free_services = {p['short_name']:p['clear_name'] for p in providers \
					if 'buy' not in p['monetization_types'] and \
					'rent' not in p['monetization_types'] and \
					'flatrate' not in p['monetization_types']}
subscription_services = {p['short_name']:p['clear_name'] for p in providers if 'flatrate' in p['monetization_types']}

def get_user_services(save_file="user_services.json"):
	if os.path.exists(save_file):
		with open(save_file) as fp:
			json_data = json.load(fp)
			return json_data
	else:
		return None

def save_user_services(services, save_file="user_services.json"):
	with open(save_file, 'w') as fp:
		json_data = json.dumps(services, indent=4)
		fp.write(json_data)
		fp.close()
		return save_file

# def parse_lxbd_url(lbxd_url):
# 	lbxd_url = "https://letterboxd.com/"
# 	url_list = url_string.split("/")
# 	url_list = list(filter(lambda x: x not in ["https:", "", "letterboxd.com"], url_list))
# 	if len(url_list) == 1:
# 		return lbxd_url

def get_watchlist_titles (username='default', 
			list_name='watchlist', url_string='', sort_by='', pages=10):
	titles = []
	if url_string == '':
		url_string = 'https://letterboxd.com/' + username + '/'
		if list_name != "watchlist":
			list_name = ''.join(["-" if char == " " else "" if char == "'" else char for char in list_name]).lower()
			url_string += "list/" + list_name
		else:
			url_string += "watchlist/"
	page_postfix = "page/" if url_string[-1] == "/" else "/page/"
	if sort_by != '':
		url_postfix = "/by/" + sort_by + page_postfix
		url_string.split("/")
	else:
		url_postfix = page_postfix
	url_string += url_postfix
	ssl._create_default_https_context = ssl._create_unverified_context
	html_str = ''
	print(url_string)
	for i in range(pages):
		fp = urllib.request.urlopen(url_string + str(i+1))
		html_str += fp.read().decode("utf8")
		fp.close()

	soup = BeautifulSoup(html_str, 'html.parser')
	html_objects = soup.findAll('li', {'class': 'poster-container'})
	for html_object in html_objects:
		object_str = str(html_object).replace('&amp;','&')
		start_index = object_str.index('<img alt="')+10
		end_index = object_str.index('"', start_index)
		movie_name = object_str[start_index:end_index]
		titles.append(movie_name)

	return titles




# get list of streaming services for list of titles.
def get_streamers(watchlist_titles, streamers, country='US'):
	just_watch = JustWatch(country=country)
	results = {}
	# nonefound = []

	for movie in watchlist_titles:
		print(movie)
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
			title_and_year = movie + " " + "(" + str(movie_year) + ")"
			results[title_and_year] = offer_lookup
		else:
			nonefound.append(title_and_year)
		# print(json.dumps({"Title":full_key, "Streaming Services": [v for k, v in streaming_services.items() if k in offer]}))
	return results

def save_json_to_html(titles_dict, fn='streaming.html'):
	json_data = json.dumps(titles_dict, indent=4)
	with open(fn, 'w') as fp:
		fp.write(json2html.convert(json=json_data))
	return fn

def save_to_csv(titles_dict, fn='services.csv'):
	with open('names.csv', 'w', newline='') as csvfile:
		fieldnames = ['movie', 'services']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for k, v in titles_dict.items():
			writer.writerow({'movie':k, 'services': v})
	return fn

# def main():
# 	username = 'grryboy'
# 	titles = get_watchlist_titles(username)
# 	streamers = free_services
# 	save_to_csv(get_streamers(titles, streamers))

# if __name__ == '__main__':
# 	main()
