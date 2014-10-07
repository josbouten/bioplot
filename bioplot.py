#!/usr/bin/env python2.7

__author__ = 'drs. ing. Jos Bouten'

'''

    bioplot.py

    Main program demonstrating several plots that can be used
    when evaluating the performance of a biometric system.


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
from config import Config
import optparse

from data import Data

from alexanderzoo import AlexanderZoo
from boutenzoo import BoutenZoo
from histogram import Histogram
from accuracy import Accuracy
from rankingnew import Ranking
from version import Version
from utils import sanitize, showLicense
from sys import exit, argv

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
You can contact me via josbouten at gmail dot com." % (argv[0], version), version='1.0',)
parser.add_option('-Z', '--zoo', action="store_true", dest="plotZoo", help="show zoo plot")
parser.add_option('-A', '--accuracy', action="store_true", dest="plotAccuracy", help="show accuracy plot")
parser.add_option('-R', '--ranking', action="store_true", dest="plotRanking", help="show ranking plot")
parser.add_option('-C', '--histogramc', action="store_true", dest="plotHistCum", help="show cumulative histogram")
parser.add_option('-H', '--histogram', action="store_true", dest="plotHist", help="show histogram")
parser.add_option('-e', '--exp', action="store", dest="expName", default='test', help="name of experiment used in plot title, default = test")
parser.add_option('-f', '--filename', action="store", dest="filename", default='input/testdata_A.txt', help="filename of data file, default = testdata_A.txt")
parser.add_option('-t', '--type', action="store", dest="dataType", default='type3', help="type of data, default = type3")
parser.add_option('-d', '--threshold', action="store", dest="threshold", type="float", default=0.7, help="system threshold for ranking plot, default = 0.7")
parser.add_option('-l', '--license', action="store_true", dest="showLicense", help="show license")
options, remainder = parser.parse_args()


# Let's handle any request for the license first.
# We stop the program after that.
if options.showLicense:
    showLicense('LICENSE.txt')
    exit(0)

print "bioplot.py version %s, Copyright (C) 2014 Jos Bouten" % version

# Name of the experiment, used as title in plots.
expName = options.expName

# We do not like spaces!
filename = sanitize(options.filename)
dataType = options.dataType

# Threshold used by biometric system to make a decision
# only of interest if you want to plot the systems Accuracy.
threshold = options.threshold

config = Config()
debug = config.getDebug()

data = Data(config, expName, threshold, dataType, debug, filename)
data.writeScores2file(data.getTargetScores(), expName + '_target.txt')
data.writeScores2file(data.getNonTargetScores(), expName + '_non_target.txt')

if len(remainder) > 0:
    data.setLabelsToShowAlways(remainder)

if options.plotZoo:
    if config.getBoutenStyle() == True:
       zoo = BoutenZoo(data, config, debug)
       zoo.plotZoo()
    else:
       zoo = AlexanderZoo(data, config, debug)
       zoo.plotZoo()

if options.plotAccuracy:
    accuracy = Accuracy(data, config, debug)
    accuracy.plotAccuracy()

if options.plotRanking:
    ranking = Ranking(data, config, debug)
    ranking.plotRanking()

if options.plotHistCum:
    # Interested in EER, then plot a cumulative histogram of the scores.
    histo = Histogram(data, config, 'cumulative', debug)
    histo.plotHistogram()

if options.plotHist:
    histo = Histogram(data, config, 'normal', debug, useMeta=True)
    histo.plotHistogram()
