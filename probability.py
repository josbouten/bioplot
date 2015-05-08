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

class Probability:
    def __init__(self, data, config, debug=True):
        self.data = data
        self.config = config
        self.debug = debug

    def _findEqualOrBigger(self, li, value):
        return [i for (i, val) in enumerate(li) if val >= value ]

    def _findEqual(self, li1, li2):
        ret = []
        cnt = 0
        for el1, el2 in zip(li1, li2):
            if el1 == el2:
                ret.append(cnt)
            cnt += 1
        return ret

    def _findBigger(self, li, value):
        return [i for (i, val) in enumerate(li) if val > value ]

    def _findBiggerInList(self, li1, li2):
        ret = []
        cnt = 0
        for el1, el2 in zip(li1, li2):
            if el1 > el2:
                ret.append(cnt)
            cnt += 1
        return ret

    def _intersectionPoint(self, PD, PP):
        indices = self._findEqual(PD, PP)
        if len(indices) == 0:
            indices = self._findBiggerInList(PD, PP)
            # get last element
            ind1 = indices[-1]
            ind2 = ind1 + 1
            c11 = PD[ind1]
            c12 = PD[ind2]
            c21 = PP[ind1]
            c22 = PP[ind2]
            x = (c21 - c11) / (c12 - c11 - c22 + c21)
            y = c11 + (c12 - c11) * x
            x = x + ind1 - 1
        else:
            x = indices[1] - 1
            y = PD[indices[1]]
        return x, y

    def eerFunc(self, ts, lt):
        return 1.0 - ts / lt

    def tippetFunc(self, ts, lt):
        return ts / lt

    def eerResample_org(self, targetScores, nonTargetScores):

        '''
            Compute eer and score at which eer point lies from target and non target scores.
            for j = 1 : length(Xx)
              PP(j) = 1 - (length(find(target_scores >= Xx(j))) / length(target_scores))
              PD(j) = length(find(non_target_scores >= Xx(j))) / length(non_target_scores)
            end

        '''

        mi = self.data.getMin()
        ma = self.data.getMax()
        range = abs(ma - mi)

        # We want N steps on the score (horizontal) axis.
        N = self.config.getNrSamples4Probability()

        lt = len(targetScores) * 1.0
        lnt = len(nonTargetScores) * 1.0
        X = np.arange(mi, ma, range / N)
        lx = len(X)
        PD = np.zeros(lx)
        PP = np.zeros(lx)
        for j in np.arange(lx):
            ts = len(self._findEqualOrBigger(targetScores, X[j])) * 1.0
            nts = len(self._findEqualOrBigger(nonTargetScores, X[j])) * 1.0
            PP[j] = self.eerFunc(ts, lt)
            PD[j] = nts / lnt
        index2score, eer = self._intersectionPoint(PD, PP)
        if self.debug:
            print 'compProbs:index2score:', index2score
            print 'compProbs:eer:', eer
        score = X[round(index2score)]
        return eer, score, PD, PP, X

    def compProbs(self, targetScores, nonTargetScores, func):

        '''
            Compute P(prosecution) and P(defense) from target and non target scores.
            In case of EER compute eer valie and score at which eer point lies
            for j = 1 : length(Xx)
              PP(j) = 1 - (length(find(target_scores >= Xx(j))) / length(target_scores))
              PD(j) = length(find(non_target_scores >= Xx(j))) / length(non_target_scores)
            end

        '''

        mi = self.data.getMin()
        ma = self.data.getMax()
        range = abs(ma - mi)

        # We want N steps on the score (horizontal) axis.
        N = self.config.getNrSamples4Probability()

        lt = len(targetScores) * 1.0
        lnt = len(nonTargetScores) * 1.0
        X = np.arange(mi, ma, range / N)
        lx = len(X)
        PD = np.zeros(lx)
        PP = np.zeros(lx)
        for j in np.arange(lx):
            ts = len(self._findEqualOrBigger(targetScores, X[j])) * 1.0
            nts = len(self._findEqualOrBigger(nonTargetScores, X[j])) * 1.0
            PP[j] = func(ts, lt)
            PD[j] = nts / lnt
        return PD, PP, X

    def computeEer(self, PD, PP, X):
        index2score, eer = self._intersectionPoint(PD, PP)
        if self.debug:
            print 'compProbs:index2score:', index2score
            print 'compProbs:eer:', eer
        score = X[round(index2score)]
        return eer, score

    def getScores(self, dict):
        ret = []
        for el in dict:
            ret = ret + dict[el]
        return ret

    def _extractValues(self, dict, metaValue):
        ret = []
        for el in dict:
            if metaValue in el:
                ret += dict[el]
        return ret

    def computeProbabilities(self, func):
        # PP = Probability of Prosecution Hypothesis
        # PD = Probability of Defense Hypothesis
        probData = []
        for metaValue in self.data.getMetaDataValues():
            targetScores = self.data.getTargetScores()
            targetScoreValues = self._extractValues(targetScores, metaValue)
            nonTargetScores = self.data.getNonTargetScores()
            nonTargetScoreValues = self._extractValues(nonTargetScores, metaValue)
            PD, PP, X = self.compProbs(targetScoreValues, nonTargetScoreValues, func)
            probData.append((metaValue, PD, PP, X))
        return probData
