#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2013 emijrp
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
import wikipedia

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

def unquote(s):
    s = re.sub(ur"&quot;", u'"', s)
    s = re.sub(ur"&#39;", u"'", s)
    s = re.sub(ur"\|", u"-", s)
    s = re.sub(ur'\\"', u'"', s)
    s = re.sub(ur'[\[\]]', u'', s)
    return s

def gethtml(url):
    f = urllib.urlopen(url)
    raw = unicode(f.read(), 'utf-8')
    f.close()
    return raw

ids = open('bambuser-videos.txt', 'r').read().splitlines()
for id in ids:
    url = 'http://bambuser.com/v/%s' % (id)
    raw = gethtml(url)
    
    try:
        title = re.findall(ur'<span class="title" title="([^>]+?)"></span>', raw)[0]
        title = unquote(title)
        dateupload = u''
        daterecorded = u''
        if re.search(ur'(?im)<div id="broadcast-date">\s*<p>\s*(\d+ [a-z]+ [\d:]+) [^<]*?</p>', raw):
            dateupload = re.findall(ur'(?im)<div id="broadcast-date">\s*<p>\s*(\d+ [a-z]+ [\d:]+) [^<]*?</p>', raw)[0]
            if not ':' in dateupload:
                dateupload = u'%s-%s-%02d' % (dateupload.split(' ')[2], month2number(dateupload.split(' ')[1]), int(dateupload.split(' ')[0]))
            else:
                dateupload = u'%s-%s-%02d' % (datetime.datetime.now().strftime('%Y'), month2number(dateupload.split(' ')[1]), int(dateupload.split(' ')[0])) 
            daterecorded = dateupload
        elif re.search(ur"(?im)<span class=\"date-label\">Recorded </span>", raw):
            daterecorded = re.findall(ur'(?im)<span class="date-label">Recorded </span>(\d+ [a-z]+ [\d:]+) ', raw)[0]
            if not ':' in dateupload:
                daterecorded = u'%s-%s-%02d' % (daterecorded.split(' ')[2], month2number(daterecorded.split(' ')[1]), int(daterecorded.split(' ')[0]))
            else:
                daterecorded = u'%s-%s-%02d' % (datetime.datetime.now().strftime('%Y'), month2number(daterecorded.split(' ')[1]), int(daterecorded.split(' ')[0]))
            dateupload = re.findall(ur'(?im)<span class="date-label">Uploaded </span>(\d+ [a-z]+ [\d:]+) ', raw)[0]
            if not ':' in dateupload:
                dateupload = u'%s-%s-%02d' % (dateupload.split(' ')[2], month2number(dateupload.split(' ')[1]), int(dateupload.split(' ')[0]))
            else:
                dateupload = u'%s-%s-%02d' % (datetime.datetime.now().strftime('%Y'), month2number(dateupload.split(' ')[1]), int(dateupload.split(' ')[0]))
        uploader = re.findall(ur'<span class="username" title="([^>]+?)"></span>', raw)[0]
        coord = u''
        if re.search(ur"bambuser_com:position:latitude", raw):
            coord = re.findall(ur"(?im)<meta property=\"bambuser_com:position:latitude\" content=\"([^\"]+?)\" */><meta property=\"bambuser_com:position:longitude\" content=\"([^\"]+?)\" */>", raw)[0]
            if coord:
                coord = '%s, %s' % (coord[0], coord[1])
    except:
        print u'Error accediendo a los parámetros del streaming', id
        g = open('streamingerrors.ids', 'a')
        g.write(u'%s\n' % (id))
        g.close()
        continue
        
    output = u"""{{Infobox Archivo
|embebido=Bambuser
|embebido id=%s
|embebido título=%s
|fecha de creación=%s
|fecha de publicación=%s
|autor={{bambuser channel|%s}}
|coordenadas=%s
}}
""" % (id, title, daterecorded, dateupload, uploader, coord)
    
    p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), 'File:Bambuser - %s - %s.jpg' % (uploader, id))
    if p.exists():# and len(p.get()) < 10:
        print output
        p.put(output, u'BOT - Importando metadatos del streaming de Bambuser http://bambuser.com/v/%s' % (id))
        time.sleep(3)
