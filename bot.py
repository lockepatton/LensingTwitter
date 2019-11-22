import tweepy
import datetime
import urllib2
import numpy as np
import time
import lensAPOD

consumer_key = 'TAOrZdVmFkuefvKWs3WM6QQML'
consumer_secret = 'sXujMnXakPJD3v2464VyfNVeHVj8Kxwc1TJ3coAvsb0WqP8dZT'
access_token = '835329970801037312-lmfkZv0y8gW6qu5CKZuumFFdn3E8Ncc'
access_secret = 'QpyPSmFQSAV3z1cNlazb0tWwG6p72wjMedCiduIWBHpAJ'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

file = './pictures/AstroPicOfTheDay_Lensed.jpg'

def run_bot():
    # pulling down image and lensing it
    # lensAPOD.run_lensAPOD()

    # finding object title
    url = "https://apod.nasa.gov/apod/astropix.html"
    response = urllib2.urlopen(url)
    the_page = response.read()
    page = the_page.split('\n')

    centerlines = []
    for i,line in enumerate(page):
        if ('<center>' in line):
            centerlines.append(i)

    titlerow_id = centerlines[1]+1
    titlerow = page[titlerow_id]
    print('titlerow',titlerow)
    title = titlerow.split('/')[0][3:-2].strip()
    print('title',title)

    # day month year for link
    now = datetime.datetime.now()
    year = '{:02d}'.format(now.year-2000)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    day_month_year = '{}{}{}'.format(year, month, day)

    status = "A gravitationally lensed "+title+"! #Astronomy picture of the day. https://apod.nasa.gov/apod/ap"+day_month_year+'.html'
    # status = "A gravitationally lensed #astronomy picture of the day! https://apod.nasa.gov/apod/ap"+day_month_year+'.html'
    print(status)
    return status

status = run_bot()

# INTERVAL = 60 * 60 * 24  # every 24 hours
# INTERVAL = 15  # every 15 seconds, for testing
#
# while True:
#     print("About to run...")
#
#     status = run_bot()
#     api.update_with_media(file, status=status)
#
#     time.sleep(INTERVAL)
