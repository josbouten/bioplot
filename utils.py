#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''

    utils.py

    A set of utility functions.

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

from numpy import linspace
from sys import exit

def showLicense(filename):
    try:
        f = open(filename, 'rt')
    except Exception, e:
        print e
        print "You should have received a copy of the GNU General Public License along \
                with this program; if not, write to the Free Software Foundation, Inc., \
                51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA."
        exit(1)
    else:
        lines = f.readlines()
        f.close()
        for line in lines:
            print line.strip()

def sanitize(filename):
    filename = filename.replace(' ', '_')
    filename = filename.replace(',', '_')
    filename = filename.replace("'", '')
    filename = filename.replace(':', '_')
    filename = filename.replace(';', '_')
    filename = filename.replace('__', '_')
    return filename

def convert(value):
    '''
    Convert a string to a float, or int or leave it as it was.
    :param value: a string
    :return: float, integer or string copy of the input param
    '''

    # It could be a float.
    try:
        value = float(value)
        if value - int(value) > 0:
            # It is a fraction
            return value
        else:
            # We prefer to return integers
            return int(value)
    except Exception:
        pass

    # But maybe it is an integer
    try:
        value = int(value)
        return value
    except Exception:
        pass

    # Otherwise it must be a string
    return value

def assignColors2MetaDataValue(setOfValues, cmap):
    cols = {}
    listOfValues = list(setOfValues)
    num = len(listOfValues) + 1
    # Sort the labels
    listOfValues.sort()
    ll = linspace(1, 255, num)
    cnt = 0
    # Assign colors to the labels.
    for el in listOfValues:
        (R, G, B, A) = cmap(int(ll[cnt]))
        cols[el] = (R, G, B)
        cnt += 1
    return cols
