#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''
    circularhist.py

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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from matplotlib.pyplot import rc

class CircularHistPlot():
    def __init__(self, debug=True):
        self.debug = debug
        self.bottom = 0.2


    def plot(self, angles, score, axes=plt):
        N = len(angles)
        if self.debug:
            print 'CircularHistPlot: N:', N
        hist, bin_edges = np.histogram(angles, bins=N, normed=True, density=False)
        maxHeight = max(hist) * 1.0
        theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
        width = 2 * np.pi / N
        bars = axes.bar(theta, hist / maxHeight, width=width, bottom=self.bottom)
        axes.set_xlabel("Distribution of slopes. $\\delta$ = %0.5f" % (score))

        # To be implemented:
        # We do not want a ticker on the radial axis.

        # Give the bars some colors
        for r, bar in zip(hist, bars):
            bar.set_facecolor(plt.cm.jet(r))
            bar.set_alpha(0.8)


    def test(self):
        N = 80
        score = 1.0012345
        radii = np.random.rand(N)
        axes = plt.subplot(111, polar=True)
        self.plot(radii, score, axes)
        plt.show()


if __name__ == '__main__':
    c = CircularHistPlot()
    c.test()