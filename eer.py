#!/usr/bin/env python

"""
    eer.py

    Object used to extract compute EER and plot EER in score plot.

    Copyright (C) 2014Jos Bouten ( josbouten at gmail dot com )

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

import matplotlib.pyplot as plt
from event import Event
from probability import Probability
import numpy as np
import listutils as lu
from utils import assignColors2MetaDataValue
from legendtext import LegendText


class Eer(Probability):
    def __init__(self, thisData, thisConfig, thisExpName, thisDebug=True):
        self.data = thisData
        self.config = thisConfig
        self._printToFilename = thisExpName
        self._expName = thisExpName
        self.debug = thisDebug
        Probability.__init__(self, self.data, self.config, self.debug)
        self.plotType = 'eer_plot'
        self.fig = None
        self.event = None

        metaDataValues = self.data.getMetaDataValues()
        metaColors = self.config.getMetaColors()
        self.colors = assignColors2MetaDataValue(metaDataValues, metaColors)

        self.eerData = self.computeProbabilities(self.eerFunc)
        self.eerValue = {}
        self.score = {}
        for thisMetaValue in sorted(self.colors.keys()):
            for metaValue, PD, PP, X in self.eerData:
                if thisMetaValue == metaValue:
                    try:
                        self.eerValue[metaValue], self.score[metaValue] = self.computeEer(PD, PP, X)
                    except Exception as e:
                        print("Problem computing EER for %s: %s" % (thisMetaValue, e))
                    else:
                        self.eerValue[metaValue] *= 100
                    break

    def _intersectionPoint(self, PD, PP):
        indices = lu.findEqual(PD, PP)
        if len(indices) == 0:
            indices = lu.findElementsBiggerInList(PD, PP)
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
        return int(x), y

    def eerResample_org(self, targetScores, nonTargetScores):

        """
            Compute eer and score at which eer point lies from target and non target scores.
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
            PP[j] = self.eerFunc(ts, lt)
            PD[j] = nts / lnt
        index2score, eer = self._intersectionPoint(PD, PP)
        if self.debug:
            print('compProbs:index2score:', index2score)
            print('compProbs:eer:', eer)
        score = X[index2score]
        return eer, score, PD, PP, X

    def computeEer(self, PD, PP, X):
        try:
            index2score, eer = self._intersectionPoint(PD, PP)
        except Exception as e:
            print('Exception in computeEer:', e)
            print('You may have too few data points to compute an eer value.')
            # sys.exit(1)
        else:
            if self.debug:
                print('computeEer:index2score:', index2score)
                print('computeEer:eer:', eer, 'for experiment:', self._expName)
            score = X[index2score]
            return eer, score

    def _makeLegendText(self, legendText, metaValue):
        thisLegendText = '%s, ' % metaValue
        # Compile legend text.
        for el in legendText[metaValue]:
            thisLegendText += el + ', '
            # Remove last comma and space.
        thisLegendText = thisLegendText[:-2]
        return thisLegendText

    def plot(self):
        self.fig = plt.figure(figsize=(self.config.getPrintToFileWidth(), self.config.getPrintToFileHeight()))
        self.event = Event(self.config, self.fig, self.data.getTitle(), self.plotType, self.debug)
        # For saving the pic we use a generic event object.
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        axes = self.fig.add_subplot(111)

        lt = LegendText(self.data, self.colors, self.config, self.config.getShowCllrInEer(),
                        self.config.getShowMinCllrInEer(), True,
                        self.config.getShowCountsInEer(),
                        self.eerValue, self.score, self.debug)

        legendText = lt.make()

        for (metaValue, PD, PP, X) in self.eerData:
            labelText = "P(pros): %s" % lt.half(legendText[metaValue])[0]
            pFr, = axes.plot(X, PP, 's-', label=labelText, color=self.colors[metaValue])

            labelText = "P(def): %s" % lt.half(legendText[metaValue])[1]
            pFa, = axes.plot(X, PD, 'o-', label=labelText, color=self.colors[metaValue])

            axes.set_title("P(defense) and P(prosecution) for '%s'" % self.data.getTitle())
            plt.xlabel('raw score')
            plt.ylabel('Probability')
        plt.grid()
        plt.legend(loc=5)  # Position legend at center right.
        if self.config.getPrintToFile():
            filename = "%s_%s.%s" % (self._printToFilename, self.plotType, "png")
            print("Writing plot to %s" % filename)
            plt.savefig(filename, orientation='landscape', papertype='letter')
        else:
            plt.show()
