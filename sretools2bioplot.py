#!/usr/bin/env python2.7

# __author__ = 'drs. ing. Jos Bouten'

'''
    Tool to convert the output of sretools (D. van Leeuwen) to bioplot type3 data format.

    Copyright (C) 2015 Jos Bouten ( josbouten at gmail dot com )

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

class tool:
    def __init__(self, thisDebug):
        self.debug = thisDebug

    def readFromFile(self, thisFilename):
        '''
        Read raw lines of text from a text file.
        Strip lines of CR/LF
        :param filename: string: name of file containing text
        :return: list of strings
        '''
        try:
            f = open(thisFilename, 'r')
            lines = f.readlines()
            f.close()
            res = []
            for line in lines:
                res.append(line.strip())
            return res
        except IOError, e:
            print 'Data.readFromFile:', e
            sys.exit(1)

def usage():
    print sys.argv[0], '<input file>'

if __name__ == '__main__':

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        t = tool(True)
        lines = t.readFromFile(filename)
        for line in lines:
            tmp = line.split(',')
            filenaam = tmp[1]
            score = tmp[6]
            truth = tmp[7]
            metaValue = tmp[2] + '_' + tmp[4] + tmp[5]
            #idTrain = tmp[3] + '_' + metaValue
            #idTest = tmp[0] + '_' + tmp[2]
            idTrain = tmp[3]
            idTest = tmp[0]
            print idTrain, filenaam, idTest, 'bla', score, truth, metaValue
    else:
        usage()