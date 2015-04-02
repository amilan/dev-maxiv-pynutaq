#!/usr/bin/env python

###############################################################################
#     Interlocks modules is part of pynutaq device server
#
#     Copyright (C) 2013  Max IV Laboratory, Lund Sweden
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see [http://www.gnu.org/licenses/].
###############################################################################

""" This module manage the interlocks attributes for diagnostics.
"""

__all__ = ["InterlocksDiags"]

__author__ = 'antmil'

__docformat__ = 'restructuredtext'

class InterlocksDiags(object):
    def __init__(self):
        itck_inputs = ['RvTet1', 'RvTet2', 'RvCircIn', 'FwLoad', 'FwHybLoad',
                       'RvCav', 'Arc', 'Vaccum', 'Manual', 'EndSwUp',
                       'EndSwdown', 'MPS']

        itck_outputs = ['DACsOffLoopsStby', 'PinDiodeSwitch', 'FDLTrg',
                        'PLCTxOff', 'MPS', 'Diag']

        self._itck_dict = {}

        for input in itck_inputs:
            for output in itck_outputs:
                self._itck_dict[input][output] = 0

    def get_itck(self, input, output):
        return self._itck_dict[input][output]

    def set_itck(self, input, output, value):
        self._itck_dict[input][output] = value
