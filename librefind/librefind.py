# -*- coding: utf-8 -*-

# Copyright (C) 2012-2013 emijrp <emijrp@gmail.com>
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

from bz2 import BZ2File
from wmf import dump #https://bitbucket.org/halfak/wikimedia-utilities/wiki/Home
import re
import time
import sys
import wikipedia

def clean(s):
    s = re.sub(ur"\'{2,5}", ur"", s)
    return s

def compensatehtmlcomments(s):
    if len(re.findall(ur"<!--", s)) > len(re.findall(ur"-->", s)):
        s += u'-->'
    return s

def removebr(s):
    s = re.sub(ur"(?im)<\s*/\s*br\s*/?\s*>", ur"", s)
    s = re.sub(ur"(?im)<\s*/\s*br\s*clear\s*=\s*[\"\']\s*all\s*[\"\']\s*/?\s*>", ur"", s)
    return s

def removehtmlcomments(s):
    s = re.sub(ur"<!--.*?-->", ur"", s)
    return s

def hidetemplates(s):
    s = re.sub(ur"(?im)(\{\{[^\{\}]*?\}\})", ur"<!-- \1 -->", s)
    return s

def removerefs(s):
    s = re.sub(ur"(?im)<ref[^<>]*>[^<>]*?</ref>", ur"", s)
    s = re.sub(ur"(?im)<ref[^<>]*>", ur"", s)
    return s

def removeanexo(s):
    s = re.sub(ur"(?im)\[\[Anexo:", ur"[[", s)
    return s

commonssite = wikipedia.Site('commons', 'commons')
path = sys.argv[1]
skip = ''
if len(sys.argv) > 2:
    skip = re.sub('_', ' ', sys.argv[2])
    print 'Skiping until', skip
if path.endswith('.bz2'):
    import bz2
    source = bz2.BZ2File(path)
elif path.endswith('.gz'):
    import gzip
    source = gzip.open(path)
elif path.endswith('.7z'):
    import subprocess
    source = subprocess.Popen('7za e -bd -so %s 2>/dev/null' % path, shell=True, stdout=subprocess.PIPE, bufsize=65535).stdout
else:
    # assume it's an uncompressed XML file
    source = open(self.filename)

dumpIterator = dump.Iterator(source)
t1 = time.time()
cpages = 0
crevs = 0
totalrevs = 0
for page in dumpIterator.readPages():
    #page.getId(), page.getTitle(), page.readRevisions()
    #rev.getId(), rev.getParentId(), rev.getTimestamp(), rev.getContributor(), rev.getMinor(), rev.getComment(), rev.getText(), rev.getSha1()
    pagetitle = page.getTitle()
    if skip:
        if pagetitle == skip:
            skip = ''
        else:
            continue
    
    if ':' in pagetitle:
        continue
    for revision in page.readRevisions():
        revtext = revision.getText()
        m = re.findall(ur"(?im)^==\s*(?:External\s*links|(?:Enlaces|Links)\s*externos)\s*==", revtext)
        if m:
            #capturar enlaces externos
            ee = revtext.split(m[0])[1]
            m = re.findall(ur"(?im)\[\[\s*Categor", ee)
            if m:
                ee = ee.split(m[0])[0]
            enlaces = re.findall(ur"(?im)^\*+\s*\'*\s*\[\s*(https?://[^\s\[\]\|]+?)\s+([^\n\r\[\]\|]*?)\]", ee)
            
            #capturar FB, TW
            facebook = ''
            m = re.findall(ur"(?im)\{\{\s*(?:facebook|facebook\.com|facebook[ _]?user)([^\}]*?)\}\}", revtext)
            if m:
                param = m[0].strip()
                if param and param[0] == '|':
                    facebook = param.split('|')[1].strip()
                else:
                    facebook = pagetitle.strip()
            twitter = ''
            m = re.findall(ur"(?im)\{\{\s*(?:twitter|twitter\.com)([^\}]*?)\}\}", revtext)
            if m:
                param = m[0].strip()
                if param and param[0] == '|':
                    twitter = param.split('|')[1].strip().lstrip('@')
                else:
                    twitter = pagetitle.strip()
            
            #capturar web oficial
            weboficial = ''
            m = re.findall(ur"(?im)\{\{\s*(?:web ?oficial|official|official ?website)([^\}]*?)\}\}", revtext)
            if m:
                param = m[0].strip()
                if param and param[0] == '|':
                    weboficial = param.split('|')[1]
            
            #capturar enlaces a proyectos hermanos
            wikiquote = ''
            wikcionario = ''
            wikinoticias = ''
            commons = ''
            wikiversity = ''
            wikisource = ''
            wikibooks = ''
            wikispecies = ''
            #{{info}}
            m = re.findall(ur"(?im)\{\{\s*(?:info|sister[ _]project[ _]links)\s*\|([^\{\}\[\]]*?)\}\}", revtext)
            if m:
                tt = [t.split('=') for t in [t.strip() for t in m[0].strip().split('|')]]
                for t in tt:
                    if len(t) == 1:
                        t = t[0].strip()
                        if t.lower() == 'q':
                            wikiquote = pagetitle
                        elif t.lower() == 'wikt':
                            wikcionario = pagetitle
                        elif t.lower() == 'n':
                            wikinoticias = pagetitle
                        elif t.lower() == 'b':
                            wikibooks = pagetitle
                        elif t.lower() == 's':
                            wikisource = pagetitle
                        elif t.lower() == 'v':
                            wikiversity = pagetitle
                        elif t.lower() == 'commons':
                            commons = pagetitle
                    elif len(t) == 2:
                        t = [t[0].strip(), t[1].strip()]
                        if t[1].lower() != 'no':
                            if t[0].lower() in ['wikiquote', 'q']:
                                wikiquote = t[1] and t[1] or pagetitle
                            elif t[0].lower() in ['wikcionario', 'wiktionary', 'wikt']:
                                wikcionario = t[1] and t[1].lower() != 'no' and t[1] or pagetitle
                            elif t[0].lower() in ['wikinoticias', 'n', 'wikinews']:
                                wikinoticias = t[1] and t[1].lower() != 'no' and t[1] or pagetitle
                            elif t[0].lower() in ['wikibooks', 'b']:
                                wikibooks = t[1] and t[1].lower() != 'no' and t[1] or pagetitle
                            elif t[0].lower() in ['wikisource', 's']:
                                wikisource = t[1] and t[1].lower() != 'no' and t[1] or pagetitle
                            elif t[0].lower() in ['wikiversity', 'v']:
                                wikiversity = t[1] and t[1].lower() != 'no' and t[1] or pagetitle
                            elif t[0].lower() in ['commons']:
                                commons = t[1] and t[1] or pagetitle
            
            if not wikiquote:
                m = re.findall(ur"(?im)\{\{\s*(?:wikicitas?|wikiquote|wikiquote-inline)\s*([^\}]*?)\s*\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        wikiquote = param.split('|')[1]
                    else:
                        wikiquote = pagetitle
            if not wikcionario:
                m = re.findall(ur"(?im)\{\{\s*(?:wikcionario|wiktionary|wikt|wiktionarypar|wiktionary-inline)\s*([^\}]*?)\s*\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        wikcionario = param.split('|')[1]
                    else:
                        wikcionario = pagetitle
            if not wikinoticias:
                m = re.findall(ur"(?im)\{\{\s*(?:wikinoticiascat|wikinews[ _]?category)\s*([^\}]*?)\s*\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        wikinoticias = u'Category:%s' % (param.split('|')[1])
                    else:
                        wikinoticias = u'Category:%s' % (pagetitle)
            if not commons:
                m = re.findall(ur"(?im)\{\{\s*(?:commons|commons-inline)\s*([^\}]*?)\s*\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        commons = param.split('|')[1]
                    else:
                        commons = pagetitle
            if not commons:
                m = re.findall(ur"(?im)\{\{\s*(?:commons[ _]?cat|categoría[ _]?commons|commonscat-inline|commons[ _]?category)\s*([^\}]*?)\s*\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        commons = u'Category:%s' % (param.split('|')[1])
                    else:
                        commons = u'Category:%s' % (pagetitle)
            if not wikiversity:
                m = re.findall(ur"(?im)\{\{\s*(?:wikiversity|wikiversity-inline)\s*([^\}]*?)\s*\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        wikiversity = param.split('|')[1]
                    else:
                        wikiversity = pagetitle
            if not wikisource:
                m = re.findall(ur"(?im)\{\{\s*(?:wikisource|wikisource-inline)\s*([^\}]*?)\s*\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        wikisource = param.split('|')[1]
                    else:
                        wikisource = pagetitle
            if not wikispecies:
                m = re.findall(ur"(?im)\{\{\s*(?:wikispecies|wikispecies-inline)\s*([^\}]*?)\s*\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        wikispecies = param.split('|')[1]
                    else:
                        wikispecies = pagetitle
            if not wikibooks:
                m = re.findall(ur"(?im)\{\{\s*(?:wikibooks|wikibooks-inline)\s*([^\}]*?)\s*\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        wikibooks = param.split('|')[1]
                    else:
                        wikibooks = pagetitle
            
            #capturar VT
            m = re.findall(ur"(?im)^==\s*(?:See\s*also|V[eé]ase\s*tambi[eé]n)\s*==", revtext)
            vt = ''
            if m:
                vt = revtext.split(m[0])[1]
                try:
                    vt = vt.split('==')[0]
                except:
                    pass
            sugerencias = re.findall(ur"(?im)^\*+\s*\[\[([^\|\]\:]{3,30})\]\]", vt)
            s = []
            for sugerencia in sugerencias:
                if not sugerencia.lower().startswith(u'list') and not sugerencia.lower().startswith(u'outline'):
                    s.append(sugerencia.strip())
            sugerencias = s
            
            #capturar abstract
            abstract = ''
            for l in hidetemplates(removehtmlcomments(removerefs(removebr(removeanexo(revtext))))).split('\n'):
                l = l.strip()
                if l:
                    if l[0] in [';', ':', '|', '{', '}', '<', '[', ']', '!', '#', '*', ' ']:
                        continue
                    else:
                        if pagetitle.lower() in l.lower():
                            abstract = compensatehtmlcomments(l)
                            break
            
            #capturar imagenes
            images = re.findall(ur"(?im)(?:(?:Archivo|File|Image)\s*\:|(?:image[ _]?skyline|picture|photo|photography|imagen?|foto|fotograf[íi]a)\s*=)\s*([^\|\[\]]+?\.(?:jpe?g))", revtext)
            selectedimage = ''
            caption = ''
            if images and images[0]:
                selectedimage = images[0]
                commonspage = wikipedia.Page(commonssite, u'File:%s' % (selectedimage))
                try:
                    if commonspage.exists():
                        caption = revtext.split(selectedimage)[1].strip()
                        if caption.startswith('|thumb') or caption.startswith('|left') or caption.startswith('|right'):
                            m = re.findall(ur'(?im)^\s*\|\s*(?:thumb|thumbnail|frame|(?:(?:up)?(?:left|right|center)(?:\s*=?\s*\d*\.?\d*)?))([^\[\]]*?)\]\]', caption)
                            if m:
                                caption = m[0].strip().lstrip('|')
                            else:
                                brackets = 2
                                c = 0
                                while len(caption) > c and c <= 500 and brackets != 0:
                                    if caption[c] == '[':
                                        brackets += 1
                                    elif caption[c] == ']':
                                        brackets -= 1
                                    c += 1
                                if brackets == 0:
                                    caption = caption[:c-2]
                                else:
                                    caption = u''
                        else:
                            caption = u''
                except:
                    pass
            caption = re.sub(ur"(((up)?(right|center|left)(\s*=?\s*\d+\.?\d*)?)|thumb|thumbnail|frame|\d+ *px)\s*\|", ur"", caption)
            caption = hidetemplates(removerefs(caption.strip().lstrip('|'))).strip().lstrip('|')
            if re.search(ur'alt *=', caption) or len(caption)>500:
                caption = u''
            
            gallery = ''
            images = list(set(images))
            if len(images) > 1:
                gallery = u'<gallery>\n%s\n</gallery>' % (u'\n'.join([u'File:%s' % (image) for image in images[1:6]]))
            
            limit1 = 3
            limit2 = 7
            limit3 = 50
            resultados1 = u''.join([u'{{Result1\n|url=%s\n|format=auto\n|description=%s\n}}' % (enlace, clean(desc)) for enlace, desc in enlaces[:limit1]])
            resultados2 = u''
            resultados3 = u''
            if len(enlaces) > limit1:
                resultados2 = u''.join([u'{{Result2\n|url=%s\n|format=auto\n|description=%s\n}}' % (enlace, clean(desc)) for enlace, desc in enlaces[limit1:limit1+limit2+1]])
            if len(enlaces) > limit1+limit2:
                resultados3 = u''.join([u'{{Result3\n|url=%s\n|format=auto\n|description=%s\n}}' % (enlace, clean(desc)) for enlace, desc in enlaces[limit1+limit2+1:limit1+limit2+limit3+1]])
            
            resultados = u''
            output = u"""{{Infobox Result
|introduction=%s
|image=%s
|caption=%s
|wikipedia=%s%s%s%s%s%s%s%s
|related=%s%s%s
|gallery=%s
|results1=%s
|results2=%s
|results3=%s
}}""" % (abstract, selectedimage, caption, pagetitle, wikcionario and u'\n|wiktionary=%s' % (wikcionario) or '', wikiquote and u'\n|wikiquote=%s' % (wikiquote) or '', wikibooks and u'\n|wikibooks=%s' % (wikibooks) or '', wikiversity and u'\n|wikiversity=%s' % (wikiversity) or '', wikisource and u'\n|wikisource=%s' % (wikisource) or '', wikispecies and u'\n|wikispecies=%s' % (wikispecies) or '', commons and u'\n|commons=%s' % (commons) or '', ', '.join(sugerencias), facebook and u'\n|facebook=%s' % (facebook) or '', twitter and u'\n|twitter=%s' % (twitter) or '', gallery, resultados1, resultados2, resultados3)
            if len(abstract)>100 and len(enlaces) >= limit1 and caption:
                #salida
                print '-'*50
                print page.getId(), pagetitle, len(enlaces)
                print '-'*50
                
                print output
                p = wikipedia.Page(wikipedia.Site('librefind', 'librefind'), pagetitle)
                p.put(output, output)
        break
