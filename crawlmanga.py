import requests
import sys
from os import path, system
from bs4 import BeautifulSoup
import re
import json
from multiprocessing import Pool
import MySQLdb
import os

db=MySQLdb.connect(user="emanga24h_admin",passwd="emanga24h@Inf0",db="emanga24h_db")
db.set_character_set('utf8')
command=db.cursor()
noimage = "http://h.s.mangapark.me/img/no-cover.jpg"

if __name__ == "__main__":
    for manga in open('manga.txt'):
	data = json.loads(manga)
	imagelink = data.get('image','noinfo')
	if imagelink == 'noinfo':
		print data['title']
		imagecontent = requests.get(noimage)
		slug = data['link'].split('/')[4]
		handle = open(slug + "/icon.jpg", "w")
        	handle.write(imagecontent.content)
        	handle.close()
		continue
	imagecontent = requests.get(imagelink)
	slug = data['link'].split('/')[4]
	handle = open(slug + "/icon.jpg", "w")
        handle.write(imagecontent.content)
        handle.close()
