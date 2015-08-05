__author__ = 'drs. ing. Jos Bouten'

'''
    ranking.py

    Object to compile a ranking list and generate a ranking plot.

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

from collections import OrderedDict
import matplotlib.pyplot as plt
import os.path
from os import makedirs
from event import Event
import sys
from utils import sanitize

class Ranking():
    def __init__(self, thisData, thisConfig, thisDebug=True):
        self.data = thisData
        self.config = thisConfig
        self.debug = thisDebug
        self.title = self.data.getTitle()

    def _findType(self, data, seek):
        '''
        Find the first occurrence of 'seek' in the ordered list of keys in dict 'data'
        A partial occurrence of seek is accepted.
        :param data: list of dicts
        :param seek: text string
        :return: int: index to position in ordered version of dict 'data'
        '''
        odata = OrderedDict(sorted(data.items(), key=lambda x: x[1], reverse=True))
        index = 1
        for el in odata:
            if seek in el:
                return index
            index += 1
        if self.debug:
            print '_find:found:', index
        return index

    def computeRanking(self):
        '''
        Compute the ranking position for all labels available in self.labels from their scores.

        :return: dict of ranking positions for key = label
        '''
        print 'Computing ranking'

        self.labels = self.data.getTargetLabels()
        ranking = {}
        maxRank = 0
        cnt = 0
        for label in self.labels:
            try:
                thisRank = self._findType(dict(self.data.getResultsOrg()[label]), label)
                ranking[label] = thisRank
                maxRank = max(maxRank, thisRank)
                cnt += 1
            except Exception:
                print 'not found'
                pass
        if self.debug:
            print 'computeRanking.max:', maxRank
            print 'computeRanking:number of ranks found:', cnt
        return ranking, maxRank

    def _onEvent(self, event):
        '''
        Callback function handling button presses
        Will write figure to disk.

        :param event: button code
        :return: nothing
        '''
        if self.debug:
            print("You pressed key {:s}".format(event.key))
        filename = self.title + "_" + self.plotType + '.png'
        filename = sanitize(filename)

        try:
            if not os.path.exists(self.config.getBasePath()):
                makedirs(self.config.getBasePath())
        except Exception, e:
            print e
            sys.exit(1)

        # Note: l, k, g, s and f are predefined keys
        # With them you can:
        # k: toggle between lin horizontal scale and log horizontal scale
        # l: toggle between lin vertical scale and log vertical scale
        # s: open save menu
        # f: toggle between standard size and full screen

        path = self.config.getBasePath() + os.path.sep + filename
        self.fig.savefig(path, bbox_inches=0)
        print 'Figure was saved to:', path

    def getNrLabels(self, ranking, thisRank):
        '''
        Count the number of labels at or below this rank.

        :param  ranking: list of ranking positions
        :param  thisRank: integer: rank value used as threshold
        '''
        cnt = 0
        for r in ranking.values():
            if r <= thisRank:
                cnt += 1
        return cnt

    def _mkPercentString(self, y):
        points = [10, 25, 50, 75]
        s = ""
        for p in points:
            if p < len(y):
                s = s + "P(r<=%d)=%d%s " % (p, y[p], "%")
        return s

    def plot(self):
        '''
        Cumulative Ranking Plot
        '''
        self.plotType = "ranking_plot"
        self.ranking, self.maxRank = self.computeRanking()
        self.fig = plt.figure()
        self.event = Event(self.config, self.fig, self.title, self.plotType, self.debug)
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        nr = len(self.ranking)
        x = []
        y = []
        increment = 1
        # range of the scores in 100 steps
        for thisRank in range(1, self.maxRank, increment):
            y.append(float(self.getNrLabels(self.ranking, thisRank)) / float(nr) * 100.0)
            x.append(thisRank)
        axes = self.fig.add_subplot(111)
        color = 'r+-'
        axes.plot(x, y, color)
        axes.set_xlim(0, self.maxRank * 1.05)
        axes.set_ylim(0, 100)
        axes.set_title("Ranking plot for '%s'" % self.title)
        plt.xlabel("Rank %s" % self._mkPercentString(y))
        plt.ylabel('Probability')
        plt.grid()
        plt.show()
