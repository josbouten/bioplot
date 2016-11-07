#!/usr/bin/env python

"""
    Object used to compute Cllr and minCllr.

    This code is based on IDIAP's calibration.py which can be found via http://idiap.github.io/bob

    @inproceedings{bob2012,
     author = {A. Anjos AND L. El Shafey AND R. Wallace AND M. G\\"unther AND C. McCool AND S. Marcel},
      title = {Bob: a free signal processing and machine learning toolbox for researchers},
      year = {2012},
      month = oct,
      booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
      publisher = {ACM Press},
      url = {http://publications.idiap.ch/downloads/papers/2012/Anjos_Bob_ACMMM12.pdf},
    }

    The minCllr function computes the 'minimum cost of log likelihood ratio' measure as given in IDIAP's BOB
    code "calibration.py", however no use is made of BOB's pavx function as it would require linking c++ code.
    Instead sklearn's (a machine learning toolkit for python, see http://scikit-learn.org/) isotonic regression
    function is used which is equivalent.

    The code was adapted to the bioplot internal data format.

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

import math
import numpy as np
from sklearn.isotonic import IsotonicRegression


class Cllr:
    def __init__(self, thisData, thisConfig, thisDebug=True):
        self.data = thisData
        self.config = thisConfig
        self.debug = thisDebug

    def _cllr(self, targetScoreValues, nonTargetScoreValues):
        """
        Computes the 'cost of log likelihood ratio' measure as given in the bosaris toolkit
        :param targetScoreValues:
        :param nonTargetScoreValues:
        :return:
        """
        sum_pos, sum_neg = 0., 0.
        for pos in targetScoreValues:
            sum_pos += math.log(1. + math.exp(-pos), 2.)
        for neg in nonTargetScoreValues:
            sum_neg += math.log(1. + math.exp(neg), 2.)
        cllr = (sum_pos / float(len(targetScoreValues)) + sum_neg / float(len(nonTargetScoreValues))) / 2.
        return cllr

    def _extractValues(self, myDict, metaValue):
        """

        :param myDict:
        :param metaValue:
        :return:
        """
        ret = []
        for el in myDict:
            if metaValue in el:
                ret += myDict[el]
        return ret

    def _minCllr(self, targetScoreValues, nonTargetScoreValues, ):
        """
            Computes the 'minimum cost of log likelihood ratio' measure as given in IDIAP's bob calibration.py
            We don't however use pavx here, as used in many other implementations, but sklearn's isotonic regression,
            which is equivalent and frees us from linking to c++ code.
        """
        # First, sort both scores.
        neg = sorted(nonTargetScoreValues)
        pos = sorted(targetScoreValues)
        N = len(neg)
        P = len(pos)
        I = N + P
        # Now, iterate through both score sets and add a 0 for negative and 1 for positive scores.
        n, p = 0, 0
        idealSequence = np.zeros(I)
        neg_indices = [0] * N
        pos_indices = [0] * P
        for i in range(I):
            if n == N or neg[n] > pos[p]:
                pos_indices[p] = i
                p += 1
                idealSequence[i] = 1
            else:
                neg_indices[n] = i
                n += 1

        # Run the pool adjacent violaters method on the ideal LLR scores.
        # pavx implements isotonic regression. Python's sklearn contains code to do just that.
        ir = IsotonicRegression()
        # Calculate the isotonic regression.
        popt = ir.fit_transform(np.arange(len(idealSequence)), idealSequence)

        # disable runtime warnings for a short time since log(0) will raise a warning.
        old_warn_setup = np.seterr(divide='ignore')
        # ... compute logs.

        # Lets assume the prior odds on a target score is the ratio #target scores / #non target scores.
        log_prior_odds = math.log(float(P) / float(N))

        posterior_log_odds = np.log(popt) - np.log(1.0 - popt)

        # ... activate old warnings.
        np.seterr(**old_warn_setup)

        llrs = posterior_log_odds - log_prior_odds

        # Unmix positive and negative scores.
        new_neg = np.zeros(N)
        for n in range(N):
            new_neg[n] = llrs[neg_indices[n]]
        new_pos = np.zeros(P)
        for p in range(P):
            new_pos[p] = llrs[pos_indices[p]]

        # Compute cllr of these new 'optimal' LLR scores.
        minCllr = self._cllr(new_pos, new_neg)
        return minCllr

    def getCllr(self):
        ret = []
        theseTargetScores = self.data.getTargetScores()
        theseNonTargetScores = self.data.getNonTargetScores()
        metaValues = self.data.getMetaDataValues()
        for metaValue in metaValues:
            targetScoreValues = self._extractValues(theseTargetScores, metaValue)
            if len(targetScoreValues) > 0:
                nonTargetScoreValues = self._extractValues(theseNonTargetScores, metaValue)
                cllr = self._cllr(targetScoreValues, nonTargetScoreValues)
                ret.append((metaValue, cllr))
            else:
                ret.append((metaValue, "undef"))
        return ret

    def getMinCllr(self):
        """
            Computes the 'minimum cost of log likelihood ratio measure.
        """
        ret = []
        # metaValues = self.data.getMetaDataValues()
        # for metaValue in metaValues:
        #     ret.append((metaValue, "undef"))
        # ret = []
        allTargetScores = self.data.getTargetScores()
        allNonTargetScores = self.data.getNonTargetScores()
        metaValues = self.data.getMetaDataValues()
        for metaValue in metaValues:
            targetScoreValues = self._extractValues(allTargetScores, metaValue)
            if len(targetScoreValues) > 0:
                nonTargetScoreValues = self._extractValues(allNonTargetScores, metaValue)
                minCllr = self._minCllr(targetScoreValues, nonTargetScoreValues)
                ret.append((metaValue, minCllr))
            else:
                ret.append((metaValue, "undef"))
        return ret


if __name__ == '__main__':

    def readData(filename):
        ret = []
        try:
            f = open(filename, 'rt')
            lines = f.readlines()
            f.close()
            for line in lines:
                ret.append(float(line))
        except Exception as e:
            print(e)
        return ret


    targetFilename = 'input/targetscores.txt'
    nonTargetFilename = 'input/nontargetscores.txt'
    c = Cllr([], [], thisDebug=True)
    targetScores = readData(targetFilename)
    nonTargetScores = readData(nonTargetFilename)
    print(c._cllr(targetScores, nonTargetScores))
    print(c._minCllr(targetScores, nonTargetScores))
    print("Result should be 0.645767685989 and 0.146121418712")
