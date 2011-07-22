# -*- coding: utf-8 -*-

# Copyright (C) 2011 emijrp
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

# This script uses the data available on this link: http://opengov.es/package/reales-decretos
# Run: python decretos.py

import csv

decretos = csv.reader(open('2011-07-16_reales-decretos.csv', 'rb'), delimiter=',', quotechar='"')

days = {}
months = {}
years = {}
c=0
for row in decretos:
    if c == 0:
        c += 1
        continue
    #print row
    day, month, year = row[3].split('/')
    day = '%02d' % int(day)
    month = '%02d' % int(month)
    
    if days.has_key(day): days[day] += 1
    else: days[day] = 1
    
    if months.has_key(month): months[month] += 1
    else: months[month] = 1
    
    if years.has_key(year): years[year] += 1
    else: years[year] = 1

for dic in [days, months, years]:
    print '\n'
    l = [[k, v] for k, v in dic.items()]
    l.sort()
    print '\n'.join(['%s,%s' % (k, v) for k, v in l])
