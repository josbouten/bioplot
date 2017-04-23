"""

    listutils.py

    A set of utility functions for lists containing numbers.

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


def findIndex2EqualOrBigger(li, value):
    return [i for (i, val) in enumerate(li) if val >= value]


def findEqual(li1, li2):
    ret = []
    cnt = 0
    for el1, el2 in zip(li1, li2):
        if el1 == el2:
            ret.append(cnt)
        cnt += 1
    return ret


def findIndex2Bigger(li, value):
    return [i for (i, val) in enumerate(li) if val > value]


def findElementsBiggerInList(li1, li2):
    ret = []
    cnt = 0
    for el1, el2 in zip(li1, li2):
        if el1 > el2:
            ret.append(cnt)
        cnt += 1
    return ret
