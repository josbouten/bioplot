__author__ = 'jos'


'''
    Object used to compute Cllr and minCllr.

    Copyright (C) 2014,2015 Jos Bouten ( josbouten at gmail dot com )

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
from utils import plotIt

# code taken from bob.measure.calibration
class Cllr:
    def __init__(self, thisData, thisConfig, thisDebug=True):
        self.data = thisData
        self.config = thisConfig
        self.debug = thisDebug

    def cllr(self, targetScoreValues, nonTargetScoreValues):
        """Computes the 'cost of log likelihood ratio' measure as given in the bosaris toolkit"""
        sum_pos, sum_neg = 0., 0.
        for pos in targetScoreValues:
            sum_pos += math.log(1. + math.exp(-pos), 2.)
        for neg in nonTargetScoreValues:
            sum_neg += math.log(1. + math.exp(neg), 2.)
        return (sum_pos / len(targetScoreValues) + sum_neg / len(nonTargetScoreValues)) / 2.

    def getCllr(self):
        metaValues = self.data.getMetaDataValues()
        targetScores = self.data.getTargetScores()
        nonTargetScores = self.data.getNonTargetScores()
        ret = []
        for metaValue in metaValues:
            targetScoreValues = self._extractValues(targetScores, metaValue)
            nonTargetScoreValues = self._extractValues(nonTargetScores, metaValue)
            ret.append((metaValue, self.cllr(targetScoreValues, nonTargetScoreValues)))
        return ret

    def _extractValues(self, dict, metaValue):
        ret = []
        for el in dict:
            if metaValue in el:
                ret += dict[el]
        return ret

    def getMinCllr(self):
        """Computes the 'minimum cost of log likelihood ratio' measure as given in the bosaris toolkit"""
        metaValues = self.data.getMetaDataValues()
        targetScores = self.data.getTargetScores()
        nonTargetScores = self.data.getNonTargetScores()
        ret = []
        for metaValue in metaValues:
            targetScoreValues = self._extractValues(targetScores, metaValue)
            nonTargetScoreValues = self._extractValues(nonTargetScores, metaValue)
            ret.append(self.minCllr(targetScoreValues, nonTargetScoreValues))
        return ret

    def minCllr(self, targetScoreValues, nonTargetScoreValues):
        neg = sorted(nonTargetScoreValues)
        pos = sorted(targetScoreValues)
        N = len(neg)
        P = len(pos)
        I = N + P
        # now, iterate through both score sets and add a 0 for negative and 1 for positive scores
        n, p = 0, 0
        ideal = np.zeros(I)
        neg_indices = [0] * N
        pos_indices = [0] * P
        for i in range(I):
            if p < P and (n == N or neg[n] > pos[p]):
                pos_indices[p] = i
                p += 1
                ideal[i] = 1
            else:
                neg_indices[n] = i
                n += 1

        plotIt(pos_indices, 'pos_indices')
        plotIt(neg_indices, 'neg_indices')

        # Compute the pool adjacent violaters method on the ideal LLR scores
        popt = np.ndarray(ideal.shape, dtype=np.float)

        plotIt(popt, 'popt1')

        # http://scikit-learn.org/stable/auto_examples/plot_isotonic_regression.html
        # ir = IsotonicRegression()
        # y_ = ir.fit_transform(x, y)

        # ir = IsotonicRegression()
        # popt_ = ir.fit_transform(popt, ideal)
        # popt_ = ir.fit_transform(ideal, popt)
        # print 'popt :', popt
        # print 'popt_:', popt_
        # popt = popt_

        #pavx(ideal, popt)

        popt = self.pavx(popt)
        plotIt(popt, 'popt2')

        # disable runtime warnings for a short time since log(0) will raise a warning
        old_warn_setup = np.seterr(divide='ignore')
        # ... compute logs
        posterior_log_odds = np.log(popt) - np.log(1. - popt)
        log_prior_odds = math.log(float(P) / float(N))
        # ... activate old warnings
        np.seterr(**old_warn_setup)

        llrs = posterior_log_odds - log_prior_odds

        # some weired addition
        # for i in range(I):
        #    llrs[i] += float(i)*1e-6/float(I)

        # unmix positive and negative scores
        new_neg = np.zeros(N)
        for n in range(N):
            new_neg[n] = llrs[neg_indices[n]]
        new_pos = np.zeros(P)
        for p in range(P):
            new_pos[p] = llrs[pos_indices[p]]

        # compute cllr of these new 'optimal' LLR scores
        return self.cllr(new_neg, new_pos)

    def pavx(self, y):

        n = len(y)

        index = np.zeros(n)
        length = np.zeros(n)
        # An interval of indices is represented by its left endpoint
        # ("index") and its length "len"
        ghat = np.zeros(n)

        ci = 1
        index[ci] = 1
        length[ci] = 1
        ghat[ci] = y[1]
        # ci is the number of the interval considered currently.
        # ghat(ci) is the mean of y-values within this interval.
        for j in np.arange(2, n):
            # a new index intervall, {j}, is created:
            ci += 1
            index[ci] = j
            length[ci] = 1
            ghat[ci] = y[j]
            while (ci >= 2) and (ghat[max(ci - 1, 1)] >= ghat[ci]):
                # "pool adjacent violators":
                nw = length[ci - 1] + length[ci]
                ghat[ci - 1] = ghat[ci - 1] + (length[ci] / nw) * (ghat[ci] - ghat[ci - 1])
                length[ci - 1] = nw
                ci -= 1

        # Now define ghat for all indices:
        while n >= 1:
            for j in np.arange(index[ci] - 1, n):
                ghat[int(j)] = ghat[int(ci)]
            n = index[ci] - 1
            ci -= 1
        return ghat
