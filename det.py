# !/usr/bin/env python

# This code was taken from http://www.tabularasa-euproject.org/
# It is published under the GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007

# Andre Anjos <andre.anjos@idiap.ch>
# Wed 11 May 2011 09:16:39 CEST

# The code was integrated in bioplot by creating a Det object and
# refactoring the code to convert it into fitting methods.

import math
import numpy as np
import matplotlib.pyplot as plt
from utils import assignColors2MetaDataValue
from collections import defaultdict
from cllr import Cllr
from eer import Eer
from probability import Probability
from event import Event

class Det(Probability):
    def __init__(self, thisData, thisConfig, thisExpName, thisDebug):
        self._debug = thisDebug
        self.data = thisData
        self.config = thisConfig
        self._expName = thisExpName
        self._printToFilename = thisExpName
        self.debug = thisDebug
        Probability.__init__(self, self.data, self.config, self.debug)
        self.plotType = 'det_plot'
        self.fig = None
        self.event = None

        # Values required for linear scale => gaussian scale conversion at __ppndf__()
        self.__SPLIT__ = 0.42
        self.__A0__ = 2.5066282388
        self.__A1__ = -18.6150006252
        self.__A2__ = 41.3911977353
        self.__A3__ = -25.4410604963
        self.__B1__ = -8.4735109309
        self.__B2__ = 23.0833674374
        self.__B3__ = -21.0622410182
        self.__B4__ = 3.1308290983
        self.__C0__ = -2.7871893113
        self.__C1__ = -2.2979647913
        self.__C2__ = 4.8501412713
        self.__C3__ = 2.3212127685
        self.__D1__ = 3.5438892476
        self.__D2__ = 1.6370678189
        self.__EPS__ = 2.2204e-16

    def _farfrr(self, negatives, positives, threshold):
        """
        Calculates the FAR and FRR for a given set of positives and negatives and
        a threshold.
        """
        far = len(negatives[negatives >= threshold]) / float(len(negatives))
        frr = len(positives[positives < threshold]) / float(len(positives))
        # print threshold, far, frr
        return (far, frr)

    def _evalROC(self, negatives, positives, points):
        """
        Evaluates the ROC curve.
    
        This method evaluates the ROC curve given a set of positives and negatives,
        returning two np arrays containing the FARs and the FRRs.
        """
        minval = min(min(negatives), min(positives))
        maxval = max(max(negatives), max(positives))
        step = (maxval - minval) / (points - 1)

        rng = np.arange(minval, maxval + step, step)
        points = len(rng)

        far = np.zeros((points,), dtype='float64')
        frr = np.zeros((points,), dtype='float64')

        for i, threshold in enumerate(rng):
            if i < points:
                far[i], frr[i] = self._farfrr(negatives, positives, threshold)
        return far, frr

    def __ppndf__(self, p):
        """
        Converts a linear scale to a "Gaussian" scale
        Method based on the NIST evaluation code (DETware version 2.1).
        """

        if p >= 1.0: p = 1 - self.__EPS__
        if p <= 0.0: p = self.__EPS__
        q = p - 0.5

        if abs(q) <= self.__SPLIT__:
            r = q * q
            retval = q * (((self.__A3__ * r + self.__A2__) * r + self.__A1__) * r + self.__A0__) \
                     / ((((self.__B4__ * r + self.__B3__) * r + self.__B2__) * r + self.__B1__) * r + 1.0)
        else:
            if q > 0.0:
                r = 1.0 - p
            else:
                r = p
            if r <= 0.0: raise(RuntimeError, 'ERROR Found r = %g\n' % r)
            r = math.sqrt((-1.0) * math.log(r))
            retval = (((self.__C3__ * r + self.__C2__) * r + self.__C1__) * r + self.__C0__) \
                     / ((self.__D2__ * r + self.__D1__) * r + 1.0)
            if (q < 0): retval *= -1.0
        return retval

    def _evalDET(self, negatives, positives, points):
        """
        Evaluates the DET curve.
    
        This method evaluates the DET curve given a set of positives and negatives,
        returning two np arrays containing the FARs and the FRRs.
        """

        def __ppndf_array__(arr):
            retval = np.zeros(arr.shape, dtype='float64')
            for i, p in enumerate(arr): retval[i] = self.__ppndf__(p)
            return retval

        far, frr = self._evalROC(negatives, positives, points)
        return (__ppndf_array__(far), __ppndf_array__(frr))

    def _makeLegendText(self, legendText, metaValue):
        thisLegendText = '%s, ' % metaValue
        # Compile legend text.
        for el in legendText[metaValue]:
            thisLegendText += el + ', '
            # Remove last comma and space.
        thisLegendText = thisLegendText[:-2]
        return thisLegendText

    def plot(self):
        self.fig = plt.figure(figsize=(self.config.getPrintToFileWidth(), self.config.getPrintToFileHeight()))
        self.event = Event(self.config, self.fig, self.data.getTitle(), self.plotType, self.debug)
        # For saving the pic we use a generic event object
        self.fig.canvas.mpl_connect('key_press_event', self.event.onEvent)
        axes = self.fig.add_subplot(111)

        metaDataValues = self.data.getMetaDataValues()
        metaColors = self.config.getMetaColors()
        colors = assignColors2MetaDataValue(metaDataValues, metaColors)

        legendText = defaultdict(list)

        # Compute and show the EER value if so desired.
        if self.config.getShowEerInDet():
            eerObject = Eer(self.data, self.config, self._expName, self.debug)
            eerData = eerObject.computeProbabilities(self.eerFunc)
            for thisMetaValue in sorted(colors.keys()):
                for metaValue, PD, PP, X in eerData:
                    if thisMetaValue == metaValue:
                        try:
                            eerValue, score = eerObject.computeEer(PD, PP, X)
                        except Exception as e:
                            print("DrawLegend: problem computing EER for %s: %s" % (thisMetaValue, e))
                        else:
                            eerValue *= 100
                            if eerValue < 10.0:
                                eerStr = "Eer:  %.2f%s" % (eerValue, '%')
                            else:
                                eerStr = "Eer: %2.2f%s" % (eerValue, '%')
                            legendText[thisMetaValue].append(eerStr)
                        break

        # Compute and show the Cllr value if so desired.
        if self.config.getShowCllrInDet():
            cllrObject = Cllr(self.data, self.config, self.debug)
            cllrData = cllrObject.getCllr()
            if self.debug:
                print(cllrData)
            for thisMetaValue in sorted(colors.keys()):
                for metaValue, cllrValue in cllrData:
                    if thisMetaValue == metaValue:
                        if type(cllrValue) is float:
                            cllrStr = "Cllr: %.3f" % cllrValue
                        else:
                            cllrStr = "Cllr: %s" % cllrValue
                        legendText[metaValue].append(cllrStr)
                        break

        # Compute and show the CllrMin value if so desired.
        if self.config.getShowMinCllrInDet():
            cllrObject = Cllr(self.data, self.config, self.debug)
            minCllrData = cllrObject.getMinCllr()
            if self.debug:
                print("minCllrData:", minCllrData)
            for thisMetaValue in sorted(colors.keys()):
                for metaValue, minCllrValue in minCllrData:
                    if thisMetaValue == metaValue:
                        if type(minCllrValue) is float:
                            minCllrStr = "minCllr: %.3f" % minCllrValue
                        else:
                            minCllrStr = "minCllr: %s" % minCllrValue
                        legendText[metaValue].append(minCllrStr)
                        break
        points = 100
        title = 'DET plot'
        figure = plt.gcf()
        figure.set_figheight(figure.get_figheight() * 1.3)

        desiredTicks = ["0.00001", "0.00002", "0.00005", "0.0001", "0.0002", "0.0005", "0.001", "0.002", "0.005",
                        "0.01", "0.02", "0.05", "0.1", "0.2", "0.4", "0.6", "0.8", "0.9", "0.95", "0.98", "0.99", "0.995",
                        "0.998", "0.999", "0.9995", "0.9998", "0.9999", "0.99995", "0.99998", "0.99999"]

        desiredLabels = self.config.getAllowedRates()

        # Available styles: please note that we plot up to the number of styles
        # available. So, for coloured plots, we can go up to 6 lines in a single
        # plot. For gray scaled ones, up to 12. If you need more plots just extend the
        # list bellow.

        limits = ('0.1', str(self.config.getMaxFalseRejectionRate()), '0.1', str(self.config.getMaxFalseAcceptRate()))

        # Check limits.
        for k in limits:
            if k not in desiredLabels:
                raise(SyntaxError, 'Unsupported limit %s. Please use one of %s' % (k, desiredLabels))

        for metaValue in metaDataValues:
            negatives = [np.array([k for k in self.data.getNonTargetScores4MetaValue(metaValue)], dtype='float64')]
            positives = [np.array([k for k in self.data.getTargetScores4MetaValue(metaValue)], dtype='float64')]
            thisLegendText = self._makeLegendText(legendText, metaValue)
            for neg, pos in zip(negatives, positives):
                ppfar, ppfrr = self._evalDET(neg, pos, points)
                #plt.plot(ppfrr, ppfar, label=thisLegendText, color=colors[metaValue])
                plt.plot(ppfar, ppfrr, label=thisLegendText, color=colors[metaValue])


        fr_minIndex = desiredLabels.index(limits[0])
        fr_maxIndex = desiredLabels.index(limits[1])
        fa_minIndex = desiredLabels.index(limits[2])
        fa_maxIndex = desiredLabels.index(limits[3])

        # Convert into DET scale
        pticks = [self.__ppndf__(float(v)) for v in desiredTicks]

        # Plot diagonal line to facilitate reading the EER-value(s) from the plot.
        if self.config.getShowDiagonalInDet():
            plt.plot(pticks, pticks, color='red', lw=1.0, linestyle="-.")

        ax = plt.gca()

        plt.axis([pticks[fa_minIndex], pticks[fa_maxIndex], pticks[fr_minIndex], pticks[fr_maxIndex]])

        ax.set_yticks(pticks[fr_minIndex:fr_maxIndex])
        ax.set_yticklabels(desiredLabels[fr_minIndex:fr_maxIndex], size='x-small', rotation='vertical')
        ax.set_xticks(pticks[fa_minIndex:fa_maxIndex])
        ax.set_xticklabels(desiredLabels[fa_minIndex:fa_maxIndex], size='x-small')
        if title:
            plt.title("DET plot for '" + self.data.getTitle() + "'")
            plt.grid(True)
            plt.ylabel('False Rejection Rate [%]')
            plt.xlabel('False Acceptance Rate [%]')
        plt.legend(loc=1)
        if self.config.getPrintToFile():
            filename = "%s_%s.%s" % (self._printToFilename, self.plotType, "png")
            print("Writing plot to %s" % filename)
            plt.savefig(filename, orientation='landscape', papertype='letter')
        else:
            plt.show()
