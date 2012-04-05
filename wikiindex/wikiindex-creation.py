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

import catlib
import re
import pagegenerators
import sys
import urllib
import wikipedia

s = wikipedia.Site('wikiindex', 'wikiindex')
#cat = catlib.Category(s, 'Category:MediaWiki')

langs = {'en': 'English', 'en-gb': 'English', 'es': 'Spanish', 'it': 'Italian', 'pt-br': 'Brazilian Portuguese', 'ru': 'Russian'}
start = '!'
if len(sys.argv) == 2:
    start = sys.argv[1]

wikis = urllib.urlopen('http://wikiteam.googlecode.com/svn/trunk/listsofwikis/referata.com').read().splitlines()
for wiki in wikis:
    #exists?
    if not re.search(ur"(?i)There are no results for this report", urllib.urlopen('http://wikiindex.org/index.php?title=Special:LinkSearch&target=%s&namespace=0' % (re.sub(ur"(?i)(https?://)(www\.)?", ur"", wiki))).read()):
       print wiki, 'exists, skiping...'
       log = wikipedia.Page(s, u'User:Emijrp/Log')
       log.put(u'%s\n* [http://wikiindex.org/index.php?title=Special:LinkSearch&target=%s&namespace=0 %s] exists' % (log.get(), re.sub(ur"(?i)(https?://)(www\.)?", ur"", wiki), wiki), u'BOT - Adding %s' % (wiki))
       continue
    
    print 'Creating', wiki
    
    raw = unicode(urllib.urlopen(wiki).read(), 'utf-8')
    if re.search(ur"(?i)404 Error\: Page Not Found", raw):
        print "Wiki was deleted?"
        log = wikipedia.Page(s, u'User:Emijrp/Log')
        log.put(u'%s\n* %s error 404' % (log.get(), wiki), u'BOT - Adding %s' % (wiki))
        continue
    
    name = u''
    name = re.findall(ur"<title>([^<]+)</title>", raw)[0]
    logo = u'[[Image:NoLogo.png]]'
    if re.search(ur'<div id="p-logo"><a style="background-image: url\((/w/skins/[^\)]+)\);', raw):
        logo = u"%s%s" % (wiki, re.findall(ur'<div id="p-logo"><a style="background-image: url\((/w/skins/[^\)]+)\);', raw)[0])
    url = wiki
    rc = u'%s/wiki/Special:RecentChanges' % (wiki)
    stats = u'%s/wiki/Special:Statistics' % (wiki)
    language = langs[re.findall(ur"<html lang=\"([^\"]+)\" ", raw)[0]]
    engine = u'MediaWiki'
    lic = u''
    pagenum = ''
    try:
        raw2 = unicode(urllib.urlopen(stats).read(), 'utf-8')
        pagenum = str(re.sub(ur'[\,\.]', '', re.findall(ur'<tr class="mw-statistics-articles"><td>[^<]+</td><td class="mw-statistics-numbers">([^<]+)</td>', raw2)[0]))
    except:
        pass
    
    output = u"""{{Wiki
|name              = %s
|logo              = %s
|URL               = %s
|recentchanges URL = %s
|wikinode URL      = No
|status            = 
|language          = %s
|editmode          = 
|engine            = %s
|license           = %s
|maintopic         = 
|backupurl         = 
|backupdate        = 
}}
{{Size
|pages = %s <!--Necessary. Type the plain number of pages - NO thousands separators.-->
|statistics URL = %s <!--Preferred, source of page count (often a 'Statistics' page). If unknown leave void.-->
|wikiFactor = <!--Optional. If unknown leave void. See: Category:wikiFactor.-->
|wikiFactor URL = <!--Preferred, source of wikiFactor (often 'PopularPages' or 'MostVisitedPages'). If unknown leave void.-->
}}(As of: 5 April 2012)<!--manually add or amend date when stats are verified and/or updated-->

==Description==
{{add}}

[[Category:FoundedIn20xx]]
""" % (name, logo, url, rc, language, engine, lic, pagenum, stats)
    
    p = wikipedia.Page(s, name)
    if not p.exists():
        wikipedia.showDiff(u'', output)
        p.put(output, u'BOT - Creating page for "%s": %s' % (name, url))
        log = wikipedia.Page(s, u'User:Emijrp/Log')
        log.put(u'%s\n* [[%s]] (%s) has been created' % (log.get(), name, url), u'BOT - Adding %s' % (url))
    else:
        log = wikipedia.Page(s, u'User:Emijrp/Log')
        log.put(u'%s\n* [[%s]] (%s) exists' % (log.get(), p.get(), url), u'BOT - Adding %s' % (url))
