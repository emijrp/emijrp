#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import time
import sys
import urllib

#http://i1.ytimg.com/vi/Us7iq61l7FY/hqdefault.jpg
#thumbs = [l.split(';') for l in open(sys.argv[0], 'r').read().splitlines()]
thumbs = open(sys.argv[1], 'r').read().splitlines()

c=0
for id in thumbs:
    print id
    url = 'http://www.youtube.com/watch?v=%s' % (id)
    f = urllib.urlopen(url)
    raw = unicode(f.read(), 'utf-8')
    f.close()
    try:
        uploader = re.findall(ur'<link itemprop="url" href="http://www.youtube.com/user/([^>]+?)">', raw)[0]
    except:
        print 'Error retrieveing uploader name'
        continue
    
    id2 = re.sub(ur'  *', u' ', id)
    os.system('wget -c http://i1.ytimg.com/vi/%s/hqdefault.jpg -O "YouTube - %s - %s.jpg"' % (id, uploader, id2))
    time.sleep(2)
    
    c+=1
    if c > 1100:
        break
