#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re
import time
import urllib
import wikipedia

site = wikipedia.Site('15mpedia', '15mpedia')
f = open('diputados.json', 'r')
raw = f.read()
f.close()
j = json.loads(raw)

partidos = {
	u"/api/v1/party/1/": u"Partido Popular",
	u"/api/v1/party/2/": u"Amaiur",
	u"/api/v1/party/3/": u"Unión Progreso y Democracia",
	u"/api/v1/party/4/": u"Partido Popular-Extremadura Unida",
	u"/api/v1/party/5/": u"Partido Socialista Obrero Español",
	u"/api/v1/party/6/": u"Foro de Ciudadanos",
	u"/api/v1/party/7/": u"Partido de los Socialistas de Cataluña", #cantabria/canarias tb?
	u"/api/v1/party/8/": u"Geroa Bai",
	u"/api/v1/party/9/": u"Convergència i Unió",
	u"/api/v1/party/10/": u"Compromís-Q",
	u"/api/v1/party/11/": u"Partido Nacionalista Vasco",
	u"/api/v1/party/12/": u"ERC-RI.cat",
	u"/api/v1/party/13/": u"Iniciativa per Catalunya-Verds",
	u"/api/v1/party/14/": u"Partido Popular en coalición con el Partido Aragonés",
	u"/api/v1/party/15/": u"Bloque Nacionalista Galego",
	u"/api/v1/party/16/": u"La Izquierda Plural",
	u"/api/v1/party/17/": u"Coalición Canaria-Nueva Canarias",
	u"/api/v1/party/18/": u"Esquerra Unida i Alternativa",
	u"/api/v1/party/19/": u"Unión del Pueblo Navarro",
	u"/api/v1/party/20/": u"Esquerra Unida del País Valencià",
	u"/api/v1/party/21/": u"Chunta Aragonesista",
}
grupos = {
	u"EAJ-PNV": u"GV (EAJ-PNV)",
	u"GS": u"GS",
	u"GP": u"GP",
	u"GIP": u"GIP",
	u"GMx": u"GMx",
	u"GUPyD": u"GUPyD",
	u"GC-CiU": u"GC-CiU",
}
for grupo in j["objects"]:
	gruponombre = grupos[grupo["acronym"].strip()]
	"""
	"objects": [
	{
	  "acronym": "EAJ-PNV",
	  "congress_id": "206",
	  "congress_url": "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/DiputadosLegFechas?_piref73_2496079_73_2496068_2496068.next_page=/wc/composicionGrupo&idGrupo=206",
	  "id": 6,
	  "members": [
		{
		  "id": 94,
		  "member": {
			"avatar": "http://www.congreso.es/wc/htdocs/web/img/diputados/244_10.jpg",
			"congress_id": "244",
			"congress_web": "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/DiputadosLegFechas?_piref73_2496079_73_2496068_2496068.next_page=%2Fwc%2FfichaDiputado&idDiputado=244",
			"division": "Bizkaia",
			"email": "",
			"id": 94,
			"inscription_date": "2011-02-12",
			"name": "Aitor",
			"resource_uri": "/api/v1/member/94/",
			"second_name": "Esteban Bravo",
			"termination_date": null,
			"twitter": "https://twitter.com/AITOR_ESTEBAN",
			"validate": true,
			"web": ""
		  },
		  "party": "/api/v1/party/11/"
		},
    """
	for dip in grupo['members']:
		diputado = dip["member"]
		legislaturaid = 10
		legislaturatext = u"X Legislatura"
		partidonombre = partidos[dip["party"]]
		inicio = diputado["inscription_date"]
		fin = diputado["termination_date"]
		circunscripcion = diputado["division"]
		
		summary = u"BOT - Añadiendo datos de [[Proyecto Colibrí]]: "
		nombre = u'%s %s' % (diputado['name'], diputado['second_name'], )
		print '-'*50
		print nombre, gruponombre, partidonombre
		print '-'*50
		
		p = wikipedia.Page(site, nombre)
		if p.exists():
			if p.isRedirectPage():
				p = p.getRedirectTarget()
			wtext = p.get()
			newtext = wtext
			
			#rellenar datos
			#secciones nuevas
			if not re.search(ur"(?im){{resumen votaciones}}", newtext):
				print "no tiene {{resumen votaciones}}"
				newtext = re.sub(ur"(?im)(== Declaraciones ==[^=]*)==", ur"\1== Votaciones ==\n{{resumen votaciones}}\n\n==", newtext)
			
			#infobox
			if nombre and not re.search(ur"(?im)\|nombre=", newtext):
				print "no tiene |nombre="
				newtext = re.sub(ur"{{Infobox Persona", ur"{{Infobox Persona\n|nombre=%s" % (nombre), newtext)
				summary += u'%s; ' % nombre
			
			if partidonombre:# and not re.search(ur"(?im)\|partido=", newtext): #sobreescribir el que esté puesto
				#print "no tiene |partido="
				if re.search(ur"(?im)\|partido=[^\n]*?\n", newtext):
					newtext = re.sub(ur"(\|partido=[^\n]*?)\n", ur"|partido=%s\n" % (partidonombre), newtext)
				else:
					newtext = re.sub(ur"{{Infobox Persona", ur"{{Infobox Persona\n|partido=%s" % (partidonombre), newtext)
				summary += u'%s; ' % partidonombre
			
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
			
			if not re.search(ur"(?im){{Parlamentario\|", newtext):
				print "no tiene {{Parlamentario"
				parlamentariolegislatura = u"{{Parlamentario|Congreso de los Diputados|%s|%s|%s}}" % (legislaturatext, gruponombre, circunscripcion)
				if re.search(ur"(?im)\|parlamentario=\n\|", newtext):
					newtext = re.sub(ur"(\|parlamentario=)", ur"\1%s" % (parlamentariolegislatura), newtext)
				elif not re.search(ur"(?im)\|parlamentario=", newtext):
					newtext = re.sub(ur"{{Infobox Persona", ur"{{Infobox Persona\n|parlamentario=%s" % (parlamentariolegislatura), newtext)
				summary += u"%s circunscripción; " % circunscripcion
				newtext = re.sub(ur"(?im)\[\[Categoría:Diputado de la X legislatura[^]]*\]\]", "", newtext)
			
			#intro
			if re.search(ur"(?im)''' es \.\.\.\n", newtext):
				if nombre.startswith(u'Amparo ') or nombre.startswith(u'Ana ') or nombre.startswith(u'Andrea ') or nombre.startswith(u'Ascensión ') or nombre.startswith(u'Beatriz ') or nombre.startswith(u'Belén ') or nombre.startswith(u'Carmen ') or nombre.startswith(u'Carolina ') or nombre.startswith(u'Cayetana ') or nombre.startswith(u'Celia ') or nombre.startswith(u'Concepci') or nombre.startswith(u'Dolor') or nombre.startswith(u'Elena ') or nombre.startswith(u'Elvira ') or nombre.startswith(u'Encarnación ') or nombre.startswith(u'Esperan') or nombre.startswith(u'Eva ') or nombre.startswith(u'Gracia ') or nombre.startswith(u'Inmaculada ') or nombre.startswith(u'Irene ') or nombre.startswith(u'Isabel ') or nombre.startswith(u'Laura ') or nombre.startswith(u'Lourdes ') or nombre.startswith(u'Macarena ') or nombre.startswith(u'Magdalena ') or nombre.startswith(u'Maite ') or nombre.startswith(u'María ') or nombre.startswith(u'Marga') or nombre.startswith(u'Marta ') or nombre.startswith(u'Matilde ') or nombre.startswith(u'Mª ') or nombre.startswith(u'Montserrat ') or nombre.startswith(u'Patricia ') or nombre.startswith(u'Pilar ') or nombre.startswith(u'Rocío ') or nombre.startswith(u'Rosa') or nombre.startswith(u'Silvia ') or nombre.startswith(u'Sofía ') or nombre.startswith(u'Soledad ') or nombre.startswith(u'Soraya ') or nombre.startswith(u'Susana ') or nombre.startswith(u'Teresa ') or nombre.startswith(u'Teófila ') or nombre.startswith(u'Trinidad ') or nombre.startswith(u'Tristana ') or nombre.startswith(u'Águeda ') or nombre.startswith(u'Ángeles ') :
					newtext = re.sub(ur"(?im)(''' es )\.\.\.", ur"\1una política del [[%s]], diputada de la [[%s]]." % (partidonombre, legislaturatext), newtext)
					if not re.search(ur"(?im)\|sexo=", newtext):
						newtext = re.sub(ur"{{Infobox Persona", ur"{{Infobox Persona\n|sexo=Mujer", newtext)
				else:
					newtext = re.sub(ur"(?im)(''' es )\.\.\.", ur"\1un político del [[%s]], diputado de la [[%s]]." % (partidonombre, legislaturatext), newtext)
					if not re.search(ur"(?im)\|sexo=", newtext):
						newtext = re.sub(ur"{{Infobox Persona", ur"{{Infobox Persona\n|sexo=Hombre", newtext)
				summary += u"+intro; "
			
			#enlaces externos
			if diputado['congress_id'] and not re.search(ur"(?im){{ficha congreso", newtext):
				print "no tiene {{ficha congreso"
				if re.search(ur"(?im){{wikipedia", newtext):
					newtext = re.sub(ur"(?im)(\*\s*{{wikipedia[^}]*}}\n)", ur"\1* {{ficha congreso|legislatura=%s|diputado=%s}}\n" % (legislaturaid, diputado['congress_id']), newtext)
				else:
					newtext = re.sub(ur"(?im)(==\s*Enlaces externos\s*==\n)", ur"\1* {{ficha congreso|legislatura=%s|diputado=%s}}\n" % (legislaturaid, diputado['congress_id']), newtext)
				summary += u'diputadoID %s; ' % diputado['congress_id']
			if diputado['web'] and not re.search(ur"(?im)^\*.*%s" % diputado['web'], newtext):
				newtext = re.sub(ur"(?im)(==\s*Enlaces externos\s*==\n)", ur"\1* %s\n" % (diputado['web']), newtext)
				summary += u'%s; ' % diputado['web']
			
			if not re.search(ur"(?im){{políticos}}", newtext):
				print "no tiene {{políticos}}"
				if re.search(ur"(?im)\[\[Categoría:", newtext):
					newtext = re.sub(ur"(\n\n\[\[Categoría:)", ur"\n\n{{políticos}}\1", newtext)
				else:
					newtext = u"%s\n\n{{políticos}}" % (newtext.strip())
			
			#guardar
			if wtext != newtext:
				wikipedia.showDiff(wtext, newtext)
				summary += u'...'
				p.put(newtext, summary, botflag=False)
