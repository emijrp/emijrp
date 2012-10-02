#!/usr/bin/env python
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

# Install: save this script in the pywikipedia directory
# Usage: python massuploader.py --flickrset:http://www.flickr.com/photos/15mmalagacc/sets/72157629844179358/ --importimagesphp:/path/to/importImages.php
# More documentation: http://www.mediawiki.org/wiki/Manual:ImportImages.php

import os
import re
import sys
import time
import urllib, urllib2
import wikipedia

def unquote(s):
    s = re.sub('&quot;', '"', s)
    return s

def main():
    photosmetadata = {}
    flickrseturl = ''
    importimagesphp = ''
    
    #load parameters
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--flickrset:'): # --flickrset:http://www.flickr.com/photos/15mmalagacc/sets/72157629844179358/
                flickrseturl = arg[12:]
            elif arg.startswith('--importimagesphp:'): # --importimagesphp:/path/to/importImages.php
                importimagesphp = arg[18:]
    
    if not flickrseturl:
        print 'Provide --flickrset: parameter'
        sys.exit()
    if not importimagesphp:
        print 'Provide --importimagesphp: parameter'
        sys.exit()
    
    flickrsetid = flickrseturl.split('/sets/')[1].split('/')[0]
    
    #load flickr set metadata
    html = urllib.urlopen(flickrseturl).read()
    flickrsetname = unquote(re.findall(ur'(?im)<meta property="og:title" content="([^>]*?)" />', html)[0])
    flickruser = re.findall(ur'(?im)<meta property="flickr_photos:by" content="http://www.flickr.com/photos/([^/]+?)/" />', html)[0]
    photoids = re.findall(ur'(?im)data-photo-id="(\d+)"', html)
    print 'There are', len(photoids), 'images in the set', flickrsetid, 'by', flickruser
    
    #load flickr images metadata
    for photoid in photoids:
        photourl = 'http://www.flickr.com/photos/%s/%s/in/set-%s' % (flickruser, photoid, flickrsetid)
        html2 = urllib.urlopen(photourl).read()
        #check license, if not free, do not donwload later
        photolicense = ''
        if re.search(ur'(?im)<a href="http://creativecommons.org/licenses/(by(-sa)?/2.0)[^=]*?" rel="license cc:license">', html2):
            photolicense = re.findall(ur'(?im)<a href="http://creativecommons.org/licenses/(by(-sa)?/2.0)[^=]*?" rel="license cc:license">', html2)[0][0]
        else:
            print 'Skiping', photoid, 'which is not Creative Commons'
            continue
        
        photosmetadata[photoid] = {
            'title': re.search(ur'<meta property="og:title" content="([^>]*?)" />', html2) and unquote(re.findall(ur'<meta property="og:title" content="([^>]*?)" />', html2)[0]).strip() or '',
            'description': re.search(ur'<meta property="og:description" content="([^>]*?)" />', html2) and unquote(re.findall(ur'<meta property="og:description" content="([^>]*?)" />', html2)[0]).strip() or '', 
            'date-taken': re.search(ur'(?im)/date-taken/(\d+/\d+/\d+)', html2) and re.sub('/', '-', re.findall(ur'(?im)/date-taken/(\d+/\d+/\d+)', html2)[0]) or '', 
            'license': photolicense, 
            'localfilename': u'%s - %s - %s.jpg' % (flickruser, flickrsetid, photoid),
        }
        print photoid
        print photosmetadata[photoid]
    
    #download flickr images
    savepath = flickrsetid
    if not os.path.exists(savepath): #create subdirectory to save images there
        os.makedirs(savepath)
    
    for photoid, photometadata in photosmetadata: #this dictionary includes only CC pics
        photourl = 'http://www.flickr.com/photos/%s/%s/sizes/o/in/set-%s/' % (flickruser, photoid, flickrsetid)
        html3 = urllib.urlopen(photourl).read()
        photourl2 = re.findall(ur'(?im)<dt>[^<]+?</dt>\s*<dd>\s*<a href="(http://[^\">]+?)">', html3)[0]
        print 'Downloading', photometadata['localfilename'], 'from', photourl2
        try:
            urllib.urlretrieve(photourl2, savepath+'/'+photometadata['localfilename'])
        except:
            time.sleep(10)
            try:
                urllib.urlretrieve(photourl2, savepath+'/'+photometadata['localfilename'])
            except:
                print 'Error while retrieving image, retry'
                sys.exit()
    
    #import images
    os.system('php %s ./%s' % (importimagesphp, flickrsetid))
    
    #create image pages
    for photoid, photometadata in photosmetadata:
        desc = photometadata['title']
        if photometadata['description']:
            if desc:
                desc = u'%s. %s' % (desc, photometadata['description'])
            else:
                desc = photometadata['description']
        source = u'[%s %s]' % (flickrseturl, flickrsetname)
        date = photometadata['date-taken']
        author = u'{{flickr|%s}}' % ()
        license = u'{{cc-%s-2.0}}' % (photometadata['license'])
        output = u"""{{Infobox Archivo
| descripción = %s
| fuente = %s
| fecha = %s
| autor = %s
| licencia = {{cc-%s}}
}}""" % (desc, source, date, author, license)
        p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), photometadata['localfilename'])
        if not p.exits():
            p.put(output, u'BOT - Importing file')

if __name__ == '__main__':
    main()

