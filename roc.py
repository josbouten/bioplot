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
import numpy as np
from sklearn import metrics

from event import Event
from legendtext import LegendText
from probability import Probability
from utils import assignColors2MetaDataValue


class Roc(Probability):
    def __init__(self, thisData, thisEer, thisCllr, thisConfig, thisExpName, thisDebug=True):
        self.data = thisData
        self._eerObject = thisEer
        self._cllrObject = thisCllr
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

        lt = LegendText(self.data, self._cllrObject, colors, self.config, self.config.getShowCllrInDet(),
                        self.config.getShowMinCllrInDet(), self.config.getShowEerInDet(),
                        self.config.getShowCountsInDet(),
                        self._eerObject.eerValue, self.debug)
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
