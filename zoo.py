#!/usr/bin/env python2.7

"""
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
"""

import sys
import os.path
from os import makedirs
from scipy import stats
import numpy
import collections
from math import sqrt, atan2, sin, tan, pi

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


class Zoo(Format, Probability):
    def __init__(self, thisData, thisConfig, thisDebug):
        self.data = thisData
        self.config = thisConfig
        self.debug = thisDebug
        Format.__init__(self, self.debug)
        Probability.__init__(self, self.data, self.config, self.debug)
        self._worms = []
        self._chameleons = []
        self._phantoms = []
        self._doves = []
        self._limited = set()
        self.plotType = 'zoo_plot'
        self.referencesWithAnnotation = []
        self.subject = []
        self._pointsWithAnnotation = []
        self.annotateEllipsesInQuartiles = self.config.getAnnotateEllipsesInQuartiles()
        self.useColorsForQuartileRanges = self.config.getUseColorsForQuartileRanges()
        self.subjects = {}
        # Keep track of the subject labels.
        self.labels = set()
        # Keep track of the number of scores per label

        self.agmStdDevStdDev = collections.defaultdict(list)
        self.aimStdDevStdDev = collections.defaultdict(list)
        self.agmMeanStdDev = collections.defaultdict(list)
        self.aimMeanStdDev = collections.defaultdict(list)

        self.agmMeanNormStdDev = collections.defaultdict(list)
        self.aimMeanNormStdDev = collections.defaultdict(list)

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

        self.aimsv = {}
        self.agmsv = {}
        self.aimsLow = collections.defaultdict(list)
        self.aimsHigh = collections.defaultdict(list)
        self.agmsLow = collections.defaultdict(list)
        self.agmsHigh = collections.defaultdict(list)

        self.xScaleFactor = collections.defaultdict(list)
        self.xScaleFactorAll = 1E099
        # xFactor? Yep, even zoo plots need to have a certain X-factor.
        # McElderry for ever !
        self.yScaleFactor = collections.defaultdict(list)
        self.yScaleFactorAll = 1E099

        # Initialize ranges

        self.yRange = collections.defaultdict(list)
        self.xRange = collections.defaultdict(list)
        self.yRangeAll = 0.0
        self.xRangeAll = 0.0

        metaDataValues = self.data.getMetaDataValues()
        metaColors = self.config.getMetaColors()
        self.colors = assignColors2MetaDataValue(metaDataValues, metaColors)
        self.nrColors = len(self.colors.keys())
        if self.debug:
            print 'colors:', self.colors
            print 'nr colors:', len(self.colors.keys())

        # We need to assess each ellipse's area to choose its opacity.
        self.minSurfaceArea = collections.defaultdict(list)
        self.maxSurfaceArea = collections.defaultdict(list)
        self.surfaceAreaRange = collections.defaultdict(list)

        # Ellipses meant to use as an aid for the user to resize the
        # zoo plot so that it becomes square. In that way the user
        # can more easily interpret the std values.
        self.helperCircles = []

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
            comment += ", nr_of_target_scores, nr_of_non_target_scores"
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
            print 'zoo.writeAnimals2file: path:', path

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

    def _getValuesFromListOfDicts(self, thisDict, metaValue):
        ret = []
        for key in thisDict:
            if metaValue in key:
                ret.append(thisDict[key])
        return ret

    def computeZooStats(self):
        """

        Compute mean target scores and mean non target scores to be used in zoo plot.

        """

        lenAgmsv = {}
        lenAimsv = {}

        for metaValue in self.data.getMetaDataValues():
            for subjectLabelPlusMetaValue in self.data.getTargetScores().keys():
                if metaValue in subjectLabelPlusMetaValue:
                    elements = self.data.getTargetScores()[subjectLabelPlusMetaValue]
                    self.agmsv[subjectLabelPlusMetaValue] = self.data.compAverageScore(elements)
                    lenAgmsv[subjectLabelPlusMetaValue] = len(self.data.getTargetScores()[subjectLabelPlusMetaValue])
            for subjectLabelPlusMetaValue in self.data.getNonTargetScores().keys():
                if metaValue in subjectLabelPlusMetaValue:
                    elements = self.data.getNonTargetScores()[subjectLabelPlusMetaValue]
                    self.aimsv[subjectLabelPlusMetaValue] = self.data.compAverageScore(elements)
                    lenAimsv[subjectLabelPlusMetaValue] = len(self.data.getNonTargetScores()[subjectLabelPlusMetaValue])
        for subjectLabelPlusMetaValue in self.agmsv:
            if subjectLabelPlusMetaValue in self.aimsv:
                # There must be at least one agms and aims value for the data to be used in the zoo plot,
                # otherwise reject the label.
                # Bundle all data for this label for this meta value.
                subject = Subject(subjectLabelPlusMetaValue,
                                  self.agmsv[subjectLabelPlusMetaValue], self.aimsv[subjectLabelPlusMetaValue],
                                  lenAgmsv[subjectLabelPlusMetaValue], lenAimsv[subjectLabelPlusMetaValue], self.debug)
                self.subjects[subjectLabelPlusMetaValue] = subject

        if len(self.subjects) == 0:
            print "Error: Unable to compute zoo statistics."
            print "No labels were found for which there are target AND non target scores."
            sys.exit(1)

        if self.debug:
            print 'computeZooStats:len(agmsv):', len(self.agmsv)
            print 'computeZooStats:len(aimsv):', len(self.aimsv)

        for metaValue in self.data.getMetaDataValues():
            aimsValues = self._getValuesFromListOfDicts(self.aimsv, metaValue)
            if not len(aimsValues) > 1:
                print "Not enough data to draw a zoo plot for %s." % metaValue
                break
            # Compute quartile ranges.
            self.aimsLow[metaValue] = stats.scoreatpercentile(aimsValues, 25)
            self.aimsHigh[metaValue] = stats.scoreatpercentile(aimsValues, 75)
            agmsValues = self._getValuesFromListOfDicts(self.agmsv, metaValue)
            if not len(agmsValues) > 1:
                print "Not enough data to draw a zoo plot for %s." % metaValue
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

            if self.config.getShowEqualAxes():
                # Force all plot so be square.
                mi = min(self.aim_mi[metaValue], self.agm_mi[metaValue])
                self.aim_mi[metaValue] = self.agm_mi[metaValue] = mi
                ma = max(self.aim_ma[metaValue], self.agm_ma[metaValue])
                self.aim_ma[metaValue] = self.agm_ma[metaValue] = ma

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
        if self.debug:
            print "computeZooStats: agm_minAll, agm_maxAll: %f %f" % (self.agm_minAll, self.agm_maxAll)
            print "computeZooStats: aim_minAll, aim_maxAll: %f %f" % (self.aim_minAll, self.aim_maxAll)

    def _sign(self, value):
        return cmp(value, 0)

    def computeZooStatsAlexanderStyle(self):
        """
            Compute statistics to plot ellipses in zoo plot as published by Alexander et al. IAFPA Zurich, 2014
        """
        self.computeZooStats()

        # Now we need the std for width and height
        # of the ellipses we want to draw in the plot.

        # To compute averages and std dev of std dev we need to collect all stdDevs.
        allTargetStdDevs = collections.defaultdict(list)
        allNonTargetStdDevs = collections.defaultdict(list)

        # Get all labels.
        self.labels = self.data.getTargetLabels()

        for metaValue in self.data.getMetaDataValues():
            self.agmStdDevMin[metaValue] = self.config.getMaxStdDev()
            self.aimStdDevMin[metaValue] = self.config.getMaxStdDev()
            self.agmStdDevMax[metaValue] = self.config.getMinStdDev()
            self.aimStdDevMax[metaValue] = self.config.getMinStdDev()

        for thisKey in self.subjects.keys():
            subject = self.subjects[thisKey]
            metaValue = subject.getMetaValue()
            # Target std dev for this subject.
            targetScores4ThisSubject = self.data.getTargetScores()[thisKey]
            if len(targetScores4ThisSubject) > 1:
                stdDev = numpy.std(targetScores4ThisSubject)
                self.agmStdDevMin[metaValue] = min(self.agmStdDevMin[metaValue], stdDev)
                self.agmStdDevMax[metaValue] = max(self.agmStdDevMax[metaValue], stdDev)
                subject.setAgmStdDev(stdDev)
            else:
                subject.setSingleTargetScore(True)
                # Value for stdDev will be set later.
                if self.debug:
                    print subject.getPattern(), ': singleTargetScore'

            # Non target std dev for this subject.
            nonTargetScores4ThisSubject = self.data.getNonTargetScores()[thisKey]

            if len(nonTargetScores4ThisSubject) > 1:
                stdDev = numpy.std(nonTargetScores4ThisSubject)
                self.aimStdDevMin[metaValue] = min(self.aimStdDevMin[metaValue], stdDev)
                self.aimStdDevMax[metaValue] = max(self.aimStdDevMax[metaValue], stdDev)
                subject.setAimStdDev(stdDev)
            else:
                subject.setSingleNonTargetScore(True)
                if self.debug:
                    print subject.getPattern(), ': singleNonTargetScore'
                # value for stdDev will be set later.

        # Select subjects that we could calculate a std dev for, so that we can normalise
        # these. The remaining subjects will be dealt with later.

        for thisKey in self.subjects.keys():
            subject = self.subjects[thisKey]
            metaValue = subject.getMetaValue()
            if not subject.getSingleTargetScore():
                # Only gather data for subjects with more than one target score.
                allTargetStdDevs[metaValue].append(subject.getAgmStdDev())
            if not subject.getSingleNonTargetScore():
                # Only gather data for subjects with more than one non target score.
                allNonTargetStdDevs[metaValue].append(subject.getAimStdDev())

        for metaValue in self.data.getMetaDataValues():
            if len(allTargetStdDevs[metaValue]) > 0:
                self.agmStdDevStdDev[metaValue] = numpy.std(allTargetStdDevs[metaValue])
                self.agmMeanStdDev[metaValue] = numpy.average(allTargetStdDevs[metaValue])
            else:
                print "Not enough target scores to normalize std devs for metavalue %s!" % metaValue
                # Implementation note: we could continue here after removing the metaValue from self.data._metaDataValues
                sys.exit(1)

            if len(allNonTargetStdDevs[metaValue]) > 0:
                self.aimStdDevStdDev[metaValue] = numpy.std(allNonTargetStdDevs[metaValue])
                self.aimMeanStdDev[metaValue] = numpy.average(allNonTargetStdDevs[metaValue])
            else:
                print "Not enough non target scores to normalize std devs for metavalue %s!" % metaValue
                # Implementation note: we could continue here after removing the metaValue from self.data._metaDataValues
                sys.exit(1)

            # Central point of the plot is determined by the mean of agms and aims per meta data value.
            # This point is plotted as a black dot and is meant as a reference.
            theseAgmsValues = self.data.getTargetScores4MetaValue(metaValue)
            theseAimValues = self.data.getNonTargetScores4MetaValue(metaValue)
            self.meanAgms[metaValue] = self.data.compAverageScore(theseAgmsValues)
            self.meanAims[metaValue] = self.data.compAverageScore(theseAimValues)
            if self.debug:
                print "central point for %s will be at: %f %f" % (
                    metaValue, self.meanAgms[metaValue], self.meanAims[metaValue])

        # Normalize stdev of all subjects.
        # Note this makes stdev values to be centered around zero.

        for thisKey in self.subjects.keys():
            subject = self.subjects[thisKey]
            metaValue = subject.getMetaValue()

            if subject.getSingleTargetScore():
                # If there are subjects with only one target or non target score, we
                # can not compute the StdDev of the StdDev
                # We can assume the subject to be similar to other subjects and assume the unit value
                # or we go for the non info option and set the std dev to the minimum accepted.
                if self.config.getShowSingleValueAsUnitValue():
                    agmNormStdDev = self.agmMeanStdDev[metaValue] / self.agmStdDevStdDev[metaValue]
                else:
                    agmNormStdDev = self.config.getMinStdDev()
            else:
                # Normalize std dev.: (x - mu) / std
                agmNormStdDev = (subject.getAgmStdDev() - self.agmMeanStdDev[metaValue]) / self.agmStdDevStdDev[metaValue]
            subject.setAgmNormStdDev(agmNormStdDev)

            if subject.getSingleNonTargetScore():
                # We can assume the subject to be similar to other subjects and assume the unit value
                # or we go for the non info option and set the std dev to the minimum accepted.
                if self.config.getShowSingleValueAsUnitValue():
                    aimNormStdDev = self.aimMeanStdDev[metaValue] / self.aimStdDevStdDev[metaValue]
                else:
                    aimNormStdDev = self.config.getMinStdDev()
            else:
                # Normalize std dev.: (x - mu) / std
                aimNormStdDev = (subject.getAimStdDev() - self.aimMeanStdDev[metaValue]) / self.aimStdDevStdDev[metaValue]
            subject.setAimNormStdDev(aimNormStdDev)

        maxStdDev = self.config.getMaxStdDev()
        # If the user wants to, the stdev values can be limited to a certain maximum value.
        if self.config.getLimitStdDevs():
            for thisKey in self.subjects.keys():
                subject = self.subjects[thisKey]
                if not subject.getSingleTargetScore():
                    agmNormStdDev = subject.getAgmNormStdDev()
                    if abs(agmNormStdDev) > maxStdDev:
                        agmNormStdDev = self._sign(agmNormStdDev) * maxStdDev
                        subject.setAgmNormStdDev(agmNormStdDev)
                        subject.setWasLimited(True)
                        # Add subject to exclusive set.
                        self._addLimited(subject)
                if not subject.getSingleNonTargetScore():
                    aimNormStdDev = subject.getAimNormStdDev()
                    if abs(aimNormStdDev) > maxStdDev:
                        aimNormStdDev = self._sign(aimNormStdDev) * maxStdDev
                        subject.setAimNormStdDev(aimNormStdDev)
                        subject.setWasLimited(True)
                        # Add subject to exclusive set.
                        self._addLimited(subject)

        # After normalisation we need to recompute aim_mi and aim_ma + agm_mi and agm_ma.
        for metaValue in self.data.getMetaDataValues():
            self.minSurfaceArea[metaValue] = 1.0E99
            self.maxSurfaceArea[metaValue] = 0.0
            self.aim_mi[metaValue] = self.agm_mi[metaValue] = self.data.getMaximum4ThisType()
            self.aim_ma[metaValue] = self.agm_ma[metaValue] = self.data.getMinimum4ThisType()

        for thisKey in self.subjects.keys():
            subject = self.subjects[thisKey]

            metaValue = subject.getMetaValue()
            self.minSurfaceArea[metaValue] = min(self.minSurfaceArea[metaValue],
                                                 subject.getAgmStdDev() * subject.getAimStdDev())
            self.maxSurfaceArea[metaValue] = max(self.maxSurfaceArea[metaValue],
                                                 subject.getAgmStdDev() * subject.getAimStdDev())

        # Compute mean of normalized std devs.
        for metaValue in self.data.getMetaDataValues():
            self.agmMeanNormStdDev[metaValue] = 0.0
            self.aimMeanNormStdDev[metaValue] = 0.0
        for thisKey in self.subjects.keys():
            subject = self.subjects[thisKey]
            metaValue = subject.getMetaValue()
            self.agmMeanNormStdDev[metaValue] += subject.getAgmNormStdDev()
            self.aimMeanNormStdDev[metaValue] += subject.getAimNormStdDev()
        for metaValue in self.data.getMetaDataValues():
            self.agmMeanNormStdDev[metaValue] /= len(self.subjects)
            self.aimMeanNormStdDev[metaValue] /= len(self.subjects)

        # Surface area of ellipse is used to normalise opacity against size in order to
        # make small ellipses visible even if they are overlapped by larger ones.
        for metaValue in self.data.getMetaDataValues():
            self.surfaceAreaRange[metaValue] = (self.maxSurfaceArea[metaValue] - self.minSurfaceArea[metaValue])
            self.agm_mi[metaValue], self.agm_ma[metaValue] = \
                self.data.minMax2(self.agmsv, metaValue, self.agm_mi[metaValue], self.agm_ma[metaValue])
            self.aim_mi[metaValue], self.aim_ma[metaValue] = \
                self.data.minMax2(self.aimsv, metaValue, self.aim_mi[metaValue], self.aim_ma[metaValue])

        # We need to know what the ranges are to be able to plot the ellipses, labels etc.
        for metaValue in self.data.getMetaDataValues():
            self.xRange[metaValue] = 1E-99
            self.yRange[metaValue] = 1E-99

        for metaValue in self.data.getMetaDataValues():
            self.xRange[metaValue] = max(self.xRange[metaValue], abs(self.agm_ma[metaValue] - self.agm_mi[metaValue]))
            self.yRange[metaValue] = max(self.yRange[metaValue], abs(self.aim_ma[metaValue] - self.aim_mi[metaValue]))
            self.xRangeAll = max(self.xRangeAll, self.xRange[metaValue])
            self.yRangeAll = max(self.yRangeAll, self.yRange[metaValue])

        for metaValue in self.data.getMetaDataValues():
            # Implementation note: We would like maybe 100 ellipses to fit next to each other?
            self.xScaleFactor[metaValue] = self.xRange[metaValue] / self.config.getScaleFactor()
            self.yScaleFactor[metaValue] = self.yRange[metaValue] / self.config.getScaleFactor()
        self.xScaleFactorAll = self.xRangeAll / self.config.getScaleFactor()
        self.yScaleFactorAll = self.yRangeAll / self.config.getScaleFactor()

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
        dX = x2 - x1
        dY = y2 - y1

        # If label is within 0.1 of unit std to position
        # then return True, else False.
        if abs(dX) < abs(thresholdX) and abs(dY) < abs(thresholdY):
            return True
        else:
            return False

    def findDataPointsNear(self, x1, y1):
        """
        Find data point(s) close to the position of the mouse click.

        :param x1: float: mouse x data position
        :param y1: float: mouse y data position
        :return: list: list of labels within 0.1 unit std of position clicked.
        """
        if self.debug:
            print "aimStdDevStdDev:", self.aimStdDevStdDev
            print "agmStdDevStdDev:", self.agmStdDevStdDev
            print "aimMeanStdDev:", self.aimMeanStdDev
            print "agmMeanStdDev:", self.agmMeanStdDev
        ret = []
        for thisKey in self.subjects.keys():
            subject = self.subjects[thisKey]
            metaValue = subject.getMetaValue()
            pattern = subject.getPattern()
            x2 = subject.getAgmsv()
            y2 = subject.getAimsv()
            thresholdX = 0.2 * self.agmStdDevStdDev[metaValue]
            thresholdY = 0.2 * self.aimStdDevStdDev[metaValue]
            if self.isNear(x1, y1, (x2, y2), thresholdX, thresholdY):
                ret.append((pattern, x2, y2))

        # Make all visible ellipses meant to help the user make a
        # square plot invisible again.
        for el in self.helperCircles:
            el.set_visible(False)
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

    def _plotReferenceEllipses(self, axes):
        """
        Plot reference ellipse with size corresponding to -2, 0 and 2 x std (i.e. mean).
        :param axes: axes object of the plot
        :return: Not a thing
        """
        angle = 0.0
        alpha = self.config.getAlpha4ReferenceCircles()
        alphaDecrement = (alpha - 0.1) / 3.0
        # It should be possible to show 20 meta value reference ellipses next to eachother.
        offset = baseOffset = self.xRangeAll / 20.0
        stdDevOffset = self.config.getMaxStdDev() * 0.5
        if self.config.getShowReference():
            for metaValue in self.data.getMetaDataValues():
                onlyOnce = True
                # Show ellipse for mu - 2 stdev, mu, mu + 2 stdev
                # In order to draw ellipses that represent a negative stdev, we
                # add maxStdDev as an offset. So mu -2s can be plotted and is
                # thinner/taller than mu or mu + 2 stdev ellipses.
                x = self.agm_minAll + offset
                y = self.aim_maxAll
                for factor in [-2, 0, 2]:
                    #thisWidth = (stdDevOffset + refEllipseStdDev * self.agmStdDevStdDev[metaValue]) * self.xScaleFactorAll
                    #thisHeight = (stdDevOffset + refEllipseStdDev * self.aimStdDevStdDev[metaValue]) * self.yScaleFactorAll
                    thisWidth = (stdDevOffset + factor * self.agmMeanNormStdDev[metaValue]) * self.xScaleFactorAll
                    thisHeight = (stdDevOffset + factor * self.aimMeanNormStdDev[metaValue]) * self.yScaleFactorAll
                    e = Ellipse((x, y), thisWidth, thisHeight, angle)
                    e.set_facecolor(self.colors[metaValue])
                    e.set_alpha(alpha)
                    axes.add_artist(e)
                    # Make next ellipse less opaque.
                    alpha -= alphaDecrement
                    if alpha < 0.1:
                        alpha = 0.1
                # Create some distance between different metavalue unit circles.
                offset += baseOffset

                experimentText = "points for experiment: %s.\n" % str(metaValue)

                if onlyOnce:
                    onlyOnce = False
                    if len(self.colors) > 1:
                        text = "These 3 ellipses are meant as scaled reference\n" + \
                               experimentText + \
                               "From the inner to the outer ellipse\n" + \
                               "they are sized $\\mu$-$2\\sigma$, $\\mu$ and $\\mu$+$2\\sigma$."
                    else:
                        text = "These 3 ellipses are meant as scaled reference\npoints for this experiment.\n" + \
                               "From the inner to the outer ellipse\n" + \
                               "they are sized $\\mu$-$2\\sigma$, $\\mu$ and $\\mu$+$2\\sigma$."
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

    def _plotUnitEllipses(self, axes):
        alpha = self.config.getAlpha4UnitCircles()
        angle = 0.0
        # The width/height where the normalized data is 0 standard deviations lies at w = maxStdDev
        stdDevOffset = self.config.getMaxStdDev() * 0.5
        for metaValue in self.data.getMetaDataValues():
            xOffset = abs(self.agm_ma[metaValue] - self.agm_mi[metaValue]) / 15.0
            yOffset = abs(self.aim_ma[metaValue] - self.aim_mi[metaValue]) / 7.0

            thisWidth = (stdDevOffset + self.agmMeanNormStdDev[metaValue]) * self.xScaleFactorAll
            thisHeight = (stdDevOffset + self.aimMeanNormStdDev[metaValue]) * self.yScaleFactorAll
            (x, y) = (self.meanAgms[metaValue], self.meanAims[metaValue])
            e = Ellipse((x, y), thisWidth, thisHeight, angle)
            e.set_facecolor('black')
            e.set_alpha(alpha)
            axes.add_artist(e)
            if len(self.colors) > 1:
                text = "This dark ellipse is meant as a reference point\nfor data set: '%s'.\nIts width and height are " \
                       "the mean value of the normalized stdevs,\nso it represents a data point for which $\\mu$ = 0.\n" \
                       "It is shown here at the center of all data points\nfor data set '%s'.\n" \
                       "Note, if you resize the plot so that this ellipse becomes a perfect circle,\n" \
                       "it will make the interpretation of the plot independent of the screen geometry." % (
                           metaValue, metaValue)
            else:
                text = "This dark ellipse is meant as a reference point for this data set.\nIts width and height are " \
                       "the mean value of the normalized stdevs,\nso it represents a data point for which $\\mu$ = 0.\n" \
                       "It is shown here at the center of all data points.\n" \
                       "Note, if you resize the plot so that this ellipse becomes a perfect circle,\n" \
                       "it will make the interpretation of the plot independent of the screen geometry."
            xText = x + xOffset
            yText = y + yOffset
            annotation = self._annotateEllipse4References(axes, (x, y), xText, yText, text)
            self.referencesWithAnnotation.append((annotation, (x, y)))
            if self.config.getShowTextAtReferenceAtStartup():
                annotation.set_visible(True)
            else:
                annotation.set_visible(False)

    def _plotHelperCircles(self, axes):
        angle = 0.0
        # The width/height where the normalized data is 0 standard deviations lies at w = maxStdDev / 2
        stdDevOffset = self.config.getMaxStdDev() * 0.5
        for metaValue in self.data.getMetaDataValues():
            # thisWidth = (stdDevOffset + self.agmMeanStdDev[metaValue] / self.agmStdDevStdDev[
            #     metaValue]) * self.xScaleFactorAll
            # thisHeight = (stdDevOffset + self.aimMeanStdDev[metaValue] / self.aimStdDevStdDev[
            #     metaValue]) * self.yScaleFactorAll
            thisWidth = (stdDevOffset + self.agmMeanStdDev[metaValue]) * self.xScaleFactorAll
            thisHeight = (stdDevOffset + self.aimMeanStdDev[metaValue]) * self.yScaleFactorAll
            (x, y) = (self.meanAgms[metaValue], self.meanAims[metaValue])
            radius = max(thisWidth, thisHeight) * 2.0
            i = 1
            while x + i * radius < self.agm_maxAll * 2.0:
                # if self.debug:
                #     print "_plotHelperCircles", x + i * radius, self.agm_maxAll
                # for i in [4, 8, 12, 16, 20]:
                e = Ellipse((x, y), i * radius, i * radius, angle)
                # No need to fill the ellipse.
                e.set_facecolor('none')
                # Let's make them black.
                e.set_edgecolor('k')
                # Make it less conspicuous.
                e.set_alpha(0.5)
                # Choose from solid, dashed, dashdot or dotted.
                e.set_linestyle('dashed')
                self.helperCircles.append(e)
                axes.add_artist(e)
                i += 1

    def _annotateEllipseInQuartile(self, xy, xRange, hx, hy, text, axes=plt):
        (x, y) = xy
        factor = tan(pi / 3.0)
        if x < hx:
            xOffset = xRange / 20
        else:
            xOffset = -xRange / 10
        if y > hy:
            yOffset = -xRange / 150 * factor
        else:
            yOffset = xRange / 150 * factor
        xText = x + xOffset
        yText = y + yOffset

        if self.config.getRunningOSX():
            axes.annotate("%s" % text,
                          xy,
                          bbox=dict(boxstyle="square", fc="0.8"),
                          xytext=(xText, yText),
                          xycoords='data',
                          textcoords='data',
                          arrowprops=dict(arrowstyle='->'))
        else:
            axes.annotate("%s" % text,
                          xy,
                          bbox=dict(boxstyle="square", fc="0.8"),
                          backgroundcolor='yellow',
                          xytext=(xText, yText),
                          xycoords='data',
                          textcoords='data',
                          arrowprops=dict(arrowstyle='->'))

    def _annotateEllipse4References(self, axesZoo, xy, xText, yText, text):
        ha = 'left'
        va = 'bottom'
        if self.config.getRunningOSX():
            annotation = axesZoo.annotate("%s" % text,
                                          xy,
                                          bbox=dict(boxstyle="square", fc="0.8"),
                                          xytext=(xText, yText),
                                          xycoords='data',
                                          textcoords='data',
                                          arrowprops=dict(arrowstyle='->'),
                                          horizontalalignment=ha,
                                          verticalalignment=va, )
        else:
            annotation = axesZoo.annotate("%s" % text,
                                          xy,
                                          bbox=dict(boxstyle="square", fc="0.8"),
                                          backgroundcolor='yellow',
                                          xytext=(xText, yText),
                                          xycoords='data',
                                          textcoords='data',
                                          arrowprops=dict(arrowstyle='->'),
                                          horizontalalignment=ha,
                                          verticalalignment=va, )

        # By default the annotation is not visible.
        annotation.set_visible(False)
        return annotation

    def _annotateEllipse(self, xy, xRange, hx, hy, text, axes=plt):
        (x, y) = xy
        factor = tan(pi / 3.0)
        if x < hx:
            xOffset = xRange / 20
        else:
            xOffset = -xRange / 10
        if y > hy:
            yOffset = -xRange / 50 * factor
        else:
            yOffset = xRange / 50 * factor
        xText = x + xOffset
        yText = y + yOffset
        angle = 0
        # angle = 45.0 / xRange * (x - xRange) + 45.0
        if self.config.getRunningOSX():
            annotation = axes.annotate("%s" % text,
                                       xy,
                                       bbox=dict(boxstyle="square", fc="0.8"),
                                       xytext=(xText, yText),
                                       xycoords='data',
                                       textcoords='data',
                                       rotation=angle,
                                       arrowprops=dict(arrowstyle='->'))
        else:
            annotation = axes.annotate("%s" % text,
                                       xy,
                                       bbox=dict(boxstyle="square", fc="0.8"),
                                       backgroundcolor='yellow',
                                       xytext=(xText, yText),
                                       xycoords='data',
                                       textcoords='data',
                                       rotation=angle,
                                       arrowprops=dict(arrowstyle='->'))

        # By default the annotation is not visible.
        if self.config.getShowAnnotationsAtStartup():
            annotation.set_visible(True)
        else:
            annotation.set_visible(False)
        return annotation

    def drawLegend(self, colors):
        """
        Draw a color legend for the metadata on the upper right
        side of the plot, if the metadata can be grouped in more
        than one group. Only show the meta value if there are more
        than one.
        """

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
        # Add meta condition value name to legend text if there are more than one meta values.
        if len(colors) > 1:
            for thisMetaValue in sorted(colors.keys()):
                legendText[thisMetaValue].append(thisMetaValue)

        # Compute and show the EER value if so desired.
        if self.config.getShowEerInZoo():
            eerObject = Eer(self.data, self.config, self.debug)
            eerData = eerObject.computeProbabilities(self.eerFunc)
            for thisMetaValue in sorted(colors.keys()):
                for metaValue, PD, PP, X in eerData:
                    if thisMetaValue == metaValue:
                        try:
                            eerValue, score = eerObject.computeEer(PD, PP, X)
                        except Exception, e:
                            print "DrawLegend: problem computing EER for %s: %s" % (thisMetaValue, e)
                        else:
                            eerValue *= 100
                            if eerValue < 10.0:
                                eerStr = "Eer:  %.2f%s" % (eerValue, '%')
                            else:
                                eerStr = "Eer: %2.2f%s" % (eerValue, '%')
                            legendText[thisMetaValue].append(eerStr)
                        break

        # Compute and show the Cllr value if so desired.
        if self.config.getShowCllrInZoo():
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

        # Compute and show the CllrMin value if so desired.
        if self.config.getShowMinCllrInZoo():
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

        divFactor = 25.0
        # Increase factor to move legend to the right.
        # Decrease factor to move legend to the left.
        xWidth = float((self.agm_maxAll - self.agm_minAll) / divFactor)

        yBase = self.aim_minAll
        xBase = self.agm_maxAll
        # Find local minimum of agm_ma values and put legend next to it.
        for metaValue in sorted(colors.keys()):
            xBase = min(xBase, self.agm_ma[metaValue])
        xBase -= xWidth
        # We do want to stay within the limits of the plot.
        offset = factor * xWidth * ((pixelWidth * maxTextLength) / xWidthInPixels)
        if xBase - offset < self.agm_minAll:
            xBase = self.agm_minAll + offset
        for metaValue in sorted(colors.keys()):
            thisLegendText = ''
            # Compile legend text.
            for el in legendText[metaValue]:
                thisLegendText += el + ', '
            # Remove last comma and space.
            thisLegendText = thisLegendText[:-2]
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

    def _plotAxes(self, comment, yagerStyle, title, axes):
        """

            Add axes to the plot and include boxes for the
            quartile ranges in red for the phantoms, in magenta for
            the doves, in green for the worms and in blue for the
            chameleons.

        :param comment: string: text to be added as comment to the plot's title
        :param yagerStyle: boolean: when False will inverse y-axes of the plot
        :param axes: axes object
        :return:
        """

        if yagerStyle:
            # Axes that shows low scores at the top of the plot, high scores at the bottom.
            axes.set_ylim(self.aim_maxAll + 0.105 * self.yRangeAll, self.aim_minAll - 0.1 * self.yRangeAll)
        else:
            # Axes that shows high scores at the top of the plot, low scores at the bottom.
            axes.set_ylim(self.aim_minAll - 0.1 * self.yRangeAll, self.aim_maxAll + 0.05 * self.yRangeAll)

        axes.set_xlim(self.agm_minAll - 0.1 * self.xRangeAll, self.agm_maxAll + 0.1 * self.xRangeAll)

        # Do not put title in title field as this will clash with the x-label of the histogram.
        # Put it in the zoo plot in a text field.
        if len(comment) > 0:
            title = "zoo plot for '%s %s'" % (title, comment)

        else:
            title = "zoo plot for '%s'" % title

        if self.config.getRunningOSX() or self.config.getRunningWindows():
            alpha = 0.7
        else:
            alpha = 0.4

        xPos = (self.agm_maxAll + self.agm_minAll) / 2 - 0.05 * self.xRangeAll
        axes.text(xPos, self.aim_minAll - 0.05 * self.yRangeAll, title,
                  bbox={'facecolor': 'white', 'alpha': alpha, 'pad': 10})

        axes.set_xlabel('Average Target (Genuine) Match Score')
        axes.set_ylabel('Average Non Target (Imposter) Match Score')

        # Plot boxes for quartile ranges.
        for metaValue in self.data.getMetaDataValues():
            # Phantoms
            self._plotBox(axes, self.agm_mi[metaValue] - 0.1 * self.xRange[metaValue],
                          self.aim_mi[metaValue] - 0.1 * self.yRange[metaValue], self.agmsLow[metaValue],
                          self.aimsLow[metaValue], self.colors[metaValue])
            # Doves
            self._plotBox(axes, self.agmsHigh[metaValue], self.aim_mi[metaValue] - 0.1 * self.yRange[metaValue],
                          self.agm_ma[metaValue] + 0.1 * self.xRange[metaValue], self.aimsLow[metaValue],
                          self.colors[metaValue])

            # Worms
            self._plotBox(axes, self.agm_mi[metaValue] - 0.1 * self.xRange[metaValue], self.aimsHigh[metaValue],
                          self.agmsLow[metaValue], self.aim_ma[metaValue] + 0.1 * self.yRange[metaValue],
                          self.colors[metaValue])

            # Chameleons
            self._plotBox(axes, self.agmsHigh[metaValue], self.aimsHigh[metaValue],
                          self.agm_ma[metaValue] + 0.1 * self.xRange[metaValue],
                          self.aim_ma[metaValue] + 0.1 * self.yRange[metaValue], self.colors[metaValue])

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
        axes.text(self.agm_maxAll, self.aim_minAll - 0.05 * self.yRangeAll, animals,
                  bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})
        # PHANTOMS
        animals = 'PHANTOMS'
        axes.text(self.agm_minAll - 0.085 * self.xRangeAll, self.aim_minAll - 0.05 * self.yRangeAll, animals,
                  bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})
        # WORMS
        animals = 'WORMS'
        if yagerStyle:
            axes.text(self.agm_minAll - 0.085 * self.xRangeAll, self.aim_maxAll + 0.085 * self.yRangeAll, animals,
                      bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})
        else:
            axes.text(self.agm_minAll - 0.085 * self.xRangeAll, self.aim_maxAll - 0.085 * self.yRangeAll, animals,
                      bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})
        # CHAMELEONS
        animals = 'CHAMELEONS'
        if yagerStyle:
            axes.text(self.agm_maxAll - 0.05 * self.xRangeAll, self.aim_maxAll + 0.085 * self.yRangeAll, animals,
                      bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})
        else:
            axes.text(self.agm_maxAll - 0.05 * self.xRangeAll, self.aim_maxAll - 0.085 * self.yRangeAll, animals,
                      bbox={'facecolor': animalColors[animals], 'alpha': alpha, 'pad': 10})

        # Last but not least, plot the graph.
        axes.grid()

    def _plotBox(self, thisPlt, x1, y1, x2, y2, col):
        """
        plot a box with a colored border (e.g. used to delimit quartile ranges in zoo plot)

        :param thisPlt: plot object
        :param x1: int: x-coordinate of lower left corner of box
        :param y1: int: y-coordinate of lower left corner of box
        :param x2: int: x-coordinate of upper right corner of box
        :param y2: int: y-coordinate of upper right corner of box
        :param col: string: color of box border
        :return: Not a thing

        """
        # draw line from left top to right top
        thisPlt.plot([x1, x2], [y1, y1], color=col, lw=2)
        # draw line from right top to right bottom
        thisPlt.plot([x2, x2], [y1, y2], color=col, lw=2)
        # draw line from right bottom to left bottom
        thisPlt.plot([x2, x1], [y2, y2], color=col, lw=2)
        # draw line from left bottom to left top
        thisPlt.plot([x1, x1], [y2, y1], color=col, lw=2)

    def _plotDistributions(self, colors, axesZoo):
        """
        Plot the average target scores against the average non target
        scores using ellipses to show a measure of each subject's
        target and non target score distribution.

        :param colors: dictionary with tuple with rgb values for each metavalue.
        :param axesZoo: axes object to plot data on
        :return:
        """
        angle = 0.0
        count = 0
        if self.debug:
            print "_plotDistributions: agmsLow, agmsHigh, aimsLow, aimsHigh:"
            for metaValue in self.data.getMetaDataValues():
                print metaValue, self.agmsLow[metaValue], self.agmsHigh[metaValue], \
                    self.aimsLow[metaValue], self.aimsHigh[metaValue]

        labelsDrawn = set()
        labelsToShow = self.data.getLabelsToShowAlways()
        for thisKey in self.subjects.keys():
            subject = self.subjects[thisKey]
            metaValue = subject.getMetaValue()
            # Show subject label and the # of targets and non targets the ellipse was drawn for.
            thisLabel = subject.getLabel()
            labelText = ("L: %s" % thisLabel)
            if self.config.getShowNrTargetsAndNonTargets():
                labelText += ("\n#T: %d" % subject.getNumberOfTargets()) + \
                            ("\n#nT: %d" % subject.getNumberOfNonTargets())
            if self.config.getShowAverageScores():
                labelText += ("\naTms: %02.2f" % subject.getAgmsv()) + ("\nanTms: %02.2f" % subject.getAimsv())
            agmNormStdDev = subject.getAgmNormStdDev()
            aimNormStdDev = subject.getAimNormStdDev()
            # width = agmNormStdDev
            # height = aimNormStdDev
            if self.config.getAlexanderStyle():
                # Only show norm stdev when ellipses are plotted.
                if self.config.getShowStdev():
                    labelText += ("\naTmNormStDev: %02.2f" % agmNormStdDev) + ("\nanTmNormStdDev: %02.2f" % aimNormStdDev)

            pattern = subject.getPattern()
            x = subject.getAgmsv()
            y = subject.getAimsv()
            xy = (x, y)
            stdDevOffset = self.config.getMaxStdDev() * 0.5
            if self.config.getAlexanderStyle():
                eWidth = (stdDevOffset + subject.getAgmNormStdDev()) * self.xScaleFactorAll
                eHeight = (stdDevOffset + subject.getAimNormStdDev()) * self.yScaleFactorAll
            else:
                (hor, vert) = self.config.getScreenResolutionTuple()
                # The width and hight should be chosen so that the data point is shown as a simple dot.
                eWidth = self.xRangeAll / (hor / 10.0)
                eHeight = self.yRangeAll / (vert / 10.0)
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
                        thisSurfaceArea = eWidth * eHeight
                        alpha = 1.0 - (thisSurfaceArea - self.minSurfaceArea[metaValue]) / \
                                      self.surfaceAreaRange[metaValue]
                    else:
                        alpha = self.config.getOpacity4Ellipses()
                else:
                    alpha = 1.0
            # Do not allow values for alpha which are too small.
            if alpha < self.config.getMinimumOpacityValue():
                alpha = self.config.getMinimumOpacityValue()
            e.set_alpha(alpha)
            # Chameleon: BLUE, right bottom quartile
            hy = self.aim_maxAll - (self.aim_maxAll - self.aim_minAll) / 2.0
            hx = self.agm_maxAll - (self.agm_maxAll - self.agm_minAll) / 2.0
            if (y > self.aimsHigh[metaValue]) and (x > self.agmsHigh[metaValue]):
                if self.annotateEllipsesInQuartiles:
                    # Set text above data point to the left.
                    annotation = self._annotateEllipse(xy, self.xRange[metaValue], hx, hy, labelText, axesZoo)
                    annotation.set_visible(True)
                if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                    e.set_facecolor('blue')
                    if self.config.getShowEdgeColor():
                        e.set_edgecolor('blue')
            # Phantom: RED, left top quartile.
            if (y < self.aimsLow[metaValue]) and (x < self.agmsLow[metaValue]):
                if self.annotateEllipsesInQuartiles:
                    # Set text below data point to the right.
                    annotation = self._annotateEllipse(xy, self.xRange[metaValue], hx, hy, labelText, axesZoo)
                    annotation.set_visible(True)
                if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                    e.set_facecolor('orange')
                    if self.config.getShowEdgeColor():
                        e.set_edgecolor('orange')
            # Worms: GREEN, left bottom
            if (y > self.aimsHigh[metaValue]) and (x < self.agmsLow[metaValue]):
                if self.annotateEllipsesInQuartiles:
                    # Set text above data point to the right.
                    annotation = self._annotateEllipse(xy, self.xRange[metaValue], hx, hy, labelText, axesZoo)
                    annotation.set_visible(True)
                if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                    e.set_facecolor('green')
                    if self.config.getShowEdgeColor():
                        e.set_edgecolor('green')
            # Doves: MAGENTA, right top
            if (y < self.aimsLow[metaValue]) and (x > self.agmsHigh[metaValue]):
                if self.annotateEllipsesInQuartiles:
                    # Set text below data point to the left.
                    annotation = self._annotateEllipse(xy, self.xRange[metaValue], hx, hy, labelText, axesZoo)
                    annotation.set_visible(True)
                if self.useColorsForQuartileRanges and (self.nrColors <= 1):
                    e.set_facecolor('magenta')
                    if self.config.getShowEdgeColor():
                        e.set_edgecolor('magenta')
            # Put the ellipse in the figure.
            point = axesZoo.add_artist(e)

            # If there are several distinct meta data values, they are interconnected.
            # In that case we do not need to annotate both ellipses. One will do.
            if self.config.getInterconnectMetaValues():
                if thisLabel in self.data.getLabelsToShowAlways() and thisLabel not in labelsDrawn:
                    labelsDrawn.add(thisLabel)
                    annotation = self._annotateEllipse(xy, self.xRange[metaValue], hx, hy, labelText, axesZoo)
                    self._pointsWithAnnotation.append([point, annotation, pattern, xy])
                    annotation.set_visible(True)
                else:
                    annotation = self._annotateEllipse(xy, self.xRange[metaValue], hx, hy, labelText, axesZoo)
                    self._pointsWithAnnotation.append([point, annotation, pattern, xy])
                    annotation.set_visible(False)
            else:
                annotation = self._annotateEllipse(xy, self.xRange[metaValue], hx, hy, labelText, axesZoo)
                self._pointsWithAnnotation.append([point, annotation, pattern, xy])
                if thisLabel in self.data.getLabelsToShowAlways():
                    annotation.set_visible(True)
            count += 1

        # Plot some ellipses meant for reference but only
        # if we do not show annotations at startup.
        if self.config.getAlexanderStyle():
            if self.config.getShowUnitDataPoint():
                self._plotUnitEllipses(axesZoo)
            # if not self.config.getShowAnnotationsAtStartup():
            #     self._plotReferenceEllipses(axesZoo)
            if self.config.getShowHelperCircles():
                self._plotHelperCircles(axesZoo)

        if self.debug:
            print '_plotDistributions:count:', count

