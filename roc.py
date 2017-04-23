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
from legendtext import LegendText
from eer import Eer
from probability import Probability


class Roc(Probability):
    def __init__(self, thisData, thisConfig, thisExpName, thisDebug=True):
        self.data = thisData
        self.config = thisConfig
        self._expName = thisExpName
        self._printToFilename = thisExpName
        self.debug = thisDebug
        self.plotType = 'roc_plot'
        self.fig = None
        self.event = None
        Probability.__init__(self, self.data, self.config, self.debug)

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
        # For saving the pic we use a generic event object
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        axes = self.fig.add_subplot(111)
        metaDataValues = self.data.getMetaDataValues()
        metaColors = self.config.getMetaColors()
        colors = assignColors2MetaDataValue(metaDataValues, metaColors)

        eerObject = Eer(self.data, self.config, self._expName, self.debug)
        eerData = eerObject.computeProbabilities(self.eerFunc)
        eerValue = {}
        score = {}
        for thisMetaValue in sorted(colors.keys()):
            for metaValue, PD, PP, X in eerData:
                if thisMetaValue == metaValue:
                    try:
                        eerValue[metaValue], score[metaValue] = eerObject.computeEer(PD, PP, X)
                    except Exception as e:
                        print("Problem computing EER for %s: %s" % (thisMetaValue, e))
                    else:
                        eerValue[metaValue] *= 100
                    break
        lt = LegendText(self.data, colors, self.config, self.config.getShowCllrInRoc(), 
                        self.config.getShowMinCllrInRoc(), self.config.getShowEerInRoc(), 
                        self.config.getShowCountsInRoc(),
                        eerValue, score, self.debug)

        legendText = lt.make()

        for metaValue in metaDataValues:
            targetScores = self.data.getTargetScores4MetaValue(metaValue)
            nonTargetScores = self.data.getNonTargetScores4MetaValue(metaValue)
            allScores = targetScores + nonTargetScores
            truthValues = np.ones(len(allScores))
            truthValues[0:len(targetScores)] = 1
            truthValues[len(targetScores):] = 0
            fpr, tpr, thresholds = metrics.roc_curve(truthValues, allScores, pos_label=1)
            bla, = axes.plot(fpr, tpr, 'x-', label=legendText[metaValue], color=colors[metaValue])
            #axes.set_title("Receiver Operating Characteristic for '%s'" % self.data.getTitle())
            axes.set_title("ROC plot for '%s'" % self.data.getTitle())
        plt.xlabel('P(false positive)')
        plt.ylabel('P(true positive)')
        plt.grid()
        plt.legend(loc=5)  # Position legend at center right.
        if self.config.getPrintToFile():
            filename = "%s_%s.%s" % (self._printToFilename, self.plotType, "png")
            print("Writing plot to %s" % filename)
            plt.savefig(filename, orientation='landscape', papertype='letter')
        else:
            plt.show()
