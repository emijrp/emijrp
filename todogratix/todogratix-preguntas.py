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

sitees = wikipedia.Site('es', 'wikipedia')
sitetg = wikipedia.Site('todogratix', 'todogratix')
#planti = wikipedia.Page(sitees, u'Plantilla:Ficha de país')
#gen = pagegenerators.ReferringPageGenerator(planti, followRedirects=True, onlyTemplateInclusion=True)
category = catlib.Category(sitetg, u'Category:Personas')
gen = pagegenerators.CategorizedPageGenerator(category, recurse=False, start='!')
pre = pagegenerators.PreloadingGenerator(gen)

skip = u'Juan Manuel Infante of Castile'
for page in pre:
    if not page.exists() or page.isRedirectPage() or page.namespace() != 0:
        continue
    if skip:
        if page.title() == skip:
            skip = ''
        continue
    
    #filter
    if re.search(ur"[\(\),\.\:\-]", page.title()) or \
        not re.search(ur"(?im)fechafallecimiento\s*=\s*\d{4}", page.get()):
        continue
    
    #field
    output = u"""{{Infobox Pregunta
|pregunta={{subst:PAGENAME}}
|respuesta={{pregunta|página=%s|pregunta=fecha de fallecimiento}}
|género=biografías, %s
}}""" % (page.title(), page.title().lower())
    
    tgpage = wikipedia.Page(sitetg, u"Pregunta:¿Cuándo murió %s?" % (page.title()))
    if not tgpage.exists():
        print output
        tgpage.put(output, output)
    
    #redirects
    redtext = u"#REDIRECT [[%s]]" % (tgpage.title())
    for red in [u"Pregunta:¿En qué año murió %s?" % (page.title()), u"Pregunta:¿Año de la muerte de %s?" % (page.title()), u"Pregunta:¿Año de fallecimiento de %s?" % (page.title()), u"Pregunta:¿Fecha de fallecimiento de %s?" % (page.title())]:
        tgpage = wikipedia.Page(sitetg, red)
        if not tgpage.exists():
            tgpage.put(redtext, redtext)
    
