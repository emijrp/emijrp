#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

import wikipedia
import pagegenerators
import unicodedata

def removeaccute(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def remove1(s):
    s = re.sub(ur"[\.\:\;\,\"\!\¡\«\»]", ur"", s)
    return s

def remove2(s):
    s = re.sub(ur"[\-\–]", ur" ", s)
    return s

def unquote(s):
    s = re.sub(ur"&#34;", ur'"', s)
    return s

skip = sys.argv[2]
site = ''
site = wikipedia.Site(sys.argv[1], sys.argv[1])
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
