#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''
    format.py

    Object to handle basic data formats

    Inherited by subject.py, matrix.py, histogram.py, data.py.

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

class Format():
    def __init__(self, thisDebug=True):
        self.debug = thisDebug
        # The separators should be characters that will
        # NOT be part of the meta data values in the
        # raw data file.
        self.LABEL_SEPARATOR = '_#_'

        '''
        Some examples of patterns:
        286_#_A
        1087_#_B
        1025_#_A
        1113_#_C
        1025_#_24_1_21
        '''

    def getLabelFromPattern(self, pattern):
        '''
        Return label part of a pattern.

        :param pattern: '1025_#_24_1_21'
        :return: '1025'
        '''
        tmp = pattern.split(self.LABEL_SEPARATOR)
        return tmp[0]

    def getMetaFromPattern(self, template):
        '''
        Return meta data value part of a pattern.

        :param pattern: '1025_#_24_1_21'
        :return: '24_1_21'
        '''
        tmp = template.split(self.LABEL_SEPARATOR)
        return tmp[1]

    def mkTemplate(self, label, metaValue):
        return label + self.LABEL_SEPARATOR + metaValue

    def prettyfy(self, pattern):
        return pattern.replace('_', ' ')