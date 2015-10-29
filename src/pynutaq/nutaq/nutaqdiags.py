#!/usr/bin/env python

###############################################################################
#     NutaqDiags device server.
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

"""This module contains the Nutaq device server for diagnostics.
"""

__all__ = ["NutaqDiags", "run_device"]

__author__ = 'antmil'

__docformat__ = 'restructuredtext'

# standard library imports
import time
import numpy
import math
import datetime

# 3rd party imports
from PyTango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from PyTango.server import Device, DeviceMeta, attribute, command, run
from PyTango.server import device_property

# local imports
#from pynutaq.nutaqattributes import attributes_dict
from pynutaq.nutaq.nutaqdefs import *

import pynutaq.extra as extra_func

import pynutaq.perseus.perseusutils as perseus_utils

try:
    from pynutaq.perseus.perseusdefs import *
    from pynutaq.perseus.perseusfactory import Perseus
except ImportError, e:
    print e


class NutaqDiags(Device):
    __metaclass__ = DeviceMeta

    Rvtet1A = attribute(label='Rvtet1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Rvtet1A",
                                   fset="set_Rvtet1A",
                                   doc=""
                                   )

    Rvtet1B = attribute(label='Rvtet1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Rvtet1B",
                                   fset="set_Rvtet1B",
                                   doc=""
                                   )

    Rvtet2A = attribute(label='Rvtet2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Rvtet2A",
                                   fset="set_Rvtet2A",
                                   doc=""
                                   )

    Rvtet2B = attribute(label='Rvtet2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Rvtet2B",
                                   fset="set_Rvtet2B",
                                   doc=""
                                   )

    RvcircA = attribute(label='RvcircA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_RvcircA",
                                   fset="set_RvcircA",
                                   doc=""
                                   )

    RvcircB = attribute(label='RvcircB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_RvcircB",
                                   fset="set_RvcircB",
                                   doc=""
                                   )

    FwloadA = attribute(label='FwloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FwloadA",
                                   fset="set_FwloadA",
                                   doc=""
                                   )

    FwloadB = attribute(label='FwloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FwloadB",
                                   fset="set_FwloadB",
                                   doc=""
                                   )

    FwhybloadA = attribute(label='FwhybloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FwhybloadA",
                                   fset="set_FwhybloadA",
                                   doc=""
                                   )

    FwhybloadB = attribute(label='FwhybloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FwhybloadB",
                                   fset="set_FwhybloadB",
                                   doc=""
                                   )

    RvcavA = attribute(label='RvcavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_RvcavA",
                                   fset="set_RvcavA",
                                   doc=""
                                   )

    RvcavB = attribute(label='RvcavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_RvcavB",
                                   fset="set_RvcavB",
                                   doc=""
                                   )

    ManualInterlockA = attribute(label='ManualInterlockA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_ManualInterlockA",
                                   fset="set_ManualInterlockA",
                                   doc=""
                                   )

    ManualInterlockB = attribute(label='ManualInterlockB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_ManualInterlockB",
                                   fset="set_ManualInterlockB",
                                   doc=""
                                   )

    DisableItckRvtet1A = attribute(label='DisableItckRvtet1A',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckRvtet1A",
                                   fset="set_DisableItckRvtet1A",
                                   doc=""
                                   )

    DisableItckRvtet1B = attribute(label='DisableItckRvtet1B',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckRvtet1B",
                                   fset="set_DisableItckRvtet1B",
                                   doc=""
                                   )

    DisableItckRvtet2A = attribute(label='DisableItckRvtet2A',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckRvtet2A",
                                   fset="set_DisableItckRvtet2A",
                                   doc=""
                                   )

    DisableItckRvtet2B = attribute(label='DisableItckRvtet2B',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckRvtet2B",
                                   fset="set_DisableItckRvtet2B",
                                   doc=""
                                   )

    DisableItckRvcircA = attribute(label='DisableItckRvcircA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckRvcircA",
                                   fset="set_DisableItckRvcircA",
                                   doc=""
                                   )

    DisableItckRvcircB = attribute(label='DisableItckRvcircB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckRvcircB",
                                   fset="set_DisableItckRvcircB",
                                   doc=""
                                   )

    DisableItckFwloadA = attribute(label='DisableItckFwloadA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckFwloadA",
                                   fset="set_DisableItckFwloadA",
                                   doc=""
                                   )

    DisableItckFwloadB = attribute(label='DisableItckFwloadB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckFwloadB",
                                   fset="set_DisableItckFwloadB",
                                   doc=""
                                   )

    DisableItckFwhybloadA = attribute(label='DisableItckFwhybloadA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckFwhybloadA",
                                   fset="set_DisableItckFwhybloadA",
                                   doc=""
                                   )

    DisableItckFwhybloadB = attribute(label='DisableItckFwhybloadB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckFwhybloadB",
                                   fset="set_DisableItckFwhybloadB",
                                   doc=""
                                   )

    DisableItckRvcavA = attribute(label='DisableItckRvcavA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckRvcavA",
                                   fset="set_DisableItckRvcavA",
                                   doc=""
                                   )

    DisableItckRvcavB = attribute(label='DisableItckRvcavB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckRvcavB",
                                   fset="set_DisableItckRvcavB",
                                   doc=""
                                   )

    DisableItckArcsA = attribute(label='DisableItckArcsA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckArcsA",
                                   fset="set_DisableItckArcsA",
                                   doc=""
                                   )

    DisableItckArcsB = attribute(label='DisableItckArcsB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckArcsB",
                                   fset="set_DisableItckArcsB",
                                   doc=""
                                   )

    DisableItckVaccumA = attribute(label='DisableItckVaccumA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckVaccumA",
                                   fset="set_DisableItckVaccumA",
                                   doc=""
                                   )

    DisableItckVaccumB = attribute(label='DisableItckVaccumB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckVaccumB",
                                   fset="set_DisableItckVaccumB",
                                   doc=""
                                   )

    DisableItckManualInterlockA = attribute(label='DisableItckManualInterlockA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckManualInterlockA",
                                   fset="set_DisableItckManualInterlockA",
                                   doc=""
                                   )

    DisableItckManualInterlockB = attribute(label='DisableItckManualInterlockB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckManualInterlockB",
                                   fset="set_DisableItckManualInterlockB",
                                   doc=""
                                   )

    DisableItckPlungerEndSwitchesUpA = attribute(label='DisableItckPlungerEndSwitchesUpA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckPlungerEndSwitchesUpA",
                                   fset="set_DisableItckPlungerEndSwitchesUpA",
                                   doc=""
                                   )

    DisableItckPlungerEndSwitchesUpB = attribute(label='DisableItckPlungerEndSwitchesUpB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckPlungerEndSwitchesUpB",
                                   fset="set_DisableItckPlungerEndSwitchesUpB",
                                   doc=""
                                   )

    DisableItckPlungerEndSwitchesDownA = attribute(label='DisableItckPlungerEndSwitchesDownA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckPlungerEndSwitchesDownA",
                                   fset="set_DisableItckPlungerEndSwitchesDownA",
                                   doc=""
                                   )

    DisableItckPlungerEndSwitchesDownB = attribute(label='DisableItckPlungerEndSwitchesDownB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckPlungerEndSwitchesDownB",
                                   fset="set_DisableItckPlungerEndSwitchesDownB",
                                   doc=""
                                   )

    DisableItckMpsA = attribute(label='DisableItckMpsA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckMpsA",
                                   fset="set_DisableItckMpsA",
                                   doc=""
                                   )

    DisableItckMpsB = attribute(label='DisableItckMpsB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_DisableItckMpsB",
                                   fset="set_DisableItckMpsB",
                                   doc=""
                                   )

    SamplesToAverageA = attribute(label='SamplesToAverageA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_SamplesToAverageA",
                                   fset="set_SamplesToAverageA",
                                   doc=""
                                   )

    SamplesToAverageB = attribute(label='SamplesToAverageB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_SamplesToAverageB",
                                   fset="set_SamplesToAverageB",
                                   doc=""
                                   )

    PulseupLogicInversionA = attribute(label='PulseupLogicInversionA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_PulseupLogicInversionA",
                                   fset="set_PulseupLogicInversionA",
                                   doc=""
                                   )

    PulseupLogicInversionB = attribute(label='PulseupLogicInversionB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_PulseupLogicInversionB",
                                   fset="set_PulseupLogicInversionB",
                                   doc=""
                                   )

    EndSwitchesConnectedToNoNcContactA = attribute(label='EndSwitchesConnectedToNoNcContactA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=1,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_EndSwitchesConnectedToNoNcContactA",
                                   fset="set_EndSwitchesConnectedToNoNcContactA",
                                   doc=""
                                   )

    EndSwitchesConnectedToNoNcContactB = attribute(label='EndSwitchesConnectedToNoNcContactB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=1,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_EndSwitchesConnectedToNoNcContactB",
                                   fset="set_EndSwitchesConnectedToNoNcContactB",
                                   doc=""
                                   )

    LookrefA = attribute(label='LookrefA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_LookrefA",
                                   fset="set_LookrefA",
                                   doc=""
                                   )

    LookrefB = attribute(label='LookrefB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_LookrefB",
                                   fset="set_LookrefB",
                                   doc=""
                                   )

    QuadrefA = attribute(label='QuadrefA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_QuadrefA",
                                   fset="set_QuadrefA",
                                   doc=""
                                   )

    QuadrefB = attribute(label='QuadrefB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_QuadrefB",
                                   fset="set_QuadrefB",
                                   doc=""
                                   )

    SpareDo1A = attribute(label='SpareDo1A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareDo1A",
                                   fset="set_SpareDo1A",
                                   doc=""
                                   )

    SpareDo1B = attribute(label='SpareDo1B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareDo1B",
                                   fset="set_SpareDo1B",
                                   doc=""
                                   )

    SpareDo2A = attribute(label='SpareDo2A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareDo2A",
                                   fset="set_SpareDo2A",
                                   doc=""
                                   )

    SpareDo2B = attribute(label='SpareDo2B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareDo2B",
                                   fset="set_SpareDo2B",
                                   doc=""
                                   )

    SpareDo3A = attribute(label='SpareDo3A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareDo3A",
                                   fset="set_SpareDo3A",
                                   doc=""
                                   )

    SpareDo3B = attribute(label='SpareDo3B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareDo3B",
                                   fset="set_SpareDo3B",
                                   doc=""
                                   )

    FdlSwTriggerA = attribute(label='FdlSwTriggerA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_FdlSwTriggerA",
                                   fset="set_FdlSwTriggerA",
                                   doc=""
                                   )

    FdlSwTriggerB = attribute(label='FdlSwTriggerB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_FdlSwTriggerB",
                                   fset="set_FdlSwTriggerB",
                                   doc=""
                                   )

    ResetInterlocksCavA = attribute(label='ResetInterlocksCavA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_ResetInterlocksCavA",
                                   fset="set_ResetInterlocksCavA",
                                   doc=""
                                   )

    ResetInterlocksCavB = attribute(label='ResetInterlocksCavB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_ResetInterlocksCavB",
                                   fset="set_ResetInterlocksCavB",
                                   doc=""
                                   )

    LandautuningenableA = attribute(label='LandautuningenableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_LandautuningenableA",
                                   fset="set_LandautuningenableA",
                                   doc=""
                                   )

    LandautuningenableB = attribute(label='LandautuningenableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_LandautuningenableB",
                                   fset="set_LandautuningenableB",
                                   doc=""
                                   )

    LandautuningresetA = attribute(label='LandautuningresetA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_LandautuningresetA",
                                   fset="set_LandautuningresetA",
                                   doc=""
                                   )

    LandautuningresetB = attribute(label='LandautuningresetB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_LandautuningresetB",
                                   fset="set_LandautuningresetB",
                                   doc=""
                                   )

    MovelandauupA = attribute(label='MovelandauupA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_MovelandauupA",
                                   fset="set_MovelandauupA",
                                   doc=""
                                   )

    MovelandauupB = attribute(label='MovelandauupB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_MovelandauupB",
                                   fset="set_MovelandauupB",
                                   doc=""
                                   )

    MovelandauplgA = attribute(label='MovelandauplgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_MovelandauplgA",
                                   fset="set_MovelandauplgA",
                                   doc=""
                                   )

    MovelandauplgB = attribute(label='MovelandauplgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_MovelandauplgB",
                                   fset="set_MovelandauplgB",
                                   doc=""
                                   )

    NumstepsA = attribute(label='NumstepsA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=10000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_NumstepsA",
                                   fset="set_NumstepsA",
                                   doc=""
                                   )

    NumstepsB = attribute(label='NumstepsB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=10000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_NumstepsB",
                                   fset="set_NumstepsB",
                                   doc=""
                                   )

    LandauphaseoffsetA = attribute(label='LandauphaseoffsetA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=180,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_LandauphaseoffsetA",
                                   fset="set_LandauphaseoffsetA",
                                   doc=""
                                   )

    LandauphaseoffsetB = attribute(label='LandauphaseoffsetB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=180,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_LandauphaseoffsetB",
                                   fset="set_LandauphaseoffsetB",
                                   doc=""
                                   )

    LandaumarginupA = attribute(label='LandaumarginupA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=50,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_LandaumarginupA",
                                   fset="set_LandaumarginupA",
                                   doc=""
                                   )

    LandaumarginupB = attribute(label='LandaumarginupB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=50,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_LandaumarginupB",
                                   fset="set_LandaumarginupB",
                                   doc=""
                                   )

    LandauMarginLowA = attribute(label='LandauMarginLowA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=10,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_LandauMarginLowA",
                                   fset="set_LandauMarginLowA",
                                   doc=""
                                   )

    LandauMarginLowB = attribute(label='LandauMarginLowB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=10,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_LandauMarginLowB",
                                   fset="set_LandauMarginLowB",
                                   doc=""
                                   )

    MinimumLandauAmplitudeA = attribute(label='MinimumLandauAmplitudeA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_MinimumLandauAmplitudeA",
                                   fset="set_MinimumLandauAmplitudeA",
                                   doc=""
                                   )

    MinimumLandauAmplitudeB = attribute(label='MinimumLandauAmplitudeB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_MinimumLandauAmplitudeB",
                                   fset="set_MinimumLandauAmplitudeB",
                                   doc=""
                                   )

    LandauPositiveEnableA = attribute(label='LandauPositiveEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_LandauPositiveEnableA",
                                   fset="set_LandauPositiveEnableA",
                                   doc=""
                                   )

    LandauPositiveEnableB = attribute(label='LandauPositiveEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_LandauPositiveEnableB",
                                   fset="set_LandauPositiveEnableB",
                                   doc=""
                                   )

    LandauampsettingA = attribute(label='LandauampsettingA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_LandauampsettingA",
                                   fset="set_LandauampsettingA",
                                   doc=""
                                   )

    LandauampsettingB = attribute(label='LandauampsettingB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_LandauampsettingB",
                                   fset="set_LandauampsettingB",
                                   doc=""
                                   )

    DisitckRvtet1DacsoffloopsstbyA = attribute(label='DisitckRvtet1DacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1DacsoffloopsstbyA",
                                   fset="set_DisitckRvtet1DacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckRvtet1DacsoffloopsstbyB = attribute(label='DisitckRvtet1DacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1DacsoffloopsstbyB",
                                   fset="set_DisitckRvtet1DacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckRvtet1PindiodeswitchA = attribute(label='DisitckRvtet1PindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1PindiodeswitchA",
                                   fset="set_DisitckRvtet1PindiodeswitchA",
                                   doc=""
                                   )

    DisitckRvtet1PindiodeswitchB = attribute(label='DisitckRvtet1PindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1PindiodeswitchB",
                                   fset="set_DisitckRvtet1PindiodeswitchB",
                                   doc=""
                                   )

    DisitckRvtet1FdltrgA = attribute(label='DisitckRvtet1FdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1FdltrgA",
                                   fset="set_DisitckRvtet1FdltrgA",
                                   doc=""
                                   )

    DisitckRvtet1FdltrgB = attribute(label='DisitckRvtet1FdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1FdltrgB",
                                   fset="set_DisitckRvtet1FdltrgB",
                                   doc=""
                                   )

    DisitckRvtet1PlctxoffA = attribute(label='DisitckRvtet1PlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1PlctxoffA",
                                   fset="set_DisitckRvtet1PlctxoffA",
                                   doc=""
                                   )

    DisitckRvtet1PlctxoffB = attribute(label='DisitckRvtet1PlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1PlctxoffB",
                                   fset="set_DisitckRvtet1PlctxoffB",
                                   doc=""
                                   )

    DisitckRvtet1MpsA = attribute(label='DisitckRvtet1MpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1MpsA",
                                   fset="set_DisitckRvtet1MpsA",
                                   doc=""
                                   )

    DisitckRvtet1MpsB = attribute(label='DisitckRvtet1MpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1MpsB",
                                   fset="set_DisitckRvtet1MpsB",
                                   doc=""
                                   )

    DisitckRvtet1DiagA = attribute(label='DisitckRvtet1DiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1DiagA",
                                   fset="set_DisitckRvtet1DiagA",
                                   doc=""
                                   )

    DisitckRvtet1DiagB = attribute(label='DisitckRvtet1DiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet1DiagB",
                                   fset="set_DisitckRvtet1DiagB",
                                   doc=""
                                   )

    DisitckRvtet2DacsoffloopsstbyA = attribute(label='DisitckRvtet2DacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2DacsoffloopsstbyA",
                                   fset="set_DisitckRvtet2DacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckRvtet2DacsoffloopsstbyB = attribute(label='DisitckRvtet2DacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2DacsoffloopsstbyB",
                                   fset="set_DisitckRvtet2DacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckRvtet2PindiodeswitchA = attribute(label='DisitckRvtet2PindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2PindiodeswitchA",
                                   fset="set_DisitckRvtet2PindiodeswitchA",
                                   doc=""
                                   )

    DisitckRvtet2PindiodeswitchB = attribute(label='DisitckRvtet2PindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2PindiodeswitchB",
                                   fset="set_DisitckRvtet2PindiodeswitchB",
                                   doc=""
                                   )

    DisitckRvtet2FdltrgA = attribute(label='DisitckRvtet2FdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2FdltrgA",
                                   fset="set_DisitckRvtet2FdltrgA",
                                   doc=""
                                   )

    DisitckRvtet2FdltrgB = attribute(label='DisitckRvtet2FdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2FdltrgB",
                                   fset="set_DisitckRvtet2FdltrgB",
                                   doc=""
                                   )

    DisitckRvtet2PlctxoffA = attribute(label='DisitckRvtet2PlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2PlctxoffA",
                                   fset="set_DisitckRvtet2PlctxoffA",
                                   doc=""
                                   )

    DisitckRvtet2PlctxoffB = attribute(label='DisitckRvtet2PlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2PlctxoffB",
                                   fset="set_DisitckRvtet2PlctxoffB",
                                   doc=""
                                   )

    DisitckRvtet2MpsA = attribute(label='DisitckRvtet2MpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2MpsA",
                                   fset="set_DisitckRvtet2MpsA",
                                   doc=""
                                   )

    DisitckRvtet2MpsB = attribute(label='DisitckRvtet2MpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2MpsB",
                                   fset="set_DisitckRvtet2MpsB",
                                   doc=""
                                   )

    DisitckRvtet2DiagA = attribute(label='DisitckRvtet2DiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2DiagA",
                                   fset="set_DisitckRvtet2DiagA",
                                   doc=""
                                   )

    DisitckRvtet2DiagB = attribute(label='DisitckRvtet2DiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvtet2DiagB",
                                   fset="set_DisitckRvtet2DiagB",
                                   doc=""
                                   )

    DisitckRvcircDacsoffloopsstbyA = attribute(label='DisitckRvcircDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircDacsoffloopsstbyA",
                                   fset="set_DisitckRvcircDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckRvcircDacsoffloopsstbyB = attribute(label='DisitckRvcircDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircDacsoffloopsstbyB",
                                   fset="set_DisitckRvcircDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckRvcircPindiodeswitchA = attribute(label='DisitckRvcircPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircPindiodeswitchA",
                                   fset="set_DisitckRvcircPindiodeswitchA",
                                   doc=""
                                   )

    DisitckRvcircPindiodeswitchB = attribute(label='DisitckRvcircPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircPindiodeswitchB",
                                   fset="set_DisitckRvcircPindiodeswitchB",
                                   doc=""
                                   )

    DisitckRvcircFdltrgA = attribute(label='DisitckRvcircFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircFdltrgA",
                                   fset="set_DisitckRvcircFdltrgA",
                                   doc=""
                                   )

    DisitckRvcircFdltrgB = attribute(label='DisitckRvcircFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircFdltrgB",
                                   fset="set_DisitckRvcircFdltrgB",
                                   doc=""
                                   )

    DisitckRvcircPlctxoffA = attribute(label='DisitckRvcircPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircPlctxoffA",
                                   fset="set_DisitckRvcircPlctxoffA",
                                   doc=""
                                   )

    DisitckRvcircPlctxoffB = attribute(label='DisitckRvcircPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircPlctxoffB",
                                   fset="set_DisitckRvcircPlctxoffB",
                                   doc=""
                                   )

    DisitckRvcircMpsA = attribute(label='DisitckRvcircMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircMpsA",
                                   fset="set_DisitckRvcircMpsA",
                                   doc=""
                                   )

    DisitckRvcircMpsB = attribute(label='DisitckRvcircMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircMpsB",
                                   fset="set_DisitckRvcircMpsB",
                                   doc=""
                                   )

    DisitckRvcircDiagA = attribute(label='DisitckRvcircDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircDiagA",
                                   fset="set_DisitckRvcircDiagA",
                                   doc=""
                                   )

    DisitckRvcircDiagB = attribute(label='DisitckRvcircDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcircDiagB",
                                   fset="set_DisitckRvcircDiagB",
                                   doc=""
                                   )

    DisitckFwloadDacsoffloopsstbyA = attribute(label='DisitckFwloadDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadDacsoffloopsstbyA",
                                   fset="set_DisitckFwloadDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckFwloadDacsoffloopsstbyB = attribute(label='DisitckFwloadDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadDacsoffloopsstbyB",
                                   fset="set_DisitckFwloadDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckFwloadPindiodeswitchA = attribute(label='DisitckFwloadPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadPindiodeswitchA",
                                   fset="set_DisitckFwloadPindiodeswitchA",
                                   doc=""
                                   )

    DisitckFwloadPindiodeswitchB = attribute(label='DisitckFwloadPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadPindiodeswitchB",
                                   fset="set_DisitckFwloadPindiodeswitchB",
                                   doc=""
                                   )

    DisitckFwloadFdltrgA = attribute(label='DisitckFwloadFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadFdltrgA",
                                   fset="set_DisitckFwloadFdltrgA",
                                   doc=""
                                   )

    DisitckFwloadFdltrgB = attribute(label='DisitckFwloadFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadFdltrgB",
                                   fset="set_DisitckFwloadFdltrgB",
                                   doc=""
                                   )

    DisitckFwloadPlctxoffA = attribute(label='DisitckFwloadPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadPlctxoffA",
                                   fset="set_DisitckFwloadPlctxoffA",
                                   doc=""
                                   )

    DisitckFwloadPlctxoffB = attribute(label='DisitckFwloadPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadPlctxoffB",
                                   fset="set_DisitckFwloadPlctxoffB",
                                   doc=""
                                   )

    DisitckFwloadMpsA = attribute(label='DisitckFwloadMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadMpsA",
                                   fset="set_DisitckFwloadMpsA",
                                   doc=""
                                   )

    DisitckFwloadMpsB = attribute(label='DisitckFwloadMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadMpsB",
                                   fset="set_DisitckFwloadMpsB",
                                   doc=""
                                   )

    DisitckFwloadDiagA = attribute(label='DisitckFwloadDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadDiagA",
                                   fset="set_DisitckFwloadDiagA",
                                   doc=""
                                   )

    DisitckFwloadDiagB = attribute(label='DisitckFwloadDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwloadDiagB",
                                   fset="set_DisitckFwloadDiagB",
                                   doc=""
                                   )

    DisitckFwhybloadDacsoffloopsstbyA = attribute(label='DisitckFwhybloadDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadDacsoffloopsstbyA",
                                   fset="set_DisitckFwhybloadDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckFwhybloadDacsoffloopsstbyB = attribute(label='DisitckFwhybloadDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadDacsoffloopsstbyB",
                                   fset="set_DisitckFwhybloadDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckFwhybloadPindiodeswitchA = attribute(label='DisitckFwhybloadPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadPindiodeswitchA",
                                   fset="set_DisitckFwhybloadPindiodeswitchA",
                                   doc=""
                                   )

    DisitckFwhybloadPindiodeswitchB = attribute(label='DisitckFwhybloadPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadPindiodeswitchB",
                                   fset="set_DisitckFwhybloadPindiodeswitchB",
                                   doc=""
                                   )

    DisitckFwhybloadFdltrgA = attribute(label='DisitckFwhybloadFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadFdltrgA",
                                   fset="set_DisitckFwhybloadFdltrgA",
                                   doc=""
                                   )

    DisitckFwhybloadFdltrgB = attribute(label='DisitckFwhybloadFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadFdltrgB",
                                   fset="set_DisitckFwhybloadFdltrgB",
                                   doc=""
                                   )

    DisitckFwhybloadPlctxoffA = attribute(label='DisitckFwhybloadPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadPlctxoffA",
                                   fset="set_DisitckFwhybloadPlctxoffA",
                                   doc=""
                                   )

    DisitckFwhybloadPlctxoffB = attribute(label='DisitckFwhybloadPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadPlctxoffB",
                                   fset="set_DisitckFwhybloadPlctxoffB",
                                   doc=""
                                   )

    DisitckFwhybloadMpsA = attribute(label='DisitckFwhybloadMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadMpsA",
                                   fset="set_DisitckFwhybloadMpsA",
                                   doc=""
                                   )

    DisitckFwhybloadMpsB = attribute(label='DisitckFwhybloadMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadMpsB",
                                   fset="set_DisitckFwhybloadMpsB",
                                   doc=""
                                   )

    DisitckFwhybloadDiagA = attribute(label='DisitckFwhybloadDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadDiagA",
                                   fset="set_DisitckFwhybloadDiagA",
                                   doc=""
                                   )

    DisitckFwhybloadDiagB = attribute(label='DisitckFwhybloadDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckFwhybloadDiagB",
                                   fset="set_DisitckFwhybloadDiagB",
                                   doc=""
                                   )

    DisitckRvcavDacsoffloopsstbyA = attribute(label='DisitckRvcavDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavDacsoffloopsstbyA",
                                   fset="set_DisitckRvcavDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckRvcavDacsoffloopsstbyB = attribute(label='DisitckRvcavDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavDacsoffloopsstbyB",
                                   fset="set_DisitckRvcavDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckRvcavPindiodeswitchA = attribute(label='DisitckRvcavPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavPindiodeswitchA",
                                   fset="set_DisitckRvcavPindiodeswitchA",
                                   doc=""
                                   )

    DisitckRvcavPindiodeswitchB = attribute(label='DisitckRvcavPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavPindiodeswitchB",
                                   fset="set_DisitckRvcavPindiodeswitchB",
                                   doc=""
                                   )

    DisitckRvcavFdltrgA = attribute(label='DisitckRvcavFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavFdltrgA",
                                   fset="set_DisitckRvcavFdltrgA",
                                   doc=""
                                   )

    DisitckRvcavFdltrgB = attribute(label='DisitckRvcavFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavFdltrgB",
                                   fset="set_DisitckRvcavFdltrgB",
                                   doc=""
                                   )

    DisitckRvcavPlctxoffA = attribute(label='DisitckRvcavPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavPlctxoffA",
                                   fset="set_DisitckRvcavPlctxoffA",
                                   doc=""
                                   )

    DisitckRvcavPlctxoffB = attribute(label='DisitckRvcavPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavPlctxoffB",
                                   fset="set_DisitckRvcavPlctxoffB",
                                   doc=""
                                   )

    DisitckRvcavMpsA = attribute(label='DisitckRvcavMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavMpsA",
                                   fset="set_DisitckRvcavMpsA",
                                   doc=""
                                   )

    DisitckRvcavMpsB = attribute(label='DisitckRvcavMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavMpsB",
                                   fset="set_DisitckRvcavMpsB",
                                   doc=""
                                   )

    DisitckRvcavDiagA = attribute(label='DisitckRvcavDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavDiagA",
                                   fset="set_DisitckRvcavDiagA",
                                   doc=""
                                   )

    DisitckRvcavDiagB = attribute(label='DisitckRvcavDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckRvcavDiagB",
                                   fset="set_DisitckRvcavDiagB",
                                   doc=""
                                   )

    DisitckArcsDacsoffloopsstbyA = attribute(label='DisitckArcsDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsDacsoffloopsstbyA",
                                   fset="set_DisitckArcsDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckArcsDacsoffloopsstbyB = attribute(label='DisitckArcsDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsDacsoffloopsstbyB",
                                   fset="set_DisitckArcsDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckArcsPindiodeswitchA = attribute(label='DisitckArcsPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsPindiodeswitchA",
                                   fset="set_DisitckArcsPindiodeswitchA",
                                   doc=""
                                   )

    DisitckArcsPindiodeswitchB = attribute(label='DisitckArcsPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsPindiodeswitchB",
                                   fset="set_DisitckArcsPindiodeswitchB",
                                   doc=""
                                   )

    DisitckArcsFdltrgA = attribute(label='DisitckArcsFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsFdltrgA",
                                   fset="set_DisitckArcsFdltrgA",
                                   doc=""
                                   )

    DisitckArcsFdltrgB = attribute(label='DisitckArcsFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsFdltrgB",
                                   fset="set_DisitckArcsFdltrgB",
                                   doc=""
                                   )

    DisitckArcsPlctxoffA = attribute(label='DisitckArcsPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsPlctxoffA",
                                   fset="set_DisitckArcsPlctxoffA",
                                   doc=""
                                   )

    DisitckArcsPlctxoffB = attribute(label='DisitckArcsPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsPlctxoffB",
                                   fset="set_DisitckArcsPlctxoffB",
                                   doc=""
                                   )

    DisitckArcsMpsA = attribute(label='DisitckArcsMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsMpsA",
                                   fset="set_DisitckArcsMpsA",
                                   doc=""
                                   )

    DisitckArcsMpsB = attribute(label='DisitckArcsMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsMpsB",
                                   fset="set_DisitckArcsMpsB",
                                   doc=""
                                   )

    DisitckArcsDiagA = attribute(label='DisitckArcsDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsDiagA",
                                   fset="set_DisitckArcsDiagA",
                                   doc=""
                                   )

    DisitckArcsDiagB = attribute(label='DisitckArcsDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckArcsDiagB",
                                   fset="set_DisitckArcsDiagB",
                                   doc=""
                                   )

    DisitckVacuumDacsoffloopsstbyA = attribute(label='DisitckVacuumDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumDacsoffloopsstbyA",
                                   fset="set_DisitckVacuumDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckVacuumDacsoffloopsstbyB = attribute(label='DisitckVacuumDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumDacsoffloopsstbyB",
                                   fset="set_DisitckVacuumDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckVacuumPindiodeswitchA = attribute(label='DisitckVacuumPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumPindiodeswitchA",
                                   fset="set_DisitckVacuumPindiodeswitchA",
                                   doc=""
                                   )

    DisitckVacuumPindiodeswitchB = attribute(label='DisitckVacuumPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumPindiodeswitchB",
                                   fset="set_DisitckVacuumPindiodeswitchB",
                                   doc=""
                                   )

    DisitckVacuumFdltrgA = attribute(label='DisitckVacuumFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumFdltrgA",
                                   fset="set_DisitckVacuumFdltrgA",
                                   doc=""
                                   )

    DisitckVacuumFdltrgB = attribute(label='DisitckVacuumFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumFdltrgB",
                                   fset="set_DisitckVacuumFdltrgB",
                                   doc=""
                                   )

    DisitckVacuumPlctxoffA = attribute(label='DisitckVacuumPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumPlctxoffA",
                                   fset="set_DisitckVacuumPlctxoffA",
                                   doc=""
                                   )

    DisitckVacuumPlctxoffB = attribute(label='DisitckVacuumPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumPlctxoffB",
                                   fset="set_DisitckVacuumPlctxoffB",
                                   doc=""
                                   )

    DisitckVacuumMpsA = attribute(label='DisitckVacuumMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumMpsA",
                                   fset="set_DisitckVacuumMpsA",
                                   doc=""
                                   )

    DisitckVacuumMpsB = attribute(label='DisitckVacuumMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumMpsB",
                                   fset="set_DisitckVacuumMpsB",
                                   doc=""
                                   )

    DisitckVacuumDiagA = attribute(label='DisitckVacuumDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumDiagA",
                                   fset="set_DisitckVacuumDiagA",
                                   doc=""
                                   )

    DisitckVacuumDiagB = attribute(label='DisitckVacuumDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckVacuumDiagB",
                                   fset="set_DisitckVacuumDiagB",
                                   doc=""
                                   )

    DisitckManualInterlockDacsoffloopsstbyA = attribute(label='DisitckManualInterlockDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockDacsoffloopsstbyA",
                                   fset="set_DisitckManualInterlockDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckManualInterlockDacsoffloopsstbyB = attribute(label='DisitckManualInterlockDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockDacsoffloopsstbyB",
                                   fset="set_DisitckManualInterlockDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckManualInterlockPindiodeswitchA = attribute(label='DisitckManualInterlockPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockPindiodeswitchA",
                                   fset="set_DisitckManualInterlockPindiodeswitchA",
                                   doc=""
                                   )

    DisitckManualInterlockPindiodeswitchB = attribute(label='DisitckManualInterlockPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockPindiodeswitchB",
                                   fset="set_DisitckManualInterlockPindiodeswitchB",
                                   doc=""
                                   )

    DisitckManualInterlockFdltrgA = attribute(label='DisitckManualInterlockFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockFdltrgA",
                                   fset="set_DisitckManualInterlockFdltrgA",
                                   doc=""
                                   )

    DisitckManualInterlockFdltrgB = attribute(label='DisitckManualInterlockFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockFdltrgB",
                                   fset="set_DisitckManualInterlockFdltrgB",
                                   doc=""
                                   )

    DisitckManualInterlockPlctxoffA = attribute(label='DisitckManualInterlockPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockPlctxoffA",
                                   fset="set_DisitckManualInterlockPlctxoffA",
                                   doc=""
                                   )

    DisitckManualInterlockPlctxoffB = attribute(label='DisitckManualInterlockPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockPlctxoffB",
                                   fset="set_DisitckManualInterlockPlctxoffB",
                                   doc=""
                                   )

    DisitckManualInterlockMpsA = attribute(label='DisitckManualInterlockMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockMpsA",
                                   fset="set_DisitckManualInterlockMpsA",
                                   doc=""
                                   )

    DisitckManualInterlockMpsB = attribute(label='DisitckManualInterlockMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockMpsB",
                                   fset="set_DisitckManualInterlockMpsB",
                                   doc=""
                                   )

    DisitckManualInterlockDiagA = attribute(label='DisitckManualInterlockDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockDiagA",
                                   fset="set_DisitckManualInterlockDiagA",
                                   doc=""
                                   )

    DisitckManualInterlockDiagB = attribute(label='DisitckManualInterlockDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckManualInterlockDiagB",
                                   fset="set_DisitckManualInterlockDiagB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpDacsoffloopsstbyA = attribute(label='DisitckPlungerEndSwitchesUpDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpDacsoffloopsstbyA",
                                   fset="set_DisitckPlungerEndSwitchesUpDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpDacsoffloopsstbyB = attribute(label='DisitckPlungerEndSwitchesUpDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpDacsoffloopsstbyB",
                                   fset="set_DisitckPlungerEndSwitchesUpDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpPindiodeswitchA = attribute(label='DisitckPlungerEndSwitchesUpPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpPindiodeswitchA",
                                   fset="set_DisitckPlungerEndSwitchesUpPindiodeswitchA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpPindiodeswitchB = attribute(label='DisitckPlungerEndSwitchesUpPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpPindiodeswitchB",
                                   fset="set_DisitckPlungerEndSwitchesUpPindiodeswitchB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpFdltrgA = attribute(label='DisitckPlungerEndSwitchesUpFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpFdltrgA",
                                   fset="set_DisitckPlungerEndSwitchesUpFdltrgA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpFdltrgB = attribute(label='DisitckPlungerEndSwitchesUpFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpFdltrgB",
                                   fset="set_DisitckPlungerEndSwitchesUpFdltrgB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpPlctxoffA = attribute(label='DisitckPlungerEndSwitchesUpPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpPlctxoffA",
                                   fset="set_DisitckPlungerEndSwitchesUpPlctxoffA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpPlctxoffB = attribute(label='DisitckPlungerEndSwitchesUpPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpPlctxoffB",
                                   fset="set_DisitckPlungerEndSwitchesUpPlctxoffB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpMpsA = attribute(label='DisitckPlungerEndSwitchesUpMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpMpsA",
                                   fset="set_DisitckPlungerEndSwitchesUpMpsA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpMpsB = attribute(label='DisitckPlungerEndSwitchesUpMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpMpsB",
                                   fset="set_DisitckPlungerEndSwitchesUpMpsB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpDiagA = attribute(label='DisitckPlungerEndSwitchesUpDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpDiagA",
                                   fset="set_DisitckPlungerEndSwitchesUpDiagA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpDiagB = attribute(label='DisitckPlungerEndSwitchesUpDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesUpDiagB",
                                   fset="set_DisitckPlungerEndSwitchesUpDiagB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownDacsoffloopsstbyA = attribute(label='DisitckPlungerEndSwitchesDownDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownDacsoffloopsstbyA",
                                   fset="set_DisitckPlungerEndSwitchesDownDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownDacsoffloopsstbyB = attribute(label='DisitckPlungerEndSwitchesDownDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownDacsoffloopsstbyB",
                                   fset="set_DisitckPlungerEndSwitchesDownDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownPindiodeswitchA = attribute(label='DisitckPlungerEndSwitchesDownPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownPindiodeswitchA",
                                   fset="set_DisitckPlungerEndSwitchesDownPindiodeswitchA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownPindiodeswitchB = attribute(label='DisitckPlungerEndSwitchesDownPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownPindiodeswitchB",
                                   fset="set_DisitckPlungerEndSwitchesDownPindiodeswitchB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownFdltrgA = attribute(label='DisitckPlungerEndSwitchesDownFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownFdltrgA",
                                   fset="set_DisitckPlungerEndSwitchesDownFdltrgA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownFdltrgB = attribute(label='DisitckPlungerEndSwitchesDownFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownFdltrgB",
                                   fset="set_DisitckPlungerEndSwitchesDownFdltrgB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownPlctxoffA = attribute(label='DisitckPlungerEndSwitchesDownPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownPlctxoffA",
                                   fset="set_DisitckPlungerEndSwitchesDownPlctxoffA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownPlctxoffB = attribute(label='DisitckPlungerEndSwitchesDownPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownPlctxoffB",
                                   fset="set_DisitckPlungerEndSwitchesDownPlctxoffB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownMpsA = attribute(label='DisitckPlungerEndSwitchesDownMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownMpsA",
                                   fset="set_DisitckPlungerEndSwitchesDownMpsA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownMpsB = attribute(label='DisitckPlungerEndSwitchesDownMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownMpsB",
                                   fset="set_DisitckPlungerEndSwitchesDownMpsB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownDiagA = attribute(label='DisitckPlungerEndSwitchesDownDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownDiagA",
                                   fset="set_DisitckPlungerEndSwitchesDownDiagA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownDiagB = attribute(label='DisitckPlungerEndSwitchesDownDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckPlungerEndSwitchesDownDiagB",
                                   fset="set_DisitckPlungerEndSwitchesDownDiagB",
                                   doc=""
                                   )

    DisitckMpsDacsoffloopsstbyA = attribute(label='DisitckMpsDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsDacsoffloopsstbyA",
                                   fset="set_DisitckMpsDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckMpsDacsoffloopsstbyB = attribute(label='DisitckMpsDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsDacsoffloopsstbyB",
                                   fset="set_DisitckMpsDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckMpsPindiodeswitchA = attribute(label='DisitckMpsPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsPindiodeswitchA",
                                   fset="set_DisitckMpsPindiodeswitchA",
                                   doc=""
                                   )

    DisitckMpsPindiodeswitchB = attribute(label='DisitckMpsPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsPindiodeswitchB",
                                   fset="set_DisitckMpsPindiodeswitchB",
                                   doc=""
                                   )

    DisitckMpsFdltrgA = attribute(label='DisitckMpsFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsFdltrgA",
                                   fset="set_DisitckMpsFdltrgA",
                                   doc=""
                                   )

    DisitckMpsFdltrgB = attribute(label='DisitckMpsFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsFdltrgB",
                                   fset="set_DisitckMpsFdltrgB",
                                   doc=""
                                   )

    DisitckMpsPlctxoffA = attribute(label='DisitckMpsPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsPlctxoffA",
                                   fset="set_DisitckMpsPlctxoffA",
                                   doc=""
                                   )

    DisitckMpsPlctxoffB = attribute(label='DisitckMpsPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsPlctxoffB",
                                   fset="set_DisitckMpsPlctxoffB",
                                   doc=""
                                   )

    DisitckMpsMpsA = attribute(label='DisitckMpsMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsMpsA",
                                   fset="set_DisitckMpsMpsA",
                                   doc=""
                                   )

    DisitckMpsMpsB = attribute(label='DisitckMpsMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsMpsB",
                                   fset="set_DisitckMpsMpsB",
                                   doc=""
                                   )

    DisitckMpsDiagA = attribute(label='DisitckMpsDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsDiagA",
                                   fset="set_DisitckMpsDiagA",
                                   doc=""
                                   )

    DisitckMpsDiagB = attribute(label='DisitckMpsDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DisitckMpsDiagB",
                                   fset="set_DisitckMpsDiagB",
                                   doc=""
                                   )

    Diag_Irvtet1A = attribute(label='Diag_Irvtet1A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Irvtet1B = attribute(label='Diag_Irvtet1B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvtet1A = attribute(label='Diag_Qrvtet1A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvtet1B = attribute(label='Diag_Qrvtet1B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvtet1A = attribute(label='Diag_Amprvtet1A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvtet1B = attribute(label='Diag_Amprvtet1B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvtet1A = attribute(label='Diag_Phrvtet1A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvtet1B = attribute(label='Diag_Phrvtet1B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Irvtet2A = attribute(label='Diag_Irvtet2A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Irvtet2B = attribute(label='Diag_Irvtet2B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvtet2A = attribute(label='Diag_Qrvtet2A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvtet2B = attribute(label='Diag_Qrvtet2B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvtet2A = attribute(label='Diag_Amprvtet2A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvtet2B = attribute(label='Diag_Amprvtet2B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvtet2A = attribute(label='Diag_Phrvtet2A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvtet2B = attribute(label='Diag_Phrvtet2B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwcircA = attribute(label='Diag_IfwcircA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwcircB = attribute(label='Diag_IfwcircB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwcircA = attribute(label='Diag_QfwcircA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwcircB = attribute(label='Diag_QfwcircB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwcircA = attribute(label='Diag_AmpfwcircA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwcircB = attribute(label='Diag_AmpfwcircB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwcircA = attribute(label='Diag_PhfwcircA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwcircB = attribute(label='Diag_PhfwcircB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrvcircA = attribute(label='Diag_IrvcircA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrvcircB = attribute(label='Diag_IrvcircB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrvcircA = attribute(label='Diag_QrvcircA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrvcircB = attribute(label='Diag_QrvcircB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmprvcircA = attribute(label='Diag_AmprvcircA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmprvcircB = attribute(label='Diag_AmprvcircB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhrvcircA = attribute(label='Diag_PhrvcircA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhrvcircB = attribute(label='Diag_PhrvcircB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwloadA = attribute(label='Diag_IfwloadA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwloadB = attribute(label='Diag_IfwloadB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwloadA = attribute(label='Diag_QfwloadA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwloadB = attribute(label='Diag_QfwloadB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwloadA = attribute(label='Diag_AmpfwloadA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwloadB = attribute(label='Diag_AmpfwloadB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwloadA = attribute(label='Diag_PhfwloadA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwloadB = attribute(label='Diag_PhfwloadB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwhybloadA = attribute(label='Diag_IfwhybloadA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwhybloadB = attribute(label='Diag_IfwhybloadB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwhybloadA = attribute(label='Diag_QfwhybloadA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwhybloadB = attribute(label='Diag_QfwhybloadB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwhybloadA = attribute(label='Diag_AmpfwhybloadA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwhybloadB = attribute(label='Diag_AmpfwhybloadB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwhybloadA = attribute(label='Diag_PhfwhybloadA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwhybloadB = attribute(label='Diag_PhfwhybloadB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrvcavA = attribute(label='Diag_IrvcavA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrvcavB = attribute(label='Diag_IrvcavB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrvcavA = attribute(label='Diag_QrvcavA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrvcavB = attribute(label='Diag_QrvcavB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmprvcavA = attribute(label='Diag_AmprvcavA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmprvcavB = attribute(label='Diag_AmprvcavB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhrvcavA = attribute(label='Diag_PhrvcavA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhrvcavB = attribute(label='Diag_PhrvcavB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ImoA = attribute(label='Diag_ImoA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ImoB = attribute(label='Diag_ImoB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QmoA = attribute(label='Diag_QmoA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QmoB = attribute(label='Diag_QmoB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpmoA = attribute(label='Diag_AmpmoA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpmoB = attribute(label='Diag_AmpmoB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhmoA = attribute(label='Diag_PhmoA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhmoB = attribute(label='Diag_PhmoB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IlandauA = attribute(label='Diag_IlandauA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IlandauB = attribute(label='Diag_IlandauB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QlandauA = attribute(label='Diag_QlandauA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QlandauB = attribute(label='Diag_QlandauB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmplandauA = attribute(label='Diag_AmplandauA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmplandauB = attribute(label='Diag_AmplandauB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhlandauA = attribute(label='Diag_PhlandauA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhlandauB = attribute(label='Diag_PhlandauB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingManualTuningA = attribute(label='Diag_PlungerMovingManualTuningA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingManualTuningB = attribute(label='Diag_PlungerMovingManualTuningB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpManualTuningA = attribute(label='Diag_PlungerMovingUpManualTuningA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpManualTuningB = attribute(label='Diag_PlungerMovingUpManualTuningB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingAutomaticTuningA = attribute(label='Diag_PlungerMovingAutomaticTuningA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingAutomaticTuningB = attribute(label='Diag_PlungerMovingAutomaticTuningB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpAutomaticTuningA = attribute(label='Diag_PlungerMovingUpAutomaticTuningA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpAutomaticTuningB = attribute(label='Diag_PlungerMovingUpAutomaticTuningB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_DephaseMoLandauA = attribute(label='Diag_DephaseMoLandauA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_DephaseMoLandauB = attribute(label='Diag_DephaseMoLandauB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvtet1A = attribute(label='Diag_Rvtet1A',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvtet1B = attribute(label='Diag_Rvtet1B',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvtet2A = attribute(label='Diag_Rvtet2A',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvtet2B = attribute(label='Diag_Rvtet2B',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_RvcircA = attribute(label='Diag_RvcircA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_RvcircB = attribute(label='Diag_RvcircB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwloadA = attribute(label='Diag_FwloadA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwloadB = attribute(label='Diag_FwloadB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwhybloadA = attribute(label='Diag_FwhybloadA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwhybloadB = attribute(label='Diag_FwhybloadB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_RvcavA = attribute(label='Diag_RvcavA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_RvcavB = attribute(label='Diag_RvcavB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ArcsA = attribute(label='Diag_ArcsA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ArcsB = attribute(label='Diag_ArcsB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VacuumA = attribute(label='Diag_VacuumA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VacuumB = attribute(label='Diag_VacuumB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualInterlockA = attribute(label='Diag_ManualInterlockA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualInterlockB = attribute(label='Diag_ManualInterlockB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ExternalItckA = attribute(label='Diag_ExternalItckA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ExternalItckB = attribute(label='Diag_ExternalItckB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchUpA = attribute(label='Diag_PlungerEndSwitchUpA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchUpB = attribute(label='Diag_PlungerEndSwitchUpB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchDownA = attribute(label='Diag_PlungerEndSwitchDownA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchDownB = attribute(label='Diag_PlungerEndSwitchDownB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp1A = attribute(label='Diag_Timestamp1A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp1B = attribute(label='Diag_Timestamp1B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp2A = attribute(label='Diag_Timestamp2A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp2B = attribute(label='Diag_Timestamp2B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp3A = attribute(label='Diag_Timestamp3A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp3B = attribute(label='Diag_Timestamp3B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp4A = attribute(label='Diag_Timestamp4A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp4B = attribute(label='Diag_Timestamp4B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp5A = attribute(label='Diag_Timestamp5A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp5B = attribute(label='Diag_Timestamp5B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp6A = attribute(label='Diag_Timestamp6A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp6B = attribute(label='Diag_Timestamp6B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp7A = attribute(label='Diag_Timestamp7A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp7B = attribute(label='Diag_Timestamp7B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_DacsDisableCommandA = attribute(label='Diag_DacsDisableCommandA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_DacsDisableCommandB = attribute(label='Diag_DacsDisableCommandB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PinSwitchA = attribute(label='Diag_PinSwitchA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PinSwitchB = attribute(label='Diag_PinSwitchB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTriggerToLoopsdiagboardA = attribute(label='Diag_FdlTriggerToLoopsdiagboardA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTriggerToLoopsdiagboardB = attribute(label='Diag_FdlTriggerToLoopsdiagboardB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_OutputToPlcA = attribute(label='Diag_OutputToPlcA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_OutputToPlcB = attribute(label='Diag_OutputToPlcB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_OutputToMpsA = attribute(label='Diag_OutputToMpsA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_OutputToMpsB = attribute(label='Diag_OutputToMpsB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvtet1b = attribute(label='Diag_AmpRvtet1b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvtet1a = attribute(label='Diag_AmpRvtet1a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMoa = attribute(label='Diag_AmpMoa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLandaua = attribute(label='Diag_AmpLandaua',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwloada = attribute(label='Diag_AmpFwloada',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvtet2b = attribute(label='Diag_AmpRvtet2b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvtet2a = attribute(label='Diag_AmpRvtet2a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwloadb = attribute(label='Diag_AmpFwloadb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvcavb = attribute(label='Diag_AmpRvcavb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvcava = attribute(label='Diag_AmpRvcava',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcircb = attribute(label='Diag_AmpFwcircb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcirca = attribute(label='Diag_AmpFwcirca',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMob = attribute(label='Diag_AmpMob',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvcirca = attribute(label='Diag_AmpRvcirca',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvcircb = attribute(label='Diag_AmpRvcircb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwhybloadb = attribute(label='Diag_AmpFwhybloadb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwhybloada = attribute(label='Diag_AmpFwhybloada',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLandaub = attribute(label='Diag_AmpLandaub',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvtet1b = attribute(label='Diag_PhRvtet1b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvtet1a = attribute(label='Diag_PhRvtet1a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMoa = attribute(label='Diag_PhMoa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLandaua = attribute(label='Diag_PhLandaua',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwloada = attribute(label='Diag_PhFwloada',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvtet2b = attribute(label='Diag_PhRvtet2b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvtet2a = attribute(label='Diag_PhRvtet2a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwloadb = attribute(label='Diag_PhFwloadb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvcavb = attribute(label='Diag_PhRvcavb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvcava = attribute(label='Diag_PhRvcava',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcircb = attribute(label='Diag_PhFwcircb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcirca = attribute(label='Diag_PhFwcirca',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMob = attribute(label='Diag_PhMob',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvcirca = attribute(label='Diag_PhRvcirca',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvcircb = attribute(label='Diag_PhRvcircb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwhybloadb = attribute(label='Diag_PhFwhybloadb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwhybloada = attribute(label='Diag_PhFwhybloada',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLandaub = attribute(label='Diag_PhLandaub',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )


    ItckNumber = attribute(label='ItckNumber',
                       dtype=int,
                       display_level=DispLevel.OPERATOR,
                       access=AttrWriteType.READ_WRITE,
                       unit='',
                       format='%6.2f',
                       min_value=0, max_value=7,
                       fget="get_ItckNumber",
                       fset="set_ItckNumber",
                       doc=""
                       )

    perseusType = device_property(dtype=str, default_value='simulated')
    perseusIp = device_property(dtype=str, default_value='192.168.0.142')
    FDLPath = device_property(dtype=str, default_value='/tmp')

    def init_device(self):
        self._itck_number = 0
        Device.init_device(self)
        try:
            self.perseus = Perseus().new_perseus(self.perseusType, self.perseusIp)
            self.set_events()
            self.set_state(DevState.ON)
        except Exception, e:
            print e
            self.set_state(DevState.FAULT)

    def set_events(self):
        self.set_change_event('Rvtet1A', True)
        self.set_change_event('Rvtet1B', True)
        self.set_change_event('Rvtet2A', True)
        self.set_change_event('Rvtet2B', True)
        self.set_change_event('RvcircA', True)
        self.set_change_event('RvcircB', True)
        self.set_change_event('FwloadA', True)
        self.set_change_event('FwloadB', True)
        self.set_change_event('FwhybloadA', True)
        self.set_change_event('FwhybloadB', True)
        self.set_change_event('RvcavA', True)
        self.set_change_event('RvcavB', True)
        self.set_change_event('ManualInterlockA', True)
        self.set_change_event('ManualInterlockB', True)
        self.set_change_event('DisableItckRvtet1A', True)
        self.set_change_event('DisableItckRvtet1B', True)
        self.set_change_event('DisableItckRvtet2A', True)
        self.set_change_event('DisableItckRvtet2B', True)
        self.set_change_event('DisableItckRvcircA', True)
        self.set_change_event('DisableItckRvcircB', True)
        self.set_change_event('DisableItckFwloadA', True)
        self.set_change_event('DisableItckFwloadB', True)
        self.set_change_event('DisableItckFwhybloadA', True)
        self.set_change_event('DisableItckFwhybloadB', True)
        self.set_change_event('DisableItckRvcavA', True)
        self.set_change_event('DisableItckRvcavB', True)
        self.set_change_event('DisableItckArcsA', True)
        self.set_change_event('DisableItckArcsB', True)
        self.set_change_event('DisableItckVaccumA', True)
        self.set_change_event('DisableItckVaccumB', True)
        self.set_change_event('DisableItckManualInterlockA', True)
        self.set_change_event('DisableItckManualInterlockB', True)
        self.set_change_event('DisableItckPlungerEndSwitchesUpA', True)
        self.set_change_event('DisableItckPlungerEndSwitchesUpB', True)
        self.set_change_event('DisableItckPlungerEndSwitchesDownA', True)
        self.set_change_event('DisableItckPlungerEndSwitchesDownB', True)
        self.set_change_event('DisableItckMpsA', True)
        self.set_change_event('DisableItckMpsB', True)
        self.set_change_event('SamplesToAverageA', True)
        self.set_change_event('SamplesToAverageB', True)
        self.set_change_event('PulseupLogicInversionA', True)
        self.set_change_event('PulseupLogicInversionB', True)
        self.set_change_event('EndSwitchesConnectedToNoNcContactA', True)
        self.set_change_event('EndSwitchesConnectedToNoNcContactB', True)
        self.set_change_event('LookrefA', True)
        self.set_change_event('LookrefB', True)
        self.set_change_event('QuadrefA', True)
        self.set_change_event('QuadrefB', True)
        self.set_change_event('SpareDo1A', True)
        self.set_change_event('SpareDo1B', True)
        self.set_change_event('SpareDo2A', True)
        self.set_change_event('SpareDo2B', True)
        self.set_change_event('SpareDo3A', True)
        self.set_change_event('SpareDo3B', True)
        self.set_change_event('FdlSwTriggerA', True)
        self.set_change_event('FdlSwTriggerB', True)
        self.set_change_event('ResetInterlocksCavA', True)
        self.set_change_event('ResetInterlocksCavB', True)
        self.set_change_event('LandautuningenableA', True)
        self.set_change_event('LandautuningenableB', True)
        self.set_change_event('LandautuningresetA', True)
        self.set_change_event('LandautuningresetB', True)
        self.set_change_event('MovelandauupA', True)
        self.set_change_event('MovelandauupB', True)
        self.set_change_event('MovelandauplgA', True)
        self.set_change_event('MovelandauplgB', True)
        self.set_change_event('NumstepsA', True)
        self.set_change_event('NumstepsB', True)
        self.set_change_event('LandauphaseoffsetA', True)
        self.set_change_event('LandauphaseoffsetB', True)
        self.set_change_event('LandaumarginupA', True)
        self.set_change_event('LandaumarginupB', True)
        self.set_change_event('LandauMarginLowA', True)
        self.set_change_event('LandauMarginLowB', True)
        self.set_change_event('MinimumLandauAmplitudeA', True)
        self.set_change_event('MinimumLandauAmplitudeB', True)
        self.set_change_event('LandauPositiveEnableA', True)
        self.set_change_event('LandauPositiveEnableB', True)
        self.set_change_event('LandauampsettingA', True)
        self.set_change_event('LandauampsettingB', True)
        self.set_change_event('DisitckRvtet1DacsoffloopsstbyA', True)
        self.set_change_event('DisitckRvtet1DacsoffloopsstbyB', True)
        self.set_change_event('DisitckRvtet1PindiodeswitchA', True)
        self.set_change_event('DisitckRvtet1PindiodeswitchB', True)
        self.set_change_event('DisitckRvtet1FdltrgA', True)
        self.set_change_event('DisitckRvtet1FdltrgB', True)
        self.set_change_event('DisitckRvtet1PlctxoffA', True)
        self.set_change_event('DisitckRvtet1PlctxoffB', True)
        self.set_change_event('DisitckRvtet1MpsA', True)
        self.set_change_event('DisitckRvtet1MpsB', True)
        self.set_change_event('DisitckRvtet1DiagA', True)
        self.set_change_event('DisitckRvtet1DiagB', True)
        self.set_change_event('DisitckRvtet2DacsoffloopsstbyA', True)
        self.set_change_event('DisitckRvtet2DacsoffloopsstbyB', True)
        self.set_change_event('DisitckRvtet2PindiodeswitchA', True)
        self.set_change_event('DisitckRvtet2PindiodeswitchB', True)
        self.set_change_event('DisitckRvtet2FdltrgA', True)
        self.set_change_event('DisitckRvtet2FdltrgB', True)
        self.set_change_event('DisitckRvtet2PlctxoffA', True)
        self.set_change_event('DisitckRvtet2PlctxoffB', True)
        self.set_change_event('DisitckRvtet2MpsA', True)
        self.set_change_event('DisitckRvtet2MpsB', True)
        self.set_change_event('DisitckRvtet2DiagA', True)
        self.set_change_event('DisitckRvtet2DiagB', True)
        self.set_change_event('DisitckRvcircDacsoffloopsstbyA', True)
        self.set_change_event('DisitckRvcircDacsoffloopsstbyB', True)
        self.set_change_event('DisitckRvcircPindiodeswitchA', True)
        self.set_change_event('DisitckRvcircPindiodeswitchB', True)
        self.set_change_event('DisitckRvcircFdltrgA', True)
        self.set_change_event('DisitckRvcircFdltrgB', True)
        self.set_change_event('DisitckRvcircPlctxoffA', True)
        self.set_change_event('DisitckRvcircPlctxoffB', True)
        self.set_change_event('DisitckRvcircMpsA', True)
        self.set_change_event('DisitckRvcircMpsB', True)
        self.set_change_event('DisitckRvcircDiagA', True)
        self.set_change_event('DisitckRvcircDiagB', True)
        self.set_change_event('DisitckFwloadDacsoffloopsstbyA', True)
        self.set_change_event('DisitckFwloadDacsoffloopsstbyB', True)
        self.set_change_event('DisitckFwloadPindiodeswitchA', True)
        self.set_change_event('DisitckFwloadPindiodeswitchB', True)
        self.set_change_event('DisitckFwloadFdltrgA', True)
        self.set_change_event('DisitckFwloadFdltrgB', True)
        self.set_change_event('DisitckFwloadPlctxoffA', True)
        self.set_change_event('DisitckFwloadPlctxoffB', True)
        self.set_change_event('DisitckFwloadMpsA', True)
        self.set_change_event('DisitckFwloadMpsB', True)
        self.set_change_event('DisitckFwloadDiagA', True)
        self.set_change_event('DisitckFwloadDiagB', True)
        self.set_change_event('DisitckFwhybloadDacsoffloopsstbyA', True)
        self.set_change_event('DisitckFwhybloadDacsoffloopsstbyB', True)
        self.set_change_event('DisitckFwhybloadPindiodeswitchA', True)
        self.set_change_event('DisitckFwhybloadPindiodeswitchB', True)
        self.set_change_event('DisitckFwhybloadFdltrgA', True)
        self.set_change_event('DisitckFwhybloadFdltrgB', True)
        self.set_change_event('DisitckFwhybloadPlctxoffA', True)
        self.set_change_event('DisitckFwhybloadPlctxoffB', True)
        self.set_change_event('DisitckFwhybloadMpsA', True)
        self.set_change_event('DisitckFwhybloadMpsB', True)
        self.set_change_event('DisitckFwhybloadDiagA', True)
        self.set_change_event('DisitckFwhybloadDiagB', True)
        self.set_change_event('DisitckRvcavDacsoffloopsstbyA', True)
        self.set_change_event('DisitckRvcavDacsoffloopsstbyB', True)
        self.set_change_event('DisitckRvcavPindiodeswitchA', True)
        self.set_change_event('DisitckRvcavPindiodeswitchB', True)
        self.set_change_event('DisitckRvcavFdltrgA', True)
        self.set_change_event('DisitckRvcavFdltrgB', True)
        self.set_change_event('DisitckRvcavPlctxoffA', True)
        self.set_change_event('DisitckRvcavPlctxoffB', True)
        self.set_change_event('DisitckRvcavMpsA', True)
        self.set_change_event('DisitckRvcavMpsB', True)
        self.set_change_event('DisitckRvcavDiagA', True)
        self.set_change_event('DisitckRvcavDiagB', True)
        self.set_change_event('DisitckArcsDacsoffloopsstbyA', True)
        self.set_change_event('DisitckArcsDacsoffloopsstbyB', True)
        self.set_change_event('DisitckArcsPindiodeswitchA', True)
        self.set_change_event('DisitckArcsPindiodeswitchB', True)
        self.set_change_event('DisitckArcsFdltrgA', True)
        self.set_change_event('DisitckArcsFdltrgB', True)
        self.set_change_event('DisitckArcsPlctxoffA', True)
        self.set_change_event('DisitckArcsPlctxoffB', True)
        self.set_change_event('DisitckArcsMpsA', True)
        self.set_change_event('DisitckArcsMpsB', True)
        self.set_change_event('DisitckArcsDiagA', True)
        self.set_change_event('DisitckArcsDiagB', True)
        self.set_change_event('DisitckVacuumDacsoffloopsstbyA', True)
        self.set_change_event('DisitckVacuumDacsoffloopsstbyB', True)
        self.set_change_event('DisitckVacuumPindiodeswitchA', True)
        self.set_change_event('DisitckVacuumPindiodeswitchB', True)
        self.set_change_event('DisitckVacuumFdltrgA', True)
        self.set_change_event('DisitckVacuumFdltrgB', True)
        self.set_change_event('DisitckVacuumPlctxoffA', True)
        self.set_change_event('DisitckVacuumPlctxoffB', True)
        self.set_change_event('DisitckVacuumMpsA', True)
        self.set_change_event('DisitckVacuumMpsB', True)
        self.set_change_event('DisitckVacuumDiagA', True)
        self.set_change_event('DisitckVacuumDiagB', True)
        self.set_change_event('DisitckManualInterlockDacsoffloopsstbyA', True)
        self.set_change_event('DisitckManualInterlockDacsoffloopsstbyB', True)
        self.set_change_event('DisitckManualInterlockPindiodeswitchA', True)
        self.set_change_event('DisitckManualInterlockPindiodeswitchB', True)
        self.set_change_event('DisitckManualInterlockFdltrgA', True)
        self.set_change_event('DisitckManualInterlockFdltrgB', True)
        self.set_change_event('DisitckManualInterlockPlctxoffA', True)
        self.set_change_event('DisitckManualInterlockPlctxoffB', True)
        self.set_change_event('DisitckManualInterlockMpsA', True)
        self.set_change_event('DisitckManualInterlockMpsB', True)
        self.set_change_event('DisitckManualInterlockDiagA', True)
        self.set_change_event('DisitckManualInterlockDiagB', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpDacsoffloopsstbyA', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpDacsoffloopsstbyB', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpPindiodeswitchA', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpPindiodeswitchB', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpFdltrgA', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpFdltrgB', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpPlctxoffA', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpPlctxoffB', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpMpsA', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpMpsB', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpDiagA', True)
        self.set_change_event('DisitckPlungerEndSwitchesUpDiagB', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownDacsoffloopsstbyA', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownDacsoffloopsstbyB', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownPindiodeswitchA', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownPindiodeswitchB', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownFdltrgA', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownFdltrgB', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownPlctxoffA', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownPlctxoffB', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownMpsA', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownMpsB', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownDiagA', True)
        self.set_change_event('DisitckPlungerEndSwitchesDownDiagB', True)
        self.set_change_event('DisitckMpsDacsoffloopsstbyA', True)
        self.set_change_event('DisitckMpsDacsoffloopsstbyB', True)
        self.set_change_event('DisitckMpsPindiodeswitchA', True)
        self.set_change_event('DisitckMpsPindiodeswitchB', True)
        self.set_change_event('DisitckMpsFdltrgA', True)
        self.set_change_event('DisitckMpsFdltrgB', True)
        self.set_change_event('DisitckMpsPlctxoffA', True)
        self.set_change_event('DisitckMpsPlctxoffB', True)
        self.set_change_event('DisitckMpsMpsA', True)
        self.set_change_event('DisitckMpsMpsB', True)
        self.set_change_event('DisitckMpsDiagA', True)
        self.set_change_event('DisitckMpsDiagB', True)
        self.set_change_event('Diag_Irvtet1A', True)
        self.set_change_event('Diag_Irvtet1B', True)
        self.set_change_event('Diag_Qrvtet1A', True)
        self.set_change_event('Diag_Qrvtet1B', True)
        self.set_change_event('Diag_Amprvtet1A', True)
        self.set_change_event('Diag_Amprvtet1B', True)
        self.set_change_event('Diag_Phrvtet1A', True)
        self.set_change_event('Diag_Phrvtet1B', True)
        self.set_change_event('Diag_Irvtet2A', True)
        self.set_change_event('Diag_Irvtet2B', True)
        self.set_change_event('Diag_Qrvtet2A', True)
        self.set_change_event('Diag_Qrvtet2B', True)
        self.set_change_event('Diag_Amprvtet2A', True)
        self.set_change_event('Diag_Amprvtet2B', True)
        self.set_change_event('Diag_Phrvtet2A', True)
        self.set_change_event('Diag_Phrvtet2B', True)
        self.set_change_event('Diag_IfwcircA', True)
        self.set_change_event('Diag_IfwcircB', True)
        self.set_change_event('Diag_QfwcircA', True)
        self.set_change_event('Diag_QfwcircB', True)
        self.set_change_event('Diag_AmpfwcircA', True)
        self.set_change_event('Diag_AmpfwcircB', True)
        self.set_change_event('Diag_PhfwcircA', True)
        self.set_change_event('Diag_PhfwcircB', True)
        self.set_change_event('Diag_IrvcircA', True)
        self.set_change_event('Diag_IrvcircB', True)
        self.set_change_event('Diag_QrvcircA', True)
        self.set_change_event('Diag_QrvcircB', True)
        self.set_change_event('Diag_AmprvcircA', True)
        self.set_change_event('Diag_AmprvcircB', True)
        self.set_change_event('Diag_PhrvcircA', True)
        self.set_change_event('Diag_PhrvcircB', True)
        self.set_change_event('Diag_IfwloadA', True)
        self.set_change_event('Diag_IfwloadB', True)
        self.set_change_event('Diag_QfwloadA', True)
        self.set_change_event('Diag_QfwloadB', True)
        self.set_change_event('Diag_AmpfwloadA', True)
        self.set_change_event('Diag_AmpfwloadB', True)
        self.set_change_event('Diag_PhfwloadA', True)
        self.set_change_event('Diag_PhfwloadB', True)
        self.set_change_event('Diag_IfwhybloadA', True)
        self.set_change_event('Diag_IfwhybloadB', True)
        self.set_change_event('Diag_QfwhybloadA', True)
        self.set_change_event('Diag_QfwhybloadB', True)
        self.set_change_event('Diag_AmpfwhybloadA', True)
        self.set_change_event('Diag_AmpfwhybloadB', True)
        self.set_change_event('Diag_PhfwhybloadA', True)
        self.set_change_event('Diag_PhfwhybloadB', True)
        self.set_change_event('Diag_IrvcavA', True)
        self.set_change_event('Diag_IrvcavB', True)
        self.set_change_event('Diag_QrvcavA', True)
        self.set_change_event('Diag_QrvcavB', True)
        self.set_change_event('Diag_AmprvcavA', True)
        self.set_change_event('Diag_AmprvcavB', True)
        self.set_change_event('Diag_PhrvcavA', True)
        self.set_change_event('Diag_PhrvcavB', True)
        self.set_change_event('Diag_ImoA', True)
        self.set_change_event('Diag_ImoB', True)
        self.set_change_event('Diag_QmoA', True)
        self.set_change_event('Diag_QmoB', True)
        self.set_change_event('Diag_AmpmoA', True)
        self.set_change_event('Diag_AmpmoB', True)
        self.set_change_event('Diag_PhmoA', True)
        self.set_change_event('Diag_PhmoB', True)
        self.set_change_event('Diag_IlandauA', True)
        self.set_change_event('Diag_IlandauB', True)
        self.set_change_event('Diag_QlandauA', True)
        self.set_change_event('Diag_QlandauB', True)
        self.set_change_event('Diag_AmplandauA', True)
        self.set_change_event('Diag_AmplandauB', True)
        self.set_change_event('Diag_PhlandauA', True)
        self.set_change_event('Diag_PhlandauB', True)
        self.set_change_event('Diag_PlungerMovingManualTuningA', True)
        self.set_change_event('Diag_PlungerMovingManualTuningB', True)
        self.set_change_event('Diag_PlungerMovingUpManualTuningA', True)
        self.set_change_event('Diag_PlungerMovingUpManualTuningB', True)
        self.set_change_event('Diag_PlungerMovingAutomaticTuningA', True)
        self.set_change_event('Diag_PlungerMovingAutomaticTuningB', True)
        self.set_change_event('Diag_PlungerMovingUpAutomaticTuningA', True)
        self.set_change_event('Diag_PlungerMovingUpAutomaticTuningB', True)
        self.set_change_event('Diag_DephaseMoLandauA', True)
        self.set_change_event('Diag_DephaseMoLandauB', True)
        self.set_change_event('Diag_Rvtet1A', True)
        self.set_change_event('Diag_Rvtet1B', True)
        self.set_change_event('Diag_Rvtet2A', True)
        self.set_change_event('Diag_Rvtet2B', True)
        self.set_change_event('Diag_RvcircA', True)
        self.set_change_event('Diag_RvcircB', True)
        self.set_change_event('Diag_FwloadA', True)
        self.set_change_event('Diag_FwloadB', True)
        self.set_change_event('Diag_FwhybloadA', True)
        self.set_change_event('Diag_FwhybloadB', True)
        self.set_change_event('Diag_RvcavA', True)
        self.set_change_event('Diag_RvcavB', True)
        self.set_change_event('Diag_ArcsA', True)
        self.set_change_event('Diag_ArcsB', True)
        self.set_change_event('Diag_VacuumA', True)
        self.set_change_event('Diag_VacuumB', True)
        self.set_change_event('Diag_ManualInterlockA', True)
        self.set_change_event('Diag_ManualInterlockB', True)
        self.set_change_event('Diag_ExternalItckA', True)
        self.set_change_event('Diag_ExternalItckB', True)
        self.set_change_event('Diag_PlungerEndSwitchUpA', True)
        self.set_change_event('Diag_PlungerEndSwitchUpB', True)
        self.set_change_event('Diag_PlungerEndSwitchDownA', True)
        self.set_change_event('Diag_PlungerEndSwitchDownB', True)
        self.set_change_event('Diag_Timestamp1A', True)
        self.set_change_event('Diag_Timestamp1B', True)
        self.set_change_event('Diag_Timestamp2A', True)
        self.set_change_event('Diag_Timestamp2B', True)
        self.set_change_event('Diag_Timestamp3A', True)
        self.set_change_event('Diag_Timestamp3B', True)
        self.set_change_event('Diag_Timestamp4A', True)
        self.set_change_event('Diag_Timestamp4B', True)
        self.set_change_event('Diag_Timestamp5A', True)
        self.set_change_event('Diag_Timestamp5B', True)
        self.set_change_event('Diag_Timestamp6A', True)
        self.set_change_event('Diag_Timestamp6B', True)
        self.set_change_event('Diag_Timestamp7A', True)
        self.set_change_event('Diag_Timestamp7B', True)
        self.set_change_event('Diag_DacsDisableCommandA', True)
        self.set_change_event('Diag_DacsDisableCommandB', True)
        self.set_change_event('Diag_PinSwitchA', True)
        self.set_change_event('Diag_PinSwitchB', True)
        self.set_change_event('Diag_FdlTriggerToLoopsdiagboardA', True)
        self.set_change_event('Diag_FdlTriggerToLoopsdiagboardB', True)
        self.set_change_event('Diag_OutputToPlcA', True)
        self.set_change_event('Diag_OutputToPlcB', True)
        self.set_change_event('Diag_OutputToMpsA', True)
        self.set_change_event('Diag_OutputToMpsB', True)
        self.set_change_event('Diag_AmpRvtet1b', True)
        self.set_change_event('Diag_AmpRvtet1a', True)
        self.set_change_event('Diag_AmpMoa', True)
        self.set_change_event('Diag_AmpLandaua', True)
        self.set_change_event('Diag_AmpFwloada', True)
        self.set_change_event('Diag_AmpRvtet2b', True)
        self.set_change_event('Diag_AmpRvtet2a', True)
        self.set_change_event('Diag_AmpFwloadb', True)
        self.set_change_event('Diag_AmpRvcavb', True)
        self.set_change_event('Diag_AmpRvcava', True)
        self.set_change_event('Diag_AmpFwcircb', True)
        self.set_change_event('Diag_AmpFwcirca', True)
        self.set_change_event('Diag_AmpMob', True)
        self.set_change_event('Diag_AmpRvcirca', True)
        self.set_change_event('Diag_AmpRvcircb', True)
        self.set_change_event('Diag_AmpFwhybloadb', True)
        self.set_change_event('Diag_AmpFwhybloada', True)
        self.set_change_event('Diag_AmpLandaub', True)
        self.set_change_event('Diag_PhRvtet1b', True)
        self.set_change_event('Diag_PhRvtet1a', True)
        self.set_change_event('Diag_PhMoa', True)
        self.set_change_event('Diag_PhLandaua', True)
        self.set_change_event('Diag_PhFwloada', True)
        self.set_change_event('Diag_PhRvtet2b', True)
        self.set_change_event('Diag_PhRvtet2a', True)
        self.set_change_event('Diag_PhFwloadb', True)
        self.set_change_event('Diag_PhRvcavb', True)
        self.set_change_event('Diag_PhRvcava', True)
        self.set_change_event('Diag_PhFwcircb', True)
        self.set_change_event('Diag_PhFwcirca', True)
        self.set_change_event('Diag_PhMob', True)
        self.set_change_event('Diag_PhRvcirca', True)
        self.set_change_event('Diag_PhRvcircb', True)
        self.set_change_event('Diag_PhFwhybloadb', True)
        self.set_change_event('Diag_PhFwhybloada', True)
        self.set_change_event('Diag_PhLandaub', True)

    @DebugIt()
    def get_ItckNumber(self):
        return self._itck_number

    @DebugIt()
    def set_ItckNumber(self, ItckNumber):
        self._itck_number = ItckNumber


    @DebugIt()
    def get_Rvtet1A(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 0, 'A')

    @DebugIt()
    def set_Rvtet1A(self, Rvtet1A):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Rvtet1A, 0, 'A')
        self.push_change_event("Rvtet1A", Rvtet1A)

    @DebugIt()
    def get_Rvtet1B(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 0, 'B')

    @DebugIt()
    def set_Rvtet1B(self, Rvtet1B):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Rvtet1B, 0, 'B')
        self.push_change_event("Rvtet1B", Rvtet1B)

    @DebugIt()
    def get_Rvtet2A(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 1, 'A')

    @DebugIt()
    def set_Rvtet2A(self, Rvtet2A):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Rvtet2A, 1, 'A')
        self.push_change_event("Rvtet2A", Rvtet2A)

    @DebugIt()
    def get_Rvtet2B(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 1, 'B')

    @DebugIt()
    def set_Rvtet2B(self, Rvtet2B):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Rvtet2B, 1, 'B')
        self.push_change_event("Rvtet2B", Rvtet2B)

    @DebugIt()
    def get_RvcircA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 2, 'A')

    @DebugIt()
    def set_RvcircA(self, RvcircA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, RvcircA, 2, 'A')
        self.push_change_event("RvcircA", RvcircA)

    @DebugIt()
    def get_RvcircB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 2, 'B')

    @DebugIt()
    def set_RvcircB(self, RvcircB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, RvcircB, 2, 'B')
        self.push_change_event("RvcircB", RvcircB)

    @DebugIt()
    def get_FwloadA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 3, 'A')

    @DebugIt()
    def set_FwloadA(self, FwloadA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, FwloadA, 3, 'A')
        self.push_change_event("FwloadA", FwloadA)

    @DebugIt()
    def get_FwloadB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 3, 'B')

    @DebugIt()
    def set_FwloadB(self, FwloadB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, FwloadB, 3, 'B')
        self.push_change_event("FwloadB", FwloadB)

    @DebugIt()
    def get_FwhybloadA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 4, 'A')

    @DebugIt()
    def set_FwhybloadA(self, FwhybloadA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, FwhybloadA, 4, 'A')
        self.push_change_event("FwhybloadA", FwhybloadA)

    @DebugIt()
    def get_FwhybloadB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 4, 'B')

    @DebugIt()
    def set_FwhybloadB(self, FwhybloadB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, FwhybloadB, 4, 'B')
        self.push_change_event("FwhybloadB", FwhybloadB)

    @DebugIt()
    def get_RvcavA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 5, 'A')

    @DebugIt()
    def set_RvcavA(self, RvcavA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, RvcavA, 5, 'A')
        self.push_change_event("RvcavA", RvcavA)

    @DebugIt()
    def get_RvcavB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 5, 'B')

    @DebugIt()
    def set_RvcavB(self, RvcavB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, RvcavB, 5, 'B')
        self.push_change_event("RvcavB", RvcavB)

    @DebugIt()
    def get_ManualInterlockA(self):
        return perseus_utils.read_direct(self.perseus, 6, 'A')

    @DebugIt()
    def set_ManualInterlockA(self, ManualInterlockA):
        perseus_utils.write_direct(self.perseus, ManualInterlockA, 6, 'A')
        self.push_change_event("ManualInterlockA", ManualInterlockA)

    @DebugIt()
    def get_ManualInterlockB(self):
        return perseus_utils.read_direct(self.perseus, 6, 'B')

    @DebugIt()
    def set_ManualInterlockB(self, ManualInterlockB):
        perseus_utils.write_direct(self.perseus, ManualInterlockB, 6, 'B')
        self.push_change_event("ManualInterlockB", ManualInterlockB)

    @DebugIt()
    def get_DisableItckRvtet1A(self):
        return perseus_utils.read_direct(self.perseus, 7, 'A')

    @DebugIt()
    def set_DisableItckRvtet1A(self, DisableItckRvtet1A):
        perseus_utils.write_direct(self.perseus, DisableItckRvtet1A, 7, 'A')
        self.push_change_event("DisableItckRvtet1A", DisableItckRvtet1A)

    @DebugIt()
    def get_DisableItckRvtet1B(self):
        return perseus_utils.read_direct(self.perseus, 7, 'B')

    @DebugIt()
    def set_DisableItckRvtet1B(self, DisableItckRvtet1B):
        perseus_utils.write_direct(self.perseus, DisableItckRvtet1B, 7, 'B')
        self.push_change_event("DisableItckRvtet1B", DisableItckRvtet1B)

    @DebugIt()
    def get_DisableItckRvtet2A(self):
        return perseus_utils.read_direct(self.perseus, 8, 'A')

    @DebugIt()
    def set_DisableItckRvtet2A(self, DisableItckRvtet2A):
        perseus_utils.write_direct(self.perseus, DisableItckRvtet2A, 8, 'A')
        self.push_change_event("DisableItckRvtet2A", DisableItckRvtet2A)

    @DebugIt()
    def get_DisableItckRvtet2B(self):
        return perseus_utils.read_direct(self.perseus, 8, 'B')

    @DebugIt()
    def set_DisableItckRvtet2B(self, DisableItckRvtet2B):
        perseus_utils.write_direct(self.perseus, DisableItckRvtet2B, 8, 'B')
        self.push_change_event("DisableItckRvtet2B", DisableItckRvtet2B)

    @DebugIt()
    def get_DisableItckRvcircA(self):
        return perseus_utils.read_direct(self.perseus, 9, 'A')

    @DebugIt()
    def set_DisableItckRvcircA(self, DisableItckRvcircA):
        perseus_utils.write_direct(self.perseus, DisableItckRvcircA, 9, 'A')
        self.push_change_event("DisableItckRvcircA", DisableItckRvcircA)

    @DebugIt()
    def get_DisableItckRvcircB(self):
        return perseus_utils.read_direct(self.perseus, 9, 'B')

    @DebugIt()
    def set_DisableItckRvcircB(self, DisableItckRvcircB):
        perseus_utils.write_direct(self.perseus, DisableItckRvcircB, 9, 'B')
        self.push_change_event("DisableItckRvcircB", DisableItckRvcircB)

    @DebugIt()
    def get_DisableItckFwloadA(self):
        return perseus_utils.read_direct(self.perseus, 10, 'A')

    @DebugIt()
    def set_DisableItckFwloadA(self, DisableItckFwloadA):
        perseus_utils.write_direct(self.perseus, DisableItckFwloadA, 10, 'A')
        self.push_change_event("DisableItckFwloadA", DisableItckFwloadA)

    @DebugIt()
    def get_DisableItckFwloadB(self):
        return perseus_utils.read_direct(self.perseus, 10, 'B')

    @DebugIt()
    def set_DisableItckFwloadB(self, DisableItckFwloadB):
        perseus_utils.write_direct(self.perseus, DisableItckFwloadB, 10, 'B')
        self.push_change_event("DisableItckFwloadB", DisableItckFwloadB)

    @DebugIt()
    def get_DisableItckFwhybloadA(self):
        return perseus_utils.read_direct(self.perseus, 11, 'A')

    @DebugIt()
    def set_DisableItckFwhybloadA(self, DisableItckFwhybloadA):
        perseus_utils.write_direct(self.perseus, DisableItckFwhybloadA, 11, 'A')
        self.push_change_event("DisableItckFwhybloadA", DisableItckFwhybloadA)

    @DebugIt()
    def get_DisableItckFwhybloadB(self):
        return perseus_utils.read_direct(self.perseus, 11, 'B')

    @DebugIt()
    def set_DisableItckFwhybloadB(self, DisableItckFwhybloadB):
        perseus_utils.write_direct(self.perseus, DisableItckFwhybloadB, 11, 'B')
        self.push_change_event("DisableItckFwhybloadB", DisableItckFwhybloadB)

    @DebugIt()
    def get_DisableItckRvcavA(self):
        return perseus_utils.read_direct(self.perseus, 12, 'A')

    @DebugIt()
    def set_DisableItckRvcavA(self, DisableItckRvcavA):
        perseus_utils.write_direct(self.perseus, DisableItckRvcavA, 12, 'A')
        self.push_change_event("DisableItckRvcavA", DisableItckRvcavA)

    @DebugIt()
    def get_DisableItckRvcavB(self):
        return perseus_utils.read_direct(self.perseus, 12, 'B')

    @DebugIt()
    def set_DisableItckRvcavB(self, DisableItckRvcavB):
        perseus_utils.write_direct(self.perseus, DisableItckRvcavB, 12, 'B')
        self.push_change_event("DisableItckRvcavB", DisableItckRvcavB)

    @DebugIt()
    def get_DisableItckArcsA(self):
        return perseus_utils.read_direct(self.perseus, 13, 'A')

    @DebugIt()
    def set_DisableItckArcsA(self, DisableItckArcsA):
        perseus_utils.write_direct(self.perseus, DisableItckArcsA, 13, 'A')
        self.push_change_event("DisableItckArcsA", DisableItckArcsA)

    @DebugIt()
    def get_DisableItckArcsB(self):
        return perseus_utils.read_direct(self.perseus, 13, 'B')

    @DebugIt()
    def set_DisableItckArcsB(self, DisableItckArcsB):
        perseus_utils.write_direct(self.perseus, DisableItckArcsB, 13, 'B')
        self.push_change_event("DisableItckArcsB", DisableItckArcsB)

    @DebugIt()
    def get_DisableItckVaccumA(self):
        return perseus_utils.read_direct(self.perseus, 14, 'A')

    @DebugIt()
    def set_DisableItckVaccumA(self, DisableItckVaccumA):
        perseus_utils.write_direct(self.perseus, DisableItckVaccumA, 14, 'A')
        self.push_change_event("DisableItckVaccumA", DisableItckVaccumA)

    @DebugIt()
    def get_DisableItckVaccumB(self):
        return perseus_utils.read_direct(self.perseus, 14, 'B')

    @DebugIt()
    def set_DisableItckVaccumB(self, DisableItckVaccumB):
        perseus_utils.write_direct(self.perseus, DisableItckVaccumB, 14, 'B')
        self.push_change_event("DisableItckVaccumB", DisableItckVaccumB)

    @DebugIt()
    def get_DisableItckManualInterlockA(self):
        return perseus_utils.read_direct(self.perseus, 15, 'A')

    @DebugIt()
    def set_DisableItckManualInterlockA(self, DisableItckManualInterlockA):
        perseus_utils.write_direct(self.perseus, DisableItckManualInterlockA, 15, 'A')
        self.push_change_event("DisableItckManualInterlockA", DisableItckManualInterlockA)

    @DebugIt()
    def get_DisableItckManualInterlockB(self):
        return perseus_utils.read_direct(self.perseus, 15, 'B')

    @DebugIt()
    def set_DisableItckManualInterlockB(self, DisableItckManualInterlockB):
        perseus_utils.write_direct(self.perseus, DisableItckManualInterlockB, 15, 'B')
        self.push_change_event("DisableItckManualInterlockB", DisableItckManualInterlockB)

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesUpA(self):
        return perseus_utils.read_direct(self.perseus, 16, 'A')

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesUpA(self, DisableItckPlungerEndSwitchesUpA):
        perseus_utils.write_direct(self.perseus, DisableItckPlungerEndSwitchesUpA, 16, 'A')
        self.push_change_event("DisableItckPlungerEndSwitchesUpA", DisableItckPlungerEndSwitchesUpA)

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesUpB(self):
        return perseus_utils.read_direct(self.perseus, 16, 'B')

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesUpB(self, DisableItckPlungerEndSwitchesUpB):
        perseus_utils.write_direct(self.perseus, DisableItckPlungerEndSwitchesUpB, 16, 'B')
        self.push_change_event("DisableItckPlungerEndSwitchesUpB", DisableItckPlungerEndSwitchesUpB)

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesDownA(self):
        return perseus_utils.read_direct(self.perseus, 17, 'A')

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesDownA(self, DisableItckPlungerEndSwitchesDownA):
        perseus_utils.write_direct(self.perseus, DisableItckPlungerEndSwitchesDownA, 17, 'A')
        self.push_change_event("DisableItckPlungerEndSwitchesDownA", DisableItckPlungerEndSwitchesDownA)

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesDownB(self):
        return perseus_utils.read_direct(self.perseus, 17, 'B')

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesDownB(self, DisableItckPlungerEndSwitchesDownB):
        perseus_utils.write_direct(self.perseus, DisableItckPlungerEndSwitchesDownB, 17, 'B')
        self.push_change_event("DisableItckPlungerEndSwitchesDownB", DisableItckPlungerEndSwitchesDownB)

    @DebugIt()
    def get_DisableItckMpsA(self):
        return perseus_utils.read_direct(self.perseus, 18, 'A')

    @DebugIt()
    def set_DisableItckMpsA(self, DisableItckMpsA):
        perseus_utils.write_direct(self.perseus, DisableItckMpsA, 18, 'A')
        self.push_change_event("DisableItckMpsA", DisableItckMpsA)

    @DebugIt()
    def get_DisableItckMpsB(self):
        return perseus_utils.read_direct(self.perseus, 18, 'B')

    @DebugIt()
    def set_DisableItckMpsB(self, DisableItckMpsB):
        perseus_utils.write_direct(self.perseus, DisableItckMpsB, 18, 'B')
        self.push_change_event("DisableItckMpsB", DisableItckMpsB)

    @DebugIt()
    def get_SamplesToAverageA(self):
        return perseus_utils.read_direct(self.perseus, 19, 'A')

    @DebugIt()
    def set_SamplesToAverageA(self, SamplesToAverageA):
        perseus_utils.write_direct(self.perseus, SamplesToAverageA, 19, 'A')
        self.push_change_event("SamplesToAverageA", SamplesToAverageA)

    @DebugIt()
    def get_SamplesToAverageB(self):
        return perseus_utils.read_direct(self.perseus, 19, 'B')

    @DebugIt()
    def set_SamplesToAverageB(self, SamplesToAverageB):
        perseus_utils.write_direct(self.perseus, SamplesToAverageB, 19, 'B')
        self.push_change_event("SamplesToAverageB", SamplesToAverageB)

    @DebugIt()
    def get_PulseupLogicInversionA(self):
        return perseus_utils.read_direct(self.perseus, 20, 'A')

    @DebugIt()
    def set_PulseupLogicInversionA(self, PulseupLogicInversionA):
        perseus_utils.write_direct(self.perseus, PulseupLogicInversionA, 20, 'A')
        self.push_change_event("PulseupLogicInversionA", PulseupLogicInversionA)

    @DebugIt()
    def get_PulseupLogicInversionB(self):
        return perseus_utils.read_direct(self.perseus, 20, 'B')

    @DebugIt()
    def set_PulseupLogicInversionB(self, PulseupLogicInversionB):
        perseus_utils.write_direct(self.perseus, PulseupLogicInversionB, 20, 'B')
        self.push_change_event("PulseupLogicInversionB", PulseupLogicInversionB)

    @DebugIt()
    def get_EndSwitchesConnectedToNoNcContactA(self):
        return perseus_utils.read_direct(self.perseus, 21, 'A')

    @DebugIt()
    def set_EndSwitchesConnectedToNoNcContactA(self, EndSwitchesConnectedToNoNcContactA):
        perseus_utils.write_direct(self.perseus, EndSwitchesConnectedToNoNcContactA, 21, 'A')
        self.push_change_event("EndSwitchesConnectedToNoNcContactA", EndSwitchesConnectedToNoNcContactA)

    @DebugIt()
    def get_EndSwitchesConnectedToNoNcContactB(self):
        return perseus_utils.read_direct(self.perseus, 21, 'B')

    @DebugIt()
    def set_EndSwitchesConnectedToNoNcContactB(self, EndSwitchesConnectedToNoNcContactB):
        perseus_utils.write_direct(self.perseus, EndSwitchesConnectedToNoNcContactB, 21, 'B')
        self.push_change_event("EndSwitchesConnectedToNoNcContactB", EndSwitchesConnectedToNoNcContactB)

    @DebugIt()
    def get_LookrefA(self):
        return perseus_utils.read_direct(self.perseus, 22, 'A')

    @DebugIt()
    def set_LookrefA(self, LookrefA):
        perseus_utils.write_direct(self.perseus, LookrefA, 22, 'A')
        self.push_change_event("LookrefA", LookrefA)

    @DebugIt()
    def get_LookrefB(self):
        return perseus_utils.read_direct(self.perseus, 22, 'B')

    @DebugIt()
    def set_LookrefB(self, LookrefB):
        perseus_utils.write_direct(self.perseus, LookrefB, 22, 'B')
        self.push_change_event("LookrefB", LookrefB)

    @DebugIt()
    def get_QuadrefA(self):
        return perseus_utils.read_direct(self.perseus, 23, 'A')

    @DebugIt()
    def set_QuadrefA(self, QuadrefA):
        perseus_utils.write_direct(self.perseus, QuadrefA, 23, 'A')
        self.push_change_event("QuadrefA", QuadrefA)

    @DebugIt()
    def get_QuadrefB(self):
        return perseus_utils.read_direct(self.perseus, 23, 'B')

    @DebugIt()
    def set_QuadrefB(self, QuadrefB):
        perseus_utils.write_direct(self.perseus, QuadrefB, 23, 'B')
        self.push_change_event("QuadrefB", QuadrefB)

    @DebugIt()
    def get_SpareDo1A(self):
        return perseus_utils.read_direct(self.perseus, 24, 'A')

    @DebugIt()
    def set_SpareDo1A(self, SpareDo1A):
        perseus_utils.write_direct(self.perseus, SpareDo1A, 24, 'A')
        self.push_change_event("SpareDo1A", SpareDo1A)

    @DebugIt()
    def get_SpareDo1B(self):
        return perseus_utils.read_direct(self.perseus, 24, 'B')

    @DebugIt()
    def set_SpareDo1B(self, SpareDo1B):
        perseus_utils.write_direct(self.perseus, SpareDo1B, 24, 'B')
        self.push_change_event("SpareDo1B", SpareDo1B)

    @DebugIt()
    def get_SpareDo2A(self):
        return perseus_utils.read_direct(self.perseus, 25, 'A')

    @DebugIt()
    def set_SpareDo2A(self, SpareDo2A):
        perseus_utils.write_direct(self.perseus, SpareDo2A, 25, 'A')
        self.push_change_event("SpareDo2A", SpareDo2A)

    @DebugIt()
    def get_SpareDo2B(self):
        return perseus_utils.read_direct(self.perseus, 25, 'B')

    @DebugIt()
    def set_SpareDo2B(self, SpareDo2B):
        perseus_utils.write_direct(self.perseus, SpareDo2B, 25, 'B')
        self.push_change_event("SpareDo2B", SpareDo2B)

    @DebugIt()
    def get_SpareDo3A(self):
        return perseus_utils.read_direct(self.perseus, 26, 'A')

    @DebugIt()
    def set_SpareDo3A(self, SpareDo3A):
        perseus_utils.write_direct(self.perseus, SpareDo3A, 26, 'A')
        self.push_change_event("SpareDo3A", SpareDo3A)

    @DebugIt()
    def get_SpareDo3B(self):
        return perseus_utils.read_direct(self.perseus, 26, 'B')

    @DebugIt()
    def set_SpareDo3B(self, SpareDo3B):
        perseus_utils.write_direct(self.perseus, SpareDo3B, 26, 'B')
        self.push_change_event("SpareDo3B", SpareDo3B)

    @DebugIt()
    def get_FdlSwTriggerA(self):
        return perseus_utils.read_direct(self.perseus, 27, 'A')

    @DebugIt()
    def set_FdlSwTriggerA(self, FdlSwTriggerA):
        perseus_utils.write_direct(self.perseus, FdlSwTriggerA, 27, 'A')
        self.push_change_event("FdlSwTriggerA", FdlSwTriggerA)

    @DebugIt()
    def get_FdlSwTriggerB(self):
        return perseus_utils.read_direct(self.perseus, 27, 'B')

    @DebugIt()
    def set_FdlSwTriggerB(self, FdlSwTriggerB):
        perseus_utils.write_direct(self.perseus, FdlSwTriggerB, 27, 'B')
        self.push_change_event("FdlSwTriggerB", FdlSwTriggerB)

    @DebugIt()
    def get_ResetInterlocksCavA(self):
        return perseus_utils.read_direct(self.perseus, 100, 'A')

    @DebugIt()
    def set_ResetInterlocksCavA(self, ResetInterlocksCavA):
        perseus_utils.write_direct(self.perseus, ResetInterlocksCavA, 100, 'A')
        self.push_change_event("ResetInterlocksCavA", ResetInterlocksCavA)

    @DebugIt()
    def get_ResetInterlocksCavB(self):
        return perseus_utils.read_direct(self.perseus, 100, 'B')

    @DebugIt()
    def set_ResetInterlocksCavB(self, ResetInterlocksCavB):
        perseus_utils.write_direct(self.perseus, ResetInterlocksCavB, 100, 'B')
        self.push_change_event("ResetInterlocksCavB", ResetInterlocksCavB)

    @DebugIt()
    def get_LandautuningenableA(self):
        return perseus_utils.read_direct(self.perseus, 200, 'A')

    @DebugIt()
    def set_LandautuningenableA(self, LandautuningenableA):
        perseus_utils.write_direct(self.perseus, LandautuningenableA, 200, 'A')
        self.push_change_event("LandautuningenableA", LandautuningenableA)

    @DebugIt()
    def get_LandautuningenableB(self):
        return perseus_utils.read_direct(self.perseus, 200, 'B')

    @DebugIt()
    def set_LandautuningenableB(self, LandautuningenableB):
        perseus_utils.write_direct(self.perseus, LandautuningenableB, 200, 'B')
        self.push_change_event("LandautuningenableB", LandautuningenableB)

    @DebugIt()
    def get_LandautuningresetA(self):
        return perseus_utils.read_direct(self.perseus, 201, 'A')

    @DebugIt()
    def set_LandautuningresetA(self, LandautuningresetA):
        perseus_utils.write_direct(self.perseus, LandautuningresetA, 201, 'A')
        self.push_change_event("LandautuningresetA", LandautuningresetA)

    @DebugIt()
    def get_LandautuningresetB(self):
        return perseus_utils.read_direct(self.perseus, 201, 'B')

    @DebugIt()
    def set_LandautuningresetB(self, LandautuningresetB):
        perseus_utils.write_direct(self.perseus, LandautuningresetB, 201, 'B')
        self.push_change_event("LandautuningresetB", LandautuningresetB)

    @DebugIt()
    def get_MovelandauupA(self):
        return perseus_utils.read_direct(self.perseus, 202, 'A')

    @DebugIt()
    def set_MovelandauupA(self, MovelandauupA):
        perseus_utils.write_direct(self.perseus, MovelandauupA, 202, 'A')
        self.push_change_event("MovelandauupA", MovelandauupA)

    @DebugIt()
    def get_MovelandauupB(self):
        return perseus_utils.read_direct(self.perseus, 202, 'B')

    @DebugIt()
    def set_MovelandauupB(self, MovelandauupB):
        perseus_utils.write_direct(self.perseus, MovelandauupB, 202, 'B')
        self.push_change_event("MovelandauupB", MovelandauupB)

    @DebugIt()
    def get_MovelandauplgA(self):
        return perseus_utils.read_direct(self.perseus, 203, 'A')

    @DebugIt()
    def set_MovelandauplgA(self, MovelandauplgA):
        perseus_utils.write_direct(self.perseus, MovelandauplgA, 203, 'A')
        self.push_change_event("MovelandauplgA", MovelandauplgA)

    @DebugIt()
    def get_MovelandauplgB(self):
        return perseus_utils.read_direct(self.perseus, 203, 'B')

    @DebugIt()
    def set_MovelandauplgB(self, MovelandauplgB):
        perseus_utils.write_direct(self.perseus, MovelandauplgB, 203, 'B')
        self.push_change_event("MovelandauplgB", MovelandauplgB)

    @DebugIt()
    def get_NumstepsA(self):
        return perseus_utils.read_direct(self.perseus, 204, 'A')

    @DebugIt()
    def set_NumstepsA(self, NumstepsA):
        perseus_utils.write_direct(self.perseus, NumstepsA, 204, 'A')
        self.push_change_event("NumstepsA", NumstepsA)

    @DebugIt()
    def get_NumstepsB(self):
        return perseus_utils.read_direct(self.perseus, 204, 'B')

    @DebugIt()
    def set_NumstepsB(self, NumstepsB):
        perseus_utils.write_direct(self.perseus, NumstepsB, 204, 'B')
        self.push_change_event("NumstepsB", NumstepsB)

    @DebugIt()
    def get_LandauphaseoffsetA(self):
        return perseus_utils.read_angle(self.perseus, 205, 'A')

    @DebugIt()
    def set_LandauphaseoffsetA(self, LandauphaseoffsetA):
        perseus_utils.write_angle(self.perseus, LandauphaseoffsetA, 205, 'A')
        self.push_change_event("LandauphaseoffsetA", LandauphaseoffsetA)

    @DebugIt()
    def get_LandauphaseoffsetB(self):
        return perseus_utils.read_angle(self.perseus, 205, 'B')

    @DebugIt()
    def set_LandauphaseoffsetB(self, LandauphaseoffsetB):
        perseus_utils.write_angle(self.perseus, LandauphaseoffsetB, 205, 'B')
        self.push_change_event("LandauphaseoffsetB", LandauphaseoffsetB)

    @DebugIt()
    def get_LandaumarginupA(self):
        return perseus_utils.read_settings_diag_percentage(self.perseus, 206, 'A')

    @DebugIt()
    def set_LandaumarginupA(self, LandaumarginupA):
        perseus_utils.write_settings_diag_percentage(self.perseus, LandaumarginupA, 206, 'A')
        self.push_change_event("LandaumarginupA", LandaumarginupA)

    @DebugIt()
    def get_LandaumarginupB(self):
        return perseus_utils.read_settings_diag_percentage(self.perseus, 206, 'B')

    @DebugIt()
    def set_LandaumarginupB(self, LandaumarginupB):
        perseus_utils.write_settings_diag_percentage(self.perseus, LandaumarginupB, 206, 'B')
        self.push_change_event("LandaumarginupB", LandaumarginupB)

    @DebugIt()
    def get_LandauMarginLowA(self):
        return perseus_utils.read_settings_diag_percentage(self.perseus, 207, 'A')

    @DebugIt()
    def set_LandauMarginLowA(self, LandauMarginLowA):
        perseus_utils.write_settings_diag_percentage(self.perseus, LandauMarginLowA, 207, 'A')
        self.push_change_event("LandauMarginLowA", LandauMarginLowA)

    @DebugIt()
    def get_LandauMarginLowB(self):
        return perseus_utils.read_settings_diag_percentage(self.perseus, 207, 'B')

    @DebugIt()
    def set_LandauMarginLowB(self, LandauMarginLowB):
        perseus_utils.write_settings_diag_percentage(self.perseus, LandauMarginLowB, 207, 'B')
        self.push_change_event("LandauMarginLowB", LandauMarginLowB)

    @DebugIt()
    def get_MinimumLandauAmplitudeA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 208, 'A')

    @DebugIt()
    def set_MinimumLandauAmplitudeA(self, MinimumLandauAmplitudeA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, MinimumLandauAmplitudeA, 208, 'A')
        self.push_change_event("MinimumLandauAmplitudeA", MinimumLandauAmplitudeA)

    @DebugIt()
    def get_MinimumLandauAmplitudeB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 208, 'B')

    @DebugIt()
    def set_MinimumLandauAmplitudeB(self, MinimumLandauAmplitudeB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, MinimumLandauAmplitudeB, 208, 'B')
        self.push_change_event("MinimumLandauAmplitudeB", MinimumLandauAmplitudeB)

    @DebugIt()
    def get_LandauPositiveEnableA(self):
        return perseus_utils.read_direct(self.perseus, 209, 'A')

    @DebugIt()
    def set_LandauPositiveEnableA(self, LandauPositiveEnableA):
        perseus_utils.write_direct(self.perseus, LandauPositiveEnableA, 209, 'A')
        self.push_change_event("LandauPositiveEnableA", LandauPositiveEnableA)

    @DebugIt()
    def get_LandauPositiveEnableB(self):
        return perseus_utils.read_direct(self.perseus, 209, 'B')

    @DebugIt()
    def set_LandauPositiveEnableB(self, LandauPositiveEnableB):
        perseus_utils.write_direct(self.perseus, LandauPositiveEnableB, 209, 'B')
        self.push_change_event("LandauPositiveEnableB", LandauPositiveEnableB)

    @DebugIt()
    def get_LandauampsettingA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 210, 'A')

    @DebugIt()
    def set_LandauampsettingA(self, LandauampsettingA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, LandauampsettingA, 210, 'A')
        self.push_change_event("LandauampsettingA", LandauampsettingA)

    @DebugIt()
    def get_LandauampsettingB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 210, 'B')

    @DebugIt()
    def set_LandauampsettingB(self, LandauampsettingB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, LandauampsettingB, 210, 'B')
        self.push_change_event("LandauampsettingB", LandauampsettingB)

    @DebugIt()
    def get_DisitckRvtet1DacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'A')
        self._DisitckRvtet1DacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckRvtet1DacsoffloopsstbyA

    @DebugIt()
    def set_DisitckRvtet1DacsoffloopsstbyA(self, DisitckRvtet1DacsoffloopsstbyA):
        self._DisitckRvtet1DacsoffloopsstbyA = DisitckRvtet1DacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1DacsoffloopsstbyA", DisitckRvtet1DacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckRvtet1DacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'B')
        self._DisitckRvtet1DacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckRvtet1DacsoffloopsstbyB

    @DebugIt()
    def set_DisitckRvtet1DacsoffloopsstbyB(self, DisitckRvtet1DacsoffloopsstbyB):
        self._DisitckRvtet1DacsoffloopsstbyB = DisitckRvtet1DacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1DacsoffloopsstbyB", DisitckRvtet1DacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckRvtet1PindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'A')
        self._DisitckRvtet1PindiodeswitchA = (value >> 1) & 1
        return self._DisitckRvtet1PindiodeswitchA

    @DebugIt()
    def set_DisitckRvtet1PindiodeswitchA(self, DisitckRvtet1PindiodeswitchA):
        self._DisitckRvtet1PindiodeswitchA = DisitckRvtet1PindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1PindiodeswitchA", DisitckRvtet1PindiodeswitchA)

    @DebugIt()
    def get_DisitckRvtet1PindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'B')
        self._DisitckRvtet1PindiodeswitchB = (value >> 1) & 1
        return self._DisitckRvtet1PindiodeswitchB

    @DebugIt()
    def set_DisitckRvtet1PindiodeswitchB(self, DisitckRvtet1PindiodeswitchB):
        self._DisitckRvtet1PindiodeswitchB = DisitckRvtet1PindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1PindiodeswitchB", DisitckRvtet1PindiodeswitchB)

    @DebugIt()
    def get_DisitckRvtet1FdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'A')
        self._DisitckRvtet1FdltrgA = (value >> 2) & 1
        return self._DisitckRvtet1FdltrgA

    @DebugIt()
    def set_DisitckRvtet1FdltrgA(self, DisitckRvtet1FdltrgA):
        self._DisitckRvtet1FdltrgA = DisitckRvtet1FdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1FdltrgA", DisitckRvtet1FdltrgA)

    @DebugIt()
    def get_DisitckRvtet1FdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'B')
        self._DisitckRvtet1FdltrgB = (value >> 2) & 1
        return self._DisitckRvtet1FdltrgB

    @DebugIt()
    def set_DisitckRvtet1FdltrgB(self, DisitckRvtet1FdltrgB):
        self._DisitckRvtet1FdltrgB = DisitckRvtet1FdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1FdltrgB", DisitckRvtet1FdltrgB)

    @DebugIt()
    def get_DisitckRvtet1PlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'A')
        self._DisitckRvtet1PlctxoffA = (value >> 3) & 1
        return self._DisitckRvtet1PlctxoffA

    @DebugIt()
    def set_DisitckRvtet1PlctxoffA(self, DisitckRvtet1PlctxoffA):
        self._DisitckRvtet1PlctxoffA = DisitckRvtet1PlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1PlctxoffA", DisitckRvtet1PlctxoffA)

    @DebugIt()
    def get_DisitckRvtet1PlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'B')
        self._DisitckRvtet1PlctxoffB = (value >> 3) & 1
        return self._DisitckRvtet1PlctxoffB

    @DebugIt()
    def set_DisitckRvtet1PlctxoffB(self, DisitckRvtet1PlctxoffB):
        self._DisitckRvtet1PlctxoffB = DisitckRvtet1PlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1PlctxoffB", DisitckRvtet1PlctxoffB)

    @DebugIt()
    def get_DisitckRvtet1MpsA(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'A')
        self._DisitckRvtet1MpsA = (value >> 4) & 1
        return self._DisitckRvtet1MpsA

    @DebugIt()
    def set_DisitckRvtet1MpsA(self, DisitckRvtet1MpsA):
        self._DisitckRvtet1MpsA = DisitckRvtet1MpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1MpsA", DisitckRvtet1MpsA)

    @DebugIt()
    def get_DisitckRvtet1MpsB(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'B')
        self._DisitckRvtet1MpsB = (value >> 4) & 1
        return self._DisitckRvtet1MpsB

    @DebugIt()
    def set_DisitckRvtet1MpsB(self, DisitckRvtet1MpsB):
        self._DisitckRvtet1MpsB = DisitckRvtet1MpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1MpsB", DisitckRvtet1MpsB)

    @DebugIt()
    def get_DisitckRvtet1DiagA(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'A')
        self._DisitckRvtet1DiagA = (value >> 5) & 1
        return self._DisitckRvtet1DiagA

    @DebugIt()
    def set_DisitckRvtet1DiagA(self, DisitckRvtet1DiagA):
        self._DisitckRvtet1DiagA = DisitckRvtet1DiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1DiagA", DisitckRvtet1DiagA)

    @DebugIt()
    def get_DisitckRvtet1DiagB(self):
        value = perseus_utils.read_direct(self.perseus, 7, 'B')
        self._DisitckRvtet1DiagB = (value >> 5) & 1
        return self._DisitckRvtet1DiagB

    @DebugIt()
    def set_DisitckRvtet1DiagB(self, DisitckRvtet1DiagB):
        self._DisitckRvtet1DiagB = DisitckRvtet1DiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet1DiagB", DisitckRvtet1DiagB)

    @DebugIt()
    def get_DisitckRvtet2DacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'A')
        self._DisitckRvtet2DacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckRvtet2DacsoffloopsstbyA

    @DebugIt()
    def set_DisitckRvtet2DacsoffloopsstbyA(self, DisitckRvtet2DacsoffloopsstbyA):
        self._DisitckRvtet2DacsoffloopsstbyA = DisitckRvtet2DacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2DacsoffloopsstbyA", DisitckRvtet2DacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckRvtet2DacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'B')
        self._DisitckRvtet2DacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckRvtet2DacsoffloopsstbyB

    @DebugIt()
    def set_DisitckRvtet2DacsoffloopsstbyB(self, DisitckRvtet2DacsoffloopsstbyB):
        self._DisitckRvtet2DacsoffloopsstbyB = DisitckRvtet2DacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2DacsoffloopsstbyB", DisitckRvtet2DacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckRvtet2PindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'A')
        self._DisitckRvtet2PindiodeswitchA = (value >> 1) & 1
        return self._DisitckRvtet2PindiodeswitchA

    @DebugIt()
    def set_DisitckRvtet2PindiodeswitchA(self, DisitckRvtet2PindiodeswitchA):
        self._DisitckRvtet2PindiodeswitchA = DisitckRvtet2PindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2PindiodeswitchA", DisitckRvtet2PindiodeswitchA)

    @DebugIt()
    def get_DisitckRvtet2PindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'B')
        self._DisitckRvtet2PindiodeswitchB = (value >> 1) & 1
        return self._DisitckRvtet2PindiodeswitchB

    @DebugIt()
    def set_DisitckRvtet2PindiodeswitchB(self, DisitckRvtet2PindiodeswitchB):
        self._DisitckRvtet2PindiodeswitchB = DisitckRvtet2PindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2PindiodeswitchB", DisitckRvtet2PindiodeswitchB)

    @DebugIt()
    def get_DisitckRvtet2FdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'A')
        self._DisitckRvtet2FdltrgA = (value >> 2) & 1
        return self._DisitckRvtet2FdltrgA

    @DebugIt()
    def set_DisitckRvtet2FdltrgA(self, DisitckRvtet2FdltrgA):
        self._DisitckRvtet2FdltrgA = DisitckRvtet2FdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2FdltrgA", DisitckRvtet2FdltrgA)

    @DebugIt()
    def get_DisitckRvtet2FdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'B')
        self._DisitckRvtet2FdltrgB = (value >> 2) & 1
        return self._DisitckRvtet2FdltrgB

    @DebugIt()
    def set_DisitckRvtet2FdltrgB(self, DisitckRvtet2FdltrgB):
        self._DisitckRvtet2FdltrgB = DisitckRvtet2FdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2FdltrgB", DisitckRvtet2FdltrgB)

    @DebugIt()
    def get_DisitckRvtet2PlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'A')
        self._DisitckRvtet2PlctxoffA = (value >> 3) & 1
        return self._DisitckRvtet2PlctxoffA

    @DebugIt()
    def set_DisitckRvtet2PlctxoffA(self, DisitckRvtet2PlctxoffA):
        self._DisitckRvtet2PlctxoffA = DisitckRvtet2PlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2PlctxoffA", DisitckRvtet2PlctxoffA)

    @DebugIt()
    def get_DisitckRvtet2PlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'B')
        self._DisitckRvtet2PlctxoffB = (value >> 3) & 1
        return self._DisitckRvtet2PlctxoffB

    @DebugIt()
    def set_DisitckRvtet2PlctxoffB(self, DisitckRvtet2PlctxoffB):
        self._DisitckRvtet2PlctxoffB = DisitckRvtet2PlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2PlctxoffB", DisitckRvtet2PlctxoffB)

    @DebugIt()
    def get_DisitckRvtet2MpsA(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'A')
        self._DisitckRvtet2MpsA = (value >> 4) & 1
        return self._DisitckRvtet2MpsA

    @DebugIt()
    def set_DisitckRvtet2MpsA(self, DisitckRvtet2MpsA):
        self._DisitckRvtet2MpsA = DisitckRvtet2MpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2MpsA", DisitckRvtet2MpsA)

    @DebugIt()
    def get_DisitckRvtet2MpsB(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'B')
        self._DisitckRvtet2MpsB = (value >> 4) & 1
        return self._DisitckRvtet2MpsB

    @DebugIt()
    def set_DisitckRvtet2MpsB(self, DisitckRvtet2MpsB):
        self._DisitckRvtet2MpsB = DisitckRvtet2MpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2MpsB", DisitckRvtet2MpsB)

    @DebugIt()
    def get_DisitckRvtet2DiagA(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'A')
        self._DisitckRvtet2DiagA = (value >> 5) & 1
        return self._DisitckRvtet2DiagA

    @DebugIt()
    def set_DisitckRvtet2DiagA(self, DisitckRvtet2DiagA):
        self._DisitckRvtet2DiagA = DisitckRvtet2DiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2DiagA", DisitckRvtet2DiagA)

    @DebugIt()
    def get_DisitckRvtet2DiagB(self):
        value = perseus_utils.read_direct(self.perseus, 8, 'B')
        self._DisitckRvtet2DiagB = (value >> 5) & 1
        return self._DisitckRvtet2DiagB

    @DebugIt()
    def set_DisitckRvtet2DiagB(self, DisitckRvtet2DiagB):
        self._DisitckRvtet2DiagB = DisitckRvtet2DiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvtet2DiagB", DisitckRvtet2DiagB)

    @DebugIt()
    def get_DisitckRvcircDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'A')
        self._DisitckRvcircDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckRvcircDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckRvcircDacsoffloopsstbyA(self, DisitckRvcircDacsoffloopsstbyA):
        self._DisitckRvcircDacsoffloopsstbyA = DisitckRvcircDacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircDacsoffloopsstbyA", DisitckRvcircDacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckRvcircDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'B')
        self._DisitckRvcircDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckRvcircDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckRvcircDacsoffloopsstbyB(self, DisitckRvcircDacsoffloopsstbyB):
        self._DisitckRvcircDacsoffloopsstbyB = DisitckRvcircDacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircDacsoffloopsstbyB", DisitckRvcircDacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckRvcircPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'A')
        self._DisitckRvcircPindiodeswitchA = (value >> 1) & 1
        return self._DisitckRvcircPindiodeswitchA

    @DebugIt()
    def set_DisitckRvcircPindiodeswitchA(self, DisitckRvcircPindiodeswitchA):
        self._DisitckRvcircPindiodeswitchA = DisitckRvcircPindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircPindiodeswitchA", DisitckRvcircPindiodeswitchA)

    @DebugIt()
    def get_DisitckRvcircPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'B')
        self._DisitckRvcircPindiodeswitchB = (value >> 1) & 1
        return self._DisitckRvcircPindiodeswitchB

    @DebugIt()
    def set_DisitckRvcircPindiodeswitchB(self, DisitckRvcircPindiodeswitchB):
        self._DisitckRvcircPindiodeswitchB = DisitckRvcircPindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircPindiodeswitchB", DisitckRvcircPindiodeswitchB)

    @DebugIt()
    def get_DisitckRvcircFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'A')
        self._DisitckRvcircFdltrgA = (value >> 2) & 1
        return self._DisitckRvcircFdltrgA

    @DebugIt()
    def set_DisitckRvcircFdltrgA(self, DisitckRvcircFdltrgA):
        self._DisitckRvcircFdltrgA = DisitckRvcircFdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircFdltrgA", DisitckRvcircFdltrgA)

    @DebugIt()
    def get_DisitckRvcircFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'B')
        self._DisitckRvcircFdltrgB = (value >> 2) & 1
        return self._DisitckRvcircFdltrgB

    @DebugIt()
    def set_DisitckRvcircFdltrgB(self, DisitckRvcircFdltrgB):
        self._DisitckRvcircFdltrgB = DisitckRvcircFdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircFdltrgB", DisitckRvcircFdltrgB)

    @DebugIt()
    def get_DisitckRvcircPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'A')
        self._DisitckRvcircPlctxoffA = (value >> 3) & 1
        return self._DisitckRvcircPlctxoffA

    @DebugIt()
    def set_DisitckRvcircPlctxoffA(self, DisitckRvcircPlctxoffA):
        self._DisitckRvcircPlctxoffA = DisitckRvcircPlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircPlctxoffA", DisitckRvcircPlctxoffA)

    @DebugIt()
    def get_DisitckRvcircPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'B')
        self._DisitckRvcircPlctxoffB = (value >> 3) & 1
        return self._DisitckRvcircPlctxoffB

    @DebugIt()
    def set_DisitckRvcircPlctxoffB(self, DisitckRvcircPlctxoffB):
        self._DisitckRvcircPlctxoffB = DisitckRvcircPlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircPlctxoffB", DisitckRvcircPlctxoffB)

    @DebugIt()
    def get_DisitckRvcircMpsA(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'A')
        self._DisitckRvcircMpsA = (value >> 4) & 1
        return self._DisitckRvcircMpsA

    @DebugIt()
    def set_DisitckRvcircMpsA(self, DisitckRvcircMpsA):
        self._DisitckRvcircMpsA = DisitckRvcircMpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircMpsA", DisitckRvcircMpsA)

    @DebugIt()
    def get_DisitckRvcircMpsB(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'B')
        self._DisitckRvcircMpsB = (value >> 4) & 1
        return self._DisitckRvcircMpsB

    @DebugIt()
    def set_DisitckRvcircMpsB(self, DisitckRvcircMpsB):
        self._DisitckRvcircMpsB = DisitckRvcircMpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircMpsB", DisitckRvcircMpsB)

    @DebugIt()
    def get_DisitckRvcircDiagA(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'A')
        self._DisitckRvcircDiagA = (value >> 5) & 1
        return self._DisitckRvcircDiagA

    @DebugIt()
    def set_DisitckRvcircDiagA(self, DisitckRvcircDiagA):
        self._DisitckRvcircDiagA = DisitckRvcircDiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircDiagA", DisitckRvcircDiagA)

    @DebugIt()
    def get_DisitckRvcircDiagB(self):
        value = perseus_utils.read_direct(self.perseus, 9, 'B')
        self._DisitckRvcircDiagB = (value >> 5) & 1
        return self._DisitckRvcircDiagB

    @DebugIt()
    def set_DisitckRvcircDiagB(self, DisitckRvcircDiagB):
        self._DisitckRvcircDiagB = DisitckRvcircDiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcircDiagB", DisitckRvcircDiagB)

    @DebugIt()
    def get_DisitckFwloadDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'A')
        self._DisitckFwloadDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckFwloadDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckFwloadDacsoffloopsstbyA(self, DisitckFwloadDacsoffloopsstbyA):
        self._DisitckFwloadDacsoffloopsstbyA = DisitckFwloadDacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadDacsoffloopsstbyA", DisitckFwloadDacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckFwloadDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'B')
        self._DisitckFwloadDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckFwloadDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckFwloadDacsoffloopsstbyB(self, DisitckFwloadDacsoffloopsstbyB):
        self._DisitckFwloadDacsoffloopsstbyB = DisitckFwloadDacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadDacsoffloopsstbyB", DisitckFwloadDacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckFwloadPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'A')
        self._DisitckFwloadPindiodeswitchA = (value >> 1) & 1
        return self._DisitckFwloadPindiodeswitchA

    @DebugIt()
    def set_DisitckFwloadPindiodeswitchA(self, DisitckFwloadPindiodeswitchA):
        self._DisitckFwloadPindiodeswitchA = DisitckFwloadPindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadPindiodeswitchA", DisitckFwloadPindiodeswitchA)

    @DebugIt()
    def get_DisitckFwloadPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'B')
        self._DisitckFwloadPindiodeswitchB = (value >> 1) & 1
        return self._DisitckFwloadPindiodeswitchB

    @DebugIt()
    def set_DisitckFwloadPindiodeswitchB(self, DisitckFwloadPindiodeswitchB):
        self._DisitckFwloadPindiodeswitchB = DisitckFwloadPindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadPindiodeswitchB", DisitckFwloadPindiodeswitchB)

    @DebugIt()
    def get_DisitckFwloadFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'A')
        self._DisitckFwloadFdltrgA = (value >> 2) & 1
        return self._DisitckFwloadFdltrgA

    @DebugIt()
    def set_DisitckFwloadFdltrgA(self, DisitckFwloadFdltrgA):
        self._DisitckFwloadFdltrgA = DisitckFwloadFdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadFdltrgA", DisitckFwloadFdltrgA)

    @DebugIt()
    def get_DisitckFwloadFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'B')
        self._DisitckFwloadFdltrgB = (value >> 2) & 1
        return self._DisitckFwloadFdltrgB

    @DebugIt()
    def set_DisitckFwloadFdltrgB(self, DisitckFwloadFdltrgB):
        self._DisitckFwloadFdltrgB = DisitckFwloadFdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadFdltrgB", DisitckFwloadFdltrgB)

    @DebugIt()
    def get_DisitckFwloadPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'A')
        self._DisitckFwloadPlctxoffA = (value >> 3) & 1
        return self._DisitckFwloadPlctxoffA

    @DebugIt()
    def set_DisitckFwloadPlctxoffA(self, DisitckFwloadPlctxoffA):
        self._DisitckFwloadPlctxoffA = DisitckFwloadPlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadPlctxoffA", DisitckFwloadPlctxoffA)

    @DebugIt()
    def get_DisitckFwloadPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'B')
        self._DisitckFwloadPlctxoffB = (value >> 3) & 1
        return self._DisitckFwloadPlctxoffB

    @DebugIt()
    def set_DisitckFwloadPlctxoffB(self, DisitckFwloadPlctxoffB):
        self._DisitckFwloadPlctxoffB = DisitckFwloadPlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadPlctxoffB", DisitckFwloadPlctxoffB)

    @DebugIt()
    def get_DisitckFwloadMpsA(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'A')
        self._DisitckFwloadMpsA = (value >> 4) & 1
        return self._DisitckFwloadMpsA

    @DebugIt()
    def set_DisitckFwloadMpsA(self, DisitckFwloadMpsA):
        self._DisitckFwloadMpsA = DisitckFwloadMpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadMpsA", DisitckFwloadMpsA)

    @DebugIt()
    def get_DisitckFwloadMpsB(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'B')
        self._DisitckFwloadMpsB = (value >> 4) & 1
        return self._DisitckFwloadMpsB

    @DebugIt()
    def set_DisitckFwloadMpsB(self, DisitckFwloadMpsB):
        self._DisitckFwloadMpsB = DisitckFwloadMpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadMpsB", DisitckFwloadMpsB)

    @DebugIt()
    def get_DisitckFwloadDiagA(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'A')
        self._DisitckFwloadDiagA = (value >> 5) & 1
        return self._DisitckFwloadDiagA

    @DebugIt()
    def set_DisitckFwloadDiagA(self, DisitckFwloadDiagA):
        self._DisitckFwloadDiagA = DisitckFwloadDiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadDiagA", DisitckFwloadDiagA)

    @DebugIt()
    def get_DisitckFwloadDiagB(self):
        value = perseus_utils.read_direct(self.perseus, 10, 'B')
        self._DisitckFwloadDiagB = (value >> 5) & 1
        return self._DisitckFwloadDiagB

    @DebugIt()
    def set_DisitckFwloadDiagB(self, DisitckFwloadDiagB):
        self._DisitckFwloadDiagB = DisitckFwloadDiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwloadDiagB", DisitckFwloadDiagB)

    @DebugIt()
    def get_DisitckFwhybloadDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'A')
        self._DisitckFwhybloadDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckFwhybloadDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckFwhybloadDacsoffloopsstbyA(self, DisitckFwhybloadDacsoffloopsstbyA):
        self._DisitckFwhybloadDacsoffloopsstbyA = DisitckFwhybloadDacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadDacsoffloopsstbyA", DisitckFwhybloadDacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckFwhybloadDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'B')
        self._DisitckFwhybloadDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckFwhybloadDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckFwhybloadDacsoffloopsstbyB(self, DisitckFwhybloadDacsoffloopsstbyB):
        self._DisitckFwhybloadDacsoffloopsstbyB = DisitckFwhybloadDacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadDacsoffloopsstbyB", DisitckFwhybloadDacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckFwhybloadPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'A')
        self._DisitckFwhybloadPindiodeswitchA = (value >> 1) & 1
        return self._DisitckFwhybloadPindiodeswitchA

    @DebugIt()
    def set_DisitckFwhybloadPindiodeswitchA(self, DisitckFwhybloadPindiodeswitchA):
        self._DisitckFwhybloadPindiodeswitchA = DisitckFwhybloadPindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadPindiodeswitchA", DisitckFwhybloadPindiodeswitchA)

    @DebugIt()
    def get_DisitckFwhybloadPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'B')
        self._DisitckFwhybloadPindiodeswitchB = (value >> 1) & 1
        return self._DisitckFwhybloadPindiodeswitchB

    @DebugIt()
    def set_DisitckFwhybloadPindiodeswitchB(self, DisitckFwhybloadPindiodeswitchB):
        self._DisitckFwhybloadPindiodeswitchB = DisitckFwhybloadPindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadPindiodeswitchB", DisitckFwhybloadPindiodeswitchB)

    @DebugIt()
    def get_DisitckFwhybloadFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'A')
        self._DisitckFwhybloadFdltrgA = (value >> 2) & 1
        return self._DisitckFwhybloadFdltrgA

    @DebugIt()
    def set_DisitckFwhybloadFdltrgA(self, DisitckFwhybloadFdltrgA):
        self._DisitckFwhybloadFdltrgA = DisitckFwhybloadFdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadFdltrgA", DisitckFwhybloadFdltrgA)

    @DebugIt()
    def get_DisitckFwhybloadFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'B')
        self._DisitckFwhybloadFdltrgB = (value >> 2) & 1
        return self._DisitckFwhybloadFdltrgB

    @DebugIt()
    def set_DisitckFwhybloadFdltrgB(self, DisitckFwhybloadFdltrgB):
        self._DisitckFwhybloadFdltrgB = DisitckFwhybloadFdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadFdltrgB", DisitckFwhybloadFdltrgB)

    @DebugIt()
    def get_DisitckFwhybloadPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'A')
        self._DisitckFwhybloadPlctxoffA = (value >> 3) & 1
        return self._DisitckFwhybloadPlctxoffA

    @DebugIt()
    def set_DisitckFwhybloadPlctxoffA(self, DisitckFwhybloadPlctxoffA):
        self._DisitckFwhybloadPlctxoffA = DisitckFwhybloadPlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadPlctxoffA", DisitckFwhybloadPlctxoffA)

    @DebugIt()
    def get_DisitckFwhybloadPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'B')
        self._DisitckFwhybloadPlctxoffB = (value >> 3) & 1
        return self._DisitckFwhybloadPlctxoffB

    @DebugIt()
    def set_DisitckFwhybloadPlctxoffB(self, DisitckFwhybloadPlctxoffB):
        self._DisitckFwhybloadPlctxoffB = DisitckFwhybloadPlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadPlctxoffB", DisitckFwhybloadPlctxoffB)

    @DebugIt()
    def get_DisitckFwhybloadMpsA(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'A')
        self._DisitckFwhybloadMpsA = (value >> 4) & 1
        return self._DisitckFwhybloadMpsA

    @DebugIt()
    def set_DisitckFwhybloadMpsA(self, DisitckFwhybloadMpsA):
        self._DisitckFwhybloadMpsA = DisitckFwhybloadMpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadMpsA", DisitckFwhybloadMpsA)

    @DebugIt()
    def get_DisitckFwhybloadMpsB(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'B')
        self._DisitckFwhybloadMpsB = (value >> 4) & 1
        return self._DisitckFwhybloadMpsB

    @DebugIt()
    def set_DisitckFwhybloadMpsB(self, DisitckFwhybloadMpsB):
        self._DisitckFwhybloadMpsB = DisitckFwhybloadMpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadMpsB", DisitckFwhybloadMpsB)

    @DebugIt()
    def get_DisitckFwhybloadDiagA(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'A')
        self._DisitckFwhybloadDiagA = (value >> 5) & 1
        return self._DisitckFwhybloadDiagA

    @DebugIt()
    def set_DisitckFwhybloadDiagA(self, DisitckFwhybloadDiagA):
        self._DisitckFwhybloadDiagA = DisitckFwhybloadDiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadDiagA", DisitckFwhybloadDiagA)

    @DebugIt()
    def get_DisitckFwhybloadDiagB(self):
        value = perseus_utils.read_direct(self.perseus, 11, 'B')
        self._DisitckFwhybloadDiagB = (value >> 5) & 1
        return self._DisitckFwhybloadDiagB

    @DebugIt()
    def set_DisitckFwhybloadDiagB(self, DisitckFwhybloadDiagB):
        self._DisitckFwhybloadDiagB = DisitckFwhybloadDiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckFwhybloadDiagB", DisitckFwhybloadDiagB)

    @DebugIt()
    def get_DisitckRvcavDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'A')
        self._DisitckRvcavDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckRvcavDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckRvcavDacsoffloopsstbyA(self, DisitckRvcavDacsoffloopsstbyA):
        self._DisitckRvcavDacsoffloopsstbyA = DisitckRvcavDacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavDacsoffloopsstbyA", DisitckRvcavDacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckRvcavDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'B')
        self._DisitckRvcavDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckRvcavDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckRvcavDacsoffloopsstbyB(self, DisitckRvcavDacsoffloopsstbyB):
        self._DisitckRvcavDacsoffloopsstbyB = DisitckRvcavDacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavDacsoffloopsstbyB", DisitckRvcavDacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckRvcavPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'A')
        self._DisitckRvcavPindiodeswitchA = (value >> 1) & 1
        return self._DisitckRvcavPindiodeswitchA

    @DebugIt()
    def set_DisitckRvcavPindiodeswitchA(self, DisitckRvcavPindiodeswitchA):
        self._DisitckRvcavPindiodeswitchA = DisitckRvcavPindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavPindiodeswitchA", DisitckRvcavPindiodeswitchA)

    @DebugIt()
    def get_DisitckRvcavPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'B')
        self._DisitckRvcavPindiodeswitchB = (value >> 1) & 1
        return self._DisitckRvcavPindiodeswitchB

    @DebugIt()
    def set_DisitckRvcavPindiodeswitchB(self, DisitckRvcavPindiodeswitchB):
        self._DisitckRvcavPindiodeswitchB = DisitckRvcavPindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavPindiodeswitchB", DisitckRvcavPindiodeswitchB)

    @DebugIt()
    def get_DisitckRvcavFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'A')
        self._DisitckRvcavFdltrgA = (value >> 2) & 1
        return self._DisitckRvcavFdltrgA

    @DebugIt()
    def set_DisitckRvcavFdltrgA(self, DisitckRvcavFdltrgA):
        self._DisitckRvcavFdltrgA = DisitckRvcavFdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavFdltrgA", DisitckRvcavFdltrgA)

    @DebugIt()
    def get_DisitckRvcavFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'B')
        self._DisitckRvcavFdltrgB = (value >> 2) & 1
        return self._DisitckRvcavFdltrgB

    @DebugIt()
    def set_DisitckRvcavFdltrgB(self, DisitckRvcavFdltrgB):
        self._DisitckRvcavFdltrgB = DisitckRvcavFdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavFdltrgB", DisitckRvcavFdltrgB)

    @DebugIt()
    def get_DisitckRvcavPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'A')
        self._DisitckRvcavPlctxoffA = (value >> 3) & 1
        return self._DisitckRvcavPlctxoffA

    @DebugIt()
    def set_DisitckRvcavPlctxoffA(self, DisitckRvcavPlctxoffA):
        self._DisitckRvcavPlctxoffA = DisitckRvcavPlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavPlctxoffA", DisitckRvcavPlctxoffA)

    @DebugIt()
    def get_DisitckRvcavPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'B')
        self._DisitckRvcavPlctxoffB = (value >> 3) & 1
        return self._DisitckRvcavPlctxoffB

    @DebugIt()
    def set_DisitckRvcavPlctxoffB(self, DisitckRvcavPlctxoffB):
        self._DisitckRvcavPlctxoffB = DisitckRvcavPlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavPlctxoffB", DisitckRvcavPlctxoffB)

    @DebugIt()
    def get_DisitckRvcavMpsA(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'A')
        self._DisitckRvcavMpsA = (value >> 4) & 1
        return self._DisitckRvcavMpsA

    @DebugIt()
    def set_DisitckRvcavMpsA(self, DisitckRvcavMpsA):
        self._DisitckRvcavMpsA = DisitckRvcavMpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavMpsA", DisitckRvcavMpsA)

    @DebugIt()
    def get_DisitckRvcavMpsB(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'B')
        self._DisitckRvcavMpsB = (value >> 4) & 1
        return self._DisitckRvcavMpsB

    @DebugIt()
    def set_DisitckRvcavMpsB(self, DisitckRvcavMpsB):
        self._DisitckRvcavMpsB = DisitckRvcavMpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavMpsB", DisitckRvcavMpsB)

    @DebugIt()
    def get_DisitckRvcavDiagA(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'A')
        self._DisitckRvcavDiagA = (value >> 5) & 1
        return self._DisitckRvcavDiagA

    @DebugIt()
    def set_DisitckRvcavDiagA(self, DisitckRvcavDiagA):
        self._DisitckRvcavDiagA = DisitckRvcavDiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavDiagA", DisitckRvcavDiagA)

    @DebugIt()
    def get_DisitckRvcavDiagB(self):
        value = perseus_utils.read_direct(self.perseus, 12, 'B')
        self._DisitckRvcavDiagB = (value >> 5) & 1
        return self._DisitckRvcavDiagB

    @DebugIt()
    def set_DisitckRvcavDiagB(self, DisitckRvcavDiagB):
        self._DisitckRvcavDiagB = DisitckRvcavDiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckRvcavDiagB", DisitckRvcavDiagB)

    @DebugIt()
    def get_DisitckArcsDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'A')
        self._DisitckArcsDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckArcsDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckArcsDacsoffloopsstbyA(self, DisitckArcsDacsoffloopsstbyA):
        self._DisitckArcsDacsoffloopsstbyA = DisitckArcsDacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsDacsoffloopsstbyA", DisitckArcsDacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckArcsDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'B')
        self._DisitckArcsDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckArcsDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckArcsDacsoffloopsstbyB(self, DisitckArcsDacsoffloopsstbyB):
        self._DisitckArcsDacsoffloopsstbyB = DisitckArcsDacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsDacsoffloopsstbyB", DisitckArcsDacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckArcsPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'A')
        self._DisitckArcsPindiodeswitchA = (value >> 1) & 1
        return self._DisitckArcsPindiodeswitchA

    @DebugIt()
    def set_DisitckArcsPindiodeswitchA(self, DisitckArcsPindiodeswitchA):
        self._DisitckArcsPindiodeswitchA = DisitckArcsPindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsPindiodeswitchA", DisitckArcsPindiodeswitchA)

    @DebugIt()
    def get_DisitckArcsPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'B')
        self._DisitckArcsPindiodeswitchB = (value >> 1) & 1
        return self._DisitckArcsPindiodeswitchB

    @DebugIt()
    def set_DisitckArcsPindiodeswitchB(self, DisitckArcsPindiodeswitchB):
        self._DisitckArcsPindiodeswitchB = DisitckArcsPindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsPindiodeswitchB", DisitckArcsPindiodeswitchB)

    @DebugIt()
    def get_DisitckArcsFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'A')
        self._DisitckArcsFdltrgA = (value >> 2) & 1
        return self._DisitckArcsFdltrgA

    @DebugIt()
    def set_DisitckArcsFdltrgA(self, DisitckArcsFdltrgA):
        self._DisitckArcsFdltrgA = DisitckArcsFdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsFdltrgA", DisitckArcsFdltrgA)

    @DebugIt()
    def get_DisitckArcsFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'B')
        self._DisitckArcsFdltrgB = (value >> 2) & 1
        return self._DisitckArcsFdltrgB

    @DebugIt()
    def set_DisitckArcsFdltrgB(self, DisitckArcsFdltrgB):
        self._DisitckArcsFdltrgB = DisitckArcsFdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsFdltrgB", DisitckArcsFdltrgB)

    @DebugIt()
    def get_DisitckArcsPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'A')
        self._DisitckArcsPlctxoffA = (value >> 3) & 1
        return self._DisitckArcsPlctxoffA

    @DebugIt()
    def set_DisitckArcsPlctxoffA(self, DisitckArcsPlctxoffA):
        self._DisitckArcsPlctxoffA = DisitckArcsPlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsPlctxoffA", DisitckArcsPlctxoffA)

    @DebugIt()
    def get_DisitckArcsPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'B')
        self._DisitckArcsPlctxoffB = (value >> 3) & 1
        return self._DisitckArcsPlctxoffB

    @DebugIt()
    def set_DisitckArcsPlctxoffB(self, DisitckArcsPlctxoffB):
        self._DisitckArcsPlctxoffB = DisitckArcsPlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsPlctxoffB", DisitckArcsPlctxoffB)

    @DebugIt()
    def get_DisitckArcsMpsA(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'A')
        self._DisitckArcsMpsA = (value >> 4) & 1
        return self._DisitckArcsMpsA

    @DebugIt()
    def set_DisitckArcsMpsA(self, DisitckArcsMpsA):
        self._DisitckArcsMpsA = DisitckArcsMpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsMpsA", DisitckArcsMpsA)

    @DebugIt()
    def get_DisitckArcsMpsB(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'B')
        self._DisitckArcsMpsB = (value >> 4) & 1
        return self._DisitckArcsMpsB

    @DebugIt()
    def set_DisitckArcsMpsB(self, DisitckArcsMpsB):
        self._DisitckArcsMpsB = DisitckArcsMpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsMpsB", DisitckArcsMpsB)

    @DebugIt()
    def get_DisitckArcsDiagA(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'A')
        self._DisitckArcsDiagA = (value >> 5) & 1
        return self._DisitckArcsDiagA

    @DebugIt()
    def set_DisitckArcsDiagA(self, DisitckArcsDiagA):
        self._DisitckArcsDiagA = DisitckArcsDiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsDiagA", DisitckArcsDiagA)

    @DebugIt()
    def get_DisitckArcsDiagB(self):
        value = perseus_utils.read_direct(self.perseus, 13, 'B')
        self._DisitckArcsDiagB = (value >> 5) & 1
        return self._DisitckArcsDiagB

    @DebugIt()
    def set_DisitckArcsDiagB(self, DisitckArcsDiagB):
        self._DisitckArcsDiagB = DisitckArcsDiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckArcsDiagB", DisitckArcsDiagB)

    @DebugIt()
    def get_DisitckVacuumDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'A')
        self._DisitckVacuumDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckVacuumDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckVacuumDacsoffloopsstbyA(self, DisitckVacuumDacsoffloopsstbyA):
        self._DisitckVacuumDacsoffloopsstbyA = DisitckVacuumDacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumDacsoffloopsstbyA", DisitckVacuumDacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckVacuumDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'B')
        self._DisitckVacuumDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckVacuumDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckVacuumDacsoffloopsstbyB(self, DisitckVacuumDacsoffloopsstbyB):
        self._DisitckVacuumDacsoffloopsstbyB = DisitckVacuumDacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumDacsoffloopsstbyB", DisitckVacuumDacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckVacuumPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'A')
        self._DisitckVacuumPindiodeswitchA = (value >> 1) & 1
        return self._DisitckVacuumPindiodeswitchA

    @DebugIt()
    def set_DisitckVacuumPindiodeswitchA(self, DisitckVacuumPindiodeswitchA):
        self._DisitckVacuumPindiodeswitchA = DisitckVacuumPindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumPindiodeswitchA", DisitckVacuumPindiodeswitchA)

    @DebugIt()
    def get_DisitckVacuumPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'B')
        self._DisitckVacuumPindiodeswitchB = (value >> 1) & 1
        return self._DisitckVacuumPindiodeswitchB

    @DebugIt()
    def set_DisitckVacuumPindiodeswitchB(self, DisitckVacuumPindiodeswitchB):
        self._DisitckVacuumPindiodeswitchB = DisitckVacuumPindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumPindiodeswitchB", DisitckVacuumPindiodeswitchB)

    @DebugIt()
    def get_DisitckVacuumFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'A')
        self._DisitckVacuumFdltrgA = (value >> 2) & 1
        return self._DisitckVacuumFdltrgA

    @DebugIt()
    def set_DisitckVacuumFdltrgA(self, DisitckVacuumFdltrgA):
        self._DisitckVacuumFdltrgA = DisitckVacuumFdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumFdltrgA", DisitckVacuumFdltrgA)

    @DebugIt()
    def get_DisitckVacuumFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'B')
        self._DisitckVacuumFdltrgB = (value >> 2) & 1
        return self._DisitckVacuumFdltrgB

    @DebugIt()
    def set_DisitckVacuumFdltrgB(self, DisitckVacuumFdltrgB):
        self._DisitckVacuumFdltrgB = DisitckVacuumFdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumFdltrgB", DisitckVacuumFdltrgB)

    @DebugIt()
    def get_DisitckVacuumPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'A')
        self._DisitckVacuumPlctxoffA = (value >> 3) & 1
        return self._DisitckVacuumPlctxoffA

    @DebugIt()
    def set_DisitckVacuumPlctxoffA(self, DisitckVacuumPlctxoffA):
        self._DisitckVacuumPlctxoffA = DisitckVacuumPlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumPlctxoffA", DisitckVacuumPlctxoffA)

    @DebugIt()
    def get_DisitckVacuumPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'B')
        self._DisitckVacuumPlctxoffB = (value >> 3) & 1
        return self._DisitckVacuumPlctxoffB

    @DebugIt()
    def set_DisitckVacuumPlctxoffB(self, DisitckVacuumPlctxoffB):
        self._DisitckVacuumPlctxoffB = DisitckVacuumPlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumPlctxoffB", DisitckVacuumPlctxoffB)

    @DebugIt()
    def get_DisitckVacuumMpsA(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'A')
        self._DisitckVacuumMpsA = (value >> 4) & 1
        return self._DisitckVacuumMpsA

    @DebugIt()
    def set_DisitckVacuumMpsA(self, DisitckVacuumMpsA):
        self._DisitckVacuumMpsA = DisitckVacuumMpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumMpsA", DisitckVacuumMpsA)

    @DebugIt()
    def get_DisitckVacuumMpsB(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'B')
        self._DisitckVacuumMpsB = (value >> 4) & 1
        return self._DisitckVacuumMpsB

    @DebugIt()
    def set_DisitckVacuumMpsB(self, DisitckVacuumMpsB):
        self._DisitckVacuumMpsB = DisitckVacuumMpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumMpsB", DisitckVacuumMpsB)

    @DebugIt()
    def get_DisitckVacuumDiagA(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'A')
        self._DisitckVacuumDiagA = (value >> 5) & 1
        return self._DisitckVacuumDiagA

    @DebugIt()
    def set_DisitckVacuumDiagA(self, DisitckVacuumDiagA):
        self._DisitckVacuumDiagA = DisitckVacuumDiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumDiagA", DisitckVacuumDiagA)

    @DebugIt()
    def get_DisitckVacuumDiagB(self):
        value = perseus_utils.read_direct(self.perseus, 14, 'B')
        self._DisitckVacuumDiagB = (value >> 5) & 1
        return self._DisitckVacuumDiagB

    @DebugIt()
    def set_DisitckVacuumDiagB(self, DisitckVacuumDiagB):
        self._DisitckVacuumDiagB = DisitckVacuumDiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckVacuumDiagB", DisitckVacuumDiagB)

    @DebugIt()
    def get_DisitckManualInterlockDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'A')
        self._DisitckManualInterlockDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckManualInterlockDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckManualInterlockDacsoffloopsstbyA(self, DisitckManualInterlockDacsoffloopsstbyA):
        self._DisitckManualInterlockDacsoffloopsstbyA = DisitckManualInterlockDacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockDacsoffloopsstbyA", DisitckManualInterlockDacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckManualInterlockDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'B')
        self._DisitckManualInterlockDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckManualInterlockDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckManualInterlockDacsoffloopsstbyB(self, DisitckManualInterlockDacsoffloopsstbyB):
        self._DisitckManualInterlockDacsoffloopsstbyB = DisitckManualInterlockDacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockDacsoffloopsstbyB", DisitckManualInterlockDacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckManualInterlockPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'A')
        self._DisitckManualInterlockPindiodeswitchA = (value >> 1) & 1
        return self._DisitckManualInterlockPindiodeswitchA

    @DebugIt()
    def set_DisitckManualInterlockPindiodeswitchA(self, DisitckManualInterlockPindiodeswitchA):
        self._DisitckManualInterlockPindiodeswitchA = DisitckManualInterlockPindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockPindiodeswitchA", DisitckManualInterlockPindiodeswitchA)

    @DebugIt()
    def get_DisitckManualInterlockPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'B')
        self._DisitckManualInterlockPindiodeswitchB = (value >> 1) & 1
        return self._DisitckManualInterlockPindiodeswitchB

    @DebugIt()
    def set_DisitckManualInterlockPindiodeswitchB(self, DisitckManualInterlockPindiodeswitchB):
        self._DisitckManualInterlockPindiodeswitchB = DisitckManualInterlockPindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockPindiodeswitchB", DisitckManualInterlockPindiodeswitchB)

    @DebugIt()
    def get_DisitckManualInterlockFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'A')
        self._DisitckManualInterlockFdltrgA = (value >> 2) & 1
        return self._DisitckManualInterlockFdltrgA

    @DebugIt()
    def set_DisitckManualInterlockFdltrgA(self, DisitckManualInterlockFdltrgA):
        self._DisitckManualInterlockFdltrgA = DisitckManualInterlockFdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockFdltrgA", DisitckManualInterlockFdltrgA)

    @DebugIt()
    def get_DisitckManualInterlockFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'B')
        self._DisitckManualInterlockFdltrgB = (value >> 2) & 1
        return self._DisitckManualInterlockFdltrgB

    @DebugIt()
    def set_DisitckManualInterlockFdltrgB(self, DisitckManualInterlockFdltrgB):
        self._DisitckManualInterlockFdltrgB = DisitckManualInterlockFdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockFdltrgB", DisitckManualInterlockFdltrgB)

    @DebugIt()
    def get_DisitckManualInterlockPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'A')
        self._DisitckManualInterlockPlctxoffA = (value >> 3) & 1
        return self._DisitckManualInterlockPlctxoffA

    @DebugIt()
    def set_DisitckManualInterlockPlctxoffA(self, DisitckManualInterlockPlctxoffA):
        self._DisitckManualInterlockPlctxoffA = DisitckManualInterlockPlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockPlctxoffA", DisitckManualInterlockPlctxoffA)

    @DebugIt()
    def get_DisitckManualInterlockPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'B')
        self._DisitckManualInterlockPlctxoffB = (value >> 3) & 1
        return self._DisitckManualInterlockPlctxoffB

    @DebugIt()
    def set_DisitckManualInterlockPlctxoffB(self, DisitckManualInterlockPlctxoffB):
        self._DisitckManualInterlockPlctxoffB = DisitckManualInterlockPlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockPlctxoffB", DisitckManualInterlockPlctxoffB)

    @DebugIt()
    def get_DisitckManualInterlockMpsA(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'A')
        self._DisitckManualInterlockMpsA = (value >> 4) & 1
        return self._DisitckManualInterlockMpsA

    @DebugIt()
    def set_DisitckManualInterlockMpsA(self, DisitckManualInterlockMpsA):
        self._DisitckManualInterlockMpsA = DisitckManualInterlockMpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockMpsA", DisitckManualInterlockMpsA)

    @DebugIt()
    def get_DisitckManualInterlockMpsB(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'B')
        self._DisitckManualInterlockMpsB = (value >> 4) & 1
        return self._DisitckManualInterlockMpsB

    @DebugIt()
    def set_DisitckManualInterlockMpsB(self, DisitckManualInterlockMpsB):
        self._DisitckManualInterlockMpsB = DisitckManualInterlockMpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockMpsB", DisitckManualInterlockMpsB)

    @DebugIt()
    def get_DisitckManualInterlockDiagA(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'A')
        self._DisitckManualInterlockDiagA = (value >> 5) & 1
        return self._DisitckManualInterlockDiagA

    @DebugIt()
    def set_DisitckManualInterlockDiagA(self, DisitckManualInterlockDiagA):
        self._DisitckManualInterlockDiagA = DisitckManualInterlockDiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockDiagA", DisitckManualInterlockDiagA)

    @DebugIt()
    def get_DisitckManualInterlockDiagB(self):
        value = perseus_utils.read_direct(self.perseus, 15, 'B')
        self._DisitckManualInterlockDiagB = (value >> 5) & 1
        return self._DisitckManualInterlockDiagB

    @DebugIt()
    def set_DisitckManualInterlockDiagB(self, DisitckManualInterlockDiagB):
        self._DisitckManualInterlockDiagB = DisitckManualInterlockDiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckManualInterlockDiagB", DisitckManualInterlockDiagB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'A')
        self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpDacsoffloopsstbyA(self, DisitckPlungerEndSwitchesUpDacsoffloopsstbyA):
        self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyA = DisitckPlungerEndSwitchesUpDacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpDacsoffloopsstbyA", DisitckPlungerEndSwitchesUpDacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'B')
        self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpDacsoffloopsstbyB(self, DisitckPlungerEndSwitchesUpDacsoffloopsstbyB):
        self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyB = DisitckPlungerEndSwitchesUpDacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpDacsoffloopsstbyB", DisitckPlungerEndSwitchesUpDacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'A')
        self._DisitckPlungerEndSwitchesUpPindiodeswitchA = (value >> 1) & 1
        return self._DisitckPlungerEndSwitchesUpPindiodeswitchA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpPindiodeswitchA(self, DisitckPlungerEndSwitchesUpPindiodeswitchA):
        self._DisitckPlungerEndSwitchesUpPindiodeswitchA = DisitckPlungerEndSwitchesUpPindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpPindiodeswitchA", DisitckPlungerEndSwitchesUpPindiodeswitchA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'B')
        self._DisitckPlungerEndSwitchesUpPindiodeswitchB = (value >> 1) & 1
        return self._DisitckPlungerEndSwitchesUpPindiodeswitchB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpPindiodeswitchB(self, DisitckPlungerEndSwitchesUpPindiodeswitchB):
        self._DisitckPlungerEndSwitchesUpPindiodeswitchB = DisitckPlungerEndSwitchesUpPindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpPindiodeswitchB", DisitckPlungerEndSwitchesUpPindiodeswitchB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'A')
        self._DisitckPlungerEndSwitchesUpFdltrgA = (value >> 2) & 1
        return self._DisitckPlungerEndSwitchesUpFdltrgA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpFdltrgA(self, DisitckPlungerEndSwitchesUpFdltrgA):
        self._DisitckPlungerEndSwitchesUpFdltrgA = DisitckPlungerEndSwitchesUpFdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpFdltrgA", DisitckPlungerEndSwitchesUpFdltrgA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'B')
        self._DisitckPlungerEndSwitchesUpFdltrgB = (value >> 2) & 1
        return self._DisitckPlungerEndSwitchesUpFdltrgB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpFdltrgB(self, DisitckPlungerEndSwitchesUpFdltrgB):
        self._DisitckPlungerEndSwitchesUpFdltrgB = DisitckPlungerEndSwitchesUpFdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpFdltrgB", DisitckPlungerEndSwitchesUpFdltrgB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'A')
        self._DisitckPlungerEndSwitchesUpPlctxoffA = (value >> 3) & 1
        return self._DisitckPlungerEndSwitchesUpPlctxoffA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpPlctxoffA(self, DisitckPlungerEndSwitchesUpPlctxoffA):
        self._DisitckPlungerEndSwitchesUpPlctxoffA = DisitckPlungerEndSwitchesUpPlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpPlctxoffA", DisitckPlungerEndSwitchesUpPlctxoffA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'B')
        self._DisitckPlungerEndSwitchesUpPlctxoffB = (value >> 3) & 1
        return self._DisitckPlungerEndSwitchesUpPlctxoffB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpPlctxoffB(self, DisitckPlungerEndSwitchesUpPlctxoffB):
        self._DisitckPlungerEndSwitchesUpPlctxoffB = DisitckPlungerEndSwitchesUpPlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpPlctxoffB", DisitckPlungerEndSwitchesUpPlctxoffB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpMpsA(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'A')
        self._DisitckPlungerEndSwitchesUpMpsA = (value >> 4) & 1
        return self._DisitckPlungerEndSwitchesUpMpsA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpMpsA(self, DisitckPlungerEndSwitchesUpMpsA):
        self._DisitckPlungerEndSwitchesUpMpsA = DisitckPlungerEndSwitchesUpMpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpMpsA", DisitckPlungerEndSwitchesUpMpsA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpMpsB(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'B')
        self._DisitckPlungerEndSwitchesUpMpsB = (value >> 4) & 1
        return self._DisitckPlungerEndSwitchesUpMpsB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpMpsB(self, DisitckPlungerEndSwitchesUpMpsB):
        self._DisitckPlungerEndSwitchesUpMpsB = DisitckPlungerEndSwitchesUpMpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpMpsB", DisitckPlungerEndSwitchesUpMpsB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpDiagA(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'A')
        self._DisitckPlungerEndSwitchesUpDiagA = (value >> 5) & 1
        return self._DisitckPlungerEndSwitchesUpDiagA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpDiagA(self, DisitckPlungerEndSwitchesUpDiagA):
        self._DisitckPlungerEndSwitchesUpDiagA = DisitckPlungerEndSwitchesUpDiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpDiagA", DisitckPlungerEndSwitchesUpDiagA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpDiagB(self):
        value = perseus_utils.read_direct(self.perseus, 16, 'B')
        self._DisitckPlungerEndSwitchesUpDiagB = (value >> 5) & 1
        return self._DisitckPlungerEndSwitchesUpDiagB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpDiagB(self, DisitckPlungerEndSwitchesUpDiagB):
        self._DisitckPlungerEndSwitchesUpDiagB = DisitckPlungerEndSwitchesUpDiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesUpDiagB", DisitckPlungerEndSwitchesUpDiagB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'A')
        self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownDacsoffloopsstbyA(self, DisitckPlungerEndSwitchesDownDacsoffloopsstbyA):
        self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyA = DisitckPlungerEndSwitchesDownDacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownDacsoffloopsstbyA", DisitckPlungerEndSwitchesDownDacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'B')
        self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownDacsoffloopsstbyB(self, DisitckPlungerEndSwitchesDownDacsoffloopsstbyB):
        self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyB = DisitckPlungerEndSwitchesDownDacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownDacsoffloopsstbyB", DisitckPlungerEndSwitchesDownDacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'A')
        self._DisitckPlungerEndSwitchesDownPindiodeswitchA = (value >> 1) & 1
        return self._DisitckPlungerEndSwitchesDownPindiodeswitchA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownPindiodeswitchA(self, DisitckPlungerEndSwitchesDownPindiodeswitchA):
        self._DisitckPlungerEndSwitchesDownPindiodeswitchA = DisitckPlungerEndSwitchesDownPindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownPindiodeswitchA", DisitckPlungerEndSwitchesDownPindiodeswitchA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'B')
        self._DisitckPlungerEndSwitchesDownPindiodeswitchB = (value >> 1) & 1
        return self._DisitckPlungerEndSwitchesDownPindiodeswitchB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownPindiodeswitchB(self, DisitckPlungerEndSwitchesDownPindiodeswitchB):
        self._DisitckPlungerEndSwitchesDownPindiodeswitchB = DisitckPlungerEndSwitchesDownPindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownPindiodeswitchB", DisitckPlungerEndSwitchesDownPindiodeswitchB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'A')
        self._DisitckPlungerEndSwitchesDownFdltrgA = (value >> 2) & 1
        return self._DisitckPlungerEndSwitchesDownFdltrgA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownFdltrgA(self, DisitckPlungerEndSwitchesDownFdltrgA):
        self._DisitckPlungerEndSwitchesDownFdltrgA = DisitckPlungerEndSwitchesDownFdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownFdltrgA", DisitckPlungerEndSwitchesDownFdltrgA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'B')
        self._DisitckPlungerEndSwitchesDownFdltrgB = (value >> 2) & 1
        return self._DisitckPlungerEndSwitchesDownFdltrgB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownFdltrgB(self, DisitckPlungerEndSwitchesDownFdltrgB):
        self._DisitckPlungerEndSwitchesDownFdltrgB = DisitckPlungerEndSwitchesDownFdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownFdltrgB", DisitckPlungerEndSwitchesDownFdltrgB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'A')
        self._DisitckPlungerEndSwitchesDownPlctxoffA = (value >> 3) & 1
        return self._DisitckPlungerEndSwitchesDownPlctxoffA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownPlctxoffA(self, DisitckPlungerEndSwitchesDownPlctxoffA):
        self._DisitckPlungerEndSwitchesDownPlctxoffA = DisitckPlungerEndSwitchesDownPlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownPlctxoffA", DisitckPlungerEndSwitchesDownPlctxoffA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'B')
        self._DisitckPlungerEndSwitchesDownPlctxoffB = (value >> 3) & 1
        return self._DisitckPlungerEndSwitchesDownPlctxoffB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownPlctxoffB(self, DisitckPlungerEndSwitchesDownPlctxoffB):
        self._DisitckPlungerEndSwitchesDownPlctxoffB = DisitckPlungerEndSwitchesDownPlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownPlctxoffB", DisitckPlungerEndSwitchesDownPlctxoffB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownMpsA(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'A')
        self._DisitckPlungerEndSwitchesDownMpsA = (value >> 4) & 1
        return self._DisitckPlungerEndSwitchesDownMpsA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownMpsA(self, DisitckPlungerEndSwitchesDownMpsA):
        self._DisitckPlungerEndSwitchesDownMpsA = DisitckPlungerEndSwitchesDownMpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownMpsA", DisitckPlungerEndSwitchesDownMpsA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownMpsB(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'B')
        self._DisitckPlungerEndSwitchesDownMpsB = (value >> 4) & 1
        return self._DisitckPlungerEndSwitchesDownMpsB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownMpsB(self, DisitckPlungerEndSwitchesDownMpsB):
        self._DisitckPlungerEndSwitchesDownMpsB = DisitckPlungerEndSwitchesDownMpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownMpsB", DisitckPlungerEndSwitchesDownMpsB)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownDiagA(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'A')
        self._DisitckPlungerEndSwitchesDownDiagA = (value >> 5) & 1
        return self._DisitckPlungerEndSwitchesDownDiagA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownDiagA(self, DisitckPlungerEndSwitchesDownDiagA):
        self._DisitckPlungerEndSwitchesDownDiagA = DisitckPlungerEndSwitchesDownDiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownDiagA", DisitckPlungerEndSwitchesDownDiagA)

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownDiagB(self):
        value = perseus_utils.read_direct(self.perseus, 17, 'B')
        self._DisitckPlungerEndSwitchesDownDiagB = (value >> 5) & 1
        return self._DisitckPlungerEndSwitchesDownDiagB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownDiagB(self, DisitckPlungerEndSwitchesDownDiagB):
        self._DisitckPlungerEndSwitchesDownDiagB = DisitckPlungerEndSwitchesDownDiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckPlungerEndSwitchesDownDiagB", DisitckPlungerEndSwitchesDownDiagB)

    @DebugIt()
    def get_DisitckMpsDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'A')
        self._DisitckMpsDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckMpsDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckMpsDacsoffloopsstbyA(self, DisitckMpsDacsoffloopsstbyA):
        self._DisitckMpsDacsoffloopsstbyA = DisitckMpsDacsoffloopsstbyA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsDacsoffloopsstbyA", DisitckMpsDacsoffloopsstbyA)

    @DebugIt()
    def get_DisitckMpsDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'B')
        self._DisitckMpsDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckMpsDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckMpsDacsoffloopsstbyB(self, DisitckMpsDacsoffloopsstbyB):
        self._DisitckMpsDacsoffloopsstbyB = DisitckMpsDacsoffloopsstbyB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsDacsoffloopsstbyB", DisitckMpsDacsoffloopsstbyB)

    @DebugIt()
    def get_DisitckMpsPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'A')
        self._DisitckMpsPindiodeswitchA = (value >> 1) & 1
        return self._DisitckMpsPindiodeswitchA

    @DebugIt()
    def set_DisitckMpsPindiodeswitchA(self, DisitckMpsPindiodeswitchA):
        self._DisitckMpsPindiodeswitchA = DisitckMpsPindiodeswitchA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsPindiodeswitchA", DisitckMpsPindiodeswitchA)

    @DebugIt()
    def get_DisitckMpsPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'B')
        self._DisitckMpsPindiodeswitchB = (value >> 1) & 1
        return self._DisitckMpsPindiodeswitchB

    @DebugIt()
    def set_DisitckMpsPindiodeswitchB(self, DisitckMpsPindiodeswitchB):
        self._DisitckMpsPindiodeswitchB = DisitckMpsPindiodeswitchB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsPindiodeswitchB", DisitckMpsPindiodeswitchB)

    @DebugIt()
    def get_DisitckMpsFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'A')
        self._DisitckMpsFdltrgA = (value >> 2) & 1
        return self._DisitckMpsFdltrgA

    @DebugIt()
    def set_DisitckMpsFdltrgA(self, DisitckMpsFdltrgA):
        self._DisitckMpsFdltrgA = DisitckMpsFdltrgA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsFdltrgA", DisitckMpsFdltrgA)

    @DebugIt()
    def get_DisitckMpsFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'B')
        self._DisitckMpsFdltrgB = (value >> 2) & 1
        return self._DisitckMpsFdltrgB

    @DebugIt()
    def set_DisitckMpsFdltrgB(self, DisitckMpsFdltrgB):
        self._DisitckMpsFdltrgB = DisitckMpsFdltrgB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsFdltrgB", DisitckMpsFdltrgB)

    @DebugIt()
    def get_DisitckMpsPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'A')
        self._DisitckMpsPlctxoffA = (value >> 3) & 1
        return self._DisitckMpsPlctxoffA

    @DebugIt()
    def set_DisitckMpsPlctxoffA(self, DisitckMpsPlctxoffA):
        self._DisitckMpsPlctxoffA = DisitckMpsPlctxoffA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsPlctxoffA", DisitckMpsPlctxoffA)

    @DebugIt()
    def get_DisitckMpsPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'B')
        self._DisitckMpsPlctxoffB = (value >> 3) & 1
        return self._DisitckMpsPlctxoffB

    @DebugIt()
    def set_DisitckMpsPlctxoffB(self, DisitckMpsPlctxoffB):
        self._DisitckMpsPlctxoffB = DisitckMpsPlctxoffB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsPlctxoffB", DisitckMpsPlctxoffB)

    @DebugIt()
    def get_DisitckMpsMpsA(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'A')
        self._DisitckMpsMpsA = (value >> 4) & 1
        return self._DisitckMpsMpsA

    @DebugIt()
    def set_DisitckMpsMpsA(self, DisitckMpsMpsA):
        self._DisitckMpsMpsA = DisitckMpsMpsA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsMpsA", DisitckMpsMpsA)

    @DebugIt()
    def get_DisitckMpsMpsB(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'B')
        self._DisitckMpsMpsB = (value >> 4) & 1
        return self._DisitckMpsMpsB

    @DebugIt()
    def set_DisitckMpsMpsB(self, DisitckMpsMpsB):
        self._DisitckMpsMpsB = DisitckMpsMpsB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsMpsB", DisitckMpsMpsB)

    @DebugIt()
    def get_DisitckMpsDiagA(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'A')
        self._DisitckMpsDiagA = (value >> 5) & 1
        return self._DisitckMpsDiagA

    @DebugIt()
    def set_DisitckMpsDiagA(self, DisitckMpsDiagA):
        self._DisitckMpsDiagA = DisitckMpsDiagA
        cavity = 'A'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsDiagA", DisitckMpsDiagA)

    @DebugIt()
    def get_DisitckMpsDiagB(self):
        value = perseus_utils.read_direct(self.perseus, 18, 'B')
        self._DisitckMpsDiagB = (value >> 5) & 1
        return self._DisitckMpsDiagB

    @DebugIt()
    def set_DisitckMpsDiagB(self, DisitckMpsDiagB):
        self._DisitckMpsDiagB = DisitckMpsDiagB
        cavity = 'B'
        self.update_fim(cavity)
        self.push_change_event("DisitckMpsDiagB", DisitckMpsDiagB)

    @DebugIt()
    def read_Diag_Irvtet1A(self):
        return self._Diag_Irvtet1A

    @DebugIt()
    def read_Diag_Irvtet1B(self):
        return self._Diag_Irvtet1B

    @DebugIt()
    def read_Diag_Qrvtet1A(self):
        return self._Diag_Qrvtet1A

    @DebugIt()
    def read_Diag_Qrvtet1B(self):
        return self._Diag_Qrvtet1B

    @DebugIt()
    def read_Diag_Amprvtet1A(self):
        return self._Diag_Amprvtet1A

    @DebugIt()
    def read_Diag_Amprvtet1B(self):
        return self._Diag_Amprvtet1B

    @DebugIt()
    def read_Diag_Phrvtet1A(self):
        return self._Diag_Phrvtet1A

    @DebugIt()
    def read_Diag_Phrvtet1B(self):
        return self._Diag_Phrvtet1B

    @DebugIt()
    def read_Diag_Irvtet2A(self):
        return self._Diag_Irvtet2A

    @DebugIt()
    def read_Diag_Irvtet2B(self):
        return self._Diag_Irvtet2B

    @DebugIt()
    def read_Diag_Qrvtet2A(self):
        return self._Diag_Qrvtet2A

    @DebugIt()
    def read_Diag_Qrvtet2B(self):
        return self._Diag_Qrvtet2B

    @DebugIt()
    def read_Diag_Amprvtet2A(self):
        return self._Diag_Amprvtet2A

    @DebugIt()
    def read_Diag_Amprvtet2B(self):
        return self._Diag_Amprvtet2B

    @DebugIt()
    def read_Diag_Phrvtet2A(self):
        return self._Diag_Phrvtet2A

    @DebugIt()
    def read_Diag_Phrvtet2B(self):
        return self._Diag_Phrvtet2B

    @DebugIt()
    def read_Diag_IfwcircA(self):
        return self._Diag_IfwcircA

    @DebugIt()
    def read_Diag_IfwcircB(self):
        return self._Diag_IfwcircB

    @DebugIt()
    def read_Diag_QfwcircA(self):
        return self._Diag_QfwcircA

    @DebugIt()
    def read_Diag_QfwcircB(self):
        return self._Diag_QfwcircB

    @DebugIt()
    def read_Diag_AmpfwcircA(self):
        return self._Diag_AmpfwcircA

    @DebugIt()
    def read_Diag_AmpfwcircB(self):
        return self._Diag_AmpfwcircB

    @DebugIt()
    def read_Diag_PhfwcircA(self):
        return self._Diag_PhfwcircA

    @DebugIt()
    def read_Diag_PhfwcircB(self):
        return self._Diag_PhfwcircB

    @DebugIt()
    def read_Diag_IrvcircA(self):
        return self._Diag_IrvcircA

    @DebugIt()
    def read_Diag_IrvcircB(self):
        return self._Diag_IrvcircB

    @DebugIt()
    def read_Diag_QrvcircA(self):
        return self._Diag_QrvcircA

    @DebugIt()
    def read_Diag_QrvcircB(self):
        return self._Diag_QrvcircB

    @DebugIt()
    def read_Diag_AmprvcircA(self):
        return self._Diag_AmprvcircA

    @DebugIt()
    def read_Diag_AmprvcircB(self):
        return self._Diag_AmprvcircB

    @DebugIt()
    def read_Diag_PhrvcircA(self):
        return self._Diag_PhrvcircA

    @DebugIt()
    def read_Diag_PhrvcircB(self):
        return self._Diag_PhrvcircB

    @DebugIt()
    def read_Diag_IfwloadA(self):
        return self._Diag_IfwloadA

    @DebugIt()
    def read_Diag_IfwloadB(self):
        return self._Diag_IfwloadB

    @DebugIt()
    def read_Diag_QfwloadA(self):
        return self._Diag_QfwloadA

    @DebugIt()
    def read_Diag_QfwloadB(self):
        return self._Diag_QfwloadB

    @DebugIt()
    def read_Diag_AmpfwloadA(self):
        return self._Diag_AmpfwloadA

    @DebugIt()
    def read_Diag_AmpfwloadB(self):
        return self._Diag_AmpfwloadB

    @DebugIt()
    def read_Diag_PhfwloadA(self):
        return self._Diag_PhfwloadA

    @DebugIt()
    def read_Diag_PhfwloadB(self):
        return self._Diag_PhfwloadB

    @DebugIt()
    def read_Diag_IfwhybloadA(self):
        return self._Diag_IfwhybloadA

    @DebugIt()
    def read_Diag_IfwhybloadB(self):
        return self._Diag_IfwhybloadB

    @DebugIt()
    def read_Diag_QfwhybloadA(self):
        return self._Diag_QfwhybloadA

    @DebugIt()
    def read_Diag_QfwhybloadB(self):
        return self._Diag_QfwhybloadB

    @DebugIt()
    def read_Diag_AmpfwhybloadA(self):
        return self._Diag_AmpfwhybloadA

    @DebugIt()
    def read_Diag_AmpfwhybloadB(self):
        return self._Diag_AmpfwhybloadB

    @DebugIt()
    def read_Diag_PhfwhybloadA(self):
        return self._Diag_PhfwhybloadA

    @DebugIt()
    def read_Diag_PhfwhybloadB(self):
        return self._Diag_PhfwhybloadB

    @DebugIt()
    def read_Diag_IrvcavA(self):
        return self._Diag_IrvcavA

    @DebugIt()
    def read_Diag_IrvcavB(self):
        return self._Diag_IrvcavB

    @DebugIt()
    def read_Diag_QrvcavA(self):
        return self._Diag_QrvcavA

    @DebugIt()
    def read_Diag_QrvcavB(self):
        return self._Diag_QrvcavB

    @DebugIt()
    def read_Diag_AmprvcavA(self):
        return self._Diag_AmprvcavA

    @DebugIt()
    def read_Diag_AmprvcavB(self):
        return self._Diag_AmprvcavB

    @DebugIt()
    def read_Diag_PhrvcavA(self):
        return self._Diag_PhrvcavA

    @DebugIt()
    def read_Diag_PhrvcavB(self):
        return self._Diag_PhrvcavB

    @DebugIt()
    def read_Diag_ImoA(self):
        return self._Diag_ImoA

    @DebugIt()
    def read_Diag_ImoB(self):
        return self._Diag_ImoB

    @DebugIt()
    def read_Diag_QmoA(self):
        return self._Diag_QmoA

    @DebugIt()
    def read_Diag_QmoB(self):
        return self._Diag_QmoB

    @DebugIt()
    def read_Diag_AmpmoA(self):
        return self._Diag_AmpmoA

    @DebugIt()
    def read_Diag_AmpmoB(self):
        return self._Diag_AmpmoB

    @DebugIt()
    def read_Diag_PhmoA(self):
        return self._Diag_PhmoA

    @DebugIt()
    def read_Diag_PhmoB(self):
        return self._Diag_PhmoB

    @DebugIt()
    def read_Diag_IlandauA(self):
        return self._Diag_IlandauA

    @DebugIt()
    def read_Diag_IlandauB(self):
        return self._Diag_IlandauB

    @DebugIt()
    def read_Diag_QlandauA(self):
        return self._Diag_QlandauA

    @DebugIt()
    def read_Diag_QlandauB(self):
        return self._Diag_QlandauB

    @DebugIt()
    def read_Diag_AmplandauA(self):
        return self._Diag_AmplandauA

    @DebugIt()
    def read_Diag_AmplandauB(self):
        return self._Diag_AmplandauB

    @DebugIt()
    def read_Diag_PhlandauA(self):
        return self._Diag_PhlandauA

    @DebugIt()
    def read_Diag_PhlandauB(self):
        return self._Diag_PhlandauB

    @DebugIt()
    def read_Diag_PlungerMovingManualTuningA(self):
        return self._Diag_PlungerMovingManualTuningA

    @DebugIt()
    def read_Diag_PlungerMovingManualTuningB(self):
        return self._Diag_PlungerMovingManualTuningB

    @DebugIt()
    def read_Diag_PlungerMovingUpManualTuningA(self):
        return self._Diag_PlungerMovingUpManualTuningA

    @DebugIt()
    def read_Diag_PlungerMovingUpManualTuningB(self):
        return self._Diag_PlungerMovingUpManualTuningB

    @DebugIt()
    def read_Diag_PlungerMovingAutomaticTuningA(self):
        return self._Diag_PlungerMovingAutomaticTuningA

    @DebugIt()
    def read_Diag_PlungerMovingAutomaticTuningB(self):
        return self._Diag_PlungerMovingAutomaticTuningB

    @DebugIt()
    def read_Diag_PlungerMovingUpAutomaticTuningA(self):
        return self._Diag_PlungerMovingUpAutomaticTuningA

    @DebugIt()
    def read_Diag_PlungerMovingUpAutomaticTuningB(self):
        return self._Diag_PlungerMovingUpAutomaticTuningB

    @DebugIt()
    def read_Diag_DephaseMoLandauA(self):
        return self._Diag_DephaseMoLandauA

    @DebugIt()
    def read_Diag_DephaseMoLandauB(self):
        return self._Diag_DephaseMoLandauB

    @DebugIt()
    def read_Diag_Rvtet1A(self):
        address = 100
        position = 0
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_Rvtet1B(self):
        address = 100
        position = 0
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_Rvtet2A(self):
        address = 100
        position = 1
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_Rvtet2B(self):
        address = 100
        position = 1
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_RvcircA(self):
        address = 100
        position = 2
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_RvcircB(self):
        address = 100
        position = 2
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_FwloadA(self):
        address = 100
        position = 3
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_FwloadB(self):
        address = 100
        position = 3
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_FwhybloadA(self):
        address = 100
        position = 4
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_FwhybloadB(self):
        address = 100
        position = 4
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_RvcavA(self):
        address = 100
        position = 5
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_RvcavB(self):
        address = 100
        position = 5
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_ArcsA(self):
        address = 100
        position = 6
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_ArcsB(self):
        address = 100
        position = 6
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_VacuumA(self):
        address = 100
        position = 7
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_VacuumB(self):
        address = 100
        position = 7
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_ManualInterlockA(self):
        address = 100
        position = 8
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_ManualInterlockB(self):
        address = 100
        position = 8
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_ExternalItckA(self):
        address = 100
        position = 9
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_ExternalItckB(self):
        address = 100
        position = 9
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_PlungerEndSwitchUpA(self):
        address = 100
        position = 10
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_PlungerEndSwitchUpB(self):
        address = 100
        position = 10
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_PlungerEndSwitchDownA(self):
        address = 100
        position = 11
        cavity = 'A'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_PlungerEndSwitchDownB(self):
        address = 100
        position = 11
        cavity = 'B'
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position, cavity)


    @DebugIt()
    def read_Diag_Timestamp1A(self):
        address = 110
        cavity = 'A'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp1(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp1B(self):
        address = 110
        cavity = 'B'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp1(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp2A(self):
        address = 111
        cavity = 'A'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp2(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp2B(self):
        address = 111
        cavity = 'B'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp2(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp3A(self):
        address = 112
        cavity = 'A'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp3(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp3B(self):
        address = 112
        cavity = 'B'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp3(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp4A(self):
        address = 113
        cavity = 'A'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp4(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp4B(self):
        address = 113
        cavity = 'B'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp4(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp5A(self):
        address = 114
        cavity = 'A'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp5(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp5B(self):
        address = 114
        cavity = 'B'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp5(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp6A(self):
        address = 115
        cavity = 'A'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp6(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp6B(self):
        address = 115
        cavity = 'B'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp6(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp7A(self):
        address = 116
        cavity = 'A'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp7(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_Timestamp7B(self):
        address = 116
        cavity = 'B'
        # @todo: add this method to special methods library ...
        return extra_func.read_Diag_Timestamp7(self.perseus, address, cavity)


    @DebugIt()
    def read_Diag_DacsDisableCommandA(self):
        address = 152
        cavity = 'A'
        return extra_func.read_diag_bit_direct(self.perseus, address, 0, cavity)


    @DebugIt()
    def read_Diag_DacsDisableCommandB(self):
        address = 152
        cavity = 'B'
        return extra_func.read_diag_bit_direct(self.perseus, address, 0, cavity)


    @DebugIt()
    def read_Diag_PinSwitchA(self):
        address = 152
        cavity = 'A'
        return extra_func.read_diag_bit_direct(self.perseus, address, 1, cavity)


    @DebugIt()
    def read_Diag_PinSwitchB(self):
        address = 152
        cavity = 'B'
        return extra_func.read_diag_bit_direct(self.perseus, address, 1, cavity)


    @DebugIt()
    def read_Diag_FdlTriggerToLoopsdiagboardA(self):
        address = 152
        cavity = 'A'
        return extra_func.read_diag_bit_direct(self.perseus, address, 2, cavity)


    @DebugIt()
    def read_Diag_FdlTriggerToLoopsdiagboardB(self):
        address = 152
        cavity = 'B'
        return extra_func.read_diag_bit_direct(self.perseus, address, 2, cavity)


    @DebugIt()
    def read_Diag_OutputToPlcA(self):
        address = 152
        cavity = 'A'
        return extra_func.read_diag_bit_direct(self.perseus, address, 3, cavity)


    @DebugIt()
    def read_Diag_OutputToPlcB(self):
        address = 152
        cavity = 'B'
        return extra_func.read_diag_bit_direct(self.perseus, address, 3, cavity)


    @DebugIt()
    def read_Diag_OutputToMpsA(self):
        address = 152
        cavity = 'A'
        return extra_func.read_diag_bit_direct(self.perseus, address, 4, cavity)


    @DebugIt()
    def read_Diag_OutputToMpsB(self):
        address = 152
        cavity = 'B'
        return extra_func.read_diag_bit_direct(self.perseus, address, 4, cavity)


    @DebugIt()
    def read_Diag_AmpRvtet1b(self):
        return self._Diag_AmpRvtet1b

    @DebugIt()
    def read_Diag_AmpRvtet1a(self):
        return self._Diag_AmpRvtet1a

    @DebugIt()
    def read_Diag_AmpMoa(self):
        return self._Diag_AmpMoa

    @DebugIt()
    def read_Diag_AmpLandaua(self):
        return self._Diag_AmpLandaua

    @DebugIt()
    def read_Diag_AmpFwloada(self):
        return self._Diag_AmpFwloada

    @DebugIt()
    def read_Diag_AmpRvtet2b(self):
        return self._Diag_AmpRvtet2b

    @DebugIt()
    def read_Diag_AmpRvtet2a(self):
        return self._Diag_AmpRvtet2a

    @DebugIt()
    def read_Diag_AmpFwloadb(self):
        return self._Diag_AmpFwloadb

    @DebugIt()
    def read_Diag_AmpRvcavb(self):
        return self._Diag_AmpRvcavb

    @DebugIt()
    def read_Diag_AmpRvcava(self):
        return self._Diag_AmpRvcava

    @DebugIt()
    def read_Diag_AmpFwcircb(self):
        return self._Diag_AmpFwcircb

    @DebugIt()
    def read_Diag_AmpFwcirca(self):
        return self._Diag_AmpFwcirca

    @DebugIt()
    def read_Diag_AmpMob(self):
        return self._Diag_AmpMob

    @DebugIt()
    def read_Diag_AmpRvcirca(self):
        return self._Diag_AmpRvcirca

    @DebugIt()
    def read_Diag_AmpRvcircb(self):
        return self._Diag_AmpRvcircb

    @DebugIt()
    def read_Diag_AmpFwhybloadb(self):
        return self._Diag_AmpFwhybloadb

    @DebugIt()
    def read_Diag_AmpFwhybloada(self):
        return self._Diag_AmpFwhybloada

    @DebugIt()
    def read_Diag_AmpLandaub(self):
        return self._Diag_AmpLandaub

    @DebugIt()
    def read_Diag_PhRvtet1b(self):
        return self._Diag_PhRvtet1b

    @DebugIt()
    def read_Diag_PhRvtet1a(self):
        return self._Diag_PhRvtet1a

    @DebugIt()
    def read_Diag_PhMoa(self):
        return self._Diag_PhMoa

    @DebugIt()
    def read_Diag_PhLandaua(self):
        return self._Diag_PhLandaua

    @DebugIt()
    def read_Diag_PhFwloada(self):
        return self._Diag_PhFwloada

    @DebugIt()
    def read_Diag_PhRvtet2b(self):
        return self._Diag_PhRvtet2b

    @DebugIt()
    def read_Diag_PhRvtet2a(self):
        return self._Diag_PhRvtet2a

    @DebugIt()
    def read_Diag_PhFwloadb(self):
        return self._Diag_PhFwloadb

    @DebugIt()
    def read_Diag_PhRvcavb(self):
        return self._Diag_PhRvcavb

    @DebugIt()
    def read_Diag_PhRvcava(self):
        return self._Diag_PhRvcava

    @DebugIt()
    def read_Diag_PhFwcircb(self):
        return self._Diag_PhFwcircb

    @DebugIt()
    def read_Diag_PhFwcirca(self):
        return self._Diag_PhFwcirca

    @DebugIt()
    def read_Diag_PhMob(self):
        return self._Diag_PhMob

    @DebugIt()
    def read_Diag_PhRvcirca(self):
        return self._Diag_PhRvcirca

    @DebugIt()
    def read_Diag_PhRvcircb(self):
        return self._Diag_PhRvcircb

    @DebugIt()
    def read_Diag_PhFwhybloadb(self):
        return self._Diag_PhFwhybloadb

    @DebugIt()
    def read_Diag_PhFwhybloada(self):
        return self._Diag_PhFwhybloada

    @DebugIt()
    def read_Diag_PhLandaub(self):
        return self._Diag_PhLandaub

    @command
    def read_diagnostics(self):
        perseus_utils.start_reading_diagnostics(self.perseus, 'A')
        perseus_utils.start_reading_diagnostics(self.perseus, 'B')

        self._Diag_Irvtet1A = perseus_utils.read_diag_milivolts(self.perseus, 0, 'A')
        self.push_change_event("Diag_Irvtet1A", self._Diag_Irvtet1A)
        self._Diag_Irvtet1B = perseus_utils.read_diag_milivolts(self.perseus, 0, 'B')
        self.push_change_event("Diag_Irvtet1B", self._Diag_Irvtet1B)
        self._Diag_Qrvtet1A = perseus_utils.read_diag_milivolts(self.perseus, 1, 'A')
        self.push_change_event("Diag_Qrvtet1A", self._Diag_Qrvtet1A)
        self._Diag_Qrvtet1B = perseus_utils.read_diag_milivolts(self.perseus, 1, 'B')
        self.push_change_event("Diag_Qrvtet1B", self._Diag_Qrvtet1B)
        self._Diag_Amprvtet1A = perseus_utils.read_diag_milivolts(self.perseus, 2, 'A')
        self.push_change_event("Diag_Amprvtet1A", self._Diag_Amprvtet1A)
        self._Diag_Amprvtet1B = perseus_utils.read_diag_milivolts(self.perseus, 2, 'B')
        self.push_change_event("Diag_Amprvtet1B", self._Diag_Amprvtet1B)
        self._Diag_Phrvtet1A = perseus_utils.read_diag_angle(self.perseus, 3, 'A')
        self.push_change_event("Diag_Phrvtet1A", self._Diag_Phrvtet1A)
        self._Diag_Phrvtet1B = perseus_utils.read_diag_angle(self.perseus, 3, 'B')
        self.push_change_event("Diag_Phrvtet1B", self._Diag_Phrvtet1B)
        self._Diag_Irvtet2A = perseus_utils.read_diag_milivolts(self.perseus, 4, 'A')
        self.push_change_event("Diag_Irvtet2A", self._Diag_Irvtet2A)
        self._Diag_Irvtet2B = perseus_utils.read_diag_milivolts(self.perseus, 4, 'B')
        self.push_change_event("Diag_Irvtet2B", self._Diag_Irvtet2B)
        self._Diag_Qrvtet2A = perseus_utils.read_diag_milivolts(self.perseus, 5, 'A')
        self.push_change_event("Diag_Qrvtet2A", self._Diag_Qrvtet2A)
        self._Diag_Qrvtet2B = perseus_utils.read_diag_milivolts(self.perseus, 5, 'B')
        self.push_change_event("Diag_Qrvtet2B", self._Diag_Qrvtet2B)
        self._Diag_Amprvtet2A = perseus_utils.read_diag_milivolts(self.perseus, 6, 'A')
        self.push_change_event("Diag_Amprvtet2A", self._Diag_Amprvtet2A)
        self._Diag_Amprvtet2B = perseus_utils.read_diag_milivolts(self.perseus, 6, 'B')
        self.push_change_event("Diag_Amprvtet2B", self._Diag_Amprvtet2B)
        self._Diag_Phrvtet2A = perseus_utils.read_diag_angle(self.perseus, 7, 'A')
        self.push_change_event("Diag_Phrvtet2A", self._Diag_Phrvtet2A)
        self._Diag_Phrvtet2B = perseus_utils.read_diag_angle(self.perseus, 7, 'B')
        self.push_change_event("Diag_Phrvtet2B", self._Diag_Phrvtet2B)
        self._Diag_IfwcircA = perseus_utils.read_diag_milivolts(self.perseus, 8, 'A')
        self.push_change_event("Diag_IfwcircA", self._Diag_IfwcircA)
        self._Diag_IfwcircB = perseus_utils.read_diag_milivolts(self.perseus, 8, 'B')
        self.push_change_event("Diag_IfwcircB", self._Diag_IfwcircB)
        self._Diag_QfwcircA = perseus_utils.read_diag_milivolts(self.perseus, 9, 'A')
        self.push_change_event("Diag_QfwcircA", self._Diag_QfwcircA)
        self._Diag_QfwcircB = perseus_utils.read_diag_milivolts(self.perseus, 9, 'B')
        self.push_change_event("Diag_QfwcircB", self._Diag_QfwcircB)
        self._Diag_AmpfwcircA = perseus_utils.read_diag_milivolts(self.perseus, 10, 'A')
        self.push_change_event("Diag_AmpfwcircA", self._Diag_AmpfwcircA)
        self._Diag_AmpfwcircB = perseus_utils.read_diag_milivolts(self.perseus, 10, 'B')
        self.push_change_event("Diag_AmpfwcircB", self._Diag_AmpfwcircB)
        self._Diag_PhfwcircA = perseus_utils.read_diag_angle(self.perseus, 11, 'A')
        self.push_change_event("Diag_PhfwcircA", self._Diag_PhfwcircA)
        self._Diag_PhfwcircB = perseus_utils.read_diag_angle(self.perseus, 11, 'B')
        self.push_change_event("Diag_PhfwcircB", self._Diag_PhfwcircB)
        self._Diag_IrvcircA = perseus_utils.read_diag_milivolts(self.perseus, 12, 'A')
        self.push_change_event("Diag_IrvcircA", self._Diag_IrvcircA)
        self._Diag_IrvcircB = perseus_utils.read_diag_milivolts(self.perseus, 12, 'B')
        self.push_change_event("Diag_IrvcircB", self._Diag_IrvcircB)
        self._Diag_QrvcircA = perseus_utils.read_diag_milivolts(self.perseus, 13, 'A')
        self.push_change_event("Diag_QrvcircA", self._Diag_QrvcircA)
        self._Diag_QrvcircB = perseus_utils.read_diag_milivolts(self.perseus, 13, 'B')
        self.push_change_event("Diag_QrvcircB", self._Diag_QrvcircB)
        self._Diag_AmprvcircA = perseus_utils.read_diag_milivolts(self.perseus, 14, 'A')
        self.push_change_event("Diag_AmprvcircA", self._Diag_AmprvcircA)
        self._Diag_AmprvcircB = perseus_utils.read_diag_milivolts(self.perseus, 14, 'B')
        self.push_change_event("Diag_AmprvcircB", self._Diag_AmprvcircB)
        self._Diag_PhrvcircA = perseus_utils.read_diag_angle(self.perseus, 15, 'A')
        self.push_change_event("Diag_PhrvcircA", self._Diag_PhrvcircA)
        self._Diag_PhrvcircB = perseus_utils.read_diag_angle(self.perseus, 15, 'B')
        self.push_change_event("Diag_PhrvcircB", self._Diag_PhrvcircB)
        self._Diag_IfwloadA = perseus_utils.read_diag_milivolts(self.perseus, 16, 'A')
        self.push_change_event("Diag_IfwloadA", self._Diag_IfwloadA)
        self._Diag_IfwloadB = perseus_utils.read_diag_milivolts(self.perseus, 16, 'B')
        self.push_change_event("Diag_IfwloadB", self._Diag_IfwloadB)
        self._Diag_QfwloadA = perseus_utils.read_diag_milivolts(self.perseus, 17, 'A')
        self.push_change_event("Diag_QfwloadA", self._Diag_QfwloadA)
        self._Diag_QfwloadB = perseus_utils.read_diag_milivolts(self.perseus, 17, 'B')
        self.push_change_event("Diag_QfwloadB", self._Diag_QfwloadB)
        self._Diag_AmpfwloadA = perseus_utils.read_diag_milivolts(self.perseus, 18, 'A')
        self.push_change_event("Diag_AmpfwloadA", self._Diag_AmpfwloadA)
        self._Diag_AmpfwloadB = perseus_utils.read_diag_milivolts(self.perseus, 18, 'B')
        self.push_change_event("Diag_AmpfwloadB", self._Diag_AmpfwloadB)
        self._Diag_PhfwloadA = perseus_utils.read_diag_angle(self.perseus, 19, 'A')
        self.push_change_event("Diag_PhfwloadA", self._Diag_PhfwloadA)
        self._Diag_PhfwloadB = perseus_utils.read_diag_angle(self.perseus, 19, 'B')
        self.push_change_event("Diag_PhfwloadB", self._Diag_PhfwloadB)
        self._Diag_IfwhybloadA = perseus_utils.read_diag_milivolts(self.perseus, 20, 'A')
        self.push_change_event("Diag_IfwhybloadA", self._Diag_IfwhybloadA)
        self._Diag_IfwhybloadB = perseus_utils.read_diag_milivolts(self.perseus, 20, 'B')
        self.push_change_event("Diag_IfwhybloadB", self._Diag_IfwhybloadB)
        self._Diag_QfwhybloadA = perseus_utils.read_diag_milivolts(self.perseus, 21, 'A')
        self.push_change_event("Diag_QfwhybloadA", self._Diag_QfwhybloadA)
        self._Diag_QfwhybloadB = perseus_utils.read_diag_milivolts(self.perseus, 21, 'B')
        self.push_change_event("Diag_QfwhybloadB", self._Diag_QfwhybloadB)
        self._Diag_AmpfwhybloadA = perseus_utils.read_diag_milivolts(self.perseus, 22, 'A')
        self.push_change_event("Diag_AmpfwhybloadA", self._Diag_AmpfwhybloadA)
        self._Diag_AmpfwhybloadB = perseus_utils.read_diag_milivolts(self.perseus, 22, 'B')
        self.push_change_event("Diag_AmpfwhybloadB", self._Diag_AmpfwhybloadB)
        self._Diag_PhfwhybloadA = perseus_utils.read_diag_angle(self.perseus, 23, 'A')
        self.push_change_event("Diag_PhfwhybloadA", self._Diag_PhfwhybloadA)
        self._Diag_PhfwhybloadB = perseus_utils.read_diag_angle(self.perseus, 23, 'B')
        self.push_change_event("Diag_PhfwhybloadB", self._Diag_PhfwhybloadB)
        self._Diag_IrvcavA = perseus_utils.read_diag_milivolts(self.perseus, 24, 'A')
        self.push_change_event("Diag_IrvcavA", self._Diag_IrvcavA)
        self._Diag_IrvcavB = perseus_utils.read_diag_milivolts(self.perseus, 24, 'B')
        self.push_change_event("Diag_IrvcavB", self._Diag_IrvcavB)
        self._Diag_QrvcavA = perseus_utils.read_diag_milivolts(self.perseus, 25, 'A')
        self.push_change_event("Diag_QrvcavA", self._Diag_QrvcavA)
        self._Diag_QrvcavB = perseus_utils.read_diag_milivolts(self.perseus, 25, 'B')
        self.push_change_event("Diag_QrvcavB", self._Diag_QrvcavB)
        self._Diag_AmprvcavA = perseus_utils.read_diag_milivolts(self.perseus, 26, 'A')
        self.push_change_event("Diag_AmprvcavA", self._Diag_AmprvcavA)
        self._Diag_AmprvcavB = perseus_utils.read_diag_milivolts(self.perseus, 26, 'B')
        self.push_change_event("Diag_AmprvcavB", self._Diag_AmprvcavB)
        self._Diag_PhrvcavA = perseus_utils.read_diag_angle(self.perseus, 27, 'A')
        self.push_change_event("Diag_PhrvcavA", self._Diag_PhrvcavA)
        self._Diag_PhrvcavB = perseus_utils.read_diag_angle(self.perseus, 27, 'B')
        self.push_change_event("Diag_PhrvcavB", self._Diag_PhrvcavB)
        self._Diag_ImoA = perseus_utils.read_diag_milivolts(self.perseus, 28, 'A')
        self.push_change_event("Diag_ImoA", self._Diag_ImoA)
        self._Diag_ImoB = perseus_utils.read_diag_milivolts(self.perseus, 28, 'B')
        self.push_change_event("Diag_ImoB", self._Diag_ImoB)
        self._Diag_QmoA = perseus_utils.read_diag_milivolts(self.perseus, 29, 'A')
        self.push_change_event("Diag_QmoA", self._Diag_QmoA)
        self._Diag_QmoB = perseus_utils.read_diag_milivolts(self.perseus, 29, 'B')
        self.push_change_event("Diag_QmoB", self._Diag_QmoB)
        self._Diag_AmpmoA = perseus_utils.read_diag_milivolts(self.perseus, 30, 'A')
        self.push_change_event("Diag_AmpmoA", self._Diag_AmpmoA)
        self._Diag_AmpmoB = perseus_utils.read_diag_milivolts(self.perseus, 30, 'B')
        self.push_change_event("Diag_AmpmoB", self._Diag_AmpmoB)
        self._Diag_PhmoA = perseus_utils.read_diag_angle(self.perseus, 31, 'A')
        self.push_change_event("Diag_PhmoA", self._Diag_PhmoA)
        self._Diag_PhmoB = perseus_utils.read_diag_angle(self.perseus, 31, 'B')
        self.push_change_event("Diag_PhmoB", self._Diag_PhmoB)
        self._Diag_IlandauA = perseus_utils.read_diag_milivolts(self.perseus, 32, 'A')
        self.push_change_event("Diag_IlandauA", self._Diag_IlandauA)
        self._Diag_IlandauB = perseus_utils.read_diag_milivolts(self.perseus, 32, 'B')
        self.push_change_event("Diag_IlandauB", self._Diag_IlandauB)
        self._Diag_QlandauA = perseus_utils.read_diag_milivolts(self.perseus, 33, 'A')
        self.push_change_event("Diag_QlandauA", self._Diag_QlandauA)
        self._Diag_QlandauB = perseus_utils.read_diag_milivolts(self.perseus, 33, 'B')
        self.push_change_event("Diag_QlandauB", self._Diag_QlandauB)
        self._Diag_AmplandauA = perseus_utils.read_diag_milivolts(self.perseus, 34, 'A')
        self.push_change_event("Diag_AmplandauA", self._Diag_AmplandauA)
        self._Diag_AmplandauB = perseus_utils.read_diag_milivolts(self.perseus, 34, 'B')
        self.push_change_event("Diag_AmplandauB", self._Diag_AmplandauB)
        self._Diag_PhlandauA = perseus_utils.read_diag_angle(self.perseus, 35, 'A')
        self.push_change_event("Diag_PhlandauA", self._Diag_PhlandauA)
        self._Diag_PhlandauB = perseus_utils.read_diag_angle(self.perseus, 35, 'B')
        self.push_change_event("Diag_PhlandauB", self._Diag_PhlandauB)
        self._Diag_PlungerMovingManualTuningA = bool(perseus_utils.read_diag_direct(self.perseus, 60, 'A'))
        self.push_change_event("Diag_PlungerMovingManualTuningA", self._Diag_PlungerMovingManualTuningA)
        self._Diag_PlungerMovingManualTuningB = bool(perseus_utils.read_diag_direct(self.perseus, 60, 'B'))
        self.push_change_event("Diag_PlungerMovingManualTuningB", self._Diag_PlungerMovingManualTuningB)
        self._Diag_PlungerMovingUpManualTuningA = bool(perseus_utils.read_diag_direct(self.perseus, 61, 'A'))
        self.push_change_event("Diag_PlungerMovingUpManualTuningA", self._Diag_PlungerMovingUpManualTuningA)
        self._Diag_PlungerMovingUpManualTuningB = bool(perseus_utils.read_diag_direct(self.perseus, 61, 'B'))
        self.push_change_event("Diag_PlungerMovingUpManualTuningB", self._Diag_PlungerMovingUpManualTuningB)
        self._Diag_PlungerMovingAutomaticTuningA = bool(perseus_utils.read_diag_direct(self.perseus, 62, 'A'))
        self.push_change_event("Diag_PlungerMovingAutomaticTuningA", self._Diag_PlungerMovingAutomaticTuningA)
        self._Diag_PlungerMovingAutomaticTuningB = bool(perseus_utils.read_diag_direct(self.perseus, 62, 'B'))
        self.push_change_event("Diag_PlungerMovingAutomaticTuningB", self._Diag_PlungerMovingAutomaticTuningB)
        self._Diag_PlungerMovingUpAutomaticTuningA = bool(perseus_utils.read_diag_direct(self.perseus, 63, 'A'))
        self.push_change_event("Diag_PlungerMovingUpAutomaticTuningA", self._Diag_PlungerMovingUpAutomaticTuningA)
        self._Diag_PlungerMovingUpAutomaticTuningB = bool(perseus_utils.read_diag_direct(self.perseus, 63, 'B'))
        self.push_change_event("Diag_PlungerMovingUpAutomaticTuningB", self._Diag_PlungerMovingUpAutomaticTuningB)
        self._Diag_DephaseMoLandauA = perseus_utils.read_diag_angle(self.perseus, 64, 'A')
        self.push_change_event("Diag_DephaseMoLandauA", self._Diag_DephaseMoLandauA)
        self._Diag_DephaseMoLandauB = perseus_utils.read_diag_angle(self.perseus, 64, 'B')
        self.push_change_event("Diag_DephaseMoLandauB", self._Diag_DephaseMoLandauB)
        self._Diag_Rvtet1A = self.read_Diag_Rvtet1A()
        self.push_change_event("Diag_Rvtet1A", self._Diag_Rvtet1A)
        self._Diag_Rvtet1B = self.read_Diag_Rvtet1B()
        self.push_change_event("Diag_Rvtet1B", self._Diag_Rvtet1B)
        self._Diag_Rvtet2A = self.read_Diag_Rvtet2A()
        self.push_change_event("Diag_Rvtet2A", self._Diag_Rvtet2A)
        self._Diag_Rvtet2B = self.read_Diag_Rvtet2B()
        self.push_change_event("Diag_Rvtet2B", self._Diag_Rvtet2B)
        self._Diag_RvcircA = self.read_Diag_RvcircA()
        self.push_change_event("Diag_RvcircA", self._Diag_RvcircA)
        self._Diag_RvcircB = self.read_Diag_RvcircB()
        self.push_change_event("Diag_RvcircB", self._Diag_RvcircB)
        self._Diag_FwloadA = self.read_Diag_FwloadA()
        self.push_change_event("Diag_FwloadA", self._Diag_FwloadA)
        self._Diag_FwloadB = self.read_Diag_FwloadB()
        self.push_change_event("Diag_FwloadB", self._Diag_FwloadB)
        self._Diag_FwhybloadA = self.read_Diag_FwhybloadA()
        self.push_change_event("Diag_FwhybloadA", self._Diag_FwhybloadA)
        self._Diag_FwhybloadB = self.read_Diag_FwhybloadB()
        self.push_change_event("Diag_FwhybloadB", self._Diag_FwhybloadB)
        self._Diag_RvcavA = self.read_Diag_RvcavA()
        self.push_change_event("Diag_RvcavA", self._Diag_RvcavA)
        self._Diag_RvcavB = self.read_Diag_RvcavB()
        self.push_change_event("Diag_RvcavB", self._Diag_RvcavB)
        self._Diag_ArcsA = self.read_Diag_ArcsA()
        self.push_change_event("Diag_ArcsA", self._Diag_ArcsA)
        self._Diag_ArcsB = self.read_Diag_ArcsB()
        self.push_change_event("Diag_ArcsB", self._Diag_ArcsB)
        self._Diag_VacuumA = self.read_Diag_VacuumA()
        self.push_change_event("Diag_VacuumA", self._Diag_VacuumA)
        self._Diag_VacuumB = self.read_Diag_VacuumB()
        self.push_change_event("Diag_VacuumB", self._Diag_VacuumB)
        self._Diag_ManualInterlockA = self.read_Diag_ManualInterlockA()
        self.push_change_event("Diag_ManualInterlockA", self._Diag_ManualInterlockA)
        self._Diag_ManualInterlockB = self.read_Diag_ManualInterlockB()
        self.push_change_event("Diag_ManualInterlockB", self._Diag_ManualInterlockB)
        self._Diag_ExternalItckA = self.read_Diag_ExternalItckA()
        self.push_change_event("Diag_ExternalItckA", self._Diag_ExternalItckA)
        self._Diag_ExternalItckB = self.read_Diag_ExternalItckB()
        self.push_change_event("Diag_ExternalItckB", self._Diag_ExternalItckB)
        self._Diag_PlungerEndSwitchUpA = self.read_Diag_PlungerEndSwitchUpA()
        self.push_change_event("Diag_PlungerEndSwitchUpA", self._Diag_PlungerEndSwitchUpA)
        self._Diag_PlungerEndSwitchUpB = self.read_Diag_PlungerEndSwitchUpB()
        self.push_change_event("Diag_PlungerEndSwitchUpB", self._Diag_PlungerEndSwitchUpB)
        self._Diag_PlungerEndSwitchDownA = self.read_Diag_PlungerEndSwitchDownA()
        self.push_change_event("Diag_PlungerEndSwitchDownA", self._Diag_PlungerEndSwitchDownA)
        self._Diag_PlungerEndSwitchDownB = self.read_Diag_PlungerEndSwitchDownB()
        self.push_change_event("Diag_PlungerEndSwitchDownB", self._Diag_PlungerEndSwitchDownB)
        self._Diag_Timestamp1A = self.read_Diag_Timestamp1A()
        self.push_change_event("Diag_Timestamp1A", self._Diag_Timestamp1A)
        self._Diag_Timestamp1B = self.read_Diag_Timestamp1B()
        self.push_change_event("Diag_Timestamp1B", self._Diag_Timestamp1B)
        self._Diag_Timestamp2A = self.read_Diag_Timestamp2A()
        self.push_change_event("Diag_Timestamp2A", self._Diag_Timestamp2A)
        self._Diag_Timestamp2B = self.read_Diag_Timestamp2B()
        self.push_change_event("Diag_Timestamp2B", self._Diag_Timestamp2B)
        self._Diag_Timestamp3A = self.read_Diag_Timestamp3A()
        self.push_change_event("Diag_Timestamp3A", self._Diag_Timestamp3A)
        self._Diag_Timestamp3B = self.read_Diag_Timestamp3B()
        self.push_change_event("Diag_Timestamp3B", self._Diag_Timestamp3B)
        self._Diag_Timestamp4A = self.read_Diag_Timestamp4A()
        self.push_change_event("Diag_Timestamp4A", self._Diag_Timestamp4A)
        self._Diag_Timestamp4B = self.read_Diag_Timestamp4B()
        self.push_change_event("Diag_Timestamp4B", self._Diag_Timestamp4B)
        self._Diag_Timestamp5A = self.read_Diag_Timestamp5A()
        self.push_change_event("Diag_Timestamp5A", self._Diag_Timestamp5A)
        self._Diag_Timestamp5B = self.read_Diag_Timestamp5B()
        self.push_change_event("Diag_Timestamp5B", self._Diag_Timestamp5B)
        self._Diag_Timestamp6A = self.read_Diag_Timestamp6A()
        self.push_change_event("Diag_Timestamp6A", self._Diag_Timestamp6A)
        self._Diag_Timestamp6B = self.read_Diag_Timestamp6B()
        self.push_change_event("Diag_Timestamp6B", self._Diag_Timestamp6B)
        self._Diag_Timestamp7A = self.read_Diag_Timestamp7A()
        self.push_change_event("Diag_Timestamp7A", self._Diag_Timestamp7A)
        self._Diag_Timestamp7B = self.read_Diag_Timestamp7B()
        self.push_change_event("Diag_Timestamp7B", self._Diag_Timestamp7B)
        self._Diag_DacsDisableCommandA = self.read_Diag_DacsDisableCommandA()
        self.push_change_event("Diag_DacsDisableCommandA", self._Diag_DacsDisableCommandA)
        self._Diag_DacsDisableCommandB = self.read_Diag_DacsDisableCommandB()
        self.push_change_event("Diag_DacsDisableCommandB", self._Diag_DacsDisableCommandB)
        self._Diag_PinSwitchA = self.read_Diag_PinSwitchA()
        self.push_change_event("Diag_PinSwitchA", self._Diag_PinSwitchA)
        self._Diag_PinSwitchB = self.read_Diag_PinSwitchB()
        self.push_change_event("Diag_PinSwitchB", self._Diag_PinSwitchB)
        self._Diag_FdlTriggerToLoopsdiagboardA = self.read_Diag_FdlTriggerToLoopsdiagboardA()
        self.push_change_event("Diag_FdlTriggerToLoopsdiagboardA", self._Diag_FdlTriggerToLoopsdiagboardA)
        self._Diag_FdlTriggerToLoopsdiagboardB = self.read_Diag_FdlTriggerToLoopsdiagboardB()
        self.push_change_event("Diag_FdlTriggerToLoopsdiagboardB", self._Diag_FdlTriggerToLoopsdiagboardB)
        self._Diag_OutputToPlcA = self.read_Diag_OutputToPlcA()
        self.push_change_event("Diag_OutputToPlcA", self._Diag_OutputToPlcA)
        self._Diag_OutputToPlcB = self.read_Diag_OutputToPlcB()
        self.push_change_event("Diag_OutputToPlcB", self._Diag_OutputToPlcB)
        self._Diag_OutputToMpsA = self.read_Diag_OutputToMpsA()
        self.push_change_event("Diag_OutputToMpsA", self._Diag_OutputToMpsA)
        self._Diag_OutputToMpsB = self.read_Diag_OutputToMpsB()
        self.push_change_event("Diag_OutputToMpsB", self._Diag_OutputToMpsB)
        self._Diag_AmpRvtet1b = math.sqrt((self._Diag_Irvtet1B**2) + (self._Diag_Qrvtet1B**2))
        self.push_change_event("Diag_AmpRvtet1b", self._Diag_AmpRvtet1b)
        self._Diag_AmpRvtet1a = math.sqrt((self._Diag_Irvtet1A**2) + (self._Diag_Qrvtet1A**2))
        self.push_change_event("Diag_AmpRvtet1a", self._Diag_AmpRvtet1a)
        self._Diag_AmpMoa = math.sqrt((self._Diag_ImoA**2) + (self._Diag_QmoA**2))
        self.push_change_event("Diag_AmpMoa", self._Diag_AmpMoa)
        self._Diag_AmpLandaua = math.sqrt((self._Diag_IlandauA**2) + (self._Diag_QlandauA**2))
        self.push_change_event("Diag_AmpLandaua", self._Diag_AmpLandaua)
        self._Diag_AmpFwloada = math.sqrt((self._Diag_IfwloadA**2) + (self._Diag_QfwloadA**2))
        self.push_change_event("Diag_AmpFwloada", self._Diag_AmpFwloada)
        self._Diag_AmpRvtet2b = math.sqrt((self._Diag_Irvtet2B**2) + (self._Diag_Qrvtet2B**2))
        self.push_change_event("Diag_AmpRvtet2b", self._Diag_AmpRvtet2b)
        self._Diag_AmpRvtet2a = math.sqrt((self._Diag_Irvtet2A**2) + (self._Diag_Qrvtet2A**2))
        self.push_change_event("Diag_AmpRvtet2a", self._Diag_AmpRvtet2a)
        self._Diag_AmpFwloadb = math.sqrt((self._Diag_IfwloadB**2) + (self._Diag_QfwloadB**2))
        self.push_change_event("Diag_AmpFwloadb", self._Diag_AmpFwloadb)
        self._Diag_AmpRvcavb = math.sqrt((self._Diag_IrvcavB**2) + (self._Diag_QrvcavB**2))
        self.push_change_event("Diag_AmpRvcavb", self._Diag_AmpRvcavb)
        self._Diag_AmpRvcava = math.sqrt((self._Diag_IrvcavA**2) + (self._Diag_QrvcavA**2))
        self.push_change_event("Diag_AmpRvcava", self._Diag_AmpRvcava)
        self._Diag_AmpFwcircb = math.sqrt((self._Diag_IfwcircB**2) + (self._Diag_QfwcircB**2))
        self.push_change_event("Diag_AmpFwcircb", self._Diag_AmpFwcircb)
        self._Diag_AmpFwcirca = math.sqrt((self._Diag_IfwcircA**2) + (self._Diag_QfwcircA**2))
        self.push_change_event("Diag_AmpFwcirca", self._Diag_AmpFwcirca)
        self._Diag_AmpMob = math.sqrt((self._Diag_ImoB**2) + (self._Diag_QmoB**2))
        self.push_change_event("Diag_AmpMob", self._Diag_AmpMob)
        self._Diag_AmpRvcirca = math.sqrt((self._Diag_IrvcircA**2) + (self._Diag_QrvcircA**2))
        self.push_change_event("Diag_AmpRvcirca", self._Diag_AmpRvcirca)
        self._Diag_AmpRvcircb = math.sqrt((self._Diag_IrvcircB**2) + (self._Diag_QrvcircB**2))
        self.push_change_event("Diag_AmpRvcircb", self._Diag_AmpRvcircb)
        self._Diag_AmpFwhybloadb = math.sqrt((self._Diag_IfwhybloadB**2) + (self._Diag_QfwhybloadB**2))
        self.push_change_event("Diag_AmpFwhybloadb", self._Diag_AmpFwhybloadb)
        self._Diag_AmpFwhybloada = math.sqrt((self._Diag_IfwhybloadA**2) + (self._Diag_QfwhybloadA**2))
        self.push_change_event("Diag_AmpFwhybloada", self._Diag_AmpFwhybloada)
        self._Diag_AmpLandaub = math.sqrt((self._Diag_IlandauB**2) + (self._Diag_QlandauB**2))
        self.push_change_event("Diag_AmpLandaub", self._Diag_AmpLandaub)
        self._Diag_PhRvtet1b = math.degrees(math.atan2(self._Diag_Qrvtet1B, self._Diag_Irvtet1B))
        self.push_change_event("Diag_PhRvtet1b", self._Diag_PhRvtet1b)
        self._Diag_PhRvtet1a = math.degrees(math.atan2(self._Diag_Qrvtet1A, self._Diag_Irvtet1A))
        self.push_change_event("Diag_PhRvtet1a", self._Diag_PhRvtet1a)
        self._Diag_PhMoa = math.degrees(math.atan2(self._Diag_QmoA, self._Diag_ImoA))
        self.push_change_event("Diag_PhMoa", self._Diag_PhMoa)
        self._Diag_PhLandaua = math.degrees(math.atan2(self._Diag_QlandauA, self._Diag_IlandauA))
        self.push_change_event("Diag_PhLandaua", self._Diag_PhLandaua)
        self._Diag_PhFwloada = math.degrees(math.atan2(self._Diag_QfwloadA, self._Diag_IfwloadA))
        self.push_change_event("Diag_PhFwloada", self._Diag_PhFwloada)
        self._Diag_PhRvtet2b = math.degrees(math.atan2(self._Diag_Qrvtet2B, self._Diag_Irvtet2B))
        self.push_change_event("Diag_PhRvtet2b", self._Diag_PhRvtet2b)
        self._Diag_PhRvtet2a = math.degrees(math.atan2(self._Diag_Qrvtet2A, self._Diag_Irvtet2A))
        self.push_change_event("Diag_PhRvtet2a", self._Diag_PhRvtet2a)
        self._Diag_PhFwloadb = math.degrees(math.atan2(self._Diag_QfwloadB, self._Diag_IfwloadB))
        self.push_change_event("Diag_PhFwloadb", self._Diag_PhFwloadb)
        self._Diag_PhRvcavb = math.degrees(math.atan2(self._Diag_QrvcavB, self._Diag_IrvcavB))
        self.push_change_event("Diag_PhRvcavb", self._Diag_PhRvcavb)
        self._Diag_PhRvcava = math.degrees(math.atan2(self._Diag_QrvcavA, self._Diag_IrvcavA))
        self.push_change_event("Diag_PhRvcava", self._Diag_PhRvcava)
        self._Diag_PhFwcircb = math.degrees(math.atan2(self._Diag_QfwcircB, self._Diag_IfwcircB))
        self.push_change_event("Diag_PhFwcircb", self._Diag_PhFwcircb)
        self._Diag_PhFwcirca = math.degrees(math.atan2(self._Diag_QfwcircA, self._Diag_IfwcircA))
        self.push_change_event("Diag_PhFwcirca", self._Diag_PhFwcirca)
        self._Diag_PhMob = math.degrees(math.atan2(self._Diag_QmoB, self._Diag_ImoB))
        self.push_change_event("Diag_PhMob", self._Diag_PhMob)
        self._Diag_PhRvcirca = math.degrees(math.atan2(self._Diag_QrvcircA, self._Diag_IrvcircA))
        self.push_change_event("Diag_PhRvcirca", self._Diag_PhRvcirca)
        self._Diag_PhRvcircb = math.degrees(math.atan2(self._Diag_QrvcircB, self._Diag_IrvcircB))
        self.push_change_event("Diag_PhRvcircb", self._Diag_PhRvcircb)
        self._Diag_PhFwhybloadb = math.degrees(math.atan2(self._Diag_QfwhybloadB, self._Diag_IfwhybloadB))
        self.push_change_event("Diag_PhFwhybloadb", self._Diag_PhFwhybloadb)
        self._Diag_PhFwhybloada = math.degrees(math.atan2(self._Diag_QfwhybloadA, self._Diag_IfwhybloadA))
        self.push_change_event("Diag_PhFwhybloada", self._Diag_PhFwhybloada)
        self._Diag_PhLandaub = math.degrees(math.atan2(self._Diag_QlandauB, self._Diag_IlandauB))
        self.push_change_event("Diag_PhLandaub", self._Diag_PhLandaub)

    @command
    def read_attrs(self):

        data = self.get_Rvtet1A()
        self.push_change_event("Rvtet1A", data)
        data = self.get_Rvtet1B()
        self.push_change_event("Rvtet1B", data)
        data = self.get_Rvtet2A()
        self.push_change_event("Rvtet2A", data)
        data = self.get_Rvtet2B()
        self.push_change_event("Rvtet2B", data)
        data = self.get_RvcircA()
        self.push_change_event("RvcircA", data)
        data = self.get_RvcircB()
        self.push_change_event("RvcircB", data)
        data = self.get_FwloadA()
        self.push_change_event("FwloadA", data)
        data = self.get_FwloadB()
        self.push_change_event("FwloadB", data)
        data = self.get_FwhybloadA()
        self.push_change_event("FwhybloadA", data)
        data = self.get_FwhybloadB()
        self.push_change_event("FwhybloadB", data)
        data = self.get_RvcavA()
        self.push_change_event("RvcavA", data)
        data = self.get_RvcavB()
        self.push_change_event("RvcavB", data)
        data = bool(self.get_ManualInterlockA())
        self.push_change_event("ManualInterlockA", data)
        data = bool(self.get_ManualInterlockB())
        self.push_change_event("ManualInterlockB", data)
        data = self.get_DisableItckRvtet1A()
        self.push_change_event("DisableItckRvtet1A", data)
        data = self.get_DisableItckRvtet1B()
        self.push_change_event("DisableItckRvtet1B", data)
        data = self.get_DisableItckRvtet2A()
        self.push_change_event("DisableItckRvtet2A", data)
        data = self.get_DisableItckRvtet2B()
        self.push_change_event("DisableItckRvtet2B", data)
        data = self.get_DisableItckRvcircA()
        self.push_change_event("DisableItckRvcircA", data)
        data = self.get_DisableItckRvcircB()
        self.push_change_event("DisableItckRvcircB", data)
        data = self.get_DisableItckFwloadA()
        self.push_change_event("DisableItckFwloadA", data)
        data = self.get_DisableItckFwloadB()
        self.push_change_event("DisableItckFwloadB", data)
        data = self.get_DisableItckFwhybloadA()
        self.push_change_event("DisableItckFwhybloadA", data)
        data = self.get_DisableItckFwhybloadB()
        self.push_change_event("DisableItckFwhybloadB", data)
        data = self.get_DisableItckRvcavA()
        self.push_change_event("DisableItckRvcavA", data)
        data = self.get_DisableItckRvcavB()
        self.push_change_event("DisableItckRvcavB", data)
        data = self.get_DisableItckArcsA()
        self.push_change_event("DisableItckArcsA", data)
        data = self.get_DisableItckArcsB()
        self.push_change_event("DisableItckArcsB", data)
        data = self.get_DisableItckVaccumA()
        self.push_change_event("DisableItckVaccumA", data)
        data = self.get_DisableItckVaccumB()
        self.push_change_event("DisableItckVaccumB", data)
        data = self.get_DisableItckManualInterlockA()
        self.push_change_event("DisableItckManualInterlockA", data)
        data = self.get_DisableItckManualInterlockB()
        self.push_change_event("DisableItckManualInterlockB", data)
        data = self.get_DisableItckPlungerEndSwitchesUpA()
        self.push_change_event("DisableItckPlungerEndSwitchesUpA", data)
        data = self.get_DisableItckPlungerEndSwitchesUpB()
        self.push_change_event("DisableItckPlungerEndSwitchesUpB", data)
        data = self.get_DisableItckPlungerEndSwitchesDownA()
        self.push_change_event("DisableItckPlungerEndSwitchesDownA", data)
        data = self.get_DisableItckPlungerEndSwitchesDownB()
        self.push_change_event("DisableItckPlungerEndSwitchesDownB", data)
        data = self.get_DisableItckMpsA()
        self.push_change_event("DisableItckMpsA", data)
        data = self.get_DisableItckMpsB()
        self.push_change_event("DisableItckMpsB", data)
        data = self.get_SamplesToAverageA()
        self.push_change_event("SamplesToAverageA", data)
        data = self.get_SamplesToAverageB()
        self.push_change_event("SamplesToAverageB", data)
        data = bool(self.get_PulseupLogicInversionA())
        self.push_change_event("PulseupLogicInversionA", data)
        data = bool(self.get_PulseupLogicInversionB())
        self.push_change_event("PulseupLogicInversionB", data)
        data = self.get_EndSwitchesConnectedToNoNcContactA()
        self.push_change_event("EndSwitchesConnectedToNoNcContactA", data)
        data = self.get_EndSwitchesConnectedToNoNcContactB()
        self.push_change_event("EndSwitchesConnectedToNoNcContactB", data)
        data = bool(self.get_LookrefA())
        self.push_change_event("LookrefA", data)
        data = bool(self.get_LookrefB())
        self.push_change_event("LookrefB", data)
        data = self.get_QuadrefA()
        self.push_change_event("QuadrefA", data)
        data = self.get_QuadrefB()
        self.push_change_event("QuadrefB", data)
        data = bool(self.get_SpareDo1A())
        self.push_change_event("SpareDo1A", data)
        data = bool(self.get_SpareDo1B())
        self.push_change_event("SpareDo1B", data)
        data = bool(self.get_SpareDo2A())
        self.push_change_event("SpareDo2A", data)
        data = bool(self.get_SpareDo2B())
        self.push_change_event("SpareDo2B", data)
        data = bool(self.get_SpareDo3A())
        self.push_change_event("SpareDo3A", data)
        data = bool(self.get_SpareDo3B())
        self.push_change_event("SpareDo3B", data)
        data = bool(self.get_FdlSwTriggerA())
        self.push_change_event("FdlSwTriggerA", data)
        data = bool(self.get_FdlSwTriggerB())
        self.push_change_event("FdlSwTriggerB", data)
        data = bool(self.get_ResetInterlocksCavA())
        self.push_change_event("ResetInterlocksCavA", data)
        data = bool(self.get_ResetInterlocksCavB())
        self.push_change_event("ResetInterlocksCavB", data)
        data = bool(self.get_LandautuningenableA())
        self.push_change_event("LandautuningenableA", data)
        data = bool(self.get_LandautuningenableB())
        self.push_change_event("LandautuningenableB", data)
        data = bool(self.get_LandautuningresetA())
        self.push_change_event("LandautuningresetA", data)
        data = bool(self.get_LandautuningresetB())
        self.push_change_event("LandautuningresetB", data)
        data = bool(self.get_MovelandauupA())
        self.push_change_event("MovelandauupA", data)
        data = bool(self.get_MovelandauupB())
        self.push_change_event("MovelandauupB", data)
        data = bool(self.get_MovelandauplgA())
        self.push_change_event("MovelandauplgA", data)
        data = bool(self.get_MovelandauplgB())
        self.push_change_event("MovelandauplgB", data)
        data = self.get_NumstepsA()
        self.push_change_event("NumstepsA", data)
        data = self.get_NumstepsB()
        self.push_change_event("NumstepsB", data)
        data = self.get_LandauphaseoffsetA()
        self.push_change_event("LandauphaseoffsetA", data)
        data = self.get_LandauphaseoffsetB()
        self.push_change_event("LandauphaseoffsetB", data)
        data = self.get_LandaumarginupA()
        self.push_change_event("LandaumarginupA", data)
        data = self.get_LandaumarginupB()
        self.push_change_event("LandaumarginupB", data)
        data = self.get_LandauMarginLowA()
        self.push_change_event("LandauMarginLowA", data)
        data = self.get_LandauMarginLowB()
        self.push_change_event("LandauMarginLowB", data)
        data = self.get_MinimumLandauAmplitudeA()
        self.push_change_event("MinimumLandauAmplitudeA", data)
        data = self.get_MinimumLandauAmplitudeB()
        self.push_change_event("MinimumLandauAmplitudeB", data)
        data = bool(self.get_LandauPositiveEnableA())
        self.push_change_event("LandauPositiveEnableA", data)
        data = bool(self.get_LandauPositiveEnableB())
        self.push_change_event("LandauPositiveEnableB", data)
        data = self.get_LandauampsettingA()
        self.push_change_event("LandauampsettingA", data)
        data = self.get_LandauampsettingB()
        self.push_change_event("LandauampsettingB", data)
        data = bool(self.get_DisitckRvtet1DacsoffloopsstbyA())
        self.push_change_event("DisitckRvtet1DacsoffloopsstbyA", data)
        data = bool(self.get_DisitckRvtet1DacsoffloopsstbyB())
        self.push_change_event("DisitckRvtet1DacsoffloopsstbyB", data)
        data = bool(self.get_DisitckRvtet1PindiodeswitchA())
        self.push_change_event("DisitckRvtet1PindiodeswitchA", data)
        data = bool(self.get_DisitckRvtet1PindiodeswitchB())
        self.push_change_event("DisitckRvtet1PindiodeswitchB", data)
        data = bool(self.get_DisitckRvtet1FdltrgA())
        self.push_change_event("DisitckRvtet1FdltrgA", data)
        data = bool(self.get_DisitckRvtet1FdltrgB())
        self.push_change_event("DisitckRvtet1FdltrgB", data)
        data = bool(self.get_DisitckRvtet1PlctxoffA())
        self.push_change_event("DisitckRvtet1PlctxoffA", data)
        data = bool(self.get_DisitckRvtet1PlctxoffB())
        self.push_change_event("DisitckRvtet1PlctxoffB", data)
        data = bool(self.get_DisitckRvtet1MpsA())
        self.push_change_event("DisitckRvtet1MpsA", data)
        data = bool(self.get_DisitckRvtet1MpsB())
        self.push_change_event("DisitckRvtet1MpsB", data)
        data = bool(self.get_DisitckRvtet1DiagA())
        self.push_change_event("DisitckRvtet1DiagA", data)
        data = bool(self.get_DisitckRvtet1DiagB())
        self.push_change_event("DisitckRvtet1DiagB", data)
        data = bool(self.get_DisitckRvtet2DacsoffloopsstbyA())
        self.push_change_event("DisitckRvtet2DacsoffloopsstbyA", data)
        data = bool(self.get_DisitckRvtet2DacsoffloopsstbyB())
        self.push_change_event("DisitckRvtet2DacsoffloopsstbyB", data)
        data = bool(self.get_DisitckRvtet2PindiodeswitchA())
        self.push_change_event("DisitckRvtet2PindiodeswitchA", data)
        data = bool(self.get_DisitckRvtet2PindiodeswitchB())
        self.push_change_event("DisitckRvtet2PindiodeswitchB", data)
        data = bool(self.get_DisitckRvtet2FdltrgA())
        self.push_change_event("DisitckRvtet2FdltrgA", data)
        data = bool(self.get_DisitckRvtet2FdltrgB())
        self.push_change_event("DisitckRvtet2FdltrgB", data)
        data = bool(self.get_DisitckRvtet2PlctxoffA())
        self.push_change_event("DisitckRvtet2PlctxoffA", data)
        data = bool(self.get_DisitckRvtet2PlctxoffB())
        self.push_change_event("DisitckRvtet2PlctxoffB", data)
        data = bool(self.get_DisitckRvtet2MpsA())
        self.push_change_event("DisitckRvtet2MpsA", data)
        data = bool(self.get_DisitckRvtet2MpsB())
        self.push_change_event("DisitckRvtet2MpsB", data)
        data = bool(self.get_DisitckRvtet2DiagA())
        self.push_change_event("DisitckRvtet2DiagA", data)
        data = bool(self.get_DisitckRvtet2DiagB())
        self.push_change_event("DisitckRvtet2DiagB", data)
        data = bool(self.get_DisitckRvcircDacsoffloopsstbyA())
        self.push_change_event("DisitckRvcircDacsoffloopsstbyA", data)
        data = bool(self.get_DisitckRvcircDacsoffloopsstbyB())
        self.push_change_event("DisitckRvcircDacsoffloopsstbyB", data)
        data = bool(self.get_DisitckRvcircPindiodeswitchA())
        self.push_change_event("DisitckRvcircPindiodeswitchA", data)
        data = bool(self.get_DisitckRvcircPindiodeswitchB())
        self.push_change_event("DisitckRvcircPindiodeswitchB", data)
        data = bool(self.get_DisitckRvcircFdltrgA())
        self.push_change_event("DisitckRvcircFdltrgA", data)
        data = bool(self.get_DisitckRvcircFdltrgB())
        self.push_change_event("DisitckRvcircFdltrgB", data)
        data = bool(self.get_DisitckRvcircPlctxoffA())
        self.push_change_event("DisitckRvcircPlctxoffA", data)
        data = bool(self.get_DisitckRvcircPlctxoffB())
        self.push_change_event("DisitckRvcircPlctxoffB", data)
        data = bool(self.get_DisitckRvcircMpsA())
        self.push_change_event("DisitckRvcircMpsA", data)
        data = bool(self.get_DisitckRvcircMpsB())
        self.push_change_event("DisitckRvcircMpsB", data)
        data = bool(self.get_DisitckRvcircDiagA())
        self.push_change_event("DisitckRvcircDiagA", data)
        data = bool(self.get_DisitckRvcircDiagB())
        self.push_change_event("DisitckRvcircDiagB", data)
        data = bool(self.get_DisitckFwloadDacsoffloopsstbyA())
        self.push_change_event("DisitckFwloadDacsoffloopsstbyA", data)
        data = bool(self.get_DisitckFwloadDacsoffloopsstbyB())
        self.push_change_event("DisitckFwloadDacsoffloopsstbyB", data)
        data = bool(self.get_DisitckFwloadPindiodeswitchA())
        self.push_change_event("DisitckFwloadPindiodeswitchA", data)
        data = bool(self.get_DisitckFwloadPindiodeswitchB())
        self.push_change_event("DisitckFwloadPindiodeswitchB", data)
        data = bool(self.get_DisitckFwloadFdltrgA())
        self.push_change_event("DisitckFwloadFdltrgA", data)
        data = bool(self.get_DisitckFwloadFdltrgB())
        self.push_change_event("DisitckFwloadFdltrgB", data)
        data = bool(self.get_DisitckFwloadPlctxoffA())
        self.push_change_event("DisitckFwloadPlctxoffA", data)
        data = bool(self.get_DisitckFwloadPlctxoffB())
        self.push_change_event("DisitckFwloadPlctxoffB", data)
        data = bool(self.get_DisitckFwloadMpsA())
        self.push_change_event("DisitckFwloadMpsA", data)
        data = bool(self.get_DisitckFwloadMpsB())
        self.push_change_event("DisitckFwloadMpsB", data)
        data = bool(self.get_DisitckFwloadDiagA())
        self.push_change_event("DisitckFwloadDiagA", data)
        data = bool(self.get_DisitckFwloadDiagB())
        self.push_change_event("DisitckFwloadDiagB", data)
        data = bool(self.get_DisitckFwhybloadDacsoffloopsstbyA())
        self.push_change_event("DisitckFwhybloadDacsoffloopsstbyA", data)
        data = bool(self.get_DisitckFwhybloadDacsoffloopsstbyB())
        self.push_change_event("DisitckFwhybloadDacsoffloopsstbyB", data)
        data = bool(self.get_DisitckFwhybloadPindiodeswitchA())
        self.push_change_event("DisitckFwhybloadPindiodeswitchA", data)
        data = bool(self.get_DisitckFwhybloadPindiodeswitchB())
        self.push_change_event("DisitckFwhybloadPindiodeswitchB", data)
        data = bool(self.get_DisitckFwhybloadFdltrgA())
        self.push_change_event("DisitckFwhybloadFdltrgA", data)
        data = bool(self.get_DisitckFwhybloadFdltrgB())
        self.push_change_event("DisitckFwhybloadFdltrgB", data)
        data = bool(self.get_DisitckFwhybloadPlctxoffA())
        self.push_change_event("DisitckFwhybloadPlctxoffA", data)
        data = bool(self.get_DisitckFwhybloadPlctxoffB())
        self.push_change_event("DisitckFwhybloadPlctxoffB", data)
        data = bool(self.get_DisitckFwhybloadMpsA())
        self.push_change_event("DisitckFwhybloadMpsA", data)
        data = bool(self.get_DisitckFwhybloadMpsB())
        self.push_change_event("DisitckFwhybloadMpsB", data)
        data = bool(self.get_DisitckFwhybloadDiagA())
        self.push_change_event("DisitckFwhybloadDiagA", data)
        data = bool(self.get_DisitckFwhybloadDiagB())
        self.push_change_event("DisitckFwhybloadDiagB", data)
        data = bool(self.get_DisitckRvcavDacsoffloopsstbyA())
        self.push_change_event("DisitckRvcavDacsoffloopsstbyA", data)
        data = bool(self.get_DisitckRvcavDacsoffloopsstbyB())
        self.push_change_event("DisitckRvcavDacsoffloopsstbyB", data)
        data = bool(self.get_DisitckRvcavPindiodeswitchA())
        self.push_change_event("DisitckRvcavPindiodeswitchA", data)
        data = bool(self.get_DisitckRvcavPindiodeswitchB())
        self.push_change_event("DisitckRvcavPindiodeswitchB", data)
        data = bool(self.get_DisitckRvcavFdltrgA())
        self.push_change_event("DisitckRvcavFdltrgA", data)
        data = bool(self.get_DisitckRvcavFdltrgB())
        self.push_change_event("DisitckRvcavFdltrgB", data)
        data = bool(self.get_DisitckRvcavPlctxoffA())
        self.push_change_event("DisitckRvcavPlctxoffA", data)
        data = bool(self.get_DisitckRvcavPlctxoffB())
        self.push_change_event("DisitckRvcavPlctxoffB", data)
        data = bool(self.get_DisitckRvcavMpsA())
        self.push_change_event("DisitckRvcavMpsA", data)
        data = bool(self.get_DisitckRvcavMpsB())
        self.push_change_event("DisitckRvcavMpsB", data)
        data = bool(self.get_DisitckRvcavDiagA())
        self.push_change_event("DisitckRvcavDiagA", data)
        data = bool(self.get_DisitckRvcavDiagB())
        self.push_change_event("DisitckRvcavDiagB", data)
        data = bool(self.get_DisitckArcsDacsoffloopsstbyA())
        self.push_change_event("DisitckArcsDacsoffloopsstbyA", data)
        data = bool(self.get_DisitckArcsDacsoffloopsstbyB())
        self.push_change_event("DisitckArcsDacsoffloopsstbyB", data)
        data = bool(self.get_DisitckArcsPindiodeswitchA())
        self.push_change_event("DisitckArcsPindiodeswitchA", data)
        data = bool(self.get_DisitckArcsPindiodeswitchB())
        self.push_change_event("DisitckArcsPindiodeswitchB", data)
        data = bool(self.get_DisitckArcsFdltrgA())
        self.push_change_event("DisitckArcsFdltrgA", data)
        data = bool(self.get_DisitckArcsFdltrgB())
        self.push_change_event("DisitckArcsFdltrgB", data)
        data = bool(self.get_DisitckArcsPlctxoffA())
        self.push_change_event("DisitckArcsPlctxoffA", data)
        data = bool(self.get_DisitckArcsPlctxoffB())
        self.push_change_event("DisitckArcsPlctxoffB", data)
        data = bool(self.get_DisitckArcsMpsA())
        self.push_change_event("DisitckArcsMpsA", data)
        data = bool(self.get_DisitckArcsMpsB())
        self.push_change_event("DisitckArcsMpsB", data)
        data = bool(self.get_DisitckArcsDiagA())
        self.push_change_event("DisitckArcsDiagA", data)
        data = bool(self.get_DisitckArcsDiagB())
        self.push_change_event("DisitckArcsDiagB", data)
        data = bool(self.get_DisitckVacuumDacsoffloopsstbyA())
        self.push_change_event("DisitckVacuumDacsoffloopsstbyA", data)
        data = bool(self.get_DisitckVacuumDacsoffloopsstbyB())
        self.push_change_event("DisitckVacuumDacsoffloopsstbyB", data)
        data = bool(self.get_DisitckVacuumPindiodeswitchA())
        self.push_change_event("DisitckVacuumPindiodeswitchA", data)
        data = bool(self.get_DisitckVacuumPindiodeswitchB())
        self.push_change_event("DisitckVacuumPindiodeswitchB", data)
        data = bool(self.get_DisitckVacuumFdltrgA())
        self.push_change_event("DisitckVacuumFdltrgA", data)
        data = bool(self.get_DisitckVacuumFdltrgB())
        self.push_change_event("DisitckVacuumFdltrgB", data)
        data = bool(self.get_DisitckVacuumPlctxoffA())
        self.push_change_event("DisitckVacuumPlctxoffA", data)
        data = bool(self.get_DisitckVacuumPlctxoffB())
        self.push_change_event("DisitckVacuumPlctxoffB", data)
        data = bool(self.get_DisitckVacuumMpsA())
        self.push_change_event("DisitckVacuumMpsA", data)
        data = bool(self.get_DisitckVacuumMpsB())
        self.push_change_event("DisitckVacuumMpsB", data)
        data = bool(self.get_DisitckVacuumDiagA())
        self.push_change_event("DisitckVacuumDiagA", data)
        data = bool(self.get_DisitckVacuumDiagB())
        self.push_change_event("DisitckVacuumDiagB", data)
        data = bool(self.get_DisitckManualInterlockDacsoffloopsstbyA())
        self.push_change_event("DisitckManualInterlockDacsoffloopsstbyA", data)
        data = bool(self.get_DisitckManualInterlockDacsoffloopsstbyB())
        self.push_change_event("DisitckManualInterlockDacsoffloopsstbyB", data)
        data = bool(self.get_DisitckManualInterlockPindiodeswitchA())
        self.push_change_event("DisitckManualInterlockPindiodeswitchA", data)
        data = bool(self.get_DisitckManualInterlockPindiodeswitchB())
        self.push_change_event("DisitckManualInterlockPindiodeswitchB", data)
        data = bool(self.get_DisitckManualInterlockFdltrgA())
        self.push_change_event("DisitckManualInterlockFdltrgA", data)
        data = bool(self.get_DisitckManualInterlockFdltrgB())
        self.push_change_event("DisitckManualInterlockFdltrgB", data)
        data = bool(self.get_DisitckManualInterlockPlctxoffA())
        self.push_change_event("DisitckManualInterlockPlctxoffA", data)
        data = bool(self.get_DisitckManualInterlockPlctxoffB())
        self.push_change_event("DisitckManualInterlockPlctxoffB", data)
        data = bool(self.get_DisitckManualInterlockMpsA())
        self.push_change_event("DisitckManualInterlockMpsA", data)
        data = bool(self.get_DisitckManualInterlockMpsB())
        self.push_change_event("DisitckManualInterlockMpsB", data)
        data = bool(self.get_DisitckManualInterlockDiagA())
        self.push_change_event("DisitckManualInterlockDiagA", data)
        data = bool(self.get_DisitckManualInterlockDiagB())
        self.push_change_event("DisitckManualInterlockDiagB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpDacsoffloopsstbyA())
        self.push_change_event("DisitckPlungerEndSwitchesUpDacsoffloopsstbyA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpDacsoffloopsstbyB())
        self.push_change_event("DisitckPlungerEndSwitchesUpDacsoffloopsstbyB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpPindiodeswitchA())
        self.push_change_event("DisitckPlungerEndSwitchesUpPindiodeswitchA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpPindiodeswitchB())
        self.push_change_event("DisitckPlungerEndSwitchesUpPindiodeswitchB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpFdltrgA())
        self.push_change_event("DisitckPlungerEndSwitchesUpFdltrgA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpFdltrgB())
        self.push_change_event("DisitckPlungerEndSwitchesUpFdltrgB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpPlctxoffA())
        self.push_change_event("DisitckPlungerEndSwitchesUpPlctxoffA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpPlctxoffB())
        self.push_change_event("DisitckPlungerEndSwitchesUpPlctxoffB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpMpsA())
        self.push_change_event("DisitckPlungerEndSwitchesUpMpsA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpMpsB())
        self.push_change_event("DisitckPlungerEndSwitchesUpMpsB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpDiagA())
        self.push_change_event("DisitckPlungerEndSwitchesUpDiagA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesUpDiagB())
        self.push_change_event("DisitckPlungerEndSwitchesUpDiagB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownDacsoffloopsstbyA())
        self.push_change_event("DisitckPlungerEndSwitchesDownDacsoffloopsstbyA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownDacsoffloopsstbyB())
        self.push_change_event("DisitckPlungerEndSwitchesDownDacsoffloopsstbyB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownPindiodeswitchA())
        self.push_change_event("DisitckPlungerEndSwitchesDownPindiodeswitchA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownPindiodeswitchB())
        self.push_change_event("DisitckPlungerEndSwitchesDownPindiodeswitchB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownFdltrgA())
        self.push_change_event("DisitckPlungerEndSwitchesDownFdltrgA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownFdltrgB())
        self.push_change_event("DisitckPlungerEndSwitchesDownFdltrgB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownPlctxoffA())
        self.push_change_event("DisitckPlungerEndSwitchesDownPlctxoffA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownPlctxoffB())
        self.push_change_event("DisitckPlungerEndSwitchesDownPlctxoffB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownMpsA())
        self.push_change_event("DisitckPlungerEndSwitchesDownMpsA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownMpsB())
        self.push_change_event("DisitckPlungerEndSwitchesDownMpsB", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownDiagA())
        self.push_change_event("DisitckPlungerEndSwitchesDownDiagA", data)
        data = bool(self.get_DisitckPlungerEndSwitchesDownDiagB())
        self.push_change_event("DisitckPlungerEndSwitchesDownDiagB", data)
        data = bool(self.get_DisitckMpsDacsoffloopsstbyA())
        self.push_change_event("DisitckMpsDacsoffloopsstbyA", data)
        data = bool(self.get_DisitckMpsDacsoffloopsstbyB())
        self.push_change_event("DisitckMpsDacsoffloopsstbyB", data)
        data = bool(self.get_DisitckMpsPindiodeswitchA())
        self.push_change_event("DisitckMpsPindiodeswitchA", data)
        data = bool(self.get_DisitckMpsPindiodeswitchB())
        self.push_change_event("DisitckMpsPindiodeswitchB", data)
        data = bool(self.get_DisitckMpsFdltrgA())
        self.push_change_event("DisitckMpsFdltrgA", data)
        data = bool(self.get_DisitckMpsFdltrgB())
        self.push_change_event("DisitckMpsFdltrgB", data)
        data = bool(self.get_DisitckMpsPlctxoffA())
        self.push_change_event("DisitckMpsPlctxoffA", data)
        data = bool(self.get_DisitckMpsPlctxoffB())
        self.push_change_event("DisitckMpsPlctxoffB", data)
        data = bool(self.get_DisitckMpsMpsA())
        self.push_change_event("DisitckMpsMpsA", data)
        data = bool(self.get_DisitckMpsMpsB())
        self.push_change_event("DisitckMpsMpsB", data)
        data = bool(self.get_DisitckMpsDiagA())
        self.push_change_event("DisitckMpsDiagA", data)
        data = bool(self.get_DisitckMpsDiagB())
        self.push_change_event("DisitckMpsDiagB", data)


    @command
    def init_hardware(self):
        try:
            self.perseus.init_hardware()
            self.set_state(DevState.RUNNING)
        except Exception, e:
            print e
            self.set_state(DevState.FAULT)

    @command
    def tuning_resetA(self):
        perseus_utils.write_direct(self.perseus, True, DIAG_TUNING_RESET_ADDRESS, 'A')
        perseus_utils.write_direct(self.perseus, False, DIAG_TUNING_RESET_ADDRESS, 'A')

    @command
    def reset_manual_itckA(self):
        perseus_utils.write_direct(self.perseus, True, RESET_MANUAL_ITCK_ADDRESS, 'A')
        perseus_utils.write_direct(self.perseus, False, RESET_MANUAL_ITCK_ADDRESS, 'A')

    @command
    def reset_itckA(self):
        perseus_utils.write_direct(self.perseus, True, RESET_ITCK_ADDRESS, 'A')
        perseus_utils.write_direct(self.perseus, False, RESET_ITCK_ADDRESS, 'A')

    @command
    def tuning_resetB(self):
        perseus_utils.write_direct(self.perseus, True, DIAG_TUNING_RESET_ADDRESS, 'B')
        perseus_utils.write_direct(self.perseus, False, DIAG_TUNING_RESET_ADDRESS, 'B')

    @command
    def reset_manual_itckB(self):
        perseus_utils.write_direct(self.perseus, True, RESET_MANUAL_ITCK_ADDRESS, 'B')
        perseus_utils.write_direct(self.perseus, False, RESET_MANUAL_ITCK_ADDRESS, 'B')

    @command
    def reset_itckB(self):
        perseus_utils.write_direct(self.perseus, True, RESET_ITCK_ADDRESS, 'B')
        perseus_utils.write_direct(self.perseus, False, RESET_ITCK_ADDRESS, 'B')

    @command
    def sw_fast_data_logger(self):
        # Ram init ... probably this should be done in init_device
        # but for the moment ...
        self.perseus.init_fast_data_logger()

        # Write delay
        self.perseus.write_fast_data_logger_delay()

        # Start recording data
        self.perseus.start_recording_data_in_ram()

        # Check status of external trigger when HWTrigger
        # Not needed right now

        # Transfer data from loops board RAM to Host PC
        now = datetime.datetime.now()
        filename = now.strftime("{0}/%Y_%m_%d__%H_%M_%S_diags_data.bin").format(self.FDLPath)
        self.perseus.get_ram_data(filename)

        # Check transfer data complete
        while self.perseus.get_transfer_over_register() is not RAM_TRANSFER_OVER:
            time.sleep(0.1) # @warning: super dangerous way of checking it ... who restarts the register?

        # Clear FDL trigger attribute
        # ... but ... HOW?

        # Restart RAM
        self.perseus.init_fast_data_logger()

    def update_fim(self, cavity):
        self.update_RvTet1(cavity)
        self.update_RvTet2(cavity)
        self.update_RvCircIn(cavity)
        self.update_FwLoad(cavity)
        self.update_FwHybLoad(cavity)
        self.update_RvCav(cavity)
        self.update_Arc(cavity)
        self.update_Vacuum(cavity)
        self.update_Manual(cavity)
        self.update_EndSwUp(cavity)
        self.update_EndSwDown(cavity)
        self.update_Mps(cavity)

    def update_RvTet1(self, cavity):
        bit0=getattr(self, "_DisitckRvtet1Dacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckRvtet1Pindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckRvtet1Fdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckRvtet1Plctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckRvtet1Mps%s" % cavity)
        bit5=getattr(self, "_DisitckRvtet1Diag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 7, cavity)

    def update_RvTet2(self, cavity):
        bit0=getattr(self, "_DisitckRvtet2Dacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckRvtet2Pindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckRvtet2Fdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckRvtet2Plctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckRvtet2Mps%s" % cavity)
        bit5=getattr(self, "_DisitckRvtet2Diag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 8, cavity)

    def update_RvCircIn(self, cavity):
        bit0=getattr(self, "_DisitckRvcircDacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckRvcircPindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckRvcircFdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckRvcircPlctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckRvcircMps%s" % cavity)
        bit5=getattr(self, "_DisitckRvcircDiag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 9, cavity)

    def update_FwLoad(self, cavity):
        bit0=getattr(self, "_DisitckFwloadDacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckFwloadPindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckFwloadFdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckFwloadPlctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckFwloadMps%s" % cavity)
        bit5=getattr(self, "_DisitckFwloadDiag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 10, cavity)

    def update_FwHybLoad(self, cavity):
        bit0=getattr(self, "_DisitckFwhybloadDacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckFwhybloadPindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckFwhybloadFdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckFwhybloadPlctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckFwhybloadMps%s" % cavity)
        bit5=getattr(self, "_DisitckFwhybloadDiag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 11, cavity)

    def update_RvCav(self, cavity):
        bit0=getattr(self, "_DisitckRvcavDacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckRvcavPindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckRvcavFdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckRvcavPlctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckRvcavMps%s" % cavity)
        bit5=getattr(self, "_DisitckRvcavDiag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 12, cavity)

    def update_Arc(self, cavity):
        bit0=getattr(self, "_DisitckArcsDacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckArcsPindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckArcsFdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckArcsPlctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckArcsMps%s" % cavity)
        bit5=getattr(self, "_DisitckArcsDiag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 13, cavity)

    def update_Vacuum(self, cavity):
        bit0=getattr(self, "_DisitckVacuumDacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckVacuumPindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckVacuumFdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckVacuumPlctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckVacuumMps%s" % cavity)
        bit5=getattr(self, "_DisitckVacuumDiag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 14, cavity)

    def update_Manual(self, cavity):
        bit0=getattr(self, "_DisitckManualInterlockDacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckManualInterlockPindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckManualInterlockFdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckManualInterlockPlctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckManualInterlockMps%s" % cavity)
        bit5=getattr(self, "_DisitckManualInterlockDiag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 15, cavity)

    def update_EndSwUp(self, cavity):
        bit0=getattr(self, "_DisitckPlungerEndSwitchesUpDacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckPlungerEndSwitchesUpPindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckPlungerEndSwitchesUpFdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckPlungerEndSwitchesUpPlctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckPlungerEndSwitchesUpMps%s" % cavity)
        bit5=getattr(self, "_DisitckPlungerEndSwitchesUpDiag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 16, cavity)

    def update_EndSwDown(self, cavity):
        bit0=getattr(self, "_DisitckPlungerEndSwitchesDownDacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckPlungerEndSwitchesDownPindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckPlungerEndSwitchesDownFdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckPlungerEndSwitchesDownPlctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckPlungerEndSwitchesDownMps%s" % cavity)
        bit5=getattr(self, "_DisitckPlungerEndSwitchesDownDiag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 17, cavity)

    def update_Mps(self, cavity):
        bit0=getattr(self, "_DisitckMpsDacsoffloopsstby%s" % cavity)
        bit1=getattr(self, "_DisitckMpsPindiodeswitch%s" % cavity)
        bit2=getattr(self, "_DisitckMpsFdltrg%s" % cavity)
        bit3=getattr(self, "_DisitckMpsPlctxoff%s" % cavity)
        bit4=getattr(self, "_DisitckMpsMps%s" % cavity)
        bit5=getattr(self, "_DisitckMpsDiag%s" % cavity)
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 18, cavity)

def run_device():
    run([NutaqDiags])

if __name__ == "__main__":
    run_device()
