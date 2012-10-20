#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

import catlib
import pagegenerators
import wikipedia

def formatnum(n):
    n = n.strip()
    n = re.sub(ur"(?im)\.([0-9]{1,2})$", ur",\1", n)
    n = re.sub(ur"\.", ur"", n)
    n = re.sub(ur",", ur".", n)
    return n

start = u'!'
if len(sys.argv) > 1:
    start = sys.argv[1]

#hechos: Almería, 
provincias = [u'Granada'] #, u'Huelva', u'Jaén', u'Málaga', u'Sevilla'] #córdoba tiene (España), moficiar la intro localizacion
ccaa = u'Andalucía'
sitetg = wikipedia.Site('todogratix', 'todogratix')
sitees = wikipedia.Site('es', 'wikipedia')

for provincia in provincias:
    category = catlib.Category(title=u"Categoría:Municipios de la provincia de %s" % (provincia), site=sitees)
    gen = pagegenerators.CategorizedPageGenerator(category, recurse=False, start=start)
    pre = pagegenerators.PreloadingGenerator(gen)

    localizacion = [u"Provincia de %s" % (provincia), ccaa, u"España"]

    #load poblacion
    pagepob = wikipedia.Page(sitees, u"Plantilla:Población municipios de España")
    m = re.findall(ur"(?im)\|(\d+)=(\d+)", pagepob.get())
    pob = {}
    for i in m:
        pob[i[0]] = re.sub(ur"[,\.]", ur"", i[1])
        #print i[0], i[1]

    for page in pre:
        if page.exists() and not page.isRedirectPage() and page.namespace() == 0 and re.search(ur"\{\{\s*Ficha de localidad de España", page.get()):
            print page.title()
            props = {'title': page.title(), 'nombre': '', 'escudo': '', 'bandera': '', 'imagen': '', 'pie': '', 'cod_provincia': '', 'cod_municipio': '', 'coord': '', 'localizacion': '', 'altitud': '', 'superficie': '', 'pob': '', 'anyopob': '', 'gentilicio': '', 'cp': '', 'alcalde': '', 'partido': '', 'patron': '', 'patrona': '', 'web': '', 'latd': 0, 'latm': 0, 'lats': 0, 'latns': '', 'longd': 0, 'longm': 0, 'longs': 0, 'longew': ''}
            m = re.findall(ur"(?im)(cod[ _]provincia|cod[ _]municipio|escudo|bandera|nombre|imagen|pie[ _]de[ _]imagen|superficie|altitud|gentilicio|cp|alcalde|patr[óo]n|patrona|sitio[ _]web|web|latd|latm|latNS|longd|longm|longEW)\s*=\s*([^\<\n\r\|]*?)\s*[\<\n\r\|]", page.get())
            print m
            for i in m:
                if i[0].lower() == 'nombre' and not props['nombre']:
                    props['nombre'] = i[1].strip()
                elif i[0].lower() == 'escudo' and not props['escudo']:
                    props['escudo'] = i[1].strip() != 'no' and i[1].strip() or ''
                elif i[0].lower() == 'bandera' and not props['bandera']:
                    props['bandera'] = i[1].strip() != 'no' and i[1].strip() or ''
                elif i[0].lower() == 'imagen' and not props['imagen']:
                    try:
                        props['imagen'] = i[1].split(':')[1].split('|')[0].strip()
                    except:
                        props['imagen'] = ''
                elif i[0].lower() in ['pie de imagen', 'pie_de_image'] and not props['pie']:
                    props['pie'] = i[1].strip()
                elif i[0].lower() in ['cod_provincia', 'cod provincia'] and not props['cod_provincia']:
                    props['cod_provincia'] = i[1].strip()
                elif i[0].lower() in ['cod_municipio', 'cod municipio'] and not props['cod_municipio']:
                    props['cod_municipio'] = i[1].strip()
                elif i[0].lower() == 'superficie' and not props['superficie']:
                    props['superficie'] = formatnum(i[1].strip())
                elif i[0].lower() == 'altitud' and not props['altitud']:
                    props['altitud'] = formatnum(i[1].strip())
                elif i[0].lower() == 'gentilicio' and not props['gentilicio']:
                    props['gentilicio'] = i[1].lower().strip() #i[1].split(',')[0].strip().split('<')[0].strip()
                elif i[0].lower() == 'cp' and not props['cp']:
                    props['cp'] = i[1].strip()
                    if re.search(ur"[^0-9\.]", props['cp']):
                        props['cp'] = ''
                elif i[0].lower() in [u'patrón', u'patron'] and not props['patron']:
                    t = re.sub(ur"\[\[([^\|\]]+)\|[^\]]+\]\]", ur"\1", i[1])
                    t = re.sub(ur"[\[\]]", ur"", t)
                    props['patron'] = t.strip()
                elif i[0].lower() == 'patrona' and not props['patrona']:
                    t = re.sub(ur"\[\[([^\|\]]+)\|[^\]]+\]\]", ur"\1", i[1])
                    t = re.sub(ur"[\[\]]", ur"", t)
                    props['patrona'] = t.strip()
                elif i[0].lower() == 'alcalde' and not props['alcalde'] and not props['partido']:
                    t = re.sub(ur"\[\[([^\|\]]+)\|[^\]]+\]\]", ur"\1", i[1])
                    t = re.sub(ur"[\[\]]", ur"", t)
                    if re.search(ur"\(", t):
                        props['alcalde'] = t.split('(')[0].strip()
                        props['partido'] = t.split('(')[1].strip()
                        if props['partido'][-1] == ')':
                            props['partido'] = props['partido'][:-1]
                    else:
                        props['alcalde'] = t.strip()
                        props['partido'] = ''
                    if props['partido'] == 'IU':
                        props['partido'] = 'Izquierda Unida'
                    elif props['partido'] == 'PP':
                        props['partido'] = 'Partido Popular'
                    elif props['partido'] == 'PSOE':
                        props['partido'] = u'Partido Socialista Obrero Español'
                elif i[0].lower() in ['web', 'sitio_web', 'sitio web'] and not props['web']:
                    props['web'] = re.findall(ur"(https?://[^/ ]+)", i[1]) and re.findall(ur"(https?://[^/ ]+)", i[1])[0].strip() or ''
                elif i[0].lower() == 'latd' and not props['latd']:
                    props['latd'] = i[1].strip()
                elif i[0].lower() == 'latm' and not props['latm']:
                    props['latm'] = i[1].strip()
                elif i[0].lower() == 'lats' and not props['lats']:
                    props['lats'] = i[1].strip()
                elif i[0].lower() == 'latns' and not props['latns']:
                    props['latns'] = i[1].strip()
                elif i[0].lower() == 'longd' and not props['longd']:
                    props['longd'] = i[1].strip()
                elif i[0].lower() == 'longm' and not props['longm']:
                    props['longm'] = i[1].strip()
                elif i[0].lower() == 'longs' and not props['longs']:
                    props['longs'] = i[1].strip()
                elif i[0].lower() == 'longew' and not props['longew']:
                    props['longew'] = i[1].strip()
                
            #localización
            props['localizacion'] = localizacion
            if props['cod_provincia'] and props['cod_municipio']:
                if pob.has_key('%s%s' % (props['cod_provincia'], props['cod_municipio'])):
                    props['pob'] = pob['%s%s' % (props['cod_provincia'], props['cod_municipio'])]
                else:
                    continue
            else:
                print props['cod_provincia'], props['cod_municipio']
                sys.exit()
            props['anyopob'] = 2011
            props['coord'] = '%f, %f'% (abs(float(props['latd'])+float(props['latm'])/60+float(props['lats'])/3600)*int((props['latns'].lower() in ['n', ''] and '1' or '-1')), abs(float(props['longd'])+float(props['longm'])/60+float(props['longs'])/3600)*int((props['longew'].lower() in ['e', ''] and '1' or '-1')))
            
            print props.items()
            output = u"""{{Infobox Ciudad
|nombre=%s
|escudo=%s
|bandera=%s
|imagen=%s
|pie de imagen=%s
|coordenadas=%s
|localización=%s
|altitud=%s
|superficie=%s
|población=%s
|año de población=%s
|gentilicio=%s
|código postal=%s
|alcalde=%s
|partido gobernante=%s
|patrón=%s
|patrona=%s
|web=%s
|wikipedia=%s
}}
""" % (props['nombre'], props['escudo'], props['bandera'], props['imagen'], props['pie'], props['coord'], ', '.join(props['localizacion']), props['altitud'], props['superficie'], props['pob'], props['anyopob'], props['gentilicio'], props['cp'], props['alcalde'], props['partido'], props['patron'], props['patrona'], props['web'], props['title'])
            print output
            
            tgpage = wikipedia.Page(sitetg, props['title'])
            #if not tgpage.exists():
            tgpage.put(output, u"BOT - Importando metadatos desde Wikipedia en español http://es.wikipedia.org/wiki/%s" % (re.sub(ur" ", ur"_", props['title'])))
