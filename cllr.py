__author__ = 'jos'

'''
    Object used to compute Cllr and minCllr.

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

import math
import numpy as np

from sklearn.isotonic import IsotonicRegression

class Cllr:
    def __init__(self, thisData, thisConfig, thisDebug=True):
        self.data = thisData
        self.config = thisConfig
        self.debug = thisDebug

    def cllr(self, targetScoreValues, nonTargetScoreValues):
        '''
        Computes the 'cost of log likelihood ratio' measure as given in the bosaris toolkit
        :param targetScoreValues:
        :param nonTargetScoreValues:
        :return:
        '''
        sum_pos, sum_neg = 0., 0.
        for pos in targetScoreValues:
            sum_pos += math.log(1. + math.exp(-pos), 2.)
        for neg in nonTargetScoreValues:
            sum_neg += math.log(1. + math.exp(neg), 2.)
        return (sum_pos / len(targetScoreValues) + sum_neg / len(nonTargetScoreValues)) / 2.

    def getCllr(self):
        ret = []
        targetScores = self.data.getTargetScores()
        nonTargetScores = self.data.getNonTargetScores()
        metaValues = self.data.getMetaDataValues()
        for metaValue in metaValues:
            targetScoreValues = self._extractValues(targetScores, metaValue)
            if len(targetScoreValues) > 0:
                nonTargetScoreValues = self._extractValues(nonTargetScores, metaValue)
                ret.append((metaValue, self.cllr(targetScoreValues, nonTargetScoreValues)))
            else:
                ret.append((metaValue, "undef"))
        return ret

    def _extractValues(self, dict, metaValue):
        '''

        :param dict:
        :param metaValue:
        :return:
        '''
        ret = []
        for el in dict:
            if metaValue in el:
                ret += dict[el]
        return ret

    def getMinCllr(self):
        return self._getMinCllr()

    def _getMinCllr(self):
        ''' Computes the 'minimum cost of log likelihood ratio measure. '''
        ret = []
        metaValues = self.data.getMetaDataValues()
        for metaValue in metaValues:
            ret.append((metaValue, "undef"))
        return ret