#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import re
import urllib

users = [u'ignaciomorer']

for user in users:
    morepages = True
    c = 0
    scrapers = []
    while morepages:
        c += 1
        url = 'https://scraperwiki.com/profiles/%s/?page=%d' % (user, c)
        html = urllib.urlopen(url).read()
        morepages = re.search(ur"\?page=", html) and True or False
        scrapers += re.findall(ur"(?im)/scrapers/([^/]+)/", html)
    scrapers = list(set(scrapers))
    print user, scrapers
    for scraper in scrapers:
        #csv
        downloadurl = u"https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=%s&query=select+*+from+%%60swdata%%60&apikey=" % (scraper)
        downloadname = u"%s-%s-%s.csv" % (user, scraper, datetime.date.today().strftime('%Y%m%d'))
        os.system('wget -c "%s" -O %s' % (downloadurl, downloadname))
        
        #json
        downloadurl = u"https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=json&name=%s&query=select+*+from+%%60swdata%%60&apikey=" % (scraper)
        downloadname = u"%s-%s-%s.json" % (user, scraper, datetime.date.today().strftime('%Y%m%d'))
        os.system('wget -c "%s" -O %s' % (downloadurl, downloadname))
        
        #sqlite
        downloadurl = u"https://scraperwiki.com/scrapers/export_sqlite/%s/" % (scraper)
        downloadname = u"%s-%s-%s.sqlite" % (user, scraper, datetime.date.today().strftime('%Y%m%d'))
        os.system('wget -c "%s" -O %s' % (downloadurl, downloadname))
        
        
