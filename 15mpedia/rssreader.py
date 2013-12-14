#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
import datetime
import re
import urllib
import wikipedia
from xml.sax.saxutils import unescape

def uncode(s):
    try:
        xml = unicode(s, 'utf-8')
    except:
        try:
            xml = unicode(s, 'iso-8859-1')
        except:
            return s
    return xml

def getLines(page):
    p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), page)
    raw = p.get()
    raw = re.sub(ur"(?im)^\*\s*", ur"", raw)
    rss = []
    for l in raw.splitlines():
        if not l.startswith('#'):
            rss.append(l)
    return rss

def sortLines(page):
    p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), page)
    raw = list(set(p.get().splitlines()))
    raw.sort()
    p.put(ur"%s" % (u'\n'.join(raw)), u"BOT - Ordenando enlaces")

def getBlogs():
    rss = sortLines(u'15Mpedia:Actualizaciones/Blogosfera (RSS)')
    rss = getLines(u'15Mpedia:Actualizaciones/Blogosfera (RSS)')
    print 'Loaded %d RSS for blogs' % (len(rss))
    
    content = []
    for url in rss:
        try:
            xml = uncode(urllib.urlopen(url).read())
            #print xml[:100]

            chunks = '</entry>'.join('<entry>'.join(xml.split('<entry>')[1:]).split('</entry>')[:-1]).split('</entry><entry>') #</entry><entry>
            
            sitetitle = u''
            if re.search(ur"(?im)>([^<>]*?)</title>", xml):
                sitetitle = re.findall(ur"(?im)>([^<>]*?)</title>", xml)[0]
            else:
                sitetitle = url
            sitesubtitle = u''
            if re.search(ur"(?im)>([^<>]*?)</subtitle>", xml):
                sitesubtitle = re.findall(ur"(?im)>([^<>]*?)</subtitle>", xml)[0]
            
            print sitetitle
            #print sitesubtitle
        
            for chunk in chunks:
                if not re.search(ur"(?im)</title>", chunk) or not re.search(ur"(?im)</updated>", chunk):
                    continue
                
                title = u'Sin título'
                title = re.findall(ur"(?im)>([^<>]*?)</title>", chunk)[0].strip()
                updated = re.findall(ur"(?im)>([^<>]*?)</updated>", chunk)[0].strip()
                updated = updated.split('T')[0]
                url = re.findall(ur"(?im)<link rel='alternate' type='text/html' href='([^>]*?)' title='", chunk)[0].strip()
                
                #print updated, title, url
                content.append([updated, sitetitle, title, url])
        except:
            print 'Error'
            continue
    
    content.sort(reverse=True)
    return content

def getFacebook():
    rss = getLines(u'15Mpedia:Actualizaciones/Facebook (RSS)')
    print 'Loaded %d RSS for Facebook' % (len(rss))
    
    content = []
    for url in rss:
        try:
            xml = uncode(urllib.urlopen(url).read())
        except:
            continue
        chunks = [u'%s</entry>' % (s) for s in '</entry>'.join('<entry>'.join(xml.split('<entry>')[1:]).split('</entry>')[:-1]).split("""</entry>""")]
        
        sitetitle = u''
        if re.search(ur"(?im)>([^<>]*?)</name>", xml):
            sitetitle = re.findall(ur"(?im)>([^<>]*?)</name>", xml)[0]
        else:
            sitetitle = url
        
        for chunk in chunks:
            if not re.search(ur"(?im)</title>", chunk) or not re.search(ur"(?im)</published>", chunk):
                continue
        
            title = u'Sin título'
            title = unescape(re.findall(ur"(?im)<title>([^\n]*?)</title>", chunk)[0][10:-3])
            published = re.findall(ur"(?im)>([^<>]*?)</published>", chunk)[0]
            published = published.split('T')[0]
            url = re.findall(ur'(?im)<link rel="alternate" type="text/html" href="([^>]*?)" />', chunk)[0]
            
            #print published, title, url
            content.append([published, sitetitle, title, url])

    content.sort(reverse=True)
    return content 

def getFlickr():
    
    return []

def getN1():
    
    return []

def getYouTube():
    rss = sortLines(u'15Mpedia:Actualizaciones/YouTube (RSS)')
    rss = getLines(u'15Mpedia:Actualizaciones/YouTube (RSS)')
    print 'Loaded %d RSS for YouTube' % (len(rss))
    
    content = []
    for url in rss:
        try:
            xml = uncode(urllib.urlopen(url).read())

            chunks = '</entry>'.join('<entry>'.join(xml.split('<entry>')[1:]).split('</entry>')[:-1]).split('</entry><entry>') #</entry><entry>
            
            sitetitle = u''
            if re.search(ur"(?im)>([^<>]*?)</name>", xml):
                sitetitle = re.findall(ur"(?im)>([^<>]*?)</name>", xml)[1] #el 0 es YouTube, el 1 el nombre del canal
            else:
                sitetitle = url
            
            print sitetitle
        
            for chunk in chunks:
                if not re.search(ur"(?im)</title>", chunk) or not re.search(ur"(?im)</published>", chunk):
                    continue
            
                title = u'Sin título'
                title = re.findall(ur"(?im)>([^<>]*?)</title>", chunk)[0]
                published = re.findall(ur"(?im)>([^<>]*?)</published>", chunk)[0]
                published = published.split('T')[0]
                url = re.findall(ur"(?im)<link rel='alternate' type='text/html' href='([^>&]*?)&", chunk)[0]
                
                #print published, title, url
                content.append([published, sitetitle, title, url])
        except:
            print 'Error'
            continue

    content.sort(reverse=True)
    return content

def getMonthName(m):
    if m == 1:
        return u'enero'
    elif m == 2:
        return u'febrero'
    elif m == 3:
        return u'marzo'
    elif m == 4:
        return u'abril'
    elif m == 5:
        return u'mayo'
    elif m == 6:
        return u'junio'
    elif m == 7:
        return u'julio'
    elif m == 8:
        return u'agosto'
    elif m == 9:
        return u'septiembre'
    elif m == 10:
        return u'octubre'
    elif m == 11:
        return u'noviembre'
    elif m == 12:
        return u'diciembre'
    else:
        return ''
    
def printContent(l, source=''):
    day0 = datetime.datetime.now().strftime('%Y-%m-%d')
    day1 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    day2 = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    
    day0_stuff = u""
    day1_stuff = u""
    day2_stuff = u""
    for ll in l:
        [updated, sitetitle, title, url] = ll
        if updated == day0:
            day0_stuff += u"* {{actualización|titular=%s|enlace=%s|fuente=%s|fecha=%s}}\n" % (title, url, sitetitle, updated)
        if updated == day1:
            day1_stuff += u"* {{actualización|titular=%s|enlace=%s|fuente=%s|fecha=%s}}\n" % (title, url, sitetitle, updated)
        if updated == day2:
            day2_stuff += u"* {{actualización|titular=%s|enlace=%s|fuente=%s|fecha=%s}}\n" % (title, url, sitetitle, updated)
    
    for k, v in [[day0, day0_stuff], [day1, day1_stuff], [day2, day2_stuff], ]:
        if v:
            page = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'15Mpedia:Actualizaciones/%s/%s' % (source, k))
            page.put(v, u"BOT - Añadiendo actualizaciones: %s [%d], %s [%d], %s [%d]" % (day0, len(re.findall(ur'\n', day0_stuff)), day1, len(re.findall(ur'\n', day1_stuff)), day2, len(re.findall(ur'\n', day2_stuff)), ))
    
def main():
    b = getBlogs()
    printContent(b, source='Blogs')
    #f = getFacebook()
    #fl = getFlickr()
    #n = getN1()
    y = getYouTube()
    printContent(y, source='YouTube')
    
if __name__ == '__main__':
    main()
