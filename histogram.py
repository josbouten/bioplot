#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''

    histogram.py

    Object to compile data for and plot several types of histogram.

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

import matplotlib
import numpy
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.mlab as mlab
from format import Format
from event import Event
from utils import assignColors2MetaDataValue, assignColors

class Histogram(Event, Format):
    def __init__(self, data, config, type = 'normal', debug=True, useMeta=False):
        Format.__init__(self, debug)
        self.data = data
        self.config = config
        self.type = type
        self.debug = debug
        self.title = self.data.title
        self.useMeta = useMeta

    def _to_percent(self, y, position):
        # Ignore the passed in position. This has the effect of scaling the default tick locations.
        s = str(100 * y)

        # The percent symbol needs escaping in latex
        if matplotlib.rcParams['text.usetex'] == True:
            return s + r'$\%$'
        else:
            return s + '%'

    def _extractValues(self, listOflists):
        ret = []
        for el in listOflists.values():
            ret += el
        return ret

    def plotHistogram(self):
        if self.useMeta:
            self.plotHistogramWithMeta()
        else:
            self.plotType = "histogram_plot"
            targetScores = self._extractValues(self.data.getTargetScores())
            nonTargetScores = self._extractValues(self.data.getNonTargetScores())

            self.fig = plt.figure()
            self.event = Event(self.config, self.fig, self.data.title, self.plotType, self.debug)
            self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)

            nrBins = self.config.getNrBins()
            # Make a normed histogram. It'll be multiplied by 100 later.
            if self.type == 'cumulative':
                plt.hist(nonTargetScores, nrBins, normed=self.config.getNormHist(), color='red', alpha=1.0, histtype='step', cumulative=-1)
                plt.hist(targetScores, nrBins, normed=self.config.getNormHist(), color='green', alpha=0.7, histtype='step', cumulative = True)
                plt.title(r"Cumulative histogram for '%s'" % (self.title))
            else:
                n, bins2, patches = plt.hist(nonTargetScores, nrBins, normed=self.config.getNormHist(), color='red', alpha=1.0)
                n, bins1, patches = plt.hist(targetScores, nrBins, normed=self.config.getNormHist(), color='green', alpha=0.7)
                if self.config.getShowKernelInHist():
                    mu1 = numpy.average(targetScores)
                    sigma1 = numpy.std(targetScores)
                    y1 = mlab.normpdf(bins1, mu1, sigma1)
                    plt.plot(bins1, y1, 'b--')

                    mu2 = numpy.average(nonTargetScores)
                    sigma2 = numpy.std(nonTargetScores)
                    y2 = mlab.normpdf(bins2, mu2, sigma2)
                    plt.plot(bins2, y2, 'b--')
                    plt.title(r"Histogram for '%s': mu, sigma = (%0.2f, %0.2f) (%0.2f, %0.2f)" % (self.title, mu1, sigma1, mu2, sigma2))
                else:
                    plt.title(r"Histogram for '%s" % (self.title))
            plt.grid(True)
            plt.xlabel('red: non target scores, green: target scores')
            plt.ylabel('Probability')

            # Set the formatter
            formatter = FuncFormatter(self._to_percent)
            plt.gca().yaxis.set_major_formatter(formatter)
            plt.show()

    def plotHistogramWithMeta(self):
        self.plotType = "histogram_plot"
        targetScores = self._extractValues(self.data.getTargetScores())
        nonTargetScores = self._extractValues(self.data.getNonTargetScores())

        self.fig = plt.figure()
        self.event = Event(self.config, self.fig, self.data.title, self.plotType, self.debug)
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)

        nrBins = self.config.getNrBins()
        # Make a normed histogram. It'll be multiplied by 100 later.
        if self.type == 'cumulative':
            plt.hist(nonTargetScores, nrBins, normed=self.config.getNormHist(), facecolor='red', alpha=1.0, histtype='step', cumulative=-1)
            plt.hist(targetScores, nrBins, normed=self.config.getNormHist(), facecolor='green', alpha=0.7, histtype='step', cumulative = True)
            plt.title(r"Cumulative histogram for '%s'" % (self.title))
        else:
            if self.config.getShowMetaInHist():
                # Split target and non target scores per meta data value
                #v alueSet = self._getDistinct(self.data._metaDataValues.values())
                valueSet = self.data.getMetaDataValues().keys()
                if self.debug:
                    print 'valueSet:', valueSet
                targetHistData = {}
                nonTargetHistData = {}
                colorMap = plt.get_cmap(self.config.getColorMap())
                self.colors = assignColors2MetaDataValue(self.data.getMetaDataValues(), colorMap)
                self.nrColors = len(self.colors.keys())
                if self.debug:
                    print 'colors:', self.colors
                    print 'nr colors:', self.nrColors

                for value in valueSet:
                    targetHistData[value] = []
                    nonTargetHistData[value] = []
                    for label in self.data.getTargetLabels():
                        template = label + self.LABEL_SEPARATOR + value
                        targetHistData[value] += self.data.getTargetScores()[template]
                    for label in self.data.getNonTargetLabels():
                        template = label + self.LABEL_SEPARATOR + value
                        nonTargetHistData[value] += self.data.getNonTargetScores()[template]
                alpha = 1.0
                allData = []
                allLabels = []
                allColors = []
                for value in targetHistData:
                    try:
                        allColors.append(self.colors[value])
                        allData.append(targetHistData[value])
                        allLabels.append(value + ' (target)')
                    except Exception:
                        pass
                for value in nonTargetHistData:
                    try:
                        allColors.append(self.colors[value])
                        allData.append(nonTargetHistData[value])
                        allLabels.append(value + ' (non target)')
                    except Exception:
                        pass
                if self.debug:
                    print 'allColors:', allColors
                try:
                    plt.hist(allData, self.config.getNrBins(), normed=self.config.getNormHist(), alpha=alpha, label=allLabels)
                except Exception:
                    print "Error: could not plot histogram!"
                    print "len(allData): %d\nnrBins: %d" % (len(allData), self.config.getNrBins())
                    print "allLabels: %s" % (allLabels)
                    pass
                plt.legend()
            else:
                plt.hist(nonTargetScores, self.config.getNrBins(), normed=self.config.getNormHist(), facecolor='red', alpha=1.0)
                plt.hist(targetScores, self.config.getNrBins(), normed=self.config.getNormHist(), facecolor='green', alpha=0.7)
                plt.title(r"Histogram for '%s'" % (self.title))
        plt.grid(True)
        plt.xlabel('Target and Non Target Scores for all Meta Values')
        plt.show()

