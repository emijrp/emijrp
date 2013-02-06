#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import time
import sys
import urllib

"""
http://bambuser.com/v/3347347

http://archive.bambuser.com/m/00/a_0020/a86ec9df-5f59-4e61-9688-4759266e0498-6e8ed1.flv

content="http://cf.archive.bambuser.com/m/00/a_0020/a86ec9df-5f59-4e61-9688-4759266e0498-7adb92.jpg?2"
"""
 
#thumbs = [l.split(';') for l in open(sys.argv[0], 'r').read().splitlines()]
thumbs = open(sys.argv[1], 'r').read().splitlines()

c=0
for id in thumbs:
    print id
    url = 'http://bambuser.com/v/%s' % (id)
    f = urllib.urlopen(url)
    raw = unicode(f.read(), 'utf-8')
    f.close()
    try:
        uploader = re.sub(ur'\+', ur' ', re.findall(ur'<span class="username" title="([^>]+?)"></span>', raw)[0])
        thumburl = re.findall(ur'<meta property="og:image" content="([^>]+?)" />', raw)[0]
    except:
        print 'Error retrieveing the thumb url'
        continue
    
    os.system('wget -c %s -O "Bambuser - %s - %s.jpg"' % (thumburl, uploader, id))
    time.sleep(2)
    
    c+=1
    if c > 2000:
        break
