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

import os
import re
import sys
import time
import unicodedata
import urllib

# description https://n-1.cc/pg/file/read/877875
# download link https://n-1.cc/mod/file/download.php?file_guid=877875

def removeoddchars(s):
    #http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
    s = ''.join((c for c in unicodedata.normalize('NFD', u'%s' % s) if unicodedata.category(c) != 'Mn'))
    s = re.sub(ur"(?im)[^a-z0-9_\.\- ]", ur"", s) 
    return s

ids = [l.strip() for l in open(sys.argv[1], 'r').readlines()]
dirlimit = 10000 #max files by directory, do not change
skip = ''
if len(sys.argv) > 2:
    skip = sys.argv[2]
for id in ids:
    if skip:
        if skip == id:
            skip = ''
        continue
    time.sleep(0.1)
    id = int(id)
    path = '%09d-%09d' % (id/dirlimit*dirlimit, (id/dirlimit+1)*dirlimit-1)
    if not os.path.exists(path):
        os.makedirs(path)
    print 'Downloading file', id
    raw = unicode(urllib.urlopen('https://n-1.cc/pg/file/read/%d' % (id)).read(), 'utf-8')
    if re.findall(ur"(?im)No se han encontrado resultados", raw):
        continue
    filename = re.findall(ur'<div class="filerepo_title"><h2><a href="https://n-1\.cc/mod/file/download.php\?file_guid=\d+">([^<]+?)</a></h2></div>', raw)[0]
    filename = removeoddchars(filename)
    os.system('wget -c --no-check-certificate https://n-1.cc/pg/file/read/%d -O "%s/[%09d] %s.html"' % (id, path, id, filename))
    os.system('wget -c --no-check-certificate https://n-1.cc/mod/file/download.php?file_guid=%d -O "%s/[%09d] %s.file"' % (id, path, id, filename))
    
    
