#!/usr/bin/env python3.5

__author__ = 'drs. ing. Jos Bouten'

'''
    alexanderzoo.py

    Object which can plot a traditional Yager et al style zoo plot or
    show a zoo plot with ellipses in stead of points where the height and width of
    the ellipses are related to the standard deviations of the scores that were used
    to calculate the mean target and mean non target scores (as published by Anil
    Alexander et al at the IAFPA conference in Zurich in 2014.

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
from zoo import Zoo
import collections


class AlexanderZoo(Zoo):
    def __init__(self, thisData, thisEerObject, thisCllerObject, thisConfig, thisExpName, thisDebug):
        Zoo.__init__(self, thisData, thisConfig, thisExpName, thisDebug)
        self.config = thisConfig
        self.data = thisData
        self._eerObject = thisEerObject
        self._cllrObject = thisCllerObject
        self._printToFilename = thisExpName
        self.debug = thisDebug
        # All ellipses will have their own annotation.
        self._pointsWithAnnotation = []
        # Directory to store animal data.
        self._outputPath = self.config.getOutputPath()

        if self.debug:
            print('nrMeta:', self.data.getNrDistinctMetaDataValues())
        self._title = self.data.getTitle()

        self.aimsStdDev = collections.defaultdict(float)
        self.agmsStdDev = collections.defaultdict(float)
        self.annotateEllipses = None

    def plot(self):
        yagerStyle = self.config.getYagerStyle()
        self.useColorsForQuartileRanges = self.config.getUseColorsForQuartileRanges()
        self.annotateEllipses = self.config.getAnnotateEllipsesInQuartiles()

        self._plotZooAlexanderStyle(yagerStyle)
        if self.config.getAlexanderStyle():
            if self.config.getInterconnectMetaValues():
                self._connectMetaValues(self._pointsWithAnnotation)

        # Gather some stats
        self.saveExceptionalAnimals()
        if self.config.getPrintToFile():
            filename = "%s_%s.%s" % (self._printToFilename, self.plotType, "png")
            print("Writing plot to %s" % filename)
            plt.savefig(filename, orientation='landscape', papertype='letter')
        else:
            plt.show()

    def _plotZooAlexanderStyle(self, yagerStyle=True):
        self.computeZooStatsAlexanderStyle()
        # plot a list of ellipses each visualising a score distribution for a target
        self.fig = plt.figure(figsize=(self.config.getPrintToFileWidth(), self.config.getPrintToFileHeight()))
        self.drawLegend(self.colors, self._eerObject, self._cllrObject)

        self.event = Event(self.config, self.fig, self._title, self.plotType, self.debug)
        # For saving the pic we use a generic event object
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)

        # For clicking on an ellipse we need a custom event handler.
        self.fig.canvas.mpl_connect('button_press_event', self._onMouseEvent)

        axes = self.fig.add_subplot(111)
        # axes.set_autoscale_on(False)
        # plt.xlim(-2.0, -1.0)
        self._plotDistributions(self.colors, axes)
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

            # Make the points close to the clicked position visible.
            for (patternFound, x, y) in labelsCloseBy:
                for point, annotation, pattern, xy in self._pointsWithAnnotation:
                    if patternFound == pattern:
                        annotation.set_visible(True)
            if self.config.getShowReference:
                # check whether we clicked near the reference ellipses.
                xRange = abs(self.agm_maxAll - self.agm_minAll)
                yRange = abs(self.aim_maxAll - self.aim_minAll)
                thresholdX = 3 * xRange / self.config.getScaleFactor()
                thresholdY = 3 * yRange / self.config.getScaleFactor()
                for (annotation, xy) in self.referencesWithAnnotation:
                    # Use dimensions of unit ellipse for threshold.
                    if self.isNear(event.xdata, event.ydata, xy, thresholdX, thresholdY):
                        annotation.set_visible(True)
            plt.draw()
