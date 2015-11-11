# This code was taken from http://www.tabularasa-euproject.org/
# It is published under the GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007

# The code was integrated in bioplot by Objectifying the code.
#  


# !/usr/bin/env python
# Andre Anjos <andre.anjos@idiap.ch>
# Wed 11 May 2011 09:16:39 CEST 

"""The ScoreToolKit (or simpy "stk") provides functionality to load TABULA
RASA conformant score files, for either plotting DET curves or for the
validation of multi-file score matching.
"""

import math
import numpy as np
import matplotlib.pyplot as plt

class Det:
    def __init__(self, thisData, thisConfig, thisDebug):
        self._debug = thisDebug
        self.data = thisData
        self.config = thisConfig
        self.debug = thisDebug
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

    def load_file(self, filename, no_labels=False):
        """Loads a score set from a single file to memory.
    
        Verifies that all fields are correctly placed and contain valid fields.
    
        Returns a python list of tuples containg the following fields:
    
          [0]
            claimed identity (string)
          [1]
            model label (string)
          [2]
            real identity (string)
          [3]
            test label (string)
          [4]
            score (float)
        """
        retval = []
        for i, l in enumerate(open(filename, 'rt')):
            s = l.strip()
            if len(s) == 0 or s[0] == '#': continue  # empty or comment
            field = [k.strip() for k in s.split()]
            if len(field) != 5:
                raise SyntaxError, 'Line %d of file "%s" is invalid: %s' % \
                                   (i, filename, l)
            try:
                score = float(field[4])
                if no_labels:  # only useful for plotting
                    t = (field[0], None, field[2], None, score)
                else:
                    t = (field[0], field[1], field[2], field[3], score)
                retval.append(t)
            except:
                raise SyntaxError, 'Cannot convert score to float at line %d of file "%s": %s' % (i, filename, l)

        return retval

    def _farfrr(self, negatives, positives, threshold):
        """
        Calculates the FAR and FRR for a given set of positives and negatives and
        a threshold
        """
        far = len(negatives[negatives >= threshold]) / float(len(negatives))
        frr = len(positives[positives < threshold]) / float(len(positives))
        # print threshold, far, frr
        return (far, frr)

    def _evalROC(self, negatives, positives, points):
        """Evaluates the ROC curve.
    
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
            if r <= 0.0: raise RuntimeError, 'ERROR Found r = %g\n' % r
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

    # def plot(self, negatives, positives, points=100, limits=None, title='DET Curve', labels=None, colour=False):

    def plot(self):
        negatives = np.array([k for k in self.data.getNonTargetScoreValues()], dtype='float64')
        positives = np.array([k for k in self.data.getTargetScoreValues()], dtype='float64')
        points = 100
        limits = None
        title = 'DET plot'
        labels = None
        colour = False
        self.plotDet(negatives, positives, points, limits, title, labels, colour)

    def plotDet(self, negatives, positives, points, limits, title, labels, colour):

        """
        Plots Detection Error Trade-off (DET) curve
    
        Keyword parameters:
    
          positives
            np.array of positive class scores in float64 format
    
          negatives
            np.array of negative class scores in float64 format
    
          points
            an (optional) number of points to use for the plot. Defaults to 100.
    
          limits
            an (optional) tuple containing 4 elements that determine the maximum and
            minimum values to plot. Values have to exist in the internal
            desiredLabels variable.
    
          title
            an (optional) string containg a title to be inprinted on the top of the
            plot
    
          labels
            an (optional) list of labels for a legend. If None or empty, the legend
            is suppressed
    
          colour
            flag determining if the plot is coloured or monochrome. By default we
            plot in monochrome scale.
        """

        figure = plt.gcf()
        figure.set_figheight(figure.get_figheight() * 1.3)

        desiredTicks = ["0.00001", "0.00002", "0.00005", "0.0001", "0.0002", "0.0005", "0.001", "0.002", "0.005",
                        "0.01",
                        "0.02", "0.05", "0.1", "0.2", "0.4", "0.6", "0.8", "0.9", "0.95", "0.98", "0.99", "0.995",
                        "0.998",
                        "0.999", "0.9995", "0.9998", "0.9999", "0.99995", "0.99998", "0.99999"]

        desiredLabels = ["0.001", "0.002", "0.005", "0.01", "0.02", "0.05", "0.1", "0.2", "0.5", "1", "2", "5", "10",
                         "20", "40", "60", "80", "90", "95", "98", "99", "99.5", "99.8", "99.9", "99.95", "99.98",
                         "99.99", "99.995", "99.998", "99.999"]

        # Available styles: please note that we plot up to the number of styles
        # available. So, for coloured plots, we can go up to 6 lines in a single
        # plot. For grayscaled ones, up to 12. If you need more plots just extend the
        # list bellow.

        colourStyle = [
            ((0, 0, 0), '-', 1),  # black
            ((0, 0, 1.0), '--', 1),  # blue
            ((0.8, 0.0, 0.0), '-.', 1),  # red
            ((0, 0.6, 0.0), ':', 1),  # green
            ((0.5, 0.0, 0.5), '-', 1),  # magenta
            ((0.3, 0.3, 0.0), '--', 1),  # orange
        ]

        grayStyle = [
            ((0, 0, 0), '-', 1),  # black
            ((0, 0, 0), '--', 1),  # black
            ((0, 0, 0), '-.', 1),  # black
            ((0, 0, 0), ':', 1),  # black
            ((0.3, 0.3, 0.3), '-', 1),  # gray
            ((0.3, 0.3, 0.3), '--', 1),  # gray
            ((0.3, 0.3, 0.3), '-.', 1),  # gray
            ((0.3, 0.3, 0.3), ':', 1),  # gray
            ((0.6, 0.6, 0.6), '-', 2),  # lighter gray
            ((0.6, 0.6, 0.6), '--', 2),  # lighter gray
            ((0.6, 0.6, 0.6), '-.', 2),  # lighter gray
            ((0.6, 0.6, 0.6), ':', 2),  # lighter gray
        ]

        if not limits: limits = ('0.001', '99.999', '0.001', '99.999')

        # check limits
        for k in limits:
            if k not in desiredLabels:
                raise SyntaxError, \
                    'Unsupported limit %s. Please use one of %s' % (k, desiredLabels)

        if colour:
            style = colourStyle
        else:
            style = grayStyle

        if labels:
            for neg, pos, lab, sty in zip(negatives, positives, labels, style):
                ppfar, ppfrr = self._evalDET(neg, pos, points)
                plt.plot(ppfrr, ppfar, label=lab, color=sty[0], linestyle=sty[1], linewidth=sty[2])

        else:
            for neg, pos, sty in zip(negatives, positives, style):
                ppfar, ppfrr = self._evalDET(neg, pos, points)
                plt.plot(ppfrr, ppfar, color=sty[0], linestyle=sty[1], linewidth=sty[2])

        # if labels:
        #     ppfar, ppfrr = self._evalDET(negatives, positives, points)
        #     plt.plot(ppfrr, ppfar, label=labels, color=style[0], linestyle=style[1], linewidth=style[2])
        # else:
        #     ppfar, ppfrr = self._evalDET(negatives, positives, points)
        #     plt.plot(ppfrr, ppfar, color=style[0], linestyle=style[1], linewidth=style[2])

        fr_minIndex = desiredLabels.index(limits[0])
        fr_maxIndex = desiredLabels.index(limits[1])
        fa_minIndex = desiredLabels.index(limits[2])
        fa_maxIndex = desiredLabels.index(limits[3])

        # Convert into DET scale
        pticks = [self.__ppndf__(float(v)) for v in desiredTicks]

        ax = plt.gca()

        plt.axis([pticks[fr_minIndex], pticks[fr_maxIndex],
                 pticks[fa_minIndex], pticks[fa_maxIndex]])

        ax.set_xticks(pticks[fr_minIndex:fr_maxIndex])
        ax.set_xticklabels(desiredLabels[fr_minIndex:fr_maxIndex], size='x-small', rotation='vertical')
        ax.set_yticks(pticks[fa_minIndex:fa_maxIndex])
        ax.set_yticklabels(desiredLabels[fa_minIndex:fa_maxIndex], size='x-small')

        if title: plt.title(title)
        plt.grid(True)
        plt.xlabel('False Rejection Rate [in %]')
        plt.ylabel('False Acceptance Rate [in %]')

        if labels: plt.legend()

        plt.plot()
        plt.show()

def split_it(data):
    """
    Splits the input tuple list (as returned by load_file()) into positives
    and negative scores.

    Returns 2 np arrays as a tuple with (negatives, positives)
    """
    return (np.array([k[4] for k in data if k[0] != k[2]], dtype='float64'),
            np.array([k[4] for k in data if k[0] == k[2]], dtype='float64'))

if __name__ == '__main__':
    # get negatives and positive scores
    negatives = []
    positives = []
    debug = True
    det = Det(None, None, debug)
    filename = 'input/det_testdata_A.txt'
    print("Loading score file %s..." % filename)
    neg, pos = split_it(det.load_file(filename, no_labels=True))
    negatives.append(neg)
    positives.append(pos)
    points = 100
    limits = None
    labels = 'condition A'
    colour = False
    title = 'condition A'
    det.plotDet(negatives, positives, points, limits, title, labels, colour)