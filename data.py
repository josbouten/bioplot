#!/usr/bin/env python3.5

__author__ = 'drs. ing. Jos Bouten'

'''
    data.py

    Object used to extract target and non target scores from a database or results file.
    Produce zoo plot, ranking plot and/or accuracy plot from the results.
    Create target results file and non target results file for computation
    of e.g. EER or plot DET-curves etc.

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

# Author: drs. ing. J.S. Bouten
# August, September 2013

import sqlite3
import sys
from os import makedirs, path
import collections

from utils import singleSanitize, convert
from format import Format
from asyncwrite import AsyncWrite


class Data(Format):
    """
        Data object containing target and non target scores per test subject.
    """

    def __init__(self, thisConfig, thisTitle, thisThreshold, thisDataType, maxNrTargetSamplesPerLabel, maxNrNonTargetSamplesPerLabel, thisDebug=True, thisSources='database'):
        Format.__init__(self, thisDebug)
        self.config = thisConfig
        self._title = thisTitle
        self._defaultThreshold = thisThreshold
        self._dataType = thisDataType
        # Annotate _doves, _phantoms, _worms and _chameleons
        self._maxNrTargetSamplesPerLabel = maxNrTargetSamplesPerLabel
        self._maxNrNonTargetSamplesPerLabel = maxNrNonTargetSamplesPerLabel
        self.debug = thisDebug
        self._sources = thisSources
        self._format = Format(self.debug)

        self._plotType = None

        # Target scores per label and meta value pattern.
        self._targetScores = collections.defaultdict(list)
        # Number of targets per label.
        self._targetCnt = collections.Counter()
        # Non target scores per label and meta value pattern.
        self._nonTargetScores = collections.defaultdict(list)
        # Number of non targets per label.
        self._nonTargetCnt = collections.Counter()
        # Target scores per label.
        self._targetScores4Label = collections.defaultdict(list)
        self._targetScores4MetaValue = collections.defaultdict(list)
        # Non target scores per label.
        self._nonTargetScores4Label = collections.defaultdict(list)
        self._nonTargetScores4MetaValue = collections.defaultdict(list)
        self._results = collections.defaultdict(list)
        # Count which labels + condition exceed the maxNrTargetSamplesPerLabel
        # and maxNrNonTargetSamplesPerLabel
        self._targetScoresInExcess = collections.Counter()
        self._nonTargetScoresInExcess = collections.Counter()
        self._nrDistinctMetaDataValues = 0
        # Contains: { speakerId: metaDataValue }
        self._metaDataValues = collections.defaultdict(set)
        self._LabelsToShowAlways = []
        self._minimumScore = collections.defaultdict(dict)
        self._maximumScore = collections.defaultdict(dict)

        # Keep track of labels.
        self._targetLabels = set()
        self._nonTargetLabels = set()

        # Do we allow both scores (A vs B and B vs A) in a symmetric tests or only the first read?
        self._allowDups = self.config.getAllowDups()

        if self.debug:
            print('Data._source(s):')
            for el in self._sources:
                print(el)

        # If the user did not specify a filename, we assume a database as the source.
        if self._sources == 'database':
            print("You need to add some code for this to work!")
            # And remove the sys.exit(1) statement.
            #res = self._readFromDatabase()
            sys.exit(1)
        else:
            res = self._readFromFiles(self._sources)
        #
        # Choose between decoder for type of results.
        #
        if self._dataType == 'type3':
            self._decodeType3Results(res)
        elif self._dataType == 'type2':
            print("Type2 data is not supported anymore. Convert it to type3!")
            sys.exit(1)
        elif self._dataType == 'type1':
            self._decodeType1Results(res)
        else:
            print("Unknown data type, must be 'type1' or 'type3'.")
            sys.exit(1)

    def getMax(self):
        return self._maAll

    def getMin(self):
        return self._miAll

    def getMetaDataValues(self):
        return self._metaDataValues

    def getDefaultThreshold(self):
        return self._defaultThreshold

    def getResults(self):
        return self._results

    def getTargetScores(self):
        """
        :return: dict of target scores.
        """
        return self._targetScores

    def getTargetCnt(self):
        """
        :return: return dict containing target counts.
        """
        return self._targetCnt

    def getNonTargetScores(self):
        """
        :return: return dict of non target scores.
        """
        return self._nonTargetScores

    def getNonTargetCnt(self):
        """
        :return: return dict containing non target counts.
        """
        return self._nonTargetCnt

    def getTargetScoreValues(self):
        thisList = self.getTargetScores()
        return self._extractValues(thisList)

    def getNonTargetScoreValues(self):
        thisList = self.getNonTargetScores()
        return self._extractValues(thisList)

    def _extractValues(self, thisList):
        ret = []
        for el in list(thisList.values()):
            ret += el
        return ret

    def getTargetScores4MetaValue(self, metaValue):
        return self._targetScores4MetaValue[metaValue]

    def getTargetScores4Label(self, label):
        return self._targetScores4Label[label]

    def getTargetScores4AllLabels(self):
        return self._targetScores4Label

    def getLabelsWithTargetScores(self):
        return self._targetScores4Label

    def getLabelsWithNonTargetScores(self):
        return self._nonTargetScores4Label

    def getNonTargetScores4AllLabels(self):
        return self._nonTargetScores4Label

    def getLabelsAndScoresForMetaValue(self, data, metaValue):
        """
        :param data:    [{'a_#_conditionA': [('p', 2.3), ('p', -3.0), ('p', 1), ('q', 2.0), ('q', 0.1)]},
                         {'b_#_conditionA': [('p', 6.0), ('p', 1.0), ('q', 3.0)]}]
                         {'a_#_conditionB': [('p', 1.0), ('p', 2.0), ('q', 1.0), ('q', -1.2)]}]
        :param metaValue: 'conditionA'
        :return:  row = {'a': [('p', 2.3), ('p', -3.0), ('p', 1), ('q', 2.0), ('q', 0.1)]
                         'b': [('p', 6.0), ('p', 1.0), ('q', 3.0)] }
                  ...
        """
        row = collections.defaultdict(list)
        odata = collections.OrderedDict(sorted(list(data.items()), key=lambda x: x[0], reverse=True))
        for pattern in list(odata.keys()):
            thisMetaValue = self.getMetaFromPattern(pattern)
            if thisMetaValue == metaValue:
                label = self.getLabelFromPattern(pattern)
                row[label] += odata[pattern]
        return row

    def getNonTargetScores4MetaValue(self, metaValue):
        return self._nonTargetScores4MetaValue[metaValue]

    def getNonTargetScores4Label(self, label):
        return self._nonTargetScores4Label[label]

    def getTargetLabels(self):
        return list(self._targetLabels)

    def getNonTargetLabels(self):
        """
        Get non target labels from raw data input.
        Split target label field using the --- separator.
        The first part is the label, the second the name of the
        wav file / feature vector used in the experiment.

        :return: set of labels. Each label is of type str.

        """
        return list(self._nonTargetLabels)

    def getNrDistinctMetaDataValues(self):
        return self._nrDistinctMetaDataValues

    def setLabelsToShowAlways(self, theseLabels):
        tmp = []
        for label in theseLabels:
            tmp.append(label.strip())
        self._LabelsToShowAlways = tmp

    def getLabelsToShowAlways(self):
        return self._LabelsToShowAlways

    def getMaximumScore(self, meta):
        return self._maximumScore[meta]

    def getMinimumScore(self, meta):
        return self._minimumScore[meta]

    def compAverageScore(self, scores):
        """
        Compute average score from dict of scores.
        :param scores: dict containing list of scores for key = label
        :return: float: average score
        """
        tot = sum(scores)
        cnt = len(scores)
        avg = float(tot) / float(cnt)
        return avg

    def getTitle(self):
        return self._title

    def minMax(self, score, mi, ma):
        """
        Compute minimum and maximum value from a list of float scores.

        :param score: list of scores
        :return: minimum value and maximum value
        """
        mi = min(score, mi)
        ma = max(score, ma)
        return mi, ma

    def minMax2(self, scoreDict, label, mi, ma):
        """
        Compute minimum and maximum value from a list of scoreDicts.

        :param scoreDict: list of scores
        :param label: string
        :param mi: float: minimum input value
        :param ma: float: maximum input value
        :return: minimum value and maximum value
        """
        for key in list(scoreDict.keys()):
            if label in key:
                mi = min(scoreDict[key], mi)
                ma = max(scoreDict[key], ma)
        return mi, ma

    def _sanitize(self, l1, f1, l2, f2, score, truth, metaValue):
        """ Get rid of leading and trailing spaces.

        :param l1: string label
        :param f1: floating point number as a string
        :param l2: string label
        :param f2: floating point number as a string
        :param score: string floating point number
        :param truth: boolean as a string
        :param metaValue: string
        :return:
        """
        l1 = l1.strip()
        f1 = f1.strip()
        l2 = l2.strip()
        f2 = f2.strip()
        score = score.strip()
        truth = truth.strip()
        metaValue = metaValue.strip()
        return l1, f1, l2, f2, score, truth, metaValue

    def _decodeType3Results(self, res):
        """
        Decoder for cross identification type results file. Example of the format used:

        80374  0000000017133729a 80359 0000000016842970b 2.1088616847991943  FALSE META_VAL1
        148407 0000260007968376b 89823 0000000008087650a 0.33669018745422363 FALSE META_VAL1
        179408 03ea7cce-a192626a 80372 0000000016749939b 1.26323664188385    FALSE META_VAL2
        80344  0000000016888750a 80344 0000000015560933b 4.423274517059326   TRUE  META_VAL2
        etc.

        :param res: list of strings (text lines) of raw data resulting from a series of trials.
        Type 3 data contains 7 fields:
        field 1: string: label identifying a subject (training data)
        field 2: string: name of data file containing biometric features or raw data originating
                         from the subject denoted by field 1 used for training the test model
        field 3: string: label identifying a subject (test data)
        field 4: string: name of data file containing biometric features or raw data originating
                         from the subject denoted by field 3 used for training the reference model
        field 5: string: float value: score of trial
        field 6: boolean: ground truth
        field 7: string: meta data value for the trial
        Field 7 can be used to contrast experiments in the zoo plot.
        So if you have 2 experiments where you change one variable, when doing a cross
        identification test, the meta value can be used to group the experiment's scores.
        """

        totCnt = 0
        resCnt = 0
        # For type 3 scores we assume that the scores are (Log) Likelyhood Ratios ranging between 0 and +infinity.
        onlyOnce = set()
        revRepeatCnt = 0
        selfCnt = 0
        valuesCnt = collections.Counter()
        # Set max and min function for this type.
        self.getMaximum4ThisType = self.config.getMaximum4Type3
        self.getMinimum4ThisType = self.config.getMinimum4Type3
        # Scores are scalar float values.
        self._miAll = self.getMaximum4ThisType()
        self._maAll = self.getMinimum4ThisType()
        for line in res:
            if ',' in line:
                splitChar = ','
            else:
                splitChar = None
            try:
                l1, f1, l2, f2, score, truth, metaValue = line.split(splitChar)
                if splitChar:
                    l1, f1, l2, f2, score, truth, metaValue = self._sanitize(l1, f1, l2, f2, score, truth, metaValue)
            except Exception as e:
                print('Error in', line)
                print('Use either comma or space as separator.')
                print(e)
            else:
                # We want to sort the data when choosing colors.
                # Therefore we convert to numbers if possible
                # otherwise we assume string values.
                if type(metaValue) != str:
                    metaValue = convert(metaValue)

                # Keep track of distinct meta data values.
                valuesCnt[metaValue] += 1

                if not metaValue in self._minimumScore:
                    self._minimumScore[metaValue] = self.getMaximum4ThisType()
                    self._maximumScore[metaValue] = self.getMinimum4ThisType()
                l1_0 = l1 + '---' + f1
                l2_0 = l2 + '---' + f2
                # If the score is not numerical, then we skip everything.
                try:
                    score = float(score)
                except Exception as e:
                    print('Error in', line)
                    print(e)
                else:
                    if l1_0 == l2_0:
                        selfCnt += 1
                        # Selfies are not interesting and therefore skipped
                        continue
                    if not (l1_0, l2_0) in onlyOnce:
                        onlyOnce.add((l1_0, l2_0))
                    if not self._allowDups:
                        # We do not want to include an experiment twice,
                        # assuming that the scores are symmetric.
                        # This may not be the case!
                        if (l2_0, l1_0) in onlyOnce:
                            revRepeatCnt += 1
                            continue
                    resCnt += 1

                    # Keep track of labels associated with meta data values.
                    metaValue = str(metaValue)

                    pattern = l1 + self.LABEL_SEPARATOR + metaValue
                    # Keep track of results for ranking purposes.
                    # print 'adding element to results[', l1 + self.LABEL_SEPARATOR + metaValue, ']'
                    #self._results4Subject[metaValue, l1].append((l2, score))  # code is just for debugging

                    self._metaDataValues[metaValue].add(l1)
                    self._metaDataValues[metaValue].add(l2)
                    totCnt += 1
                    if truth.lower() == 'true':
                        if len(self._targetScores[pattern]) < self._maxNrTargetSamplesPerLabel:
                            self._targetScores[pattern].append(score)
                            self._targetScores4Label[l1].append(score)
                            self._targetScores4MetaValue[metaValue].append(score)
                            self._targetCnt[metaValue] += 1
                            self._targetLabels.add(l1)
                            self._results[pattern].append((l2, score))
                            self._miAll = min(self._miAll, score)
                            self._maAll = max(self._maAll, score)
                            self._minimumScore[metaValue] = min(self._minimumScore[metaValue], score)
                            self._maximumScore[metaValue] = max(self._maximumScore[metaValue], score)
                        else:
                            self._targetScoresInExcess[pattern] += 1

                    else:
                        if len(self._nonTargetScores[pattern]) < self._maxNrNonTargetSamplesPerLabel:
                            self._nonTargetScores[pattern].append(score)
                            self._nonTargetScores4Label[l1].append(score)
                            self._nonTargetScores4MetaValue[metaValue].append(score)
                            self._nonTargetCnt[metaValue] += 1
                            self._nonTargetLabels.add(l1)
                            self._results[pattern].append((l2, score))
                            self._miAll = min(self._miAll, score)
                            self._maAll = max(self._maAll, score)
                            self._minimumScore[metaValue] = min(self._minimumScore[metaValue], score)
                            self._maximumScore[metaValue] = max(self._maximumScore[metaValue], score)
                        else:
                            self._nonTargetScoresInExcess[pattern] += 1
        # If there is too much data for a given label / metaValue, tell the user now that it was skipped
        if len(self._targetScoresInExcess) > 0:
            print("Skipped the following number of target samples because the number for the label exceeds {} ".format(
                self._maxNrTargetSamplesPerLabel))
            for key in sorted(self._targetScoresInExcess):
                print("{:>5} {}".format(self._targetScoresInExcess[key], key))
        if len(self._nonTargetScoresInExcess) > 0:
            print("Skipped the following number of non target samples because the number for the label exceeds {} ".format(
                self._maxNrNonTargetSamplesPerLabel))
            for key in sorted(self._nonTargetScoresInExcess):
                print("{:>5} {}".format(self._nonTargetScoresInExcess[key], key))

        if self.debug:
            print('Number of results in file:', resCnt)
            #print('Number of subjects:', len(self._results4Subject))
        print('Number of scores:', totCnt)
        if totCnt == 0:
            print('No scores were found. Maybe the dataType is not set correctly.')
            print("DataType is '%s'" % self._dataType)
            print('Is this correct?')
            sys.exit(1)
        print("Number of target and non target scores for: ")
        maxLen = 0
        for metaValue in self._nonTargetCnt:
            maxLen = max(maxLen, len(metaValue))
        template = "{:<%d}" % maxLen
        scoreLen = len(str(self.compLen(self._nonTargetScores)))
        template += " {:>%d} {:>%d}" % (scoreLen + 1, scoreLen + 1)

        for metaValue in self._targetCnt:
            #print("{:<10} {:>7} {:>7}".format(metaValue, self._targetCnt[metaValue], self._nonTargetCnt[metaValue]))
            print(template.format(metaValue, self._targetCnt[metaValue], self._nonTargetCnt[metaValue]))
        # print("Number of non target scores for: ")

        print(template.format("Total", self.compLen(self._targetScores), self.compLen(self._nonTargetScores)))
        # print('Total number of target scores:', self.compLen(self._targetScores))
        # print('Total number of non target scores:', self.compLen(self._nonTargetScores))
        print('Number of repeats (multiple instances of same data in input):', revRepeatCnt)
        print('Number of selfies (A vs A):', selfCnt)
        self._nrDistinctMetaDataValues = len(self._metaDataValues)
        print('Nr of distinct meta data values:', self._nrDistinctMetaDataValues)

    def _decodeType1Results(self, res):
        """
        This function is a stub.
        You need to convert the type1 data read from the database
        here and convert it to the type3 format.
        Then call _decodeType3Results(res)

        :param res:
        :return:
        """
        ret = []
        for line in res:
            # Do your type1 to type3 conversion here
            ret.append(line)
        # Finally call the Type3 decoder
        self._decodeType3Results(ret)
        return ret

    def compLen(self, scoreDict):
        """

        Compute the total length of the  values
        stored in scoreDict

        :param scoreDict: key = string: label, value = float: score
        :return: int: total length

        """
        tot = 0
        for k in list(scoreDict.keys()):
            tot += len(scoreDict[k])
        return tot

    def _readFromDatabase(self):
        """
        This function contains some (incomplete) example code in case you want to read
        data from a database. It is suggested to add some code here which does the following:
        1: connect to the database
        2: read the data from the database and concatenate the data elements separated by spaces
        so that you end up with a list of lines.
        3: then exit this function
        4: In _decodeType1Results transform the lines to the Type3 format and call _decodeType3Results there.

        :return: list of lines containing data elements separated by spaces.
        """
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        res = c.execute("SELECT ProbeId, GalleryId, Score FROM crossidentificationresults")
        # Note: ProbeId = label1 corresponding to a test model
        # GalleryId = label2 corresponding to a training model
        # Score = distance measure / score between label1 and label2
        return res

    def _readFromFiles(self, filenames):
        """
        Read raw lines of text from a text file.
        Strip lines of CR/LF
        :param filename: string: name of file containing text
        :return: list of strings
        """
        def readFromFile(filename):
            try:
                f = open(filename, 'r')
                lines = f.readlines()
                f.close()
                res = []
                for line in lines:
                    res.append(line.strip())
                return res
            except IOError as e:
                print(e)
                sys.exit(1)

        ret = []
        for filename in filenames:
            print("Reading data from: {}".format(filename))
            ret = ret + readFromFile(filename)
        return ret


    def writeScores2file(self, scoreDict, expName, extention):
        """
        Write scores to a file
        :param scoreDict: dict of scores, key = label
        :param expName: string used as part of the file name
        :param extention: string used as file extention
        :return: not a thing
        """
        dataOutputPath = self.config.getOutputPath()
        k = list(scoreDict.keys())
        try:
            if not path.exists(dataOutputPath):
                makedirs(dataOutputPath)
        except Exception as e:
            print('writeScores2file', e)
            sys.exit(1)

        scoresPerMetaValue = collections.defaultdict(list)
        for el in k:
            scores = scoreDict[el]
            metaValue = self._format.getMetaFromPattern(el)
            scoresPerMetaValue[metaValue].append(scores)
        for metaValue in scoresPerMetaValue:
            scores = scoresPerMetaValue[metaValue]
            filename = dataOutputPath + path.sep + expName + '_' + metaValue + extention
            # We do not like spaces in file names.
            # Sorry windows dudes and dudettes !
            filename = singleSanitize(filename)
            if self.config.getAllwaysSave():
                background = AsyncWrite(filename, scores, self.debug)
                background.start()
                background.join()
            else:
                if not path.exists(filename):
                    background = AsyncWrite(filename, scores, self.debug)
                    background.start()
                    background.join()
                else:
                    print("File %s already exists." % filename)
