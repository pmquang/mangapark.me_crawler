import requests
import sys
from os import path, system
from bs4 import BeautifulSoup
import re
import json
from multiprocessing import Pool
import os
import MySQLdb
import datetime
import time

MANGA_URL='http://mangapark.me'
noimage = "http://h.s.mangapark.me/img/no-cover.jpg"
now = datetime.datetime.now()
_datetime = now.strftime("%Y-%m-%d %H:%M:%S +0000")
db=MySQLdb.connect(user="emanga24h_admin",passwd="emanga24h@Inf0",db="emanga24h_db")
db.set_character_set('utf8')
command=db.cursor()

def checkManga(slug):
    db=MySQLdb.connect(user="emanga24h_admin",passwd="emanga24h@Inf0",db="emanga24h_db")
    db.set_character_set('utf8')
    command=db.cursor()
    query = "select id from wp_comic_series where slug = '%s'" % slug
    command.execute(query)
    mangaid = command.fetchone()
    if (mangaid):
        command.close()
        return True
    else:
        command.close()
        return False

def getMangaId(slug):
    db=MySQLdb.connect(user="emanga24h_admin",passwd="emanga24h@Inf0",db="emanga24h_db")
    db.set_character_set('utf8')
    command=db.cursor()
    query = "select id from wp_comic_series where slug = '%s'" % slug
    command.execute(query)
    mangaid = command.fetchone()
    if (mangaid):
        command.close()
        return mangaid
    else:
        command.close()
        return False

def checkNewestChapter(mangaid):
    db=MySQLdb.connect(user="emanga24h_admin",passwd="emanga24h@Inf0",db="emanga24h_db")
    db.set_character_set('utf8')
    command=db.cursor()
    query = "select max(number) from wp_comic_chapter where series_id = %d" % mangaid
    command.execute(query)
    latestnumber = command.fetchone()
    if (latestnumber):
        command.close()
        return latestnumber
    else:
        command.close()
        return False

def chapter_download(chapterlink,number):
    slug = chapterlink.split('/')[4]
    if not (os.path.isdir(slug + "/%d" % number)):
        os.makedirs(slug + "/%d" % number)
        
    response = requests.get(chapterlink)
    i = 1 
    while 1:
        picture = re.search("http://.*%d\.jpg" % i, response.text)
        if (picture):
            piclink = picture.group(0)
            picdownload = requests.get(piclink)
            handle = open(slug + "/%d/%d.jpg" % (number,i), "w")
            handle.write(picdownload.content)
            handle.close()
            i = i + 1
        else:
            break

def chapter_update(slug,chapnumber):
    i = int(chapnumber)
    query = "select id from wp_comic_series where slug = '%s'" % slug
    command.execute(query)
    mangaid = command.fetchone()
    if (mangaid):
        _datetime = now.strftime("%Y-%m-%d %H:%M:%S +0000")
        query_insert = """insert into wp_comic_chapter (title,number,series_id,pubdate,slug,folder) values ('%s',%d,%d,'%s','%s','/%s/%s/')""" % (str(i),i,int(mangaid[0]),_datetime,str(i),slug,str(i))
        command.execute(query_insert)
    else:
        print 'bbb'
    
    
def crawl(mangalink):
    try:
        manga = {}
        manga['link']  = mangalink
        manga['slug']  = mangalink.split('/')[4]  
        response = requests.get(mangalink)
        
        # Title
        _title_soup = BeautifulSoup(response.text)
        for _title in _title_soup.findAll('a'):
            if "/manga/%s\"" % manga['slug'] in "%s\"" % _title.get('href','default'):
                manga['title'] = re.sub(" Manga| Manhwa| Manhua", "", _title.text )
        
        
        # Summary
        _summary_soup = BeautifulSoup(response.text)
        for _summary in _summary_soup.findAll('p'):
            if 'summary' in _summary.get('class','default'):
                manga['summary'] = _summary.text.replace("\r\n", "")
                manga['summary'] = manga['summary'].replace("\"", "")
                manga['summary'] = manga['summary'].replace("\n", "")
        
        # Image
        for _image in re.findall("http://.*200\.jpg", response.text):
            manga['image'] = _image
        
        # Author
        _author_search = re.search("<a target=\"_blank\" href=\"/search\?autart.*</a>" , response.text)
        if _author_search:
            _author_soup = BeautifulSoup(_author_search.group(0))
            manga['author'] = _author_soup.text
        # Category
        _cat_array = []
        _cat_search = re.findall("<a target=\"_blank\".*/genre.*</a>" , response.text)
        for _cat in _cat_search:
            _cat_soup = BeautifulSoup(_cat)
            _cat_array.append(_cat_soup.get_text())
        manga['category'] = _cat_array
        
        ## Chapter
        chapterrepsond = requests.get(mangalink)
        _chapter_array = []
        _chapter = re.search("/manga/.*oneshot" , chapterrepsond.text)
        if (_chapter):
            _chapter_array.append(MANGA_URL + _chapter.group(0))
            print 'oneshot'
        else:
            i = 0
            while 1:
                _chapter = re.search("/manga/.*c%d\"" % i, chapterrepsond.text)
                if (_chapter):
                    _chapter_array.append (MANGA_URL + _chapter.group(0).split('"')[0])
                    i = i + 1
                else:
                    if (i == 0):
                        i = i + 1
                        continue
                    else:
                        break
        manga['chapter'] = _chapter_array
        result = json.dumps(manga)
        return str(result)
    except:
        return False

def createManga(manga):
    _title = manga['title'].replace('"','')
    _slug = manga['link'].split('/')[4]
    _summary = manga.get('summary','No infomation')
    _summary = _summary.replace('"','')
    _author = manga['author'].replace('"','')
    _read = 1
    _creation = _datetime
    _status    = 1
    _rating = 0
    _type = 0
    _img = 'icon.jpg'
    _category = ''
    for _cat in manga['category']:
        _category = _cat + ',' + _category
    _category.replace('"','')
    query = """insert into wp_comic_series (title,slug,summary,categories,author,`read`,creation,status,rating,type,img) values ("%s",'%s',"%s","%s","%s",%d,'%s',%d,%d,%d,'%s')""" % (_title,_slug,_summary,_category,_author,_read,_creation,_status,_rating,_type,_img)
    command.execute(query)
    
    if not (os.path.isdir(manga['slug'])):
        os.makedirs(manga['slug'])
        piclink = manga.get('image','http://h.s.mangapark.me/img/no-cover.jpg')
        picdownload = requests.get(piclink)
        handle = open(manga['slug'] + "icon.jpg", "w")
        handle.write(picdownload.content)
        handle.close()
        
def updateChapter(manga):
    mangaid = getMangaId(manga['slug'])
    maxchapter = checkNewestChapter(mangaid)
    
    if not maxchapter:
        maxchapter = -1
        
    for chapter in manga['chapter']:
        number = int(chapter.split('/')[len(chapter.split('/'))-1].split('c')[1])
        if number > maxchapter:
            chapter_download(chapter, number)
            chapter_update(manga['slug'],number)
            
def updateManga(mangalink):
    manga = crawl(mangalink)
    if not checkManga(manga['slug']):
        createManga(manga)
    updateChapter(manga)
   
if __name__ == "__main__":
    response = requests.get('http://mangapark.me/latest')
    soup = BeautifulSoup(response.text)
    for tag in soup.find_all('h3'):
        if "ago" in tag.i.text:
            print tag.a['href']
            updateManga(tag.a['href'])    
                
                
                
        
    
    