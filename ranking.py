__author__ = 'drs. ing. Jos Bouten'

'''
    ranking.py

    Class to compile a ranking list and generate a ranking plot.

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
from event import Event
from utils import assignColors2MetaDataValue

class Ranking:
    def __init__(self, thisData, thisConfig, thisExpName, thisDebug=True):
        self.data = thisData
        self.config = thisConfig
        self._printToFilename = thisExpName
        self.debug = thisDebug
        self.title = self.data.getTitle()
        self.labels = None
        self.fig = None
        self.event = None
        self.colors = None
        self.nrColors = None
        self.plotType = None

    def _findType(self, data, seek):
        """
        Find the first occurrence of 'seek' in the ordered list of keys in dict 'data'.
        A partial occurrence of seek is accepted.
        :param data: list of dicts.
        :param seek: text string.
        :return: int: index to position in ordered version of dict 'data'.
        """
        odata = OrderedDict(sorted(data.items(), key=lambda x: x[1], reverse=True))
        index = 1
        for el in odata:
            if seek in el:
                return index
            index += 1
        if self.debug:
            print('_find:found:', index)
        return index

    def computeRanking(self, metaValue):
        """
        Compute the ranking position for all labels available in self.labels from their scores.

        :return: dict of ranking positions for key = label.
        """
        if self.debug:
            print('Computing ranking')

        self.labels = self.data.getTargetLabels()
        ranking = {}
        maxRank = 0
        cnt = 0
        for label in self.labels:
            try:
                thisRank = self._findType(dict(self.data.getResults4Subject()[metaValue, label]), label)
                ranking[label] = thisRank
                maxRank = max(maxRank, thisRank)
                cnt += 1
            except Exception as e:
                print('not found')
                pass
        if self.debug:
            print('computeRanking.max:', maxRank)
            print('computeRanking:number of ranks found:', cnt)
        return ranking, maxRank

    def getNrLabels(self, ranking, thisRank):
        """
        Count the number of labels at or below this rank.

        :param  ranking: list of ranking positions
        :param  thisRank: integer: rank value used as threshold
        """
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
                s += "P(r<=%d)=%d%s " % (p, y[p], "%")
        return s

    def plot(self):
        """
        Cumulative Ranking Plot
        """
        self.fig = plt.figure(figsize=(self.config.getPrintToFileWidth(), self.config.getPrintToFileHeight()))
        self.plotType = "ranking_plot"
        self.event = Event(self.config, self.fig, self.title, self.plotType, self.debug)
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        axes = self.fig.add_subplot(111)
        metaColors = self.config.getMetaColors()
        metaDataValues = self.data.getMetaDataValues()
        self.colors = assignColors2MetaDataValue(metaDataValues, metaColors)
        self.nrColors = len(self.colors.keys())
        xlab = "Rank "
        for metaValue in metaDataValues:
            ranking, maxRank = self.computeRanking(metaValue)
            nr = len(ranking)
            x = []
            y = []
            increment = 1
            # range of the scores in 100 steps
            for thisRank in range(1, maxRank, increment):
                y.append(float(self.getNrLabels(ranking, thisRank)) / float(nr) * 100.0)
                x.append(thisRank)
            axes.plot(x, y, "o-", color=self.colors[metaValue], label=metaValue)
            # prepare x-label.
            axes.set_xlim(0, maxRank * 1.05)
            axes.set_ylim(0, 100)
            axes.set_title("Ranking plot for '%s'" % self.title)
            xlab += metaValue + ": " + self._mkPercentString(y) + "\n"
            #print(metaValue)
        # Add labels to the plot.
        plt.ylabel('Probability')
        # Show the x-label without the last /n.
        plt.xlabel(xlab[:-1])
        # Add a legend to the plot.
        axes.legend(loc=5)
        # Add a grid to the plot.
        plt.grid()
        # If so desired, print the plot to a file.
        if self.config.getPrintToFile():
            filename = "%s_%s.%s" % (self._printToFilename, self.plotType, "png")
            print("Writing plot to %s" % filename)
            plt.savefig(filename, orientation='landscape', papertype='letter')
        else:
            # Finally: show the plot.
            plt.show()
