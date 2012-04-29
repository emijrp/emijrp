# -*- coding: utf-8 -*-

# Copyright (C) 2011 TodoGratix
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
import wikipedia

#más en http://ocw.universia.net/es/instituciones-integrantes-iberoamericanas-opencourseware.php
#codification errors: 'http://www.unav.es/ocw/rss/ocw.rss',

tgsite = wikipedia.Site('todogratix', 'todogratix')
rsss = [
#'http://ocw.unican.es/rss_all',
#'http://ocw.uniovi.es/ocw/rss/file.php/rss.xml',
#'http://ocw.innova.uned.es/ocwuniversia/RSS',
#'http://ocw.ehu.es/front-page/rss',
#'http://ocw.upm.es/rss',
#'http://ocw.uca.es/rss/rss.xml',
#'http://ocw.uv.es/rss',
#'http://ocw.ua.es/front-page/rss',
#'http://ocw.usal.es/rss',
#'http://ocw.unizar.es/ocw/rss',
#'http://ocwus.us.es/front-page/rss',
#'http://ocw.uib.es/ocw/courselist/rss',

'http://ocw.ceu.es/rss',
'http://ocw.uoc.edu/rss',
'http://ocw.uva.es/rss/file.php/rss.xml',
'http://www.uhu.es/sevirtual/ocw/rss/',
'http://ocw.ulpgc.es/front-page/courselist/rss',
'http://ocw.uab.cat/cursos/rss',
'http://edunetworks.ugr.es/ocw/file.php/1/opencoursewareugr.xml',
#'http://ocw.uc3m.es/front-page/courses/rss',
]

skip = 'TRADUCCION GENERAL (ALEMAN)'
for rss in rsss:
    raw = urllib.urlopen(rss).read()
    try:
        raw = unicode(raw, 'utf-8')
        try:
            raw = unicode(raw, 'iso-8859-1')
        except:
            continue
    except:
        pass
    raw = raw.split('</channel>')[1]
    ocw = re.sub(ur"(?im)^https?://([^/]+)/.*$", ur"\1", rss)
    print len(raw), ocw, rss
    
    for t in raw.split('</item>'):
        try:
            title = re.findall(ur"(?im)<title>([^<]*)</title>", t)[0].strip()
        except:
            continue
        title = re.sub('\[', '(', title)
        title = re.sub('\]', ')', title)
        if skip:
            if title == skip:
                skip = ''
            else:
                continue
        try:
            link = re.sub(ur"&amp;", "&", re.findall(ur"(?im)<link>([^<]*)</link>", t)[0].strip())
        except:
            continue
        try:
            description = re.findall(ur"(?im)<description>([^<]*)</description>", t)[0].strip()
            if len(description) <= 10:
                description = ''
        except:
            continue
        try:
            creators_ = t.split('<dc:creator>')[1].split('</dc:creator>')[0].strip()
        except:
            continue
        creators = []
        if creators_:
            if re.search(ur"<rdf:li>", creators_):
                creators = re.findall(ur"<rdf:li>([^<]*)</rdf:li>", creators_)
            else:
                creators = [creators_]
        #print creators
        tags_ = ''
        if re.search(ur'<dc:subject>', t):
            tags_ = t.split('<dc:subject>')[1].split('</dc:subject>')[0].strip().lower()
        tags = []
        if tags_:
            if re.search(ur"<rdf:li>", tags_):
                tags = re.findall(ur"<rdf:li>([^<]*)</rdf:li>", tags_)
            else:
                tags = [tags_]
        #print tags
        #<cc:license rdf:resource="http://creativecommons.org/licenses/by-nc-sa/3.0/"/>
        lic = ''
        if re.search(ur"<cc:license", t):
            try:
                lic = re.findall(ur"(?im)<cc:license rdf:resource=\"([^\"]+?)\"/>", t)[0].strip()
            except:
                continue
            lic = u'CC %s' % (re.sub(ur"[\-\/]", ur" ", lic.split('licenses/')[1]).upper().strip())
        output = u"""{{Infobox Obra
|tipo=ocw
|título=%s
|autor=%s
|género=%s
|idioma=Español
|licencia=%s
|sinopsis=%s
}}
* %s
""" % (title, u', '.join(creators), u', '.join(tags), lic, description, link)
        print output
        page = wikipedia.Page(tgsite, '%s (%s)' % (title, ocw))
        if not page.exists():
            page.put(output, output)
