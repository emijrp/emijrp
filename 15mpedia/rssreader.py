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
        if url.startswith('http://a'):
            break

        try:
            xml = uncode(urllib.urlopen(url).read())
        except:
            continue
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
            published = published.split('+')[0]
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
    rss = getLines(u'Actualizaciones/YouTube (RSS)')
    print 'Loaded %d RSS for YouTube' % (len(rss))
    
    content = []
    for url in rss:
        try:
            xml = uncode(urllib.urlopen(url).read())
        except:
            continue
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

def convertToTextCore(sitetitle, buff):
    t = u''
    if len(buff) > 1:
        t += u"\n* '''%s:'''\n" % (sitetitle)
        for lbuff in buff:
            [lupdated, lsitetitle, ltitle, lurl] = lbuff
            t += u"** [%s %s]\n" % (lurl, re.sub(ur"[\[\]]", ur"", ltitle and ltitle or u'Sin título'))
    else:
        lbuff = buff[0]
        [lupdated, lsitetitle, ltitle, lurl] = lbuff
        t += u"\n* [%s %s]\n" % (lurl, re.sub(ur"[\[\]]", ur"", ltitle and ltitle or u'Sin título'))
    return t
    
def convertToText(l):
    day = u''
    sitetitle = u''
    t = u''
    buff = []
    for ll in l[:200]:
        [updated, sitetitle2, title, url] = ll
        day2 = updated.split('T')[0]
        if day != day2:
            sectionday = u'== %d de %s ==\n' % (int(day2.split('-')[2]), getMonthName(int(day2.split('-')[1])))
            t += t and u'\n%s' % (sectionday) or u'%s' % (sectionday)
            day = day2
        if buff and sitetitle != sitetitle2:
            t += convertToTextCore(sitetitle, buff)
            sitetitle = sitetitle2
            buff = []
        buff.append(ll)
    if buff:
        t += convertToTextCore(sitetitle, buff)
    return t

def main():
    b = getBlogs()
    f = getFacebook()
    fl = getFlickr()
    n = getN1()
    y = getYouTube()
    a = b + f + fl + n + y
    a.sort(reverse=True)
    
    all = convertToText(a)
    blogosfera = convertToText(b)
    facebook = convertToText(f)
    flickr = u'En desarrollo...'#convertToText(fl)
    n1 = u'En desarrollo...'#convertToText(n)
    twitter = u'En desarrollo...'#convertToText(t)
    youtube = convertToText(y)
    
    #print blogosfera
    
    hv = [video[3].split('?v=')[1] for video in y[:3]]
    headervideos = u"""<center>
{|
| valign=top | {{youtube|%s|left}}
| valign=top | {{youtube|%s|left}}
| valign=top | {{youtube|%s|left}}
|}
</center>"""% (hv[0], hv[1], hv[2])

    output = u"""= Actualizaciones =

Estas son las últimas '''actualizaciones'''.
%s
{{twitter widget|#15M|height=400}}
%s

= Blogosfera =

Estas son las últimas actualizaciones en la '''blogosfera'''.

%s

:''Para añadir un nuevo RSS entra en [[Actualizaciones/Blogosfera (RSS)]]''

= Facebook =

Estas son las últimas actualizaciones en las '''cuentas de Facebook'''.

%s

:''Para añadir un nuevo RSS entra en [[Actualizaciones/Facebook (RSS)]]''

= Flickr =

Estas son las últimas actualizaciones en las '''cuentas de Flickr'''.

%s

:''Para añadir un nuevo RSS entra en [[Actualizaciones/Flickr (RSS)]]''

= n-1 =

Estas son las últimas actualizaciones en '''n-1'''.

%s

= Twitter =

Estas son las últimas actualizaciones en las '''cuentas de Twitter'''.
{{twitter widget|#15M|height=400}}
%s

= YouTube =

Estas son las últimas actualizaciones en los '''canales de YouTube'''.
%s
%s

:''Para añadir un nuevo RSS entra en [[Actualizaciones/YouTube (RSS)]]''

<headertabs/>
__NOTOC__ __NOEDITSECTION__
[[Categoría:15Mpedia]]
""" % (headervideos, all, blogosfera, facebook, flickr, n1, twitter, headervideos, youtube)
    page = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'Actualizaciones')
    page.put(output, u"BOT - Añadiendo actualizaciones")

if __name__ == '__main__':
    main()
