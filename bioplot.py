#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''

    bioplot.py

    Main program demonstrating several plots that can be used
    when evaluating the performance of a biometric system.


    Copyright (C) 2014, 2015 Jos Bouten ( josbouten at gmail dot com )

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
import argparse
from sys import exit, argv

from config import Config
from data import Data
from alexanderzoo import AlexanderZoo
from boutenzoo import BoutenZoo
from det import Det
from eer import Eer
from tippett import Tippett
from histogram import Histogram
from accuracy import Accuracy
from ranking import Ranking
from roc import Roc
from matrix import MatrixPlot
from version import Version
from utils import sanitize
from license import License


def printConfig(theseOptions, thisConfig):
    if thisConfig.getFileNotFound():
        print "Config info taken from 'default values':\n%s" % thisConfig.toString()
    else:
        if theseOptions.configFilename:
            print "Config info as read from '%s':\n%s" % (theseOptions.configFilename, thisConfig.toString())
        else:
            print "Config info taken from 'default values':\n%s" % thisConfig.toString()


#
#  Main
#

v = Version()
version = v.getVersion()

parser = argparse.ArgumentParser(description="%s [plot type] [<label1> <label2> <label3> ...]\n\
bioplot.py version %s, Copyright (C) 2014, 2015, 2016 Jos Bouten\n\
This program comes with ABSOLUTELY NO WARRANTY; for details run `bioplot.py -l\'.\n\
This is free software, and you are welcome to redistribute it\n\
under certain conditions; type `bioplot.py -l\' for details.\n\
This program was written by Jos Bouten.\n\
You can contact me via josbouten at gmail dot com." % (argv[0], version),
                               version="This is bioplot.py version %s, Copyright (C) 2014, 2015 Jos Bouten" % version, )
parser.add_argument('-Z', '--zoo', action="store_true", dest="plotZoo", help="show zoo plot")
parser.add_argument('-A', '--accuracy', action="store_true", dest="plotAccuracy", help="show accuracy plot")
parser.add_argument('-D', '--det', action="store_true", dest="plotDet", help="show Det plot")
parser.add_argument('-E', '--eer', action="store_true", dest="plotEer", help="show EER plot")
parser.add_argument('-T', '--tippet', action="store_true", dest="plotTippet", help="show Tippett plot")
parser.add_argument('-M', '--matrix', action="store_true", dest="plotMatrix", help="show matrix plot")
parser.add_argument('-O', '--roc', action="store_true", dest="plotRoc", help="show roc plot")
parser.add_argument('-R', '--ranking', action="store_true", dest="plotRanking", help="show ranking plot")
parser.add_argument('-C', '--histogramc', action="store_true", dest="plotHistCum", help="show cumulative histogram")
parser.add_argument('-H', '--histogram', action="store_true", dest="plotHist", help="show histogram")
parser.add_argument('-k', '--kernel', action="store_true", dest="plotKernel", help="show kernel estimate in histogram")
parser.add_argument('-e', '--exp', action="store", dest="expName", default='test',
                  help="name of experiment used in plot title, default = test")
parser.add_argument('-i', '--inputfile', action="store", dest="filename", default='input/testdata_A.txt',
                  help="filename of data file, default = input/testdata_A.txt")
parser.add_argument('-t', '--type', action="store", dest="dataType", default='type3',
                  help="type of data, default = type3, use 'database' if you want to read data from a database.")
parser.add_argument('-d', '--threshold', action="store", dest="threshold", type=float, default=0.7,
                  help="system threshold for ranking plot, default = 0.7")
parser.add_argument('-c', '--config', action="store", dest="configFilename", default='bioplot.cfg',
                  help="use alternative config file")
parser.add_argument('-l', '--license', action="store_true", dest="showLicense", help="show license")
parser.add_argument('-s', '--settings', action="store_true", dest="showOptions", help="show settings only")
parser.add_argument('-q', '--quiet', action="store_true", dest="quiet", help="do not show settings")
options = parser.parse_args()

# Let's handle any request for the license first.
# We stop the program after that.
if options.showLicense:
    l = License('LICENSE.txt')
    l.showLicense()
    exit(0)

print "bioplot.py version %s, Copyright (C) 2014, 2015, 2016 Jos Bouten" % version

# Name of the experiment, used as _title in plots.
expName = options.expName

# We do not like spaces!
filename = sanitize(options.filename)
# filename = options.filename
dataType = options.dataType

# Threshold used by biometric system to make a decision
# only of interest if you want to plot the systems Accuracy.
threshold = options.threshold

config = Config(options.configFilename)

debug = config.getDebug()

if options.quiet:
    config.setShowConfigInfo(False)

if options.showOptions:
    print "Ignoring all command line parameters except -s"
    printConfig(options, config)
    exit(1)

if config.getShowConfigInfo():
    printConfig(options, config)

print "Reading data from '%s'." % options.filename

data = Data(config, expName, threshold, dataType, debug, filename)

if config.getSaveScores():
    # Write data to text files sorted by meta values.
    data.writeScores2file(data.getTargetScores(), expName, '_target.txt')
    data.writeScores2file(data.getNonTargetScores(), expName, '_non_target.txt')

if len(remainder) > 0:
    data.setLabelsToShowAlways(remainder)


if options.plotAccuracy:
    accuracy = Accuracy(data, config, debug)
    accuracy.plot()

if options.plotDet:
    det = Det(data, config, debug)
    det.plot()

if options.plotEer:
    eer = Eer(data, config, debug)
    eer.plot()

if options.plotHistCum:
    # Interested in EER plot? Then plot a cumulative histogram of the scores.
    # More crude than eer.plot and not differentiating between meta values.
    histogram = Histogram(data, config, 'cumulative', debug)
    histogram.plot()

if options.plotHist:
    # Show histogram for data split by meta data value.
    useMeta = True
    if options.plotKernel:
        # Add all target and non target data together, i.e. do not use meta data label info.
        useMeta = False
    histogram = Histogram(data, config, 'normal', debug, useMeta)
    histogram.plot()


if options.plotMatrix:
    matrix = MatrixPlot(data, config, debug)
    matrix.plot()

if options.plotRanking:
    ranking = Ranking(data, config, debug)
    ranking.plot()

if options.plotRoc:
    roc = Roc(data, config, debug)
    roc.plot()

if options.plotTippet:
    tippet = Tippett(data, config, debug)
    tippet.plot()

if options.plotZoo:
    if config.getBoutenStyle() is True:
        zoo = BoutenZoo(data, config, debug)
        zoo.plot()
    else:
        zoo = AlexanderZoo(data, config, debug)
        zoo.plot()
