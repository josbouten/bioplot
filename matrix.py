__author__ = 'drs. ing. Jos Bouten'

'''

    matrix.py: basic matrix plot routine, will plot a matrix of
    scores in grey values for each meta data value.

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
from collections import Counter, defaultdict
from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

from format import Format
from config import Config
from event import Event

class MatrixPlot(Format):
    def __init__(self, thisData, thisConfig, thisExpName, thisDebug=True):
        Format.__init__(self, thisDebug)
        self.data = thisData
        self.config = thisConfig
        self._printToFilename = thisExpName
        self.debug = thisDebug
        self.colorMap = plt.get_cmap(self.config.getMatrixColorMap())
        self.SPECIAL_SCORE = 12345
        self.plotType = 'matrix_plot'
        self.title = self.data.getTitle()
        self.event = None

    def _checkCheckerPlot(self, thisNr):
        # if the number has an integer square OR if it is devidable by 2
        # then return true, else false
        if thisNr < 4:
            return False, 0, 0
        thisNr *= 1.0
        x = sqrt(thisNr)
        if int(x) == x:
            return True, int(x), int(x)
        if (thisNr / 2.0) - int(thisNr / 2) == 0:
            return True, 2, int(thisNr / 2)
        return False, 0, 0

    def plot(self):
        # plot content of self.mat (individual matrices are not normalized)
        metaValues = self.data.getMetaDataValues()
        # metaValues e.g. ['metaA', 'metaB']
        nrOfMetaValues = len(metaValues)
        overallMin = self.data.getMaximum4ThisType()
        overallMax = self.data.getMinimum4ThisType()
        cnt = 0
        results = self.data.getResults()
        # results e.g. [{'a_#_metaA': [('a', 2.3), ('a', -3.0), ('a',  1.0), ('b', 2.0), ('b', 0.1)]},
        #               {'b_#_metaA': [('a', 3.0), ('a', -1.0), ('a',  0.4), ('b', 2.0), ('b', 1.1)} ]
        # ...
        #              [{'a_#_metaB': [('a', 2.3), ('a', -3.0), ('a',  1.0), ('b', 2.0), ('b', 0.1)]},
        #               {'b_#_metaB': [('a', 6.0), ('a',  1.0), ('a', -2.1), ('b', 3.0), ('b', 2.2)]},
        #               {'c_#_metaB': [('a', 1.0), ('a',  2.0), ('a', -3.1), ('b', 6.0), ('b', 2.2)]},
        #               { .... } ]
        #
        # Split this in multiple matrices; use the same number of elements per label in these matrices.
        # For metaA this will be:
        #      a    a    a    b    b
        # a  2.3, -3.0, 2.0, 2.0, 0.1
        # b  3.0, -1.0, 0.4, 2.0, 1.1

        # For metaB:
        #     a   a     a    b
        # b 6.0, 1.0, -2.1, 3.0,

        matrixAccu = []
        for metaValue in metaValues:
            labelsAndScores = self.data.getLabelsAndScoresForMetaValue(results, metaValue)
            # results          = [{'a_#_meta1': [('a', 2.3), ('a', -3.0), ('a', 1.3), ('b', 2.0), ('b', 0.1)]},
            #                     {'b_#_meta1': [('a', 1.3), ('a',  2.0), ('a', 0.3), ('b', 1.0), ('b', 1.1)]},
            #                     {'a_#_meta2': [('a', 6.0), ('a',  1.0), ('b', 3.0)]}]
            # labelsAndScores for 'meta1' = [{'a': [('a', 2.3), ('a', -3.0), ('a', 1.3), ('b', 2.0), ('b', 0.1)},
            #                                {'b': [('a', 1.3), ('a',  2.0), ('a', 0.3), ('b', 1.0), ('b', 1.1)}]
            if len(labelsAndScores) > 0:
                matrix, mi, ma, tickLabels = self.mkMatrix(labelsAndScores)
                # if skipCnt > 0:
                #     print "Skipped %d labels for meta value %s: " % (skipCnt, metaValue)
                matrixAccu.append((matrix, metaValue, tickLabels))
                # if self.debug:
                #   print 'metaValue:', metaValue, 'min:', matrix.min(), 'max:', matrix.max()
                overallMin = min(overallMin, mi)
                overallMax = max(overallMax, ma)
        checkerPlotIsPossible, x, y = self._checkCheckerPlot(nrOfMetaValues)
        if self.debug:
            print('plot: check:', checkerPlotIsPossible, self.config.getMinNrScores4MatrixPlot())
        if checkerPlotIsPossible and self.config.getCombineMatrices():
            # Combine all matrices in one square or oblong matrix and plot that.
            (scores, meta, tickLabels) = matrixAccu[0]
            (dim1, dim2) = scores.shape
            bigMatrix = np.zeros((x * dim1, y * dim2))
            title = ''
            cnt = 0
            for ii in range(x):
                for jj in range(y):
                    matrix, metaValue, tickLabels = matrixAccu[cnt]
                    title += metaValue + ' '
                    cnt += 1
                    for i in range(dim1):
                        for j in range(dim2):
                            bigMatrix[i + ii * dim1, j + jj * dim2] = matrix[i, j]
            fig, ax = plt.subplots(1, 1, figsize=(int(5 * nrOfMetaValues / 2.0), 5))
            # nullfmt = NullFormatter()
            # gca().xaxis.set_major_formatter(nullfmt)
            # gca().xaxis.set_minor_formatter(nullfmt)
            pos = np.arange(len(tickLabels))
            plt.xticks(pos, tickLabels, rotation=self.config.getLabelAngle())
            plt.yticks(pos, tickLabels)
            # plt.title("matrix plot for %s" % self.title)
            self.event = Event(self.config, fig, self.title, self.plotType, self.debug)
            fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
            # fig, ax = plt.subplots(1, 1, figsize=(5, 5))

            ax.imshow(bigMatrix, cmap=self.colorMap, alpha=1.0, interpolation='nearest', origin='upper', norm=None,
                      vmin=overallMin, vmax=overallMax, shape=(dim1, nrOfMetaValues * dim2), filternorm=1)
            ax.set_title(title, fontsize=18, color="red")
        else:
            (scores, meta, tickLabels) = matrixAccu[0]
            (dim1, dim2) = scores.shape
            # If the vertical dimension of a matrix is larger than the horizontal one, then
            # the matrices are best visible when plotted next to each other.
            nullfmt = NullFormatter()
            if dim1 >= dim2:
                fig, ax = plt.subplots(1, nrOfMetaValues, squeeze=False, figsize=(5 * nrOfMetaValues, 5))
                # plt.title("matrix plot for %s" % self.title)
                self.event = Event(self.config, fig, self.title, self.plotType, self.debug)
                fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
                plt.subplots_adjust(wspace=0, hspace=0)
                # Plot each matrix individually, but use overallMin, overallMax to normalize them.
                xx = 0
                for (matrix, metaValue, tickLabels) in matrixAccu:
                    if self.debug:
                        print('plot, metaValue:', metaValue, 'minScore:', overallMin, 'maxScore:', overallMax)
                    # Plot matrices in separate figures OR combine all of them in one big square matrix ?
                    im = ax[0, xx].imshow(matrix, cmap=self.colorMap, origin='lower', norm=None, vmin=overallMin,
                                          vmax=overallMax)
                    pos = np.arange(len(tickLabels))
                    # No labels.
                    plt.gca().yaxis.set_major_formatter(nullfmt)
                    plt.gca().yaxis.set_minor_formatter(nullfmt)
                    plt.gca().xaxis.set_major_formatter(nullfmt)
                    plt.gca().xaxis.set_minor_formatter(nullfmt)
                    plt.xticks(pos, tickLabels, rotation=self.config.getLabelAngle())
                    plt.yticks(pos, tickLabels)

                    ax[0, xx].set_title(metaValue, fontsize=18, color="red")
                    xx += 1
                    im.set_interpolation('none')
                    cnt += 1
            else:
                # If the vertical dimension of a matrix is smaller than the horizontal one, then
                # the matrices are best visible when plotted above each other.
                fig, ax = plt.subplots(nrOfMetaValues, 1, squeeze=False, figsize=(5 * nrOfMetaValues, 5))
                pos = np.arange(len(tickLabels))
                plt.yticks(pos, tickLabels)
                plt.xticks(pos, tickLabels, rotation=70)
                # plt.title("matrix plot for %s" % self.title)
                self.event = Event(self.config, fig, self.title, self.plotType, self.debug)
                fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
                plt.subplots_adjust(wspace=0, hspace=0)
                # Plot each matrix individually, but use overallMin, overallMax to normalize them.
                yy = 0
                for (matrix, metaValue, tickLabels) in matrixAccu:
                    if self.debug:
                        print('plot, metaValue:', metaValue, 'minScore:', overallMin, 'maxScore:', overallMax)
                    # Plot matrices in separate figures OR combine all of them in one big square matrix ?
                    im = ax[yy, 0].imshow(matrix, cmap=self.colorMap, origin='lower', norm=None, vmin=overallMin,
                                          vmax=overallMax)
                    # No labels.
                    pos = np.arange(len(tickLabels))
                    plt.xticks(pos, tickLabels, rotation=self.config.getLabelAngle())
                    plt.yticks(pos, tickLabels)
                    nullfmt = NullFormatter()
                    plt.gca().yaxis.set_major_formatter(nullfmt)
                    plt.gca().yaxis.set_minor_formatter(nullfmt)
                    ax[yy, 0].set_title(metaValue, fontsize=18, color="red")
                    yy += 1
                    im.set_interpolation('none')
                    cnt += 1
        if self.config.getPrintToFile():
            filename = "%s%s.%s" % (self._printToFilename, self.plotType, ".png")
            plt.savefig(filename, orientation='landscape', papertype='letter')
        else:
            plt.show()

    def _findMaxNrOccurencesOfLabel2(self, listOfLabelsAndScores):
        labelCounter = Counter()
        for (el, score) in listOfLabelsAndScores:
            labelCounter[el] += 1
        mostFrequentLabel = labelCounter.most_common()[0][0]
        maxNr = labelCounter.most_common()[0][1]
        return maxNr, len(labelCounter), mostFrequentLabel

    def _findMinNrOccurencesOfLabel2(self, listOfLabelsAndScores):
        cnt = 0
        minNr = 1E+99
        keepThisLabel = None
        labelCounter = Counter()
        for (el, score) in listOfLabelsAndScores:
            labelCounter[el] += 1
            if labelCounter[el] < minNr:
                minNr = labelCounter[el]
                keepThisLabel = el
            cnt += 1
        return minNr, cnt, keepThisLabel

    def _countLabels(self, labelsAndScores4Label):
        # Count the number of uniq labels.
        labelCounter = Counter()
        for (label, score) in labelsAndScores4Label:
            labelCounter[label] += 1
        return len(labelCounter.items())

    def mkMatrix(self, labelsAndScores):
        """

        :param labelsAndScores for a given meta value:
            labelsAndScore:

                {'label1-1': [('label2-1', 2.3), ('label2-1', -3.0), ('label2-1', 1.3), ('label2-2', 2.0), ('label2-2', 0.1)],
                 'label1-2': [('label2-1', 1.3), ('label2-1',  2.0), ('label2-1', 0.3), ('label2-2', 1.0), ('label2-2', 1.1)]}

        :return: matrix of label1 vs mean scores per label2 value

        """
        # Some labels may have more scores than others because for some labels possibly
        # no models exist, or because the recognizer could not handle the data.

        maxNrLabels2 = 0

        # Find the max nr of tuples per label2 pattern.
        for label1 in labelsAndScores:
            nrLabels = self._countLabels(labelsAndScores[label1])
            maxNrLabels2 = max(maxNrLabels2, nrLabels)
        hCount = maxNrLabels2
        vCount = len(labelsAndScores.keys())
        matrix = np.zeros((vCount, hCount)) + self.SPECIAL_SCORE
        mi = self.data.getMaximum4ThisType()
        ma = self.data.getMinimum4ThisType()
        overallMi = self.data.getMaximum4ThisType()
        overallMa = self.data.getMinimum4ThisType()
        listOfScoresPerLabel = defaultdict(list)
        meanScores4Label = defaultdict(list)
        i = 0
        tickLabels = []
        for label1 in labelsAndScores:
            j = 0
            listOfScoresPerLabel.clear()
            for (label2, score) in labelsAndScores[label1]:
                listOfScoresPerLabel[label2].append(score)
            for label2 in listOfScoresPerLabel:
                meanScores4Label[label2] = sum(listOfScoresPerLabel[label2]) / len(listOfScoresPerLabel[label2])
                mi = min(mi, meanScores4Label[label2])
                ma = max(ma, meanScores4Label[label2])
                overallMi = min(mi, overallMi)
                overallMa = max(ma, overallMa)
            # Note: not all label1 values have the same number of label2 labels.
            # Iin that case gaps (initial zero values) will remain in the matrix.
            for label2 in listOfScoresPerLabel:
                matrix[i, j] = meanScores4Label[label2]
                j += 1
            i += 1
            tickLabels.append(label1)
        # Now we need to make sure the gaps do not interfere with
        # the gray values the real scores get.
        # So we replace SPECIAL_SCORE with a less conspicuous value.
        # Use np.where to do this more quickly?
        for i in range(vCount):
            for j in range(hCount):
                if matrix[i, j] == self.SPECIAL_SCORE:
                    matrix[i, j] = (overallMa + overallMi) / 2
        return matrix, mi, ma, tickLabels


if __name__ == '__main__':

    from matrixdata import MatrixData

    config = Config('bioplot.cfg')
    config.setMinNrScores4MatrixPlot(3)
    data = MatrixData(config)
    debug = True
    data.makeRandomMatrix(rand=True)
    matrixPlot = MatrixPlot(data, config, debug)
    for nr in range(10):
        print('checker plot is possible:', nr, matrixPlot._checkCheckerPlot(nr))
    matrixPlot.plot()
