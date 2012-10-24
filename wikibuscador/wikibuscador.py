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

from bz2 import BZ2File
from wmf import dump
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
        m = re.findall(ur"(?im)^==\s*Enlaces\s*externos\s*==", revtext)
        if m:
            #capturar enlaces externos
            ee = revtext.split(m[0])[1]
            m = re.findall(ur"(?im)\[\[\s*Categor", ee)
            if m:
                ee = ee.split(m[0])[0]
            enlaces = re.findall(ur"(?im)^\*+\s*\[\s*(https?://[^\s\[\]\|]+?)\s+([^\n\r\[\]\|]*?)\]", ee)
            
            #capturar FB, TW
            facebook = ''
            m = re.findall(ur"(?im)\{\{\s*(?:facebook|facebook user)([^\}]*?)\}\}", revtext)
            if m:
                param = m[0].strip()
                if param and param[0] == '|':
                    facebook = param.split('|')[1].strip()
                else:
                    facebook = pagetitle.strip()
            twitter = ''
            m = re.findall(ur"(?im)\{\{\s*(?:twitter)([^\}]*?)\}\}", revtext)
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
            #{{info}}
            m = re.findall(ur"(?im)\{\{\s*info\s*\|([^\{\}\[\]]*?)\}\}", revtext)
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
                        elif t.lower() == 'commons':
                            commons = pagetitle
                    elif len(t) == 2:
                        t = [t[0].strip(), t[1].strip()]
                        if t[0].lower() == 'wikiquote':
                            wikiquote = t[1]
                        elif t[0].lower() == 'wikcionario':
                            wikcionario = t[1]
                        elif t[0].lower() == 'wikinoticias':
                            wikinoticias = t[1]
                        elif t[0].lower() == 'commons':
                            commons = t[1]
            
            if not wikiquote:
                m = re.findall(ur"(?im)\{\{\s*(?:wikicitas?|wikiquote)([^\}]*?)\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        wikiquote = param.split('|')[1]
                    else:
                        wikiquote = pagetitle
            if not wikcionario:
                m = re.findall(ur"(?im)\{\{\s*(?:wikcionario|wiktionary|wikt|wiktionarypar)([^\}]*?)\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        wikcionario = param.split('|')[1]
                    else:
                        wikcionario = pagetitle
            if not wikinoticias:
                m = re.findall(ur"(?im)\{\{\s*(?:wikinoticiascat)([^\}]*?)\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        wikinoticias = u'Category:%s' % (param.split('|')[1])
                    else:
                        wikinoticias = u'Category:%s' % (pagetitle)
            if not commons:
                m = re.findall(ur"(?im)\{\{\s*(?:commons|commons-inline)([^\}]*?)\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        commons = param.split('|')[1]
                    else:
                        commons = pagetitle
            if not commons:
                m = re.findall(ur"(?im)\{\{\s*(?:commons ?cat|categoría ?commons|commonscat-inline|commons ?category)([^\}]*?)\}\}", revtext)
                if m:
                    param = m[0].strip()
                    if param and param[0] == '|':
                        commons = u'Category:%s' % (param.split('|')[1])
                    else:
                        commons = u'Category:%s' % (pagetitle)
            
            #capturar VT
            m = re.findall(ur"(?im)^==\s*V[eé]ase\s*tambi[eé]n\s*==", revtext)
            vt = ''
            if m:
                vt = revtext.split(m[0])[1]
                try:
                    vt = vt.split('==')[0]
                except:
                    pass
            sugerencias = re.findall(ur"(?im)^\*+\s*\[\[([^\|\]\:]{3,30})\]\]", vt)
            
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
            
            #capturar la mejor imagen
            images = re.findall(ur"(?im)(?:(?:Archivo|File|Image)\s*\:|(?:imagen?|foto|fotograf[íi]a)\s*=)\s*([^\|\[\]]+?\.(?:jpe?g))", revtext)
            selectedimage = ''
            if images:
                selectedimage = images[0]
            gallery = ''
            if len(images) > 1:
                gallery = u'<gallery>\n%s\n</gallery>' % (u'\n'.join([u'Archivo:%s' % (image) for image in images[1:6]]))
            
            limit1 = 3
            limit2 = 7
            limit3 = 50
            resultados1 = u''.join([u'{{Resultado1\n|url=%s\n|formato=Autodetectar\n|título=%s\n|descripción=%s\n}}' % (enlace, '', clean(desc)) for enlace, desc in enlaces[:limit1]])
            resultados2 = u''
            resultados3 = u''
            if len(enlaces) > limit1:
                resultados2 = u''.join([u'{{Resultado2\n|url=%s\n|formato=Autodetectar\n|título=%s\n|descripción=%s\n}}' % (enlace, '', clean(desc)) for enlace, desc in enlaces[limit1:limit1+limit2+1]])
            if len(enlaces) > limit1+limit2:
                resultados3 = u''.join([u'{{Resultado3\n|url=%s\n|formato=Autodetectar\n|título=%s\n|descripción=%s\n}}' % (enlace, '', clean(desc)) for enlace, desc in enlaces[limit1+limit2+1:limit1+limit2+limit3+1]])
            
            resultados = u''
            output = u"""{{Infobox Resultado
|introducción=%s
|imagen=%s
|pie de imagen=
|wikipedia=%s%s%s%s
|sugerencias=%s%s%s
|galería=%s
|resultados1=%s
|resultados2=%s
|resultados3=%s
}}""" % (abstract, selectedimage, pagetitle, wikcionario and u'\n|wikcionario=%s' % (wikcionario) or '', wikiquote and u'\n|wikicitas=%s' % (wikiquote) or '', commons and u'\n|commons=%s' % (commons) or '', ', '.join(sugerencias), facebook and u'\n|facebook=%s' % (facebook) or '', twitter and u'\n|twitter=%s' % (twitter) or '', gallery, resultados1, resultados2, resultados3)
            if len(abstract)>100 and len(enlaces) >= limit1:
                #salida
                print '-'*50
                print page.getId(), pagetitle, len(enlaces)
                print '-'*50
                print output
                p = wikipedia.Page(wikipedia.Site('todogratix', 'todogratix'), pagetitle)
                p.put(output, output)
        break
