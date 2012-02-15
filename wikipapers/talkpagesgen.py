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

skip = u'!'
site = wikipedia.Site('wikipapers', 'wikipapers')
gen = pagegenerators.AllpagesPageGenerator(start = skip, namespace=0, includeredirects=False, site=site)
pre = pagegenerators.PreloadingGenerator(gen)
output = u"<noinclude>{{talk}}</noinclude>"
for page in pre:
    if page.exists() and not page.isRedirectPage():
        if re.search(ur"(?im)\{\{\s*Infobox Publication", page.get()):
            talk = page.toggleTalkPage()
            if not talk.exists():
                talk.put(output, output)
            
            
