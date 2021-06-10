__author__ = 'jos'
# !/usr/bin/env python

'''
    tippet.py

    Object to plot a Tippett plot.

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

import matplotlib.pyplot as plt

from event import Event
from legendtext import LegendText
from probability import Probability
from utils import assignColors2MetaDataValue


class Tippett(Probability):
    def __init__(self, thisData, thisEer, thisCllr, thisConfig, thisExpName, thisDebug=True):
        self.data = thisData
        self._eerObject = thisEer
        self._cllrObject = thisCllr
        self.config = thisConfig
        self._expName = thisExpName
        self._printToFilename = thisExpName
        self.debug = thisDebug
        self.plotType = 'tippett_plot'
        Probability.__init__(self, self.data, self.config, self.debug)
        self.fig = None
        self.event = None

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
                        self._eerObject.eerValue, self._eerObject.eerScore, self.debug)

        legendText = lt.make()

        eerData = self.computeProbabilities(self.tippetFunc)

        for (metaValue, PD, PP, X) in eerData:
            pFr, = axes.plot(X, PP, 's-', label="P(pros): %s" % lt.half(legendText[metaValue])[0], color=colors[metaValue])
            pFa, = axes.plot(X, PD, 'o-', label="P(def): %s" % lt.half(legendText[metaValue])[1], color=colors[metaValue])

        plt.legend()
        axes.set_title("Tippett Plot: P(defense) and P(prosecution) for '%s'" % self.data.getTitle())
        plt.xlabel('score')
        plt.ylabel('Probability (cumulative distribution function)')
        plt.grid()
        if self.config.getPrintToFile():
            filename = "%s_%s.%s" % (self._printToFilename, self.plotType, "png")
            print("Writing plot to %s" % filename)
            plt.savefig(filename, orientation='landscape', papertype='letter')
        else:
            plt.show()
