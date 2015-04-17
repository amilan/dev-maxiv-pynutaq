#!/usr/bin/env python

###############################################################################
#     Perseus constanst.
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

"""This module defines a set of perseus constants.
"""

__author__ = 'antmil'

__docformat__ = 'restructuredtext'

PERSEUS_LOOP_IP = '192.168.0.101'
PERSEUS_DIAG_IP = '192.168.0.102'

SETTINGS_WRITE_OFFSET = 0x70000040
SETTINGS_READ_OFFSET = 0x70000044
DIAGNOSTICS_OFFSET = 0x70000048

# Init RAM
RAM_INIT_OFFSET = 0x73000018
RAM_INIT_VALUE = 0x26E82

RAM_TRANSFER_REGISTER = 0x7300002C
RAM_TRANSFER_OVER = 1

#