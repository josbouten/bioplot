#!/usr/bin/env python

"""
    roc.py

    Object used to plot a Receiver Operating Characteristic i.e. ROC-curve.

    Copyright (C) 2015 Jos Bouten ( josbouten at gmail dot com )

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
import numpy as np
from utils import assignColors2MetaDataValue
from sklearn import metrics
from cllr import Cllr
from collections import defaultdict
from eer import Eer
from probability import Probability


class Roc(Probability):
    def __init__(self, thisData, thisConfig, thisDebug=True):
        self.data = thisData
        self.config = thisConfig
        self.debug = thisDebug
        self.plotType = 'roc_plot'
        self.fig = None
        self.event = None
        Probability.__init__(self, self.data, self.config, self.debug)

    def plot(self):
        self.fig = plt.figure()
        self.event = Event(self.config, self.fig, self.data.getTitle(), self.plotType, self.debug)
        # For saving the pic we use a generic event object
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        axes = self.fig.add_subplot(111)
        metaDataValues = self.data.getMetaDataValues()
        metaColors = self.config.getMetaColors()
        colors = assignColors2MetaDataValue(metaDataValues, metaColors)

        # legendText = defaultdict(list)

        legendText = defaultdict(list)
        # Add meta condition value name to legend text if there are more than one meta values.
        if len(metaColors) > 1:
            for thisMetaValue in sorted(colors.keys()):
                legendText[thisMetaValue].append(thisMetaValue)

        # Compute and show the EER value if so desired.
        if self.config.getShowEerValuesInRoc():
            eerObject = Eer(self.data, self.config, self.debug)
            eerData = eerObject.computeProbabilities(self.eerFunc)
            for thisMetaValue in sorted(colors.keys()):
                for metaValue, PD, PP, X in eerData:
                    if thisMetaValue == metaValue:
                        try:
                            eerValue, score = eerObject.computeEer(PD, PP, X)
                        except Exception, e:
                            print "DrawLegend: problem computing EER for %s: %s" % (thisMetaValue, e)
                        else:
                            eerValue *= 100
                            if eerValue < 10.0:
                                eerStr = "Eer:  %.2f%s" % (eerValue, '%')
                            else:
                                eerStr = "Eer: %2.2f%s" % (eerValue, '%')
                            legendText[thisMetaValue].append(eerStr)
                        break

        # Compute and show the Cllr value if so desired.
        if self.config.getShowCllrValuesInRoc():
            cllrObject = Cllr(self.data, self.config, self.debug)
            cllrData = cllrObject.getCllr()
            if self.debug:
                print cllrData
            for thisMetaValue in sorted(colors.keys()):
                for metaValue, cllrValue in cllrData:
                    if thisMetaValue == metaValue:
                        if type(cllrValue) is float:
                            cllrStr = "Cllr: %.3f" % cllrValue
                        else:
                            cllrStr = "Cllr: %s" % cllrValue
                        legendText[metaValue].append(cllrStr)
                        break

        # Compute and show the CllrMin value if so desired.
        if self.config.getShowMinCllrValuesInRoc():
            cllrObject = Cllr(self.data, self.config, self.debug)
            minCllrData = cllrObject.getMinCllr()
            if self.debug:
                print "minCllrData:", minCllrData
            for thisMetaValue in sorted(colors.keys()):
                for metaValue, minCllrValue in minCllrData:
                    if thisMetaValue == metaValue:
                        if type(minCllrValue) is float:
                            minCllrStr = "minCllr: %.3f" % minCllrValue
                        else:
                            minCllrStr = "minCllr: %s" % minCllrValue
                        legendText[metaValue].append(minCllrStr)
                        break

        for metaValue in metaDataValues:
            thisLegendText = ''
            # Compile legend text.
            for el in legendText[metaValue]:
                thisLegendText += el + ', '
                # Remove last comma and space.
            thisLegendText = thisLegendText[:-2]
            targetScores = self.data.getTargetScores4MetaValue(metaValue)
            nonTargetScores = self.data.getNonTargetScores4MetaValue(metaValue)
            allScores = targetScores + nonTargetScores
            truthValues = np.ones(len(allScores))
            truthValues[0:len(targetScores)] = 1
            truthValues[len(targetScores):] = 0
            fpr, tpr, thresholds = metrics.roc_curve(truthValues, allScores, pos_label=1)
            bla, = axes.plot(fpr, tpr, 'x-', label=thisLegendText, color=colors[metaValue])
        plt.xlabel('P(false positive)')
        plt.ylabel('P(true positive)')
        plt.grid()
        plt.legend(loc=5)  # position logend at center right
        plt.show()
