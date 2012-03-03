#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import urllib

import wikipedia

site = wikipedia.Site('todogratix', 'todogratix')
f = open('booksall.spa', 'r')
books = f.read().splitlines()
f.close()

skip = u'/b/OL14006205M'
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
            #create authors
            if data2.has_key('birth_date') and data2.has_key('death_date'):
                data2['birth_date'] = data2['birth_date'].strip().strip('.')
                data2['death_date'] = data2['death_date'].strip().strip('.')
                if re.search(ur"(?im)^\d{4}$", data2['birth_date']) and re.search(ur"(?im)^\d{4}$", data2['death_date']):
                    authorpage = wikipedia.Page(site, data2['name'])
                    if not authorpage.exists():
                        wauthorpage = wikipedia.Page(wikipedia.Site('es', 'wikipedia'), data2['name'])
                        while wauthorpage.exists() and wauthorpage.isRedirectPage():
                            wauthorpage = wauthorpage.getRedirectTarget()
                        if wikipedia.Page(site, wauthorpage.title()).exists():
                            red = u"#REDIRECT [[%s]]" % (wauthorpage.title())
                            authorpage.put(red, red)
                            continue
                        ocupacion = []
                        nacionalidad = '' #no siempre la nacionalidad indicada es donde se nace, pero...
                        if wauthorpage.exists():
                            if re.search(ur"(?im)Nacidos en %s" % (data2['birth_date']), wauthorpage.get()) and re.search(ur"(?im)Fallecidos en %s" % (data2['death_date']), wauthorpage.get()):
                                if re.search(ur"(?im)\:\s*Escritores (de|en)", wauthorpage.get()):
                                    ocupacion.append('escritor')
                                if re.search(ur"(?im)\:\s*Juristas (de|en)", wauthorpage.get()):
                                    ocupacion.append('jurista')
                                if re.search(ur"(?im)\:\s*Abogados (de|en)", wauthorpage.get()):
                                    ocupacion.append('abogado')
                                if re.search(ur"(?im)\:\s*Dramaturgos (de|en)", wauthorpage.get()):
                                    ocupacion.append('dramaturgo')
                                if re.search(ur"(?im)\:\s*Poetas (de|en)", wauthorpage.get()):
                                    ocupacion.append('poeta')
                                if re.search(ur"(?im)\:\s*Bibliógrafos (de|en)", wauthorpage.get()):
                                    ocupacion.append(u'bibliógrafo')
                                if re.search(ur"(?im)\:\s*Filósofos (de|en)", wauthorpage.get()):
                                    ocupacion.append(u'filósofo')
                                if re.search(ur"(?im)\:\s*Matemáticos (de|en)", wauthorpage.get()):
                                    ocupacion.append(u'matemático')
                                if re.search(ur"(?im)\:\s*Teólogos (de|en)", wauthorpage.get()):
                                    ocupacion.append(u'teólogo')
                                if re.search(ur"(?im)\:\s*Historiadores (de|en)", wauthorpage.get()):
                                    ocupacion.append('historiador')
                                if re.search(ur"(?im)\:\s*Políticos (de|en)", wauthorpage.get()):
                                    ocupacion.append(u'político')
                                if re.search(ur"(?im)\:\s*Filólogos (de|en)", wauthorpage.get()):
                                    ocupacion.append(u'filólogo')
                                m = re.findall(ur"(?im)(?:Escritores|Juristas|Abogados|Dramaturgos|Poetas|Filósofos|Bibliógrafos|Matemáticos|Teólogos|Historiadores|Políticos|Filólogos) (?:de|en) (Alemania|Austria|Chile|Colombia|Cuba|Ecuador|El Salvador|España|Estados Unidos|Finlandia|Francia|Grecia|Guatemala|Honduras|India|Italia|Nicaragua|Paraguay|Perú|Polonia|Portugal|Puerto Rico|Rumanía|Rusia|Suecia|Suiza)", wauthorpage.get())
                                if m:
                                    sett = set(m)
                                    if len(sett) == 1:
                                        nacionalidad = sett.pop()
                        else:
                            pass #no tenemos datos de ocupación ni nacionalidad...
                        output = u"""{{Infobox Persona
|nombre=%s
|apellidos=%s
|imagen=
|fechanacimiento=%s
|lugarnacimiento=%s
|fechafallecimiento=%s
|lugarfallecimiento=
|ocupación=%s
}}

{{obras por autor}}%s""" % (data2['name'].split(' ')[0], u' '.join(data2['name'].split(' ')[1:]), data2['birth_date'], nacionalidad, data2['death_date'], u', '.join(ocupacion), wauthorpage.exists() and u'\n\n== Enlaces externos ==\n* {{w|es|%s}}' % (wauthorpage.title()) or '')
                        print output
                        authorpage.put(output, output)
                    
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

