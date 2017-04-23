#!/usr/bin/env python3

'''

    raw2bioplot.py
    
    This program will convert raw score files to a format that can be read by bioplot.
    Most of the plots require target and non target scores. You can however make a histogram from one set of scores.
    Therefore it is not required to supply target and non target scores.

    Copyright (C) 2017 Jos Bouten ( josbouten at gmail dot com )

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
import os.path
import argparse


class RawReader:
    def __init__(self, thisTargetInputFile, thisNonTargetInputFile, thisOutputFile, thisCondition, thisDebug):
        '''
        Constructor for RawReader object
        :param thisTargetInputFile: string: name of input file containing target data
        :param thisNonTargetInputFile: string: name of input file containing non target data
        :param thisOutputFile: string: name of output file
        :param thisCondition: string: label describing experimental variable
        :param thisDebug: boolean: when true will cause debug info to be printed
        '''
        self._thisTargetInputFile = thisTargetInputFile
        self._thisNonTargetInputFile = thisNonTargetInputFile
        self._outputFile = thisOutputFile
        self._condition = thisCondition
        self._debug = thisDebug

    def _readData(self, filename):
        '''
        Private method to open a file and read its data
        :param filename: string: name of file
        :return: a list of strings: data read from file
        '''
        with open(filename) as fp:
            data = fp.readlines()
        return data

    def readTargetData(self):
        '''
        Public method which allows to read  data from the object's target input file.
        :return: a list of strings: data read from file
        '''
        targetData = self._readData(self._thisTargetInputFile)
        return targetData

    def readNonTargetData(self):
        '''
        Public method which allows to read data from the object's non target input file.
        :return: a list of strings: data read from file
        '''
        nonTargetData = self._readData(self._thisNonTargetInputFile)
        return nonTargetData

    def _reformat(self, data, truth):
        '''
        Reformat data read from file into bioplot format.
        :param data: list of strings: data read from raw data file
        :param truth: list of booleans: truth value (does the line show same speaker results)
        :return: a list of strings: reformatted data
        '''
        res = []
        for score in data:
            score = score.strip()
            new_format = "{} {} {} {} {} {} {}".format("1", "from_raw", "2", "from_raw", str(score), truth, self._condition)
            res.append(new_format)
            if self._debug:
                print(score)
        return res

    def _reformat_target(self, data):
        '''
        Private method to reformat the target data
        :param data: list of strings: input data
        :return: list of strings: reformatted input data
        '''
        return (self._reformat(data, "TRUE"))

    def _reformat_nontarget(self, data):
        '''
        Private method to reformat the non target data
        :param data: list of strings: input data
        :return: list of strings: reformatted input data
        '''
        return (self._reformat(data, "FALSE"))

    def write2file(self, data):
        '''
        Public method: write data to the class's output file
        :param data: list of strings: all data in one line
        :return: nothing
        '''
        self._write2file(self._outputFile, data)

    def _write2file(self, filename, data):
        '''
        Private method to write data to a file
        :param filename: string: filename
        :param data: list of strings: data to be written to a file
        :return: nothing
        '''
        with open(filename, 'wt') as fp:
            for datum in data:
                fp.write(datum + '\n')

    def reformat(self, data, type):
        '''
        Public method to reformat data
        :param data: list of strings: data to be reformatted
        :param type: list of strings: reformatted data
        :return: list of strings: reformatted data
        '''
        new_format = []
        if type == 'target':
            new_format = self._reformat_target(data)
        elif type == 'nontarget':
            new_format = self._reformat_nontarget(data)
        else:
            print('Unknown data type:', type)
        return new_format


def parseArguments():
    '''
    Parse arguments from command line
    :return: argparse object
    '''
    version = "0.1"
    progName = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        description="{} version {}, Copyright (C) 2017, Jos Bouten.".format(progName, version) + \
                    " This program converts a raw target and/or a raw non target score file to a input data file suitable for reading by {}.".format(
                        progName) +
                    " {} comes with ABSOLUTELY NO WARRANTY; for details run {} -h".format(progName, progName) +
                    " This is free software, and you are welcome to redistribute it " +
                    "under certain conditions; please read LICENSE.TXT supplied with this program. " +
                    "This program was written by Jos Bouten. " +
                    "You can contact me via josbouten at gmail dot com.", )
    parser.add_argument('-t', '--target_input', action="store", dest="target_inputfile", help="input file name",
                        required=True)
    parser.add_argument('-n', '--nontarget_input', action="store", dest="nontarget_inputfile", help="input file name",
                        required=True)
    parser.add_argument('-o', '--output', action="store", dest="outputfile", help="output file name", required=True)
    parser.add_argument('-l', '--label', action="store", dest="label", help="label for the data", type=str, default='test')

    return parser.parse_args()

if __name__ == '__main__':

    args = parseArguments()
    debug = False

    r = RawReader(args.target_inputfile, args.nontarget_inputfile, args.outputfile, args.label, debug)
    nonTargetData = r.readNonTargetData()
    targetData = r.readTargetData()
    reformattedTargetData = r.reformat(targetData, 'target')
    reformattedNonTargetData = r.reformat(nonTargetData, 'nontarget')
    allData = reformattedNonTargetData + reformattedTargetData
    r.write2file(allData)
