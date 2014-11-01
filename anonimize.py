#!/usr/bin/python2.7

__author__ = 'drs. ing. Jos Bouten'

import sys
import hashlib

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

def usage():
    print sys.argv[0], '<input filename> <output filename>'
    sys.exit(1)

def anonimize(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

#
# MAIN
#


if len(sys.argv) < 2:
    usage()
else:
    inFilename = sys.argv[1]
    outFilename = sys.argv[2]

    # Read data from input file
    try:
        fIn = open(inFilename, 'rt')
    except Exception, e:
        print e
        sys.exit(1)
    else:
        lines = fIn.readlines()
        fIn.close()

    # Open output file and write data to it
    try:
        fo = open(outFilename, 'wt')
    except Exception, e:
        print e
        sys.exit(1)
    else:
        for line in lines:
            line = line.strip()
            tmp = line.split()
            l1 = tmp[0]
            filename1 = tmp[1]
            l2 = tmp[2]
            filename2 = tmp[3]
            score = tmp[4]
            truth = tmp[5]
            metaValue = tmp[6]

            # The filenames contains some private info,
            # therefore we anonymize them
            filename1Anon = anonimize(filename1)
            filename2Anon = anonimize(filename2)

            # print plain and anonymized labels
            fo.write("%s %s %s %s %s %s %s\n" % (l1, filename1Anon, l2, filename2Anon, score, truth, metaValue))
        fo.close()