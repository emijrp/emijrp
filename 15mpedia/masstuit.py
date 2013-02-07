#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2013 emijrp <emijrp@gmail.com>
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

import datetime
import random
import re
import sys

saludos = [
    u'',
    u'',
    u'',
    u'',
    u'',
    u'',
    u'',
    u'Hola,',
    u'Hey!',
    u'Buenas,',
    u'Seguimos,',
]

despedidas = [
    u'',
    u'',
    u'gracias',
    u'¡gracias!',
    u'gracias por tu ayuda',
    u'gracias por ayudar',
    u'¡ánimo!',
    u'adelante!',
    u'échale un ojo',
    u'échale un vistazo',
]

emoticonos = [ #no poner ;) ni :D ya que algunos tuits pueden ser sobre temas poco amables
    u'',
    u'',
    u'',
    u':)',
]

cuerpos = [
    #todos los msg comienzan en minúscula
    #no usar la palabra ayuda en el cuerpo, ya que se usa en la despedida a veces
    
    #acampadas
    [u'revisa la lista de #acampadas y mejora la tuya!', u'http://wiki.15m.cc/wiki/Lista_de_acampadas'],
    [u'comprueba que en el listado de #acampadas no falte ninguna', u'http://wiki.15m.cc/wiki/Lista_de_acampadas'],
    
    #asambleas
    [u'esta es la lista de #asambleas, amplíala!', u'http://wiki.15m.cc/wiki/Lista_de_asambleas'],
    [u'elige tu #asamblea y complétala!', u'http://wiki.15m.cc/wiki/Lista_de_asambleas'],
    [u'puedes elegir tu #asamblea y mejora su artículo', u'http://wiki.15m.cc/wiki/Lista_de_asambleas'],
    
    #bancos de tiempo
    [u'comprueba que el #bancodetiempo de tu barrio o ciudad está aquí', u'http://wiki.15m.cc/wiki/Lista_de_bancos_de_tiempo'],
    [u'amplía la lista de #bancodetiempo y colabora', u'http://wiki.15m.cc/wiki/Lista_de_bancos_de_tiempo'],
    
    #centros de salud
    [u'revisa la lista de centros de salud en peligro de cierre', u'http://wiki.15m.cc/wiki/Lista_de_centros_de_salud_y_servicios_de_urgencia_cerrados'],
    [u'amplía la lista de centros de salud en peligro', u'http://wiki.15m.cc/wiki/Lista_de_centros_de_salud_y_servicios_de_urgencia_cerrados'],
    
    #centros sociales
    [u'¿colaboras completando la lista de centros sociales de toda España?', u'http://wiki.15m.cc/wiki/Lista_de_centros_sociales'],
    [u'agrega tu #CSOA al listado, todavía faltan muchos!', u'http://wiki.15m.cc/wiki/Lista_de_centros_sociales'],
    [u'¿conoces algún #CSOA que no esté aquí puesto?', u'http://wiki.15m.cc/wiki/Lista_de_centros_sociales'],
    
    #comedores
    [u'cada vez más personas necesitan #comedorsocial ¿faltan? mejóralo', u'http://wiki.15m.cc/wiki/Lista_de_comedores_sociales'],
    [u'aquí #comedoresociales, colabora a completarlo', u'http://wiki.15m.cc/wiki/Lista_de_comedores_sociales'],
    
    #cooperativas
    [u'aquí un listado de #cooperativas, complétalo!', u'http://wiki.15m.cc/wiki/Lista_de_cooperativas'],
    [u'la lista de #cooperativas te necesita! mejórala!', u'http://wiki.15m.cc/wiki/Lista_de_cooperativas'],
    
    #desahucios
    [u'colabora completando la lista de #desahucios parados #stopdesahucios', u'http://wiki.15m.cc/wiki/Lista_de_desahucios'],
    [u'mira la lista de #desahucios y complétala', u'http://wiki.15m.cc/wiki/Lista_de_desahucios'],
    
    #indultos
    #[u'', u'http://wiki.15m.cc/wiki/Lista_de_indultos'],
    #[u'', u'http://wiki.15m.cc/wiki/Lista_de_indultos'],
    
    #manifestaciones
    #[u'', u'http://wiki.15m.cc/wiki/Lista_de_manifestaciones'],
    #[u'', u'http://wiki.15m.cc/wiki/Lista_de_manifestaciones'],
    
    #mareas
    [u'la página dedicada a la #mareaamarilla necesita más cosillas', u'http://wiki.15m.cc/wiki/Marea_Amarilla'],
    [u'aquí la página para #mareaazul, complétala', u'http://wiki.15m.cc/wiki/Marea_Azul'],
    [u'sobre #mareablanca tenemos esto, mejóralo', u'http://wiki.15m.cc/wiki/Marea_Blanca'],
    [u'si sabes más sobre #mareanaranja, aquí puedes colaborar', u'http://wiki.15m.cc/wiki/Marea_Naranja'],
    [u'participa en la página sobre #mareanegra', u'http://wiki.15m.cc/wiki/Marea_Negra'],
    [u'queremos completar la página de #marearoja, participa', u'http://wiki.15m.cc/wiki/Marea_Roja'],
    [u'en #mareaverde seguro que nos hemos olvidado algo, colabora', u'http://wiki.15m.cc/wiki/Marea_Verde'],
    [u'si sabes más sobre #mareavioleta, aquí puedes participar', u'http://wiki.15m.cc/wiki/Marea_Violeta'],
    
    #parados
    [u'estar en el paro no es estar parado, ¿conoces la asociación de tu ciudad?', u'http://wiki.15m.cc/wiki/Lista_de_asociaciones_de_parados'],
    [u'completa la lista de asociaciones de parados', u'http://wiki.15m.cc/wiki/Lista_de_asociaciones_de_parados'],
    
    #partidos y fundaciones
    #[u'', u'http://wiki.15m.cc/wiki/Lista_de_partidos_pol%C3%ADticos'],
    [u'completa la información sobre fundaciones de partidos políticos', u'http://wiki.15m.cc/wiki/Lista_de_fundaciones_de_partidos_pol%C3%ADticos'],
    [u'mejora la información de financiación de partidos', u'http://wiki.15m.cc/wiki/Financiaci%C3%B3n_de_partidos_pol%C3%ADticos'],
    
    #plataformas
    [u'mira las plataformas que hay y completa sus páginas', u'http://wiki.15m.cc/wiki/Lista_de_plataformas'],
    [u'¿falta alguna plataforma? seguro que sí', u'http://wiki.15m.cc/wiki/Lista_de_plataformas'],
    
    #realojos
    [u'añade información a lista de #realojos y mejórala', u'http://wiki.15m.cc/wiki/Lista_de_realojos'],
    [u'un listado con #realojos esperando a que lo mejores', u'http://wiki.15m.cc/wiki/Lista_de_realojos'],
    
    #recortes
    [u'aquí la lista de recortes, complétala con más ejemplos', u'http://wiki.15m.cc/wiki/Lista_de_recortes'],
    [u'¿se nos ha pasado algún recorte? agrégalo', u'http://wiki.15m.cc/wiki/Lista_de_recortes'],
    
    #streamings
    [u'mejora la lista de #streamings de manis', u'http://wiki.15m.cc/wiki/Lista_de_streamings'],
    [u'tenemos muchos #streamings pero seguro faltan más', u'http://wiki.15m.cc/wiki/Lista_de_streamings'],
    
    #suicidios
    #tema delicado, no automatizar
    
    #tutorial
    [u'hemos preparado un tutorial muy sencillo explicando cómo participar en 15Mpedia', u'http://wiki.15m.cc/wiki/Ayuda:B%C3%A1sica'],
    [u'hay un tutorial breve para convertirse en 15Mpedista', u'http://wiki.15m.cc/wiki/Ayuda:B%C3%A1sica'],
    [u'para la gente nueva, aquí un tutorial para aprender a usar el wiki', u'http://wiki.15m.cc/wiki/Ayuda:B%C3%A1sica'],
]

l = []
for saludo in saludos:
    for despedida in despedidas:
        for cuerpo in cuerpos:
            for emoticono in emoticonos:
                if cuerpo[0] and cuerpo[1]:
                    msg = u'"%s %s, %s %s","%s"' % (saludo, saludo and cuerpo[0] or '%s%s' % (cuerpo[0][0].upper(), cuerpo[0][1:]), despedida, emoticono, cuerpo[1])
                    msg = msg.strip()
                    msg = re.sub(ur'  +', u' ', msg)
                    msg = re.sub(ur'(?im)^" *', u'"', msg)
                    msg = re.sub(ur'(?im) *","', u'","', msg)
                    if not msg in l:
                        l.append(msg)

limit = 300
if len(l) < limit:
    print 'Se necesitan mas de %d mensajes aleatorios' % (limit)
    sys.exit()

random.shuffle(l)
output = u''
dstart = datetime.datetime.now() #mañana
dstart = datetime.datetime(day=1, month=3, year=2013)
ddelta = datetime.timedelta(days=1)
c = 0
while c<limit/3:
    dstart += ddelta
    #mañana
    h = '%02d:%02d' % (random.randrange(9,11+1), random.randrange(0,59+1))
    d = u'%s %s' % (dstart.strftime('%m/%d/%Y'), h)
    output += u'"%s",%s\n' % (d, l[c])
    #tarde
    h = '%02d:%02d' % (random.randrange(16,19+1), random.randrange(0,59+1))
    d = u'%s %s' % (dstart.strftime('%m/%d/%Y'), h)
    output += u'"%s",%s\n' % (d, l[c+100])
    #noche
    h = '%02d:%02d' % (random.randrange(22,23+1), random.randrange(0,59+1))
    d = u'%s %s' % (dstart.strftime('%m/%d/%Y'), h)
    output += u'"%s",%s\n' % (d, l[c+200])
    c += 1

print output.encode('utf-8')

