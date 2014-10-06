#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''

    config.py

    Parse and read values from config file 'bioplot.cfg'

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

import ConfigParser
import sys

class Config():
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()

        try:
            self.config.read('bioplot.cfg')
        except ConfigParser.ParsingError, e:
            print e
            sys.exit(1)

        # Show vertical axis as in Alexander et al [2014].
        self._alexanderStyleDefault = True
        try:
            self._alexanderStyle = self.config.getboolean('zoo', 'alexanderStyle')
        except Exception:
            self._alexanderStyle = self._alexanderStyleDefault

        # We do not want to include an experiment twice,
        # assuming that the scores are symmetric.
        # This may not be the case! So choose what is
        # appropriate.
        self._allowDupsDefault = False
        try:
            self._allowDups = self.config.getboolean('cfg', 'allowDups')
        except Exception:
            self._allowDups = self._allowDupsDefault

        # Show labels for data points within quartile ranges
        self._annotateQuartileMembersDefault = False
        try:
            self._annotateQuartileMembers = self.config.getboolean('zoo', 'annotateQuartileMembers')
        except Exception:
            self._annotateQuartileMembers = self._annotateQuartileMembersDefault

        self._boutenStyleDefault = True
        try:
            self._boutenStyle = self.config.getboolean('zoo', 'boutenStyle')
        except Exception:
            self._boutenStyle = self._boutenStyleDefault

        # The colormap used to colour the ellipses and histograms
        # Usable colormaps are:
        # Spectral, gist_ncar, hsv, gist_rainbow, prism'
        self._colorLookUpTableDefault = 'Spectral'
        try:
            self._colorLookUpTable = self.config.get('cfg', 'colorMap').strip()
        except Exception:
            self._colorLookUpTable = self._colorLookUpTableDefault

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

        self._limitStdDevsDefault = True
        try:
            self._limitStdDevs = self.config.getboolean('zoo', 'limitStdDevs')
        except Exception:
            self._limitStdDevs = True

        ''' max nr steps in ranking plot '''
        self._maxNrStepsDefault = 500
        try:
            self._maxNrSteps = self.config.getint('ranking', 'maxNrSteps')
        except Exception:
            self._maxNrSteps = self._maxNrStepsDefault

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
            self._nrBins = self.config.getint('histogram', 'nrBins')
        except Exception:
            self._nrBins = self._nrBinsDefault

        self._nrAccPointsDefault = 50
        try:
            self._nrAccPoints = self.config.getint('accuracy', 'nrPoints')
        except Exception:
            self._nrAccPoints = self._nrAccPointsDefault

        self._nrRankingPointsDefault = 50
        try:
            self._nrRankingPoints = self.config.getint('ranking', 'nrPoints')
        except Exception:
            self._nrRankingPoints = self._nrRankingPointsDefault


        self._opacityLimitFactorDefault = 0.75
        try:
            self._opacityLimitFactor = self.config.getfloat('zoo', 'opacityLimitFactor')
        except Exception:
            self._opacityLimitFactor = self._opacityLimitFactorDefault

        # Path to store the target and non target score values in text file
        # for further processing ( maybe calculation of EER ? ).
        self._outputPathDefault = 'output'
        try:
            self._outputPath = self.config.get('cfg', 'outputPath').strip()
        except Exception:
            self._outputPath = self._outputPathDefault

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

        # How wide and high do we want the ellipses in the zoo plot to be.
        # Since they cover 3 std's at max we normalize their height and width values
        # to the figure's full resolution width (assuming a square plot)
        # and multiply by a scaleFactor to make them visible as not too small and
        # not too bit
        self._scaleFactorDefault = 150
        try:
            self._scaleFactor = self.config.getint('zoo', 'scaleFactor')
        except Exception:
            self._scaleFactor = self._scaleFactorDefault

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

        # Show config info at startup of program ( actually when instantiating the config object )
        self._showConfigInfoDefault = True
        try:
            self._showConfigInfo = self.config.getboolean('cfg', 'showConfigInfo')
        except Exception:
            self._showConfigInfo = self._showConfigInfoDefault

        self._showKernelInHistDefault = True
        try:
            self._showKernelInHist = self.config.getboolean('zoo', 'showKernelInHist')
        except Exception:
            self._showKernelInHist = self._showKernelInHistDefault

        self._showMetaInHistDefault = True
        try:
            self._showMetaInHist = self.config.getboolean('histogram', 'showMetaInHist')
        except Exception:
            self._showMetaInHist = self._showMetaInHistDefault

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

        self._showTextAtReferenceAtStartupDefault = True
        try:
            self._showTextAtReferenceAtStartup = self.config.getboolean('zoo', 'showTextAtReferenceAtStartup')
        except Exception:
            self._showTextAtReferenceAtStartup = self._showTextAtReferenceAtStartupDefault

        self._spacingDefault = 0.02
        try:
            self._spacing = self.config.getfloat('layout', 'spacing')
        except Exception:
            self._spacing = self._spacingDefault

        self._useOpacityForBigEllipsesDefault = True
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
        if self.getShowConfigInfo():
            print 'Config info:', self.toString()

    # GETTERS

    def getAlexanderStyle(self):
        return self._alexanderStyle

    def getAnnnotateQuartileMembers(self):
        return self._annotateQuartileMembers

    def getAllowDups(self):
        return self._allowDups

    def getBoutenStyle(self):
        return self._boutenStyle

    def getColorMap(self):
        '''
        Get name of color lookup table
        :return: color lookup table name
        '''
        return self._colorLookUpTable

    def getDebug(self):
        return self._debug

    def getDimmingFactor(self):
        return self._dimmingFactor

    def getInterconnectMetaValues(self):
        return self._interconnectMetaValues

    def getLimitStdDevs(self):
        return self._limitStdDevs

    def getMaxNrSteps(self):
        return self._maxNrSteps

    def getNoHistAnnot(self):
        return self._noHistAnnot

    def getNormHist(self):
        return self._normHist

    def getNrBins(self):
        return abs(self._nrBins)

    def getNrAccPoints(self):
        return self._nrAccPoints

    def getNrRankingPoints(self):
        return self._nrRankingPoints

    def getOpacityLimitFactor(self):
        if self._opacityLimitFactor > 1.0:
            self._opacityLimitFactor = 1.0
        if self._opacityLimitFactor < 0:
            self._opacityLimitFactor = 0.0
        return self._opacityLimitFactor

    def getOutputPath(self):
        '''
        Get path to data directory
        :return: string: path to data directory
        '''
        return self._outputPath

    def getRunningOSX(self):
        return self._runningOSX

    def getScaleFactor(self):
        '''
        Get scale factor to give the width and heights of ellipses.
        :return: int: scale factor
        '''
        if self._scaleFactor < 0.0:
            self._scaleFactor = self._scaleFactorDefault
        return self._scaleFactor

    def getShowAnnotationsAtStartup(self):
        return self._showAnnotationsAtStartup

    def getShowCircularHistogram(self):
        return self._showCircularHistogram

    def getShowConfigInfo(self):
        return self._showConfigInfo

    def getShowKernelInHist(self):
        return self._showKernelInHist

    def getShowMetaInHist(self):
        return self._showMetaInHist

    def getShowReference(self):
        return self._showReference

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

    def setShowConfigInfo(self, value):
        self._showConfigInfo = False

    def setShowAnnotationsAtStartup(self, value):
        self._showAnnotationsAtStartup = value

    def toString(self):
        string = "annotateQuartileMembers = " + str(self.getAnnnotateQuartileMembers())
        string += ", alexanderStyle = " + str(self.getAlexanderStyle())
        string += ", allowDups = " + str(self.getAllowDups())
        string += ", boutenStyle = " + str(self.getBoutenStyle())
        string += ", colorMap = " + str(self.getColorMap())
        string += ", debug = " + str(self.getDebug())
        string += ", dimmingFactor = " + str(self.getDimmingFactor())
        string += ", interconnectMetaValues = " + str(self.getInterconnectMetaValues())
        string += ", limitStdDevs = " + str(self.getLimitStdDevs())
        string += ", maxNrSteps = " + str(self.getMaxNrSteps())
        string += ", noHistAnnot = " + str(self.getNoHistAnnot())
        string += ", normHist = " + str(self.getNormHist())
        string += ", nrAccPoints = " + str(self.getNrAccPoints())
        string += ", nrBins = " + str(self.getNrBins())
        string += ", nrRankingPoints = " + str(self.getNrRankingPoints())
        string += ", opacityLimitFactor = " + str(self.getOpacityLimitFactor())
        string += ", outputPath = " + self.getOutputPath()
        string += ", runningOSX = " + str(self.getRunningOSX())
        string += ", scaleFactor = " + str(self.getScaleFactor())
        string += ", showAnnotationsAtStartup = " + str(self.getShowAnnotationsAtStartup())
        string += ", showCircularHistogram = " + str(self.getShowCircularHistogram())
        string += ", showConfigInfo = " + str(self.getShowConfigInfo())
        string += ", showKernelInHist = " + str(self.getShowKernelInHist())
        string += ", showMetaInHist = " + str(self.getShowMetaInHist())
        string += ", showReference = " + str(self.getShowReference())
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