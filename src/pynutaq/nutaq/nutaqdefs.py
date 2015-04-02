#!/usr/bin/env python

###############################################################################
#     Set of constants to be used by the nutaq device servers
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

""" This module contains a set of constants used by the device servers.
"""

__author__ = 'antmil'

__docformat__ = 'restructuredtext'

# Addresses for settings
PHASE_SHIFT_CAV_ADDRESS = 2
PHASE_SHIFT_FW_CAV_ADDRESS = 3
PHASE_SHIFT_FW_TET1_ADDRESS = 4
AMP_REF_IN_ADDRESS = 19
PHASE_REF_IN_ADDRESS = 20
LOOP_ENABLE_ADDRESS = 100
LOOP_INPUT_SELECTION_ADDRESS = 112
TUNING_ENABLE_ADDRESS = 300
NUM_STEPS_ADDRESS = 302
PHASE_OFFSET_ADDRESS = 304
MOVE_ADDRESS = 305
MOVE_UP_ADDRESS = 306
TUNING_RESET_ADDRESS = 307

# Addresses for diagnostics
ICAV_LOOPS_ADDRESS = 0
QCAV_LOOPS_ADDRESS = 1
ICONTROL_ADDRESS = 2
QCONTROL_ADDRESS = 3
IERROR_ADDRESS = 8
QERROR_ADDRESS = 9
IFW_CAV_LOOPS_ADDRESS = 14
QFW_CAV_LOOPS_ADDRESS = 15
IFW_TET1_LOOPS_ADDRESS = 16
QFW_TET1_LOOPS_ADDRESS = 17
ISPARE_ADDRESS = 24
QSPARE_ADDRESS = 25
AMP_CAV_ADDRESS = 38
AMP_FW_ADDRESS = 39
ANG_CAV_FW_ADDRESS = 40
ANG_CAV_L_ADDRESS = 41
ANG_FW_L_ADDRESS = 42
