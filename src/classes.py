import os
import urllib.request
import ssl
import json
from json2html import *
from bs4 import BeautifulSoup
from justwatch import JustWatch
from pprint import pprint

with open('../providers.json') as fp:
	providers = json.load(fp)
service_names = {p['short_name']:p['clear_name'] for p in providers}
free_services = {p['short_name']:p['clear_name'] for p in providers \
					if 'buy' not in p['monetization_types'] and \
					'rent' not in p['monetization_types'] and \
					'flatrate' not in p['monetization_types']}
subscription_services = {p['short_name']:p['clear_name'] for p in providers \
					if 'flatrate' in p['monetization_types']}

def isEmpty(value):
	return True if value in [None, '', {}, []] else False
LBXD_URL = "letterboxd.com"
class Monetization():
	def __init__(self, mtypes):
		self.flatrate = True if 'flatrate' in mtypes else False
		self.free = True if 'free' in mtypes else False
		self.ads = True if 'ads' in mtypes else False
		self.buy = True if 'buy' in mtypes else False
		self.rent = True if 'rent' in mtypes else False
	def __iter__(self):
		for k, v in self.__dict__.items():
			yield k, v
	def getType(self):
		return 	'flatrate' if self.flatrate is True else \
				'free' if self.free is True else 'ads' if self.ads is True else\
				'buy or rent' if self.buy is True or self.rent is True else None

class Provider():
	def __init__(self, provider):
		self.code = provider['short_name']
		self.name = provider['clear_name']	
		self.paid = Monetization(provider['monetization_types'])
		self.cost = self.paid.getType()
	def costType(self):
		return self.cost.getType()

class JustBoxdMovie():
	letterboxdUrl = "https://leterrboxd.com"
	def __init__(self, url=None, slug=None):
		
		self.url = url
		self.slug = slug
		self.title = ''
		self.year = None
		self.display_title = ''
		self.description = ''
		self.poster = ''
		self.year = None
		self.providers = []

	# Properly formed slugs start with a forward slash
	def isSlug(self, lbxd):
		return True if lbxd.startswith("/film/") else False

	def connect(self):
		url = self.url
		html_str = ''
		ssl._create_default_https_context = ssl._create_unverified_context
		fp = urllib.request.urlopen(url)
		html_str += fp.read().decode("utf8")
		fp.close()
		return html_str

	def fromUrl(self, url=None, slug=None):
		if slug:
			self.url = "https://letterboxd.com" + slug
		if url:
			self.url = url
		html_str = self.connect()
		soup = BeautifulSoup(html_str, 'html.parser')
		tags = soup.findAll('meta')
		for tag in tags:
			tag = str(tag).replace('&amp;','&')
			if 'content' in tag:
				if 'og:title' in tag:
					self.display_title = self.getIndex(tag,'content="')
					self.title = self.display_title[0:-7]
					self.year = self.display_title[len(self.display_title)-5:len(self.display_title)-1]
				if 'og:description' in tag:
					self.description = self.getIndex(tag, 'content="')
				if 'property="og:image"' in tag:
					self.poster = self.getIndex(tag, 'content="', end='?')

	def getIndex(self, line, substr, end='"'):
		start = line.index(substr) + len(substr)
		stop = line.index(end, start)
		return line[start: stop]

	def getProviders(self, streamers, country='US'):
		just_watch = JustWatch(country=country)
		offer = []
		movie_found = just_watch.search_for_item( query=self.display_title, 
							monetization_types=['flatrate', 'free', 'ads'])
		if not isEmpty(movie_found['items']):
			movie = movie_found['items']
			for i in range(len(movie_found)):
				if movie[i]['title'] == self.title and movie[i]['original_release_year']:
					offer = [o['package_short_name'] for o in movie_found['items'][0]['offers'] \
								if o['monetization_type'] != 'buy' and o['monetization_type'] != 'rent']
					offer = [s for s in offer if s in streamers]
					offer = [*set(offer)]
		return offer

	def getMovie(self, country='US',title=None):
		watch = JustWatch(country=country)
		movie = watch.search_title_id(self.title)

		return [k for k in movie.keys()]

class JustBoxdMovieList():
	def __init__(self, url=None, slug=None username=None, list_name=None,
				sort_by=None, pages=10):
		self.url = url
		self.username = username
		self.list_name = list_name
		self.sort_by = sort_by
		self.pages = pages
		self.titles = []

	def byList(self):
		url = self.url
		html_str = ''
		if url == '':
			url = 'letterboxd.com/' + username + '/'
		if list_name != "watchlist":
			list_name = ''.join(["-" if char == " " else "" if char == "'" else char for char in list_name]).lower()
			url += "list/" + list_name
		page_postfix = "/by/popular/page/" if url[-1] == "/" else "/page/"
		url_postfix = 'watchlist/' + page_postfix 
		url += url_postfix
		url += 'page/'
		ssl._create_default_https_context = ssl._create_unverified_context
		html_str = ''

	def byUrl(self):
		url = self.url
		url += 'page/'
		for i in range(self.pages):
			fp = urllib.request.urlopen(url + str(i+1))
			html_str += fp.read().decode("utf8")
			fp.close()		
		soup = BeautifulSoup(html_str, 'html.parser')
		html_objects = soup.findAll('li', {'class': 'poster-container'})
		for html_object in html_objects:
			object_str = str(html_object).replace('&amp;','&')
			slug_start = object_str.index('data-film-slug="')+16
			#start_index = object_str.index('<img alt="')+10
			#end_index = object_str.index('"', start_index)
			slug_end = object_str.index('"', slug_start)
			slug = object_str[slug_start:slug_end]
			movie = JustBoxdMovie()
			movie.fromUrl(slug=slug)
			# movie = JustBoxdMovie(title=object_str[start_index:end_index],
			# 				url=slug)
			self.titles.append(movie)
		return self.titles

	def __iter__(self):
		for each in self.titles:
			yield each


class Providers():
	def __init__(self, providers_json="..data/providers.json"):
		with open('../providers.json') as fp:
			providers = json.load(fp)
		self.providers = [Provider(p) for p in providers]
	def __iter__(self):
		for each in self.providers:
			yield each

def main():
	# providers = Providers()
	# [print(p.name) for p in providers]
	# movies = JustBoxdMovieList(url="https://letterboxd.com/s4ppho/list/internet-archive/")
	# [print(m.slug) for m in movies.byUrl()]
	movie = JustBoxdMovie()
	movie.fromUrl('https://letterboxd.com/film/hellraiser-2022/')
	pprint([movie.display_title,
	movie.description,
	movie.poster])
	print(movie.getProviders([p['short_name'] for p in providers]))

if __name__ == '__main__':
	main()

    	




