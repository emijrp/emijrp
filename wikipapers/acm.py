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

import os
import re
import sys
import time
import urllib

import wikipedia

class MyOpener(urllib.FancyURLopener, object):
    version = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0'

def convert(t):
    t = re.sub(ur"(?im)\\\"\{([^\}]+?)\}", ur"\1", t)
    t = re.sub(ur"\{\\'(.)\}", ur"\1", t)
    return t

"""
@article{Park:2012:FII:2148241.2148347,
 author = {Park, Namkee and Oh, Hyun Sook and Kang, Naewon},
 title = {Factors influencing intention to upload content on Wikipedia in South Korea: The effects of social norms and individual differences},
 journal = {Comput. Hum. Behav.},
 issue_date = {May, 2012},
 volume = {28},
 number = {3},
 month = may,
 year = {2012},
 issn = {0747-5632},
 pages = {898--905},
 numpages = {8},
 url = {http://dx.doi.org/10.1016/j.chb.2011.12.010},
 doi = {10.1016/j.chb.2011.12.010},
 acmid = {2148347},
 publisher = {Elsevier Science Publishers B. V.},
 address = {Amsterdam, The Netherlands, The Netherlands},
 keywords = {Descriptive norms, Ego involvement, Injunctive norms, Issue involvement, Self-efficacy, Wikipedia},
} 
"""

s = wikipedia.Site('wikipapers', 'wikipapers')
url = "http://dl.acm.org/results.cfm?query=%28Title%3Awikipedia%29&querydisp=%28Title%3Awikipedia%29&srt=meta_published_date%20dsc&short=0&coll=DL&dl=GUIDE&source_disp=&source_query=&since_month=&since_year=&before_month=&before_year=&termshow=matchboolean&range_query=&zadv=1"

for i in range(30):
    time.sleep(0.1)
    myopener = MyOpener()
    myopener.retrieve(url+'&start='+str(i*20+1), 'acm.html')
    raw = open('acm.html').read()
    os.remove('acm.html')
    ids = re.findall(ur"citation\.cfm\?id=([^&]+?)&", raw)
    #print raw
    
    for id in ids:
        print i, id
        try:
            id = id.split('.')[1]
        except:
            print 'No paper?'
            continue
        time.sleep(0.1)
        #print id
        myopener.retrieve("https://dl.acm.org/exportformats.cfm?id=%s&expformat=bibtex" % (id), 'ref.html')
        bibtex = open('ref.html').read()
        os.remove('ref.html')
        
        #get params
        #print bibtex
        try:
            title = convert(re.findall(ur"(?im) title = {([^\n]+?)}", bibtex)[0]) # space before title, to avoi to get booktitle
            if re.search(ur"\\", title):# \\#  \\
                continue
            authors = re.findall(ur"(?im) author = {([^\n]+?)}", bibtex)[0].split(' and ')
            authors = [convert('%s %s' % (author.split(', ')[1], author.split(', ')[0])) for author in authors]
            year = re.findall(ur"(?im) year = {([^\n]+?)}", bibtex)[0]
            try:
                journal = convert(re.findall(ur"(?im) journal = {([^\n]+?)}", bibtex)[0])
            except:
                journal = ''
            try:
                conference = convert(re.findall(ur"(?im) series = {([^\n]+?)\s*\'\d+}", bibtex)[0])
            except:
                conference = ''
            try:
                volume = re.findall(ur"(?im) volume = {([^\n]+?)}", bibtex)[0]
            except:
                volume = ''
            try:
                number = re.findall(ur"(?im) number = {([^\n]+?)}", bibtex)[0]
            except:
                number = ''
            try:
                issn = re.findall(ur"(?im) issn = {([^\n]+?)}", bibtex)[0]
            except:
                issn = ''
            try:
                isbn = re.findall(ur"(?im) isbn = {([^\n]+?)}", bibtex)[0]
            except:
                isbn = ''
            try:
                pages = re.sub('--', '-', re.findall(ur"(?im) pages = {([^\n]+?)}", bibtex)[0])
            except:
                pages = ''
            try:
                doi = re.findall(ur"(?im) doi = {([^\n]+?)}", bibtex)[0]
            except:
                doi = ''
            try:
                keywords = [convert(keyword) for keyword in re.findall(ur"(?im) keywords = {([^\n]+?)}", bibtex)[0].split(', ')]
            except:
                keywords = []
            
            remotemirror = ''
            type_ = journal and 'journal article' or 'conference paper'
            publishedin = journal and journal or conference
        except:
            continue
        #end get params
        
        #filter
        if not 'wiki' in title.lower():
            continue
        
        output = u"""{{Infobox Publication
|type=%s
|title=%s
|authors=%s
|publishedin=%s
|keywords=%s""" % (type_, title, u', '.join(authors), publishedin, ', '.join(keywords))
        
        if year:
            output += u'\n|date=%s' % (year)
        if volume:
            output += u'\n|volume=%s' % (volume)
        if number:
            output += u'\n|issue=%s' % (number)
        if pages:
            output += u'\n|pages=%s' % (pages)
        
        if issn:
            output += u'\n|issn=%s' % (issn)
        elif isbn:
            output += u'\n|isbn=%s' % (isbn)
        if doi:
            output += u'\n|doi=%s' % (doi)
        
        output += u'\n|language=English'
        if remotemirror:
            output += u'\n|remotemirror=%s' % (remotemirror)
        
        output += u'\n|abstract='
        output += u'\n}}\n\n{{talk}}'
        
        try:
            #check if exists
            page1 = wikipedia.Page(s, title)
            page2 = wikipedia.Page(s, title.lower())
            if page1.exists() or page2.exists():
                print 'Exists >', title
                continue #skip
            #create page
            print '\n', '#'*50, '\n', output, '\n', '#'*50
            page1.put(output, output)
            
            #create redirect
            redoutput = u"#redirect [[%s]]" % (title)
            if not page2.exists():
                page2.put(redoutput, redoutput)
            
            #create talkpage
            talkoutput = u"<noinclude>{{talk}}</noinclude>"
            talk = page1.toggleTalkPage()
            if not talk.exists():
                talk.put(talkoutput, talkoutput)
        except:
            print 'Skiping, possible char error'
            pass

