__author__ = 'jos'

import numpy as np

'''
    probability.py

    Object to compute PDF related statistics.

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

import listutils as lu

class Probability:
    def __init__(self, thisData, thisConfig, thisDebug=True):
        self.data = thisData
        self.config = thisConfig
        self.debug = thisDebug

    def eerFunc(self, ts, lt):
        return 1.0 - ts / lt

    def tippetFunc(self, ts, lt):
        return ts / lt

    def compProbs(self, targetScores, nonTargetScores, func):

        """
            Compute P(prosecution) and P(defense) from target and non target scores.
            In case of EER compute eer value and score at which eer point lies
            for j = 1 : length(Xx)
              PP(j) = 1 - (length(find(target_scores >= Xx(j))) / length(target_scores))
              PD(j) = length(find(non_target_scores >= Xx(j))) / length(non_target_scores)
            end

        """

        mi = self.data.getMin()
        ma = self.data.getMax()
        thisRange = abs(ma - mi)

        # We want N steps on the score (horizontal) axis.
        N = self.config.getNrSamples4Probability()

        lt = len(targetScores) * 1.0
        lnt = len(nonTargetScores) * 1.0
        X = np.arange(mi, ma, thisRange / N)
        lx = len(X)
        PD = np.zeros(lx)
        PP = np.zeros(lx)
        for j in np.arange(lx):
            ts = len(lu.findIndex2EqualOrBigger(targetScores, X[j])) * 1.0
            nts = len(lu.findIndex2EqualOrBigger(nonTargetScores, X[j])) * 1.0
            PP[j] = func(ts, lt)
            PD[j] = nts / lnt
        return PD, PP, X

    def getScores(self, thisDict):
        ret = []
        for el in thisDict:
            ret = ret + thisDict[el]
        return ret

    def _extractValues(self, thisDict, metaValue):
        ret = []
        for el in thisDict:
            if metaValue in el:
                ret += thisDict[el]
        return ret

    def computeProbabilities(self, func):
        # PP = Probability of Prosecution Hypothesis
        # PD = Probability of Defense Hypothesis
        probData = []
        for metaValue in self.data.getMetaDataValues():
            targetScores = self.data.getTargetScores()
            targetScoreValues = self._extractValues(targetScores, metaValue)
            if len(targetScoreValues) > 0:
                nonTargetScores = self.data.getNonTargetScores()
                nonTargetScoreValues = self._extractValues(nonTargetScores, metaValue)
                PD, PP, X = self.compProbs(targetScoreValues, nonTargetScoreValues, func)
                probData.append((metaValue, PD, PP, X))
        return probData