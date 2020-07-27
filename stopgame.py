import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

host = 'https://parfumelover.herokuapp.com/'
url = 'https://parfumelover.herokuapp.com/show?id=5'

r = requests.get(url)
html = BS(r.content, 'html.parser')

poster =html.select('.display-4')[0].text
print(poster)