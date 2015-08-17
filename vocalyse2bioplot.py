#!/usr/bin/env python2.7

# __author__ = 'drs. ing. Jos Bouten'

'''
    Tool to convert the output of Vocalise (oxford wave research) to bioplot data format.

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
import csv
import collections

class VocaliseData:
    def __init__(self, thisFilename, thisMetaValue, thisDebug):
        self.filename = thisFilename
        self.metaValue = thisMetaValue
        self.debug = thisDebug
        self.modelNames = []
        self.scores = collections.defaultdict(list)
        self.testNames = []
        self.patternLength = 0
        self.errorsInRow = []
        self.readFromFile()

    def readFromFile(self):
        '''
        Read raw lines of text from a csv file.
        :param filename: string: name of file containing text
        :return list of strings
        '''
        onlyOnce = True
        delimiter = ','
        length = 0
        with open(self.filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=delimiter, strict=True) #, skipinitialspace=True)
            rowLength = 0
            for row in spamreader:
                if onlyOnce:
                    self.modelNames = row[1:]
                    onlyOnce = False
                    # In the result lines we expect #modelNames + 1 element.
                    rowLength = len(self.modelNames) + 1
                else:
                    # If there is a formatting error, the row will not have the required length.
                    # In that case we skip the line and tell the user afterwards.
                    if len(row) == rowLength:
                        subject = row[0]
                        self.testNames.append(subject)
                        self.scores[subject] = row[1:]
                    else:
                        self.errorsInRow.append(row)
        self.patternLength = self._findKeyPatternLength()

    def _findKeyPatternLength(self):
        # Find first non zero length model name
        thisModelName = None
        for el in self.modelNames:
            if len(el) > 0:
                thisModelName = el
                break
        # Find longest correspondence between test name and model name
        maxLength = 0
        for thisTestName in self.testNames:
            length = self._longestCommonString(thisModelName, thisTestName)
            if length > maxLength:
                maxLength = length
        return maxLength

    def _longestCommonString(self, s1, s2):
        ''' Find longest correspondence between 2 strings from the beginning of the strings.
            :param s1, s2 strings
            :return int length
        '''
        m = len(s1)
        c = 0
        for i in range(m):
            try:
                if s1[i] == s2[i]:
                    c += 1
                else:
                    break
            except Exception:
                # We need to stop if the lengths of s1 and s2 are different
                break
        return c

    def printTable(self):
        errors = []
        for m, modelName in enumerate(self.modelNames):
            for t, testName in enumerate(self.testNames):
                shortModelName = modelName[:self.patternLength]
                shortTestName = testName[:self.patternLength]
                if shortModelName == shortTestName:
                    truthValue = 'TRUE'
                else:
                    truthValue = 'FALSE'
                try:
                    print shortModelName, modelName, shortTestName, testName, self.scores[testName][m], truthValue, self.metaValue
                except Exception:
                    pass
                    # If for whatever reason there is no score for a given combination of
                    # test model vs training model, then we skip the experiment.
        if len(self.errorsInRow) > 0:
            sys.stderr.write("There were problems with the following results from %s:\n" % self.filename)
            sys.stderr.write("Note, this is often caused by results split over more than 1 line.\n")
            for el in self.errorsInRow:
                sys.stderr.write("%s\n" % (str(el)))

def usage():
    print sys.argv[0], '<input file>'

if __name__ == '__main__':

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        metaValue = 'META'
        vData = VocaliseData(filename, metaValue, True)
        vData.printTable()
    else:
        usage()