#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import urllib

import wikipedia

site = wikipedia.Site('todogratix', 'todogratix')
f = open('books.spa', 'r')
books = f.read().splitlines()
f.close()

skip = u'/b/OL22886366M'
for book in books:
    print book
    if skip:
        if book == skip:
            skip = ''
        else:
            continue
    
    query = 'http://openlibrary.org%s.json' % (book)
    json_data = urllib.urlopen(query)
    data = json.load(json_data)
    #print data.keys()
    if not data.has_key('title') or not data.has_key('languages') or not data.has_key('authors') or not data.has_key('publish_date') or not data.has_key('ocaid'):
        continue
    
    title = data['title'].strip('.')
    if len(title)>160:
        continue
    subtitle = ''
    if data.has_key('subtitle'): #not mandatory
        subtitle = data['subtitle']
    language = ''
    for lang in data['languages']:
        if lang['key'] == '/languages/spa':
            language = u'Español'
    authors = []
    for author in data['authors']:
        query2 = 'http://openlibrary.org%s.json' % (author['key'])
        json_data2 = urllib.urlopen(query2)
        data2 = json.load(json_data2)
        if data2.has_key('name'):
            authors.append(data2['name'])
        else: #break
            authors = []
            break
    if not authors:
        continue
    publish_date = data['publish_date']
    ocaid = data['ocaid']
    
    output = u"""{{Infobox Obra
|tipo=libro
|título=%s
|subtítulo=%s
|imagen=
|autor=%s
|género=
|fechadepublicación=%s
|idioma=%s
|olid=%s
}}

{{Internet Archive book|id=%s}}
""" % (title, subtitle, ', '.join([author.strip('.') for author in authors]), publish_date, language, book.split('/')[2], ocaid)
    
    if re.search(ur"[\[\]]", title+subtitle+', '.join(authors)):
        continue
    
    try: #sometimes date is January XXXX, so break
        if int(publish_date) >= 1900:
            continue
    except:
        continue
    
    if re.search(ur",", ''.join(authors)):
        continue
    
    page = wikipedia.Page(site, title)
    if not page.exists():
        print output
        page.put(output, u"BOT - Importando desde [[Open Library]] http://openlibrary.org%s" % (book))

