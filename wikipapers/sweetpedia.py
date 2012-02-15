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
import urllib2
import unicodedata
from urllib import FancyURLopener
from random import choice

import wikipedia

def removeaccute(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def removedots(s):
    s = re.sub(ur"[\.\:\;]", ur"", s)
    return s

def unquote(s):
    s = re.sub(ur"&#34;", ur'"', s)
    return s

skip = u'Decoding Wikipedia Categories for Knowledge Acquisition'
f = open('sweetpedia.txt')
raw = unicode(f.read(), 'utf-8')
m = re.compile(ur"""(?im)(?:\.?\[new\] )?(?P<authors>[^\d\n]+)(?P<year>\d+)\. *(?P<title>[^\n\.\;\,]*?) *(?:, (?:in|at) *(?P<event>.*?))? *[\.\,\;] *see[^\n]*[^a-z](?P<url>[a-z]{3,5}://[^ \n]*pdf) *\. *\n""").finditer(raw)
for i in m:
    authors = []
    for author in re.sub(' and ', ',', i.group("authors")).strip().split(','):
        author = author.strip()
        if len(author) >= 5:
            authors.append(author)
    year = i.group("year")
    title = i.group("title")
    event = i.group("event")
    url = i.group("url")
    
    if skip:
        if title != skip:
            continue
        else:
            skip = ''
    
    if title and len(title)>=20 and authors and year and url:
        title = re.sub(ur"(?im)\s*\.*\s*$", ur"", title.strip())
        #if not re.search(ur"(?im)(wiki|wiktion)", dic['dc:title']): #wikipedia #wiktionary #wikiversity
        #    continue
        if re.search(ur'[\;\&\#\{\(\)\$\\]', title+''.join(authors)):
            continue
        
        title = re.sub(ur"(?im)wikipedia", ur"Wikipedia", title)
        title = re.sub(ur"(?im)wikiversity", ur"Wikiversity", title)
        title = re.sub(ur"(?im)wiktionary", ur"Wiktionary", title)
        
        publishedin = u''
        if event:
            if re.search(ur"(?im)(international symposium on Wikis|wikisym)", event):
                publishedin = u'WikiSym'
            elif re.search(ur"(?im)(wikiman[ií]a)", event):
                publishedin = u'Wikimania'
            elif re.search(ur"(?im)(wikipedia academy)", event):
                publishedin = u'Wikipedia Academy'
            elif re.search(ur"(?im)(wikiviz)", event):
                publishedin = u'WikiViz'
            elif re.search(ur"(?im)(semwiki)", event):
                publishedin = u'SemWiki'
            elif re.search(ur"(?im)(mathwikis)", event):
                publishedin = u'MathWikis'
            elif re.search(ur"(?im)(clef)", event):
                publishedin = u'CLEF'
            elif re.search(ur"(?im)(wikiai)", event):
                publishedin = u'WikiAI'
        
        type_ = u'unknown'
        if publishedin in ['WikiSym', 'Wikimania', 'WikiViz', 'SemWiki', 'MathWikis', 'CLEF', 'WikiAI']:
            type_ = u'conference paper'
        
        output = u"""{{Infobox Publication
|type=%s
|title=%s
|authors=%s
|publishedin=%s""" % (type_, title, u', '.join(authors), publishedin)
        
        if year:
            output += u'\n|year=%s' % (year)
        
        output += u'\n|language=English'
        if url:
            output += u'\n|remotemirror=%s' % (url)
        
        output += u'\n|abstract='
        output += u'\n}}\n\n{{talk}}'
        print '\n', '#'*50, '\n', output, '\n', '#'*50
        
        if raw_input("Create this page [Y, Yes]? ") in ['Y', 'y', 'yes']:
            try: #a veces falla, ej: "Wikipedia: blabla" se cree que estás llamando al family wikipedia
                p = wikipedia.Page(wikipedia.Site('wikipapers', 'wikipapers'), title)
            except:
                continue
            
            if not p.exists():
                p.put(output, output)
            else:
                continue
            t = wikipedia.Page(wikipedia.Site('wikipapers', 'wikipapers'), u"Talk:%s" % title)
            if not t.exists():
                t.put(u"{{talk}}", u"{{talk}}")
            
            redirects = [
                title[0]+title[1:].lower(),
                removeaccute(title),
                removeaccute(title[0]+title[1:].lower()),
                removedots(title),
                removedots(title[0]+title[1:].lower()),
                ]
            
            redirects = set(redirects)
            for r in redirects:
                if r != title:
                    print r
                    red = u"#redirect [[%s]]" % (title)
                    pr = wikipedia.Page(wikipedia.Site('wikipapers', 'wikipapers'), r)
                    if not pr.exists():
                        pr.put(red, red)

