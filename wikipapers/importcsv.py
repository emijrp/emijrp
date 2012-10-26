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

import csv
import re
import sys
import wikipedia

import redirectsgen

s = wikipedia.Site('wikipapers', 'wikipapers')

#Authors,Title,Year,Source title,Volume,Issue,Art. No.,Page start,Page end,Page count,Link,Document Type,Source
f = csv.reader(open(sys.argv[1], 'rb'), delimiter=',', quotechar='"')
for row in f:
    row = [unicode(r, 'utf-8') for r in row]
    title = row[1]
    print '-'*50, '\n', title, '\n', '-'*50
    if row[11] == u'Conference Paper':
        print title
    
    if not ' ' in row[1] or len(row[1]) < 10:
        continue
    
    output = u"""{{Infobox Publication
|type=%s
|title=%s""" % (u'conference paper', row[1])
    if row[2]:
        output += u'\n|date=%s' % (row[2])
    if row[3]:
        if u'wikisym' in row[3].lower():
            output += u'\n|publishedin=WikiSym'
        else:
            output += u'\n|publishedin=%s' % (row[3])
    if row[4]:
        output += u'\n|volume=%s' % (row[4])
    if row[5]:
        output += u'\n|issue=%s' % (row[5])
    if row[7] and row[8]:
        output += u'\n|pages=%s-%s' % (row[7], row[8])
    output += u'\n|language=English'
    output += u'\n}}\n\n{{talk}}'
    
    #continue
    #try:
    #check if exists
    page1 = wikipedia.Page(s, title)
    page2 = wikipedia.Page(s, title.lower())
    page3 = wikipedia.Page(s, redirectsgen.remove1(redirectsgen.remove2(redirectsgen.removeaccute(title))))
    if page1.exists() or page2.exists() or page3.exists():
        print 'Exists >', title
        continue #skip
    #create page
    print '\n', '#'*50, '\n', output, '\n', '#'*50
    page1.put(output, output)
    
    #create redirect
    redoutput = u"#redirect [[%s]]" % (title)
    if not page2.exists():
        page2.put(redoutput, redoutput)
    if not page3.exists():
        page3.put(redoutput, redoutput)
    
    #create talkpage
    talkoutput = u"<noinclude>{{talk}}</noinclude>"
    talk = page1.toggleTalkPage()
    if not talk.exists():
        talk.put(talkoutput, talkoutput)
    """except:
        print 'Skiping, possible char error'
        pass"""
        
