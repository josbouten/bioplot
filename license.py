#!/usr/bin/env python

"""
    license.py, class to read and show the license.

    Copyright (C) 2015 Jos Bouten ( josbouten at gmail dot com )

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

"""

import sys


class License:
    def __init__(self, thisFilename, thisDebug=True):
        self.filename = thisFilename
        self.debug = thisDebug

    def showLicense(self):
        try:
            f = open(self.filename, 'rt')
        except Exception, e:
            print e
            print "You should have received a copy of the GNU General Public License along \
                    with this program; if not, write to the Free Software Foundation, Inc., \
                    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA."
            sys.exit(1)
        else:
            lines = f.readlines()
            f.close()
            for line in lines:
                print line.strip()


if __name__ == '__main__':
    l = License('LICENSE.txt')
    l.showLicense()
