#!/usr/bin/python
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

import catlib
import re
import pagegenerators
import sys
import urllib
import wikipedia

s = wikipedia.Site('wikiindex', 'wikiindex')
cat = catlib.Category(s, 'Category:MediaWiki')

start = '!'
if len(sys.argv) == 2:
    start = sys.argv[1]

gen = pagegenerators.CategorizedPageGenerator(cat, start=start)
pre = pagegenerators.PreloadingGenerator(gen, pageNumber=50)

"""
{{Size
|pages = <!--Necessary. Type the plain number of pages here - no thousands separators.-->
wiki pages, wiki_pages

|statistics URL = <!--Preferred, source of page count (mostly a statistics page). If unknown leave void.-->
wiki statistics URL, wiki_statistics_URL

|wikiFactor = <!--Optional. If unknown leave void. (See Proposal:wikiFactor)-->
|wikiFactor URL = <!--Optional, source of wiki factor. If unknown leave void.-->
}}
"""

size_r = re.compile(ur"""(?im)(?P<all>\{\{\s*Size\s*((\s*\|\s*(?P<pages>pages|wiki[ _]pages)\s*=\s*(?P<pages_value>\d*)\s*[^\|\}]*\s*)|(\s*\|\s*(?P<pagesurl>statistics[ _]URL|wiki[ _]statistics[ _]URL)\s*=\s*(?P<pagesurl_value>https?://[^ \|\}\<]*)\s*[^\|\}]*\s*)|(\s*\|\s*(?P<wikifactor>wikiFactor)\s*=\s*(?P<wikifactor_value>\d*)\s*[^\|\}]*\s*)|(\s*\|\s*(?P<wikifactorurl>wikiFactor[ _]URL)\s*=\s*(?P<wikifactorurl_value>http://[^ \|\}\<]*)\s*[^\|\}]*\s*))+\s*\|?\s*\}\})""")

for page in pre:
    if not page.exists() or page.isRedirectPage():
        continue
    
    wikipedia.output('--> %s <--' % (page.title()))
    wtext = page.get()
    newtext = wtext
    
    m = size_r.finditer(wtext)
    for i in m:
        all = i.group('all') and i.group('all').strip() or ''
        pages = i.group('pages') and i.group('pages').strip() or ''
        pagesurl = i.group('pagesurl') and i.group('pagesurl').strip() or ''
        wikifactor = i.group('wikifactor') and i.group('wikifactor').strip() or ''
        wikifactorurl = i.group('wikifactorurl') and i.group('wikifactorurl').strip() or ''
        
        pages_value = i.group('pages_value') and i.group('pages_value').strip() or '0'
        pagesurl_value = i.group('pagesurl_value') and i.group('pagesurl_value').strip() or ''
        wikifactor_value = i.group('wikifactor_value') and i.group('wikifactor_value').strip() or ''
        wikifactorurl_value = i.group('wikifactorurl_value') and i.group('wikifactorurl_value').strip() or ''
        
        #get new values
        n = re.findall(ur"(https?://[^\|\}\]]+\?action=raw|https?://[^\|\}\]]+:Statistics)", pagesurl_value)
        if n:
            raw = ''
            try:
                url = n[0]
                if url.endswith(":Statistics"):
                    url += '?action=raw'
                f = urllib.urlopen(url)
                raw = unicode(f.read(), 'utf-8')
                f.close()
            except:
                break
            o = re.findall(ur"total=\d+;good=(\d+);", raw)
            if o:
                if o[0] and int(pages_value) != int(o[0]):
                    summary = u"BOT - Updating size: %s -> %s" % (pages_value, o[0])
                    pages_value = o[0]
                else:
                    break
            else:
                break
        else:
            break
        #end get
        
        #recalculate wikifactor
        pass #todo, leave AS IS meanwhile
        #end recalculate
        
        """print pages, pages_value
        print pagesurl, pagesurl_value
        print wikifactor, wikifactor_value
        print wikifactorurl, wikifactorurl_value"""
        
        newvalues = u"""{{Size
| %s = %s <!--Necessary. Type the plain number of pages here - no thousands separators.-->
| %s = %s <!--Preferred, source of page count (mostly a statistics page). If unknown leave void.-->
| %s = %s <!--Optional. If unknown leave void. (See Proposal:wikiFactor)-->
| %s = %s <!--Optional, source of wiki factor. If unknown leave void.-->
}}""" % (pages and pages or 'pages', pages_value and pages_value or '', pagesurl and pagesurl or 'statistics URL', pagesurl_value and pagesurl_value or '', wikifactor and wikifactor or 'wikiFactor', wikifactor_value and wikifactor_value or '', wikifactorurl and wikifactorurl or 'wikiFactor URL', wikifactorurl_value and wikifactorurl_value or '')
        newtext = wtext.replace(all, newvalues)
        if wtext != newtext:
            wikipedia.showDiff(wtext, newtext)
            page.put(newtext, summary)
            
        break
