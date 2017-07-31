import requests
import sys
from os import path, system
from bs4 import BeautifulSoup
import re
import json
from multiprocessing import Pool
import MySQLdb

db=MySQLdb.connect(user="emanga24h_admin",passwd="emanga24h@Inf0",db="emanga24h_db")
db.set_character_set('utf8')
command=db.cursor()
if __name__ == "__main__":
    id = 1
    for manga in open('manga.txt'):
        data = json.loads(manga)
    _id = id
    _title = data['title'].replace('"','')
    _slug = data['link'].split('/')[4]
    _summary = data.get('summary','No infomation')
    _summary = _summary.replace('"','')
    _author = data['author'].replace('"','')
    _read = 1
    _creation = '12/08/2015'
    _status    = 1
    _rating = 0
    _type = 0
    _img = 'icon.jpg'
    _category = ''
    for _cat in data['category']:
        _category = _cat + ','
    _category.replace('"','')
    query = """insert into wp_comic_series (id,title,slug,summary,categories,author,`read`,creation,status,rating,type,img) values (%d,"%s",'%s',"%s","%s","%s",%d,'%s',%d,%d,%d,'%s')""" % (_id,_title,_slug,_summary,_category,_author,_read,_creation,_status,_rating,_type,_img)
    command.execute(query)
    i = 1
    for chapter in data['chapter']:
        if "c0" in chapter:
            i = 0
            break
        if "c1" in chapter:
            i = 1
            break
    for chapter in data['chapter']:
        query = """insert into wp_comic_chapter (title,number,series_id,pubdate,slug,folder) values ('%s',%d,%d,'%s','%s','/%s/%s/')""" % (str(i),i,_id,'2015-09-12 01:57:25 +0000',str(i),_slug,str(i))
        command.execute(query)
        i = i + 1
        id = id + 1
    command.close()