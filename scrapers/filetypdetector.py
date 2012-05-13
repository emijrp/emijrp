#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 emijrp
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

import os
import re
import subprocess

targetdir = 'actas'
for dirname, dirnames, filenames in os.walk(targetdir):
    if dirname == targetdir:
        for f in filenames:
            if f.endswith('.file'):
                filepath = '%s/%s' % (targetdir, f)
                mime = subprocess.check_output(['file', '-b', '--mime', '%s/%s' % (targetdir, f)]) 
                print filepath, mime
                if 'application/pdf' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.pdf')
                elif 'application/msword' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.doc')
                elif 'application/rtf' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.rtf')
                elif 'application/vnd.oasis.opendocument.text' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.odt')
                elif 'application/jpeg' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.jpeg')
                elif 'application/png' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.png')
                elif 'application/gif' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.gif')
                elif 'application/xml' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.xml')
                elif 'application/mpeg' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.mpeg')
                elif 'application/plain' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.txt')
                elif 'application/html' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.htm')
                elif 'application/x-rar' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.rar')
                elif 'application/zip' in mime:
                    os.rename(filepath, '.'.join(filepath.split('.')[:-1]) + '.odt')
