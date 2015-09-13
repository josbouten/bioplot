#!/usr/bin/env python2.7

'''
    Tool to convert the output of BV result text files to bioplot data format.

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


class BVData:
    def __init__(self, thisFilename, thisMetaValue, thisDebug):
        self.inputFilename = thisFilename
        self.metaValue = thisMetaValue
        self.debug = thisDebug
        self.errorsInRow = []

        '''
        Scores and LRs output
        Expected output: target|audio filename|model|score or lr value
        -  target: value will be 0 if non-target, 1 otherwise;
        -  audio filename: name of the file used as target;
        -  model: name of the Speaker;
        -  score or lr value: result value or the score.
        Example:

        1|001-2-060310-edit-4mins-target.wav|Speaker1|19.75356409358525
        0|001-2-060310-edit-4mins-target.wav|Speaker10|-4.2008717897736245
        0|001-2-060310-edit-4mins-target.wav|Speaker11|-7.394203686297978
        0|001-2-060310-edit-4mins-target.wav|Speaker12|-2.725574466317258
        0|001-2-060310-edit-4mins-target.wav|Speaker13|-4.276117340898227

        '''

    def convert2bioplot(self, thisFilename='stdout'):
        '''
        Read raw lines of text from a BV csv file and print them in bioplot sequence.
        '''
        if thisFilename != 'stdout':
            try:
                f = open(thisFilename, 'wt')
            except Exception, e:
                print e
                sys.exit(1)
        delimiter = '|'
        speaker4Model = collections.defaultdict(list)
        keep = set()
        with open(self.inputFilename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=delimiter, strict=True)  # , skipinitialspace=True)
            rowLength = 4
            cnt = 0
            for row in spamreader:
                if len(row) == rowLength:
                    truth = row[0]
                    testModel = row[1]
                    speaker = row[2]
                    score = row[3]
                    if truth == '1':
                        speaker4Model[testModel] = speaker
                    keep.add((truth, testModel, speaker, score))
                    cnt += 1
                else:
                    self.errorsInRow.append(row)
            for el in keep:
                (truth, testModel, speaker, score) = el
                if truth == '1':
                    truth = "TRUE"
                else:
                    truth = "FALSE"
                if thisFilename != 'stdout':
                    f.write("%s %s %s %s %s %s %s\n" % (speaker, testModel, speaker4Model[testModel],\
                                speaker4Model[testModel] + '_' + testModel, str(score), truth, self.metaValue))
                else:
                    print speaker, testModel, speaker4Model[testModel], testModel, score, truth, self.metaValue
                    # print speaker, testModel, speaker4Model[testModel], speaker4Model[testModel] + \
                    #                 '_' + testModel, score, truth, self.metaValue
        if len(self.errorsInRow) > 0:
            sys.stderr.write("There were problems with the following results from %s:\n" % self.inputFilename)
            sys.stderr.write("Note, this is often caused by results split over more than 1 line.\n")
            for el in self.errorsInRow:
                sys.stderr.write("%s\n" % (str(el)))
        # Close file if necessary.
        if thisFilename != 'stdout':
            f.close()


if __name__ == '__main__':
    version = "0.1"
    parser = optparse.OptionParser(usage="%s [options filename] \n\
    bv2bioplot.py version %s, Copyright (C) 2015 Jos Bouten\n\
    bv2bioplot.py comes with ABSOLUTELY NO WARRANTY; for details type `bv2bioplot.py -l\'.\n\
    This is free software, and you are welcome to redistribute it\n\
    under certain conditions; type `bv2bioplot.py -l\' for details.\n\
    This program was written by Jos Bouten.\n\
    You can contact me via josbouten at gmail dot com." % (sys.argv[0], version),
                                   version="This is bv2bioplot.py version %s, Copyright (C) 2015 Jos Bouten" % version, )
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
        bData = BVData(options.inputfile, metaValue, debug)
        if options.outputfile:
            # Print converted data to file
            bData.convert2bioplot(options.outputfile)
        else:
            # Print to standard output device.
            bData.convert2bioplot('stdout')
