#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''
    accuracy.py

    Object which allows to calculate the accuracy of a biometric system
    at various score threshold levels and show this in a plot.

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
import sys
import os.path
from os import makedirs
from event import Event

class Accuracy():
    def __init__(self, data, config, debug=True):
        self.data = data
        self.config = config
        self.debug = debug
        self.targetScores = self.data.getTargetScores()
        self.nonTargetScores = self.data.getNonTargetScores()

    def compAcc(self, threshold):
        '''
        Compute the accuracy measures using:


                                  number of true positives + number of true negatives
        random accuracy= -----------------------------------------------------------------------------
                         number of true positives + false positives + false negatives + true negatives


                            sensitivity + specificity
        balanced accuracy = -------------------------- =
                                        2

                                 0.5 * true positives                   0.5 * true negatives
                           --------------------------------  +  ----------------------------------
                           true positives + false negatives      true negatives + false positives

        Do this for a range of thresholds.

        :param threshold:
        :return: float: accuracy in %
        '''
        acc = None
        nrTruePositives = 0
        nrFalseNegatives = 0
        nrFalsePositives = 0
        nrTrueNegatives = 0

        lt = self.data._compLen(self.targetScores)
        if lt > 0:
            for k in self.targetScores.keys():
                for s in self.targetScores[k]:
                    if float(s) >= threshold:
                        nrTruePositives += 1
                    else:
                        nrFalseNegatives +=1
        ln = self.data._compLen(self.nonTargetScores)
        if ln > 0:
            for k in self.nonTargetScores.keys():
                for s in self.nonTargetScores[k]:
                    if float(s) <= threshold:
                        nrTrueNegatives += 1
                    else:
                        nrFalsePositives += 1
        randomAcc = float(nrTruePositives + nrTrueNegatives) / float(lt + ln)

        balancedAcc = 0.5 * nrTruePositives / (nrTruePositives + nrFalseNegatives) + \
                       0.5 * nrTrueNegatives / (nrTrueNegatives + nrFalsePositives)

        return 100 * randomAcc, 100 * balancedAcc


    def plot(self):
        '''
        Compute statistics to plot the random accuracy versus the score threshold.

        :return:
        '''
        print 'Computing Accuracy, this may take a moment (or two)...'
        self.plotType = "accuracy_plot"
        x = []
        yAcc = []
        yBacc = []
        threshold = self.data.getMin()
        # Range of the scores in 100 steps.
        increment = (float(self.data.getMax()) - self.data.getMin()) / self.config.getNrAccPoints()
        while threshold <= float(self.data.getMax()):
            accuracy, balancedAccuracy = self.compAcc(threshold)
            yAcc.append(accuracy)
            yBacc.append(balancedAccuracy)
            x.append(threshold)
            threshold += increment
        self.fig = plt.figure()
        self.event = Event(self.config, self.fig, self.data.getTitle(), self.plotType, self.debug)
        # For saving the pic we use a generic event object
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        axes = self.fig.add_subplot(111)
        pAcc, = axes.plot(x, yAcc, 's-', color='green')
        pBacc, = axes.plot(x, yBacc, 'o-', color='red')
        plt.legend([pAcc, pBacc], ['random accuracy', 'balanced accuracy'])
        axes.set_xlim(0, self.data.getMax())
        axes.set_ylim(0, 100)
        axes.set_title("Accuracy vs Threshold for '%s'" % self.data.getTitle())
        lt = self.data._compLen(self.targetScores)
        ln = self.data._compLen(self.nonTargetScores)
        plt.xlabel("Threshold (#t: %d, #nt: %d)" % (lt, ln))
        plt.ylabel('Accuracy')
        accuracyAtDefault, balancedAccuracyAtDefault = self.compAcc(self.data.getDefaultThreshold())
        axes.annotate("t=%0.2f, random acc=%0.2f%s" % (self.data.getDefaultThreshold(), accuracyAtDefault, '%'),
                      xy=(self.data.getDefaultThreshold(), accuracyAtDefault), xycoords='data',
                      xytext=(self.data.getDefaultThreshold(), accuracyAtDefault - 10), textcoords='data',
                      arrowprops=dict(arrowstyle='->', connectionstyle="arc3"), )
        axes.annotate("t=%0.2f, balanced acc=%0.2f%s" % (self.data.getDefaultThreshold(), balancedAccuracyAtDefault, '%'),
                      xy=(self.data.getDefaultThreshold(), balancedAccuracyAtDefault), xycoords='data',
                      xytext=(self.data.getDefaultThreshold(), balancedAccuracyAtDefault - 10), textcoords='data',
                      arrowprops=dict(arrowstyle='->', connectionstyle="arc3"), )
        plt.grid()
        plt.show()