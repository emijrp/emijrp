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

import datetime
import re
import sys
import urllib

def month2number(month):
    m = month.lower()
    if m == 'jan':
        return '01'
    elif m == 'feb':
        return '02'
    elif m == 'mar':
        return '03'
    elif m == 'apr':
        return '04'
    elif m == 'may':
        return '05'
    elif m == 'jun':
        return '06'
    elif m == 'jul':
        return '07'
    elif m == 'aug':
        return '08'
    elif m == 'sep':
        return '09'
    elif m == 'oct':
        return '10'
    elif m == 'nov':
        return '11'
    elif m == 'dec':
        return '12'
    return ''

user = sys.argv[1]
channel = 'http://bambuser.com/channel/%s' % (user)
rss = 'http://feed.bambuser.com/channel/%s.rss' % (user)

raw = urllib.urlopen(rss).read()
lastvideoid = re.findall(ur"(?im)<link>http://bambuser\.com/v/(\d+)</link>", raw)[0]

videoids = []
lengths = []
thumbs = []
c = 0
pageurl = "http://bambuser.com/v/%s?page_profile_more_user=" % (lastvideoid)
raw2 = urllib.urlopen(pageurl).read()
limit = 1
try:
    limit = int(re.findall(ur"(?im)page_profile_more_user=\d+\">(\d+)</a></li></ul>", raw2)[0])
except:
    pass
print 'Scraping videos from %d pages' % (limit)
while c < limit:
    pageurl2 = pageurl + str(c)
    raw3 = urllib.urlopen(pageurl2).read()
    videoids += re.findall(ur"(?im)<a class=\"preview-wrapper\" href=\"http://bambuser.com/v/(\d+)\">", raw3)
    lengths += re.findall(ur"(?im)<div class=\"preview-length\"><span>([^<]*?)</span></div>", raw3)
    thumbs += re.findall(ur"(?im)<img class=\"preview\" src=\"(https?://[^\"]+?\.(?:jpe?g|pne?g))\"", raw3)
    c += 1

print 'Loaded ids for %d videos' % (len(videoids))

videos = {}
c = 0
for videoid in videoids:
    #print 'Loading metadata for video %s' % (videoid)
    videourl = "http://bambuser.com/v/%s" % (videoid)
    raw4 = urllib.urlopen(videourl).read()
    title = re.findall(ur"<span class=\"title\" title=\"([^>]*?)\"></span>", raw4)[0]
    length = lengths[c]
    thumb = thumbs[c]
    urllib.urlretrieve(thumb, 'Bambuser %s %s.%s' % (videoid, user, thumb.split('.')[-1]))
    try:
        [likes, views, lives] = re.findall(ur"(?im)<span class=\"count-wrapper\">(\d+)? ?likes?</span></form><span class=\"broadcast-views\">(\d+) views? \((\d+) lives?\)</span>", raw4)[0]
    except:
        [likes, views, lives] = ['0', '0', '0']
    comments = ''
    coord = re.findall(ur"(?im)\"lat\":\"([^\"]+?)\",\"lon\":\"([^\"]+?)\"", raw4)[0]
    if coord:
        coord = '%s, %s' % (coord[0], coord[1])
    date = ''
    date2 = ''
    hour = ''
    try:
        date2 = re.findall(ur"(?im)<div id=\"broadcast-date\">\s*<p>([^<]*?)</p>", raw4)[0]
    except:
        date2 = re.findall(ur"(?im)<div id=\"broadcast-date\">\s*<p id=\"upload-recorded-date\"><span class=\"date-label\">Recorded </span>([^<]*?)<br>", raw4)[0]
    #9 Nov 2009 18:39 CET
    if not ':' in date2.split(' ')[2] and int(date2.split(' ')[2]) > 2000 and int(date2.split(' ')[2]) < 2020:
        date = '%s/%s/%02d' % (date2.split(' ')[2], month2number(date2.split(' ')[1]), int(date2.split(' ')[0]))
        hour = date2.split(' ')[3]
    else:
        date = '%s/%s/%02d' % (datetime.datetime.now().year, month2number(date2.split(' ')[1]), int(date2.split(' ')[0]))
        hour = date2.split(' ')[2]
    
    if not likes:
        likes = '0'
    tags = re.findall(ur"(?im)<span class=\"tag\" style=\"display:none;\" title=\"([^>]*?)\"></span>", raw4)
    videos[videoid] = {
        'likes': likes, 'views': views, 'lives': lives,
        'coord': coord,
        'date': date,
        'hour': hour,
        'length': length,
        'tags': tags,
        'user': user,
    }
    print ';;;'.join([videoid, coord, date, hour, length, likes, views, lives, title, ', '.join(tags), user])
    c += 1

