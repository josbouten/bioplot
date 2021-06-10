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
    # Note: the values in li must be sorted in ascending order!
    b = -1
    e = len(li)
    index = (b + e) // 2
    index_old = index + 1
    while index != index_old:
        if value <= li[index]:
            e = index
            index_old = index
        else:
            b = index
            index_old = index
        index = (b + e) // 2
    return list(range(index + 1, len(li)))


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


if __name__ == '__main__':
    #
    # Some test code.
    #
    thisList = [-4.3, -5, -6, -7, 0, 11, 12, 14, 15, 16, 18, 19, 22, 33, 44, 55, 66, 77, 86]
    ret = findIndex2EqualOrBigger(thisList, 5)
    print(type(ret))
    print(5, ret)
    ret = findIndex2EqualOrBigger(thisList, -3)
    print(type(ret))
    print(22, ret)
    ret = findIndex2EqualOrBigger(thisList, 90)
    print(type(ret))
    print(90, ret)

