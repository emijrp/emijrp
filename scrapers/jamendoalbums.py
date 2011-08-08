# -*- coding: utf-8 -*-

#license: gpl v3

#help: python jamendo.py 0 10000
#arguments 1 and 2 are the range of albums IDs to download (mandatory)
#argument 3 is the download speed in kb/s (optional)

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

a = 0
b = 90000
speed = '1000000k'
#your bittorrent client options
incoming = '/media/.../Torrent'
incomingtorrents = '/media/.../Torrent/torrentfiles'

if len(sys.argv)==1:
    pass
elif len(sys.argv)==2:
    a=int(sys.argv[1])
    b=a+b
elif len(sys.argv)==3:
    a=int(sys.argv[1])
    b=int(sys.argv[2])
elif len(sys.argv)==4:
    a=int(sys.argv[1])
    b=int(sys.argv[2])
    speed=sys.argv[3]
else:
    sys.exit()

for id in range(a, b):
    time.sleep(1)
    url = 'http://www.jamendo.com/en/download/album/%d/?output=contentonly' % id
    #os.system('wget "%s" -O jamendo%d.html' % (url, id))
    #file='jamendo%d.html' % id
    #f=open(file, 'r')
    #raw=f.read()
    f = urllib.urlopen(url)
    raw = f.read()
    f.close()
    
    torrents=re.findall(ur'href=\"([^\"]+?\.torrent)\"', raw)
    if torrents:
        torrentoggurl=torrents[1]
        torrentoggname=torrentoggurl.split('/')[-1]
        torrentoggname=urllib.unquote(torrentoggname)
        torrentoggname=re.sub(ur'"', ur'\\"', torrentoggname) #i think it is not neccesary, no quotes in files http://www.jamendo.com/en/album/25410
        oggname=torrentoggname.split('.torrent')[0]
        subdir='%.6d-%.6d' % ((id/1000)*1000, (id/1000)*1000+999)
        
        pathtorrentogg = "%s/torrentsogg" % subdir
        if not os.path.exists(pathtorrentogg):
            os.makedirs(pathtorrentogg)
        
        prefix = '[%.6d] ' % (id)
        #download .torrent
        os.system('wget "%s" -O "%s/%s%s" -c --limit-rate=%s' % (torrentoggurl, pathtorrentogg, prefix, torrentoggname, speed))
        time.sleep(2)
        
        #download .zip
        urloggzip = 'http://www.jamendo.com/get/album/id/album/archiverestricted/redirect/%d/?are=ogg3' % (id)
        pathoggzip = subdir
        oggzipname = '%s%s.zip' % (prefix, oggname)
        os.system('wget "%s" -O "%s/%s" -c --limit-rate=%s' % (urloggzip, pathoggzip, oggzipname, speed))
        time.sleep(2)
        
        #unzip to Bittorent client incoming directory
        #unzip_file_into_dir(open('%s/%s' % (pathoggzip, oggzipname)), '%s/%s' % (incoming, oggname))
        
        #copy .torrent to Bittorrent client torrents directory
        #os.system('cp "%s/%s%s" "%s/%s"' % (pathtorrentogg, prefix, torrentoggname, incomingtorrents, torrentoggname))
        
    f.close()
    try:
        os.remove(file)
    except:
        pass
