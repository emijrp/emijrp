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

import wikipedia
import pagegenerators
import unicodedata

def removeaccute(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def remove1(s):
    s = re.sub(ur"[\.\:\;\,]", ur"", s)
    return s

def remove2(s):
    s = re.sub(ur"[\-\–]", ur" ", s)
    return s

def unquote(s):
    s = re.sub(ur"&#34;", ur'"', s)
    return s

skip = u''
site = wikipedia.Site('wikipapers', 'wikipapers')
gen = pagegenerators.AllpagesPageGenerator(start = skip, namespace=0, site=site)
pre = pagegenerators.PreloadingGenerator(gen)
for page in pre:
    if not page.exists():
        continue
    wtitle = page.title()
    
    print wtitle
    if page.isRedirectPage():
        tar = page.getRedirectTarget()
        if tar.exists():
            target = tar.title()
        else:
            continue
    else:
        target = wtitle
    
    if len(wtitle) > 1:
        wtitle_ = wtitle[0]+wtitle[1:].lower()
        redirects = set()
        redirects.add(wtitle)
        redirects.add(remove1(wtitle))
        redirects.add(remove2(wtitle))
        redirects.add(removeaccute(wtitle))
        redirects.add(remove1(remove2(wtitle)))
        redirects.add(remove1(removeaccute(wtitle)))
        redirects.add(remove2(removeaccute(wtitle)))
        redirects.add(remove1(remove2(removeaccute(wtitle))))
        redirects.add(wtitle_)
        redirects.add(remove1(wtitle_))
        redirects.add(remove2(wtitle_))
        redirects.add(removeaccute(wtitle_))
        redirects.add(remove1(remove2(wtitle_)))
        redirects.add(remove1(removeaccute(wtitle_)))
        redirects.add(remove2(removeaccute(wtitle_)))
        redirects.add(remove1(remove2(removeaccute(wtitle_))))
        
        print redirects
        for redirect in redirects:
            redirect = redirect.strip()
            if redirect and redirect != wtitle:
                red = wikipedia.Page(site, redirect)
                if not red.exists():
                    output = u"#REDIRECT [[%s]]" % (target)
                    red.put(output, output)
