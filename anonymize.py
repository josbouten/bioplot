#!/usr/bin/python2.7

__author__ = 'drs. ing. Jos Bouten'

import sys
import hashlib

'''
    anonymize.py

    Use this code as an example of how to make an anonymized copy of a bioplot data file.

    Copyright (C) 2014, 2015, 2016 Jos Bouten ( josbouten at gmail dot com )

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
    print sys.argv[0], 'input_filename output_filename'
    sys.exit(1)

def anonymize(string):
    m = hashlib.sha256()
    m.update(string)
    return m.hexdigest()

#
# MAIN
#

if len(sys.argv) < 3:
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
        fOut = open(outFilename, 'wt')
    except Exception, e:
        print e
        sys.exit(1)
    else:
        for line in lines:
            line = line.strip()
            tmp = line.split()
            label1 = tmp[0]
            filename1 = tmp[1]
            label2 = tmp[2]
            filename2 = tmp[3]
            score = tmp[4]
            truth = tmp[5]
            metaValue = tmp[6]

            # The labels and filenames may contain private info, 
            # therefore they are anonymized.
            label1 = anonymize(label1)
            label2 = anonymize(label2)
            filename1Anon = anonymize(filename1)
            filename2Anon = anonymize(filename2)

            # print plain and anonymized elements
            fOut.write("%s %s %s %s %s %s %s\n" % (label1, filename1Anon, label2, filename2Anon, score, truth, metaValue))
        fOut.close()
