'''

    legendtext.py

    Class used to create text used in a plot's legend.

    Copyright (C) 2017 Jos Bouten ( josbouten at gmail dot com )

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

from collections import defaultdict


class LegendText:
    def __init__(self, thisData, thisCllrObject, theseColors, thisConfig, thisShowCllr, thisShowMinCllr, thisShowEer, thisShowCounts,
                 thisEerValue, thisDebug=False):
        '''
        
        :param thisData: object: 
        :param theseColors: list of dicts: color values for meta data
        :param thisConfig: object: config values
        :param thisShowCllr: boolean: 
        :param thisShowMinCllr:  boolean:
        :param thisShowEer: boolean:
        :param thisShowCounts:  boolean:
        :param thisEerValue: float: eer value 
        :param thisScore: float: score at which eer lies
        :param thisDebug: boolean: when true 
        '''
        self._data = thisData
        self._cllrObject = thisCllrObject
        self._colors = theseColors
        self._config = thisConfig
        self._showCllr = thisShowCllr
        self._showMinCllr = thisShowMinCllr
        self._showEer = thisShowEer
        self._showCounts = thisShowCounts
        self._eerValue = thisEerValue
        self._debug = thisDebug

    # getShowCllr, getShowMinCllr, getShowEer

    def make(self):
        legendText = defaultdict(list)
        # Compute and show the Cllr value if so desired.
        if self._showCllr:
            cllrData = self._cllrObject.getCllr()
            if self._debug:
                print(cllrData)
            for thisMetaValue in sorted(self._colors.keys()):
                for metaValue, cllrValue in cllrData:
                    if thisMetaValue == metaValue:
                        if type(cllrValue) is float:
                            cllrStr = "Cllr: %.3f" % cllrValue
                        else:
                            cllrStr = "Cllr: %s" % cllrValue
                        legendText[metaValue].append(cllrStr)
                        break

        # Compute and show the CllrMin value if so desired.
        if self._showMinCllr:
            minCllrData = self._cllrObject.getMinCllr()
            if self._debug:
                print("minCllrData:", minCllrData)
            for thisMetaValue in sorted(self._colors.keys()):
                for metaValue, minCllrValue in minCllrData:
                    if thisMetaValue == metaValue:
                        if type(minCllrValue) is float:
                            minCllrStr = "minCllr: %.3f" % minCllrValue
                        else:
                            minCllrStr = "minCllr: %s" % minCllrValue
                        legendText[metaValue].append(minCllrStr)
                        break

        # Compute and show the EER value if so desired.
        if self._showEer:
            cllrData = self._cllrObject.getCllr()
            for thisMetaValue in sorted(self._colors.keys()):
                for metaValue, x in cllrData:
                    if len(self._eerValue) > 0:
                        if thisMetaValue == metaValue:
                            if self._eerValue[metaValue] < 10.0:
                                eerStr = "Eer:  %.2f%s" % (self._eerValue[metaValue] * 100, '%')
                            else:
                                eerStr = "Eer: %2.2f%s" % (self._eerValue[metaValue] * 100, '%')
                            legendText[metaValue].append(eerStr)
                            break
                    else:
                        break

        if self._showCounts:
            if self._debug:
                print("Show target and non target counts in legend")
            for thisMetaValue in sorted(self._colors.keys()):
                nrT = len(self._data.getTargetScores4MetaValue(thisMetaValue))
                nrNt = len(self._data.getNonTargetScores4MetaValue(thisMetaValue))
                countStr = "#t: %d, #nt: %d" % (nrT, nrNt)
                legendText[thisMetaValue].append(countStr)

        for metaValue in self._data.getMetaDataValues():
            legendText[metaValue] = self._makeLegendText(legendText[metaValue], metaValue)
        return legendText

    def half(self, thisLegendText):
        # if more than 3 semicolons in the text, then split it up.
        tmp = thisLegendText.split(':')
        if len(tmp) > 3:
            part1 = ""
            part2 = ""
            tmp = thisLegendText.split(',')
            for i, el in enumerate(tmp):
                if i < 3:
                    part1 += el
                else:
                    part2 += el
            return [part1, part2]
        else:
            ret = []
            ret[0] = thisLegendText
            ret[1] = None
            return ret

    def _makeLegendText(self, legendText, metaValue):
        thisLegendText = '%s, ' % metaValue
        # Compile legend text.
        for el in legendText:
            thisLegendText += el + ', '
            # Remove last comma and space.
        thisLegendText = thisLegendText[:-2]
        return thisLegendText
