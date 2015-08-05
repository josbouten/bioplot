#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''

    bioplot.py

    Main program demonstrating several plots that can be used
    when evaluating the performance of a biometric system.


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
import optparse
from sys import exit, argv

from config import Config
from data import Data
from alexanderzoo import AlexanderZoo
from boutenzoo import BoutenZoo
from eer import Eer
from tippett import Tippett
from histogram import Histogram
from accuracy import Accuracy
from ranking import Ranking
from matrix import MatrixPlot
from version import Version
from utils import sanitize, showLicense

def printConfig(theseOptions, thisConfig):
    if thisConfig.getFileNotFound():
        print "Config info taken from default values:\n%s" % thisConfig.toString()
    else:
        if theseOptions.configFilename:
            print "Config info as read from %s:\n%s" % (theseOptions.configFilename, thisConfig.toString())
        else:
            print "Config info taken from default values:\n%s" % thisConfig.toString()

#
#  Main
#

v = Version()
version = v.getVersion()

parser = optparse.OptionParser(usage="%s [options] [option <arg1>] [<label1> <label2> <label3> ...]\n\
bioplot.py version %s, Copyright (C) 2014 Jos Bouten\n\
bioplot.py comes with ABSOLUTELY NO WARRANTY; for details type `bioplot.py -l\'.\n\
This is free software, and you are welcome to redistribute it\n\
under certain conditions; type `bioplot.py -l\' for details.\n\
This program was written by Jos Bouten.\n\
You can contact me via josbouten at gmail dot com." % (argv[0], version),
                               version="This is bioplot.py version %s, Copyright (C) 2014 Jos Bouten" % version, )
parser.add_option('-Z', '--zoo', action="store_true", dest="plotZoo", help="show zoo plot")
parser.add_option('-A', '--accuracy', action="store_true", dest="plotAccuracy", help="show accuracy plot")
parser.add_option('-E', '--eer', action="store_true", dest="plotEer", help="show EER plot")
parser.add_option('-T', '--tippet', action="store_true", dest="plotTippet", help="show Tippett plot")
parser.add_option('-M', '--matrix', action="store_true", dest="plotMatrix", help="show matrix plot")
parser.add_option('-R', '--ranking', action="store_true", dest="plotRanking", help="show ranking plot")
parser.add_option('-C', '--histogramc', action="store_true", dest="plotHistCum", help="show cumulative histogram")
parser.add_option('-H', '--histogram', action="store_true", dest="plotHist", help="show histogram")
parser.add_option('-k', '--kernel', action="store_true", dest="plotKernel", help="show kernel estimate in histogram")
parser.add_option('-e', '--exp', action="store", dest="expName", default='test',
                  help="name of experiment used in plot title, default = test")
parser.add_option('-f', '--filename', action="store", dest="filename", default='input/testdata_A.txt',
                  help="filename of data file, default = input/testdata_A.txt")
parser.add_option('-t', '--type', action="store", dest="dataType", default='type3',
                  help="type of data, default = type3")
parser.add_option('-d', '--threshold', action="store", dest="threshold", type="float", default=0.7,
                  help="system threshold for ranking plot, default = 0.7")
parser.add_option('-c', '--config', action="store", dest="configFilename", help="use alternative config file")
parser.add_option('-l', '--license', action="store_true", dest="showLicense", help="show license")
parser.add_option('-s', '--settings', action="store_true", dest="showOptions", help="show settings only")
parser.add_option('-q', '--quiet', action="store_true", dest="quiet", help="do not show settings")
parser.add_option('-V', action="store_false", dest="showVersion", help="show version info")
options, remainder = parser.parse_args()


# Let's handle any request for the license first.
# We stop the program after that.
if options.showLicense:
    showLicense('LICENSE.txt')
    exit(0)

if options.showVersion:
    print "This is bioplot.py version %s, Copyright (C) 2014 Jos Bouten" % version
    exit(0)

print "bioplot.py version %s, Copyright (C) 2014 Jos Bouten" % version

# Name of the experiment, used as _title in plots.
expName = options.expName

# We do not like spaces!
filename = sanitize(options.filename)
dataType = options.dataType

# Threshold used by biometric system to make a decision
# only of interest if you want to plot the systems Accuracy.
threshold = options.threshold

if options.configFilename:
    config = Config(options.configFilename)
else:
    config = Config()

debug = config.getDebug()

if options.quiet:
    config.setShowConfigInfo(False)

if options.showOptions:
    print "Ignoring all command line parameters except -s"
    printConfig(options, config)
    exit(1)

if config.getShowConfigInfo():
    printConfig(options, config)

data = Data(config, expName, threshold, dataType, debug, filename)

if config.getSaveScores():
    # Write data to text files sorted by meta values.
    data.writeScores2file(data.getTargetScores(), expName, '_target.txt')
    data.writeScores2file(data.getNonTargetScores(), expName, '_non_target.txt')

if len(remainder) > 0:
    data.setLabelsToShowAlways(remainder)

if options.plotZoo:
    if config.getBoutenStyle() is True:
        zoo = BoutenZoo(data, config, debug)
        zoo.plot()
    else:
        zoo = AlexanderZoo(data, config, debug)
        zoo.plot()

if options.plotAccuracy:
    accuracy = Accuracy(data, config, debug)
    accuracy.plot()

if options.plotRanking:
    ranking = Ranking(data, config, debug)
    ranking.plot()

if options.plotEer:
    eer = Eer(data, config, debug)
    eer.plot()

if options.plotTippet:
    tippet = Tippett(data, config, debug)
    tippet.plot()

if options.plotHistCum:
    # Interested in EER plot? Then plot a cumulative histogram of the scores.
    # More crude than eer.plot and not differentiating between meta values.
    histogram = Histogram(data, config, 'cumulative', debug)
    histogram.plot()

if options.plotHist:
    # Show histogram for data split by meta data value
    useMeta = True
    if options.plotKernel:
        # Add all target and non target data together, i.e. do not use meta data label info.
        useMeta = False
    histogram = Histogram(data, config, 'normal', debug, useMeta)
    histogram.plot()

if options.plotMatrix:
    matrix = MatrixPlot(data, config, debug)
    matrix.plot()
