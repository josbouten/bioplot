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

from numpy import arange
from sys import exit

import matplotlib.pyplot as plt

def singleSanitize(filename):
    filename = filename.replace(' ', '_')
    filename = filename.replace(',', '_')
    filename = filename.replace("'", '')
    filename = filename.replace(':', '_')
    filename = filename.replace(';', '_')
    filename = filename.replace('__', '_')
    return filename

def sanitize(filenames):
    ret = []
    for filename in filenames:
        ret.append(singleSanitize(filename))
    return ret

def convert(value):
    """
    Convert a string to a float, or int or leave it as it was.
    :param value: a string
    :return: float, integer or string copy of the input param
    """

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

    # But maybe it is an integer.
    try:
        value = int(value)
        return value
    except Exception:
        pass

    # Otherwise it must be a string
    return value


def assignColors2MetaDataValue(setOfMetaDataValues, listOfColorTuples):
    cols = {}
    listOfMetaDataValues = list(setOfMetaDataValues)
    # Sort the labels
    listOfMetaDataValues.sort()
    cnt = 0
    # Assign colors to the labels.
    for el in listOfMetaDataValues:
        thisColor = listOfColorTuples[cnt]
        cols[el] = thisColor
        cnt += 1
        # If there are not enough colors, wrap around.
        if cnt == len(listOfColorTuples):
            cnt = 0
    return cols


def plotIt(y, title=None):
    """
    plot a signal
    """
    fig = plt.figure()
    axes = fig.add_subplot(111)
    color = 'r+-'
    x = arange(len(y))
    axes.plot(x, y, color)
    if title:
        axes.set_title(title)
    plt.show()


def plotIt2(y1, y2, label1, label2):
    """
    plot 2 signals
    """
    if len(y1) < len(y2):
        x = arange(len(y1))
    else:
        x = arange(len(y2))
    fig = plt.figure()
    axes = fig.add_subplot(111)
    color = 'r+-'
    axes.plot(x, y1[0:len(x)], color, label=label1)
    color = 'go-'
    axes.plot(x, y2[0:len(x)], color, label=label2)
    axes.legend()
    plt.show()

def write2file(filename, thisList):
    try:
        f = open(filename, 'wt')
        for el in thisList:
            f.write("%s\n" % el)
        f.close()
    except Exception as e:
        print(e)
        exit(1)
