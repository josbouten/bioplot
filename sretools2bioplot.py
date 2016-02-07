#!/usr/bin/env python2.7

"""
    Tool to convert the input data for sretools (D. van Leeuwen) to bioplot data format.

    Copyright (C) 2015, 2016 Jos Bouten ( josbouten at gmail dot com )

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
"""

import sys
import csv
import argparse
from license import License
import os.path

class SreData:
    def __init__(self, thisInputFilename, thisMetaValue, thisDebug):
        self.inputFilename = thisInputFilename
        self.metaValue = thisMetaValue
        self.debug = thisDebug

    def convert2bioplot(self, thisFilename='stdout'):
        """
        Tspid,Tfrid,Mspid,Mfrid,score,target
        114849,0000000005712904a,114849,0000000005713112b,5.368496418,TRUE
        114849,0000000005712904a,114853,0000000005281055b,1.67685461,FALSE
        114849,0000000005712904a,114853,0000000005288357b,1.363172889,FALSE
        114849,0000000005712904a,114854,0000000005133202a,-0.024709666,FALSE


        into
        114849 0000000005713112b 114849 0000000005712904a 5.368496418  TRUE  META_VALUE
        114853 0000000005281055b 114849 0000000005712904a 1.67685461   FALSE META_VALUE
        114853 0000000005288357b 114849 0000000005712904a 1.363172889  FALSE META_VALUE
        114854 0000000005133202a 114849 0000000005712904a -0.024709666 FALSE META_VALUE

        :param thisFilename:
        :return:
        """
        '''
        :param thisFilename:
        :return:
        '''
        if thisFilename != 'stdout':
            try:
                f = open(thisFilename, 'wt')
            except Exception, e:
                print e
                sys.exit(1)
        delimiter = ','
        with open(self.inputFilename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=delimiter, strict=True)
            for row in spamreader:
                # Skip first line
                if not 'Tspid' in row[0]:
                    idTest = row[0]
                    testFilename = row[1]
                    idTrain = row[2]
                    trainFilename = row[3]
                    score = row[4]
                    truth = row[5]
                    if thisFilename != 'stdout':
                        f.write("%s %s %s %s %s %s %s\n" % \
                            (idTrain, trainFilename, idTest, testFilename, str(score), truth, self.metaValue))
                    else:
                        print idTrain, trainFilename, idTest, testFilename, str(score), truth, self.metaValue
        if thisFilename != 'stdout':
            f.close()

if __name__ == '__main__':
    version = "0.2"
    progName = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(description="%s [options filename] \n\
    %s version %s, Copyright (C) 2015, 2016 Jos Bouten\n\
    This program comes with ABSOLUTELY NO WARRANTY. For details run \'%s -h\'.\n\
    This is free software, and you are welcome to redistribute it\n\
    under certain conditions; run \'%s -l\' for details.\n\
    This program was written by Jos Bouten.\n\
    You can contact me via josbouten at gmail dot com." % (progName, progName, version, progName, progName),
    version="This is %s version %s, Copyright (C) 2015, 2016 Jos Bouten" % (progName, version), )
    parser.add_argument('-i', '--input', action="store", dest="inputfile", help="input file name")
    parser.add_argument('-o', '--output', action="store", dest="outputfile", help="output file name")
    parser.add_argument('-l', '--license', action="store_true", dest="showLicense", help="show license")
    options = parser.parse_args()

    # Let's handle any request for the license first.
    # We stop the program after that.
    debug = False
    if options.showLicense:
        l = License('LICENSE.txt', debug)
        l.showLicense()
        exit(0)

    if options.inputfile:
        metaValue = 'META'
        sData = SreData(options.inputfile, metaValue, debug)
        if options.outputfile:
            # Print converted data to file
            sData.convert2bioplot(options.outputfile)
        else:
            # Print to standard output device.
            sData.convert2bioplot('stdout')