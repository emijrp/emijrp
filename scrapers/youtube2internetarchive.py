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

# Keys: http://archive.org/account/s3.php
# Documentation: http://archive.org/help/abouts3.txt
# https://wiki.archive.org/twiki/bin/view/Main/IAS3BulkUploader

import json
import os
import re
import subprocess
import unicodedata
import urllib

"""
Required files:
 * download/videostodo.txt: list of YouTube videos inside a directory named download
 * keys.txt: accesskey and secretkey (in that order) for IA S3 (in two separated lines) in the current directory
"""

sizelimit = 25*1024*1024 # file size, if you want to skip those videos greater than this size, else put 10000*1024*1024 for 10GB

num2month = {'01':'enero', '02': 'febrero', '03':'marzo', '04':'abril', '05':'mayo', '06':'junio', '07':'julio', '08':'agosto','09':'septiembre','10':'octubre', '11':'noviembre', '12':'diciembre'}
accesskey = open('keys.txt', 'r').readlines()[0].strip()
secretkey = open('keys.txt', 'r').readlines()[1].strip()
videotodourls = [l.strip() for l in open('download/videostodo.txt', 'r').readlines()]

def quote(t):
    return re.sub(ur"'", ur"\'", t)

def removeoddchars(s):
    #http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
    s = ''.join((c for c in unicodedata.normalize('NFD', u'%s' % s) if unicodedata.category(c) != 'Mn'))
    s = re.sub(ur"/", ur"-", s)
    return s

def updatetodo(l):
    f = open('videostodo.txt', 'w')
    f.write('\n'.join(l))
    f.close()

while len(videotodourls) > 0:
    os.chdir('download')
    videotodourl = videotodourls[0]
    videohtml = unicode(urllib.urlopen(videotodourl).read(), 'utf-8')
    videoid = videotodourl.split('watch?v=')[1]
    #verify license in youtube
    if not re.search(ur"(?i)/t/creative_commons", videohtml):
        print "It is not Creative Commons", videotodourl
        videotodourls.remove(videotodourl)
        updatetodo(videotodourls)
        os.chdir('..')
        continue
    #get tags
    tags = re.findall(ur"search=tag\">([^<]+)</a>", videohtml)
    tags = [quote(tag) for tag in tags]
    
    os.system('python ../youtube-dl -t -i -c - %s --write-info-json --format 18' % (videotodourl)) #mp4 (18)
    videofilename = ''
    jsonfilename = ''
    for dirname, dirnames, filenames in os.walk('.'):
        if dirname == '.':
            for f in filenames:
                if f.endswith('%s.mp4' % videoid):
                    videofilename = unicode(f, 'utf-8')
            break #stop searching, dot not explore subdirectories
    
    if videofilename:
        jsonfilename = '%s.info.json' % (videofilename)
        if os.path.getsize(videofilename) > sizelimit:
            print 'Video is greater than', sizelimit, 'bytes'
            print 'Skiping...'
            videotodourls.remove(videotodourl)
            updatetodo(videotodourls)
            os.chdir('..')
            continue
    else:
        print 'No video downloaded, an error ocurred'
        videotodourls.remove(videotodourl)
        updatetodo(videotodourls)
        os.chdir('..')
        continue
    
    json_ = json.loads(unicode(open(jsonfilename, 'r').read(), 'utf-8'))
    upload_date = json_['upload_date'][:4] + '-' + json_['upload_date'][4:6] + '-' + json_['upload_date'][6:8]
    upload_year = json_['upload_date'][:4]
    upload_month = num2month[json_['upload_date'][4:6]]
    description = json_['description']
    uploader = json_['uploader']
    title = json_['title']
    language = 'Spanish'
    
    itemname = 'spanishrevolution-%s' % (videofilename)
    itemname = itemname[:100]
    if not re.search(ur"Item cannot be found", urllib.urlopen('http://archive.org/details/%s' % (itemname)).read()):
        print 'That item exists at Internet Archive', 'http://archive.org/details/%s' % (itemname)
        videotodourls.remove(videotodourl)
        updatetodo(videotodourls)
        os.chdir('..')
        continue
    
    curl = ['curl', '--location', 
        '--header', u"'x-amz-auto-make-bucket:1'",
        '--header', u"'x-archive-meta01-collection:spanishrevolution'",
        '--header', u"'x-archive-meta-mediatype:movies'",
        '--header', u"'x-archive-size-hint:%d'" % (os.path.getsize(videofilename)), 
        '--header', u'"authorization: LOW %s:%s"' % (accesskey, secretkey),
        '--header', u"'x-archive-meta-title:%s'" % (quote(title)),
        '--header', u"'x-archive-meta-description:%s<br/><br/>Source: <a href=\"%s\">%s</a><br/>Uploader: <a href=\"http://www.youtube.com/user/%s\">%s</a><br/>Upload date: %s'" % (quote(description), videotodourl, videotodourl, quote(uploader), quote(uploader), upload_date),
        '--header', u"'x-archive-meta-date:%s'" % (upload_date),
        '--header', u"'x-archive-meta-year:%s'" % (upload_year),
        '--header', u"'x-archive-meta-language:%s'" % (language),
        '--header', u"'x-archive-meta-creator:%s'" % (quote(uploader)),
        '--header', u"'x-archive-meta-subject:%s'" % (u'; '.join(['spanishrevolution', 'videos', upload_month, upload_year] + tags)),
        '--header', u"'x-archive-meta-licenseurl:%s'" % ('http://creativecommons.org/licenses/by/3.0/'), # from https://www.youtube.com/t/creative_commons
        #'--header', "'x-archive-meta-rights:%s'" % (rights),
        '--header', u"'x-archive-meta-originalurl:%s'" % (videotodourl),
        '--upload-file', videofilename,
            u"http://s3.us.archive.org/%s/%s" % (removeoddchars(itemname), removeoddchars(videofilename)),
    ]
    print 'Uploading to Internet Archive as:', removeoddchars(itemname)
    curlline = ' '.join(curl)
    os.system(curlline.encode('utf-8'))
    
    print 'You can browse it in http://archive.org/details/%s' % (removeoddchars(itemname))
    videotodourls.remove(videotodourl)
    updatetodo(videotodourls)
    os.remove(videofilename)
    os.remove(jsonfilename)
    os.chdir('..')
