import requests
import sys
from os import path, system
from bs4 import BeautifulSoup
import re
import json
from multiprocessing import Pool
import os

MANGA_URL='http://mangapark.me'
noimage = "http://h.s.mangapark.me/img/no-cover.jpg"

def manga_download(manga):
    data = json.loads(manga)
    slug = data['link'].split('/')[4]
    chapterrepsond = requests.get(data['link'])
    _chapter_array = []
    _chapter = re.search("/manga/.*oneshot" , chapterrepsond.text)
    if (_chapter):
        _chapter_array.append(MANGA_URL + _chapter.group(0))
 
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
        response = requests.get(chapter)
        i = 1
        while 1:
            picture = re.search("http://.*%d\.jpg" % i, response.text)
            if (picture):
                piclink = picture.group(0)
                picdownload = requests.get(piclink)
                handle = open(slug + "/%d/%d.jpg" % (c,i), "w")
                handle.write(picdownload.content)
                handle.close()
                i = i + 1 
            else:
                break
        c = c + 1
if __name__ == "__main__":
    pool = Pool(processes=100)
    pool.imap(manga_download, [manga for manga in open ('manga.txt')])
    pool.close()
    pool.join()
        #handle = open(slug + "/icon.jpg", "w")
        #handle.write(imagecontent.content)
        #handle.close()
