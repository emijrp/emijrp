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

import random
import re

saludos = [
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
    u'¡Gracias!',
    u'Gracias por ayudar',
    u'¡Ánimo!',
    u'Adelante!',
    u'Échale un ojo',
    u'Échale un vistazo',
]

emoticonos = [
    u'',
    u':)',
    u';)',
    u':D',
    u';D',
]

cuerpos = [
    #todos los msg comienzan en minúscula
    #acampadas
    [u'revisa la lista de #acampadas y mejora la tuya!', u'http://wiki.15m.cc/wiki/Lista_de_acampadas'],
    [u'comprueba que en el listado de #acampadas no falte ninguna', u'http://wiki.15m.cc/wiki/Lista_de_acampadas'],
    
    #asambleas
    [u'esta es la lista de #asambleas, ayuda a ampliar!', u'http://wiki.15m.cc/wiki/Lista_de_asambleas'],
    [u'elige tu #asamblea y echa una mano completándola!', u'http://wiki.15m.cc/wiki/Lista_de_asambleas'],
    [u'puedes elegir tu #asamblea y mejora su artículo, adelante!', u'http://wiki.15m.cc/wiki/Lista_de_asambleas'],
    
    #bancos de tiempo
    [u'', u''],
    [u'', u''],
    
    #centros sociales
    [u'¿nos ayudas a completar la lista de centros sociales de toda España?', u'http://wiki.15m.cc/wiki/Lista_de_centros_sociales'],
    [u'agrega tu #CSOA al listado, todavía faltan muchos!', u'http://wiki.15m.cc/wiki/Lista_de_centros_sociales'],
    [u'¿conoces algún #CSOA que no esté aquí puesto?', u'http://wiki.15m.cc/wiki/Lista_de_centros_sociales'],
    [u'', u''],
    
    #comedores
    [u'', u''],
    [u'', u''],
    
    #cooperativas
    [u'aquí un listado de cooperativas, ayuda a completar!', u'http://wiki.15m.cc/wiki/Lista_de_cooperativas'],
    [u'la lista de cooperativas te necesita! mejórala!', u'http://wiki.15m.cc/wiki/Lista_de_cooperativas'],
    
    #desahucios
    [u'ayuda a completar la lista de #desahucios parados #stopdesahucios', u'http://wiki.15m.cc/wiki/Lista_de_desahucios'],
    [u'', u''],
    
    #indultos
    [u'', u''],
    [u'', u''],
    
    #manifestaciones
    [u'', u''],
    [u'', u''],
    
    #mareas
    [u'', u''],
    [u'', u''],
    
    #plataformas
    [u'', u''],
    [u'', u''],
    
    #realojos
    [u'ayuda a completar la lista de realojos con datos de más lugares', u'http://wiki.15m.cc/wiki/Lista_de_realojos'],
    [u'un listado con realojos esperando a que lo mejores', u'http://wiki.15m.cc/wiki/Lista_de_realojos'],
    [u'', u''],
    
    #recortes
    [u'', u''],
    [u'', u''],
    
    #streamings
    [u'', u''],
    [u'', u''],
    
    #suicidios
    [u'', u''],
    [u'', u''],
    
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
                    msg = u'%s %s %s %s %s' % (saludo, cuerpo[0], cuerpo[1], despedida, emoticono)
                    msg = msg.strip()
                    msg = re.sub(ur'  +', u' ', msg)
                    msg = msg[0].upper() + msg[1:]
                    if not msg in l:
                        l.append(msg)

random.shuffle(l)
output = u'\n'.join(l[:350])
print output.encode('utf-8')

