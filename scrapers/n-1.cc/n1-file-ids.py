#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 emijrp
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
import sys
import time
import urllib

offset = len(sys.argv) > 1 and sys.argv[1] or 0
file_r = re.compile('https?://n-1.cc/pg/file/read/(\d+)/')
raw = ''
while offset == 0 or re.findall(file_r, raw):
    print 'Loading from offset', offset
    url = 'https://n-1.cc/mod/file/world.php?offset=%d' % (offset)
    raw = unicode(urllib.urlopen(url).read(), 'utf-8')
    new_ids = re.findall(file_r, raw)
    ids = [id.strip() for id in open('file.ids', 'r').readlines()]
    ids += new_ids
    uniq = []
    for id in ids:
        if not id in uniq:
            uniq.append(id)
    ids = uniq
    print 'We have', len(ids), 'ids'
    f = open('file.ids', 'w')
    f.write('\n'.join(ids))
    f.close()
    offset += 10
