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

import datetime
import json
import os
import re
import urllib
import sys
import time

# wikis (edits, uploads), repositories

def convert2unix(mwtimestamp):
    #2010-12-25T12:12:12Z
    [year, month, day] = [int(mwtimestamp[0:4]), int(mwtimestamp[5:7]), int(mwtimestamp[8:10])]
    [hour, minute, second] = [int(mwtimestamp[11:13]), int(mwtimestamp[14:16]), int(mwtimestamp[17:19])]
    d = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    return int((time.mktime(d.timetuple())+1e-6*d.microsecond)*1000)

def generateHTML(title, description, js):
    return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
 <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>%s</title>
    <link href="style.css" rel="stylesheet" type="text/css"></link>
    <!--[if IE]><script language="javascript" type="text/javascript" src="lib/flot/excanvas.min.js"></script><![endif]-->
    <script language="javascript" type="text/javascript" src="lib/flot/jquery.js"></script>
    <script language="javascript" type="text/javascript" src="lib/flot/jquery.flot.js"></script>
 </head>
    <body>
    <!-- start content -->
    <h1>%s</h1>
    
    <div id="placeholder" style="width:98%%;height:250px;"></div>

    <p>%s</p>

<script id="source">
%s

//from http://people.iola.dk/olau/flot/examples/interacting.html
function showTooltip(x, y, contents) {
    $('<div id="tooltip">' + contents + '</div>').css( {
        position: 'absolute',
        display: 'none',
        top: y + 5,
        left: x + 12,
        border: '1px solid #fdd',
        padding: '2px',
        'background-color': '#fee',
        opacity: 0.80
    }).appendTo("body").fadeIn(200);
}

var previousPoint = null;
$("#placeholder").bind("plothover", function (event, pos, item) {
    $("#x").text(pos.x.toFixed(2));
    $("#y").text(pos.y.toFixed(2));
    
    if (item) {
        if (previousPoint != item.datapoint) {
            previousPoint = item.datapoint;
            
            $("#tooltip").remove();
            var x = item.datapoint[0].toFixed(2),
                y = item.datapoint[1].toFixed(2);
            
            showTooltip(item.pageX, item.pageY,
                        "y = "+Math.round(y));
        }
    } else {
        $("#tooltip").remove();
        previousPoint = null;            
    }
});
</script>

<hr/>
<p><i>This page was last modified on <!-- timestamp -->%s<!-- timestamp --> (UTC).</i></p>
<!-- end content -->
</body>
</html>
""" % (title, title, description, js, datetime.datetime.now())

def writeHTML(filename, output):
    f = open(os.path.expanduser('./%s' % (filename)), 'w')
    f.write(output)
    f.close()

config = ''
if len(sys.argv) >= 2:
    config = sys.argv[1]
else:
    print 'python script.py config.txt\n'
    print 'where config.txt is a file with this format:'
    print 'username;project name;api'
    print 'username;project name;api'
    print 'username;project name;api'
    sys.exit()

projects = []
f = open(config, 'r')
lines = f.readlines()
f.close()
for line in lines:
    if len(line)>0 and line[0] != '#':
        projects.append(line[:-1].split(';'))

dic = {}
for nick, project, api in projects:
    apiquery = '?action=query&list=usercontribs&ucuser=%s&uclimit=500&ucprop=timestamp|title|comment&format=json&ucstart=' % (nick)
    dic[project] = {}
    ucstart = '2099-01-01T00:00:00Z'
    while ucstart:
        sys.stderr.write(".")
        json_data = urllib.urlopen(api+apiquery+ucstart)
        data = json.load(json_data)
        for edit in data['query']['usercontribs']:
            d = datetime.datetime.strptime(edit['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
            t = d.strftime('%Y-%m-01T00:00:00Z')
            if dic[project].has_key(t):
                dic[project][t] += 1
            else:
                dic[project][t] = 1
        json_data.close()
        if data.has_key('query-continue'):
            ucstart = data['query-continue']['usercontribs']['ucstart']
        else:
            ucstart = ''
        #print ucstart
    
    print dic[project].items()

var = []
for nick, project, api in projects:
    l = []
    for k2, v2 in dic[project].items():
        l.append([str(convert2unix(k2)) , str(v2)])
    l.sort()
    l.reverse()
    var.append(l)

var_ = ''
data_ = ''
c = 1
for l in var:
    var_ += 'var d%d = %s;\n' % (c, str(l))
    data_ += '{ data: d%d, label: "%s"}, ' % (c, projects[c-1][1])
    c += 1

js = """function p() {
    %s
    
    var placeholder = $("#placeholder");
    var data = [%s];
    var options = { xaxis: { mode: "time" }, lines: { show: true }, points: { show: true }, legend: { noColumns: %s }, grid: { hoverable: true }, };
    $.plot(placeholder, data, options);
}
p();""" % (var_, data_, len(var))

output = generateHTML(title='My stats', description='', js=js)
writeHTML(filename='mystats.html', output=output)
