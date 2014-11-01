#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''
    data.py

    Object used to extract target and non target scores from a database or results file.
    Produce zoo plot, ranking plot and/or accuracy plot from the results.
    Create target results file and non target results file for computation
    of e.g. EER or plot DET-curves etc.




    Copyright (C) 2014 Jos Bouten ( josbouten@gmail.com )

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
# email: josbouten@gmail.com

_author_ = 'drs. ing. Jos Bouten'

import sqlite3
import sys

from os import makedirs, path
import collections

from utils import sanitize, convert
from format import Format

class Data(Format):
    '''
        Data object containing target and non target scores per test picture.
    '''

    def __init__(self, config, title, threshold, dataType, debug=True, source='database'):
        Format.__init__(self, debug)
        self._title = title
        self.config = config
        self._defaultThreshold = threshold
        self._dataType = dataType
        self._plotType = None
        self._format = Format(self.debug)

        # Annotate doves, phantoms, worms and chameleons
        self.debug = debug
        self._source = source

        # target scores per label and meta value pattern
        self._targetScores = collections.defaultdict(list)
        # non target scores per label and meta value pattern
        self._nonTargetScores = collections.defaultdict(list)
        # target scores per label
        self._targetScores4Label = collections.defaultdict(list)
        # non target scores per label
        self._nonTargetScores4Label = collections.defaultdict(list)
        self._results = collections.defaultdict(list)
        self._resultsOrg = collections.defaultdict(list)
        self._nrDistinctMetaDataValues = 0
        # contains: { speakerId: metaDataValue }
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
            print 'Data._source:', self._source

        if self._source == 'database':
            res = self._readFromDatabase()
        else:
            res = self._readFromFile(self._source)
        #
        # Choose between decoder for type of results.
        #
        if self._dataType == 'type3':
            self.scores = self._decodeType3Results(res)
        elif self._dataType == 'type2':
            self.scores = self._decodeType2Results(res)
        elif self._dataType == 'type1':
            self.scores = self._decodeType1Results(res)
        else:
            print "Unknown data type, must be 'type1, type2 or type3'"
            sys.exit(1)

    def getMax(self):
        return self._ma

    def getMin(self):
        return self._mi

    def getMetaDataValues(self):
        return self._metaDataValues

    def getDefaultThreshold(self):
        return self._defaultThreshold

    def getResults(self):
        return self._results

    def getResultsOrg(self):
        return self._resultsOrg

    def getTargetScores(self):
        '''
        :return: dict of target scores. Key = label
        '''
        return self._targetScores

    def getNonTargetScores(self):
        '''
        :return: return dict of non target scores. Key = label
        '''
        return self._nonTargetScores

    def getTargetScoreValues(self):
        thisList = self.getTargetScores()
        return self._extractValues(thisList)

    def getNonTargetScoreValues(self):
        thisList = self.getNonTargetScores()
        return self._extractValues(thisList)

    def _extractValues(self, thisList):
        ret = []
        for el in thisList.values():
            ret += el
        return ret

    def getTargetScores4Label(self, label):
        return self._targetScores4Label[label]

    def getLabelsWithTargetScores(self):
        return self._targetScores4Label

    def getLabelsWithNonTargetScores(self):
        return self._nonTargetScores4Label

    def getLabelsAndScoresForMetaValue(self, data, metaValue):
        '''
        :param data:    [{'a_#_conditionA': [('p', 2.3), ('p', -3.0), ('p', 1), ('q', 2.0), ('q', 0.1)]},
                         {'b_#_conditionA': [('p', 6.0), ('p', 1.0), ('q', 3.0)]}]
                         {'a_#_conditionB': [('p', 1.0), ('p', 2.0), ('q', 1.0), ('q', -1.2)]}]
        :param metaValue: 'conditionA'
        :return:  row = {'a': [('p', 2.3), ('p', -3.0), ('p', 1), ('q', 2.0), ('q', 0.1)]
                         'b': [('p', 6.0), ('p', 1.0), ('q', 3.0)] }
                  ...
        '''
        row = collections.defaultdict(list)
        odata = collections.OrderedDict(sorted(data.items(), key=lambda x: x[0], reverse=True))
        for pattern in odata.keys():
            thisMetaValue = self.getMetaFromPattern(pattern)
            if thisMetaValue == metaValue:
                label = self.getLabelFromPattern(pattern)
                row[label] += odata[pattern]
        return row

    def getNonTargetScores4Label(self, label):
        return self._nonTargetScores4Label[label]

    def getTargetLabels(self):
        return list(self._targetLabels)

    def getNonTargetLabels(self):
        '''
        Get non target labels from raw data input.
        Split target label field using the --- separator.
        The first part is the label, the second the name of the
        wav file / feature vector used in the experiment.

        :return: set of labels. Each label is of type str.

        '''
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
        '''
        Compute average score from dict of scores
        :param scores: dict containing list of scores for key = label
        :return: float: average score
        '''
        tot = sum(scores)
        cnt = len(scores)
        avg = float(tot) / float(cnt)
        return avg

    def getTitle(self):
        return self._title

    def minMax(self, score, mi, ma):
        '''
        Compute minimum and maximum value from a list of scores.

        :param scoreList: list of scores
        :return: minimum value and maximum value
        '''
        mi = min(score, mi)
        ma = max(score, ma)
        return mi, ma

    def _sanitize(self, l1, f1, l2, f2, score, truth, metaValue):
        l1 = l1.strip()
        f1 = f1.strip()
        l2 = l2.strip()
        f2 = f2.strip()
        score = score.strip()
        truth = truth.strip()
        metaValue = metaValue.strip()
        return l1, f1, l2, f2, score, truth, metaValue

    def _decodeType3Results(self, res):
        '''
        Decoder for cross identification type results file. Example of the format used:

        80374 0000000017133729a 80359 0000000016842970b 2.1088616847991943 FALSE META_VAL1
        148407 0000260007968376b 89823 0000000008087650a 0.33669018745422363 FALSE META_VAL1
        179408 03ea7cce-a192626a 80372 0000000016749939b 1.26323664188385 FALSE META_VAL2
        80344 0000000016888750a 80344 0000000015560933b 4.423274517059326 TRUE META_VAL2
        etc.

        :param res: list of strings (text lines) of raw data resulting from a series of trials.
        Type 3 data contains 7 fields:
        field 1: string: label identifying a person (training data)
        field 2: string: name of data file containing biometric features or raw data originating
                         from the person denoted by field 1 used for training the test model
        field 3: string: label identifying a person (test data)
        field 4: string: name of data file containing biometric features or raw data originating
                         from the person denoted by field 3 used for training the reference model
        field 5: string: float value: score of trial
        field 6: string: meta data value for the trial
        Field 6 can be used to contrast experiments in the zoo plot.
        So if you have 2 experiments where you change one variable, when doing a cross
        identification test, the meta value can be used to group the experiment's scores.
        '''

        totCnt = 0
        targetCnt = collections.Counter()
        nonTargetCnt = collections.Counter()
        resCnt = 0
        selfCnt = 0
        # We assume that the scores are Log Likelyhood Ratios ranging between 0 and +infinity
        self._mi = self.config.getMaximum4Type3()
        self._ma = self.config.getMinimum4Type3()
        onlyOnce = set()
        revRepeatCnt = 0
        selfCnt = 0
        valuesCnt = collections.Counter()
        # Set max and min function for this type
        self.getMaximum4ThisType = self.config.getMaximum4Type3
        self.getMinimum4ThisType = self.config.getMinimum4Type3
        # Scores are scalar float values.
        self._mi = self.getMaximum4ThisType()
        self._ma = self.getMinimum4ThisType()
        for line in res:
            #print 'line:', lineA
            if ',' in line:
                splitChar = ','
            else:
                splitChar = None
            try:
                l1, f1, l2, f2, score, truth, metaValue = line.split(splitChar)
                if splitChar:
                    l1, f1, l2, f2, score, truth, metaValue = self._sanitize(l1, f1, l2, f2, score, truth, metaValue)
            except Exception, e:
                print e, line
            else:
                # We want to sort the data when choosing colors
                # Therefore we convert to numbers if possible
                # otherwise we assume string values.

                metaValue = convert(metaValue)

                # keep track of distinct meta data values
                valuesCnt[metaValue] += 1

                if not metaValue in self._minimumScore:
                    self._minimumScore[metaValue] = self.config.getMaximum4Type3()
                    self._maximumScore[metaValue] = self.config.getMinimum4Type3()
                l1_0 = l1 + '---' + f1
                l2_0 = l2 + '---' + f2
                score = float(score)
                self._mi = min(self._mi, score)
                self._ma = max(self._ma, score)
                self._minimumScore[metaValue] = min(self._minimumScore[metaValue], score)
                self._maximumScore[metaValue] = max(self._maximumScore[metaValue], score)

                if l1_0 == l2_0:
                    selfCnt += 1
                    #print 'totally equal', line
                    # Selfies are not interesting and therefore skipped
                    # continue
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
                self._results[pattern].append((l2, score))
                self._resultsOrg[l1].append((l2, score))

                self._metaDataValues[metaValue].add(l1)
                self._metaDataValues[metaValue].add(l2)
                totCnt += 1
                if truth.lower() == 'true':
                    self._targetScores[pattern].append(score)
                    self._targetScores4Label[l1].append(score)
                    targetCnt[metaValue] += 1
                    self._targetLabels.add(l1)
                else:
                    self._nonTargetScores[pattern].append(score)
                    self._nonTargetScores4Label[l1].append(score)
                    nonTargetCnt[metaValue] += 1
                    self._nonTargetLabels.add(l1)
        if self.debug:
            print 'Number of results in res:', resCnt
            print 'Number of persons:', len(self._resultsOrg)
        print 'Number of scores:', totCnt
        if totCnt == 0:
            print 'No scores were found. Maybe dataType is not set correctly.'
            print "DataType is '%s'" % self._dataType
            print 'Is this correct?'
            sys.exit(1)
        print 'Number target scores:', self._compLen(self._targetScores)
        print 'Number non target scores:', self._compLen(self._nonTargetScores)
        print 'Number of repeats:', revRepeatCnt
        print 'Number of selfies:', selfCnt
        self._nrDistinctMetaDataValues = len(self._metaDataValues)
        print 'Nr of distinct meta data values:', self._nrDistinctMetaDataValues
        if self.debug:
            print 'mi, ma:', self._mi, self._ma

    def _decodeType2Results(self, res):
        '''
        Yet another results format
        :param results:
        :return:
        '''
        targetCnt = 0
        nonTargetCnt = 0
        totCnt = 0
        allTests = set()
        dCnt = 0
        skipCnt = 0
        selfCnt = 0
        valuesCnt = collections.Counter()
        self.valueCounter = set()
        metaValue = 'M1'
        # set max and min function for this type
        self.getMaximum4ThisType = self.config.getMaximum4Type2
        self.getMinimum4ThisType = self.config.getMinimum4Type2
        # Scores are scalar float values.
        self._mi = self.getMaximum4ThisType()
        self._ma = self.getMinimum4ThisType()
        for line in res:
            # Results may look like this:
            #
            # EC_xxx_yyy_19630516_1,EC_xxx_yyy_19630516_1,1,1
            # EC_xxx_yyy_19630516_1,EC_aaa_bbb_19771219_4,0.359354,2
            # EC_xxx_yyy_19630516_1,EC_ccc_ddd_19560109_23,0.302631,3
            # EC_xxx_yyy_19630516_1,RC_ccc_ddd_19560109_91,0.298384,4
            # Target and test segment names differ only in prefix: EC_aa_1 vs RC_aa_1
            #
            # Note, EC_aa_2 does not exits. Only the aa bit will change from target to target.
            #
            p, g, score, n = line.split(',')
            score = float(score)
            if p[0] == 'R':  # we only need the results of Exx vs Ryy, so we exclude doubles like Ryy vs Exx
                skipCnt += 1
            else:
                tmp = p.split('_')
                po = p
                p = tmp[1] + '_' + tmp[2] + '_' + tmp[3]
                tmp = g.split('_')
                go = g
                g = tmp[1] + '_' + tmp[2] + '_' + tmp[3]
                # We want each test result to be used only once.
                if (po, go) in allTests:
                    dCnt += 1
                else:
                    # Keep track of results for ranking purposes.
                    self._results[p].append((g, score))
                    self._resultsOrg[p].append((g, score))
                    valuesCnt[metaValue] += 1
                    #self._results[p].append((g, score))
                    self._resultsOrg[p].append((g, score))
                    if self.debug:
                        print 'p[1:]', p[1:], 'g:', g
                    allTests.add((po, go))

                    self._metaDataValues[p] = metaValue
                    self.valueCounter.add(metaValue)
                    valuesCnt[metaValue] += 1

                    totCnt += 1
                    # Keep track of labels and meta data values.
                    pattern = p + self.LABEL_SEPARATOR + str(metaValue)

                    self._mi = min(self._mi, score)
                    self._ma = max(self._ma, score)
                    if p[1:] in g:
                        if po != go:  # we want to exclude scores for which p = g
                            if self.debug:
                                print 'target:', po, go, score
                            self._targetScores[pattern].append(score)
                            self._targetScores4Label[p].append(score)
                            targetCnt[pattern] += 1
                            self._targetLabels.add(p)
                        else:
                            if self.debug:
                                print 'self:', po, go, score
                            selfCnt += 1
                    else:  # This is a non target test result.
                        if self.debug:
                            print 'nontarget:', po, go, score
                        self._nonTargetScores[p + self.LABEL_SEPARATOR + pattern].append(score)
                        self._nonTargetScores4Label[p].append(score)
                        nonTargetCnt[pattern] += 1
                        self._nonTargetLabels.add(p)

        if self.debug:
            print 'Number of lines:', len(res)
        print 'Number of scores:', totCnt
        if totCnt == 0:
            print 'No scores were found. Maybe dataType is not set correctly.'
            print "dataType is '%s'" % self._dataType
            print 'Is this correct?'
            sys.exit(1)
        print 'Number of doubles:', dCnt
        print 'Number of skipped (train) scores:', skipCnt
        print 'Number of target and non target scores:', targetCnt + nonTargetCnt
        print 'Number of self scores:', selfCnt
        print 'Number target scores:', self._compLen(self._targetScores)
        print 'Number non target scores:', self._compLen(self._nonTargetScores)
        self.nrDistinctMetaDataValues = len(self.valueCounter)


    def _decodeType1Results(self, res):
        '''
        Extract scores from type1 results.
        Example of some results in res
        62124-0 62124-0 1.0 M1
        62124-0 62124-1 0.383234709501 M1
        62124-0 62124-3 0.325683742762 M1
        62124-0 80491-2 0.239269435406 M1
        62124-0 64568-2 0.19219391048 M1
        62124-0 64568-3 0.125796630979 M1
        62124-0 77223-1 0.0895956531167 M1

        Decoding these must be done by splitting the fields.
        Target and non target scores can be detected by comparing
        the first fields of the label names prior to the '-':

        62124-0 62124-0 1.0 M1              -> self test
        62124-0 62124-1 0.383234709501 M1   -> target test
        62124-0 62124-3 0.325683742762 M1   -> target test
        62124-0 80491-2 0.239269435406 M1   -> non target test
        62124-0 64568-2 0.19219391048 M1    -> non target test
        62124-0 64568-3 0.125796630979 M1   -> non target test
        62124-0 77223-1 0.0895956531167 M1  -> non target test

        :param res: list of strings containing results
        :return:
        '''

        totCnt = 0
        targetCnt = collections.Counter()
        nonTargetCnt = collections.Counter()
        resCnt = 0
        selfCnt = 0
        # set max and min function for this type
        self.getMaximum4ThisType = self.config.getMaximum4Type1
        self.getMinimum4ThisType = self.config.getMinimum4Type1
        valuesCnt = collections.Counter()
        self._metaDataValues = collections.defaultdict(set)
        self.valueCounter = set()
        allTests = set()
        dCnt = 0
        # A meta data value is added here since the databse of the use case I took this
        # example from did not supply one.
        metaValue = 'M1'
        # Scores are scalar float values.
        self._mi = self.getMaximum4ThisType()
        self._ma = self.getMinimum4ThisType()
        for p, g, score in res:
            resCnt += 1
            #
            po = p
            go = g
            if (p, g) in allTests:
                dCnt += 1
            else:
                score = float(score)
                self._mi = min(self._mi, score)
                self._ma = max(self._ma, score)
                self._minimumScore[metaValue] = min(self._minimumScore[metaValue], score)
                self._maximumScore[metaValue] = max(self._maximumScore[metaValue], score)

                tmp = p.split('-')
                p = tmp[0]
                tmp = g.split('-')
                g = tmp[0]
                # We want each test result to be used only once.
                allTests.add((p, g))

                pattern = p + self.LABEL_SEPARATOR + metaValue
                #self._results[pattern].append((g, score))
                self._results[pattern].append((g, score))
                self._resultsOrg[p].append((g, score))

                # Keep track of distinct meta data values.
                self._metaDataValues[metaValue].add(p)
                self._metaDataValues[metaValue].add(g)
                self.valueCounter.add(metaValue)
                valuesCnt[metaValue] += 1

                totCnt += 1
                if p == g:
                    if po != go:
                        self._targetScores[pattern].append(score)
                        self._targetScores4Label[p].append(score)
                        targetCnt[metaValue] += 1
                        self._targetLabels.add(p)
                    else:
                        selfCnt += 1
                else:
                    self._nonTargetScores[pattern].append(score)
                    self._nonTargetScores4Label[p].append(score)
                    nonTargetCnt[metaValue] += 1
                    self._nonTargetLabels.add(p)

        if self.debug:
            print 'data.mi:', self._mi
            print 'data.ma:', self._ma

        print 'Number of results in db:', resCnt
        if self.debug:
            print 'Number of results used:', self._compLen(self._resultsOrg)
        if totCnt == 0:
            print 'No scores were found. Maybe dataType is not set correctly.'
            print "DataType is '%s'" % self._dataType
            print 'Is this correct?'
            sys.exit(1)
        print 'Number of doubles:', dCnt
        print 'Number of selfies:', selfCnt
        print 'Number target scores:', self._compLen(self._targetScores)
        print 'Number non target scores:', self._compLen(self._nonTargetScores)
        self._nrDistinctMetaDataValues = len(self._metaDataValues)
        print 'Nr of distinct meta data values:', self._nrDistinctMetaDataValues
        if self.debug:
            print 'valueCounter:', valuesCnt

    def _compLen(self, scoreDict):
        '''

        Compute the total length of the  values
        stored in scoreDict

        :param scoreDict: key = string: label, value = float: score
        :return: int: total length

        '''
        tot = 0
        for k in scoreDict.keys():
            tot += len(scoreDict[k])
        return tot

    def _readFromDatabase(self):
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        res = c.execute("SELECT ProbeId, GalleryId, Score FROM crossidentificationresults")
        # Note: ProbeId = label1 corresponding to a test model
        # GalleryId = label2 corresponding to a training model
        # Score = distance measure / score between label1 and label2
        return res

    def _readFromFile(self, filename):
        '''
        Read raw lines of text from a text file.
        Strip lines of CR/LF
        :param filename: string: name of file containing text
        :return: list of strings
        '''
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            f.close()
            res = []
            for line in lines:
                res.append(line.strip())
            return res
        except IOError, e:
            print 'Data.readFromFile:', e
            sys.exit(1)

    def writeScores2file(self, scoreDict, expName, extention):
        '''
        Write scores to a file
        :param scoreDict: dict of scores, key = label
        :param filename: string, name of file to write data to
        :return: not a thing
        '''
        dataOutputPath = self.config.getOutputPath()
        k = scoreDict.keys()
        try:
            if not path.exists(dataOutputPath):
                makedirs(dataOutputPath)
        except Exception, e:
            print 'writeScores2file', e
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
            filename = sanitize(filename)
            if not path.exists(filename):
                if self.debug:
                    print 'data.writeScores2file:writing to:', filename
                try:
                    f = open(filename, 'w')
                    for score in scores:
                        f.write("%s\n" % str(score))
                    f.close()
                except IOError, e:
                    print e
                    sys.exit(1)
            else:
                print "File %s already exists." % (filename)
