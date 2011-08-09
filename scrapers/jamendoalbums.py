# -*- coding: utf-8 -*-

# Copyright (C) 2011 emijrp
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

# HOWTO: python jamendoalbums.py 0 100000
# Arguments 1 and 2 are the range of albums IDs to download (mandatory). Currently there are about 50000 albums on Jamendo (but as people delete albums you will have to request from ID 0 to ID 100000 aprox.)

# Argument 3 is the sound format (ogg (by default) or mp3)
# python jamendoalbums.py 0 100000 mp3
# or python jamendoalbums.py 0 100000 ogg
# If you want to download both formats, I recommend to create two different directories and run the script inside both

# Argument 4 is the download speed in kb/s (optional). Format (number + k): 100k
# python jamendoalbums.py 0 100000 mp3 250k
# or python jamendoalbums.py 0 100000 ogg 400k

# More info (and XML database with albums metadata) http://developer.jamendo.com/en/wiki/NewDatabaseDumps

import os
import re
import time
import urllib
import sys
import zipfile, os.path

def unzip_file_into_dir(file, dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    zfobj = zipfile.ZipFile(file)
    for name in zfobj.namelist():
        if name.endswith('/'):
            os.mkdir(os.path.join(dir, name))
        else:
            outfile = open(os.path.join(dir, name), 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()

startid = 0
endid = 100000
sound = 'ogg3'
speed = '1000000k'

# Your bittorrent client options (if you want to load the albums into your bittorrent)
# Disabled with comments below
# incoming = '/media/.../Torrent'
# incomingtorrents = '/media/.../Torrent/torrentfiles'

if len(sys.argv) >= 1:
    pass # startid = 0 & endid = 100000

if len(sys.argv) >= 2:
    startid = int(sys.argv[1]) # endid = 100000

if len(sys.argv) >= 3:
    endid = int(sys.argv[2])

if len(sys.argv) >= 4:
    temp = sys.argv[3].lower().strip()
    if temp == 'ogg':
        sound = 'ogg3'
    elif temp == 'mp3':
        sound = 'mp32'

if len(sys.argv) >= 5:
    speed = sys.argv[4]

for id in range(startid, endid):
    print 'Trying downloading album [%d]' % (id)
    time.sleep(1)
    #url = 'http://www.jamendo.com/en/download/album/%d/?output=contentonly' % (id)
    url = 'http://api.jamendo.com/get2/bittorrent/file/plain/?album_id=%d&type=archive&class=%s' % (id, sound)
    f = urllib.urlopen(url)
    raw = f.read()
    f.close()
    
    torrents = re.findall(ur'(?im)^(http://[^\"]+?\.torrent)$', raw)
    if torrents:
        torrenturl = torrents[0]
        torrentname = torrenturl.split('/')[-1] # we get text from last / http://imgjam.com/torrents/album/666/6666/6666-ogg3.torrent/mob%20-%20celete%20--%20Jamendo%20-%20OGG%20Vorbis%20q7%20-%202007.07.23%20%5Bwww.jamendo.com%5D.torrent
        torrentname = urllib.unquote(torrentname)
        torrentname = re.sub(ur'"', ur'\\"', torrentname) #i think it is not neccesary, no quotes in files http://www.jamendo.com/en/album/25410
        name = torrentname.split('.torrent')[0]
        subdir = '%.6d-%.6d' % ((id/1000)*1000, (id/1000)*1000+999)
        
        pathtorrent = ''
        if sound == 'ogg3':
            pathtorrent = "%s/torrentsogg" % (subdir)
        elif sound == 'mp32':
            pathtorrent = "%s/torrentsmp3" % (subdir)
        if not os.path.exists(pathtorrent):
            os.makedirs(pathtorrent)
        
        prefix = '[%.6d] ' % (id)
        #download .torrent
        os.system('wget "%s" -O "%s/%s%s" -c --limit-rate=%s' % (torrenturl, pathtorrent, prefix, torrentname, speed))
        time.sleep(2)
        
        #download .zip
        urlzip = 'http://www.jamendo.com/get/album/id/album/archiverestricted/redirect/%d/?are=%s' % (id, sound)
        pathzip = subdir
        zipname = '%s%s.zip' % (prefix, name)
        os.system('wget "%s" -O "%s/%s" -c --limit-rate=%s' % (urlzip, pathzip, zipname, speed))
        time.sleep(2)
        
        #unzip to Bittorent client incoming directory
        #unzip_file_into_dir(open('%s/%s' % (pathzip, zipname)), '%s/%s' % (incoming, name))
        
        #copy .torrent to Bittorrent client torrents directory
        #os.system('cp "%s/%s%s" "%s/%s"' % (pathtorrent, prefix, torrentname, incomingtorrents, torrentname))
    else:
        print 'No album [%d] available' % (id)
