import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

class StopGame:
	host = 'https://parfumelover.herokuapp.com'
	url = 'https://parfumelover.herokuapp.com'
	lastkey = ""
	lastkey_file = ""

	def __init__(self, lastkey_file):
		self.lastkey_file = lastkey_file

		if(os.path.exists(lastkey_file)):
			self.lastkey = open(lastkey_file, 'r').read()
		else:
			f = open(lastkey_file, 'w')
			self.lastkey = self.get_lastkey()
			f.write(self.lastkey)
			f.close()

	def new_games(self):
		while True:
			try:
				r = requests.get(self.url)
				break
			except:
				r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		new = []
		items = html.select('.info-wrap > .fix-height >  a')
		for i in items:
			key = int((i['href'].replace('/show?id=','')))
			if(int(self.lastkey) < int(key)):
				new.append(i['href'])

		return new

	def game_info(self, uri):
		link = self.host + uri
		while True:
			try:
				r = requests.get(link)
				break
			except:
				r = requests.get(link)
		html = BS(r.content, 'html.parser')

		# poster =html.select('.img-wrap > .img-fluid')[1]['src']
		
		poster=html.select('.img-fluid')[0]['src']
		
		# 'https://aromateque.com.ua/media/catalog/product/cache/1/small_image/174x222/9df78eab33525d08d6e5fb8d27136e95/e/a/eau_sauvage_eau_de_toilette-50_2.jpg'
		# html.select('.img-fluid')[0]['src']
		info = {
			"id": uri.replace('/show?id=','').strip(),
			"title": html.select('.p-4')[0].text.split('\n')[1],
			"link": link,
			"image": poster,
			# 'https://parfumelover.herokuapp.com/',+poster,
			"excerpt":html.select('.p-4')[0].text.split('\n')[2],
			"price":html.select('.display-4')[0].text
		};

		return info

	def download_image(self, url):
		r = requests.get(url, allow_redirects=True)

		a = urlparse(url)
		filename = os.path.basename(a.path)
		open(filename, 'wb').write(r.content)

		return filename


	def get_lastkey(self):
		r = requests.get(self.url)
		html = BS(r.content, 'html.parser')

		items = html.select('.info-wrap > .fix-height >  a')
		return items[0]['href'].replace('/show?id=','')

	def parse_href(self, href):
		result = href['href'].replace('/show?id=','')
		return result

	def update_lastkey(self, new_key):
		self.lastkey = new_key

		with open(self.lastkey_file, "r+") as f:
			data = f.read()
			f.seek(0)
			f.write(str(new_key))
			f.truncate()

		return new_key