# -*- coding: utf-8 -*-

# license: gpl v3

#it downloads all the images at full resolution (and some metadata) from a twitpic tag search and sort them by date
#python twitpic.py mypreferedtag

import os
import re
import sys
import time
import urllib

def undoHTMLEntities(text=''):
    text = re.sub('&lt;', '<', text)
    text = re.sub('&gt;', '>', text)
    text = re.sub('&amp;', '&', text)
    text = re.sub('&quot;', '"', text)
    text = re.sub('&#039;', '\'', text)
    return text

if len(sys.argv) > 1:
    tags = sys.argv[1:]
else:
    print 'tell me a tag to explore'
    sys.exit()

print "downloading photos with tags:", tags

#twitpic
for tag in tags:
    url = 'http://twitpic.com/tag/%s?page=' % (tag)
    raw = ''
    page = 1
    while not re.search(r'No images found', raw):
        f = urllib.urlopen('%s%s' % (url, page))
        raw = f.read()
        f.close()
        
        #extract images
        m = re.findall(r'(?i)<a href="/([a-z0-9]+)"><img', raw)
        if m:
            for id in m:
                time.sleep(3)
                f2 = urllib.urlopen('http://twitpic.com/%s' % id)
                raw2 = f2.read()
                f2.close()
                
                #metadata
                try:
                    username = re.findall(r'(?im)<a id="photo_username" class="nav-link" href="/photos/[^>]+">@([^<]+)</a>', raw2)[0]
                    date = re.findall(r'(?im)\s\s([a-z0-9 ]+, 2011)', raw2)[0]
                    desc = re.findall(r'(?im)data-text="([^>]+)" data-related=', raw2)[0]
                    desc = undoHTMLEntities(text=desc)
                except:
                    print "ERROR: no metadata, skiping..."
                    continue
                
                if not os.path.exists(date):
                    os.makedirs(date)
                
                filename = 'twitpic %s by %s on %s' % (id, username, date)
                print tag, 'Downloading http://twitpic.com/', id, username, date, desc[:40]
                
                if os.path.exists('%s/%s.jpg' % (date, filename)) and os.path.exists('%s/%s.txt' % (date, filename)):
                    print "image and descriptions were downloaded previously, skiping...."
                    continue
                
                #full resolution
                try:
                    f3 = urllib.urlopen('http://twitpic.com/%s/full' % id)
                    raw3 = f3.read()
                    f3.close()
                    fullimage = re.findall(r'(?im)<img src="([^>]+)"\s+alt=', raw3)[0]
                    urllib.urlretrieve(fullimage, '%s/%s.jpg' % (date, filename))
                    g = open('%s/%s.txt' % (date, filename), 'w')
                    output = """URL: http://twitpic.com/%s\nUploader: %s\nDate: %s\nDescription: %s\n\n""" % (id, username, date, desc)
                    g.write(output)
                    g.close()
                    time.sleep(10)
                except:
                    print 'ERROR while retrieving fullimage'
        page += 1
