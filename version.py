
__author__ = 'drs. ing. Jos Bouten'

'''

    version.py

    Object which contains the version number of the program.

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

class Version():
    def __init__(self, thisDebug=False):
        self.debug = thisDebug

    def getVersion(self):
        '''
        Return the version number of the first version
        description in the changelog.txt file encountered.
        '''
        version = '?'
        try:
            f = open('changelog.txt', 'rt')
        except Exception:
            return version
        else:
            lines = f.readlines()
            f.close()
            for line in lines:
                if '# v' in line:
                    tmp = line.split()
                    versionStr = tmp[1]
                    version = versionStr.replace('v', '')
                    break
        return version
