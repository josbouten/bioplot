#!/usr/bin/python2.7

__author__ = 'drs. ing. Jos Bouten'

'''
    anonimize.py

    Use this code as an example of how to make an anonimized copy of the data file.

    Copyright (C) 2014 Jos Bouten ( josbouten@gmail.com )

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

'''

import sys

import hashlib
m = hashlib.md5()
filename = sys.argv[1]

try:
    f = open(filename, 'rt')
except Exception, e:
    print e
    sys.exit(1)
else:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    tmp = line.split()
    l1 = tmp[0]
    l2 = tmp[2]
    file1 = tmp[1]
    m.update(file1)
    file1n = m.hexdigest() + '.wav'
    file2 = tmp[3]
    m.update(file2)
    file2n = m.hexdigest() + '.wav'
    score = tmp[4]
    truth = tmp[5]
    m1 = tmp[6]
    m2 = tmp[7]
    print l1, file1n, l2, file2n, score, truth, m1, m2
