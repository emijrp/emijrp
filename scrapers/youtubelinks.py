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
import time
import urllib

filenamevideos = "youtube-videos.txt"
filenametags = "youtube-tags.txt"

tags = [l.strip() for l in open(filenametags, 'r').readlines()]
videos = []
for tag in tags:
    for pagenum in range(1, 51):
        if os.path.exists(filenamevideos):
            for l in open(filenamevideos, "r").readlines():
                l = l.strip()
                if not l in videos:
                    videos.append(l)
        rawhtml = unicode(urllib.urlopen("http://www.youtube.com/results?search_type=videos&search_query=%s&page=%s" % (tag, pagenum)).read(), 'utf-8')
        
        #no hay ninguno?
        if re.search(ur"No hay resultados de vídeo de", rawhtml):
            print 'No videos for this tag'
            break
        ids = re.findall(ur"/watch\?v=([0-9a-zA-Z\-\_]+)\"", rawhtml)
        for id in ids:
            videourl = "http://www.youtube.com/watch?v=%s" % (id)
            if not videourl in videos:
                videos.append(videourl)
        videos.sort()
        f = open(filenamevideos, "w")
        output = '\n'.join(videos)
        f.write(output.encode('utf-8'))
        f.close()
        print 'Total videos', len(videos)
        
        #es esta la última página?
        if re.search(ur"(?im)\"yt-uix-button-content\">%d</span></a>&nbsp;\s*</div>" % (pagenum), rawhtml):
            print 'No more videos for this tag'
            break
        
        time.sleep(1)
