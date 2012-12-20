#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 emijrp <emijrp@gmail.com>
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

import re
import urllib

user = 'suysulucha'
channel = 'http://bambuser.com/channel/%s' % (user)
rss = 'http://feed.bambuser.com/channel/%s.rss' % (user)

raw = urllib.urlopen(rss).read()
lastvideoid = re.findall(ur"(?im)<link>http://bambuser\.com/v/(\d+)</link>", raw)[0]

videoids = []
c = 0
pageurl = "http://bambuser.com/v/%s?page_profile_more_user=" % (lastvideoid)
raw2 = urllib.urlopen(pageurl).read()
limit = int(re.findall(ur"(?im)page_profile_more_user=\d+\">(\d+)</a></li></ul>", raw2)[0])
print 'Scraping videos from %d pages' % (limit)
while c < 1:
    pageurl2 = pageurl + str(c)
    raw3 = urllib.urlopen(pageurl2).read()
    videoids += re.findall(ur"(?im)<a class=\"preview-wrapper\" href=\"http://bambuser.com/v/(\d+)\">", raw3)
    c += 1

print 'Loaded ids for %d videos' % (len(videoids))

videos = {}
for videoid in videoids:
    print 'Loading metadata for video %s' % (videoid)
    videourl = "http://bambuser.com/v/%s" % (videoid)
    raw4 = urllib.urlopen(videourl).read()
    title = re.findall(ur"<span class=\"title\" title=\"([^>]*?)\"></span>", raw4)
    length = ''
    [likes, views, lives] = re.findall(ur"(?im)<span class=\"count-wrapper\">(\d+)? ?likes?</span></form><span class=\"broadcast-views\">(\d+) views? \((\d+) lives?\)</span>", raw4)[0]
    tags = ''
    comments = ''
    coord = re.findall(ur"(?im)\"lat\":\"([^\"]+?)\",\"lon\":\"([^\"]+?)\"", raw4)[0]
    date = re.findall(ur"(?im)<div id=\"broadcast-date\">\s*<p>(\d+ [a-z]+ \d\d:\d\d CET)</p>", raw4)[0]
    if not likes:
        likes = 0
    views = int(views)
    lives = int(lives)
    print '%s likes, %s views, %s lives' % (likes, views, lives)
    print '%s, %s' % (coord[0], coord[1])
    print date
    videos[videoid] = {
        'likes': likes, 'views': views, 'lives': lives,
        'coord': [coord[0][0], coord[0][1]],
        'date': date,
    }
