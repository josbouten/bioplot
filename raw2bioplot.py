#!/usr/bin/env python3

import sys
import os.path
import argparse

"""
This program will convert raw score files to a format that can be read by bioplot.
Most of the plots require target and non target scores. You can however make a histogram from one set of scores.
Therefore it is not required to supply target and non target scores.
"""


class RawReader:
    def __init__(self, thisTargetInputFile, thisNonTargetInputFile, thisOutputFile, thisCondition, thisDebug):
        self._thisTargetInputFile = thisTargetInputFile
        self._thisNonTargetInputFile = thisNonTargetInputFile
        self._outputFile = thisOutputFile
        self._condition = thisCondition
        self._debug = thisDebug

    def _readData(self, filename):
        with open(filename) as fp:
            data = fp.readlines()
        return data

    def readTargetData(self):
        targetData = self._readData(self._thisTargetInputFile)
        return targetData

    def readNonTargetData(self):
        nonTargetData = self._readData(self._thisNonTargetInputFile)
        return nonTargetData

    def _reformat(self, data, truth):
        res = []
        for score in data:
            score = score.strip()
            new_format = "{} {} {} {} {} {} {}".format("1", "bla", "2", "bla", str(score), truth, self._condition)
            res.append(new_format)
            if self._debug:
                print(score)
        return res

    def _reformat_target(self, data):
        return (self._reformat(data, "TRUE"))

    def _reformat_nontarget(self, data):
        return (self._reformat(data, "FALSE"))

    def write2file(self, data):
        self._write2file(self._outputFile, data)

    def _write2file(self, filename, data):
        with open(filename, 'wt') as fp:
            for datum in data:
                fp.write(datum + '\n')

    def reformat(self, data, type):
        new_format = []
        if type == 'target':
            new_format = self._reformat_target(data)
        elif type == 'nontarget':
            new_format = self._reformat_nontarget(data)
        else:
            print('Unknown data type:', type)
        return new_format


if __name__ == '__main__':
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

    args = parser.parse_args()

    debug = False

    r = RawReader(args.target_inputfile, args.nontarget_inputfile, args.outputfile, args.label, debug)
    nonTargetData = r.readNonTargetData()
    targetData = r.readTargetData()
    reformattedTargetData = r.reformat(targetData, 'target')
    reformattedNonTargetData = r.reformat(nonTargetData, 'nontarget')
    allData = reformattedNonTargetData + reformattedTargetData
    r.write2file(allData)
