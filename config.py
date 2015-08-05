#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''

    config.py

    Parse and read values from config file 'bioplot.cfg'

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

import ConfigParser
import sys
import numpy as np
import os.path

class Config():
    def __init__(self, thisConfigFilename='bioplot.cfg'):
        self.configFilename = thisConfigFilename
        self.config = ConfigParser.RawConfigParser()
        self._fileNotFound = False

        if os.path.exists(self.configFilename):
            try:
                self.config.read(self.configFilename)
            except Exception, e:
                print e
                sys.exit(1)
        else:
            print "Error reading %s, file not found." % self.configFilename
            self._fileNotFound = True

        # Show vertical axis as in Alexander et al [2014].
        self._alexanderStyleDefault = True
        try:
            self._alexanderStyle = self.config.getboolean('zoo', 'alexanderStyle')
        except Exception:
            self._alexanderStyle = self._alexanderStyleDefault

        self._alpha4ReferencesDefault = 0.5
        try:
            self._alpha4ReferenceCircles = self.config.getfloat('zoo', 'alpha4ReferenceCircles')
        except Exception:
            self._alpha4ReferenceCircles = self._alpha4ReferencesDefault

        self._alpha4UnitCirclesDefault = 0.5
        try:
            self._alpha4UnitCircles = self.config.getfloat('zoo', 'alpha4UnitCircles')
        except Exception:
            self._alpha4UnitCircles = self._alpha4UnitCirclesDefault


        self._alwaysSaveDefault = True
        try:
            self._alwaysSave = self.config.getboolean('cfg', 'alwaysSave')
        except Exception:
            self._alwaysSave = self._alwaysSaveDefault

        # We do not want to include an experiment twice,
        # assuming that the scores are symmetric.
        # This may not be the case! So choose what is
        # appropriate.
        self._allowDupsDefault = False
        try:
            self._allowDups = self.config.getboolean('data', 'allowDups')
        except Exception:
            self._allowDups = self._allowDupsDefault

        # Show labels for animals in data points within quartile ranges
        self._animalColorsDefault = 'multi'
        try:
            self._animalColors = self.config.get('zoo', 'animalColors')
        except Exception:
            self._animalColors = self._animalColorsDefault


        # Show labels for data points within quartile ranges
        self._annotateEllipsesDefault = False
        try:
            self._annotateEllipses = self.config.getboolean('zoo', 'annotateEllipses')
        except Exception:
            self._annotateEllipses = self._annotateEllipsesDefault

        self._boutenStyleDefault = True
        try:
            self._boutenStyle = self.config.getboolean('zoo', 'boutenStyle')
        except Exception:
            self._boutenStyle = self._boutenStyleDefault

        self._colorsDefault = [("IWouldCallThisBlueIsh", "3399FF"),
                              ("Orangy", "255, 125, 10"),
                              ("rustLike", "96, 17, 0"),
                              ("someSortOfPink", "255, 54, 160"),
                              ("OneOf50ShadesOfGrey", "10, 5, 8"),
                              ("someWhatBlue", "1414FF"),
                              ("definatelyGreen", "0, 255, 0"),
                              ("definatelyRed", "255, 0, 0")]
        try:
            self._colors = self.config.items("metacolors")
        except Exception:
            self._colors = self._colorsDefault

        self._combineMatricesDefault = False
        try:
            self._combineMatrices = self.config.getboolean('matrix', 'combineMatrices')
        except Exception:
            self._combineMatrices = self._combineMatricesDefault

        # If set to true, debug will make all object produce lots of info
        # which may be of use when debugging the program.
        self._debugDefault = False
        try:
            self._debug = self.config.getboolean('cfg', 'debug')
        except Exception:
            self._debug = self._debugDefault

        self._dimmingFactorDefault = 0.8
        try:
            self._dimmingFactor = self.config.getfloat('zoo', 'dimmingFactor')
        except Exception:
            self._dimmingFactor = self._dimmingFactorDefault

        self._interconnectMetaValuesDefault = True
        try:
            self._interconnectMetaValues = self.config.getboolean('zoo', 'interconnectMetaValues')
        except Exception:
            self._interconnectMetaValues = self._interconnectMetaValuesDefault

        self._labelAngleDefault = 70
        try:
            self._labelAngle = self.config.getint('matrix', 'labelAngle')
        except Exception:
            self._labelAngle = self._labelAngleDefault

        self._labelColorDefault = 'A0A0A0'
        try:
            self._labelColor = self.config.get('zoo', 'labelColor')
        except Exception:
            self._labelColor = self._labelColorDefault

        self._lineWidthDefault = 1.0
        try:
            self._lineWidth = self.config.getfloat('zoo', 'lineWidth')
        except Exception:
            self._lineWidth = 1.0

        self._limitStdDevsDefault = True
        try:
            self._limitStdDevs = self.config.getboolean('zoo', 'limitStdDevs')
        except Exception:
            self._limitStdDevs = True

        self._matrixColorMapDefault = 'Greys'
        try:
            self._matrixColorMap = self.config.get('matrix', 'matrixColorMap')
        except Exception:
            self._matrixColorMap = self._matrixColorMapDefault

        self._maximum4Type1Default = 1.0E+99
        try:
            self._maximum4Type1 = self.config.getfloat('data', 'maximum4Type1')
        except Exception:
            self._maximum4Type1 = self._maximum4Type1Default

        self._maximum4Type3Default = 1.0E+99
        try:
            self._maximum4Type3 = self.config.getfloat('data', 'maximum4Type3')
        except Exception:
            self._maximum4Type3 = self._maximum4Type3Default

        self._maxStdDevDefault = 6.0
        try:
            self._maxStdDev = self.config.getfloat('zoo', 'maxStdDev')
        except Exception:
            self._maxStdDev = self._maxStdDevDefault

        self._minimum4Type1Default = -1.0E+99
        try:
            self._minimum4Type1 = self.config.getfloat('data', 'minimum4Type1')
        except Exception:
            self._minimum4Type1 = self._minimum4Type1Default

        self._minimum4Type3Default = -1.0E+99
        try:
            self._minimum4Type3 = self.config.getfloat('data', 'minimum4Type3')
        except Exception:
            self._minimum4Type3 = self._minimum4Type3Default

        self._minNrScores4MatrixPlotDefault = 3
        try:
            self._minNrScores4MatrixPlot = self.config.getint('matrix', 'minNrScores4MatrixPlot')
        except Exception:
            self._minNrScores4MatrixPlot = self._minNrScores4MatrixPlotDefault

        self._minStdDevDefault = 0.01
        try:
            self._minStdDev = self.config.getfloat('zoo', 'minStdDev')
        except Exception:
            self._minStdDev = self._minStdDevDefault

        self._noHistAnnotDefault = False
        try:
            self._noHistAnnot = self.config.getboolean('zoo', 'noHistAnnot')
        except Exception:
            self._noHistAnnot = self._noHistAnnotDefault

        self._normHistDefault = False
        try:
            self._normHist = self.config.getboolean('histogram', 'normHist')
        except Exception:
            self._normHist = self._normHistDefault

        self._nrBinsDefault = 100
        try:
            self._nrBins = self.config.get('histogram', 'nrBins')
        except Exception:
            self._nrBins = self._nrBinsDefault

        self._nrAccPointsDefault = 50
        try:
            self._nrAccPoints = self.config.getint('accuracy', 'nrPoints')
        except Exception:
            self._nrAccPoints = self._nrAccPointsDefault

        self._nrSamples4EERDefault = 200
        try:
            self._nrSamples4Probability = self.config.getint('probability', 'nrSamples4Probability')
        except Exception:
            self._nrSamples4Probability = self._nrSamples4EERDefault

        self._minimumOpacityValueDefault = 0.1
        try:
            self._minimumOpacityValue = self.config.getfloat('zoo', 'minimumOpacityValue')
        except Exception:
            self._minimumOpacityValue = self._minimumOpacityValueDefault

        # Path to store the target and non target score values in text file
        # for further processing ( maybe calculation of EER ? ).
        self._outputPathDefault = 'output'
        try:
            self._outputPath = self.config.get('cfg', 'outputPath').strip()
        except Exception:
            self._outputPath = self._outputPathDefault

        self._opacity4EllipsesDefault = 0.7
        try:
            self._opacity4Ellipses = self.config.getfloat('zoo', 'opacity4Ellipses').strip()
        except Exception:
            self._opacity4Ellipses = self._opacity4EllipsesDefault

        # How wide and high do we want the ellipses in the zoo plot to be.
        # Since they cover 3 std's at max we normalize their height and width values
        # to the figure's full resolution width (assuming a square plot)
        # and multiply by a scaleFactor to make them visible as not too small and
        # not too bit

        self._saveScoresDefault = True
        try:
            self._saveScores = self.config.getboolean('cfg', 'saveScores')
        except Exception:
            self._saveScores = self._saveScoresDefault

        self._scaleFactorDefault = 150
        try:
            self._scaleFactor = self.config.getint('zoo', 'scaleFactor')
        except Exception:
            self._scaleFactor = self._scaleFactorDefault

        self._screenResolutionDefault = "1280x1024"
        try:
            self._screenResolution = self.config.get('layout', 'screenResolution')
        except Exception:
            self._screenResolution = self._screenResolutionDefault

        self._showAnnotationsAtStartupDefault = False
        try:
            self._showAnnotationsAtStartup = self.config.getboolean('zoo', 'showAnnotationsAtStartup')
        except Exception:
            self._showAnnotationsAtStartup = self._showAnnotationsAtStartupDefault

        self._showCircularHistogramDefault = False
        try:
            self._showCircularHistogram = self.config.getboolean('zoo', 'showCircularHistogram')
        except Exception:
            self._showCircularHistogram = self._showCircularHistogramDefault

        self._showCllrValuesDefault = True
        try:
            self._showCllrValues = self.config.getboolean('zoo', 'showCllrValues')
        except Exception:
            self._showCllrValues = self._showCllrValuesDefault

        self._showEdgeColorDefault = True
        try:
            self._showEdgeColor = self.config.getboolean('zoo', 'showEdgeColor')
        except Exception:
            self._showEdgeColor = self._showEdgeColorDefault

        self._showMinCllrValuesDefault = True
        try:
            self._showMinCllrValues = self.config.getboolean('zoo', 'showMinCllrValues')
        except Exception:
            self._showMinCllrValues = self._showMinCllrValuesDefault

        # Show config info at startup of program ( actually when instantiating the config object )
        self._showConfigInfoDefault = True
        try:
            self._showConfigInfo = self.config.getboolean('cfg', 'showConfigInfo')
        except Exception:
            self._showConfigInfo = self._showConfigInfoDefault

        self._showEerValuesDefault = True
        try:
            self._showEerValues = self.config.getboolean('zoo', 'showEerValues')
        except Exception:
            self._showEerValues = self._showEerValuesDefault

        self._showKernelInHistDefault = True
        try:
            self._showKernelInHist = self.config.getboolean('histogram', 'showKernelInHist')
        except Exception:
            self._showKernelInHist = self._showKernelInHistDefault

        self._showMatrixLabelsDefault = True
        try:
            self._showMatrixLabels =  self.config.getboolean('matrix', 'showMatrixLabels')
        except Exception:
            self._showMatrixLabels = self._showMatrixLabelsDefault

        self._showAverageTargetAndNonTargetMatchScoresDefault = True
        try:
            self._showAverageTargetAndNonTargetMatchScores = self.config.getboolean('zoo', 'showAverageTargetAndNonTargetMatchScores')
        except Exception:
            self._showAverageTargetAndNonTargetMatchScores = self._showAverageTargetAndNonTargetMatchScoresDefault

        self._showMetaInHistDefault = True
        try:
            self._showMetaInHist = self.config.getboolean('histogram', 'showMetaInHist')
        except Exception:
            self._showMetaInHist = self._showMetaInHistDefault

        self._showNrTargetsAndNonTargetsDefault = True
        try:
            self._showNrTargetsAndNonTargets = self.config.getboolean('zoo', 'showNrTargetsAndNonTargets')
        except Exception:
            self._showNrTargetsAndNonTargets = self._showNrTargetsAndNonTargetsDefault

        self._showUnitDataPointDefault = True
        try:
            self._showUnitDataPoint = self.config.getboolean('zoo', 'showUnitDataPoint')
        except Exception:
            self._showUnitDataPoint = self._showUnitDataPointDefault

        # Show ellipse for -2, 0 and 2 std and one for mean agm/aim.
        self._showReferenceDefault = True
        try:
            self._showReference = self.config.getboolean('zoo', 'showReference')
        except Exception:
            self._showReference = self._showReferenceDefault

        self._showStdDevDefault = False
        try:
            self._showStdDev = self.config.getboolean('zoo', 'showStdDev')
        except Exception:
            self._showStdDev = self._showStdDevDefault

        self._showTextAtReferenceAtStartupDefault = False
        try:
            self._showTextAtReferenceAtStartup = self.config.getboolean('zoo', 'showTextAtReferenceAtStartup')
        except Exception:
            self._showTextAtReferenceAtStartup = self._showTextAtReferenceAtStartupDefault

        self._spacingDefault = 0.02
        try:
            self._spacing = self.config.getfloat('layout', 'spacing')
        except Exception:
            self._spacing = self._spacingDefault

        self._runningWindowsDefault = False
        try:
            self._runningWindows = self.config.getboolean('cfg', 'runningWindows')
        except Exception:
            self._runningWindows = self._runningWindowsDefault

        self._runningOSXDefault = False
        try:
            self._runningOSX = self.config.getboolean('cfg', 'runningOSX')
        except Exception:
            self._runningOSX = self._runningOSXDefault

        self._useColorsForQuartileRangesDefault = False
        try:
            self._useColorsForQuartileRanges = self.config.getboolean('zoo', 'useColorsForQuartileRanges')
        except Exception:
            self._useColorsForQuartileRanges = self._useColorsForQuartileRangesDefault

        self._useOpacityForBigEllipsesDefault = False
        try:
            self._useOpacityForBigEllipses = self.config.getboolean('zoo', 'useOpacityForBigEllipses')
        except Exception:
            self._useOpacityForBigEllipses = self._useOpacityForBigEllipsesDefault

        self._xHeightDefault = 0.2
        try:
            self._xHeight = self.config.getfloat('layout', 'xheight')
        except Exception:
            self._xHeight = self._xHeightDefault

        # Show vertical axis as in Yager et al.as
        self._yagerStyleDefault = True
        try:
            self._yagerStyle = self.config.getboolean('zoo', 'yagerstyle')
        except Exception:
            self._yagerStyle = self._yagerStyleDefault

        self._yWidthDefault = 0.2
        try:
            self._yWidth = self.config.getfloat('layout', 'ywidth')
        except Exception:
            self._yWidth = self._yWidthDefault

        self._zLeftDefault = 0.1
        try:
            self._zLeft = self.config.getfloat('layout', 'zleft')
        except Exception:
            self._zLeft = self._zLeftDefault

        self._zWidthDefault = 0.65
        try:
            self._zWidth = self.config.getfloat('layout', 'zwidth')
        except Exception:
            self._zWidth = self._zWidthDefault

        self._zBottomDefault = 0.05
        try:
            self._zBottom = self.config.getfloat('layout', 'zbottom')
        except Exception:
            self._zBottom = self._zBottomDefault

        self._zHeightDefault = 0.63
        try:
            self._zHeight = self.config.getfloat('layout', 'zheight')
        except Exception:
            self._zHeight = self._zHeightDefault

        # Show all info on the command line.
        # if self.getShowConfigInfo():
        #     print 'Config info:', self.toString()

    # GETTERS

    def getAlexanderStyle(self):
        return self._alexanderStyle

    def getAlpha4ReferenceCircles(self):
        return self._alpha4ReferenceCircles

    def getAlpha4UnitCircles(self):
        return self._alpha4UnitCircles

    def getAnimalColors(self):
        if self._animalColors == "multi":
            return True
        else:
            return False

    def getAnnnotateEllipses(self):
        return self._annotateEllipses

    def getAllwaysSave(self):
        return self._alwaysSave

    def getAllowDups(self):
        return self._allowDups

    def getBoutenStyle(self):
        return self._boutenStyle

    def _convertColor2RGB(self, colorValue):
        if ',' in colorValue:
            tmp = colorValue.split(',')
            if len(tmp) < 3:
                return None
            else:
                color = (float(tmp[0].strip())/255.0, float(tmp[1].strip())/255.0, float(tmp[2].strip())/255.0)
        else:
            # this must be hex in 6 digits, like 0FA232
            if len(colorValue) < 6:
                return None
            else:
                rValue = int(colorValue[0:2], 16)
                gValue = int(colorValue[2:4], 16)
                bValue = int(colorValue[4:6], 16)
                color = (float(rValue)/255.0, float(gValue)/255.0, float(bValue)/255.0)
        return color

    def getCombineMatrices(self):
        return self._combineMatrices

    def getDebug(self):
        return self._debug

    def getDimmingFactor(self):
        return self._dimmingFactor

    def getFileNotFound(self):
        # Used to signal that the specified config file could not be found.
        return self._fileNotFound

    def getInterconnectMetaValues(self):
        return self._interconnectMetaValues

    def getLabelAngle(self):
        return self._labelAngle

    def getLabelColor(self):
        labelColor = self._convertColor2RGB(self._labelColor)
        if labelColor is None:
            labelColor = self._labelColorDefault
        return labelColor

    def getLimitStdDevs(self):
        return self._limitStdDevs

    def getLineWidth(self):
        return self._lineWidth

    def getMatrixColorMap(self):
        return self._matrixColorMap

    def getMaximum4Type1(self):
        return self._maximum4Type1

    def getMaximum4Type3(self):
        return self._maximum4Type3

    def getMaxStdDev(self):
        return self._maxStdDev

    def getMetaColors(self):
        colors = []
        for (meta, colorValue) in self._colors:
            rgb = self._convertColor2RGB(colorValue)
            if rgb is None:
                print "Format Error: %s %s will be ignored:" % (meta, colorValue)
            else:
                colors.append(rgb)
        return colors

    def getMinimum4Type1(self):
        return self._minimum4Type1

    def getMinimum4Type3(self):
        return self._minimum4Type3

    def getMinNrScores4MatrixPlot(self):
        return self._minNrScores4MatrixPlot

    def getMinStdDev(self):
        return self._minStdDev

    def getNoHistAnnot(self):
        return self._noHistAnnot

    def getNormHist(self):
        return self._normHist

    def _getNrBins(self):
        '''
        :return: String: either a string or a number (as a string)
        '''
        return str(self._nrBins)

    def getNrBins(self, nrDataElements):
        # nrBins = self.config.getNrBins()
        # Square root

        configNrBins = self._getNrBins()
        if configNrBins:
            if "sqrt" in configNrBins:
                nrBins = int(np.sqrt(nrDataElements))
            elif "rice" in configNrBins:
                nrBins = int(2 * np.power(nrDataElements, 1.0/3.0))
            elif "sturges" in configNrBins:
                # Sturges, see https://en.wikipedia.org/wiki/Histogram#Number_of_bins_and_width
                nrBins = np.log2(nrDataElements) + 1
            else:
                nrBins = int(configNrBins)
        else:
            nrBins = 50
        if self.getDebug():
            print 'config::getNrBins:nrBins:', nrBins
        return nrBins

    def getNrAccPoints(self):
        return self._nrAccPoints

    def getNrSamples4Probability(self):
        return self._nrSamples4Probability

    def getMinimumOpacityValue(self):
        """

        :rtype : float
        """
        return self._minimumOpacityValue

    def getOpacity4Ellipses(self):
        return self._opacity4Ellipses

    def getOutputPath(self):
        '''
        Get path to data directory
        :return: string: path to data directory
        '''
        return self._outputPath

    def getRunningWindows(self):
        return self._runningWindows

    def getRunningOSX(self):
        return self._runningOSX

    def getSaveScores(self):
        return self._saveScores

    def getScaleFactor(self):
        '''
        Get scale factor to give the width and heights of ellipses.
        :return: int: scale factor
        '''
        if self._scaleFactor < 0.0:
            self._scaleFactor = self._scaleFactorDefault
        return self._scaleFactor

    def getScreenResolutionString(self):
        # Return screen resolution as string e.g. "1280x1024".
        return self._screenResolution

    def getScreenResolutionTuple(self):
        # Return screen resolution as tuple of integers e.g. (1280, 1024).
        tmp = self._screenResolution.split('x')
        width = int(tmp[0])
        height = int(tmp[1])
        return (width, height)

    def getShowAnnotationsAtStartup(self):
        return self._showAnnotationsAtStartup

    def getShowAverageTargetAndNonTargetMatchScores(self):
        return self._showAverageTargetAndNonTargetMatchScores

    def getShowCircularHistogram(self):
        return self._showCircularHistogram

    def getShowCllrValues(self):
        return self._showCllrValues

    def getShowConfigInfo(self):
        return self._showConfigInfo

    def getShowEerValues(self):
        return self._showEerValues

    def getShowEdgeColor(self):
        return self._showEdgeColor

    def getShowMatrixLabels(self):
        return self._showMatrixLabels

    def getShowMetaInHist(self):
        return self._showMetaInHist

    def getShowMinCllrValues(self):
        return self._showMinCllrValues

    def getShowNrTargetsAndNonTargets(self):
        return self._showNrTargetsAndNonTargets

    def getShowKernelInHist(self):
        return self._showKernelInHist

    def getShowReference(self):
        return self._showReference

    def getShowStdev(self):
        return self._showStdDev

    def getShowTextAtReferenceAtStartup(self):
        return self._showTextAtReferenceAtStartup

    def getShowUnitDataPoint(self):
        return self._showUnitDataPoint

    def getSpacing(self):
        return abs(self._spacing)

    def getUseOpacityForBigEllipses(self):
        return self._useOpacityForBigEllipses

    def getUseColorsForQuartileRanges(self):
        return self._useColorsForQuartileRanges

    def getYagerStyle(self):
        return self._yagerStyle

    def getXheight(self):
        return abs(self._xHeight)

    def getYwidth(self):
        return abs(self._yWidth)

    def getZleft(self):
        return abs(self._zLeft)

    def getZheight(self):
        return abs(self._zHeight)

    def getZbottom(self):
        return abs(self._zBottom)

    def getZwidth(self):
        return abs(self._zWidth)

    # SETTERS

    def setMinNrScores4MatrixPlot(self, value):
        if isinstance(value, int):
            self._minNrScores4MatrixPlot = value

    def setShowConfigInfo(self, value):
        if isinstance(value, bool):
            self._showConfigInfo = value

    def setShowAnnotationsAtStartup(self, value):
        if isinstance(value, bool):
            self._showAnnotationsAtStartup = value

    # Get info.

    def toString(self):
        string  = "alexanderStyle = " + str(self.getAlexanderStyle())
        string += ", alwaysSave = " + str(self.getAllwaysSave())
        string += ", allowDups = " + str(self.getAllowDups())
        string += ", alpha4References = " + str(self.getAlpha4ReferenceCircles())
        string += ", alpha4UnitCircles = " + str(self.getAlpha4UnitCircles())
        string += ", animalColors = " + str(self.getAnimalColors())
        string += ", annotateEllipses = " + str(self.getAnnnotateEllipses())
        string += ", boutenStyle = " + str(self.getBoutenStyle())
        string += ", combineMatrices = " + str(self.getCombineMatrices())
        string += ", debug = " + str(self.getDebug())
        string += ", dimmingFactor = " + str(self.getDimmingFactor())
        string += ", interconnectMetaValues = " + str(self.getInterconnectMetaValues())
        string += ", labelAngle = " + str(self.getLabelAngle())
        string += ", labelColor = " + str(self.getLabelColor())        
        string += ", limitStdDevs = " + str(self.getLimitStdDevs())
        string += ", lineWidth = " + str(self.getLineWidth())
        string += ", matrixColorMap = " + str(self.getMatrixColorMap())
        string += ", maximum4Type1 = " + str(self.getMaximum4Type1())
        string += ", maximum4Type3 = " + str(self.getMaximum4Type3())
        string += ", maxStdDev = " + str(self.getMaxStdDev())
        string += ", metaColors = " + str(self.getMetaColors())
        string += ", minimum4Type1 = " + str(self.getMinimum4Type1())
        string += ", minimum4Type3 = " + str(self.getMinimum4Type3())
        string += ", minNrScores4MatrixPlot =" + str(self.getMinNrScores4MatrixPlot())
        string += ", minimumOpacityValue = " + str(self.getMinimumOpacityValue())
        string += ", minStdDev = " + str(self.getMinStdDev())
        string += ", noHistAnnot = " + str(self.getNoHistAnnot())
        string += ", normHist = " + str(self.getNormHist())
        string += ", nrAccPoints = " + str(self.getNrAccPoints())
        string += ", nrBins = " + str(self._getNrBins()) # use private function here!
        string += ", nrSamples4Probability = " + str(self.getNrSamples4Probability())
        string += ", opacity4Ellipses = " + str(self.getOpacity4Ellipses())
        string += ", outputPath = " + self.getOutputPath()
        string += ", runningWindows = " + str(self.getRunningWindows())
        string += ", runningOSX = " + str(self.getRunningOSX())
        string += ", saveScores = " + str(self.getSaveScores())
        string += ", scaleFactor = " + str(self.getScaleFactor())
        string += ", screenResolution = " + str(self.getScreenResolutionString())
        string += ", showAnnotationsAtStartup = " + str(self.getShowAnnotationsAtStartup())
        string += ", showAverageTargetAndNonTargetMatchScores = " + str(self.getShowAverageTargetAndNonTargetMatchScores())
        string += ", showCircularHistogram = " + str(self.getShowCircularHistogram())
        string += ", showCllrValues = " + str(self.getShowCllrValues())
        string += ", showConfigInfo = " + str(self.getShowConfigInfo())
        string += ", getShowEdgeColor = " + str(self.getShowEdgeColor())
        string += ", showEerValues = " + str(self.getShowEerValues())
        string += ", showKernelInHist = " + str(self.getShowKernelInHist())
        string += ", showMatrixLabels = " + str(self.getShowMatrixLabels())
        string += ", showMetaInHist = " + str(self.getShowMetaInHist())
        string += ", showMinCllrValues = " + str(self.getShowMinCllrValues())
        string += ", showNrTargetsAndNonTargets = " + str(self.getShowNrTargetsAndNonTargets())
        string += ", showReference = " + str(self.getShowReference())
        string += ", showStdev = " + str(self.getShowStdev())
        string += ", showTextAtReferenceAtStartup = " + str(self.getShowTextAtReferenceAtStartup())
        string += ", showUnitDataPoint = " + str(self.getShowUnitDataPoint())
        string += ", spacing = " + str(self.getSpacing())
        string += ", useColorsForQuartileRanges = " + str(self.getUseColorsForQuartileRanges())
        string += ", useOpacityForBigEllipses = " + str(self.getUseOpacityForBigEllipses())
        string += ", xHeight = " + str(self.getXheight())
        string += ", yagerStyle = " + str(self.getYagerStyle())
        string += ", yWidth = " + str(self.getYwidth())
        string += ", zBottom = " + str(self.getZbottom())
        string += ", zHeight = " + str(self.getZheight())
        string += ", zLeft = " + str(self.getZleft())
        string += ", zWidth = " + str(self.getZwidth())
        return string

    def openCfg(self):
        try:
            f = open('cfg.txt', 'w')
        except Exception, e:
            print e
            sys.exit(1)

    def writeLine(self, f, lines):
        for line in lines:
            f.write(line + "\n")

if __name__ == '__main__':

    config = Config()
    print 'main:', config.toString()
