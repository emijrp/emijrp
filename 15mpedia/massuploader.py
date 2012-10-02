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

# http://www.mediawiki.org/wiki/Manual:ImportImages.php

import os
import re
import sys
import urllib, urllib2
import wikipedia

def unquote(s):
    return s

def main():
    photometadata = {}
    flickrseturl = ''
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--flickrset:'): # --flickrset:http://www.flickr.com/photos/15mmalagacc/sets/72157629844179358/
                flickrseturl = arg[12:]
    
    if not flickrseturl:
        print 'Provide --flickrset: parameter'
        sys.exit()
    
    flickrsetid = flickrseturl.split('/sets/')[1].split('/')[0]
    
    #load flickr set metadata
    html = urllib.urlopen(flickrseturl).read()
    flickruser = re.findall(ur'(?im)<meta property="flickr_photos:by" content="http://www.flickr.com/photos/([^/]+?)/" />', html)[0]
    photoids = re.findall(ur'(?im)data-photo-id="(\d+)"', html)
    print 'There are', len(photoids), 'images in the set', flickrsetid, 'by', flickruser
    
    #load flickr images metadata
    for photoid in photoids:
        photourl = 'http://www.flickr.com/photos/%s/%s/in/set-%s' % (flickruser, photoid, flickrsetid)
        html2 = urllib.urlopen(photourl).read()
        #check license, if not free, do not donwload later
        
        photometadata[photoid] = {
            'title': re.search(ur'<meta property="og:title" content="([^>]*?)" />', html2) and unquote(re.findall(ur'<meta property="og:title" content="([^>]*?)" />', html2)[0]) or '',
            'description': re.search(ur'<meta property="og:description" content="([^>]*?)" />', html2) and unquote(re.findall(ur'<meta property="og:description" content="([^>]*?)" />', html2)[0]) or '', 
            'date-taken': re.search(ur'(?im)/date-taken/(\d+/\d+/\d+)', html2) and re.sub('/', '-', re.findall(ur'(?im)/date-taken/(\d+/\d+/\d+)', html2)[0]) or '', 
            'license': '', 
        }
        print photoid
        print photometadata[photoid]
    
    #download flickr images
    savepath = flickrsetid
    if not os.path.exists(savepath): #create subdirectory to save images there
        os.makedirs(savepath)
    
    for photoid in photoids:
        photofilename = '%s - %s - %s.jpg' % (flickruser, flickrsetid, photoid)
        photourl = 'http://www.flickr.com/photos/%s/%s/sizes/o/in/set-%s/' % (flickruser, photoid, flickrsetid)
        html3 = urllib.urlopen(photourl).read()
        photourl2 = re.findall(ur'(?im)<dt>[^<]+?</dt>\s*<dd>\s*<a href="(http://[^\">]+?)">', html3)[0]
        print 'Downloading', photofilename, 'from', photourl2
        urllib.urlretrieve(photourl2, savepath+'/'+photofilename)
    
    #import images
    os.system('php importImages.php')
    
    
    #create image pages
    
    

if __name__ == '__main__':
    main()

