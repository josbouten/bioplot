__author__ = 'drs. ing. Jos Bouten'

'''
    matrixdata.py

    class MatrixData is an object which can be used to test the matrix
    plot routine in matrix.py

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

    Example of data (principle):
    [
        {'label0_#_conditionA': [('p', 2.3), ('p', -3.0), ('p', 1.6), ... 20 values, ('q', 2.0), ('q', 0.1) ... 20 values, ('r', 0.1) ... 20 values, etc]},
        {'label1_#_conditionA': [('p', 2.3), ('p', 3.0),  ('p', 1.8), ... 20 values, ('q', 1.2), ('q', 1.1) ... 20 values, ('r', 0.9) ... 20 values, etc]},
        ...
        {'labelN_#_conditionA' [('p', 1.1), ('p', -2.0), ('p', 1.1), ... 20 values, ('q', 2.2), ('q', 2.1) ... 20 values, ('r', 1.1) ... 20 values, etc]},

        {'label0_#_conditionB': [('p', 1.3), ('p', -3.2), ('p', 1.2), ... 20 values, ('q', 1.0), ('q', 1.1) ... 20 values, ('r', 1.4) ... 20 values, etc]},
        {'label1_#_conditionB': [('p', 3.3), ('p', 3.3),  ('p', 1.1), ... 20 values, ('q', 3.2), ('q', 4.1) ... 20 values, ('r', 0.1) ... 20 values, etc]},
        ...
        {'labelN_#_conditionB' [('p', 0.1), ('p', -2.3), ('p', 1.4), ... 20 values, ('q', 1.2), ('q', 0.1) ... 20 values, ('r', 1.1) ... 20 values, etc]}
    ]
'''

import collections
from random import random
from format import Format

class MatrixData(Format):
    def __init__(self, thisConfig, thisDebug=True):
        self.debug = thisDebug
        Format.__init__(self, self.debug)
        self._config = thisConfig
        # N must be bigger than 3 otherwise the matrix will be all white.
        self._N = 4
        self._metaValues = ['condA', 'condB', 'condC', 'condD', 'condE', 'condF']
        #self._metaValues = ['condA']
        self.getMaximum4ThisType = self._config.getMaximum4Type3
        self.getMinimum4ThisType = self._config.getMinimum4Type3
        self._ma = self.getMinimum4ThisType()
        self._mi = self.getMaximum4ThisType()
        self._data = collections.defaultdict(list)
        self._title = 'dummy test title for matrix data'

    def getTitle(self):
        return self._title


    def makeRandomMatrix(self, rand=True):
        """
        Make a matrix containing scores for test purposes.
        Choose a different range of scores per metaValue by incrementing
        scores for successive meta values with 1.0

        :param rand: If set to True, generate random scores, if set to false,
        all scores will be the same per meta value.

        :return: a matrix of dicts containing self._N dict keys
        The value for each key is a list of self._N (label score) tuples.
        Note: scores will differ by 1.0 between meta values.

        Example of data assuming 2 meta data values: conditionA and conditionB:
        [
            {'label0_#_conditionA': [('p', 2.3), ('p', -3.0), ('p', 1.6), ... 20 values, ('q', 2.0), ('q', 0.1) ... 20 values, ('r', 0.1) ... 20 values, etc]},
            {'label1_#_conditionA': [('p', 2.3), ('p', 3.0),  ('p', 1.8), ... 20 values, ('q', 1.2), ('q', 1.1) ... 20 values, ('r', 0.9) ... 20 values, etc]},
            ...
            {'labelN_#_conditionA' [('p', 1.1), ('p', -2.0), ('p', 1.1), ... 20 values, ('q', 2.2), ('q', 2.1) ... 20 values, ('r', 1.1) ... 20 values, etc]},

            {'label0_#_conditionB': [('p', 1.3), ('p', -3.2), ('p', 1.2), ... 20 values, ('q', 1.0), ('q', 1.1) ... 20 values, ('r', 1.4) ... 20 values, etc]},
            {'label1_#_conditionB': [('p', 3.3), ('p', 3.3),  ('p', 1.1), ... 20 values, ('q', 3.2), ('q', 4.1) ... 20 values, ('r', 0.1) ... 20 values, etc]},
            ...
            {'labelN_#_conditionB' [('p', 0.1), ('p', -2.3), ('p', 1.4), ... 20 values, ('q', 1.2), ('q', 0.1) ... 20 values, ('r', 1.1) ... 20 values, etc]}
        ]

        """
        baseScore = 1.0
        metaValueScoreOffset = 0.0
        for metaValue in self._metaValues:
            # Choose a different range of scores per metaValue.
            metaValueScoreOffset += 1.0
            for i in range(self._N):
                pattern = "p%03d%s%s" % (i, self.LABEL_SEPARATOR, metaValue)
                for j in range(self._N):
                    label2 = "q%02d" % j
                    #for x in range(int(self._N * random())):
                    for x in range(self._N):
                        if rand:
                            score = random() + metaValueScoreOffset
                        else:
                            score = baseScore + metaValueScoreOffset
                        self._mi = min(self._mi, score)
                        self._ma = max(self._ma, score)
                        self._data[pattern].append((label2, score))
        pass

    def dumpMatrix(self, matrix, metaValue):
        """
        # Save matrix in a text file ( for debug purposes ).
        :param matrix: matrix of labels and label, scores tuples.
        :param metaValue: value used to distinguish between experimental conditions
        :return:
        """
        try:
            f = open("matrix_%s.txt" % metaValue, 'wt')
        except Exception, e:
            print e
        else:
            (x, y) = matrix.shape
            for i in range(x):
                for j in range(y):
                    f.write("%f " % matrix[i, j])
                f.write("\n")
            f.close()

    def getLabelsAndScoresForMetaValue(self, data, metaValue):
        """
        :param data:    [{'a_#_conditionA': [('p', 2.3), ('p', -3.0), ('p', 1), ('q', 2.0), ('q', 0.1)]},
                         {'b_#_conditionA': [('p', 6.0), ('p', 1.0), ('q', 3.0)]}]
                         {'a_#_conditionB': [('p', 1.0), ('p', 2.0), ('q', 1.0), ('q', -1.2)]}]
        :param metaValue: 'conditionA'
        :return:  row = {'a': [('p', 2.3), ('p', -3.0), ('p', 1), ('q', 2.0), ('q', 0.1)]
                         'b': [('p', 6.0), ('p', 1.0), ('q', 3.0)] }
                  ...
                  Data is sorted, i.e. keys and values are sorted.
        """
        row = collections.OrderedDict()
        odata = collections.OrderedDict(sorted(data.items(), key=lambda x: x[0], reverse=True))
        for pattern in odata.keys():
            thisMetaValue = self.getMetaFromPattern(pattern)
            if thisMetaValue == metaValue:
                label = self.getLabelFromPattern(pattern)
                if label not in row:
                    row[label] = []
                row[label] += odata[pattern]
        return row

    def getResults(self):
        return self._data

    def getMetaDataValues(self):
        return self._metaValues

    def getData(self):
        return self._data

    def getMinimum(self):
        return self._mi

    def getMaximum(self):
        return self._ma

if __name__ == '__main__':
    from config import Config
    debug = True
    config = Config('bioplot.cfg')
    d = MatrixData(config, debug)

    d.makeRandomMatrix(False)
    print d.getMinimum(), d.getMaximum()
    print d.getData()