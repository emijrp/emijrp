# -*- coding: utf-8 -*-

# Copyright (C) 2013 emijrp <emijrp@gmail.com>
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

import catlib
import pagegenerators
import sys
import wikipedia

start = sys.argv[1]
lfsite = wikipedia.Site('librefind', 'librefind')
ensite = wikipedia.Site('en', 'wikipedia')

cat = catlib.Category(lfsite, u"Category:All the searches")
gen = pagegenerators.CategorizedPageGenerator(cat, start=start)
pre = pagegenerators.PreloadingGenerator(gen)

for page in pre:
    title = page.title()
    enpage = wikipedia.Page(ensite, title)
    if enpage.exists() and not enpage.isRedirectPage() and not enpage.isDisambig():
        redirects = enpage.getReferences(redirectsOnly=True)
        for redirect in redirects:
            if redirect.namespace() != 0: #skiping redirects from userpages etc
                continue
            rtitle = redirect.title()
            print rtitle, title
            rpage = wikipedia.Page(lfsite, rtitle)
            if rpage.exists():
                break #skiping, this title was probably analysed in the past
            else:
                rtext = u"#REDIRECT [[%s]]" % (title)
                rpage.put(rtext, rtext)
            
        

