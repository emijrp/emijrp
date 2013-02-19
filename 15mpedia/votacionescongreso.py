#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import string
import wikipedia
import zipfile

parlamento = u'Congreso de los Diputados'
l = '10'
s = '4'
url = 'http://www.congreso.es/votaciones/OpenData?sesion=%s&completa=1&legislatura=%s' % (s, l)
zipname = 'l%ss%s.zip' % (l, s)
#os.system('wget -c "%s" -O %s' % (url, zipname))

zipfile = zipfile.ZipFile(zipname)
for zipp in zipfile.namelist():
    xmlraw = unicode(zipfile.read(zipp), 'ISO-8859-1')
    #print xmlraw

    legislatura = u''
    if l == '10':
        legislatura = u'X Legislatura'
    else:
        print 'Error legislatura'
        break
    
    sesion = re.findall(ur"(?im)<sesion>(\d+)</sesion>", xmlraw)[0]
    numero = re.findall(ur"(?im)<numerovotacion>(\d+)</numerovotacion>", xmlraw)[0]
    fecha = re.findall(ur"(?im)<fecha>([^<]+)</fecha>", xmlraw)[0]
    fecha = u'%s-%s-%s' % (fecha.split('/')[2], '%02d' % (int(fecha.split('/')[1])), '%02d' % (int(fecha.split('/')[0])))
    titulo = re.search(ur"(?im)<titulo>", xmlraw) and re.findall(ur"(?im)<titulo>([^<]+)</titulo>", xmlraw)[0] or u''
    textoexp = re.search(ur"(?im)<textoexpediente>", xmlraw) and re.findall(ur"(?im)<textoexpediente>([^<]+)</textoexpediente>", xmlraw)[0] or u''
    titulosub = re.search(ur"(?im)<titulosubgrupo>", xmlraw) and re.findall(ur"(?im)<titulosubgrupo>([^<]+)</titulosubgrupo>", xmlraw)[0] or u''
    textosub = re.search(ur"(?im)<textosubgrupo>", xmlraw) and re.findall(ur"(?im)<textosubgrupo>([^<]+)</textosubgrupo>", xmlraw)[0] or u''
    
    print sesion, numero, fecha

    asentimiento = re.search(ur"(?im)<asentimiento>", xmlraw) and re.findall(ur"(?im)<asentimiento>([^<]+)</asentimiento>", xmlraw)[0] or u''
    presentes = re.search(ur"(?im)<presentes>", xmlraw) and re.findall(ur"(?im)<presentes>([^<]+)</presentes>", xmlraw)[0] or u''
    afavor = re.search(ur"(?im)<afavor>", xmlraw) and re.findall(ur"(?im)<afavor>([^<]+)</afavor>", xmlraw)[0] or u''
    encontra = re.search(ur"(?im)<encontra>", xmlraw) and re.findall(ur"(?im)<encontra>([^<]+)</encontra>", xmlraw)[0] or u''
    abstenciones = re.search(ur"(?im)<abstenciones>", xmlraw) and re.findall(ur"(?im)<abstenciones>([^<]+)</abstenciones>", xmlraw)[0] or u''
    novotan = re.search(ur"(?im)<novotan>", xmlraw) and re.findall(ur"(?im)<novotan>([^<]+)</novotan>", xmlraw)[0] or u''
    
    print asentimiento, presentes, afavor, encontra, abstenciones, novotan
    
    votosraw = re.search(ur"(?im)<votaciones>", xmlraw) and re.findall(ur"(?im)<votacion>\s*<asiento>([^<]+)</asiento>\s*<diputado>([^<]+)</diputado>\s*<voto>([^<]+)</voto>\s*</votacion>", xmlraw) or []
    votos = u''
    for asiento, votante, voto in votosraw:
        votos += u'{{votación voto|parlamento=%s|legislatura=%s|sesión=%s|número=%s|asiento=%s|votante=%s|voto=%s}}\n' % (parlamento, legislatura, sesion, numero, asiento, votante, voto)
    #print votos
    
    output = string.Template(u"""{{Votación información
|parlamento=$parlamento
|legislatura=$legislatura
|sesión=$sesion
|número=$numero
|fecha=$fecha
|título=$titulo
|texto expediente=$textoexp
|título subgrupo=$titulosub
|texto subgrupo=$textosub
}}

{{Votación totales
|asentimiento=$asentimiento
|presentes=$presentes
|a favor=$afavor
|en contra=$encontra
|abstenciones=$abstenciones
|no votan=$novotan
}}
<noinclude>
{{votación votos inicio}}
%s
{{votación votos fin}}

== Enlaces externos ==
* {{votaciones congreso xml|legislatura=$legislatura|sesión=$sesion}}
</noinclude>""")
    print output%{'parlamento':parlamento, 'legislatura':legislatura, 'sesion':sesion, 'numero':numero, 'fecha':fecha, 'titulo':titulo, 'textoexp':textoexp, 'titulosub':titulosub, 'textosub':textosub, 'asentimiento':asentimiento, 'presentes':presentes, 'afavor':afavor, 'encontra':encontra, 'abstenciones':abstenciones, 'novotan':novotan, 'votos':votos, }
    
    
