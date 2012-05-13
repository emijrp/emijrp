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

import os
import re
import time
import urllib

filenametags = "flickr-tags.txt"
tags = [l.strip() for l in open(filenametags, 'r').readlines()]
for tag in tags:
    photos = []
    filenamephotos = "flickr-photos-%s.txt" % (tag)
    for pagenum in range(1,100): #max is around 60-70, but we manage the error below
        print tag, pagenum
        if os.path.exists(filenamephotos):
            for l in open(filenamephotos, "r").readlines():
                l = l.strip()
                if not l in photos:
                    photos.append(l)
        searchurl = "https://secure.flickr.com/search/?q=%s&l=cc&mt=all&adv=1&s=rec&page=%s" % (tag, pagenum)
        rawhtml = unicode(urllib.urlopen(searchurl).read(), 'utf-8')
        
        if re.search(ur"(?im)<div class=\"NoneFound\">", rawhtml):
            print 'No more photos for this tag'
            break
        
        for id in re.findall(ur"<span class=\"photo_container pc_t\"><a href=\"(/photos/[^/]+/[^/]+/)\"", rawhtml):
            photourl = 'https://secure.flickr.com%s' % (id)
            if photourl not in photos:
                photos.append(photourl)
        
        #save
        photos.sort()
        f = open(filenamephotos, "w")
        output = '\n'.join(photos) + '\n'
        f.write(output.encode('utf-8'))
        f.close()
        
        print len(photos), 'photos'
        
        time.sleep(0.2)
