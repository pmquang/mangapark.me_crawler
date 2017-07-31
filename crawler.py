import requests
import sys
from os import path, system
from bs4 import BeautifulSoup
import re
import json
from multiprocessing import Pool

MANGA_URL='http://mangapark.me'

def log (_info,_filename,_mode):
    try:
        handle = open(path.abspath(_filename), _mode)
        handle.write(str(_info))
        handle.close()
    except:
        print "Error while writing log!"
        exit()


def crawl(tag):
    try:
        if tag['target'] == '_blank' and 'cover' in tag['class']:
            manga = {}
            manga['title'] = str(tag['title'])
            manga['link']  = MANGA_URL + str(tag['href'])            
            #manga['fimage'] = str(tag.img['src'])
            
            response = requests.get(manga['link'])
            # Summary
            _summary_soup = BeautifulSoup(response.text)
            for _summary in _summary_soup.findAll('p'):
                if 'summary' in _summary.get('class','default'):
                    manga['summary'] = _summary.text.replace("\r\n", "")
            
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
            
            # Chapter
            # Oneshot Chapter
            #_chapter_array = []
            #_chapter = re.search("/manga/.*oneshot" , response.text)
            
            #if (_chapter):
            #    _chapter_array.append(MANGA_URL + _chapter.group(0))
            # Multiple chapter 
            #else:
            #    i = 0
            #    while 1:
            #        _chapter = re.search("/manga/.*c%d" % i, response.text)
            #        if (_chapter):
            #            _chapter_array.append(MANGA_URL + _chapter.group(0))
            #            i = i + 1
            #        else:
            #            if (i == 0):
            #                i = i + 1
            #                continue
            #            else:
            #                break
            #
            #manga['chapter'] = _chapter_array
            result = json.dumps(manga)
            return str(result)
    except:
        return False

if __name__ == "__main__":
    for i in range (1,309):
        response = requests.get("%s/genre/%d" % (MANGA_URL,i))
        soup = BeautifulSoup(response.text) 
        for tag in soup.findAll('a'):
            result = crawl(tag)
            if (result):
                log(result + "\n", "manga.txt","a+")