#!/usr/bin/env python

###############################################################################
#     Perseus simulator.
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

"""This module contains the main class for the simulation.
"""

__all__ = ["PerseusSimulated"]

__author__ = 'antmil'

__docformat__ = 'restructuredtext'

from random import randint

MI125_BOARD_NUMBER = 1


class PerseusSimulated(object):

    def __init__(self):
        self.connect()
        print "Init DONE"

    def connect(self):
        print "Connected"

    def write(self, address, value):
        print "Value to write in address %d -> %d" % (address, value)

    def read(self, address):
        return randint(0, 0xFFFFFFFF)
