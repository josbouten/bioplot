#!/usr/bin/env python

'''
    eer.py

    Object used to extract compute EER and plot EER in score plot.

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

import matplotlib.pyplot as plt
from event import Event
from probability import Probability

class Eer(Probability):
    def __init__(self, data, config, debug=True):
        self.data = data
        self.config = config
        self.debug = debug
        self.plotType = 'eer_plot'
        Probability.__init__(self, self.data, self.config, self.debug)

    def plot(self):
        self.fig = plt.figure()
        self.event = Event(self.config, self.fig, self.data.getTitle(), self.plotType, self.debug)
        # For saving the pic we use a generic event object
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        axes = self.fig.add_subplot(111)
        eerData = self.computeProbabilities(self.eerFunc)
        for (metaValue, PD, PP, X) in eerData:
            eer, score = self.computeEer(PD, PP, X)
            pFr, = axes.plot(X, PP, 's-', label="P(pros), %s Eer: %0.2f%s at %0.2f" % (metaValue, eer * 100, '%', score))
            pFa, = axes.plot(X, PD, 'o-', label="P(def), %s" % metaValue)
        plt.legend()
        axes.set_title("P(defense) and P(prosecution) for '%s'" % self.data.getTitle())
        plt.xlabel('Threshold (raw score)')
        plt.ylabel('Probability (cumulative distribution function)')
        plt.grid()
        plt.show()