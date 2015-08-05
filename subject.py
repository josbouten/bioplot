__author__ = 'jos'

'''
    This class represents the data for a given subject.

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

from format import Format

class Subject(Format):
    def __init__(self, thisPattern, thisAgmsv, thisAimsv, thisNumberOfTargets, thisNumberOfNonTargets, thisDebug=True):
        Format.__init__(self, thisDebug)
        self._pattern = thisPattern
        self._aimsv = thisAimsv
        self._agmsv = thisAgmsv
        self._numberOfTargets = thisNumberOfTargets
        self._numberOfNonTargets = thisNumberOfNonTargets
        self.debug = thisDebug

        self._agmStdDev = None
        self._aimStdDev = None
        self._soLonly = False


    def getAimsv(self):
        return self._aimsv

    def getAimStdDev(self):
        return self._aimStdDev

    def getAgmsv(self):
        return self._agmsv

    def getAgmStdDev(self):
        return self._agmStdDev

    def getLabel(self):
        return self.getLabelFromPattern(self.getPattern())

    def getSingleScore(self):
        return self._soLonly

    def getNumberOfNonTargets(self):
        return self._numberOfNonTargets

    def getNumberOfTargets(self):
        return self._numberOfTargets

    def getMetaValue(self):
        return self.getMetaFromPattern(self.getPattern())

    def getPattern(self):
        # Pattern is label of subject combined with meta data tag.
        return self._pattern

    def setAgmsv(self, thisAgmsv):
        self._agmsv = thisAgmsv

    def setAgmStdDev(self, value):
        self._agmStdDev = value

    def setAimsv(self, thisAimsv):
        self._aimsv = thisAimsv

    def setAimStdDev(self, value):
        self._aimStdDev = value

    def setSingleScore(self, boolean):
        self._soLonly = boolean

    def setNumberOfTargets(self, thisNumber):
        self._numberOfTargets = thisNumber

    def setNumberOfNonTargets(self, thisNumber):
        self._numberOfNonTargets = thisNumber

