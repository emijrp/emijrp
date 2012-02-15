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

"""
<meta property="dc:title" content="Understanding learning: the Wiki way" />
<meta property="dc:creator" content="Joachim Kimmerle" />
<meta property="dc:creator" content="Johannes Moskaliuk" />
<meta property="dc:creator" content="Ulrike Cress" />
<meta property="dc:identifier" content="10.1145/1641309.1641315" />
<meta property="dc:source" content="In Proceedings of the 5th International Symposium on Wikis and Open Collaboration (2009)" />
<meta property="dc:date" content="2011-04-20T10:28:03-00:00" />
<meta property="prism:publicationYear" content="2009" />
<meta property="prism:publisher" content="ACM" />
<meta property="prism:category" content="co-evolution" />
<meta property="prism:category" content="collective_knowledge" />
<meta property="prism:category" content="knowledge_building" />
<meta property="prism:category" content="wiki" />
"""

"""
<input type="hidden" name="abstract" value="Learning &#34;the wiki way&#34;, learning through wikis is a form of self-regulated learning that is independent of formal learning settings and takes place in a community of knowledge. Such a community may work jointly on a digital artifact to create new, innovative and emergent knowledge. We regard wikis as a prototype of tools for community-based learning, and point out five relevant features. We will present the co-evolution model, as introduced by Cress and Kimmerle [3][4], that may be understood as a framework to describe learning in the wiki way. This model describes collaborative knowledge building as a co-evolution between cognitive and social systems. To investigate learning the wiki way, we have to consider both individual processes and processes within the wiki, which represent the processes that are going on within a community. This paper presents three empirical studies that investigate learning the wiki way in a laboratory setting. We take a look at participants' contributions to a wiki indicating processes within the wiki community, and measure the extent of individual learning at the end of the experiment. Our conclusion is that the model of co-evolution has a strong impact on understanding learning the wiki way, may be helpful to designers of learning environments, and serve as framework for further research."/>
"""

def removeaccute(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def removedots(s):
    s = re.sub(ur"[\.\:\;]", ur"", s)
    return s

def unquote(s):
    s = re.sub(ur"&#34;", ur'"', s)
    return s

skip = u''
for page in range(1,3):
    headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.106 Chrome/15.0.874.106 Safari/535.2' }
    #url = 'http://www.citeulike.org/search/all/page/%d?q=title%%3awiki+or+title%%3awikipedia' % (page)
    url = 'http://www.citeulike.org/search/all/page/%d?q=title%%3awiktionary+or+title%%3awikiversity' % (page)
    #req = urllib2.Request(url, '', headers)
    #raw = unicode(urllib2.urlopen(req).read(), 'utf-8')
    raw = unicode(urllib.urlopen(url).read(), 'utf-8')
    #print raw

    m = re.findall('/article/(\d+)', raw)
    m = set(m)

    print m

    for id in m:
        print "--> Page", page, "CiteULike ID", id
        
        if skip:
            if id != skip: #dic['dc:title'] != skip:
                print "Skiping until...", skip
                continue
            else:
                skip = ''
        
        url2 = 'http://www.citeulike.org/article/' + id
        #req2 = urllib2.Request(url2, '', headers)
        #raw2 = unicode(urllib2.urlopen(req2).read(), 'utf-8')
        raw2 = unicode(urllib.urlopen(url2).read(), 'utf-8')
        meta = re.findall('<meta property="([^=]*?)" content="([^>]*?)" />', raw2)
        dic = {}
        for k, v in meta:
            if k == 'dc:creator':
                if dic.has_key(k):
                    dic[k].append(v)
                else:
                    dic[k] = [v]
            else:
                dic[k] = v
        
        if dic.has_key('dc:title') and len(dic['dc:title'])>=20 and \
           dic.has_key('dc:creator') and \
           dic.has_key('dc:identifier') and \
           dic.has_key('dc:source') and \
           dic.has_key('prism:publicationYear'):     
            
            dic['dc:title'] = re.sub(ur"(?im)\s*\.*\s*$", ur"", dic['dc:title'].strip())
            if not re.search(ur"(?im)(wiki|wiktion)", dic['dc:title']): #wikipedia #wiktionary #wikiversity
                continue
            if re.search(ur'[\;\&\#\{\(\)\$\\]', dic['dc:title']+''.join(dic['dc:creator'])):
                continue
            
            dic['dc:title'] = re.sub(ur"(?im)wikipedia", ur"Wikipedia", dic['dc:title'])
            dic['dc:title'] = re.sub(ur"(?im)wikiversity", ur"Wikiversity", dic['dc:title'])
            dic['dc:title'] = re.sub(ur"(?im)wiktionary", ur"Wiktionary", dic['dc:title'])
            
            print dic.items()
            publishedin = u''
            if re.search(ur"(?im)(international symposium on Wikis|wikisym)", dic['dc:source']):
                publishedin = u'WikiSym'
            elif re.search(ur"(?im)(wikiman[ií]a)", dic['dc:source']):
                publishedin = u'Wikimania'
            elif re.search(ur"(?im)(wikipedia academy)", dic['dc:source']):
                publishedin = u'Wikipedia Academy'
            elif re.search(ur"(?im)(wikiviz)", dic['dc:source']):
                publishedin = u'WikiViz'
            elif re.search(ur"(?im)(semwiki)", dic['dc:source']):
                publishedin = u'SemWiki'
            elif re.search(ur"(?im)(mathwikis)", dic['dc:source']):
                publishedin = u'MathWikis'
            elif re.search(ur"(?im)(clef)", dic['dc:source']):
                publishedin = u'CLEF'
            elif re.search(ur"(?im)(wikiai)", dic['dc:source']):
                publishedin = u'WikiAI'
            
            if not publishedin and dic.has_key('prism:publicationName') and not re.search(ur'[\;\&\#\{\\]', dic['prism:publicationName']):
                publishedin = dic['prism:publicationName']
            
            type_ = u'unknown'
            if publishedin in ['WikiSym', 'Wikimania', 'WikiViz', 'SemWiki', 'MathWikis', 'CLEF', 'WikiAI']:
                type_ = u'conference paper'
            
            output = u"""{{Infobox Publication
|type=%s
|title=%s
|authors=%s
|publishedin=%s
|year=%s
|keywords=
|doi=%s
|citeulike=%s""" % (type_, dic['dc:title'], u', '.join(dic['dc:creator']), publishedin, dic['prism:publicationYear'], dic['dc:identifier'], id)
            
            if dic.has_key('prism:isbn'):
                output += u'\n|isbn=%s' % (dic['prism:isbn'])
            elif dic.has_key('prism:issn'):
                output += u'\n|issn=%s' % (dic['prism:issn'])
            
            if dic.has_key('prism:volume'):
                output += u'\n|volume=%s' % (dic['prism:volume'])
            if dic.has_key('prism:number'):
                output += u'\n|issue=%s' % (dic['prism:number'])
            
            output += u'\n|language=English'
            
            if dic.has_key('prism:startingPage') and dic.has_key('prism:endingPage'):
                if dic['prism:startingPage'] != dic['prism:endingPage']:
                    output += u'\n|pages=%s-%s' % (dic['prism:startingPage'], dic['prism:endingPage'])
                else:
                    output += u'\n|pages=%s' % (dic['prism:startingPage'])
            
            url3 = u"http://scholar.google.es/scholar?q=%s" % (re.sub(' ', '+', dic['dc:title']))
            req3 = urllib2.Request(url3, '', headers)
            try:
                raw3 = unicode(urllib2.urlopen(req3).read(), 'utf-8')
            except:
                continue
            #print raw3
            #<b>Improving science education </b>and <b>understanding through editing Wikipedia</b></a></h3><div class="gs_ggs gs_fl"><a href="http://www-personal.umich.edu/~bcoppola/publications/68.JCEWiki.pdf" onmousedown=
            pdf = re.findall(ur"""(?im)%s[^<]*</a></h3><div[^<]+<a *href=\"([^ ]*?\.pdf)\" *onmousedown=[^>]*>[^<]*<span[^>]*>[^<]*</span>[^<]*(?:</a>)?[^<]*</div>[^<]*<div class=[^>]*>[^<]*%s[^<]*</div>""" % (dic['dc:title'], dic['prism:publicationYear']), re.sub(ur"(?im)(</?b>)", ur"", raw3))
            if pdf:
                print pdf
                pdf = pdf[0]
                pdf = re.sub(ur"&amp;", ur"&", pdf)
                output += u'\n|remotemirror=%s' % (pdf)
            
            abstract = re.findall(ur"""<input type="hidden" name="abstract" value="([^>]*?)"/>""", raw2)
            if abstract and len(abstract[0]) > 100:
                output += u'\n|abstract=%s' % (unquote(abstract[0].strip()))
            else:
                output += u'\n|abstract='
            output += u'\n}}\n\n{{talk}}'
            print '\n', '#'*50, '\n', output, '\n', '#'*50
            
            try: #a veces falla, ej: "Wikipedia: blabla" se cree que estás llamando al family wikipedia
                p = wikipedia.Page(wikipedia.Site('wikipapers', 'wikipapers'), dic['dc:title'])
            except:
                continue
            
            if not p.exists():
                p.put(output, output)
            else:
                continue
            t = wikipedia.Page(wikipedia.Site('wikipapers', 'wikipapers'), u"Talk:%s" % dic['dc:title'])
            if not t.exists():
                t.put(u"{{talk}}", u"{{talk}}")
            
            redirects = [
                dic['dc:title'][0]+dic['dc:title'][1:].lower(),
                removeaccute(dic['dc:title']),
                removeaccute(dic['dc:title'][0]+dic['dc:title'][1:].lower()),
                removedots(dic['dc:title']),
                removedots(dic['dc:title'][0]+dic['dc:title'][1:].lower()),
                ]
            
            redirects = set(redirects)
            for r in redirects:
                if r != dic['dc:title']:
                    print r
                    red = u"#redirect [[%s]]" % (dic['dc:title'])
                    pr = wikipedia.Page(wikipedia.Site('wikipapers', 'wikipapers'), r)
                    if not pr.exists():
                        pr.put(red, red)

