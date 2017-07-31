import requests
import sys
from os import path, system
from bs4 import BeautifulSoup
import re
import json
from multiprocessing import Pool
import os
import datetime
import time

if __name__ == "__main__":
    response = requests.get('http://mangapark.me/search')
    soup = BeautifulSoup(response.text)
    for tmp in soup.find_all('span',class_="either",hidefocus="true"):
        if "And mode" in tmp.text or "Or mode" in tmp.text:
            continue
        else:
            print tmp.text.replace(" ","-").lower()