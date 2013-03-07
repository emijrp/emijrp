#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
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
    rss = raw.splitlines()
    return rss

def getBlogs():
    rss = getLines(u'Actualizaciones/Blogosfera (RSS)')
    print 'Loaded %d RSS for blogs' % (len(rss))
    
    content = []
    for url in rss:
        xml = uncode(urllib.urlopen(url).read())
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
            title = re.findall(ur"(?im)>([^<>]*?)</title>", chunk)[0]
            updated = re.findall(ur"(?im)>([^<>]*?)</updated>", chunk)[0]
            updated = updated.split('.')[0]
            url = re.findall(ur"(?im)<link rel='alternate' type='text/html' href='([^>]*?)' title='", chunk)[0]
            
            #print updated, title, url
            content.append([updated, sitetitle, title, url])

    content.sort(reverse=True)
    return content

def getFacebook():
    rss = getLines(u'Actualizaciones/Facebook (RSS)')
    print 'Loaded %d RSS for Facebook' % (len(rss))
    
    content = []
    for url in rss:
        xml = uncode(urllib.urlopen(url).read())
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
            published = published.split('+')[0]
            url = re.findall(ur'(?im)<link rel="alternate" type="text/html" href="([^>]*?)" />', chunk)[0]
            
            #print published, title, url
            content.append([published, sitetitle, title, url])

    content.sort(reverse=True)
    return content 

def getYouTube():
    rss = getLines(u'Actualizaciones/YouTube (RSS)')
    print 'Loaded %d RSS for YouTube' % (len(rss))
    
    content = []
    for url in rss:
        xml = uncode(urllib.urlopen(url).read())
        chunks = '</entry>'.join('<entry>'.join(xml.split('<entry>')[1:]).split('</entry>')[:-1]).split('</entry><entry>') #</entry><entry>
        
        sitetitle = u''
        if re.search(ur"(?im)>([^<>]*?)</name>", xml):
            sitetitle = re.findall(ur"(?im)>([^<>]*?)</name>", xml)[1] #el 0 es YouTube, el 1 el nombre del canal
        else:
            sitetitle = url
        
        for chunk in chunks:
            if not re.search(ur"(?im)</title>", chunk) or not re.search(ur"(?im)</published>", chunk):
                continue
        
            title = u'Sin título'
            title = re.findall(ur"(?im)>([^<>]*?)</title>", chunk)[0]
            published = re.findall(ur"(?im)>([^<>]*?)</published>", chunk)[0]
            published = published.split('.')[0]
            url = re.findall(ur"(?im)<link rel='alternate' type='text/html' href='([^>&]*?)&", chunk)[0]
            
            #print published, title, url
            content.append([published, sitetitle, title, url])

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

def convertToText(l):
    day = u''
    t = u''
    for updated, sitetitle, title, url in l[:100]:
        day2 = updated.split('T')[0]
        if day != day2:
            sectionday = u'== %d de %s ==\n' % (int(day2.split('-')[2]), getMonthName(int(day2.split('-')[1])))
            t += t and u'\n%s' % (sectionday) or u'%s' % (sectionday)
            day = day2
        t += u"* '''%s:''' [%s %s]\n" % (sitetitle, url, title)
    return t

def main():
    b = getBlogs()
    f = getFacebook()
    y = getYouTube()
    a = b + f + y
    a.sort(reverse=True)
    
    all = convertToText(a)
    blogosfera = convertToText(b)
    facebook = convertToText(f)
    twitter = u''#convertToText(f)
    youtube = convertToText(y)
    
    hv = [video[3].split('?v=')[1] for video in y[:3]]
    headervideos = u"""{|
| valign=top | {{youtube|%s|left}}
| valign=top | {{youtube|%s|left}}
| valign=top | {{youtube|%s|left}}
|}"""% (hv[0], hv[1], hv[2])

    output = u"""= Actualizaciones =

Estas son las últimas '''actualizaciones del 15M'''.
%s
{{twitter widget|#15M|height=400px}}
%s

= Blogosfera =

Estas son las últimas actualizaciones en la '''blogosfera del 15M'''.

%s

:''Para añadir un nuevo RSS entra en [[Actualizaciones/Blogosfera (RSS)]]''

= Facebook =

Estas son las últimas actualizaciones en las '''cuentas de Facebook del 15M'''.

%s

:''Para añadir un nuevo RSS entra en [[Actualizaciones/Facebook (RSS)]]''

= Twitter =

Estas son las últimas actualizaciones en las '''cuentas de Twitter del 15M'''.
{{twitter widget|#15M|height=400px}}
%s

= YouTube =

Estas son las últimas actualizaciones en los '''canales de YouTube del 15M'''.
%s
%s

:''Para añadir un nuevo RSS entra en [[Actualizaciones/YouTube (RSS)]]''

<headertabs/>
__NOTOC__ __NOEDITSECTION__
[[Categoría:15Mpedia]]
""" % (headervideos, all, blogosfera, facebook, twitter, headervideos, youtube)
    page = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'Actualizaciones')
    page.put(output, u"BOT - Añadiendo actualizaciones")

if __name__ == '__main__':
    main()
