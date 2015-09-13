#!/usr/bin/env python2.7

'''
    Tool to convert the output of Vocalise (Oxford Wave Research) to bioplot data format.

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
import optparse
from license import License

class VocaliseData:
    def __init__(self, thisFilename, thisMetaValue, thisDebug):
        self.inputFilename = thisFilename
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
        with open(self.inputFilename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=delimiter, strict=True)
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
                        # All scores are treated as strings. So nothing will happen if one of
                        # the scores is not numerical. Handling this is left to bioplot.
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
            length = self._lenghtOfLongestCommonString(thisModelName, thisTestName)
            if length > maxLength:
                maxLength = length
        return maxLength

    def _lenghtOfLongestCommonString(self, s1, s2):
        ''' Find longest correspondence between 2 strings from the beginning of the strings.
            :param s1, s2 strings
            :return int length
        '''
        m = len(s1)
        length = 0
        for i in range(m):
            try:
                if s1[i] == s2[i]:
                    length += 1
                else:
                    break
            except Exception:
                # We need to stop if the lengths of s1 and s2 are different
                # and we reach the end of one of them.
                break
        return length

    def convert2bioplot(self, thisFilename='stdout'):
        if thisFilename != 'stdout':
            try:
                f = open(thisFilename, 'wt')
            except Exception, e:
                print e
                sys.exit(1)
        for m, modelName in enumerate(self.modelNames):
            for t, testName in enumerate(self.testNames):
                shortModelName = modelName[:self.patternLength]
                shortTestName = testName[:self.patternLength]
                if shortModelName == shortTestName:
                    truthValue = 'TRUE'
                else:
                    truthValue = 'FALSE'
                try:
                    if thisFilename == 'stdout':
                        print shortModelName, modelName, shortTestName, testName, self.scores[testName][m], \
                            truthValue, self.metaValue
                    else:
                        f.write("%s %s %s %s %s %s %s\n" % (shortModelName, modelName, shortTestName, testName, \
                            str(self.scores[testName][m]), truthValue, self.metaValue))
                except Exception, e:
                    print e
                    pass
                    # If for whatever reason there is no score for a given combination of
                    # test model vs training model, then we skip the experiment.
        if thisFilename != 'stdout':
            f.close()
        if len(self.errorsInRow) > 0:
            sys.stderr.write("There were problems with the following results from %s:\n" % self.inputFilename)
            sys.stderr.write("Note, this is often caused by results split over more than 1 line.\n")
            for el in self.errorsInRow:
                sys.stderr.write("%s\n" % (str(el)))


if __name__ == '__main__':
    version = "0.1"
    parser = optparse.OptionParser(usage="%s [options filename] \n\
    vocalise2bioplot.py version %s, Copyright (C) 2015 Jos Bouten\n\
    vocalise2bioplot.py comes with ABSOLUTELY NO WARRANTY; for details type `vocalise2bioplot.py -l\'.\n\
    This is free software, and you are welcome to redistribute it\n\
    under certain conditions; type `vocalise2bioplot.py -l\' for details.\n\
    This program was written by Jos Bouten.\n\
    You can contact me via josbouten at gmail dot com." % (sys.argv[0], version),
    version="This is vocalise2bioplot.py version %s, Copyright (C) 2015 Jos Bouten" % version, )
    parser.add_option('-i', '--input', action="store", dest="inputfile", help="input file name")
    parser.add_option('-o', '--output', action="store", dest="outputfile", help="output file name")
    parser.add_option('-l', '--license', action="store_true", dest="showLicense", help="show license")
    options, remainder = parser.parse_args()

    # Let's handle any request for the license first.
    # We stop the program after that.
    debug = False
    if options.showLicense:
        l = License('LICENSE.txt', debug)
        l.showLicense()
        exit(0)

    if options.inputfile:
        metaValue = 'META'
        vData = VocaliseData(options.inputfile, metaValue, debug)
        if options.outputfile:
            # Print converted data to file
            vData.convert2bioplot(options.outputfile)
        else:
            # Print to standard output device.
            vData.convert2bioplot('stdout')
