#!/usr/bin/env python

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