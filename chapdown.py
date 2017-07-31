import requests
import sys
from os import path, system
from bs4 import BeautifulSoup
import re
import json
from multiprocessing import Pool
import os

MANGA_URL='http://mangapark.me'
#db=MySQLdb.connect(user="emanga24h_admin",passwd="emanga24h@Inf0",db="emanga24h_db")
#db.set_character_set('utf8')
#command=db.cursor()

def manga_download(mangalink,chapnumber):
    #data = json.loads(manga)
    slug = mangalink.split('/')[4]
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
    print slug
    print _chapter_array
    c = 1
    for chapter in _chapter_array:
        if 'c0' in chapter:
            c = 0
            break
        if 'c1' in chapter:
            c = 1
            break
    for chapter in _chapter_array:
        print chapter
	print chapnumber
	print c 
	if (chapnumber):
		print 'aaaaaa'
		if int(chapnumber) == int(c):
			print 'aaaaabbba'
			response = requests.get(chapter)
			i = 1
			while 1:
            			picture = re.search("http://.*%d\.jpg" % i, response.text)
            			if (picture):
                			piclink = picture.group(0)
                			picdownload = requests.get(piclink)
					if not (os.path.isdir(slug + "/%d" % c)):
						os.makedirs(slug + "/%d" % c)
                			handle = open(slug + "/%d/%d.jpg" % (c,i), "w")
                			handle.write(picdownload.content)
                			handle.close()
                			i = i + 1
            			else:
					break
			break
		else:
			c = c + 1
			continue
	else:		
        	response = requests.get(chapter)
        	i = 1
        	while 1:
            		picture = re.search("http://.*%d\.jpg" % i, response.text)
            		if (picture):
                		piclink = picture.group(0)
                		picdownload = requests.get(piclink)
				if not (os.path.isdir(slug + "/%d" % c)):
               				os.makedirs(slug + "/%d" % c)
                		handle = open(slug + "/%d/%d.jpg" % (c,i), "w")
                		handle.write(picdownload.content)
                		handle.close()
                		i = i + 1
            		else:
                		break
        	c = c + 1
if __name__ == "__main__":
    mangalink = sys.argv[1]
    chapnumber = sys.argv[2]
    manga_download(mangalink,chapnumber)
