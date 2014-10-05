#!/usr/bin/env python2.7

_author_ = 'drs. ing. Jos Bouten'

'''
    zoo.py

    Basic object which is super to the boutenzoo and alexanderzoo objects

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

import sys
import os.path
from os import makedirs
from scipy import stats
import numpy
import collections
from format import Format
from math import sqrt, atan2, sin
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from utils import sanitize

class Zoo(Format):
    def __init__(self, data, config, debug):
        Format.__init__(self, debug)
        self.data = data
        self.config = config
        self.debug = debug
        self.worms = []
        self.chameleons = []
        self.phantoms = []
        self.doves = []
        self.limitedStdDevs = set()
        self.plotType = 'zoo_plot'
        self.referencesWithAnnotation = []
        self.person = []
        self._pointsWithAnnotation = []
        self.annotateQuartileMembers = self.config.getAnnnotateQuartileMembers()
        self.useColorsForQuartileRanges = self.config.getUseColorsForQuartileRanges()

    def getWorms(self):
        return self.worms

    def getChameleons(self):
        return self.chameleons

    def getPhantoms(self):
        return self.phantoms

    def getDoves(self):
        return self.doves

    def getLimited(self):
        return self.limitedStdDevs

    def _addWorm(self, worm):
        self.worms.append(worm)

    def _addChameleon(self, chameleon):
        self.chameleons.append(chameleon)

    def _addPhamtom(self, phantom):
        self.phantoms.append(phantom)

    def _addDove(self, dove):
        self.doves.append(dove)

    def _addLimited(self, info):
        self.limitedStdDevs.add(info)

    def _write2file(self, filename, animals):
        try:
            f = open(filename, 'wt')
        except Exception, e:
            print e
            sys.exit(1)
        else:
            animals.sort()
            for animal in animals:
                if self.debug:
                    print "animal:>%s<" % (animal)
                tmp = animal.split(self.LABEL_SEPARATOR)
                thisAnimal = tmp[0]
                metaValue = tmp[1]
                f.write("%s %s\n" % (thisAnimal, metaValue))
            f.close()
            return len(animals)

    def _printText(self, name, l, filename):
        if l > 1:
            print "Writing %d %ss to %s" % (l, name, filename)
        else:
            print "Writing %d %s to %s" % (l, name, filename)

    def writeAnimals2file(self):
        try:
            if not os.path.exists(self.config.getOutputPath()):
                makedirs(self.config.getOutputPath())
        except Exception, e:
            print e
            sys.exit(1)

        path = self.config.getOutputPath() + os.path.sep
        if self.debug:
            print 'zoo._write2file: path:', path

        thisPlotTitle = sanitize(self.data.title)

        #
        #  Worms
        #
        animals = self.getWorms()
        la = len(animals)
        if la > 0:
            filename = path + thisPlotTitle + '_worms.txt'
            self._printText('worm', la, filename)
            self._write2file(filename, animals)
        else:
            print 'No worms to save.'
        #
        # Chameleons
        #
        animals = self.getChameleons()
        la = len(animals)
        if la > 0:
            filename = path + thisPlotTitle + '_chameleons.txt'
            self._printText('chameleon', la, filename)
            self._write2file(filename, animals)
        else:
            print 'No chameleons to save.'
        #
        # Phantoms
        #
        animals = self.getPhantoms()
        la = len(animals)
        if la > 0:
            filename = path + thisPlotTitle + '_phantoms.txt'
            self._printText('phantom', la, filename)
            self._write2file(filename, self.getPhantoms())
        else:
            print 'No phantoms to save.'
        #
        # Doves
        #
        animals = self.getDoves()
        la = len(animals)
        if la > 0:
            filename = path + thisPlotTitle + '_doves.txt'
            self._printText('dove', la, filename)
            self._write2file(filename, animals)
        else:
            print 'No doves to save.'

        limited = list(self.getLimited())
        la = len(limited)
        if la > 0:
            filename = path + thisPlotTitle + '_limited.txt'
            self._printText('label', la, filename)
            self._write2file(filename, limited)
        else:
            print 'No computed std dev values were limited.'


    def _limit(self, value, maxLevel, minLevel):
        '''
        Limit value to a maximum or minimum value.

        :param value: float: number to fbe limited
        :param maxLevel: float: maximum value
        :param minLevel: float: minimum value
        :return: float: limited value
        '''
        limited = False
        if value > 2 * maxLevel:
            value = 2 * maxLevel
            limited = True
        if value < minLevel:
            value = minLevel
            limited = True
        return value, limited

    def _computeZooStats(self):
        '''
        Compute mean target scores and mean non target scores to be used in zoo plot (Yaget et al.)
        '''
        self.aimsv = {}
        self.agmsv = {}

        for pattern in self.data.getMetaDataValues():
            for keyPlusPattern in self.data.getTargetScores().keys():
                if pattern in keyPlusPattern:
                    #print 'computeZooStats:agmsv:pattern:', pattern, 'keyPlusPattern:', keyPlusPattern
                    self.agmsv[keyPlusPattern] = self.data.compAverageScore(self.data.getTargetScores()[keyPlusPattern])
            for keyPlusPattern in self.data.getNonTargetScores().keys():
                if pattern in keyPlusPattern:
                    #print 'computeZooStats:aimsv:pattern:', pattern, 'keyPlusPattern:', keyPlusPattern
                    self.aimsv[keyPlusPattern] = self.data.compAverageScore(self.data.getNonTargetScores()[keyPlusPattern])
        for pattern in self.agmsv:
            if pattern in self.aimsv:
                self.person.append((pattern, self.aimsv[pattern], self.agmsv[pattern]))

        if len(self.person) == 0:
            print "Error:Unable to compute zoo statistics."
            print '_computeZooStats:len(agmsv):', len(self.agmsv)
            print '_computeZooStats:len(aimsv):', len(self.aimsv)
            sys.exit(1)

        if self.debug:
            print 'len(self.person): ', len(self.person)
            print '_computeZooStats:len(agmsv):', len(self.agmsv)
            print '_computeZooStats:len(aimsv):', len(self.aimsv)

        self.aimsLow = stats.scoreatpercentile(self.aimsv.values(), 25)
        self.aimsHigh = stats.scoreatpercentile(self.aimsv.values(), 75)
        self.agmsLow = stats.scoreatpercentile(self.agmsv.values(), 25)
        self.agmsHigh = stats.scoreatpercentile(self.agmsv.values(), 75)

        # Compute min and max aim and agm values irrespective
        # of values for target and non target experiments.
        self.aim_mi = self.agm_mi = 1.0E99
        self.aim_ma = self.agm_ma = -1.0E99
        for pattern in self.agmsv.keys():
            self.agm_mi, self.agm_ma = self.data.minmax(self.agmsv[pattern], self.agm_mi, self.agm_ma)
        for pattern in self.aimsv.keys():
            self.aim_mi, self.aim_ma = self.data.minmax(self.aimsv[pattern], self.aim_mi, self.aim_ma)

        if self.debug:
            print '_computeZooStats: agm_mi, agm_ma:', self.agm_mi, self.agm_ma
            print '_computeZooStats: aim_mi, aim_ma:', self.aim_mi, self.aim_ma


    def _computeZooStatsAlexanderStyle(self):
        '''
        Compute statistics to plot ellipses in zooplot as published by Alexander et al. IAFPA Zurich, 2014
        '''
        self._computeZooStats()
        # Now we need the std for width and height
        # of the ellipses we want to draw in the plot.
        self.aimsStdDev = collections.defaultdict(float)
        self.agmsStdDev = collections.defaultdict(float)

        # To compute averages and std dev of std dev we need to collect all stdDevs.
        allTargetStdDevs = []
        allNonTargetStdDevs = []

        # labels: p1000, p1001, p1002 etc.
        self.labels = self.data.getTargetLabels()
        if self.debug:
            print '_computeZooStatsAlexanderStyle for agms'

        # stdDevs are computed per label, irrespective of the meta data values
        for label in self.labels:
            if label in self.data.getLabelsWithTargetScores():
                self.agmsStdDev[label] = numpy.std(self.data.getTargetScores4Label(label))
                allTargetStdDevs.append(self.agmsStdDev[label])
        if self.debug:
            print '_computeZooStatsAlexanderStyle for aims'
        for label in self.labels:
            if label in self.data.getLabelsWithNonTargetScores():
                self.aimsStdDev[label] = numpy.std(self.data.getNonTargetScores4Label(label))
                allNonTargetStdDevs.append(self.aimsStdDev[label])

        self.unitTargetStdDev = numpy.std(allTargetStdDevs)
        self.unitNonTargetStdDev = numpy.std(allNonTargetStdDevs)
        self.unitMeanTargetStdDev = numpy.average(allTargetStdDevs)
        self.unitMeanNonTargetStdDev = numpy.average(allNonTargetStdDevs)
        #
        # Central point of the plot is determined by the mean of agms and aims
        # This point is plotted as a black dot and is meant as a reference
        self.meanAgms = self.data.compAverageScore(self.agmsv.values())
        self.meanAims = self.data.compAverageScore(self.aimsv.values())
        if self.debug:
            print 'central point will be at:', self.meanAgms, self.meanAims

        # At max we plot 3 x normalized std dev = 3.
        SATURATION_LEVEL = 3
        MIN_STD_DEV = 0.01
        for label in self.aimsStdDev:
            self.aimsStdDev[label] = SATURATION_LEVEL + \
                                (self.aimsStdDev[label] - self.unitMeanNonTargetStdDev) / self.unitNonTargetStdDev
            self.agmsStdDev[label] = SATURATION_LEVEL + \
                                (self.agmsStdDev[label] - self.unitMeanTargetStdDev) / self.unitTargetStdDev
            if self.config.getLimitStdDevs():
                copy = self.aimsStdDev[label]
                self.aimsStdDev[label], valueWasLimited = self._limit(self.aimsStdDev[label], SATURATION_LEVEL, MIN_STD_DEV)
                if valueWasLimited:
                    self._addLimited(label + self.LABEL_SEPARATOR + 'non target std dev: ' + str(copy))

                copy = self.agmsStdDev[label]
                self.agmsStdDev[label], valueWasLimited = self._limit(self.agmsStdDev[label], SATURATION_LEVEL, MIN_STD_DEV)
                if valueWasLimited:
                    self._addLimited(label + self.LABEL_SEPARATOR + 'target std dev: ' + str(copy))

        # Compute minStdDev and maxStdDev to compute alpha values for ellipses.
        minAimsStdDev = 1.0E99
        maxAimsStdDev = 0.0
        minAgmsStdDev = 1.0E99
        maxAgmsStdDev = 0.0
        minAlphaStdDev = 1.0E99
        maxAlphaStdDev = 0.0
        self.newLabels = []

        for label in self.labels:
            if label in self.aimsStdDev and label in self.agmsStdDev:
                self.newLabels.append(label)
                minAlphaStdDev = min(minAlphaStdDev, self.aimsStdDev[label] + self.agmsStdDev[label])
                maxAlphaStdDev = max(maxAlphaStdDev, self.aimsStdDev[label] + self.agmsStdDev[label])
                minAimsStdDev = min(minAimsStdDev, self.aimsStdDev[label])
                minAgmsStdDev = min(minAgmsStdDev, self.agmsStdDev[label])
                maxAimsStdDev = max(maxAimsStdDev, self.aimsStdDev[label])
                maxAgmsStdDev = max(maxAgmsStdDev, self.agmsStdDev[label])
        self.StdDevAlphaRange = (maxAlphaStdDev - minAlphaStdDev)
        self.StdDevAlphaMin = minAlphaStdDev

        if self.debug:
            print 'maxAgmsStdDev:', maxAgmsStdDev
            print 'minAgmsStdDev:', minAgmsStdDev
            print 'maxAimsStdDev:', maxAimsStdDev
            print 'minAimsStdDev:', minAimsStdDev
        self.minAimsStdDev = minAimsStdDev
        self.minAgmsStdDev = minAgmsStdDev
        self.maxAgmsStdDev = maxAgmsStdDev
        self.maxAimsStdDev = maxAimsStdDev


    def isNear(self, x1, y1, (x2, y2), thresholdX, thresholdY):
        dX = (x2 - x1)
        dY = (y2 - y1)
        #print dX, thresholdX, dY, thresholdY
        # If label is within 0.1 of unit std, to position
        # then return True, else False
        if abs(dX) < abs(thresholdX) and abs(dY) < abs(thresholdY):
            return True
        else:
            return False


    def findDataPointsNear(self, x1, y1):
        '''
        Find data point(s) close to the position of the mouse click.

        :param x1: float: mouse x data position
        :param y1: float: mouse y data position
        :return: list: list of labels within 0.1 unit std of position clicked.
        '''
        if self.debug:
            print "unitNonTargetStdDev:", self.unitNonTargetStdDev
            print "unitTargetStdDev:", self.unitTargetStdDev
            print "unitMeanNonTargetStdDev:", self.unitMeanNonTargetStdDev
            print "unitMeanTargetStdDev:", self.unitMeanTargetStdDev
        ret = []
        for pattern in self.agmsv:
            x2 = self.agmsv[pattern]
            # pattern might not be in aimsv
            try:
                y2 = self.aimsv[pattern]
                xRange = abs(self.agm_ma - self.agm_mi)
                yRange = abs(self.aim_ma - self.aim_mi)
                thresholdX = 3 * xRange / self.config.getScaleFactor()
                thresholdY = 3 * yRange / self.config.getScaleFactor()
                if self.isNear(x1, y1, (x2, y2), thresholdX, thresholdY):
                    ret.append((pattern, x2, y2))
            except Exception:
                pass
        return ret


    def _getXyOfPoint4pattern(self, pattern, pointsWithAnnotation):
        for point, annotation, thisPattern, xy in pointsWithAnnotation:
            if thisPattern == pattern:
                return xy
        return None


    def _getXyOfPoints4label(self, label, pointsWithAnnotation):
        ret = []
        #print '_getXyOfPoints4label:label:', label
        for point, annotation, pattern, xy in pointsWithAnnotation:
            if label == self.getLabelFromPattern(pattern):
                ret.append(xy)
        return ret


    def saveExceptionalAnimals(self):
        # Do the WWF thing!
        # See also http://www.worldwildlife.org

        # Chameleons
        for (label, aims, agms) in self.person:
            if (aims > self.aimsHigh) and (agms > self.agmsHigh):
                self._addChameleon(label)

        # Phantoms
        for (label, aims, agms) in self.person:
            if (aims < self.aimsLow) and (agms < self.agmsLow):
                self._addPhamtom(label)

        # Worms
        for (label, aims, agms) in self.person:
            if (aims > self.aimsHigh) and (agms < self.agmsLow):
                self._addWorm(label)

        # Doves
        for (label, aims, agms) in self.person:
            if (aims < self.aimsLow) and (agms > self.agmsHigh):
                self._addDove(label)

        # Print some of the stats
        if self.debug:
            print("Number of phantoms: %d" % (len(self.phantoms)))
            print("Number of worms: %d" % (len(self.worms)))
            print("Number of chameleons: %d" % (len(self.chameleons)))
            print("Number of doves: %d" % (len(self.doves)))

        # Save results to file.
        self.writeAnimals2file()


    def _connectMetaValues(self, pointsWithAnnotation, axes=plt):
        cnt = 0
        allAngles = []
        allDistances = []
        # We traverse over all patterns except the last.
        for pattern in self.data.getMetaDataValues().keys()[:-1]:
            if self.debug:
                print '_connectMetaValues:pattern:', pattern
            print '_connectMetaValues:pattern:', pattern
            labels = self.data.getMetaDataValues()[pattern]
            print '_connectMetaValues:labels:', labels
            for thisLabel in labels:
                template = self.mkTemplate(thisLabel, pattern)
                startXy = self._getXyOfPoint4pattern(template, pointsWithAnnotation)
                destXy = self._getXyOfPoints4label(thisLabel, pointsWithAnnotation)
                # Draw lines between xy-points.
                if startXy is not None and len(destXy) > 1:
                    # Note, the angles depend on the sequence of meta values processed.
                    if thisLabel in self.data.getLabelsToShowAlways():
                        lineWidth = 1
                    else:
                        lineWidth = 0.2
                    angles, distances = self._drawInterconnectingLines(startXy, destXy, lineWidth, axes)
                    allAngles += angles
                    allDistances += distances
                    cnt += 1
        if cnt == 0:
            print "No ellipses were interconnected."
            print "This means that most likely there were no labels found with contrasting"
            print "meta data values, or there was insufficient data available to do so."

        # We want some stats, don't we?
        if self.debug:
            if self.debug:
                print 'allAngles[:5] = ', allAngles[:5]
                print 'allDistances[:5] = ', allDistances[:5]

        # This is highly experimental, bordering on speculating ...
        deltaZoo = self._compScore(allAngles, allDistances)
        if self.debug:
            print '_connectMetaValues:Score: ', deltaZoo

        return allAngles, allDistances, deltaZoo


    def _compScore(self, angles, distances):

        # Score is computed as follows:
        # s = 1/N * sum( delta_distance_i * sin(Alpha_i) + delta_distance_i)
        # This is done for i = 0 .. length(delta_distances)
        # Delta distance is the difference in distance of two points to the diagonal.
        # S expresses the gain ( or loss ) in recognition when changing meta values.

        totScore = 0.0
        for a, d in zip(angles, distances):
            totScore += d * sin(a) + d
        if totScore > 0.0:
            totScore /= len(angles)
        return totScore


    def _drawInterconnectingLines(self, startXy, destXy, lineWidth, axes=plt):
        allAngles = []
        allDistances = []
        # Note, the angles depend on the sequence of meta values processed.
        (sx, sy) = startXy
        for (ex, ey) in destXy:
            if not (sx, sy) == (ex, ey):
                axes.plot([sx, ex], [sy, ey], color='k', linestyle='-', linewidth=lineWidth)
                mi = min(sx, sy)
                distanceOld = sqrt(pow(sy - mi, 2) + pow(sx - mi, 2))
                # compute distance from diagonal
                mi = min(ex, ey)
                distanceNew = sqrt(pow(ey - mi, 2) + pow(ex - mi, 2))
                distance = distanceNew - distanceOld
                angle = atan2(ey - sy, ex - sx) / 2.0 / 3.14 * 360.0
                allAngles.append(angle)
                allDistances.append(distance)
        return allAngles, allDistances


    def _plotReferenceEllipses(self, axes, xRange, yRange):
        '''
        plot reference ellipse with size corresponding to -2, 0 and 2 x std (i.e. mean)
        :param axes: axes object of the plot
        :param xRange: total x range of the data plotted
        :param yRange: total y range of the data plotted
        :return: Not a thing
        '''

        angle = 0.0
        onlyOnce = True

        if self.config.getShowReference():
            for width in [5, 3, 1]:
                thisWidth = width * xRange / self.config.getScaleFactor()
                thisHeight = width * yRange / self.config.getScaleFactor()
                x = self.agm_mi
                y = self.aim_ma - (self.aim_ma - self.aim_mi) / 20.0
                e = Ellipse((x, y), thisWidth, thisHeight, angle)
                e.set_facecolor('red')
                alpha = self.StdDevAlphaMin/self.StdDevAlphaRange
                e.set_alpha(alpha)
                axes.add_artist(e)

                if onlyOnce:
                    text = 'These 3 ellipses are meant as reference points.\n' + \
                            'From the inner to the outer ellipse\n' + \
                            'they are sized $\\mu$-$2\\sigma$, $\\mu$ and $\\mu$+$2\\sigma$.'
                    onlyOnce = False
                    xOffset = abs(self.agm_ma - self.agm_mi) / 5.0
                    yOffset = abs(self.aim_ma - self.aim_mi) / 10.0
                    xText = x + xOffset
                    yText = y + yOffset
                    annotation = self._annotateEllipse4References(axes, (x, y), xText, yText, text)
                    self.referencesWithAnnotation.append((annotation, (x, y)))
                    if self.config.getShowTextAtReferenceAtStartup():
                        annotation.set_visible(True)
                    else:
                        annotation.set_visible(False)

        if self.config.getShowUnitDataPoint():
            xOffset = abs(self.agm_ma - self.agm_mi) / 15.0
            yOffset = abs(self.aim_ma - self.aim_mi) / 7.0

            # Plot a black dot at the mean value spot of the plot.
            thisWidth = 3 * xRange / self.config.getScaleFactor()
            thisHeight = 3 * yRange / self.config.getScaleFactor()
            (x, y) = (self.meanAgms, self.meanAims)
            e = Ellipse((x, y), thisWidth, thisHeight, angle)
            e.set_facecolor('black')
            e.set_alpha(0.4)
            axes.add_artist(e)
            text = 'This black ellipse is meant as a reference point.\nIt represents the mean of all ellipses shown.'
            xText = x + xOffset
            yText = y + yOffset
            annotation = self._annotateEllipse4References(axes, (x, y), xText, yText, text)
            self.referencesWithAnnotation.append((annotation, (x, y)))
            if self.config.getShowTextAtReferenceAtStartup():
                annotation.set_visible(True)
            else:
                annotation.set_visible(False)


    def _annotateInQuartile(self, xy, height, label, where, axes=plt):
        (x, y) = xy
        dx = x - self.meanAgms
        dy = y - self.meanAims
        xText = 0
        yText = 0
        ha = ''
        va = ''
        ok = False
        xOffset = 0.5 * dx
        yOffset = 0.5 * dy
        if where == 'lt':
            y = y - height / 2
            xText = x + xOffset
            if xText < self.agm_mi:
                xText = self.agm_mi
            yText = y + yOffset
            if yText < self.aim_mi:
                yText = self.aim_mi
            ha = 'right'
            va = 'bottom'
            ok = True
        if where == 'rt':
            y = y - height / 2
            xText = x + xOffset
            if xText > self.agm_ma:
                xText = self.agm_ma
            yText = y + yOffset
            if yText < self.aim_mi:
                yText = self.aim_mi
            ha = 'left'
            va = 'bottom'
            ok = True
        if where == 'lb':
            y = y + height / 2
            xText = x + xOffset
            if xText < self.agm_mi:
                xText = self.agm_mi
            yText = y + yOffset
            if yText < self.aim_mi:
                yText = self.aim_mi
            ha = 'right'
            va = 'top'
            ok = True
        if where == 'rb':
            y = y + height / 2
            xText = x + xOffset
            ddx = 0
            if xText > self.agm_ma:
                xText = self.agm_ma
            yText = y + yOffset - ddx
            if yText > self.aim_ma:
                yText = self.aim_ma
            ha = 'left'
            va = 'top'
            ok = True
        xy = (x, y)
        if ok:
            axes.annotate("%s" % (label),
                     xy,
                     bbox=dict(boxstyle="square", fc="0.8"),
                     backgroundcolor='yellow',
                     xytext=(xText, yText),
                     xycoords='data',
                     textcoords='data',
                     arrowprops=dict(arrowstyle='->'),
                     horizontalalignment=ha,
                     verticalalignment=va,)


    def _annotateEllipse4References(self, axesZoo, xy, xText, yText, text):
        ha = 'left'
        va = 'bottom'
        annotation = axesZoo.annotate("%s" % (text),
                     xy,
                     bbox=dict(boxstyle="square", fc="0.8"),
                     backgroundcolor='yellow',
                     xytext=(xText, yText),
                     xycoords='data',
                     textcoords='data',
                     arrowprops=dict(arrowstyle='->'),
                     horizontalalignment=ha,
                     verticalalignment=va,)
        # By default the annotation is not visible
        annotation.set_visible(False)
        return annotation


    def _annotateEllipse(self, xy, xRange, yRange, text, axes=plt):
        (x, y) = xy
        dx = xRange / 20
        dy = yRange / 15
        xText = x + dx
        yText = y + dy
        ha = 'right'
        va = 'bottom'
        annotation = axes.annotate("%s" % (text),
                     xy,
                     bbox=dict(boxstyle="square", fc="0.8"),
                     backgroundcolor='yellow',
                     xytext=(xText, yText),
                     xycoords='data',
                     textcoords='data',
                     arrowprops=dict(arrowstyle='->'),
                     horizontalalignment=ha,
                     verticalalignment=va,)
        # By default the annotation is not visible
        if self.config.getShowAnnotationsAtStartup():
            annotation.set_visible(True)
        else:
            annotation.set_visible(False)
        return annotation


    def drawLegend(self, colors):
        '''
        Draw a color legend for the metadata on the upper right
        side of the plot, if the metadata can be grouped in more
        than one group.
        '''

        nrColors = len(colors)
        if nrColors > 1:
            if nrColors > 10:
                incr = float((self.aim_ma - self.aim_mi) / 6.0 / nrColors)
            else:
                incr = float((self.aim_ma - self.aim_mi) / 20.0 / nrColors)
            width = float((self.agm_ma - self.agm_mi) / 20.0)
            delta = 0
            boxes = []
            xBase = self.agm_ma - width
            yBase = self.aim_mi

            if self.debug:
                print 'drawLegend:self.colors.items():', colors.items()
                print 'drawLegend:self.colors.keys():', colors.keys()
            for key in sorted(colors.keys()):
                Color = colors[key]
                points = [[xBase, yBase + delta], [xBase, yBase + incr + delta], [xBase + width, yBase + incr + delta],
                          [xBase + width, yBase + delta], [xBase, yBase + delta]]
                rect = plt.Polygon(points, closed=True, fill=True, color=Color)
                boxes.append(rect)
                plt.text(xBase + 1.3 * width, yBase + incr + delta, self.prettyfy(key))
                delta += 1.5 * incr
                plt.gca().add_patch(rect)


    def _plotAxes(self, comment, yagerStyle, title, axes):
        '''

            Add axes to the plot and include boxes for the
            quartile ranges in red for the phantoms, in magenta for
            the doves, in green for the worms and in blue for the
            chameleons.

        :param comment: string: text to be added as comment to the plot's title
        :param yagerStyle: boolean: when False will inverse y-axes of the plot
        :param axes: axes object
        :return:
        '''

        yRange = abs(self.aim_ma - self.aim_mi)
        if yagerStyle:
            # Axes that shows low scores at the top of the plot, low scores at the bottom
            axes.set_ylim(self.aim_ma + 0.105 * yRange, self.aim_mi - 0.1 * yRange)
        else:
            # Axes that shows low scores at the bottom of the plot, high scores at the top.
            axes.set_ylim(self.aim_mi - 0.1 * yRange, self.aim_ma + 0.05 * yRange)
        xRange = abs(self.agm_ma - self.agm_mi)
        axes.set_xlim(self.agm_mi - 0.1 * xRange, self.agm_ma + 0.1 * xRange)

        # Do not put title in title field as this will clash with the x-label of the histogram
        # Put it in the zoo plot in a text field
        if len(comment) > 0:
            title = "zoo plot for '%s %s'" % (title, comment)

        else:
            title = "zoo plot for '%s'" % (title)

        axes.text(self.agmsHigh + 0.05 * xRange , self.aim_mi - 0.05 * yRange, title,
                  bbox={'facecolor': 'black', 'alpha': 0.1, 'pad': 10})

        axes.set_xlabel('Average Target Match Score')
        axes.set_ylabel('Average Non Target Match Score')

        # Phantoms
        self._plotBox(axes, self.agm_mi - 0.1 * xRange, self.aim_mi - 0.1 * yRange, self.agmsLow, self.aimsLow, 'r-')
        axes.text(self.agm_mi - 0.085 * xRange, self.aim_mi - 0.05 * yRange, 'PHANTOMS',
                  bbox={'facecolor': 'red', 'alpha': 0.1, 'pad': 10})
        # Doves
        self._plotBox(axes, self.agmsHigh, self.aim_mi - 0.1 * yRange, self.agm_ma + 0.1 * xRange, self.aimsLow, 'm-')
        axes.text(self.agm_ma, self.aim_mi - 0.05 * yRange, 'DOVES',
                  bbox={'facecolor': 'magenta', 'alpha': 0.1, 'pad': 10})
        # Worms
        self._plotBox(axes, self.agm_mi - 0.1 * xRange, self.aimsHigh, self.agmsLow, self.aim_ma + 0.1 * yRange, 'g-')
        if yagerStyle:
            axes.text(self.agm_mi - 0.085 * xRange, self.aim_ma + 0.085 * yRange, 'WORMS',
                      bbox={'facecolor': 'green', 'alpha': 0.1, 'pad': 10})
        else:
            axes.text(self.agm_mi - 0.085 * xRange, self.aim_ma - 0.085 * yRange, 'WORMS',
                      bbox={'facecolor': 'green', 'alpha': 0.1, 'pad': 10})
        # Chameleons
        self._plotBox(axes, self.agmsHigh, self.aimsHigh, self.agm_ma + 0.1 * xRange, self.aim_ma + 0.1 * yRange, 'b-')
        if yagerStyle:
            axes.text(self.agm_ma, self.aim_ma + 0.085 * yRange, 'CHAMELEONS',
                      bbox={'facecolor': 'blue', 'alpha': 0.1, 'pad': 10})
        else:
            axes.text(self.agm_ma, self.aim_ma - 0.085 * yRange, 'CHAMELEONS',
                      bbox={'facecolor': 'blue', 'alpha': 0.1, 'pad': 10})

        # Last but not least, plot the graph.
        axes.grid()


    def _plotBox(self, plt, x1, y1, x2, y2, col):
        '''
        plot a box with a colored border (e.g. used to delimit quartile ranges in zoo plot)

        :param plt: plot object
        :param x1: int: x-coordinate of lower left corner of box
        :param y1: int: y-coordinate of lower left corner of box
        :param x2: int: x-coordinate of upper right corner of box
        :param y2: int: y-coordinate of upper right corner of box
        :param col: string: color of box border
        :return: Not a thing

        '''
        # draw line from left top to right top
        plt.plot([x1, x2], [y1, y1], col, lw=2)
        # draw line from right top to right bottom
        plt.plot([x2, x2], [y1, y2], col, lw=2)
        # draw line from right bottom to left bottom
        plt.plot([x2, x1], [y2, y2], col, lw=2)
        # draw line from left bottom to left top
        plt.plot([x1, x1], [y2, y1], col, lw=2)


    def _plotDistributions(self, colors, axesZoo):
        '''
        Plot the average target scores against the average non target
        scores using ellipses to show a measure of each label's distribution.

        :param axes: axes object to plot data on
        :return:
        '''
        angle = 0.0
        count = 0
        if self.debug:
            print "_plotDistributions: agmsLow, agmsHigh, aimsLow, aimsHigh:", self.agmsLow, self.agmsHigh, self.aimsLow, self.aimsHigh

        labelsDrawn = set()
        xRange = abs(self.agm_ma - self.agm_mi)
        yRange = abs(self.aim_ma - self.aim_mi)
        scaleFactor = self.config.getScaleFactor()
        alphaLimitFactor = self.config.getOpacityLimitFactor()
        xFactor = xRange / scaleFactor
        # xFactor? Yep, even zoo plots need to have a certain x-factor.
        # McElderry for ever !
        labelsToShow = self.data.getLabelsToShowAlways()
        yFactor = yRange / scaleFactor
        for pattern in self.data.getMetaDataValues().keys():
            labels = self.data.getMetaDataValues()[pattern]
            for thisLabel in labels:
                template = self.mkTemplate(thisLabel, pattern)
                if template in self.agmsv and template in self.aimsv:
                    width = self.agmsStdDev[thisLabel]
                    height = self.aimsStdDev[thisLabel]
                    # If labels were added to the command line, we can make the corresponding ellipses
                    # more prominent by dimming the other ellipses and making the interconnecting
                    # lines thinner.
                    if not thisLabel in labelsToShow:
                        alpha = 1
                    else:
                        alpha = self.config.getDimmingFactor() * ((width + height) - self.StdDevAlphaMin) / self.StdDevAlphaRange
                    xy = [self.agmsv[template], self.aimsv[template]]
                    e = Ellipse(xy, width * xFactor, height * yFactor, angle)
                    e.set_facecolor(colors[pattern])
                    if len(labelsToShow) > 0:
                        e.set_alpha(1 - alphaLimitFactor * alpha)

                    # Limit opacity so that the ellipses wil not become too transparent.
                    if self.config.getUseOpacityForBigEllipses():
                        alpha = ((width + height) - self.StdDevAlphaMin) / self.StdDevAlphaRange
                        e.set_alpha(1 - alphaLimitFactor * alpha)

                    # Chameleon: BLUE
                    if (self.aimsv[template] > self.aimsHigh) and (self.agmsv[template] > self.agmsHigh):
                        if self.annotateQuartileMembers:
                            self._annotateInQuartile(xy, height, thisLabel, 'rb', axesZoo)
                        if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                            e.set_facecolor('blue')
                    # Phantom: RED
                    if (self.aimsv[template] < self.aimsLow) and (self.agmsv[template] < self.agmsLow):
                        if self.annotateQuartileMembers:
                            self._annotateInQuartile(xy, height, thisLabel, 'lt', axesZoo)
                        if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                            e.set_facecolor('red')
                    # Worms: GREEN
                    if (self.aimsv[template] > self.aimsHigh) and (self.agmsv[template] < self.agmsLow):
                        if self.annotateQuartileMembers:
                            self._annotateInQuartile(xy, height, thisLabel, 'lb', axesZoo)
                        if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                            e.set_facecolor('green')
                    # Doves: MAGENTA
                    if (self.aimsv[template] < self.aimsLow) and (self.agmsv[template] > self.agmsHigh):
                        if self.annotateQuartileMembers:
                            self._annotateInQuartile(xy, height, thisLabel, 'rt', axesZoo)
                        if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                            e.set_facecolor('magenta')

                    # Put the ellipse in the figure
                    point = axesZoo.add_artist(e)

                    # If there are several distinct meta data values, they are interconnected.
                    # In that case we do not need to annotate both ellipses.
                    if self.config.getInterconnectMetaValues():
                        if thisLabel in self.data.getLabelsToShowAlways() and thisLabel not in labelsDrawn:
                            labelsDrawn.add(thisLabel)
                            annotation = self._annotateEllipse(xy, xRange, yRange, thisLabel, axesZoo)
                            self._pointsWithAnnotation.append([point, annotation, template, xy])
                            annotation.set_visible(True)
                        else:
                            annotation = self._annotateEllipse(xy, xRange, yRange, thisLabel, axesZoo)
                            self._pointsWithAnnotation.append([point, annotation, template, xy])
                            annotation.set_visible(False)
                    else:
                        annotation = self._annotateEllipse(xy, xRange, yRange, thisLabel, axesZoo)
                        self._pointsWithAnnotation.append([point, annotation, template, xy])
                        if thisLabel in self.data.getAlwaysShowTheseLabels():
                            annotation.set_visible(True)
                    count += 1
        if self.debug:
            print '_plotDistributions:count:', count

        # Plot some ellipses meant for reference but only
        # if we do not show annotations at startup.
        if not self.config.getShowAnnotationsAtStartup():
            self._plotReferenceEllipses(axesZoo, xRange, yRange)