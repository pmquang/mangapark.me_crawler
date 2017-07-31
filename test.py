import requests
import sys
from os import path, system
from bs4 import BeautifulSoup
import re
import json

MANGA_URL='http://mangapark.me'

response = requests.get('http://mangapark.me/latest')

soup = BeautifulSoup(response.text)

for tag in soup.find_all('h3'):
    if "ago" in tag.i.text:
        print tag.a['href']