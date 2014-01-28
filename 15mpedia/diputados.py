#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re
import time
import wikipedia

site = wikipedia.Site('15mpedia', '15mpedia')
f = open('diputados.json', 'r')
raw = f.read()
f.close()
j = json.loads(raw)

for diputado in j["objects"]:
	"""
	"avatar": "http://www.congreso.es/wc/htdocs/web/img/diputados/79_10.jpg",
	"congress_id": "79",
	"congress_web": "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/DiputadosLegFechas?_piref73_2496079_73_2496068_2496068.next_page=%2Fwc%2FfichaDiputado&idDiputado=79",
	"division": "Salamanca",
	"email": "jesus.caldera@congreso.es",
	"id": 54,
	"inscription_date": "2011-11-29",
	"name": "Jesús",
	"resource_uri": "/api/v1/member/54/",
	"second_name": "Caldera Sánchez-Capitán",
	"termination_date": null,
	"twitter": "https://twitter.com/jcalderac",
	"validate": true,
	"web": ""
    """
	legislaturaid = 10
	summary = u"BOT - Añadiendo datos de [[Proyecto Colibrí]]: "
	nombre = u'%s %s' % (diputado['name'], diputado['second_name'], )
	print '-'*50
	print nombre
	print '-'*50
	p = wikipedia.Page(site, nombre)
	if p.exists():
		if p.isRedirectPage():
			p = p.getRedirectTarget()
		wtext = p.get()
		newtext = wtext
		
		#rellenar datos
		if not re.search(ur"(?im){{resumen votaciones}}", newtext):
			print "no tiene {{resumen votaciones}}"
			newtext = re.sub(ur"(?im)(== Declaraciones ==[^=]*)==", ur"\1== Votaciones ==\n{{resumen votaciones}}\n\n==", newtext)
		
		if nombre and not re.search(ur"(?im)\|nombre=", newtext):
			print "no tiene |nombre="
			newtext = re.sub(ur"{{Infobox Persona", ur"{{Infobox Persona\n|nombre=%s" % (nombre), newtext)
			summary += u'%s; ' % nombre
		
		if diputado['congress_id'] and not re.search(ur"(?im){{ficha congreso", newtext):
			print "no tiene {{ficha congreso"
			if re.search(ur"(?im){{wikipedia", newtext):
				newtext = re.sub(ur"(?im)(\*\s*{{wikipedia[^}]*}}\n)", ur"\1* {{ficha congreso|legislatura=%s|diputado=%s}}\n" % (legislaturaid, diputado['congress_id']), newtext)
			else:
				newtext = re.sub(ur"(?im)(==\s*Enlaces externos\s*==\n)", ur"\1* {{ficha congreso|legislatura=%s|diputado=%s}}\n" % (legislaturaid, diputado['congress_id']), newtext)
			summary += u'diputadoID %s; ' % diputado['congress_id']
		
		if diputado['email'] and not re.search(ur"(?im)\|email=", newtext):
			print "no tiene |email="
			newtext = re.sub(ur"{{Infobox Persona", ur"{{Infobox Persona\n|email=%s" % (diputado['email']), newtext)
			summary += u'%s; ' % diputado['email']
		
		if diputado['twitter'] and not re.search(ur"(?im)\|twitter=", newtext):
			print "no tiene |twitter="
			newtext = re.sub(ur"{{Infobox Persona", ur"{{Infobox Persona\n|twitter=%s" % (diputado['twitter'].split('/')[3]), newtext)
			summary += u'@%s; ' % diputado['twitter'].split('/')[3]
		
		if diputado['web'] and not re.search(ur"(?im)\|sitio web=", newtext):
			print "no tiene |sitio web="
			newtext = re.sub(ur"{{Infobox Persona", ur"{{Infobox Persona\n|sitio web=%s" % (diputado['web']), newtext)
			newtext = re.sub(ur"(?im)(==\s*Enlaces externos\s*==\n)", ur"\1* %s\n" % (diputado['web']), newtext)
			summary += u'%s; ' % diputado['web']
		
		if not re.search(ur"(?im){{políticos}}", newtext):
			print "no tiene {{políticos}}"
			newtext = re.sub(ur"(\n\n\[\[Categoría:)", ur"\n\n{{políticos}}\1", newtext)
		
		#if re.search(ur"''' es ...", newtext):
		#	newtext = re.sub(ur"''' es ...", ur"''' es un político.", newtext)
		
		if wtext != newtext:
			wikipedia.showDiff(wtext, newtext)
			summary += u'...'
			p.put(newtext, summary, botflag=False)
			
