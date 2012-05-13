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

tags = ['12m15m']
photoids = []
for tag in tags:
    for pagenum in range(1,100): #max is around 60-70, but we manage the error below
        print tag, pagenum
        searchurl = "https://secure.flickr.com/search/?q=%s&l=cc&mt=all&adv=1&s=rec&page=%s" % (tag, pagenum)
        rawhtml = unicode(urllib.urlopen(searchurl).read(), 'utf-8')
        
        if re.search(ur"(?im)You may have reached the limit of how many results", rawhtml):
            print 'Max pagenum for this tag reachead'
            break
        
        if re.search(ur"(?im)We couldn\'t find anything matching your search", rawhtml):
            print 'No more photos for this tag'
            break
        
        for id in re.findall(ur"<span class=\"photo_container pc_t\"><a href=\"(/photos/[^/]+/[^/]+/)\"", rawhtml):
            if id not in photoids:
                photoids.append(id)
        
        #print photoids
        print len(photoids), 'photos'
