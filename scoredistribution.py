import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import matplotlib.pyplot as plt
from event import Event
# from legendtext import LegendText
# from utils import assignColors2MetaDataValue
import numpy as np
from utils import isNumeric, assignColors2MetaDataValue


class ScoreDistribution:
    def __init__(self, data, eer, cllr, config, thisExpName, thisType='normal', debug=False):
        self.data = data
        self._eerObject = eer
        self._cllrObject = cllr
        self.config = config
        self.printToFilename = thisExpName
        self.type = thisType
        self.debug = debug
        self.plotType = "distribution_plot"
        self.fig = None
        self.event = None
        self.colors = None
        self.nrColors = None

    def plotTargetDistribution(self):
        self.fig = plt.figure(figsize=(self.config.getPrintToFileWidth(), self.config.getPrintToFileHeight()))
        self.event = Event(self.config, self.fig, self.data.getTitle(), self.plotType, self.debug)
        # For saving the pic we use a generic event object
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        axes = self.fig.add_subplot(111)
        # metaDataValues = self.data.getMetaDataValues()
        # metaColors = self.config.getMetaColors()
        # colors = assignColors2MetaDataValue(metaDataValues, metaColors)
        # lt = LegendText(self.data, self._cllrObject, colors, self.config, self.config.getShowCllrInDet(),
        #                 self.config.getShowMinCllrInDet(), self.config.getShowEerInDet(),
        #                 self.config.getShowCountsInDet(),
        #                 self._eerObject.eerValue, self._eerObject.eerScore, self.debug)
        # legendText = lt.make()

        lengths = [len(self.data._targetScores4Label[label]) for label in self.data._targetScores4Label]
        yValues = np.arange(len(lengths))
        plt.bar(yValues, lengths, align='center', alpha=0.5)
        plt.legend()
        plt.xticks(yValues, lengths)
        plt.ylabel('Number')
        plt.title('Distribution of labels for {} target'.format(len(self.data.getTargetLabels())))

        if self.config.getPrintToFile():
            filename = "%s_%s_%s.%s" % (self.printToFilename, self.plotType, self.plotType, "png")
            print("Writing plot to %s" % filename)
            plt.savefig(filename, orientation='landscape', papertype='letter')
        else:
            plt.show()

    def autolabel(self, ax, rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    def is_numeric(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def allLabelsAreNumeric(self, labels):
        ret = True
        i = 0
        while i < len(labels):
            if not isNumeric(labels[i]):
                ret = False
                break
            i += 1
        return ret

    def setAxAttributes(self, ax, label, title, xtics, xtickLabels):
        ax.set_ylabel(label)
        ax.set_title(title)
        ax.set_xticks(xtics)
        ax.set_xticklabels(xtickLabels)


    def plotMeta(self):
        fig, ax = plt.subplots(2, 1, figsize=(self.config.getPrintToFileWidth(), self.config.getPrintToFileHeight()))
        self.event = Event(self.config, self.fig, self.data.getTitle(), self.plotType, self.debug)
        # For saving the pic we use a generic event object
        fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        plt.subplots_adjust(wspace=0, hspace=0)

        valueSet = self.data.getMetaDataValues().keys()
        results = self.data.getResults()
        metaColors = self.config.getMetaColors()
        self.colors = assignColors2MetaDataValue(self.data.getMetaDataValues(), metaColors)
        allTargetScores = self.data.getTargetScores()
        allNonTargetScores = self.data.getNonTargetScores()
        self._plot(ax, allTargetScores, allNonTargetScores)

        fig.tight_layout()
        if self.config.getPrintToFile():
            filename = "%s_%s_%s.%s" % (self.printToFilename, self.plotType, self.plotType, "png")
            print("Writing plot to %s" % filename)
            plt.savefig(filename, orientation='landscape', papertype='letter')
        else:
            plt.show()

    def _plot(self, ax, targetLabelsAndScores, nonTargetLabelsAndScores):
        # ToDo: plot numbers in range from their minimum -15% to their maximum +15% for a nice plot.
        # ToDo: split data per experiment/meta label.
        targetLabels = [label for label in targetLabelsAndScores.keys()]
        nonTargetLabels = [label for label in nonTargetLabelsAndScores.keys()]
        targetsAreNumeric = self.allLabelsAreNumeric(targetLabels)
        nonTargetsAreNumeric = self.allLabelsAreNumeric(nonTargetLabels)
        barWidth = 0.35
        #color = self.colors[metaValue]

        if targetsAreNumeric and nonTargetsAreNumeric:
            sortedTargetLabels = sorted(targetLabelsAndScores, key=int)
        else:
            sortedTargetLabels = sorted(targetLabelsAndScores)

        targetCnt = [len(targetLabelsAndScores[label]) for label in
                     sortedTargetLabels]
        nrTargetLabels = np.arange(len(sortedTargetLabels))
        targetRects = ax[0].bar(nrTargetLabels - barWidth / 2, targetCnt, barWidth, label='target')#, color=color)

        if targetsAreNumeric and nonTargetsAreNumeric:
            sortedNonTargetLabels = sorted(nonTargetLabelsAndScores, key=int)
        else:
            sortedNonTargetLabels = sorted(nonTargetLabelsAndScores)

        nonTargetCnt = [len(nonTargetLabelsAndScores[label]) for label in
                        sortedNonTargetLabels]
        nrNonTargetLabels = np.arange(len(sortedNonTargetLabels))
        nonTargetRects = ax[1].bar(nrNonTargetLabels + barWidth / 2, nonTargetCnt, barWidth, label='non target')#, color=color)

        # self.setAxAttributes(ax[0], "nr of tests", "targets", nrTargetLabels, sortedTargetLabels)
        # self.setAxAttributes(ax[1], "nr of tests", "non targets", nrNonTargetLabels, sortedNonTargetLabels)

        self.setAxAttributes(ax[0], "nr of tests", "scores per target, ({} targets)".format(len(nrTargetLabels)),
                             nrTargetLabels, sortedTargetLabels)
        self.setAxAttributes(ax[1], "nr of tests", "scores per non target, ({} non targets)".format(len(nrNonTargetLabels)),
                             nrNonTargetLabels, sortedNonTargetLabels)

        self.autolabel(ax[0], targetRects)
        self.autolabel(ax[1], nonTargetRects)


    def plot(self):
        fig, ax = plt.subplots(2, 1, figsize=(self.config.getPrintToFileWidth(), self.config.getPrintToFileHeight()))
        self.event = Event(self.config, self.fig, self.data.getTitle(), self.plotType, self.debug)
        # For saving the pic we use a generic event object
        fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        plt.subplots_adjust(wspace=0, hspace=0)

        # ToDo: plot numbers in range from their minimum -15% to their maximum +15% for a nice plot.
        # ToDo: split data per experiment/meta label.

        targetLabels = self.data.getTargetLabels()
        nonTargetLabels = self.data.getNonTargetLabels()
        targetsAreNumeric = self.allLabelsAreNumeric(targetLabels)
        nonTargetsAreNumeric = self.allLabelsAreNumeric(nonTargetLabels)
        barWidth = 0.35

        if targetsAreNumeric and nonTargetsAreNumeric:
            sortedTargetLabels = sorted(self.data.getTargetLabels(), key=int)
        else:
            sortedTargetLabels = sorted(self.data.getTargetLabels())

        targetCnt = [len(self.data.getTargetScores4AllLabels()[label]) for label in
                     sortedTargetLabels]
        nrTargetLabels = np.arange(len(sortedTargetLabels))
        targetRects = ax[0].bar(nrTargetLabels - barWidth / 2, targetCnt, barWidth, label='target')

        if targetsAreNumeric and nonTargetsAreNumeric:
            sortedNonTargetLabels = sorted(self.data.getNonTargetLabels(), key=int)
        else:
            sortedNonTargetLabels = sorted(self.data.getNonTargetLabels())

        nonTargetCnt = [len(self.data.getNonTargetScores4AllLabels()[label]) for label in
                        sortedNonTargetLabels]
        nrNonTargetLabels = np.arange(len(sortedNonTargetLabels))
        nonTargetRects = ax[1].bar(nrNonTargetLabels + barWidth / 2, nonTargetCnt, barWidth, label='non target')

        # self.setAxAttributes(ax[0], "nr of tests", "targets", nrTargetLabels, sortedTargetLabels)
        # self.setAxAttributes(ax[1], "nr of tests", "non targets", nrNonTargetLabels, sortedNonTargetLabels)

        self.setAxAttributes(ax[0], "nr of tests", "scores per target, ({} targets)".format(len(nrTargetLabels)), nrTargetLabels, sortedTargetLabels)
        self.setAxAttributes(ax[1], "nr of tests", "scores per non target, ({} targets)".format(len(nrNonTargetLabels)), nrNonTargetLabels, sortedNonTargetLabels)

        self.autolabel(ax[0], targetRects)
        self.autolabel(ax[1], nonTargetRects)
        fig.tight_layout()

        if self.config.getPrintToFile():
            filename = "%s_%s_%s.%s" % (self.printToFilename, self.plotType, self.plotType, "png")
            print("Writing plot to %s" % filename)
            plt.savefig(filename, orientation='landscape', papertype='letter')
        else:
            plt.show()

if __name__ == '__main__':

    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    men_means = [20, 34, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, men_means, width, label='Men')
    rects2 = ax.bar(x + width / 2, women_means, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.show()
