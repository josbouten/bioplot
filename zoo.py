#!/usr/bin/env python2.7

_author_ = 'drs. ing. Jos Bouten'

'''
    zoo.py

    Basic object which is super to the boutenzoo and alexanderzoo objects

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

import sys
import os.path
from os import makedirs
from scipy import stats
import numpy
import collections
from math import sqrt, atan2, sin

import matplotlib.pyplot as plt

from matplotlib.patches import Ellipse

from eer import Eer
from utils import sanitize

# import these super classes
from format import Format
from cllr import Cllr
from probability import Probability
from collections import defaultdict
from subject import Subject
# import utilities
from utils import assignColors2MetaDataValue


class Zoo(Format, Probability, Cllr):
    def __init__(self, thisData, thisConfig, thisDebug):
        self.data = thisData
        self.config = thisConfig
        self.debug = thisDebug
        Format.__init__(self, self.debug)
        Cllr.__init__(self, self.data, self.config, self.debug)
        self._worms = []
        self._chameleons = []
        self._phantoms = []
        self._doves = []
        self._limited = set()
        self.plotType = 'zoo_plot'
        self.referencesWithAnnotation = []
        self.subject = []
        self._pointsWithAnnotation = []
        self.annotateEllipses = self.config.getAnnnotateEllipses()
        self.useColorsForQuartileRanges = self.config.getUseColorsForQuartileRanges()
        self.subjects = {}
        self.aimsv = {}
        self.agmsv = {}
        self.lenAgmsv = {}
        self.lenAimsv = {}

        self.unitTargetStdDev = collections.defaultdict(list)
        self.unitNonTargetStdDev = collections.defaultdict(list)
        self.unitMeanTargetStdDev = collections.defaultdict(list)
        self.unitMeanNonTargetStdDev = collections.defaultdict(list)

        self.agmStdDevMin = collections.defaultdict(list)
        self.agmStdDevMax = collections.defaultdict(list)
        self.aimStdDevMin = collections.defaultdict(list)
        self.aimStdDevMax = collections.defaultdict(list)

        self.aim_mi = collections.defaultdict(float)
        self.aim_ma = collections.defaultdict(float)
        self.agm_mi = collections.defaultdict(float)
        self.agm_ma = collections.defaultdict(float)

        self.aim_maxAll = -1E99
        self.aim_minAll = 1e99
        self.agm_maxAll = -1E99
        self.agm_minAll = 1E99

        self.meanAgms = collections.defaultdict(list)
        self.meanAims = collections.defaultdict(list)

        self.aimsLow = collections.defaultdict(list)
        self.aimsHigh = collections.defaultdict(list)
        self.agmsLow = collections.defaultdict(list)
        self.agmsHigh = collections.defaultdict(list)

        metaDataValues = self.data.getMetaDataValues()
        metaColors = self.config.getMetaColors()
        self.colors = assignColors2MetaDataValue(metaDataValues, metaColors)
        self.nrColors = len(self.colors.keys())
        if self.debug:
            print 'colors:', self.colors
            print 'nr colors:', len(self.colors.keys())

    def getWorms(self):
        return self._worms

    def getChameleons(self):
        return self._chameleons

    def getPhantoms(self):
        return self._phantoms

    def getDoves(self):
        return self._doves

    def getLimited(self):
        return self._limited

    def _addWorm(self, worm):
        self._worms.append(worm)

    def _addChameleon(self, chameleon):
        self._chameleons.append(chameleon)

    def _addPhamtom(self, phantom):
        self._phantoms.append(phantom)

    def _addDove(self, dove):
        self._doves.append(dove)

    def _addLimited(self, thisSubject):
        self._limited.add(thisSubject)

    def _writeSubjects2file(self, filename, subjects):
        try:
            f = open(filename, 'wt')
            comment = "# label, metavalue"
            comment += ", average_target_score, average_non_target_score"
            comment += ", #target_scores, #non_target_scores"
            comment += ", average_target_score_stdev, average_non_target_score_stdev"
            f.write("%s\n" % comment)
            for subject in subjects:
                f.write("%s %s %s %s %d %s %f %s\n" %
                        (subject.getLabel(), subject.getMetaValue(),
                         subject.getAgmsv(), subject.getAimsv(),
                         subject.getNumberOfTargets(), subject.getNumberOfNonTargets(),
                         subject.getAgmStdDev(), subject.getAimStdDev()))
            f.close()
        except Exception, e:
            print e
            sys.exit(1)

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
            print 'zoo._writeLimited2file: path:', path

        thisPlotTitle = sanitize(self.data.getTitle())

        #
        #  Worms
        #
        animals = self.getWorms()
        la = len(animals)
        if la > 0:
            filename = path + thisPlotTitle + '_worms.txt'
            self._printText('worm', la, filename)
            self._writeSubjects2file(filename, animals)
        else:
            print 'No _worms to save.'
        #
        # Chameleons
        #
        animals = self.getChameleons()
        la = len(animals)
        if la > 0:
            filename = path + thisPlotTitle + '_chameleons.txt'
            self._printText('chameleon', la, filename)
            self._writeSubjects2file(filename, animals)
        else:
            print 'No _chameleons to save.'
        #
        # Phantoms
        #
        animals = self.getPhantoms()
        la = len(animals)
        if la > 0:
            filename = path + thisPlotTitle + '_phantoms.txt'
            self._printText('phantom', la, filename)
            self._writeSubjects2file(filename, animals)
        else:
            print 'No _phantoms to save.'
        #
        # Doves
        #
        animals = self.getDoves()
        la = len(animals)
        if la > 0:
            filename = path + thisPlotTitle + '_doves.txt'
            self._printText('dove', la, filename)
            self._writeSubjects2file(filename, animals)
        else:
            print 'No _doves to save.'

        limited = list(self.getLimited())
        la = len(limited)
        if la > 0:
            filename = path + thisPlotTitle + '_limited.txt'
            self._printText('label', la, filename)
            self._writeSubjects2file(filename, limited)
        else:
            print 'No computed std dev values were limited.'

    def _limit(self, value, maxLevel, minLevel):
        '''
        Limit value to a maximum or minimum value.

        :param value: float: number to be limited
        :param maxLevel: float: maximum value
        :param minLevel: float: minimum value
        :return: float: limited value
        '''
        limited = False
        if value > maxLevel:
            value = maxLevel
            limited = True
        if value < minLevel:
            value = minLevel
            limited = True
        return value, limited

    def _getValuesFromListOfDicts(self, thisDict, metaValue):
        ret = []
        for key in thisDict:
            if metaValue in key:
                ret.append(thisDict[key])
        return ret

    def computeZooStats(self):
        '''
        Compute mean target scores and mean non target scores to be used in zoo plot (Yaget et al.)
        '''

        for metaValue in self.data.getMetaDataValues():
            for subjectLabelPlusMetaValue in self.data.getTargetScores().keys():
                if metaValue in subjectLabelPlusMetaValue:
                    # print 'computeZooStats:agmsv:subjectLabelPlusMetaValue:', subjectLabelPlusMetaValue, 'subjectLabelPlusMetaValue:', subjectLabelPlusMetaValue
                    elements = self.data.getTargetScores()[subjectLabelPlusMetaValue]
                    self.agmsv[subjectLabelPlusMetaValue] = self.data.compAverageScore(elements)
                    self.lenAgmsv[subjectLabelPlusMetaValue] = len(elements)
                    # else:
                    #     print "Only 1 target value for %s" % subjectLabelPlusMetaValue
            for subjectLabelPlusMetaValue in self.data.getNonTargetScores().keys():
                if metaValue in subjectLabelPlusMetaValue:
                    elements = self.data.getNonTargetScores()[subjectLabelPlusMetaValue]
                    self.aimsv[subjectLabelPlusMetaValue] = self.data.compAverageScore(elements)
                    self.lenAimsv[subjectLabelPlusMetaValue] = len(elements)
                    # else:
                    #     print "Only 1 non target value for %s" % subjectLabelPlusMetaValue
        for subjectLabelPlusMetaValue in self.agmsv:
            if subjectLabelPlusMetaValue in self.aimsv:
                subject = Subject(subjectLabelPlusMetaValue, self.agmsv[subjectLabelPlusMetaValue],
                                  self.aimsv[subjectLabelPlusMetaValue], self.lenAgmsv[subjectLabelPlusMetaValue],
                                  self.lenAimsv[subjectLabelPlusMetaValue], self.debug)
                self.subjects[subjectLabelPlusMetaValue] = subject

        if len(self.subjects) == 0:
            print "Error:Unable to compute zoo statistics."
            print "No labels were found for which there are target AND non target scores."
            sys.exit(1)

        if self.debug:
            print 'computeZooStats:len(agmsv):', len(self.agmsv)
            print 'computeZooStats:len(aimsv):', len(self.aimsv)

        for metaValue in self.data.getMetaDataValues():
            aimsValues = self._getValuesFromListOfDicts(self.aimsv, metaValue)
            if not len(aimsValues) > 1:
                print "Not enough data to plot zoo for %s" % metaValue
                break
            # Compute quartile ranges.
            self.aimsLow[metaValue] = stats.scoreatpercentile(aimsValues, 25)
            self.aimsHigh[metaValue] = stats.scoreatpercentile(aimsValues, 75)
            agmsValues = self._getValuesFromListOfDicts(self.agmsv, metaValue)
            if not len(agmsValues) > 1:
                print "Not enough data to plot zoo for %s" % metaValue
                break
            self.agmsLow[metaValue] = stats.scoreatpercentile(agmsValues, 25)
            self.agmsHigh[metaValue] = stats.scoreatpercentile(agmsValues, 75)

            # Compute min and max aim and agm values irrespective
            # of values for target and non target experiments.
            self.aim_mi[metaValue] = self.agm_mi[metaValue] = self.data.getMaximum4ThisType()
            self.aim_ma[metaValue] = self.agm_ma[metaValue] = self.data.getMinimum4ThisType()
            for subjectLabelPlusMetaValue in self.agmsv.keys():
                self.agm_mi[metaValue], self.agm_ma[metaValue] = \
                    self.data.minMax(self.agmsv[subjectLabelPlusMetaValue], self.agm_mi[metaValue],
                                     self.agm_ma[metaValue])
            for subjectLabelPlusMetaValue in self.aimsv.keys():
                self.aim_mi[metaValue], self.aim_ma[metaValue] = \
                    self.data.minMax(self.aimsv[subjectLabelPlusMetaValue], self.aim_mi[metaValue],
                                     self.aim_ma[metaValue])
            # We need the absolute max and min values for combining all metaValue data in one plot.
            self.aim_maxAll = max(self.aim_maxAll, self.aim_ma[metaValue])
            self.aim_minAll = min(self.aim_minAll, self.aim_mi[metaValue])
            self.agm_maxAll = max(self.agm_maxAll, self.agm_ma[metaValue])
            self.agm_minAll = min(self.agm_minAll, self.agm_mi[metaValue])
            if self.debug:
                print "computeZooStats: %s agm_mi, agm_ma: %f %f" % (
                metaValue, self.agm_mi[metaValue], self.agm_ma[metaValue])
                print "computeZooStats: %s aim_mi, aim_ma: %f %f" % (
                metaValue, self.aim_mi[metaValue], self.aim_ma[metaValue])

    def computeZooStatsAlexanderStyle(self):
        '''
            Compute statistics to plot ellipses in zoo plot as published by Alexander et al. IAFPA Zurich, 2014
        '''
        self.computeZooStats()
        # Now we need the std for width and height
        # of the ellipses we want to draw in the plot.

        # To compute averages and std dev of std dev we need to collect all stdDevs.
        allTargetStdDevs = collections.defaultdict(list)
        allNonTargetStdDevs = collections.defaultdict(list)

        # labels: p1000, p1001, p1002 etc.
        self.labels = self.data.getTargetLabels()
        if self.debug:
            print 'computeZooStatsAlexanderStyle for agms'

        for metaValue in self.data.getMetaDataValues():
            self.agmStdDevMin[metaValue] = self.config.getMaxStdDev()
            self.aimStdDevMin[metaValue] = self.config.getMaxStdDev()
            self.agmStdDevMax[metaValue] = self.config.getMinStdDev()
            self.aimStdDevMax[metaValue] = self.config.getMinStdDev()

        for thisKey in self.subjects.keys():
            subject = self.subjects[thisKey]
            metaValue = subject.getMetaValue()
            # target for each meta value
            targetScores4ThisSubject = self.data.getTargetScores()[thisKey]
            if len(targetScores4ThisSubject) > 1:
                stdDev = numpy.std(targetScores4ThisSubject)
            else:
                stdDev = self.config.getMinStdDev()
            self.agmStdDevMin[metaValue] = min(self.agmStdDevMin[metaValue], stdDev)
            self.agmStdDevMax[metaValue] = max(self.agmStdDevMax[metaValue], stdDev)
            subject.setAgmStdDev(stdDev)

            # non target std for each meta value
            nonTargetScores4ThisSubject = self.data.getNonTargetScores()[thisKey]
            if len(nonTargetScores4ThisSubject) > 1:
                stdDev = numpy.std(nonTargetScores4ThisSubject)
            else:
                stdDev = self.config.getMinStdDev()
            self.aimStdDevMin[metaValue] = min(self.aimStdDevMin[metaValue], stdDev)
            self.aimStdDevMax[metaValue] = max(self.aimStdDevMax[metaValue], stdDev)
            subject.setAimStdDev(stdDev)

        if self.config.getLimitStdDevs():
            # We may need to limit certain stdevs to a max or min value.
            # After this we collect the stdev values in order
            # to compute corrected means and std devs of these stdevs
            # to have proper unit values for scaling
            for thisKey in self.subjects.keys():
                subject = self.subjects[thisKey]
                metaValue = subject.getMetaValue()

                # All stdev values bigger than MAX and smaller than MIN are set to either MAX or MIN.
                unlimitedValue = subject.getAgmStdDev()
                limitedValue, valueWasLimited = self._limit(subject.getAgmStdDev(), self.config.getMaxStdDev(),
                                                     self.config.getMinStdDev())
                if valueWasLimited:
                    self._addLimited(subject)
                    subject.setAgmStdDev(limitedValue)
                    allTargetStdDevs[metaValue].append(limitedValue)
                else:
                    allTargetStdDevs[metaValue].append(unlimitedValue)

                unlimitedValue = subject.getAimStdDev()
                limitedValue, valueWasLimited = self._limit(subject.getAimStdDev(), self.config.getMaxStdDev(),
                                                     self.config.getMinStdDev())
                if valueWasLimited:
                    subject.setAimStdDev(limitedValue)
                    self._addLimited(subject)
                    allNonTargetStdDevs[metaValue].append(limitedValue)
                else:
                    allNonTargetStdDevs[metaValue].append(unlimitedValue)
        else:
            for thisKey in self.subjects.keys():
                subject = self.subjects[thisKey]
                metaValue = subject.getMetaValue()
                allTargetStdDevs[metaValue].append(subject.getAgmStdDev())
                allNonTargetStdDevs[metaValue].append(subject.getAimStdDev())

        for metaValue in self.data.getMetaDataValues():
            self.unitTargetStdDev[metaValue] = numpy.std(allTargetStdDevs[metaValue])
            self.unitNonTargetStdDev[metaValue] = numpy.std(allNonTargetStdDevs[metaValue])
            self.unitMeanTargetStdDev[metaValue] = numpy.average(allTargetStdDevs[metaValue])
            self.unitMeanNonTargetStdDev[metaValue] = numpy.average(allNonTargetStdDevs[metaValue])
            # Central point of the plot is determined by the mean of agms and aims per meta data value.
            # This point is plotted as a black dot and is meant as a reference.
            theseAgmsValues = self.data.getTargetScores4MetaValue(metaValue)
            theseAimValues = self.data.getNonTargetScores4MetaValue(metaValue)
            self.meanAgms[metaValue] = self.data.compAverageScore(theseAgmsValues)
            self.meanAims[metaValue] = self.data.compAverageScore(theseAimValues)
            if self.debug:
                print "central point for %s will be at: %f %f" % (
                metaValue, self.meanAgms[metaValue], self.meanAims[metaValue])

        # At max we plot 3 x normalized std dev = 3.
        for thisKey in self.subjects.keys():
            subject = self.subjects[thisKey]
            metaValue = subject.getMetaValue()
            agmStdDev = self.config.getMaxStdDev() + (subject.getAgmStdDev() -
                        self.unitMeanTargetStdDev[metaValue]) / self.unitTargetStdDev[metaValue]
            subject.setAgmStdDev(agmStdDev)
            aimStdDev = self.config.getMaxStdDev() + (subject.getAimStdDev() -
                        self.unitMeanNonTargetStdDev[metaValue]) / self.unitNonTargetStdDev[metaValue]
            subject.setAimStdDev(aimStdDev)

        self.minSurfaceArea = collections.defaultdict(list)
        self.maxSurfaceArea = collections.defaultdict(list)
        self.surfaceAreaRange = collections.defaultdict(list)

        for metaValue in self.data.getMetaDataValues():
            self.minSurfaceArea[metaValue] = 1.0E99
            self.maxSurfaceArea[metaValue] = 0.0
            self.aim_mi[metaValue] = self.agm_mi[metaValue] = self.data.getMaximum4ThisType()
            self.aim_ma[metaValue] = self.agm_ma[metaValue] = self.data.getMinimum4ThisType()

        for thisKey in self.subjects.keys():
            subject = self.subjects[thisKey]
            metaValue = subject.getMetaValue()
            self.minSurfaceArea[metaValue] = min(self.minSurfaceArea[metaValue], subject.getAgmStdDev() * subject.getAimStdDev())
            self.maxSurfaceArea[metaValue] = max(self.maxSurfaceArea[metaValue], subject.getAgmStdDev() * subject.getAimStdDev())

        for metaValue in self.data.getMetaDataValues():
            self.surfaceAreaRange[metaValue] = (self.maxSurfaceArea[metaValue] - self.minSurfaceArea[metaValue])
            self.agm_mi[metaValue], self.agm_ma[metaValue] = \
                self.data.minMax2(self.agmsv, metaValue, self.agm_mi[metaValue], self.agm_ma[metaValue])
            self.aim_mi[metaValue], self.aim_ma[metaValue] = \
                self.data.minMax2(self.aimsv, metaValue, self.aim_mi[metaValue], self.aim_ma[metaValue])

        if self.debug:
            for metaValue in self.data.getMetaDataValues():
                print "agmStdDevMax[%s]: %f" % (metaValue, self.agmStdDevMax[metaValue])
                print "agmStdDevMin[%s]: %f" % (metaValue, self.agmStdDevMin[metaValue])
                print "aimStdDevMax[%s]: %f" % (metaValue, self.aimStdDevMax[metaValue])
                print "aimStdDevMin[%s]: %f" % (metaValue, self.aimStdDevMin[metaValue])
                print "agm_mi[%s]: %f" % (metaValue, self.agm_mi[metaValue])
                print "agm_ma[%s]: %f" % (metaValue, self.agm_ma[metaValue])
                print "aim_mi[%s]: %f" % (metaValue, self.aim_mi[metaValue])
                print "aim_ma[%s]: %f" % (metaValue, self.aim_ma[metaValue])

    def isNear(self, x1, y1, (x2, y2), thresholdX, thresholdY):
        dX = (x2 - x1)
        dY = (y2 - y1)

        # If label is within 0.1 of unit std to position
        # then return True, else False.
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
            except Exception:
                pass
            else:
                xRange = abs(self.agm_maxAll - self.agm_minAll)
                yRange = abs(self.aim_maxAll - self.aim_minAll)
                thresholdX = 3 * xRange / self.config.getScaleFactor()
                thresholdY = 3 * yRange / self.config.getScaleFactor()
                if self.isNear(x1, y1, (x2, y2), thresholdX, thresholdY):
                    ret.append((pattern, x2, y2))
        return ret

    def _getXyOfPoint4pattern(self, pattern, pointsWithAnnotation):
        for point, annotation, thisPattern, xy in pointsWithAnnotation:
            if thisPattern == pattern:
                return xy
        return None

    def _getXyOfPoints4label(self, label, pointsWithAnnotation):
        ret = []
        # print '_getXyOfPoints4label:label:', label
        for point, annotation, pattern, xy in pointsWithAnnotation:
            if label == self.getLabelFromPattern(pattern):
                ret.append(xy)
        return ret

    def saveExceptionalAnimals(self):
        # Save the animals. Do the WWF thing!
        # See also http://www.worldwildlife.org

        for subject in self.subjects.values():
            # Chameleons
            aims = subject.getAimsv()
            agms = subject.getAgmsv()
            metaValue = subject.getMetaValue()
            if (aims > self.aimsHigh[metaValue]) and (agms > self.agmsHigh[metaValue]):
                self._addChameleon(subject)
            # Phantoms
            elif (aims < self.aimsLow[metaValue]) and (agms < self.agmsLow[metaValue]):
                self._addPhamtom(subject)
            # Worms
            elif (aims > self.aimsHigh[metaValue]) and (agms < self.agmsLow[metaValue]):
                self._addWorm(subject)
            # Doves
            elif (aims < self.aimsLow[metaValue]) and (agms > self.agmsHigh[metaValue]):
                self._addDove(subject)

        # Print some of the stats
        if self.debug:
            print("Number of _phantoms: %d" % (len(self._phantoms)))
            print("Number of _worms: %d" % (len(self._worms)))
            print("Number of _chameleons: %d" % (len(self._chameleons)))
            print("Number of _doves: %d" % (len(self._doves)))

        # Save results to file.
        self.writeAnimals2file()

    def _connectMetaValues(self, pointsWithAnnotation, axes=plt):
        cnt = 0
        allAngles = []
        allDistances = []
        lineWidth = self.config.getLineWidth()
        alpha = 1.0
        # We traverse over all patterns except the last.
        for pattern in sorted(self.data.getMetaDataValues().keys()[:-1]):
            if self.debug:
                print '_connectMetaValues:pattern:', pattern
            labels = self.data.getMetaDataValues()[pattern]

            for thisLabel in labels:
                template = self.mkTemplate(thisLabel, pattern)
                startXy = self._getXyOfPoint4pattern(template, pointsWithAnnotation)
                destXy = self._getXyOfPoints4label(thisLabel, pointsWithAnnotation)
                # Draw lines between xy-points.
                if startXy is not None and len(destXy) > 1:
                    # Note, the angles depend on the sequence of meta values processed.
                    if thisLabel in self.data.getLabelsToShowAlways():
                        lineWidth = 1
                        alpha = 1.0
                    else:
                        if len(self.data.getLabelsToShowAlways()) > 0:
                            # If there were any labels selected make the lines thin and dimm them
                            # so that only the selected labels stand out.
                            lineWidth = self.config.getLineWidth()
                            alpha = (1.0 - self.config.getDimmingFactor())
                        else:
                            alpha = 1.0
                            lineWidth = 1.0
                    angles, distances = self._drawInterconnectingLines(startXy, destXy, lineWidth, alpha, axes)
                    allAngles += angles
                    allDistances += distances
                    cnt += 1
        if cnt == 0:
            print "No ellipses were interconnected."
            print "This means that most likely there were no labels found with contrasting"
            print "meta data values, or there was insufficient data available to do so."
        else:
            # We want some stats, don't we?
            if self.debug:
                print 'allAngles[:5] = ', allAngles[:5]
                print 'allDistances[:5] = ', allDistances[:5]

        # This is still experimental and only makes sense when there are
        # 2 different experiments in the dataset (no more, no less).
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

    def _drawInterconnectingLines(self, startXy, destXy, lineWidth, alpha, axes=plt):
        allAngles = []
        allDistances = []
        # Note, the angles depend on the sequence of meta values processed.
        # This makes sense only when there are 2 meta values.
        (sx, sy) = startXy
        for (ex, ey) in destXy:
            if not (sx, sy) == (ex, ey):
                axes.plot([sx, ex], [sy, ey], color='k', linestyle='-', alpha=alpha, linewidth=lineWidth)
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
        alpha = self.config.getAlpha4ReferenceCircles()
        if self.config.getShowReference():
            baseOffset = 5 * xRange / self.config.getScaleFactor()
            offset = baseOffset
            for metaValue in self.data.getMetaDataValues():
                onlyOnce = True
                for width in [5, 3, 1]:
                    thisWidth = width * xRange / self.config.getScaleFactor()
                    thisHeight = width * yRange / self.config.getScaleFactor()

                    # x = self.agm_mi[metaValue]
                    # y = self.aim_ma[metaValue] - (self.aim_ma[metaValue] - self.aim_mi[metaValue]) / 20.0
                    x = self.agm_minAll + offset
                    y = self.aim_maxAll - (self.aim_maxAll - self.aim_minAll) / 30.0
                    # TOT HIER EN NIET VERDER
                    # Waarom zit de ellipse niet op de onderste lijn?
                    y = self.aim_maxAll

                    e = Ellipse((x, y), thisWidth, thisHeight, angle)
                    e.set_facecolor(self.colors[metaValue])
                    e.set_alpha(alpha)
                    axes.add_artist(e)
                # Create some distance between the unit circles
                offset += 1.2 * baseOffset

                experimentText = "points for experiment: %s.\n" % str(metaValue)
                if onlyOnce:
                    text = "These 3 ellipses are meant as scaled reference\n" + \
                           experimentText + \
                           "From the inner to the outer ellipse\n" + \
                           "they are sized $\\mu$-$2\\sigma$, $\\mu$ and $\\mu$+$2\\sigma$."
                    onlyOnce = False
                    xOffset = abs(self.agm_ma[metaValue] - self.agm_mi[metaValue]) / 5.0
                    yOffset = abs(self.aim_ma[metaValue] - self.aim_mi[metaValue]) / 10.0
                    xText = x + xOffset
                    yText = y + yOffset
                    annotation = self._annotateEllipse4References(axes, (x, y), xText, yText, text)
                    self.referencesWithAnnotation.append((annotation, (x, y)))
                    if self.config.getShowTextAtReferenceAtStartup():
                        annotation.set_visible(True)
                    else:
                        annotation.set_visible(False)

        if self.config.getShowUnitDataPoint():
            alpha = self.config.getAlpha4UnitCircles()
            for metaValue in self.data.getMetaDataValues():
                xOffset = abs(self.agm_ma[metaValue] - self.agm_mi[metaValue]) / 15.0
                yOffset = abs(self.aim_ma[metaValue] - self.aim_mi[metaValue]) / 7.0

                # Plot a black dot at the mean value spot of the plot.
                thisWidth = 3 * xRange / self.config.getScaleFactor()
                thisHeight = 3 * yRange / self.config.getScaleFactor()
                (x, y) = (self.meanAgms[metaValue], self.meanAims[metaValue])
                e = Ellipse((x, y), thisWidth, thisHeight, angle)
                e.set_facecolor('black')
                e.set_alpha(alpha)
                axes.add_artist(e)
                text = "This black ellipse is meant as a reference\npoint for experiment: %s.\nIt represents the mean of all data points shown." % metaValue
                xText = x + xOffset
                yText = y + yOffset
                annotation = self._annotateEllipse4References(axes, (x, y), xText, yText, text)
                self.referencesWithAnnotation.append((annotation, (x, y)))
                if self.config.getShowTextAtReferenceAtStartup():
                    annotation.set_visible(True)
                else:
                    annotation.set_visible(False)

    def _annotateEllipseInQuartile(self, xy, height, label, metaValue, where, axes=plt):
        (x, y) = xy
        dx = x + self.meanAgms[metaValue]
        dy = y + self.meanAims[metaValue]
        xText = 0
        yText = 0
        ha = ''
        va = ''
        ok = False
        xOffset = dx
        yOffset = dy
        if where == 'lt':
            y -= height / 2
            xText = x + xOffset
            if xText < self.agm_mi[metaValue]:
                xText = self.agm_mi[metaValue]
            yText = y + yOffset
            if yText < self.aim_mi[metaValue]:
                yText = self.aim_mi[metaValue]
            ha = 'right'
            va = 'bottom'
            ok = True
        if where == 'rt':
            y -= height / 2
            xText = x + xOffset
            if xText > self.agm_ma[metaValue]:
                xText = self.agm_ma[metaValue]
            yText = y + yOffset
            if yText < self.aim_mi[metaValue]:
                yText = self.aim_mi[metaValue]
            ha = 'left'
            va = 'bottom'
            ok = True
        if where == 'lb':
            y += height / 2
            xText = x + xOffset
            if xText < self.agm_mi[metaValue]:
                xText = self.agm_mi[metaValue]
            yText = y + yOffset
            if yText < self.aim_mi[metaValue]:
                yText = self.aim_mi[metaValue]
            ha = 'right'
            va = 'top'
            ok = True
        if where == 'rb':
            y += height / 2
            xText = x + xOffset
            ddx = 0
            if xText > self.agm_ma[metaValue]:
                xText = self.agm_ma[metaValue]
            yText = y + yOffset - ddx
            if yText > self.aim_ma[metaValue]:
                yText = self.aim_ma[metaValue]
            ha = 'left'
            va = 'top'
            ok = True
        xy = (x, y)
        if ok:
            if self.config.getRunningOSX() or self.config.getRunningWindows():
                axes.annotate("%s" % (label),
                              xy,
                              bbox=dict(boxstyle="square", fc="0.8"),
                              xytext=(xText, yText),
                              xycoords='data',
                              textcoords='data',
                              arrowprops=dict(arrowstyle='->'),
                              horizontalalignment=ha,
                              verticalalignment=va,
                              multialignment='left', )
            else:
                axes.annotate("%s" % (label),
                              xy,
                              bbox=dict(boxstyle="square", fc="0.8"),
                              backgroundcolor='yellow',
                              xytext=(xText, yText),
                              xycoords='data',
                              textcoords='data',
                              arrowprops=dict(arrowstyle='->'),
                              horizontalalignment=ha,
                              verticalalignment=va,
                              multialignment='left', )

    def _annotateEllipse4References(self, axesZoo, xy, xText, yText, text):
        ha = 'left'
        va = 'bottom'
        if self.config.getRunningOSX() or self.config.getRunningWindows():
            annotation = axesZoo.annotate("%s" % (text),
                                          xy,
                                          bbox=dict(boxstyle="square", fc="0.8"),
                                          xytext=(xText, yText),
                                          xycoords='data',
                                          textcoords='data',
                                          arrowprops=dict(arrowstyle='->'),
                                          horizontalalignment=ha,
                                          verticalalignment=va, )
        else:
            annotation = axesZoo.annotate("%s" % (text),
                                          xy,
                                          bbox=dict(boxstyle="square", fc="0.8"),
                                          backgroundcolor='yellow',
                                          xytext=(xText, yText),
                                          xycoords='data',
                                          textcoords='data',
                                          arrowprops=dict(arrowstyle='->'),
                                          horizontalalignment=ha,
                                          verticalalignment=va, )

        # By default the annotation is not visible
        annotation.set_visible(False)
        return annotation

    def _annotateEllipse(self, xy, xRange, yRange, text, axes=plt):
        """

        :rtype : annotation object
        """
        (x, y) = xy
        dx = xRange / 20
        dy = yRange / 15
        xText = x + dx
        yText = y + dy
        ha = 'right'
        va = 'bottom'
        if self.config.getRunningOSX() or self.config.getRunningWindows():
            annotation = axes.annotate("%s" % (text),
                                       xy,
                                       bbox=dict(boxstyle="square", fc="0.8"),
                                       xytext=(xText, yText),
                                       xycoords='data',
                                       textcoords='data',
                                       arrowprops=dict(arrowstyle='->'),
                                       horizontalalignment=ha,
                                       verticalalignment=va,
                                       multialignment='left', )
        else:
            annotation = axes.annotate("%s" % (text),
                                       xy,
                                       bbox=dict(boxstyle="square", fc="0.8"),
                                       backgroundcolor='yellow',
                                       xytext=(xText, yText),
                                       xycoords='data',
                                       textcoords='data',
                                       arrowprops=dict(arrowstyle='->'),
                                       horizontalalignment=ha,
                                       verticalalignment=va,
                                       multialignment='left', )

        # By default the annotation is not visible.
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
        delta = 0.01
        boxes = []

        incr = 0.0
        for metaValue in sorted(colors.keys()):
            if nrColors > 10:
                incr = max(incr, float((self.aim_ma[metaValue] - self.aim_mi[metaValue]) / 6.0 / nrColors))
            else:
                incr = max(incr, float((self.aim_ma[metaValue] - self.aim_mi[metaValue]) / 20.0 / nrColors))

        if self.debug:
            print 'drawLegend:self.colors.items():', colors.items()
            print 'drawLegend:self.colors.keys():', colors.keys()

        legendText = defaultdict(list)
        # Add meta condition value name to legend text.
        for thisMetaValue in sorted(colors.keys()):
            legendText[thisMetaValue].append(thisMetaValue)

        # Compute and show the EER value if so desired
        if self.config.getShowEerValues():
            eerObject = Eer(self.data, self.config, self.debug)
            eerData = eerObject.computeProbabilities(self.eerFunc)
            for thisMetaValue in sorted(colors.keys()):
                for metaValue, PD, PP, X in eerData:
                    if thisMetaValue == metaValue:
                        try:
                            eerValue, score = eerObject.computeEer(PD, PP, X)
                        except Exception, e:
                            print "DrawLegend: problem computing EER for %s" % thisMetaValue
                        else:
                            eerValue *= 100
                            if eerValue < 10.0:
                                eerStr = "Eer:  %.2f%s" % (eerValue, '%')
                            else:
                                eerStr = "Eer: %2.2f%s" % (eerValue, '%')
                            legendText[thisMetaValue].append(eerStr)
                        break

        # Compute and show the Cllr value if so desired
        if self.config.getShowCllrValues():
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

        # Compute and show the CllrMin value if so desired
        if self.config.getShowMinCllrValues():
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

        maxTextLength = 0
        for metaValue in legendText:
            length = 0
            for el in legendText[metaValue]:
                length += len(el)
            maxTextLength = max(length, maxTextLength)

        pixelWidth = 8.0
        (nrHorzPixels, nrVertPixels) = self.config.getScreenResolutionTuple()
        xWidthInPixels = self.config.getZwidth() * nrHorzPixels
        if nrHorzPixels > 1280:
            factor = 17.0
        else:
            factor = 20.0

        xWidth = float((self.agm_maxAll - self.agm_minAll) / 20.0)
        yBase = self.aim_minAll
        xBase = self.agm_maxAll
        # Find local minimum of agm_ma values and put legend next to it
        for metaValue in sorted(colors.keys()):
            xBase = min(xBase, self.agm_ma[metaValue])
        xBase -= xWidth
        for metaValue in sorted(colors.keys()):
            thisLegendText = ''
            # Compile legend text.
            for el in legendText[metaValue]:
                thisLegendText += el + ', '
            # Remove last comma and space.
            thisLegendText = thisLegendText[:-2]
            offset = factor * xWidth * ((pixelWidth * maxTextLength) / xWidthInPixels)

            Color = colors[metaValue]
            points = [[xBase - offset, yBase + delta],
                      [xBase - offset, yBase + incr + delta],
                      [xBase + xWidth / 1.5 - offset, yBase + incr + delta],
                      [xBase + xWidth / 1.5 - offset, yBase + delta],
                      [xBase - offset, yBase + delta]]
            rect = plt.Polygon(points, closed=True, fill=True, color=Color)
            boxes.append(rect)
            plt.text(xBase + xWidth - offset, yBase + incr + delta, thisLegendText)
            delta += 1.5 * incr
            plt.gca().add_patch(rect)

    def getRanges(self):
        yRange = collections.defaultdict(list)
        xRange = collections.defaultdict(list)
        yRangeAll = 0.0
        xRangeAll = 0.0

        for metaValue in self.data.getMetaDataValues():
            yRange[metaValue] = 1E-99
            xRange[metaValue] = 1E-99

        for metaValue in self.data.getMetaDataValues():
            yRange[metaValue] = max(yRange[metaValue], abs(self.aim_ma[metaValue] - self.aim_mi[metaValue]))
            xRange[metaValue] = max(xRange[metaValue], abs(self.agm_ma[metaValue] - self.agm_mi[metaValue]))
            yRangeAll = max(yRangeAll, yRange[metaValue])
            xRangeAll = max(xRangeAll, xRange[metaValue])
        return xRange, yRange, xRangeAll, yRangeAll

    def _plotAxes(self, comment, yagerStyle, title, axes):
        '''

            Add axes to the plot and include boxes for the
            quartile ranges in red for the _phantoms, in magenta for
            the _doves, in green for the _worms and in blue for the
            _chameleons.

        :param comment: string: text to be added as comment to the plot's title
        :param yagerStyle: boolean: when False will inverse y-axes of the plot
        :param axes: axes object
        :return:
        '''

        xRange, yRange, xRangeAll, yRangeAll = self.getRanges()

        if yagerStyle:
            # Axes that shows low scores at the top of the plot, low scores at the bottom
            axes.set_ylim(self.aim_maxAll + 0.105 * yRangeAll, self.aim_minAll - 0.1 * yRangeAll)
        else:
            # Axes that shows low scores at the bottom of the plot, high scores at the top.
            axes.set_ylim(self.aim_minAll - 0.1 * yRangeAll, self.aim_maxAll + 0.05 * yRangeAll)

        axes.set_xlim(self.agm_minAll - 0.1 * xRangeAll, self.agm_maxAll + 0.1 * xRangeAll)

        # Do not put title in title field as this will clash with the x-label of the histogram
        # Put it in the zoo plot in a text field
        if len(comment) > 0:
            title = "zoo plot for '%s %s'" % (title, comment)

        else:
            title = "zoo plot for '%s'" % (title)

        if self.config.getRunningOSX() or self.config.getRunningWindows():
            alpha = 0.7
        else:
            alpha = 0.4

        xPos = (self.agm_maxAll + self.agm_minAll) / 2 - 0.05 * xRangeAll
        axes.text(xPos, self.aim_minAll - 0.05 * yRangeAll, title,
                  bbox={'facecolor': 'white', 'alpha': alpha, 'pad': 10})

        axes.set_xlabel('Average Target Match Score')
        axes.set_ylabel('Average Non Target Match Score')

        # Plot boxes for quartile ranges.
        for metaValue in self.data.getMetaDataValues():
            # Phantoms
            self._plotBox(axes, self.agm_mi[metaValue] - 0.1 * xRange[metaValue],
                          self.aim_mi[metaValue] - 0.1 * yRange[metaValue], self.agmsLow[metaValue],
                          self.aimsLow[metaValue], self.colors[metaValue])

            self._plotBox(axes, self.agmsHigh[metaValue], self.aim_mi[metaValue] - 0.1 * yRange[metaValue],
                          self.agm_ma[metaValue] + 0.1 * xRange[metaValue], self.aimsLow[metaValue],
                          self.colors[metaValue])

            # Worms
            self._plotBox(axes, self.agm_mi[metaValue] - 0.1 * xRange[metaValue], self.aimsHigh[metaValue],
                          self.agmsLow[metaValue], self.aim_ma[metaValue] + 0.1 * yRange[metaValue],
                          self.colors[metaValue])

            # Chameleons
            self._plotBox(axes, self.agmsHigh[metaValue], self.aimsHigh[metaValue],
                          self.agm_ma[metaValue] + 0.1 * xRange[metaValue],
                          self.aim_ma[metaValue] + 0.1 * yRange[metaValue], self.colors[metaValue])

        # Plot labels in quartile areas: DOVES PHANTOMS WORMS CHAMELEONS
        animalColors = {}
        if self.config.getAnimalColors():
            animalColors['DOVES'] = 'magenta'
            animalColors['PHANTOMS'] = 'red'
            animalColors['WORMS'] = 'green'
            animalColors['CHAMELEONS'] = 'blue'
        else:
            labelColor = self.config.getLabelColor()
            animalColors['DOVES'] = labelColor
            animalColors['PHANTOMS'] = labelColor
            animalColors['WORMS'] = labelColor
            animalColors['CHAMELEONS'] = labelColor

        # DOVES
        animals = 'DOVES'
        axes.text(self.agm_maxAll, self.aim_minAll - 0.05 * yRangeAll, animals,
                  bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})
        # PHANTOMS
        animals = 'PHANTOMS'
        axes.text(self.agm_minAll - 0.085 * xRangeAll, self.aim_minAll - 0.05 * yRangeAll, animals,
                  bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})
        # WORMS
        animals = 'WORMS'
        if yagerStyle:
            axes.text(self.agm_minAll - 0.085 * xRangeAll, self.aim_maxAll + 0.085 * yRangeAll, animals,
                      bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})
        else:
            axes.text(self.agm_minAll - 0.085 * xRangeAll, self.aim_maxAll - 0.085 * yRangeAll, animals,
                      bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})
        # CHAMELEONS
        animals = 'CHAMELEONS'
        if yagerStyle:
            axes.text(self.agm_maxAll - 0.05 * xRangeAll, self.aim_maxAll + 0.085 * yRangeAll, animals,
                      bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})
        else:
            axes.text(self.agm_maxAll - 0.05 * xRangeAll, self.aim_maxAll - 0.085 * yRangeAll, animals,
                      bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})



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
        plt.plot([x1, x2], [y1, y1], color=col, lw=2)
        # draw line from right top to right bottom
        plt.plot([x2, x2], [y1, y2], color=col, lw=2)
        # draw line from right bottom to left bottom
        plt.plot([x2, x1], [y2, y2], color=col, lw=2)
        # draw line from left bottom to left top
        plt.plot([x1, x1], [y2, y1], color=col, lw=2)

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
            print "_plotDistributions: agmsLow, agmsHigh, aimsLow, aimsHigh:"
            for metaValue in self.data.getMetaDataValues():
                print metaValue, self.agmsLow[metaValue], self.agmsHigh[metaValue], \
                    self.aimsLow[metaValue], self.aimsHigh[metaValue]

        xRange = collections.defaultdict(list)
        yRange = collections.defaultdict(list)
        xFactor = collections.defaultdict(list)
        # xFactor? Yep, even zoo plots need to have a certain X-factor.
        # McElderry for ever !
        yFactor = collections.defaultdict(list)

        labelsDrawn = set()
        scaleFactor = self.config.getScaleFactor()
        for metaValue in self.data.getMetaDataValues():
            xRange[metaValue] = abs(self.agm_ma[metaValue] - self.agm_mi[metaValue])
            yRange[metaValue] = abs(self.aim_ma[metaValue] - self.aim_mi[metaValue])
            xFactor[metaValue] = xRange[metaValue] / scaleFactor
            yFactor[metaValue] = yRange[metaValue] / scaleFactor

        labelsToShow = self.data.getLabelsToShowAlways()
        for thisKey in self.subjects.keys():
            subject = self.subjects[thisKey]
            metaValue = subject.getMetaValue()
            # Show subject label and the # of targets and non targets the ellipse was drawn for.
            thisLabel = subject.getLabel()
            if self.config.getShowNrTargetsAndNonTargets():
                labelText = ("L:%s " % thisLabel) + (" #T:%d" % subject.getNumberOfTargets()) + \
                            (" #nT:%d" % subject.getNumberOfNonTargets())
            else:
                labelText = ("L:%s " % thisLabel)
            if self.config.getShowAverageTargetAndNonTargetMatchScores():
                labelText += (" aTms:%02.2f" % subject.getAgmsv()) + (" anTms:%02.2f" % subject.getAimsv())
            agmStdDev = subject.getAgmStdDev()
            aimStdDev = subject.getAimStdDev()
            width = agmStdDev
            height = aimStdDev
            if self.config.getAlexanderStyle():
                # Only show stdev when ellipses are plotted.
                if self.config.getShowStdev():
                    labelText += (" aTmStDev:%02.2f" % agmStdDev) + (" anTStdDev:%02.2f" % aimStdDev)

            pattern = subject.getPattern()
            xy = [self.agmsv[pattern], self.aimsv[pattern]]

            xRange, yRange, xRangeAll, yRangeAll = self.getRanges()
            if self.config.getAlexanderStyle():
                eWidth = subject.getAgmStdDev() * xFactor[metaValue]
                eHeight =subject.getAimStdDev() * yFactor[metaValue]
            else:
                (hor, vert) = self.config.getScreenResolutionTuple()
                eWidth = xRangeAll / (hor / 10.0)
                eHeight = yRangeAll / (vert / 10.0)
            e = Ellipse(xy, eWidth, eHeight, angle)
            e.set_facecolor(colors[metaValue])
            if self.config.getShowEdgeColor():
                e.set_edgecolor(colors[metaValue])

            # If labels were added to the command line, we can make the corresponding ellipses
            # more prominent by dimming the other ellipses and making the interconnecting
            # lines thinner.

            # The bigger alpha is (0 ... 1.0), the more you see of a data point.
            if subject.getLabel() in labelsToShow:
                # If we are showing data points as ellipses we show them in full glory!
                alpha = 1.0
            else:
                if len(labelsToShow) > 0:
                    # Dim all other data points.
                    alpha = (1 - self.config.getDimmingFactor())
                elif self.config.getAlexanderStyle():
                    if self.config.getUseOpacityForBigEllipses():
                        # Make the data point less visible if it is bigger.
                        # Then smaller data points (partly) lying on top of it will still be visible.
                        # We normalise the opacity using the surface area of the ellipse.
                        thisSurfaceArea = width * height
                        alpha = 1.0 - (thisSurfaceArea - self.minSurfaceArea[metaValue]) / self.surfaceAreaRange[metaValue]
                    else:
                        alpha = self.config.getOpacity4Ellipses()
                else:
                    alpha = 1.0
            # Do not allow values for alpha which are too small.
            if alpha < self.config.getMinimumOpacityValue():
                alpha = self.config.getMinimumOpacityValue()
            e.set_alpha(alpha)
            # Chameleon: BLUE
            if (self.aimsv[pattern] > self.aimsHigh[metaValue]) and (self.agmsv[pattern] > self.agmsHigh[metaValue]):
                if self.annotateEllipses:
                    self._annotateEllipseInQuartile(xy, height, labelText, metaValue, 'rb', axesZoo)
                if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                    e.set_facecolor('blue')
                    if self.config.getShowEdgeColor():
                        e.set_edgecolor('blue')
            # Phantom: RED
            if (self.aimsv[pattern] < self.aimsLow[metaValue]) and (self.agmsv[pattern] < self.agmsLow[metaValue]):
                if self.annotateEllipses:
                    self._annotateEllipseInQuartile(xy, height, labelText, metaValue, 'lt', axesZoo)
                if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                    e.set_facecolor('orange')
                    if self.config.getShowEdgeColor():
                        e.set_edgecolor('orange')
            # Worms: GREEN
            if (self.aimsv[pattern] > self.aimsHigh[metaValue]) and (self.agmsv[pattern] < self.agmsLow[metaValue]):
                if self.annotateEllipses:
                    self._annotateEllipseInQuartile(xy, height, labelText, metaValue, 'lb', axesZoo)
                if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                    e.set_facecolor('green')
                    if self.config.getShowEdgeColor():
                        e.set_edgecolor('green')
            # Doves: MAGENTA
            if (self.aimsv[pattern] < self.aimsLow[metaValue]) and (self.agmsv[pattern] > self.agmsHigh[metaValue]):
                if self.annotateEllipses:
                    self._annotateEllipseInQuartile(xy, height, labelText, metaValue, 'rt', axesZoo)
                if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                    e.set_facecolor('magenta')
                    if self.config.getShowEdgeColor():
                        e.set_edgecolor('magenta')
            # Put the ellipse in the figure.
            point = axesZoo.add_artist(e)

            # If there are several distinct meta data values, they are interconnected.
            # In that case we do not need to annotate both ellipses.
            if self.config.getInterconnectMetaValues():
                if thisLabel in self.data.getLabelsToShowAlways() and thisLabel not in labelsDrawn:
                    labelsDrawn.add(thisLabel)
                    annotation = self._annotateEllipse(xy, xRange[metaValue], yRange[metaValue], labelText, axesZoo)
                    self._pointsWithAnnotation.append([point, annotation, pattern, xy])
                    annotation.set_visible(True)
                else:
                    annotation = self._annotateEllipse(xy, xRange[metaValue], yRange[metaValue], labelText, axesZoo)
                    self._pointsWithAnnotation.append([point, annotation, pattern, xy])
                    annotation.set_visible(False)
            else:
                annotation = self._annotateEllipse(xy, xRange[metaValue], yRange[metaValue], labelText, axesZoo)
                self._pointsWithAnnotation.append([point, annotation, pattern, xy])
                if thisLabel in self.data.getLabelsToShowAlways():
                    annotation.set_visible(True)
            count += 1

            # Plot some ellipses meant for reference but only
            # if we do not show annotations at startup.
        if self.config.getAlexanderStyle():
            if not self.config.getShowAnnotationsAtStartup():
                self._plotReferenceEllipses(axesZoo, xRange[metaValue], yRange[metaValue])

        if self.debug:
            print '_plotDistributions:count:', count
