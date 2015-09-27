__author__ = 'jos'

'''
    AsyncWrite

    Object used write data to a text file in a thread so not to stop
    the output of the gui while writing data.

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

import threading
import sys

class AsyncWrite(threading.Thread):
    def __init__(self, thisFilename, theseScores, thisDebug=True):
        threading.Thread.__init__(self)
        self.filename = thisFilename
        self.scores = theseScores
        self.debug = thisDebug

    def run(self):
        if self.debug:
            print "Writing data to: %s." % self.filename
        try:
            f = open(self.filename, 'w')
            for score in self.scores:
                for el in score:
                    f.write("%s\n" % str(el))
            f.close()
            if self.debug:
                print "Finished writing to: %s." % self.filename
        except IOError, e:
            print e
            sys.exit(1)
