import requests
import sys
from os import path, system
from bs4 import BeautifulSoup
import re
import json
from multiprocessing import Pool
import MySQLdb
import datetime
import time
now = datetime.datetime.now()
db=MySQLdb.connect(user="emanga24h_admin",passwd="emanga24h@Inf0",db="emanga24h_db")
db.set_character_set('utf8')
command=db.cursor()
if __name__ == "__main__":
	slug = sys.argv[1]
	chapnumber = sys.argv[2]
	action = sys.argv[3]
	i = int(chapnumber)
	query = "select id from wp_comic_series where slug = '%s'" % slug
	command.execute(query)
	id = command.fetchone()
	if (id):
		_datetime = now.strftime("%Y-%m-%d %H:%M:%S +0000")
		query_insert = """insert into wp_comic_chapter (title,number,series_id,pubdate,slug,folder) values ('%s',%d,%d,'%s','%s','/%s/%s/')""" % (str(i),i,int(id[0]),_datetime,str(i),slug,str(i))
		query_update = """update wp_comic_chapter set title = '%s', number = %d, pubdate = '%s', slug = '%s', folder = '/%s/%s/' where number = %d and series_id = %d """ % (str(i),i,_datetime,str(i),slug,str(i),i,int(id[0]))
		if action == 'update':
			command.execute(query_update)
		if action == 'create':
			command.execute(query_insert)
	else:
		print 'bbb'

	command.close()
