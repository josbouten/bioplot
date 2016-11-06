#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''

    Show zoo plot with ellipses in stead of points where the height and width of the
    ellipses are related to the standard deviations of the scores that were used to
    calculate the mean target and mean non target scores. This was first shown
    by Anil Alexander et al. at the Zurich 2014 IAFPA conference.
    Show histograms of the target and the non target scores.
    Finally, show lines interconnecting the point with equal labels to show the effect
    of changing a variable in an experimental.

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

    bottom_h = left_h = zleft + zwidth + spacing
    rectZoo = [zleft, zbottom, zwidth, zheight]
    rectHistx = [zleft, bottom_h, zwidth, xheight]
    rectHisty = [left_h, zbottom, ywidth, zheight]

'''
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

from event import Event
from zoo import Zoo
from circularhist import CircularHistPlot


class BoutenZoo(Zoo):
    def __init__(self, thisData, thisConfig, thisExpName, thisDebug):
        self.data = thisData
        self.config = thisConfig
        self._expName = thisExpName
        self._printToFilename = thisExpName
        self.debug = thisDebug
        Zoo.__init__(self, self.data, self.config, self._expName, self.debug)

        self.title = self.data.getTitle()
        # All ellipses will have their own annotation.
        self._pointsWithAnnotation = []
        # Directory to store animal data.
        self._outputPath = self.config.getOutputPath()
        self.aimsStdDev = []
        self.agmsStdDev = []
        self.fig = None

    def _prepareFigs(self):
        zleft = self.config.getZleft()
        zwidth = self.config.getZwidth()
        zbottom = self.config.getZbottom()
        zheight = self.config.getZheight()
        bottom_h = left_h = zleft + zwidth + self.config.getSpacing()
        xheight = self.config.getXheight()
        ywidth = self.config.getYwidth()
        rectZoo = [zleft, zbottom, zwidth, zheight]
        rectHistx = [zleft, bottom_h, zwidth, xheight]
        rectHisty = [left_h, zbottom, ywidth, zheight]
        rectHistc = [left_h, bottom_h, ywidth, xheight]

        # Define layout.
        axesZoo = self.fig.add_axes(rectZoo)
        self.drawLegend(self.colors)
        axesHistx = self.fig.add_axes(rectHistx)
        axesHisty = self.fig.add_axes(rectHisty)

        #axesHistx.set_xlabel('Distribution of Target Scores')
        axesHistx.set_title('Distribution of Target Scores')
        axesHisty.set_xlabel('Distribution of Non Target Scores')

        nullfmt = NullFormatter()
        if self.config.getNoHistAnnot():
            # No labels.
            axesHistx.xaxis.set_major_formatter(nullfmt)
            axesHisty.yaxis.set_major_formatter(nullfmt)

        axesHistx.yaxis.set_major_formatter(nullfmt)
        axesHisty.xaxis.set_major_formatter(nullfmt)

        axesHistc = None
        nr = len(self.data.getMetaDataValues())
        if nr == 2:
            if self.config.getInterconnectMetaValues():
                if self.config.getShowCircularHistogram():
                    axesHistc = self.fig.add_axes(rectHistc, polar=True)
                    #axesHistc.set_xlabel('Distribution of Slopes.')
                    axesHistc.set_title('Distribution of Slopes.')
                    axesHistc.yaxis.set_major_formatter(nullfmt)
                    axesHistc.xaxis.set_major_formatter(nullfmt)
        return self.fig, axesZoo, axesHistx, axesHisty, axesHistc

    def _plotHistogram(self, histData, extraLabel, axes, orientation, nrDataElements):
        self.plotType = "histogram_plot"
        nrBins = self.config.getNrBins(nrDataElements)
        allData = []
        allLabels = []
        allColors = []
        alpha = 1.0
        if self.debug:
            print('self.colors:', self.colors)
        for value in sorted(histData):
            try:
                allColors.append(self.colors[value])
                allData.append(histData[value])
                allLabels.append(value + " (%s)" % extraLabel)
            except Exception:
                pass
        try:
            n, bins, patches = axes.hist(allData, bins=nrBins, normed=self.config.getNormHist(), color=allColors,
                                         alpha=alpha, orientation=orientation, label=allLabels)
        except Exception:
            print("Error: could not plot histogram for %s values." % extraLabel)
            pass
        axes.legend()
        axes.grid(True)

    def plot(self):
        yagerStyle = self.config.getYagerStyle()
        self.useColorsForQuartileRanges = self.config.getUseColorsForQuartileRanges()
        self.annotateEllipsesInQuartiles = self.config.getAnnotateEllipsesInQuartiles()
        self.fig = plt.figure(figsize=(self.config.getPrintToFileWidth(), self.config.getPrintToFileHeight()))
        #self.fig = plt.figure(1, figsize=(8, 8))
        self.computeZooStatsAlexanderStyle()

        thisPlot, axesZoo, axesHistX, axesHistY, axesHistC = self._prepareFigs()
        self._plotZooAlexanderStyle(axesZoo, yagerStyle)
        if self.config.getAlexanderStyle():
            if self.config.getInterconnectMetaValues():
                allAngles, allDistances, deltaZoo = self._connectMetaValues(self._pointsWithAnnotation, axesZoo)
                if self.config.getShowCircularHistogram() and len(self.data.getMetaDataValues()) == 2:
                    if len(allAngles) > 0:
                        if axesHistC:
                            c = CircularHistPlot(allAngles, deltaZoo, axesHistC, self.debug)
                            c.plot()

        valueSet = self.data.getMetaDataValues().keys()
        targetHistData = {}
        nonTargetHistData = {}
        maxNrT = 0
        maxNrNt = 0
        for value in valueSet:
            targetHistData[value] = []
            nonTargetHistData[value] = []
            for label in self.data.getTargetLabels():
                template = label + self.LABEL_SEPARATOR + value
                targetHistData[value] += self.data.getTargetScores()[template]
                maxNrT = max(maxNrT, len(targetHistData[value]))
            for label in self.data.getNonTargetLabels():
                template = label + self.LABEL_SEPARATOR + value
                nonTargetHistData[value] += self.data.getNonTargetScores()[template]
                maxNrNt = max(maxNrNt, len(nonTargetHistData[value]))
        self._plotHistogram(targetHistData, 'target', axesHistX, 'vertical', maxNrT)
        self._plotHistogram(nonTargetHistData, 'non target', axesHistY, 'horizontal', maxNrNt)
        # Do the WWF-thing!
        self.saveExceptionalAnimals()
        # plt.show(block=True)
        if self.config.getPrintToFile():
            filename = "%s_%s.%s" % (self._printToFilename, self.plotType, "png")
            print("Writing plot to %s" % filename)
            plt.savefig(filename, orientation='landscape', papertype='letter')
        else:
            plt.show()

    def _plotZooAlexanderStyle(self, axesZoo, yagerStyle=False):
        # Plot a list of ellipses each visualising a score distribution for a target.
        self.event = Event(self.config, self.fig, self.title, self.plotType, self.debug)

        # For saving the pic we use a generic event object
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)

        # For clicking on an ellipse we need a custom event handler.
        self.fig.canvas.mpl_connect('button_press_event', self._onMouseEvent)

        self._plotDistributions(self.colors, axesZoo)
        if yagerStyle:
            comment = ''
        else:
            comment = '(inverse y-axis)'
        self._plotAxes(comment, yagerStyle, self.title, axesZoo)

    def _onMouseEvent(self, event):
        # We do not want the annotations to reappear after the first click.
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
                # Check whether we clicked near the reference ellipses.
                xRange = abs(self.agm_maxAll - self.agm_minAll)
                yRange = abs(self.aim_maxAll - self.aim_minAll)
                thresholdX = 3 * xRange / self.config.getScaleFactor()
                thresholdY = 3 * yRange / self.config.getScaleFactor()
                for (annotation, xy) in self.referencesWithAnnotation:
                    # Use dimensions of unit ellipse for threshold.
                    if self.isNear(event.xdata, event.ydata, xy, thresholdX, thresholdY):
                        annotation.set_visible(True)
            plt.draw()
