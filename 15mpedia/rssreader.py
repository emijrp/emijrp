#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib
import wikipedia

urls = open('rss.txt', 'r').read().splitlines()
urls.sort()

content = []
for url in urls:
    try:
        xml = unicode(urllib.urlopen(url).read(), 'utf-8')
    except:
        try:
            xml = unicode(urllib.urlopen(url).read(), 'iso-8859-1')
        except:
            continue
    chunks = '</entry>'.join('<entry>'.join(xml.split('<entry>')[1:]).split('</entry>')[:-1]).split('</entry><entry>') #</entry><entry>
    
    sitetitle = u''
    if re.search(ur"(?im)>([^<>]*?)</title>", xml):
        sitetitle = re.findall(ur">([^<>]*?)</title>", xml)[0]
    else:
        sitetitle = url
    sitesubtitle = u''
    if re.search(ur"(?im)>([^<>]*?)</subtitle>", xml):
        sitesubtitle = re.findall(ur">([^<>]*?)</subtitle>", xml)[0]
    
    print sitetitle
    print sitesubtitle
    
    for chunk in chunks:
        if not re.search(ur"(?im)</title>", chunk) or not re.search(ur"(?im)</updated>", chunk):
            continue
        
        title = re.findall(ur"(?im)>([^<>]*?)</title>", chunk)[0]
        updated = re.findall(ur"(?im)>([^<>]*?)</updated>", chunk)[0]
        updated = updated.split('.')[0]
        url = re.findall(ur"(?im)<link rel='alternate' type='text/html' href='([^>]*?)' title='", chunk)[0]
        
        #print updated, title, url
        content.append([updated, sitetitle, title, url])

content.sort(reverse=True)
output = u''
for updated, sitetitle, title, url in content[:100]:
    output += u'* %s: [%s %s] (%s)\n' % (updated, url, title, sitetitle)

page = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'Usuario:Emijrp/Sandbox')
page.put(output, u"BOT - Añadiendo RSS")

