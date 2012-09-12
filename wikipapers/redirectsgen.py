#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011-2012 emijrp
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
import sys

import wikipedia
import pagegenerators
import unicodedata

def removeaccute(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def remove1(s): #replace with no-space
    s = re.sub(ur"[\.\:\;\,\"\!\¡\«\»]", ur"", s)
    return s

def remove2(s): #replace with a single space
    s = re.sub(ur"[\-\–]", ur" ", s)
    return s

def unquote(s):
    s = re.sub(ur"&#34;", ur'"', s)
    return s

def main():
    skip = u''
    if len(sys.argv) > 1:
        site = wikipedia.Site(sys.argv[1], sys.argv[1])
    else:
        print 'python script.py wikifamily [skiptopage]'
        sys.exit()
    if len(sys.argv) > 2:
        skip = sys.argv[2]
    gen = pagegenerators.AllpagesPageGenerator(start=skip, namespace=0, site=site)
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=250)
    alltitles = []
    for page in pre:
        if not page.exists() or page.isRedirectPage():
            continue
        alltitles.append(page.title())
        print page.title()
        
    for wtitle in alltitles:
        if len(wtitle) > 1:
            wtitle_ = wtitle[0]+wtitle[1:].lower()
            redirects = set()
            for t in [wtitle, wtitle_]:
                redirects.add(t)
                redirects.add(remove1(t))
                redirects.add(remove2(t))
                redirects.add(removeaccute(t))
                redirects.add(remove1(remove2(t)))
                redirects.add(remove1(removeaccute(t)))
                redirects.add(remove2(removeaccute(t)))
                redirects.add(remove1(remove2(removeaccute(t))))
            
            print redirects
            for redirect in redirects:
                redirect = redirect.strip()
                if redirect and redirect != wtitle and not redirect in alltitles:
                    red = wikipedia.Page(site, redirect)
                    if not red.exists():
                        output = u"#REDIRECT [[%s]]" % (wtitle)
                        msg = u"BOT - Creating redirect to [[%s]]" % (wtitle)
                        red.put(output, msg)

if __name__ == '__main__':
    main()
