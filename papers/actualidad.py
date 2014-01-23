# -*- coding: utf-8 -*-

#sudo apt-get install p7zip-full (for 7za)
import datetime
import re
import subprocess
from wmf import util, dump

#https://es.wikipedia.org/wiki/Plantilla:Evento_actual
#calcular la duracion media de la plantilla, en total y por tema
#excluir namespaces que no sean 0

actualidad_r = re.compile(ur"(?im)(\{\{\s*(Actual|Actualidad|Actualidad[ _]deporte|Current|EA|Evento[ _]actual|Launching|Muerte[ _]reciente|Sencillo[ _]actual|Single[ _]actual|Telenovela[ _]en[ _]emisión|Teleserie[ _]en[ _]emisión)\s*[\|\}]([^\}]*?)\}\}?)")

filename = "eswiki-20140113-pages-meta-history4.xml.7z"
fp = subprocess.Popen('7za e -bd -so %s 2>/dev/null' % filename, shell=True, stdout=subprocess.PIPE, bufsize=65535).stdout
    
dumpIterator = dump.Iterator(fp)

def calculartiempo(inicio, fin):
	tiempo = datetime.datetime.strptime(fin, '%Y%m%d%H%M%S') - datetime.datetime.strptime(inicio, '%Y%m%d%H%M%S')
	#print tiempo
	return tiempo

def main():
	actualidad = {}
	pagecount = 0
	for page in dumpIterator.readPages():
		if page.getNamespace() not in [0, 104]:
			continue
		pagecount += 1
		if pagecount % 1000 == 0:
			print pagecount
		plantillapuesta = False
		for rev in page.readRevisions():
			revtext = rev.getText()
			if revtext:
				if re.search(actualidad_r, revtext):
					if plantillapuesta:
						pass #la plantilla sigue puesta
					else:
						#alguien acaba de poner la plantilla
						plantillapuesta = util.timestamp2WP(rev.getTimestamp())
						if not actualidad.has_key(page.getTitle()):
							actualidad[page.getTitle()] = []
						tipo = re.findall(actualidad_r, revtext)[0][2] and re.findall(actualidad_r, revtext)[0][2] or 'Sin especificar'
						actualidad[page.getTitle()] = [[rev.getId(), util.timestamp2WP(rev.getTimestamp()), rev.getContributor().getUsername(), tipo, rev.getComment() and rev.getComment() or u"", u"", u"", u"", u"", u""]]
						#https://es.wikipedia.org/w/index.php?oldid=%s&diff=prev
				else:
					if plantillapuesta:
						#la plantilla la acaban de quitar
						actualidad[page.getTitle()][-1][-1] = u"%s" % calculartiempo(plantillapuesta, util.timestamp2WP(rev.getTimestamp()))
						plantillapuesta = False
						actualidad[page.getTitle()][-1][-2] = rev.getComment() and rev.getComment() or u""
						actualidad[page.getTitle()][-1][-3] = rev.getContributor().getUsername()
						actualidad[page.getTitle()][-1][-4] = util.timestamp2WP(rev.getTimestamp())
						actualidad[page.getTitle()][-1][-5] = rev.getId()
						print page.getTitle(), actualidad[page.getTitle()][-1]

if __name__ == '__main__':
    main()
