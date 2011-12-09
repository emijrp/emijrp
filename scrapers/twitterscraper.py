#!/usr/bin/python

import time
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
import sys

# Replace USERNAME with your twitter username
user = sys.argv[1]
url = u'http://twitter.com/%s?page=' % (user)
tweets_file = open('tweets-%s' % user, 'w')

for x in range(100000):
    print x
    f = urlopen(url+str(x))
    soup = BeautifulSoup(f.read())
    f.close()
    tweets = soup.findAll('span', {'class': 'entry-content'})
    dates = soup.findAll('span', {'class': 'published timestamp'})
    if len(tweets) == 0:
        break
    [tweets_file.write(tweets[i].renderContents() + '\n' + dates[i].renderContents() + '\n') for i in range(len(tweets))]
    # being nice to twitter's servers
    time.sleep(3)

tweets_file.close()
