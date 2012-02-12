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
import string

import catlib
import pagegenerators
import wikipedia

el = wikipedia.Site("enciclopedialibre", "enciclopedialibre")
#gen = pagegenerators.AllpagesPageGenerator(start='!', namespace=0, includeredirects=False)
cat = catlib.Category(site=el, title=u"Desambiguación")

az = string.uppercase[:26]
dic = {}

for letter in az:
    gen = pagegenerators.CategorizedPageGenerator(cat, recurse=False, start=letter)
    pre = pagegenerators.PreloadingGenerator(generator=gen, pageNumber=1)
    for page in pre:
        dic[letter] = page.title()
        #print dic.items()
        break

print dic
gen = pagegenerators.CategorizedPageGenerator(cat, recurse=False, start=az[0])
pre = pagegenerators.PreloadingGenerator(generator=gen, pageNumber=200)
titles = []
for page in pre:
    if page.namespace() == 0 and not page.isRedirectPage():
        titles.append(page.title())
    #if page.title() == 'C':
    #    break

print titles

output = u""
c = 0
for letter in az:
    ok = False
    acum = []
    for title in titles:
        if not ok and title == dic[letter]:
            ok = True
        if ok and c!=len(az)-1 and title == dic[az[c+1]]:
            ok = False
            break
        if ok:
            acum.append(title)
    output += u"\n\n=== %s ===\n%s" % (letter, ' - '.join(['[[%s]]' % p for p in acum]))
    c += 1

page = wikipedia.Page(el, u"Enciclopedia:Páginas de desambiguación")
wtext = page.get()
newtext = u'%s{{IndiceAlfabetico}}%s\n\n[[Categoría:Mantenimiento de la enciclopedia|Desambiguación]]' % (wtext.split('{{IndiceAlfabetico}}')[0], output)
newtext = newtext.strip()

print newtext

if wtext != newtext:
    wikipedia.showDiff(wtext, newtext)
    page=wikipedia.Page(el, u"Usuario:Emijrp/Pruebas")
    page.put(newtext, newtext)
