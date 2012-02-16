# -*- coding: utf-8 -*-

# Copyright (C) 2011 TodoGratix
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

import catlib
import pagegenerators
import wikipedia

s = wikipedia.Site('es', 'wikisource')
w = wikipedia.Site('es', 'wikipedia')
q = wikipedia.Site('es', 'wikiquote')
c = wikipedia.Site('commons', 'commons')
category = catlib.Category(s, u'Category:DP-Autores-100')
gen = pagegenerators.CategorizedPageGenerator(category, recurse=False, start='!')
pre = pagegenerators.PreloadingGenerator(gen)

skip = u'Francisco de Rioja'
for page in pre:
    if not page.exists() or page.isRedirectPage() or page.namespace() != 0:
        continue
    
    stitle = page.title()
    print stitle
    if skip:
        if stitle == skip:
            skip = ''
        continue
    stext = page.get()
    
    #proyectos hermanos
    proys = {'wikiquote': '', 'commons': '', 'wikipedia': ''}
    wtext = ''
    for proy in proys.keys():
        m = re.findall(ur"(?im)%s\s*=\s*([^\|\n\r]+)\s*[\|\n\r]" % (proy), stext)
        if m:
            proys[proy] = re.sub(ur"_", ur" ", m[0])
        if re.search(ur"(?im)pagename", proys[proy]):
            proys[proy] = stitle
        proys[proy] = proys[proy].strip()
        if not proys[proy]:
            continue
        tpage = ''
        if proy == 'wikiquote':
            tpage = wikipedia.Page(q, proys[proy])
        elif proy == 'commons':
            tpage = wikipedia.Page(c, proys[proy])
        elif proy == 'wikipedia':
            tpage = wikipedia.Page(w, proys[proy])
        
        if tpage and tpage.exists():
            if tpage.isRedirectPage():
                tpage = tpage.getRedirectTarget()
                if tpage.isRedirectPage():
                    proys[proy] = ''
                    tpage = ''
            if tpage:
                if proy == 'wikipedia':
                    wtext = tpage.get()
        else:
            proys[proy] = ''
            tpage = ''
    
    if not wtext:
        continue
    
    #foto
    m = re.findall(ur"(?im)Foto\s*=\s*([^\|\n\r]+\.jpe?g)\s*[\|\n\r]", stext)
    image = ''
    if m:
        if not re.search(ur"(?im)falta", m[0]): #falta foto.jpg
            image = m[0]
    
    #nombre, apellidos
    nombre = ''
    apellidos = ''
    for r in [ur"(?im)\{\{\s*DEFAULTSORT\s*:\s*([^,]+)\s*,\s*([^\}]+)\s*\}\}", ur"(?im)\{\{\s*(?:BD|NF)\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*([^,]+)\s*,\s*([^\}]+)\s*\}\}"]:
        m = re.findall(r, wtext)
        if m:
            print m
            nombre = m[0][1]
            apellidos = m[0][0]
            break
    
    #fechas
    m = re.findall(ur"(?im)\[\[\s*Categor(?:y|ía)\s*:\s*(N|F)(\d+)\s*[\|\]]", stext)
    nyear = ''
    fyear = ''
    if m:
        for n in m:
            if n[0].lower() == 'n':
                nyear = n[1]
            elif n[0].lower() == 'f':
                fyear = n[1]
    
    #lugar nacimiento
    #las nacionalidades con más autores de momento
    lugarnacimiento = ''
    if re.search(ur"(?im)Autores españoles", stext):
        lugarnacimiento = u'España'
    elif re.search(ur"(?im)Autores estadounidenses", stext):
        lugarnacimiento = u'Estados Unidos'
    elif re.search(ur"(?im)Autores franceses", stext):
        lugarnacimiento = u'Francia'
    elif re.search(ur"(?im)Autores italianos", stext):
        lugarnacimiento = u'Italia'
    elif re.search(ur"(?im)Autores argentinos", stext):
        lugarnacimiento = u'Argentina'
    elif re.search(ur"(?im)Autores alemanes", stext):
        lugarnacimiento = u'Alemania'
    
    #ocupacion
    ocupacion = []
    m = re.findall(ur"(?im)Texto\s*=\s*([^\=]+)\s*[\=]", stext)
    if m:
        n = re.findall(ur"(?im)\b(abogado|actor|crítico literario|cuentista|dramaturgo|escritor|explorador|filósofo|geógrafo|matemático|médico|militar|músico|naturalista|novelista|poeta|político)\b", m[0])
        for o in n:
            ocupacion.append(o.lower())
            if o.lower() in ['cuentista', 'dramaturgo', 'novelista', 'poeta'] and not 'escritor' in ocupacion:
                ocupacion.append('escritor') #general para todos los de letras
    ocupacion = ', '.join(set(ocupacion))
    
    if nombre and apellidos and nyear and fyear and proys['wikipedia']:
        output = u"""{{Infobox Persona
|nombre=%s
|apellidos=%s
|imagen=%s
|fechanacimiento=%s
|lugarnacimiento=%s
|fechafallecimiento=%s
|lugarfallecimiento=
|ocupación=%s
}}

{{obras por autor}}

== Enlaces externos ==
%s* {{s|es|%s}}%s%s""" % (nombre, apellidos, image, nyear, lugarnacimiento, fyear, ocupacion, proys['wikipedia'] and '* {{w|es|%s}}\n' % proys['wikipedia'] or '', stitle, proys['wikiquote'] and '\n* {{q|es|%s}}' % proys['wikiquote'] or '', proys['commons'] and '\n* {{commons|%s}}' % proys['commons'] or '')
        
        todogratix = wikipedia.Page(wikipedia.Site('todogratix', 'todogratix'), stitle)
        if not todogratix.exists():
            print output
            todogratix.put(output, output)
    
