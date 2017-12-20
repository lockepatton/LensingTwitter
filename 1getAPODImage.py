from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

DIR = "/Users/lockepatton/LensingTwitter/pictures"
url = "https://apod.nasa.gov/apod/astropix.html"
header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
soup = get_soup(url,header)

a = soup.find_all("img")[0]

imageExists = 0
for junk in str(a).split("\""):
    if junk[:5] == 'image':
        image = junk
        imageExists = 1

if imageExists:
    print "image found:", image

if not os.path.exists(DIR):
    os.mkdir(DIR)

img = os.path.join("https://apod.nasa.gov/apod/", image)
Type = image.split('.')[-1]

try:
    req = urllib2.Request(img, headers={'User-Agent' : header})
    raw_img = urllib2.urlopen(req).read()

    f = open(os.path.join(DIR , "AstroPicOfTheDay." + Type), 'wb')

    f.write(raw_img)
    f.close()
except Exception as e:
    print "could not load : "+img
    print e
