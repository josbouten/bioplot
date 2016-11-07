__author__ = 'jos'
#!/usr/bin/env python

'''
    tippet.py

    Object to plot a Tippett plot.

    Copyright (C) 2014, 2015, 2016 Jos Bouten ( josbouten at gmail dot com )

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
from probability import Probability
from utils import assignColors2MetaDataValue

class Tippett(Probability):
    def __init__(self, thisData, thisConfig, thisExpName, thisDebug=True):
        self.data = thisData
        self.config = thisConfig
        self._printToFilename = thisExpName
        self.debug = thisDebug
        self.plotType = 'tippett_plot'
        Probability.__init__(self, self.data, self.config, self.debug)
        self.fig = None
        self.event = None


    def plot(self):
        self.fig = plt.figure(figsize=(self.config.getPrintToFileWidth(), self.config.getPrintToFileHeight()))
        self.event = Event(self.config, self.fig, self.data.getTitle(), self.plotType, self.debug)
        # For saving the pic we use a generic event object
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        axes = self.fig.add_subplot(111)
        eerData = self.computeProbabilities(self.tippetFunc)
        metaDataValues = self.data.getMetaDataValues()
        metaColors = self.config.getMetaColors()
        colors = assignColors2MetaDataValue(metaDataValues, metaColors)
        for (metaValue, PD, PP, X) in eerData:
            pFr, = axes.plot(X, PP, 's-', label="P(pros), %s" % metaValue, color=colors[metaValue])
            pFa, = axes.plot(X, PD, 'o-', label="P(def), %s" % metaValue, color=colors[metaValue])
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
