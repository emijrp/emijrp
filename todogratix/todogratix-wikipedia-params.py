#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import catlib
import pagegenerators
import wikipedia

site = wikipedia.Site('todogratix', 'todogratix')
category = catlib.Category(title=u"Category:Personas", site=site)
gen = pagegenerators.CategorizedPageGenerator(category, recurse=False, start='!')
pre = pagegenerators.PreloadingGenerator(gen)

for page in pre:
    print page.title()
    output = page.get()
    m = re.findall(ur"(?im)\{\{\s*(?:w|wikipedia)\s*\|(?:\s*[a-z]{2,3}\s*\|)?([^\}]+)\}\}", page.get())
    if m:
        print m[0]
        wpage = wikipedia.Page(wikipedia.Site('es', 'wikipedia'), m[0])
        if wpage.exists():
            while wpage.isRedirectPage():
                wpage = wpage.getRedirectTarget()
            
            params = []
            
            fechafallecimiento = ''
            if not re.search(ur"(?im)fechafallecimiento\s*=", page.get()):
                print 'Sin fecha fallecimiento'
                n = re.findall(ur"(?im)(?:\[\[\s*Categor(?:y|ía)\s*:Fallecidos en (\d+)\s*[\|\]]|\{\{\s*(?:BD|NF)\s*\|[^\|]+\|\s*(\d+)\s*[\|\}])", wpage.get())
                if n:
                    if n[0][0]:
                        fechafallecimiento = n[0][0]
                    elif n[0][1]:
                        fechafallecimiento = n[0][1]
            if fechafallecimiento:
                output = re.sub(ur"\{\{Infobox Persona", ur"{{Infobox Persona\n|fechafallecimiento=%s" % (fechafallecimiento), output)
                params.append(['fechafallecimiento', fechafallecimiento])
            
            fechanacimiento = ''
            if not re.search(ur"(?im)fechanacimiento\s*=", page.get()):
                print 'Sin fecha nacimiento'
                n = re.findall(ur"(?im)(?:\[\[\s*Categor(?:y|ía)\s*:Nacidos en (\d+)\s*[\|\]]|\{\{\s*(?:BD|NF)\s*\|\s*(\d+)\s*[\|\}])", wpage.get())
                if n:
                    if n[0][0]:
                        fechanacimiento = n[0][0]
                    elif n[0][1]:
                        fechanacimiento = n[0][1]
            if fechanacimiento:
                output = re.sub(ur"\{\{Infobox Persona", ur"{{Infobox Persona\n|fechanacimiento=%s" % (fechanacimiento), output)
                params.append(['fechanacimiento', fechanacimiento])
            
            imagen = ''
            if not re.search(ur"(?im)imagen\s*=", page.get()):
                print 'Sin imagen'
                n = re.findall(ur"(?im)imagen\s*=\s*([^=\n\r\|]+\.jpe?g)", wpage.get())
                if n:
                    imagen = n[0]
            if imagen:
                output = re.sub(ur"\{\{Infobox Persona", ur"{{Infobox Persona\n|imagen=%s" % (imagen), output)
                params.append(['imagen', imagen])
            
            #save params
            if output != page.get():
                #print fechanacimiento, fechafallecimiento, imagen, wpage.imagelinks()
                wikipedia.showDiff(page.get(), output)
                page.put(output, u"BOT - Añadiendo parámetros: %s" % (', '.join(['%s=%s' % (k, v) for k, v in params])))
            
            #redirects
            redtext = u"#REDIRECT [[%s]]" % (page.title())
            reds = wpage.getReferences(redirectsOnly=True)
            for red in reds:
                redpage = wikipedia.Page(site, red.title())
                if not redpage.exists():
                    print '--> ', red.title()
                    redpage.put(redtext, redtext)
            redpage = wikipedia.Page(site, wpage.title())
            if not redpage.exists():
                print '--> ', red.title()
                redpage.put(redtext, redtext)
            
