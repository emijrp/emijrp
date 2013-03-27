#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 emijrp
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import os
import re
import sys
import time
import urllib

filenametags = "bambuser-tags.txt"
tags = [l.strip() for l in open(filenametags, 'r').readlines()]
for tag in tags:
    videos = []
    filenamevideos = "bambuser-videos-%s.txt" % (tag)
    for pagenum in range(0, 500):
        print 'tag', tag, 'pagenum', pagenum
        if os.path.exists(filenamevideos):
            for l in open(filenamevideos, "r").readlines():
                l = l.strip()
                if not l in videos:
                    videos.append(l)
        rawhtml = unicode(urllib.urlopen("http://bambuser.com/search/bambuser_search/%%2523%s?page=%s" % (tag, pagenum)).read(), 'utf-8') #prefijo # siempre
        
        #no hay ninguno?
        if re.search(ur"Your search yielded no results", rawhtml):
            if pagenum == 0:
                print 'No videos for this tag'
                time.sleep(2)
                break
            else: #bambuser fails a lot, retry until moves from page 1 to forward
                while re.search(ur"Your search yielded no results", rawhtml):
                    print 'Retrying to download the same page'
                    time.sleep(5)
                    rawhtml = unicode(urllib.urlopen("http://bambuser.com/search/bambuser_search/%s?page=%s" % (tag, pagenum)).read(), 'utf-8')
        
        ids = re.findall(ur"http://bambuser.com/v/([0-9]+)\"", rawhtml)
        for id in ids:
            videourl = "http://bambuser.com/v/%s" % (id)
            if not videourl in videos:
                videos.append(videourl)
        videos.sort()
        f = open(filenamevideos, "w")
        output = '\n'.join(videos) + '\n'
        f.write(output.encode('utf-8'))
        f.close()
        print 'Total videos', len(videos)
        
        #es esta la última página?
        if not re.search(ur"<div class=\"pager\">", rawhtml) or \
           re.search(ur"(?im)<strong class=\"pager-current\">%d</strong></span></div>" % (pagenum), rawhtml):
            print 'No more videos for this tag'
            time.sleep(0.5)
            break
        
        time.sleep(0.5)
