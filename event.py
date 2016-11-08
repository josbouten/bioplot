#!/usr/bin/env python3.5

__author__ = 'drs. ing. Jos Bouten'
'''
    event.py

    Object to handle gui events.

    Copyright (C) 2014, 2015, 2016 Jos Bouten ( josbouten at gmail dot com )

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
from utils import sanitize

class Event:
    def __init__(self, thisConfig, thisFig, thisTitle, thisPlotType, thisDebug):
        self.config = thisConfig
        self.fig = thisFig
        self.title = thisTitle
        self.plotType = thisPlotType
        self.debug = thisDebug

    def onEvent(self, event):
        """
        Callback function handling button presses
        will write figure to disk.

        :param event: button code
        :return: nothing
        """
        if self.debug:
            print(("You pressed key {:s}".format(event.key)))
        filename = self.title + "_" + self.plotType + '.png'

        # Spaces in filenames are a nuisance.
        filename = sanitize(filename)

        try:
            if not os.path.exists(self.config.getOutputPath()):
                makedirs(self.config.getOutputPath())
        except Exception as e:
            print(e)
            sys.exit(1)

        # Note: l, k, g, s and f are predefined keys
        # With them you can:
        # k: toggle between lin horizontal scale and log horizontal scale
        # l: toggle between lin vertical scale and log vertical scale
        # s: open save menu
        # f: toggle between standard size and full screen
        # any other key will make that the file is saved in its current dimensions.
        # To get a nice plot it is wise to maximise and then press any key. Then close
        # the window.

        path = self.config.getOutputPath() + os.path.sep + filename
        self.fig.savefig(path, bbox_inches=0)
        print('Figure was saved to:', path)
