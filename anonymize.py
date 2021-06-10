#!/usr/bin/env python3.5

__author__ = 'drs. ing. Jos Bouten'

import sys
import hashlib
import os.path
import argparse

'''
    anonymize.py

    This program will copy a bioplot data file into a file while converting the names of subjects and 
    audio files used in the experiment into anonymized strings (sha256 has values) thus anonymizing the data file.
    Analysis with bioplot of the file's content remains possible but retrieving the names of the subjects or
    audio filenames involved in the experiment will be almost impossible given the nature of the sha encoding.
    
    Copyright (C) 2014 Jos Bouten ( josbouten at gmail dot com )

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

class Anonimyzer():
    def __init__(self, thisDebug=False):
        self._debug = thisDebug

    def anonymise(self, string):
        m = hashlib.sha256()
        m.update(string)
        return m.hexdigest()

def parseArguments():
    '''
    Parse arguments from command line
    :return: argparse object
    '''
    version = "0.2"
    progName = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        description="{} version {}, Copyright (C) 2014, Jos Bouten.".format(progName, version) + \
                    " This program anonymizes a bioplot data file." +
                    " {} comes with ABSOLUTELY NO WARRANTY; for details run {} -h".format(progName, progName) +
                    " This is free software, and you are welcome to redistribute it " +
                    "under certain conditions; please read LICENSE.TXT supplied with this program. " +
                    "This program was written by Jos Bouten. " +
                    "You can contact me via josbouten at gmail dot com.", )
    parser.add_argument('-o', '--outputfile', action="store", dest="outputfile", help="output file name", type=str, required=True)
    parser.add_argument('-i', '--inputfile', action="store", dest="inputfile", help="input file name", type=str, required=True)

    return parser.parse_args()

#
# MAIN
#

args = parseArguments()

# Read data from input file.
try:
    fIn = open(args.inputfile, 'rt')
except Exception as e:
    print(e)
    sys.exit(1)
else:
    lines = fIn.readlines()
    fIn.close()

# Open output file and write data to it.
try:
    fOut = open(args.outputfile, 'wt')
except Exception as e:
    print(e)
    sys.exit(1)
else:
    anonimizer = Anonimyzer()
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
        label1 = anonimizer.anonymise(label1)
        label2 = anonimizer.anonymise(label2)
        filename1Anon = anonimizer.anonymise(filename1)
        filename2Anon = anonimizer.anonymise(filename2)

        # write plain and anonymized elements to file.
        fOut.write("%s %s %s %s %s %s %s\n" % (label1, filename1Anon, label2, filename2Anon, score, truth, metaValue))
    fOut.close()