# -*- coding: utf-8 -*-

# Copyright (C) 2011 emijrp
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
import random
import re
import time
import urllib

"""
http://knol.google.com/k/knol/Search?q=incategory%3Acomputaci%C3%B3n&start=0&num=50

<li class="knol-search-bullet"><div class="knol-search-knol"><div class="knol-search-left"><div class="knol-search-knol-image-c"><img class="knol-search-knol-image knol-search-knol-image-sized" src="/c/photos/public/AIbEiAIAAABDCPLa0afuk_ThISILdmNhcmRfcGhvdG8qKDA0M2M4YmRmMWM0N2U2ODk2OWUzMzQ2ODU5ZGM2NTk0ZjY4NmRkYzIwAeKU766LYhPDnvHgDJ-VMPvBajVf" alt="Abrir puerto..." title="Abrir puertos en modem 2wire de Telmex" /></div></div><div class="knol-search-mid"><div class="knol-title-wrapper"><a class="knol-search-knol-title" href="/k/abrir-puertos-en-modem-2wire-de-telmex" target="">Abrir puertos en modem 2wire de Telmex</a></div><div class="knol-search-knol-author"><span>De <a href="/k/angelinux-slack/angelinux-slack/zm2rb13bda/0">Angelinux Slack</a></span></div><div class="knol-search-knol-snippet">Al tener contratado el servicio de Internet "Infinitum" de telmex, se nos proporcionaba un modem 2wire, al cual nos...</div><div id="knol-search-redirect-url-zm2rb13bda.30" class="knol-search-redirect-url"></div></div><div class="knol-search-right"><div class="knol-search-knol-author"><div class="knol-search-knol-info knol-search-knol-info-pageviews">Vistas: <span class="knol-search-knol-info-details">12000</span></div><div class="knol-clearer-div"></div><div class="knol-clearer-div"></div><span class="knol-search-knol-info knol-search-knol-info-version">Versión publicada: <span class="knol-search-knol-info-details">27</span></span><div class="knol-clearer-div"></div><span class="knol-search-knol-info knol-search-knol-info-edited">Editado a la(s): <span class="knol-search-knol-info-details">29/03/2010 10:42</span></span><div class="knol-clearer-div"></div><div class="knol-search-knol-info"></div><div class="knol-clearer-div"></div></div></div><div class="knol-clearer-div"></div></div></li>
"""

def removetildes(t):
    t = re.sub(ur"(?im)[áä]", ur"a", t)
    t = re.sub(ur"(?im)[éë]", ur"e", t)
    t = re.sub(ur"(?im)[íï]", ur"i", t)
    t = re.sub(ur"(?im)[óö]", ur"o", t)
    t = re.sub(ur"(?im)[úü]", ur"u", t)
    t = re.sub(ur"(?im)[ñ]", ur"n", t)
    t = re.sub(ur"(?im)[ç]", ur"c", t)
    return t

knolsfilename = 'knols.txt'
knolstxt = open(knolsfilename, 'r')
knols = [line.split('\t') for line in unicode(knolstxt.read(), 'utf-8').splitlines()]
knolstxt.close()

print 'Loaded %d knols metadata' % (len(knols))

#campo username es difícil de capturar, puede tener varios autores, lo limitamos a 1500 chars que serían unos 10 autores, suficiente...
knol_r = re.compile(ur"(?im)<a class=\"knol-search-knol-title\" href=\"(?P<knolurl>[^>]+)\" target=\"\">(?P<knoltitle>[^<]+)</a></div><div class=\"knol-search-knol-author\"><span>[^<>]+(?P<username>.{,1500})</span></div>(<div class=\"knol-search-knol-snippet\">(?P<description>[^<]+)</div>)?<div id=\"knol-search-redirect[^=]+\" class=\"knol-search-redirect-url\">(<span id=\"knol-search-redirect-url-display-[^=]+\" class=\"knol-search-redirect-url-display\"></span><span id=\"knol-search-redirect-url-set-[^=]+\" class=\"knol-search-redirect-url-set\"></span>)?</div></div><div class=\"knol-search-right\"><div class=\"knol-search-knol-author\">(<div class=\"knol-search-knol-info knol-search-knol-info-pageviews\">[^<]+<span class=\"knol-search-knol-info-details\">(?P<views>\d+)</span></div><div class=\"knol-clearer-div\"></div>)?<div class=\"knol-clearer-div\"></div><span class=\"knol-search-knol-info knol-search-knol-info-version\">[^<]+<span class=\"knol-search-knol-info-details\">(?P<publishedrevision>\d+)</span></span><div class=\"knol-clearer-div\"></div><span class=\"knol-search-knol-info knol-search-knol-info-edited\">[^<]+<span class=\"knol-search-knol-info-details\">(?P<date>[^<]+)</span></span>")

langs = ['es', 'en', 'fr', 'de', 'pt', 'it', 'nl', ] #other codifications ko, ru, ar, iw, ja
tags = set([])
f = open('tags.txt', 'r')
tags = tags.union(set(unicode(f.read(), 'utf-8').splitlines()))
f.close()
tagsdone = set([])
f = open('tagsdone.txt', 'r')
tagsdone = tagsdone.union(set(unicode(f.read(), 'utf-8').splitlines()))
f.close()
tags = tags - tagsdone
while len(tags) > 0:
    tag = random.sample(tags, 1)[0]
    for lang in langs:
        num = 50 #max knols per page result is 50, do not increase or you will cause errors
        start = 0
        raw = ''
        while start == 0 or re.findall(knol_r, raw):
            print 'Exploring tag...', tag, ', for lang', lang, ', from', start, 'to', start+num
            
            url = 'http://knol.google.com/k/knol/Search?' + urllib.urlencode({'q': 'incategory:%s' % (tag), 'start': str(start), 'num': str(num), 'hl': lang})
            f = urllib.urlopen(url)
            raw = unicode(f.read(), 'utf-8')
            f.close()
            
            m = re.finditer(knol_r, raw)
            newtags = set([])
            for i in m:
                dupe = False
                for knol in knols:
                    if knol[0] == i.group('knolurl'):
                        dupe = True
                        break
                
                if dupe:
                    continue
                else:
                    #split usernames if needed
                    username = []
                    userurl = []
                    for userurl1, username1 in re.findall(ur"<a href=\"([^<]+)\">([^<]+)</a>", i.group('username')):
                        username.append(username1)
                        userurl.append(userurl1)
                    userurl = '|'.join(userurl)
                    username = '|'.join(username)
                    try: #codification errors sometimes
                        knoltitle = i.group('knoltitle')
                        knoltitle = re.sub(ur"(?m)[\t\n]", ur" ", knoltitle) #removing new lines if any
                        description = i.group('description') and i.group('description') or ''
                        description = re.sub(ur"(?m)[\t\n]", ur" ", description) #removing new lines if any
                    except:
                        continue #skip to next knol in results page
                    
                    knols.append([i.group('knolurl'), knoltitle, userurl, username, description, i.group('views') and i.group('views') or '', i.group('publishedrevision'), i.group('date'), lang])
                
                    try: #codification errors sometimes
                        for newtag in re.sub(ur"(?im)[^a-z]", ur" ", removetildes(i.group('knoltitle').lower())).split(' '):
                            if len(newtag) >= 4 and newtag not in tags and newtag not in tagsdone: #min 4 for knol
                                tags.add(newtag)
                    except:
                        pass
            
            knolstxt = open('knols.txt', 'w')
            errors = 0
            for knol in knols:
                try:
                    outputline = u'%s\n' % ('\t'.join(knol))
                    knolstxt.write(outputline.encode('utf-8'))
                except:
                    errors += 1
            knolstxt.close()
            print '%d knols explored, %d tags done, %d tags left, %d errors' % (len(knols), len(tagsdone), len(tags), errors)
            
            time.sleep(random.randint(1, 5))
            start += num
    
    tagsdone.add(tag)
    tags = tags - tagsdone
    f = open('tags.txt', 'w')
    output = '\n'.join(tags)
    f.write(output.encode('utf-8'))
    f.close()
    f = open('tagsdone.txt', 'w')
    output = '\n'.join(tagsdone)
    f.write(output.encode('utf-8'))
    f.close()
