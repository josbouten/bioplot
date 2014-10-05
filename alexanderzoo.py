#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''

    alexanderzoo.py

    Object which can plot a traditional Yager et al style zoo plot or
    show a zoo plot with ellipses in stead of points where the height and width of
    the ellipses are related to the standard deviations of the scores that were used
    to calculate the mean target and mean non target scores (as published by Anil
    Alexander et al at the IAFPA conference in Zurich in 2014.

    Copyright (C) 2014 Jos Bouten ( josbouten@gmail.com )

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
from zoo import Zoo
from utils import assignColors2MetaDataValue

class AlexanderZoo(Zoo):
    def __init__(self, data, config, debug):
        Zoo.__init__(self, data, config, debug)
        self.config = config
        self.data = data
        self.debug = debug
        # All ellipses will have their own annotation.
        self._pointsWithAnnotation = []
        self.interconnectMetaValues = self.config.getInterconnectMetaValues()
        # Directory to store animal data.
        self._outputPath = self.config.getOutputPath()

        if self.debug:
            print 'nrMeta:', self.data.getNrDistinctMetaDataValues()
        self._title = data.title
        colorMap = plt.get_cmap(self.config.getColorMap())
        self.colors = assignColors2MetaDataValue(self.data.getMetaDataValues(), colorMap)
        self.nrColors = len(self.colors.keys())
        if self.debug:
            print 'colors:', self.colors
            print 'nr colors:', self.nrColors


    def plotZoo(self):
        yagerStyle = self.config.getYagerStyle()
        alexanderStyle = self.config.getAlexanderStyle()
        self.useColorsForQuartileRanges = self.config.getUseColorsForQuartileRanges()
        self.annotateQuartileMembers = self.config.getAnnnotateQuartileMembers()

        if alexanderStyle:
            self.aimsStdDev = []
            self.agmsStdDev = []
            self._plotZooAlexanderStyle(yagerStyle)
            if self.config.getInterconnectMetaValues():
                self._connectMetaValues(self._pointsWithAnnotation)
        else:
            self._computeZooStats()
            self._plotZooTraditional(yagerStyle)

        # Gather some stats
        self.saveExceptionalAnimals()
        plt.show()


    def _plotZooAlexanderStyle(self, yagerStyle=False):
        self._computeZooStatsAlexanderStyle()
        # plot a list of ellipses each visualising a score distribution for a target
        self.fig = plt.figure()
        self.drawLegend(self.colors)

        self.event = Event(self.config, self.fig, self._title, self.plotType, self.debug)
        # For saving the pic we use a generic event object
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)

        # For clicking on an ellipse we need a custom event handler.
        self.fig.canvas.mpl_connect('button_press_event', self._onMouseEvent)

        axes = self.fig.add_subplot(111)
        self._plotDistributions(self.colors, axes)
        if yagerStyle:
            comment = ''
        else:
            comment = '(inverse y-axis)'
        self._plotAxes(comment, yagerStyle, self._title, axes)


    def _plotZooTraditional(self, yagerStyle=False):
        self.fig = plt.figure()
        axes = self.fig.add_subplot(111)
        self.drawLegend(self.colors)
        if self.debug:
            print 'aimsv:', len(self.aimsv), 'agmsv:', len(self.agmsv)
        self.event = Event(self.config, self.fig, self._title, self.plotType, self.debug)
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        allAgmsv = []
        allAimsv = []
        allColors = []
        for template in self.agmsv.keys():
            if template in self.aimsv.keys():
                pattern = self.getMetaFromPattern(template)
                try:
                    allColors.append(self.colors[pattern])
                except Exception:
                    pass
                else:
                    allAgmsv.append(self.agmsv[template])
                    allAimsv.append(self.aimsv[template])
        axes.scatter(allAgmsv, allAimsv, color=allColors, marker='o', linewidth=0.5)
        if yagerStyle:
            comment = ''
        else:
            comment = '(inverse y-axis)'
        self._plotAxes(comment, yagerStyle, self._title, axes)


    def _onMouseEvent(self, event):
        # We do not want the annotations to reappear after the first click
        self.config.setShowAnnotationsAtStartup(False)

        if event.xdata is not None and event.ydata is not None:
            # Check whether we clicked close to a data point.
            labelsCloseBy = self.findDataPointsNear(event.xdata, event.ydata)

            # Make all annotations invisible.
            for point, annotation, pattern, xy in self._pointsWithAnnotation:
                thisLabel = self.getLabelFromPattern(pattern)
                if not thisLabel in self.data.getLabelsToShowAlways():
                    annotation.set_visible(False)
            for (annotation, xy) in self.referencesWithAnnotation:
                annotation.set_visible(False)

            # Make the points close to the click visible.
            for (patternFound, x, y) in labelsCloseBy:
                for point, annotation, pattern, xy in self._pointsWithAnnotation:
                    if patternFound == pattern:
                        annotation.set_visible(True)
            if self.config.getShowReference:
                # check whether we clicked near the reference ellipses.
                xRange = abs(self.agm_ma - self.agm_mi)
                yRange = abs(self.aim_ma - self.aim_mi)
                thresholdX = 3 * xRange / self.config.getScaleFactor()
                thresholdY = 3 * yRange / self.config.getScaleFactor()
                for (annotation, xy) in self.referencesWithAnnotation:
                    # Use dimensions of unit ellipse for threshold.
                    if self.isNear(event.xdata, event.ydata, xy, thresholdX, thresholdY):
                        annotation.set_visible(True)
            plt.draw()