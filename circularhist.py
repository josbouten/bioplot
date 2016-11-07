#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''
    circularhist.py

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
import numpy as np

import matplotlib.pyplot as plt

class CircularHistPlot:
    def __init__(self, theseAngles, theseScores, theseAxes=plt, thisDebug=True):
        self.angles = theseAngles
        self.score = theseScores
        self.axes = theseAxes
        self.debug = thisDebug
        self.bottom = 0.2

    def plot(self):
        N = len(self.angles)
        if self.debug:
            print('CircularHistPlot: N:', N)
        hist, bin_edges = np.histogram(self.angles, bins=N, normed=True, density=False)
        maxHeight = max(hist) * 1.0
        theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
        width = 2 * np.pi / N
        bars = self.axes.bar(theta, hist / maxHeight, width=width, bottom=self.bottom)
        self.axes.set_xlabel("$\\delta$ = %0.5f" % self.score)

        # To be implemented:
        # We do not want a ticker on the radial axis.

        # Give the bars some colors
        for r, bar in zip(hist, bars):
            bar.set_facecolor(plt.cm.jet(r))
            bar.set_alpha(0.8)

def testCircularPlot():
    N = 80
    score = 1.0012345
    radii = np.random.rand(N)
    axes = plt.subplot(111, polar=True)
    c = CircularHistPlot(radii, score, axes)
    c.plot()
    plt.show()


if __name__ == '__main__':
    testCircularPlot()
