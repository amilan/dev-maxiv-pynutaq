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
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_Rvtet1A",
                                   fset="set_Rvtet1A",
                                   doc=""
                                   )

    Rvtet1B = attribute(label='Rvtet1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_Rvtet1B",
                                   fset="set_Rvtet1B",
                                   doc=""
                                   )

    Rvtet2A = attribute(label='Rvtet2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_Rvtet2A",
                                   fset="set_Rvtet2A",
                                   doc=""
                                   )

    Rvtet2B = attribute(label='Rvtet2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_Rvtet2B",
                                   fset="set_Rvtet2B",
                                   doc=""
                                   )

    RvcircA = attribute(label='RvcircA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_RvcircA",
                                   fset="set_RvcircA",
                                   doc=""
                                   )

    RvcircB = attribute(label='RvcircB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_RvcircB",
                                   fset="set_RvcircB",
                                   doc=""
                                   )

    FwloadA = attribute(label='FwloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_FwloadA",
                                   fset="set_FwloadA",
                                   doc=""
                                   )

    FwloadB = attribute(label='FwloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_FwloadB",
                                   fset="set_FwloadB",
                                   doc=""
                                   )

    FwhybloadA = attribute(label='FwhybloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_FwhybloadA",
                                   fset="set_FwhybloadA",
                                   doc=""
                                   )

    FwhybloadB = attribute(label='FwhybloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_FwhybloadB",
                                   fset="set_FwhybloadB",
                                   doc=""
                                   )

    RvcavA = attribute(label='RvcavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_RvcavA",
                                   fset="set_RvcavA",
                                   doc=""
                                   )

    RvcavB = attribute(label='RvcavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_RvcavB",
                                   fset="set_RvcavB",
                                   doc=""
                                   )

    ManualInterlockA = attribute(label='ManualInterlockA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_ManualInterlockA",
                                   fset="set_ManualInterlockA",
                                   doc=""
                                   )

    ManualInterlockB = attribute(label='ManualInterlockB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_ManualInterlockB",
                                   fset="set_ManualInterlockB",
                                   doc=""
                                   )

    DisableItckRvtet1A = attribute(label='DisableItckRvtet1A',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvtet1A",
                                   fset="set_DisableItckRvtet1A",
                                   doc=""
                                   )

    DisableItckRvtet1B = attribute(label='DisableItckRvtet1B',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvtet1B",
                                   fset="set_DisableItckRvtet1B",
                                   doc=""
                                   )

    DisableItckRvtet2A = attribute(label='DisableItckRvtet2A',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvtet2A",
                                   fset="set_DisableItckRvtet2A",
                                   doc=""
                                   )

    DisableItckRvtet2B = attribute(label='DisableItckRvtet2B',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvtet2B",
                                   fset="set_DisableItckRvtet2B",
                                   doc=""
                                   )

    DisableItckRvcircA = attribute(label='DisableItckRvcircA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvcircA",
                                   fset="set_DisableItckRvcircA",
                                   doc=""
                                   )

    DisableItckRvcircB = attribute(label='DisableItckRvcircB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvcircB",
                                   fset="set_DisableItckRvcircB",
                                   doc=""
                                   )

    DisableItckFwloadA = attribute(label='DisableItckFwloadA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckFwloadA",
                                   fset="set_DisableItckFwloadA",
                                   doc=""
                                   )

    DisableItckFwloadB = attribute(label='DisableItckFwloadB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckFwloadB",
                                   fset="set_DisableItckFwloadB",
                                   doc=""
                                   )

    DisableItckFwhybloadA = attribute(label='DisableItckFwhybloadA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckFwhybloadA",
                                   fset="set_DisableItckFwhybloadA",
                                   doc=""
                                   )

    DisableItckFwhybloadB = attribute(label='DisableItckFwhybloadB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckFwhybloadB",
                                   fset="set_DisableItckFwhybloadB",
                                   doc=""
                                   )

    DisableItckRvcavA = attribute(label='DisableItckRvcavA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvcavA",
                                   fset="set_DisableItckRvcavA",
                                   doc=""
                                   )

    DisableItckRvcavB = attribute(label='DisableItckRvcavB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvcavB",
                                   fset="set_DisableItckRvcavB",
                                   doc=""
                                   )

    DisableItckArcsA = attribute(label='DisableItckArcsA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckArcsA",
                                   fset="set_DisableItckArcsA",
                                   doc=""
                                   )

    DisableItckArcsB = attribute(label='DisableItckArcsB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckArcsB",
                                   fset="set_DisableItckArcsB",
                                   doc=""
                                   )

    DisableItckVaccumA = attribute(label='DisableItckVaccumA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckVaccumA",
                                   fset="set_DisableItckVaccumA",
                                   doc=""
                                   )

    DisableItckVaccumB = attribute(label='DisableItckVaccumB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckVaccumB",
                                   fset="set_DisableItckVaccumB",
                                   doc=""
                                   )

    DisableItckManualInterlockA = attribute(label='DisableItckManualInterlockA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckManualInterlockA",
                                   fset="set_DisableItckManualInterlockA",
                                   doc=""
                                   )

    DisableItckManualInterlockB = attribute(label='DisableItckManualInterlockB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckManualInterlockB",
                                   fset="set_DisableItckManualInterlockB",
                                   doc=""
                                   )

    DisableItckPlungerEndSwitchesUpA = attribute(label='DisableItckPlungerEndSwitchesUpA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckPlungerEndSwitchesUpA",
                                   fset="set_DisableItckPlungerEndSwitchesUpA",
                                   doc=""
                                   )

    DisableItckPlungerEndSwitchesUpB = attribute(label='DisableItckPlungerEndSwitchesUpB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckPlungerEndSwitchesUpB",
                                   fset="set_DisableItckPlungerEndSwitchesUpB",
                                   doc=""
                                   )

    DisableItckPlungerEndSwitchesDownA = attribute(label='DisableItckPlungerEndSwitchesDownA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckPlungerEndSwitchesDownA",
                                   fset="set_DisableItckPlungerEndSwitchesDownA",
                                   doc=""
                                   )

    DisableItckPlungerEndSwitchesDownB = attribute(label='DisableItckPlungerEndSwitchesDownB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckPlungerEndSwitchesDownB",
                                   fset="set_DisableItckPlungerEndSwitchesDownB",
                                   doc=""
                                   )

    DisableItckMpsA = attribute(label='DisableItckMpsA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckMpsA",
                                   fset="set_DisableItckMpsA",
                                   doc=""
                                   )

    DisableItckMpsB = attribute(label='DisableItckMpsB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckMpsB",
                                   fset="set_DisableItckMpsB",
                                   doc=""
                                   )

    SamplesToAverageA = attribute(label='SamplesToAverageA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   fget="get_SamplesToAverageA",
                                   fset="set_SamplesToAverageA",
                                   doc=""
                                   )

    SamplesToAverageB = attribute(label='SamplesToAverageB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   fget="get_SamplesToAverageB",
                                   fset="set_SamplesToAverageB",
                                   doc=""
                                   )

    PulseupLogicInversionA = attribute(label='PulseupLogicInversionA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_PulseupLogicInversionA",
                                   fset="set_PulseupLogicInversionA",
                                   doc=""
                                   )

    PulseupLogicInversionB = attribute(label='PulseupLogicInversionB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_PulseupLogicInversionB",
                                   fset="set_PulseupLogicInversionB",
                                   doc=""
                                   )

    EndSwitchesConnectedToNoNcContactA = attribute(label='EndSwitchesConnectedToNoNcContactA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=1,
                                   fget="get_EndSwitchesConnectedToNoNcContactA",
                                   fset="set_EndSwitchesConnectedToNoNcContactA",
                                   doc=""
                                   )

    EndSwitchesConnectedToNoNcContactB = attribute(label='EndSwitchesConnectedToNoNcContactB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=1,
                                   fget="get_EndSwitchesConnectedToNoNcContactB",
                                   fset="set_EndSwitchesConnectedToNoNcContactB",
                                   doc=""
                                   )

    LookrefA = attribute(label='LookrefA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_LookrefA",
                                   fset="set_LookrefA",
                                   doc=""
                                   )

    LookrefB = attribute(label='LookrefB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_LookrefB",
                                   fset="set_LookrefB",
                                   doc=""
                                   )

    QuadrefA = attribute(label='QuadrefA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   fget="get_QuadrefA",
                                   fset="set_QuadrefA",
                                   doc=""
                                   )

    QuadrefB = attribute(label='QuadrefB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   fget="get_QuadrefB",
                                   fset="set_QuadrefB",
                                   doc=""
                                   )

    SpareDo1A = attribute(label='SpareDo1A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_SpareDo1A",
                                   fset="set_SpareDo1A",
                                   doc=""
                                   )

    SpareDo1B = attribute(label='SpareDo1B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_SpareDo1B",
                                   fset="set_SpareDo1B",
                                   doc=""
                                   )

    SpareDo2A = attribute(label='SpareDo2A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_SpareDo2A",
                                   fset="set_SpareDo2A",
                                   doc=""
                                   )

    SpareDo2B = attribute(label='SpareDo2B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_SpareDo2B",
                                   fset="set_SpareDo2B",
                                   doc=""
                                   )

    SpareDo3A = attribute(label='SpareDo3A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_SpareDo3A",
                                   fset="set_SpareDo3A",
                                   doc=""
                                   )

    SpareDo3B = attribute(label='SpareDo3B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_SpareDo3B",
                                   fset="set_SpareDo3B",
                                   doc=""
                                   )

    FdlSwTriggerA = attribute(label='FdlSwTriggerA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_FdlSwTriggerA",
                                   fset="set_FdlSwTriggerA",
                                   doc=""
                                   )

    FdlSwTriggerB = attribute(label='FdlSwTriggerB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_FdlSwTriggerB",
                                   fset="set_FdlSwTriggerB",
                                   doc=""
                                   )

    ResetInterlocksCavA = attribute(label='ResetInterlocksCavA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_ResetInterlocksCavA",
                                   fset="set_ResetInterlocksCavA",
                                   doc=""
                                   )

    ResetInterlocksCavB = attribute(label='ResetInterlocksCavB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_ResetInterlocksCavB",
                                   fset="set_ResetInterlocksCavB",
                                   doc=""
                                   )

    LandautuningenableA = attribute(label='LandautuningenableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_LandautuningenableA",
                                   fset="set_LandautuningenableA",
                                   doc=""
                                   )

    LandautuningenableB = attribute(label='LandautuningenableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_LandautuningenableB",
                                   fset="set_LandautuningenableB",
                                   doc=""
                                   )

    LandautuningresetA = attribute(label='LandautuningresetA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_LandautuningresetA",
                                   fset="set_LandautuningresetA",
                                   doc=""
                                   )

    LandautuningresetB = attribute(label='LandautuningresetB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_LandautuningresetB",
                                   fset="set_LandautuningresetB",
                                   doc=""
                                   )

    MovelandauupA = attribute(label='MovelandauupA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_MovelandauupA",
                                   fset="set_MovelandauupA",
                                   doc=""
                                   )

    MovelandauupB = attribute(label='MovelandauupB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_MovelandauupB",
                                   fset="set_MovelandauupB",
                                   doc=""
                                   )

    MovelandauplgA = attribute(label='MovelandauplgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_MovelandauplgA",
                                   fset="set_MovelandauplgA",
                                   doc=""
                                   )

    MovelandauplgB = attribute(label='MovelandauplgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_MovelandauplgB",
                                   fset="set_MovelandauplgB",
                                   doc=""
                                   )

    NumstepsA = attribute(label='NumstepsA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=10000,
                                   fget="get_NumstepsA",
                                   fset="set_NumstepsA",
                                   doc=""
                                   )

    NumstepsB = attribute(label='NumstepsB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=10000,
                                   fget="get_NumstepsB",
                                   fset="set_NumstepsB",
                                   doc=""
                                   )

    LandauphaseoffsetA = attribute(label='LandauphaseoffsetA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=180,
                                   fget="get_LandauphaseoffsetA",
                                   fset="set_LandauphaseoffsetA",
                                   doc=""
                                   )

    LandauphaseoffsetB = attribute(label='LandauphaseoffsetB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=180,
                                   fget="get_LandauphaseoffsetB",
                                   fset="set_LandauphaseoffsetB",
                                   doc=""
                                   )

    LandaumarginupA = attribute(label='LandaumarginupA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=50,
                                   fget="get_LandaumarginupA",
                                   fset="set_LandaumarginupA",
                                   doc=""
                                   )

    LandaumarginupB = attribute(label='LandaumarginupB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=50,
                                   fget="get_LandaumarginupB",
                                   fset="set_LandaumarginupB",
                                   doc=""
                                   )

    LandauMarginLowA = attribute(label='LandauMarginLowA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=10,
                                   fget="get_LandauMarginLowA",
                                   fset="set_LandauMarginLowA",
                                   doc=""
                                   )

    LandauMarginLowB = attribute(label='LandauMarginLowB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=10,
                                   fget="get_LandauMarginLowB",
                                   fset="set_LandauMarginLowB",
                                   doc=""
                                   )

    MinimumLandauAmplitudeA = attribute(label='MinimumLandauAmplitudeA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_MinimumLandauAmplitudeA",
                                   fset="set_MinimumLandauAmplitudeA",
                                   doc=""
                                   )

    MinimumLandauAmplitudeB = attribute(label='MinimumLandauAmplitudeB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_MinimumLandauAmplitudeB",
                                   fset="set_MinimumLandauAmplitudeB",
                                   doc=""
                                   )

    LandauPositiveEnableA = attribute(label='LandauPositiveEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_LandauPositiveEnableA",
                                   fset="set_LandauPositiveEnableA",
                                   doc=""
                                   )

    LandauPositiveEnableB = attribute(label='LandauPositiveEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_LandauPositiveEnableB",
                                   fset="set_LandauPositiveEnableB",
                                   doc=""
                                   )

    LandauampsettingA = attribute(label='LandauampsettingA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_LandauampsettingA",
                                   fset="set_LandauampsettingA",
                                   doc=""
                                   )

    LandauampsettingB = attribute(label='LandauampsettingB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_LandauampsettingB",
                                   fset="set_LandauampsettingB",
                                   doc=""
                                   )

    DisitckRvtet1DacsoffloopsstbyA = attribute(label='DisitckRvtet1DacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1DacsoffloopsstbyA",
                                   fset="set_DisitckRvtet1DacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckRvtet1DacsoffloopsstbyB = attribute(label='DisitckRvtet1DacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1DacsoffloopsstbyB",
                                   fset="set_DisitckRvtet1DacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckRvtet1PindiodeswitchA = attribute(label='DisitckRvtet1PindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1PindiodeswitchA",
                                   fset="set_DisitckRvtet1PindiodeswitchA",
                                   doc=""
                                   )

    DisitckRvtet1PindiodeswitchB = attribute(label='DisitckRvtet1PindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1PindiodeswitchB",
                                   fset="set_DisitckRvtet1PindiodeswitchB",
                                   doc=""
                                   )

    DisitckRvtet1FdltrgA = attribute(label='DisitckRvtet1FdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1FdltrgA",
                                   fset="set_DisitckRvtet1FdltrgA",
                                   doc=""
                                   )

    DisitckRvtet1FdltrgB = attribute(label='DisitckRvtet1FdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1FdltrgB",
                                   fset="set_DisitckRvtet1FdltrgB",
                                   doc=""
                                   )

    DisitckRvtet1PlctxoffA = attribute(label='DisitckRvtet1PlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1PlctxoffA",
                                   fset="set_DisitckRvtet1PlctxoffA",
                                   doc=""
                                   )

    DisitckRvtet1PlctxoffB = attribute(label='DisitckRvtet1PlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1PlctxoffB",
                                   fset="set_DisitckRvtet1PlctxoffB",
                                   doc=""
                                   )

    DisitckRvtet1MpsA = attribute(label='DisitckRvtet1MpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1MpsA",
                                   fset="set_DisitckRvtet1MpsA",
                                   doc=""
                                   )

    DisitckRvtet1MpsB = attribute(label='DisitckRvtet1MpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1MpsB",
                                   fset="set_DisitckRvtet1MpsB",
                                   doc=""
                                   )

    DisitckRvtet1DiagA = attribute(label='DisitckRvtet1DiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1DiagA",
                                   fset="set_DisitckRvtet1DiagA",
                                   doc=""
                                   )

    DisitckRvtet1DiagB = attribute(label='DisitckRvtet1DiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1DiagB",
                                   fset="set_DisitckRvtet1DiagB",
                                   doc=""
                                   )

    DisitckRvtet2DacsoffloopsstbyA = attribute(label='DisitckRvtet2DacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2DacsoffloopsstbyA",
                                   fset="set_DisitckRvtet2DacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckRvtet2DacsoffloopsstbyB = attribute(label='DisitckRvtet2DacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2DacsoffloopsstbyB",
                                   fset="set_DisitckRvtet2DacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckRvtet2PindiodeswitchA = attribute(label='DisitckRvtet2PindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2PindiodeswitchA",
                                   fset="set_DisitckRvtet2PindiodeswitchA",
                                   doc=""
                                   )

    DisitckRvtet2PindiodeswitchB = attribute(label='DisitckRvtet2PindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2PindiodeswitchB",
                                   fset="set_DisitckRvtet2PindiodeswitchB",
                                   doc=""
                                   )

    DisitckRvtet2FdltrgA = attribute(label='DisitckRvtet2FdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2FdltrgA",
                                   fset="set_DisitckRvtet2FdltrgA",
                                   doc=""
                                   )

    DisitckRvtet2FdltrgB = attribute(label='DisitckRvtet2FdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2FdltrgB",
                                   fset="set_DisitckRvtet2FdltrgB",
                                   doc=""
                                   )

    DisitckRvtet2PlctxoffA = attribute(label='DisitckRvtet2PlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2PlctxoffA",
                                   fset="set_DisitckRvtet2PlctxoffA",
                                   doc=""
                                   )

    DisitckRvtet2PlctxoffB = attribute(label='DisitckRvtet2PlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2PlctxoffB",
                                   fset="set_DisitckRvtet2PlctxoffB",
                                   doc=""
                                   )

    DisitckRvtet2MpsA = attribute(label='DisitckRvtet2MpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2MpsA",
                                   fset="set_DisitckRvtet2MpsA",
                                   doc=""
                                   )

    DisitckRvtet2MpsB = attribute(label='DisitckRvtet2MpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2MpsB",
                                   fset="set_DisitckRvtet2MpsB",
                                   doc=""
                                   )

    DisitckRvtet2DiagA = attribute(label='DisitckRvtet2DiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2DiagA",
                                   fset="set_DisitckRvtet2DiagA",
                                   doc=""
                                   )

    DisitckRvtet2DiagB = attribute(label='DisitckRvtet2DiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2DiagB",
                                   fset="set_DisitckRvtet2DiagB",
                                   doc=""
                                   )

    DisitckRvcircDacsoffloopsstbyA = attribute(label='DisitckRvcircDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircDacsoffloopsstbyA",
                                   fset="set_DisitckRvcircDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckRvcircDacsoffloopsstbyB = attribute(label='DisitckRvcircDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircDacsoffloopsstbyB",
                                   fset="set_DisitckRvcircDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckRvcircPindiodeswitchA = attribute(label='DisitckRvcircPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircPindiodeswitchA",
                                   fset="set_DisitckRvcircPindiodeswitchA",
                                   doc=""
                                   )

    DisitckRvcircPindiodeswitchB = attribute(label='DisitckRvcircPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircPindiodeswitchB",
                                   fset="set_DisitckRvcircPindiodeswitchB",
                                   doc=""
                                   )

    DisitckRvcircFdltrgA = attribute(label='DisitckRvcircFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircFdltrgA",
                                   fset="set_DisitckRvcircFdltrgA",
                                   doc=""
                                   )

    DisitckRvcircFdltrgB = attribute(label='DisitckRvcircFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircFdltrgB",
                                   fset="set_DisitckRvcircFdltrgB",
                                   doc=""
                                   )

    DisitckRvcircPlctxoffA = attribute(label='DisitckRvcircPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircPlctxoffA",
                                   fset="set_DisitckRvcircPlctxoffA",
                                   doc=""
                                   )

    DisitckRvcircPlctxoffB = attribute(label='DisitckRvcircPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircPlctxoffB",
                                   fset="set_DisitckRvcircPlctxoffB",
                                   doc=""
                                   )

    DisitckRvcircMpsA = attribute(label='DisitckRvcircMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircMpsA",
                                   fset="set_DisitckRvcircMpsA",
                                   doc=""
                                   )

    DisitckRvcircMpsB = attribute(label='DisitckRvcircMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircMpsB",
                                   fset="set_DisitckRvcircMpsB",
                                   doc=""
                                   )

    DisitckRvcircDiagA = attribute(label='DisitckRvcircDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircDiagA",
                                   fset="set_DisitckRvcircDiagA",
                                   doc=""
                                   )

    DisitckRvcircDiagB = attribute(label='DisitckRvcircDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircDiagB",
                                   fset="set_DisitckRvcircDiagB",
                                   doc=""
                                   )

    DisitckFwloadDacsoffloopsstbyA = attribute(label='DisitckFwloadDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadDacsoffloopsstbyA",
                                   fset="set_DisitckFwloadDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckFwloadDacsoffloopsstbyB = attribute(label='DisitckFwloadDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadDacsoffloopsstbyB",
                                   fset="set_DisitckFwloadDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckFwloadPindiodeswitchA = attribute(label='DisitckFwloadPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadPindiodeswitchA",
                                   fset="set_DisitckFwloadPindiodeswitchA",
                                   doc=""
                                   )

    DisitckFwloadPindiodeswitchB = attribute(label='DisitckFwloadPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadPindiodeswitchB",
                                   fset="set_DisitckFwloadPindiodeswitchB",
                                   doc=""
                                   )

    DisitckFwloadFdltrgA = attribute(label='DisitckFwloadFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadFdltrgA",
                                   fset="set_DisitckFwloadFdltrgA",
                                   doc=""
                                   )

    DisitckFwloadFdltrgB = attribute(label='DisitckFwloadFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadFdltrgB",
                                   fset="set_DisitckFwloadFdltrgB",
                                   doc=""
                                   )

    DisitckFwloadPlctxoffA = attribute(label='DisitckFwloadPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadPlctxoffA",
                                   fset="set_DisitckFwloadPlctxoffA",
                                   doc=""
                                   )

    DisitckFwloadPlctxoffB = attribute(label='DisitckFwloadPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadPlctxoffB",
                                   fset="set_DisitckFwloadPlctxoffB",
                                   doc=""
                                   )

    DisitckFwloadMpsA = attribute(label='DisitckFwloadMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadMpsA",
                                   fset="set_DisitckFwloadMpsA",
                                   doc=""
                                   )

    DisitckFwloadMpsB = attribute(label='DisitckFwloadMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadMpsB",
                                   fset="set_DisitckFwloadMpsB",
                                   doc=""
                                   )

    DisitckFwloadDiagA = attribute(label='DisitckFwloadDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadDiagA",
                                   fset="set_DisitckFwloadDiagA",
                                   doc=""
                                   )

    DisitckFwloadDiagB = attribute(label='DisitckFwloadDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadDiagB",
                                   fset="set_DisitckFwloadDiagB",
                                   doc=""
                                   )

    DisitckFwhybloadDacsoffloopsstbyA = attribute(label='DisitckFwhybloadDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadDacsoffloopsstbyA",
                                   fset="set_DisitckFwhybloadDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckFwhybloadDacsoffloopsstbyB = attribute(label='DisitckFwhybloadDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadDacsoffloopsstbyB",
                                   fset="set_DisitckFwhybloadDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckFwhybloadPindiodeswitchA = attribute(label='DisitckFwhybloadPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadPindiodeswitchA",
                                   fset="set_DisitckFwhybloadPindiodeswitchA",
                                   doc=""
                                   )

    DisitckFwhybloadPindiodeswitchB = attribute(label='DisitckFwhybloadPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadPindiodeswitchB",
                                   fset="set_DisitckFwhybloadPindiodeswitchB",
                                   doc=""
                                   )

    DisitckFwhybloadFdltrgA = attribute(label='DisitckFwhybloadFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadFdltrgA",
                                   fset="set_DisitckFwhybloadFdltrgA",
                                   doc=""
                                   )

    DisitckFwhybloadFdltrgB = attribute(label='DisitckFwhybloadFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadFdltrgB",
                                   fset="set_DisitckFwhybloadFdltrgB",
                                   doc=""
                                   )

    DisitckFwhybloadPlctxoffA = attribute(label='DisitckFwhybloadPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadPlctxoffA",
                                   fset="set_DisitckFwhybloadPlctxoffA",
                                   doc=""
                                   )

    DisitckFwhybloadPlctxoffB = attribute(label='DisitckFwhybloadPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadPlctxoffB",
                                   fset="set_DisitckFwhybloadPlctxoffB",
                                   doc=""
                                   )

    DisitckFwhybloadMpsA = attribute(label='DisitckFwhybloadMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadMpsA",
                                   fset="set_DisitckFwhybloadMpsA",
                                   doc=""
                                   )

    DisitckFwhybloadMpsB = attribute(label='DisitckFwhybloadMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadMpsB",
                                   fset="set_DisitckFwhybloadMpsB",
                                   doc=""
                                   )

    DisitckFwhybloadDiagA = attribute(label='DisitckFwhybloadDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadDiagA",
                                   fset="set_DisitckFwhybloadDiagA",
                                   doc=""
                                   )

    DisitckFwhybloadDiagB = attribute(label='DisitckFwhybloadDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadDiagB",
                                   fset="set_DisitckFwhybloadDiagB",
                                   doc=""
                                   )

    DisitckRvcavDacsoffloopsstbyA = attribute(label='DisitckRvcavDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavDacsoffloopsstbyA",
                                   fset="set_DisitckRvcavDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckRvcavDacsoffloopsstbyB = attribute(label='DisitckRvcavDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavDacsoffloopsstbyB",
                                   fset="set_DisitckRvcavDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckRvcavPindiodeswitchA = attribute(label='DisitckRvcavPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavPindiodeswitchA",
                                   fset="set_DisitckRvcavPindiodeswitchA",
                                   doc=""
                                   )

    DisitckRvcavPindiodeswitchB = attribute(label='DisitckRvcavPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavPindiodeswitchB",
                                   fset="set_DisitckRvcavPindiodeswitchB",
                                   doc=""
                                   )

    DisitckRvcavFdltrgA = attribute(label='DisitckRvcavFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavFdltrgA",
                                   fset="set_DisitckRvcavFdltrgA",
                                   doc=""
                                   )

    DisitckRvcavFdltrgB = attribute(label='DisitckRvcavFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavFdltrgB",
                                   fset="set_DisitckRvcavFdltrgB",
                                   doc=""
                                   )

    DisitckRvcavPlctxoffA = attribute(label='DisitckRvcavPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavPlctxoffA",
                                   fset="set_DisitckRvcavPlctxoffA",
                                   doc=""
                                   )

    DisitckRvcavPlctxoffB = attribute(label='DisitckRvcavPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavPlctxoffB",
                                   fset="set_DisitckRvcavPlctxoffB",
                                   doc=""
                                   )

    DisitckRvcavMpsA = attribute(label='DisitckRvcavMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavMpsA",
                                   fset="set_DisitckRvcavMpsA",
                                   doc=""
                                   )

    DisitckRvcavMpsB = attribute(label='DisitckRvcavMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavMpsB",
                                   fset="set_DisitckRvcavMpsB",
                                   doc=""
                                   )

    DisitckRvcavDiagA = attribute(label='DisitckRvcavDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavDiagA",
                                   fset="set_DisitckRvcavDiagA",
                                   doc=""
                                   )

    DisitckRvcavDiagB = attribute(label='DisitckRvcavDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavDiagB",
                                   fset="set_DisitckRvcavDiagB",
                                   doc=""
                                   )

    DisitckArcsDacsoffloopsstbyA = attribute(label='DisitckArcsDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsDacsoffloopsstbyA",
                                   fset="set_DisitckArcsDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckArcsDacsoffloopsstbyB = attribute(label='DisitckArcsDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsDacsoffloopsstbyB",
                                   fset="set_DisitckArcsDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckArcsPindiodeswitchA = attribute(label='DisitckArcsPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsPindiodeswitchA",
                                   fset="set_DisitckArcsPindiodeswitchA",
                                   doc=""
                                   )

    DisitckArcsPindiodeswitchB = attribute(label='DisitckArcsPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsPindiodeswitchB",
                                   fset="set_DisitckArcsPindiodeswitchB",
                                   doc=""
                                   )

    DisitckArcsFdltrgA = attribute(label='DisitckArcsFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsFdltrgA",
                                   fset="set_DisitckArcsFdltrgA",
                                   doc=""
                                   )

    DisitckArcsFdltrgB = attribute(label='DisitckArcsFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsFdltrgB",
                                   fset="set_DisitckArcsFdltrgB",
                                   doc=""
                                   )

    DisitckArcsPlctxoffA = attribute(label='DisitckArcsPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsPlctxoffA",
                                   fset="set_DisitckArcsPlctxoffA",
                                   doc=""
                                   )

    DisitckArcsPlctxoffB = attribute(label='DisitckArcsPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsPlctxoffB",
                                   fset="set_DisitckArcsPlctxoffB",
                                   doc=""
                                   )

    DisitckArcsMpsA = attribute(label='DisitckArcsMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsMpsA",
                                   fset="set_DisitckArcsMpsA",
                                   doc=""
                                   )

    DisitckArcsMpsB = attribute(label='DisitckArcsMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsMpsB",
                                   fset="set_DisitckArcsMpsB",
                                   doc=""
                                   )

    DisitckArcsDiagA = attribute(label='DisitckArcsDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsDiagA",
                                   fset="set_DisitckArcsDiagA",
                                   doc=""
                                   )

    DisitckArcsDiagB = attribute(label='DisitckArcsDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsDiagB",
                                   fset="set_DisitckArcsDiagB",
                                   doc=""
                                   )

    DisitckVacuumDacsoffloopsstbyA = attribute(label='DisitckVacuumDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumDacsoffloopsstbyA",
                                   fset="set_DisitckVacuumDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckVacuumDacsoffloopsstbyB = attribute(label='DisitckVacuumDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumDacsoffloopsstbyB",
                                   fset="set_DisitckVacuumDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckVacuumPindiodeswitchA = attribute(label='DisitckVacuumPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumPindiodeswitchA",
                                   fset="set_DisitckVacuumPindiodeswitchA",
                                   doc=""
                                   )

    DisitckVacuumPindiodeswitchB = attribute(label='DisitckVacuumPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumPindiodeswitchB",
                                   fset="set_DisitckVacuumPindiodeswitchB",
                                   doc=""
                                   )

    DisitckVacuumFdltrgA = attribute(label='DisitckVacuumFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumFdltrgA",
                                   fset="set_DisitckVacuumFdltrgA",
                                   doc=""
                                   )

    DisitckVacuumFdltrgB = attribute(label='DisitckVacuumFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumFdltrgB",
                                   fset="set_DisitckVacuumFdltrgB",
                                   doc=""
                                   )

    DisitckVacuumPlctxoffA = attribute(label='DisitckVacuumPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumPlctxoffA",
                                   fset="set_DisitckVacuumPlctxoffA",
                                   doc=""
                                   )

    DisitckVacuumPlctxoffB = attribute(label='DisitckVacuumPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumPlctxoffB",
                                   fset="set_DisitckVacuumPlctxoffB",
                                   doc=""
                                   )

    DisitckVacuumMpsA = attribute(label='DisitckVacuumMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumMpsA",
                                   fset="set_DisitckVacuumMpsA",
                                   doc=""
                                   )

    DisitckVacuumMpsB = attribute(label='DisitckVacuumMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumMpsB",
                                   fset="set_DisitckVacuumMpsB",
                                   doc=""
                                   )

    DisitckVacuumDiagA = attribute(label='DisitckVacuumDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumDiagA",
                                   fset="set_DisitckVacuumDiagA",
                                   doc=""
                                   )

    DisitckVacuumDiagB = attribute(label='DisitckVacuumDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumDiagB",
                                   fset="set_DisitckVacuumDiagB",
                                   doc=""
                                   )

    DisitckManualInterlockDacsoffloopsstbyA = attribute(label='DisitckManualInterlockDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockDacsoffloopsstbyA",
                                   fset="set_DisitckManualInterlockDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckManualInterlockDacsoffloopsstbyB = attribute(label='DisitckManualInterlockDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockDacsoffloopsstbyB",
                                   fset="set_DisitckManualInterlockDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckManualInterlockPindiodeswitchA = attribute(label='DisitckManualInterlockPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockPindiodeswitchA",
                                   fset="set_DisitckManualInterlockPindiodeswitchA",
                                   doc=""
                                   )

    DisitckManualInterlockPindiodeswitchB = attribute(label='DisitckManualInterlockPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockPindiodeswitchB",
                                   fset="set_DisitckManualInterlockPindiodeswitchB",
                                   doc=""
                                   )

    DisitckManualInterlockFdltrgA = attribute(label='DisitckManualInterlockFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockFdltrgA",
                                   fset="set_DisitckManualInterlockFdltrgA",
                                   doc=""
                                   )

    DisitckManualInterlockFdltrgB = attribute(label='DisitckManualInterlockFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockFdltrgB",
                                   fset="set_DisitckManualInterlockFdltrgB",
                                   doc=""
                                   )

    DisitckManualInterlockPlctxoffA = attribute(label='DisitckManualInterlockPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockPlctxoffA",
                                   fset="set_DisitckManualInterlockPlctxoffA",
                                   doc=""
                                   )

    DisitckManualInterlockPlctxoffB = attribute(label='DisitckManualInterlockPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockPlctxoffB",
                                   fset="set_DisitckManualInterlockPlctxoffB",
                                   doc=""
                                   )

    DisitckManualInterlockMpsA = attribute(label='DisitckManualInterlockMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockMpsA",
                                   fset="set_DisitckManualInterlockMpsA",
                                   doc=""
                                   )

    DisitckManualInterlockMpsB = attribute(label='DisitckManualInterlockMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockMpsB",
                                   fset="set_DisitckManualInterlockMpsB",
                                   doc=""
                                   )

    DisitckManualInterlockDiagA = attribute(label='DisitckManualInterlockDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockDiagA",
                                   fset="set_DisitckManualInterlockDiagA",
                                   doc=""
                                   )

    DisitckManualInterlockDiagB = attribute(label='DisitckManualInterlockDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockDiagB",
                                   fset="set_DisitckManualInterlockDiagB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpDacsoffloopsstbyA = attribute(label='DisitckPlungerEndSwitchesUpDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpDacsoffloopsstbyA",
                                   fset="set_DisitckPlungerEndSwitchesUpDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpDacsoffloopsstbyB = attribute(label='DisitckPlungerEndSwitchesUpDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpDacsoffloopsstbyB",
                                   fset="set_DisitckPlungerEndSwitchesUpDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpPindiodeswitchA = attribute(label='DisitckPlungerEndSwitchesUpPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpPindiodeswitchA",
                                   fset="set_DisitckPlungerEndSwitchesUpPindiodeswitchA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpPindiodeswitchB = attribute(label='DisitckPlungerEndSwitchesUpPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpPindiodeswitchB",
                                   fset="set_DisitckPlungerEndSwitchesUpPindiodeswitchB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpFdltrgA = attribute(label='DisitckPlungerEndSwitchesUpFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpFdltrgA",
                                   fset="set_DisitckPlungerEndSwitchesUpFdltrgA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpFdltrgB = attribute(label='DisitckPlungerEndSwitchesUpFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpFdltrgB",
                                   fset="set_DisitckPlungerEndSwitchesUpFdltrgB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpPlctxoffA = attribute(label='DisitckPlungerEndSwitchesUpPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpPlctxoffA",
                                   fset="set_DisitckPlungerEndSwitchesUpPlctxoffA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpPlctxoffB = attribute(label='DisitckPlungerEndSwitchesUpPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpPlctxoffB",
                                   fset="set_DisitckPlungerEndSwitchesUpPlctxoffB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpMpsA = attribute(label='DisitckPlungerEndSwitchesUpMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpMpsA",
                                   fset="set_DisitckPlungerEndSwitchesUpMpsA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpMpsB = attribute(label='DisitckPlungerEndSwitchesUpMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpMpsB",
                                   fset="set_DisitckPlungerEndSwitchesUpMpsB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpDiagA = attribute(label='DisitckPlungerEndSwitchesUpDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpDiagA",
                                   fset="set_DisitckPlungerEndSwitchesUpDiagA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpDiagB = attribute(label='DisitckPlungerEndSwitchesUpDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpDiagB",
                                   fset="set_DisitckPlungerEndSwitchesUpDiagB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownDacsoffloopsstbyA = attribute(label='DisitckPlungerEndSwitchesDownDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownDacsoffloopsstbyA",
                                   fset="set_DisitckPlungerEndSwitchesDownDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownDacsoffloopsstbyB = attribute(label='DisitckPlungerEndSwitchesDownDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownDacsoffloopsstbyB",
                                   fset="set_DisitckPlungerEndSwitchesDownDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownPindiodeswitchA = attribute(label='DisitckPlungerEndSwitchesDownPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownPindiodeswitchA",
                                   fset="set_DisitckPlungerEndSwitchesDownPindiodeswitchA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownPindiodeswitchB = attribute(label='DisitckPlungerEndSwitchesDownPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownPindiodeswitchB",
                                   fset="set_DisitckPlungerEndSwitchesDownPindiodeswitchB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownFdltrgA = attribute(label='DisitckPlungerEndSwitchesDownFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownFdltrgA",
                                   fset="set_DisitckPlungerEndSwitchesDownFdltrgA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownFdltrgB = attribute(label='DisitckPlungerEndSwitchesDownFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownFdltrgB",
                                   fset="set_DisitckPlungerEndSwitchesDownFdltrgB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownPlctxoffA = attribute(label='DisitckPlungerEndSwitchesDownPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownPlctxoffA",
                                   fset="set_DisitckPlungerEndSwitchesDownPlctxoffA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownPlctxoffB = attribute(label='DisitckPlungerEndSwitchesDownPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownPlctxoffB",
                                   fset="set_DisitckPlungerEndSwitchesDownPlctxoffB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownMpsA = attribute(label='DisitckPlungerEndSwitchesDownMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownMpsA",
                                   fset="set_DisitckPlungerEndSwitchesDownMpsA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownMpsB = attribute(label='DisitckPlungerEndSwitchesDownMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownMpsB",
                                   fset="set_DisitckPlungerEndSwitchesDownMpsB",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownDiagA = attribute(label='DisitckPlungerEndSwitchesDownDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownDiagA",
                                   fset="set_DisitckPlungerEndSwitchesDownDiagA",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownDiagB = attribute(label='DisitckPlungerEndSwitchesDownDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownDiagB",
                                   fset="set_DisitckPlungerEndSwitchesDownDiagB",
                                   doc=""
                                   )

    DisitckMpsDacsoffloopsstbyA = attribute(label='DisitckMpsDacsoffloopsstbyA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsDacsoffloopsstbyA",
                                   fset="set_DisitckMpsDacsoffloopsstbyA",
                                   doc=""
                                   )

    DisitckMpsDacsoffloopsstbyB = attribute(label='DisitckMpsDacsoffloopsstbyB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsDacsoffloopsstbyB",
                                   fset="set_DisitckMpsDacsoffloopsstbyB",
                                   doc=""
                                   )

    DisitckMpsPindiodeswitchA = attribute(label='DisitckMpsPindiodeswitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsPindiodeswitchA",
                                   fset="set_DisitckMpsPindiodeswitchA",
                                   doc=""
                                   )

    DisitckMpsPindiodeswitchB = attribute(label='DisitckMpsPindiodeswitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsPindiodeswitchB",
                                   fset="set_DisitckMpsPindiodeswitchB",
                                   doc=""
                                   )

    DisitckMpsFdltrgA = attribute(label='DisitckMpsFdltrgA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsFdltrgA",
                                   fset="set_DisitckMpsFdltrgA",
                                   doc=""
                                   )

    DisitckMpsFdltrgB = attribute(label='DisitckMpsFdltrgB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsFdltrgB",
                                   fset="set_DisitckMpsFdltrgB",
                                   doc=""
                                   )

    DisitckMpsPlctxoffA = attribute(label='DisitckMpsPlctxoffA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsPlctxoffA",
                                   fset="set_DisitckMpsPlctxoffA",
                                   doc=""
                                   )

    DisitckMpsPlctxoffB = attribute(label='DisitckMpsPlctxoffB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsPlctxoffB",
                                   fset="set_DisitckMpsPlctxoffB",
                                   doc=""
                                   )

    DisitckMpsMpsA = attribute(label='DisitckMpsMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsMpsA",
                                   fset="set_DisitckMpsMpsA",
                                   doc=""
                                   )

    DisitckMpsMpsB = attribute(label='DisitckMpsMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsMpsB",
                                   fset="set_DisitckMpsMpsB",
                                   doc=""
                                   )

    DisitckMpsDiagA = attribute(label='DisitckMpsDiagA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsDiagA",
                                   fset="set_DisitckMpsDiagA",
                                   doc=""
                                   )

    DisitckMpsDiagB = attribute(label='DisitckMpsDiagB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsDiagB",
                                   fset="set_DisitckMpsDiagB",
                                   doc=""
                                   )

    Diag_Irvtet1A = attribute(label='Diag_Irvtet1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Irvtet1B = attribute(label='Diag_Irvtet1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvtet1A = attribute(label='Diag_Qrvtet1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvtet1B = attribute(label='Diag_Qrvtet1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvtet1A = attribute(label='Diag_Amprvtet1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvtet1B = attribute(label='Diag_Amprvtet1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvtet1A = attribute(label='Diag_Phrvtet1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvtet1B = attribute(label='Diag_Phrvtet1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Irvtet2A = attribute(label='Diag_Irvtet2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Irvtet2B = attribute(label='Diag_Irvtet2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvtet2A = attribute(label='Diag_Qrvtet2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvtet2B = attribute(label='Diag_Qrvtet2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvtet2A = attribute(label='Diag_Amprvtet2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvtet2B = attribute(label='Diag_Amprvtet2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvtet2A = attribute(label='Diag_Phrvtet2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvtet2B = attribute(label='Diag_Phrvtet2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwcircA = attribute(label='Diag_IfwcircA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwcircB = attribute(label='Diag_IfwcircB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwcircA = attribute(label='Diag_QfwcircA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwcircB = attribute(label='Diag_QfwcircB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwcircA = attribute(label='Diag_AmpfwcircA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwcircB = attribute(label='Diag_AmpfwcircB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwcircA = attribute(label='Diag_PhfwcircA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwcircB = attribute(label='Diag_PhfwcircB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrvcircA = attribute(label='Diag_IrvcircA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrvcircB = attribute(label='Diag_IrvcircB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrvcircA = attribute(label='Diag_QrvcircA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrvcircB = attribute(label='Diag_QrvcircB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmprvcircA = attribute(label='Diag_AmprvcircA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmprvcircB = attribute(label='Diag_AmprvcircB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhrvcircA = attribute(label='Diag_PhrvcircA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhrvcircB = attribute(label='Diag_PhrvcircB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwloadA = attribute(label='Diag_IfwloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwloadB = attribute(label='Diag_IfwloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwloadA = attribute(label='Diag_QfwloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwloadB = attribute(label='Diag_QfwloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwloadA = attribute(label='Diag_AmpfwloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwloadB = attribute(label='Diag_AmpfwloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwloadA = attribute(label='Diag_PhfwloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwloadB = attribute(label='Diag_PhfwloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwhybloadA = attribute(label='Diag_IfwhybloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IfwhybloadB = attribute(label='Diag_IfwhybloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwhybloadA = attribute(label='Diag_QfwhybloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QfwhybloadB = attribute(label='Diag_QfwhybloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwhybloadA = attribute(label='Diag_AmpfwhybloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpfwhybloadB = attribute(label='Diag_AmpfwhybloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwhybloadA = attribute(label='Diag_PhfwhybloadA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhfwhybloadB = attribute(label='Diag_PhfwhybloadB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrvcavA = attribute(label='Diag_IrvcavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrvcavB = attribute(label='Diag_IrvcavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrvcavA = attribute(label='Diag_QrvcavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrvcavB = attribute(label='Diag_QrvcavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmprvcavA = attribute(label='Diag_AmprvcavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmprvcavB = attribute(label='Diag_AmprvcavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhrvcavA = attribute(label='Diag_PhrvcavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhrvcavB = attribute(label='Diag_PhrvcavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ImoA = attribute(label='Diag_ImoA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ImoB = attribute(label='Diag_ImoB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QmoA = attribute(label='Diag_QmoA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QmoB = attribute(label='Diag_QmoB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpmoA = attribute(label='Diag_AmpmoA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpmoB = attribute(label='Diag_AmpmoB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhmoA = attribute(label='Diag_PhmoA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhmoB = attribute(label='Diag_PhmoB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IlandauA = attribute(label='Diag_IlandauA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IlandauB = attribute(label='Diag_IlandauB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QlandauA = attribute(label='Diag_QlandauA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QlandauB = attribute(label='Diag_QlandauB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmplandauA = attribute(label='Diag_AmplandauA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmplandauB = attribute(label='Diag_AmplandauB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhlandauA = attribute(label='Diag_PhlandauA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhlandauB = attribute(label='Diag_PhlandauB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingManualTuningA = attribute(label='Diag_PlungerMovingManualTuningA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingManualTuningB = attribute(label='Diag_PlungerMovingManualTuningB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpManualTuningA = attribute(label='Diag_PlungerMovingUpManualTuningA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpManualTuningB = attribute(label='Diag_PlungerMovingUpManualTuningB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingAutomaticTuningA = attribute(label='Diag_PlungerMovingAutomaticTuningA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingAutomaticTuningB = attribute(label='Diag_PlungerMovingAutomaticTuningB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpAutomaticTuningA = attribute(label='Diag_PlungerMovingUpAutomaticTuningA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpAutomaticTuningB = attribute(label='Diag_PlungerMovingUpAutomaticTuningB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_DephaseMoLandauA = attribute(label='Diag_DephaseMoLandauA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_DephaseMoLandauB = attribute(label='Diag_DephaseMoLandauB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvtet1A = attribute(label='Diag_Rvtet1A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvtet1B = attribute(label='Diag_Rvtet1B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvtet2A = attribute(label='Diag_Rvtet2A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvtet2B = attribute(label='Diag_Rvtet2B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_RvcircA = attribute(label='Diag_RvcircA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_RvcircB = attribute(label='Diag_RvcircB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwloadA = attribute(label='Diag_FwloadA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwloadB = attribute(label='Diag_FwloadB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwhybloadA = attribute(label='Diag_FwhybloadA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwhybloadB = attribute(label='Diag_FwhybloadB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_RvcavA = attribute(label='Diag_RvcavA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_RvcavB = attribute(label='Diag_RvcavB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ArcsA = attribute(label='Diag_ArcsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ArcsB = attribute(label='Diag_ArcsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VacuumA = attribute(label='Diag_VacuumA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VacuumB = attribute(label='Diag_VacuumB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualInterlockA = attribute(label='Diag_ManualInterlockA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualInterlockB = attribute(label='Diag_ManualInterlockB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ExternalItckA = attribute(label='Diag_ExternalItckA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ExternalItckB = attribute(label='Diag_ExternalItckB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchUpA = attribute(label='Diag_PlungerEndSwitchUpA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchUpB = attribute(label='Diag_PlungerEndSwitchUpB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchDownA = attribute(label='Diag_PlungerEndSwitchDownA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchDownB = attribute(label='Diag_PlungerEndSwitchDownB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp1A = attribute(label='Diag_Timestamp1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp1B = attribute(label='Diag_Timestamp1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp2A = attribute(label='Diag_Timestamp2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp2B = attribute(label='Diag_Timestamp2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp3A = attribute(label='Diag_Timestamp3A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp3B = attribute(label='Diag_Timestamp3B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp4A = attribute(label='Diag_Timestamp4A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp4B = attribute(label='Diag_Timestamp4B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp5A = attribute(label='Diag_Timestamp5A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp5B = attribute(label='Diag_Timestamp5B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp6A = attribute(label='Diag_Timestamp6A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp6B = attribute(label='Diag_Timestamp6B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp7A = attribute(label='Diag_Timestamp7A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp7B = attribute(label='Diag_Timestamp7B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_DacsDisableCommandA = attribute(label='Diag_DacsDisableCommandA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_DacsDisableCommandB = attribute(label='Diag_DacsDisableCommandB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PinSwitchA = attribute(label='Diag_PinSwitchA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PinSwitchB = attribute(label='Diag_PinSwitchB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTriggerToLoopsdiagboardA = attribute(label='Diag_FdlTriggerToLoopsdiagboardA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTriggerToLoopsdiagboardB = attribute(label='Diag_FdlTriggerToLoopsdiagboardB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_OutputToPlcA = attribute(label='Diag_OutputToPlcA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_OutputToPlcB = attribute(label='Diag_OutputToPlcB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_OutputToMpsA = attribute(label='Diag_OutputToMpsA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_OutputToMpsB = attribute(label='Diag_OutputToMpsB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvtet1b = attribute(label='Diag_AmpRvtet1b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvtet1a = attribute(label='Diag_AmpRvtet1a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMoa = attribute(label='Diag_AmpMoa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLandaua = attribute(label='Diag_AmpLandaua',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwloada = attribute(label='Diag_AmpFwloada',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvtet2b = attribute(label='Diag_AmpRvtet2b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvtet2a = attribute(label='Diag_AmpRvtet2a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwloadb = attribute(label='Diag_AmpFwloadb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvcavb = attribute(label='Diag_AmpRvcavb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvcava = attribute(label='Diag_AmpRvcava',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcircb = attribute(label='Diag_AmpFwcircb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcirca = attribute(label='Diag_AmpFwcirca',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMob = attribute(label='Diag_AmpMob',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvcirca = attribute(label='Diag_AmpRvcirca',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvcircb = attribute(label='Diag_AmpRvcircb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwhybloadb = attribute(label='Diag_AmpFwhybloadb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwhybloada = attribute(label='Diag_AmpFwhybloada',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLandaub = attribute(label='Diag_AmpLandaub',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvtet1b = attribute(label='Diag_PhRvtet1b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvtet1a = attribute(label='Diag_PhRvtet1a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMoa = attribute(label='Diag_PhMoa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLandaua = attribute(label='Diag_PhLandaua',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwloada = attribute(label='Diag_PhFwloada',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvtet2b = attribute(label='Diag_PhRvtet2b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvtet2a = attribute(label='Diag_PhRvtet2a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwloadb = attribute(label='Diag_PhFwloadb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvcavb = attribute(label='Diag_PhRvcavb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvcava = attribute(label='Diag_PhRvcava',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcircb = attribute(label='Diag_PhFwcircb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcirca = attribute(label='Diag_PhFwcirca',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMob = attribute(label='Diag_PhMob',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvcirca = attribute(label='Diag_PhRvcirca',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvcircb = attribute(label='Diag_PhRvcircb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwhybloadb = attribute(label='Diag_PhFwhybloadb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwhybloada = attribute(label='Diag_PhFwhybloada',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLandaub = attribute(label='Diag_PhLandaub',
                                   dtype=float,
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
            self.set_state(DevState.ON)
        except Exception, e:
            print e
            self.set_state(DevState.FAULT)

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

    @DebugIt()
    def get_Rvtet1B(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 0, 'B')

    @DebugIt()
    def set_Rvtet1B(self, Rvtet1B):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Rvtet1B, 0, 'B')

    @DebugIt()
    def get_Rvtet2A(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 1, 'A')

    @DebugIt()
    def set_Rvtet2A(self, Rvtet2A):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Rvtet2A, 1, 'A')

    @DebugIt()
    def get_Rvtet2B(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 1, 'B')

    @DebugIt()
    def set_Rvtet2B(self, Rvtet2B):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Rvtet2B, 1, 'B')

    @DebugIt()
    def get_RvcircA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 2, 'A')

    @DebugIt()
    def set_RvcircA(self, RvcircA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, RvcircA, 2, 'A')

    @DebugIt()
    def get_RvcircB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 2, 'B')

    @DebugIt()
    def set_RvcircB(self, RvcircB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, RvcircB, 2, 'B')

    @DebugIt()
    def get_FwloadA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 3, 'A')

    @DebugIt()
    def set_FwloadA(self, FwloadA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, FwloadA, 3, 'A')

    @DebugIt()
    def get_FwloadB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 3, 'B')

    @DebugIt()
    def set_FwloadB(self, FwloadB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, FwloadB, 3, 'B')

    @DebugIt()
    def get_FwhybloadA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 4, 'A')

    @DebugIt()
    def set_FwhybloadA(self, FwhybloadA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, FwhybloadA, 4, 'A')

    @DebugIt()
    def get_FwhybloadB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 4, 'B')

    @DebugIt()
    def set_FwhybloadB(self, FwhybloadB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, FwhybloadB, 4, 'B')

    @DebugIt()
    def get_RvcavA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 5, 'A')

    @DebugIt()
    def set_RvcavA(self, RvcavA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, RvcavA, 5, 'A')

    @DebugIt()
    def get_RvcavB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 5, 'B')

    @DebugIt()
    def set_RvcavB(self, RvcavB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, RvcavB, 5, 'B')

    @DebugIt()
    def get_ManualInterlockA(self):
        return perseus_utils.read_direct(self.perseus, 6, 'A')

    @DebugIt()
    def set_ManualInterlockA(self, ManualInterlockA):
        perseus_utils.write_direct(self.perseus, ManualInterlockA, 6, 'A')

    @DebugIt()
    def get_ManualInterlockB(self):
        return perseus_utils.read_direct(self.perseus, 6, 'B')

    @DebugIt()
    def set_ManualInterlockB(self, ManualInterlockB):
        perseus_utils.write_direct(self.perseus, ManualInterlockB, 6, 'B')

    @DebugIt()
    def get_DisableItckRvtet1A(self):
        return perseus_utils.read_direct(self.perseus, 7, 'A')

    @DebugIt()
    def set_DisableItckRvtet1A(self, DisableItckRvtet1A):
        perseus_utils.write_direct(self.perseus, DisableItckRvtet1A, 7, 'A')

    @DebugIt()
    def get_DisableItckRvtet1B(self):
        return perseus_utils.read_direct(self.perseus, 7, 'B')

    @DebugIt()
    def set_DisableItckRvtet1B(self, DisableItckRvtet1B):
        perseus_utils.write_direct(self.perseus, DisableItckRvtet1B, 7, 'B')

    @DebugIt()
    def get_DisableItckRvtet2A(self):
        return perseus_utils.read_direct(self.perseus, 8, 'A')

    @DebugIt()
    def set_DisableItckRvtet2A(self, DisableItckRvtet2A):
        perseus_utils.write_direct(self.perseus, DisableItckRvtet2A, 8, 'A')

    @DebugIt()
    def get_DisableItckRvtet2B(self):
        return perseus_utils.read_direct(self.perseus, 8, 'B')

    @DebugIt()
    def set_DisableItckRvtet2B(self, DisableItckRvtet2B):
        perseus_utils.write_direct(self.perseus, DisableItckRvtet2B, 8, 'B')

    @DebugIt()
    def get_DisableItckRvcircA(self):
        return perseus_utils.read_direct(self.perseus, 9, 'A')

    @DebugIt()
    def set_DisableItckRvcircA(self, DisableItckRvcircA):
        perseus_utils.write_direct(self.perseus, DisableItckRvcircA, 9, 'A')

    @DebugIt()
    def get_DisableItckRvcircB(self):
        return perseus_utils.read_direct(self.perseus, 9, 'B')

    @DebugIt()
    def set_DisableItckRvcircB(self, DisableItckRvcircB):
        perseus_utils.write_direct(self.perseus, DisableItckRvcircB, 9, 'B')

    @DebugIt()
    def get_DisableItckFwloadA(self):
        return perseus_utils.read_direct(self.perseus, 10, 'A')

    @DebugIt()
    def set_DisableItckFwloadA(self, DisableItckFwloadA):
        perseus_utils.write_direct(self.perseus, DisableItckFwloadA, 10, 'A')

    @DebugIt()
    def get_DisableItckFwloadB(self):
        return perseus_utils.read_direct(self.perseus, 10, 'B')

    @DebugIt()
    def set_DisableItckFwloadB(self, DisableItckFwloadB):
        perseus_utils.write_direct(self.perseus, DisableItckFwloadB, 10, 'B')

    @DebugIt()
    def get_DisableItckFwhybloadA(self):
        return perseus_utils.read_direct(self.perseus, 11, 'A')

    @DebugIt()
    def set_DisableItckFwhybloadA(self, DisableItckFwhybloadA):
        perseus_utils.write_direct(self.perseus, DisableItckFwhybloadA, 11, 'A')

    @DebugIt()
    def get_DisableItckFwhybloadB(self):
        return perseus_utils.read_direct(self.perseus, 11, 'B')

    @DebugIt()
    def set_DisableItckFwhybloadB(self, DisableItckFwhybloadB):
        perseus_utils.write_direct(self.perseus, DisableItckFwhybloadB, 11, 'B')

    @DebugIt()
    def get_DisableItckRvcavA(self):
        return perseus_utils.read_direct(self.perseus, 12, 'A')

    @DebugIt()
    def set_DisableItckRvcavA(self, DisableItckRvcavA):
        perseus_utils.write_direct(self.perseus, DisableItckRvcavA, 12, 'A')

    @DebugIt()
    def get_DisableItckRvcavB(self):
        return perseus_utils.read_direct(self.perseus, 12, 'B')

    @DebugIt()
    def set_DisableItckRvcavB(self, DisableItckRvcavB):
        perseus_utils.write_direct(self.perseus, DisableItckRvcavB, 12, 'B')

    @DebugIt()
    def get_DisableItckArcsA(self):
        return perseus_utils.read_direct(self.perseus, 13, 'A')

    @DebugIt()
    def set_DisableItckArcsA(self, DisableItckArcsA):
        perseus_utils.write_direct(self.perseus, DisableItckArcsA, 13, 'A')

    @DebugIt()
    def get_DisableItckArcsB(self):
        return perseus_utils.read_direct(self.perseus, 13, 'B')

    @DebugIt()
    def set_DisableItckArcsB(self, DisableItckArcsB):
        perseus_utils.write_direct(self.perseus, DisableItckArcsB, 13, 'B')

    @DebugIt()
    def get_DisableItckVaccumA(self):
        return perseus_utils.read_direct(self.perseus, 14, 'A')

    @DebugIt()
    def set_DisableItckVaccumA(self, DisableItckVaccumA):
        perseus_utils.write_direct(self.perseus, DisableItckVaccumA, 14, 'A')

    @DebugIt()
    def get_DisableItckVaccumB(self):
        return perseus_utils.read_direct(self.perseus, 14, 'B')

    @DebugIt()
    def set_DisableItckVaccumB(self, DisableItckVaccumB):
        perseus_utils.write_direct(self.perseus, DisableItckVaccumB, 14, 'B')

    @DebugIt()
    def get_DisableItckManualInterlockA(self):
        return perseus_utils.read_direct(self.perseus, 15, 'A')

    @DebugIt()
    def set_DisableItckManualInterlockA(self, DisableItckManualInterlockA):
        perseus_utils.write_direct(self.perseus, DisableItckManualInterlockA, 15, 'A')

    @DebugIt()
    def get_DisableItckManualInterlockB(self):
        return perseus_utils.read_direct(self.perseus, 15, 'B')

    @DebugIt()
    def set_DisableItckManualInterlockB(self, DisableItckManualInterlockB):
        perseus_utils.write_direct(self.perseus, DisableItckManualInterlockB, 15, 'B')

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesUpA(self):
        return perseus_utils.read_direct(self.perseus, 16, 'A')

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesUpA(self, DisableItckPlungerEndSwitchesUpA):
        perseus_utils.write_direct(self.perseus, DisableItckPlungerEndSwitchesUpA, 16, 'A')

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesUpB(self):
        return perseus_utils.read_direct(self.perseus, 16, 'B')

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesUpB(self, DisableItckPlungerEndSwitchesUpB):
        perseus_utils.write_direct(self.perseus, DisableItckPlungerEndSwitchesUpB, 16, 'B')

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesDownA(self):
        return perseus_utils.read_direct(self.perseus, 17, 'A')

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesDownA(self, DisableItckPlungerEndSwitchesDownA):
        perseus_utils.write_direct(self.perseus, DisableItckPlungerEndSwitchesDownA, 17, 'A')

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesDownB(self):
        return perseus_utils.read_direct(self.perseus, 17, 'B')

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesDownB(self, DisableItckPlungerEndSwitchesDownB):
        perseus_utils.write_direct(self.perseus, DisableItckPlungerEndSwitchesDownB, 17, 'B')

    @DebugIt()
    def get_DisableItckMpsA(self):
        return perseus_utils.read_direct(self.perseus, 18, 'A')

    @DebugIt()
    def set_DisableItckMpsA(self, DisableItckMpsA):
        perseus_utils.write_direct(self.perseus, DisableItckMpsA, 18, 'A')

    @DebugIt()
    def get_DisableItckMpsB(self):
        return perseus_utils.read_direct(self.perseus, 18, 'B')

    @DebugIt()
    def set_DisableItckMpsB(self, DisableItckMpsB):
        perseus_utils.write_direct(self.perseus, DisableItckMpsB, 18, 'B')

    @DebugIt()
    def get_SamplesToAverageA(self):
        return perseus_utils.read_direct(self.perseus, 19, 'A')

    @DebugIt()
    def set_SamplesToAverageA(self, SamplesToAverageA):
        perseus_utils.write_direct(self.perseus, SamplesToAverageA, 19, 'A')

    @DebugIt()
    def get_SamplesToAverageB(self):
        return perseus_utils.read_direct(self.perseus, 19, 'B')

    @DebugIt()
    def set_SamplesToAverageB(self, SamplesToAverageB):
        perseus_utils.write_direct(self.perseus, SamplesToAverageB, 19, 'B')

    @DebugIt()
    def get_PulseupLogicInversionA(self):
        return perseus_utils.read_direct(self.perseus, 20, 'A')

    @DebugIt()
    def set_PulseupLogicInversionA(self, PulseupLogicInversionA):
        perseus_utils.write_direct(self.perseus, PulseupLogicInversionA, 20, 'A')

    @DebugIt()
    def get_PulseupLogicInversionB(self):
        return perseus_utils.read_direct(self.perseus, 20, 'B')

    @DebugIt()
    def set_PulseupLogicInversionB(self, PulseupLogicInversionB):
        perseus_utils.write_direct(self.perseus, PulseupLogicInversionB, 20, 'B')

    @DebugIt()
    def get_EndSwitchesConnectedToNoNcContactA(self):
        return perseus_utils.read_direct(self.perseus, 21, 'A')

    @DebugIt()
    def set_EndSwitchesConnectedToNoNcContactA(self, EndSwitchesConnectedToNoNcContactA):
        perseus_utils.write_direct(self.perseus, EndSwitchesConnectedToNoNcContactA, 21, 'A')

    @DebugIt()
    def get_EndSwitchesConnectedToNoNcContactB(self):
        return perseus_utils.read_direct(self.perseus, 21, 'B')

    @DebugIt()
    def set_EndSwitchesConnectedToNoNcContactB(self, EndSwitchesConnectedToNoNcContactB):
        perseus_utils.write_direct(self.perseus, EndSwitchesConnectedToNoNcContactB, 21, 'B')

    @DebugIt()
    def get_LookrefA(self):
        return perseus_utils.read_direct(self.perseus, 22, 'A')

    @DebugIt()
    def set_LookrefA(self, LookrefA):
        perseus_utils.write_direct(self.perseus, LookrefA, 22, 'A')

    @DebugIt()
    def get_LookrefB(self):
        return perseus_utils.read_direct(self.perseus, 22, 'B')

    @DebugIt()
    def set_LookrefB(self, LookrefB):
        perseus_utils.write_direct(self.perseus, LookrefB, 22, 'B')

    @DebugIt()
    def get_QuadrefA(self):
        return perseus_utils.read_direct(self.perseus, 23, 'A')

    @DebugIt()
    def set_QuadrefA(self, QuadrefA):
        perseus_utils.write_direct(self.perseus, QuadrefA, 23, 'A')

    @DebugIt()
    def get_QuadrefB(self):
        return perseus_utils.read_direct(self.perseus, 23, 'B')

    @DebugIt()
    def set_QuadrefB(self, QuadrefB):
        perseus_utils.write_direct(self.perseus, QuadrefB, 23, 'B')

    @DebugIt()
    def get_SpareDo1A(self):
        return perseus_utils.read_direct(self.perseus, 24, 'A')

    @DebugIt()
    def set_SpareDo1A(self, SpareDo1A):
        perseus_utils.write_direct(self.perseus, SpareDo1A, 24, 'A')

    @DebugIt()
    def get_SpareDo1B(self):
        return perseus_utils.read_direct(self.perseus, 24, 'B')

    @DebugIt()
    def set_SpareDo1B(self, SpareDo1B):
        perseus_utils.write_direct(self.perseus, SpareDo1B, 24, 'B')

    @DebugIt()
    def get_SpareDo2A(self):
        return perseus_utils.read_direct(self.perseus, 25, 'A')

    @DebugIt()
    def set_SpareDo2A(self, SpareDo2A):
        perseus_utils.write_direct(self.perseus, SpareDo2A, 25, 'A')

    @DebugIt()
    def get_SpareDo2B(self):
        return perseus_utils.read_direct(self.perseus, 25, 'B')

    @DebugIt()
    def set_SpareDo2B(self, SpareDo2B):
        perseus_utils.write_direct(self.perseus, SpareDo2B, 25, 'B')

    @DebugIt()
    def get_SpareDo3A(self):
        return perseus_utils.read_direct(self.perseus, 26, 'A')

    @DebugIt()
    def set_SpareDo3A(self, SpareDo3A):
        perseus_utils.write_direct(self.perseus, SpareDo3A, 26, 'A')

    @DebugIt()
    def get_SpareDo3B(self):
        return perseus_utils.read_direct(self.perseus, 26, 'B')

    @DebugIt()
    def set_SpareDo3B(self, SpareDo3B):
        perseus_utils.write_direct(self.perseus, SpareDo3B, 26, 'B')

    @DebugIt()
    def get_FdlSwTriggerA(self):
        return perseus_utils.read_direct(self.perseus, 27, 'A')

    @DebugIt()
    def set_FdlSwTriggerA(self, FdlSwTriggerA):
        perseus_utils.write_direct(self.perseus, FdlSwTriggerA, 27, 'A')

    @DebugIt()
    def get_FdlSwTriggerB(self):
        return perseus_utils.read_direct(self.perseus, 27, 'B')

    @DebugIt()
    def set_FdlSwTriggerB(self, FdlSwTriggerB):
        perseus_utils.write_direct(self.perseus, FdlSwTriggerB, 27, 'B')

    @DebugIt()
    def get_ResetInterlocksCavA(self):
        return perseus_utils.read_direct(self.perseus, 100, 'A')

    @DebugIt()
    def set_ResetInterlocksCavA(self, ResetInterlocksCavA):
        perseus_utils.write_direct(self.perseus, ResetInterlocksCavA, 100, 'A')

    @DebugIt()
    def get_ResetInterlocksCavB(self):
        return perseus_utils.read_direct(self.perseus, 100, 'B')

    @DebugIt()
    def set_ResetInterlocksCavB(self, ResetInterlocksCavB):
        perseus_utils.write_direct(self.perseus, ResetInterlocksCavB, 100, 'B')

    @DebugIt()
    def get_LandautuningenableA(self):
        return perseus_utils.read_direct(self.perseus, 200, 'A')

    @DebugIt()
    def set_LandautuningenableA(self, LandautuningenableA):
        perseus_utils.write_direct(self.perseus, LandautuningenableA, 200, 'A')

    @DebugIt()
    def get_LandautuningenableB(self):
        return perseus_utils.read_direct(self.perseus, 200, 'B')

    @DebugIt()
    def set_LandautuningenableB(self, LandautuningenableB):
        perseus_utils.write_direct(self.perseus, LandautuningenableB, 200, 'B')

    @DebugIt()
    def get_LandautuningresetA(self):
        return perseus_utils.read_direct(self.perseus, 201, 'A')

    @DebugIt()
    def set_LandautuningresetA(self, LandautuningresetA):
        perseus_utils.write_direct(self.perseus, LandautuningresetA, 201, 'A')

    @DebugIt()
    def get_LandautuningresetB(self):
        return perseus_utils.read_direct(self.perseus, 201, 'B')

    @DebugIt()
    def set_LandautuningresetB(self, LandautuningresetB):
        perseus_utils.write_direct(self.perseus, LandautuningresetB, 201, 'B')

    @DebugIt()
    def get_MovelandauupA(self):
        return perseus_utils.read_direct(self.perseus, 202, 'A')

    @DebugIt()
    def set_MovelandauupA(self, MovelandauupA):
        perseus_utils.write_direct(self.perseus, MovelandauupA, 202, 'A')

    @DebugIt()
    def get_MovelandauupB(self):
        return perseus_utils.read_direct(self.perseus, 202, 'B')

    @DebugIt()
    def set_MovelandauupB(self, MovelandauupB):
        perseus_utils.write_direct(self.perseus, MovelandauupB, 202, 'B')

    @DebugIt()
    def get_MovelandauplgA(self):
        return perseus_utils.read_direct(self.perseus, 203, 'A')

    @DebugIt()
    def set_MovelandauplgA(self, MovelandauplgA):
        perseus_utils.write_direct(self.perseus, MovelandauplgA, 203, 'A')

    @DebugIt()
    def get_MovelandauplgB(self):
        return perseus_utils.read_direct(self.perseus, 203, 'B')

    @DebugIt()
    def set_MovelandauplgB(self, MovelandauplgB):
        perseus_utils.write_direct(self.perseus, MovelandauplgB, 203, 'B')

    @DebugIt()
    def get_NumstepsA(self):
        return perseus_utils.read_direct(self.perseus, 204, 'A')

    @DebugIt()
    def set_NumstepsA(self, NumstepsA):
        perseus_utils.write_direct(self.perseus, NumstepsA, 204, 'A')

    @DebugIt()
    def get_NumstepsB(self):
        return perseus_utils.read_direct(self.perseus, 204, 'B')

    @DebugIt()
    def set_NumstepsB(self, NumstepsB):
        perseus_utils.write_direct(self.perseus, NumstepsB, 204, 'B')

    @DebugIt()
    def get_LandauphaseoffsetA(self):
        return perseus_utils.read_angle(self.perseus, 205, 'A')

    @DebugIt()
    def set_LandauphaseoffsetA(self, LandauphaseoffsetA):
        perseus_utils.write_angle(self.perseus, LandauphaseoffsetA, 205, 'A')

    @DebugIt()
    def get_LandauphaseoffsetB(self):
        return perseus_utils.read_angle(self.perseus, 205, 'B')

    @DebugIt()
    def set_LandauphaseoffsetB(self, LandauphaseoffsetB):
        perseus_utils.write_angle(self.perseus, LandauphaseoffsetB, 205, 'B')

    @DebugIt()
    def get_LandaumarginupA(self):
        return perseus_utils.read_settings_diag_percentage(self.perseus, 206, 'A')

    @DebugIt()
    def set_LandaumarginupA(self, LandaumarginupA):
        perseus_utils.write_settings_diag_percentage(self.perseus, LandaumarginupA, 206, 'A')

    @DebugIt()
    def get_LandaumarginupB(self):
        return perseus_utils.read_settings_diag_percentage(self.perseus, 206, 'B')

    @DebugIt()
    def set_LandaumarginupB(self, LandaumarginupB):
        perseus_utils.write_settings_diag_percentage(self.perseus, LandaumarginupB, 206, 'B')

    @DebugIt()
    def get_LandauMarginLowA(self):
        return perseus_utils.read_settings_diag_percentage(self.perseus, 207, 'A')

    @DebugIt()
    def set_LandauMarginLowA(self, LandauMarginLowA):
        perseus_utils.write_settings_diag_percentage(self.perseus, LandauMarginLowA, 207, 'A')

    @DebugIt()
    def get_LandauMarginLowB(self):
        return perseus_utils.read_settings_diag_percentage(self.perseus, 207, 'B')

    @DebugIt()
    def set_LandauMarginLowB(self, LandauMarginLowB):
        perseus_utils.write_settings_diag_percentage(self.perseus, LandauMarginLowB, 207, 'B')

    @DebugIt()
    def get_MinimumLandauAmplitudeA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 208, 'A')

    @DebugIt()
    def set_MinimumLandauAmplitudeA(self, MinimumLandauAmplitudeA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, MinimumLandauAmplitudeA, 208, 'A')

    @DebugIt()
    def get_MinimumLandauAmplitudeB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 208, 'B')

    @DebugIt()
    def set_MinimumLandauAmplitudeB(self, MinimumLandauAmplitudeB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, MinimumLandauAmplitudeB, 208, 'B')

    @DebugIt()
    def get_LandauPositiveEnableA(self):
        return perseus_utils.read_direct(self.perseus, 209, 'A')

    @DebugIt()
    def set_LandauPositiveEnableA(self, LandauPositiveEnableA):
        perseus_utils.write_direct(self.perseus, LandauPositiveEnableA, 209, 'A')

    @DebugIt()
    def get_LandauPositiveEnableB(self):
        return perseus_utils.read_direct(self.perseus, 209, 'B')

    @DebugIt()
    def set_LandauPositiveEnableB(self, LandauPositiveEnableB):
        perseus_utils.write_direct(self.perseus, LandauPositiveEnableB, 209, 'B')

    @DebugIt()
    def get_LandauampsettingA(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 210, 'A')

    @DebugIt()
    def set_LandauampsettingA(self, LandauampsettingA):
        perseus_utils.write_settings_diag_milivolts(self.perseus, LandauampsettingA, 210, 'A')

    @DebugIt()
    def get_LandauampsettingB(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 210, 'B')

    @DebugIt()
    def set_LandauampsettingB(self, LandauampsettingB):
        perseus_utils.write_settings_diag_milivolts(self.perseus, LandauampsettingB, 210, 'B')

    @DebugIt()
    def get_DisitckRvtet1DacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,7, 'A')
        self._DisitckRvtet1DacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckRvtet1DacsoffloopsstbyA

    @DebugIt()
    def set_DisitckRvtet1DacsoffloopsstbyA(self, DisitckRvtet1DacsoffloopsstbyA):
        self._DisitckRvtet1DacsoffloopsstbyA = DisitckRvtet1DacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1DacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,7, 'B')
        self._DisitckRvtet1DacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckRvtet1DacsoffloopsstbyB

    @DebugIt()
    def set_DisitckRvtet1DacsoffloopsstbyB(self, DisitckRvtet1DacsoffloopsstbyB):
        self._DisitckRvtet1DacsoffloopsstbyB = DisitckRvtet1DacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1PindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,7, 'A')
        self._DisitckRvtet1PindiodeswitchA = (value >> 1) & 1
        return self._DisitckRvtet1PindiodeswitchA

    @DebugIt()
    def set_DisitckRvtet1PindiodeswitchA(self, DisitckRvtet1PindiodeswitchA):
        self._DisitckRvtet1PindiodeswitchA = DisitckRvtet1PindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1PindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,7, 'B')
        self._DisitckRvtet1PindiodeswitchB = (value >> 1) & 1
        return self._DisitckRvtet1PindiodeswitchB

    @DebugIt()
    def set_DisitckRvtet1PindiodeswitchB(self, DisitckRvtet1PindiodeswitchB):
        self._DisitckRvtet1PindiodeswitchB = DisitckRvtet1PindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1FdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,7, 'A')
        self._DisitckRvtet1FdltrgA = (value >> 2) & 1
        return self._DisitckRvtet1FdltrgA

    @DebugIt()
    def set_DisitckRvtet1FdltrgA(self, DisitckRvtet1FdltrgA):
        self._DisitckRvtet1FdltrgA = DisitckRvtet1FdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1FdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,7, 'B')
        self._DisitckRvtet1FdltrgB = (value >> 2) & 1
        return self._DisitckRvtet1FdltrgB

    @DebugIt()
    def set_DisitckRvtet1FdltrgB(self, DisitckRvtet1FdltrgB):
        self._DisitckRvtet1FdltrgB = DisitckRvtet1FdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1PlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,7, 'A')
        self._DisitckRvtet1PlctxoffA = (value >> 3) & 1
        return self._DisitckRvtet1PlctxoffA

    @DebugIt()
    def set_DisitckRvtet1PlctxoffA(self, DisitckRvtet1PlctxoffA):
        self._DisitckRvtet1PlctxoffA = DisitckRvtet1PlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1PlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,7, 'B')
        self._DisitckRvtet1PlctxoffB = (value >> 3) & 1
        return self._DisitckRvtet1PlctxoffB

    @DebugIt()
    def set_DisitckRvtet1PlctxoffB(self, DisitckRvtet1PlctxoffB):
        self._DisitckRvtet1PlctxoffB = DisitckRvtet1PlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1MpsA(self):
        value = perseus_utils.read_direct(self.perseus,7, 'A')
        self._DisitckRvtet1MpsA = (value >> 4) & 1
        return self._DisitckRvtet1MpsA

    @DebugIt()
    def set_DisitckRvtet1MpsA(self, DisitckRvtet1MpsA):
        self._DisitckRvtet1MpsA = DisitckRvtet1MpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1MpsB(self):
        value = perseus_utils.read_direct(self.perseus,7, 'B')
        self._DisitckRvtet1MpsB = (value >> 4) & 1
        return self._DisitckRvtet1MpsB

    @DebugIt()
    def set_DisitckRvtet1MpsB(self, DisitckRvtet1MpsB):
        self._DisitckRvtet1MpsB = DisitckRvtet1MpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1DiagA(self):
        value = perseus_utils.read_direct(self.perseus,7, 'A')
        self._DisitckRvtet1DiagA = (value >> 5) & 1
        return self._DisitckRvtet1DiagA

    @DebugIt()
    def set_DisitckRvtet1DiagA(self, DisitckRvtet1DiagA):
        self._DisitckRvtet1DiagA = DisitckRvtet1DiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1DiagB(self):
        value = perseus_utils.read_direct(self.perseus,7, 'B')
        self._DisitckRvtet1DiagB = (value >> 5) & 1
        return self._DisitckRvtet1DiagB

    @DebugIt()
    def set_DisitckRvtet1DiagB(self, DisitckRvtet1DiagB):
        self._DisitckRvtet1DiagB = DisitckRvtet1DiagB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2DacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,8, 'A')
        self._DisitckRvtet2DacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckRvtet2DacsoffloopsstbyA

    @DebugIt()
    def set_DisitckRvtet2DacsoffloopsstbyA(self, DisitckRvtet2DacsoffloopsstbyA):
        self._DisitckRvtet2DacsoffloopsstbyA = DisitckRvtet2DacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2DacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,8, 'B')
        self._DisitckRvtet2DacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckRvtet2DacsoffloopsstbyB

    @DebugIt()
    def set_DisitckRvtet2DacsoffloopsstbyB(self, DisitckRvtet2DacsoffloopsstbyB):
        self._DisitckRvtet2DacsoffloopsstbyB = DisitckRvtet2DacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2PindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,8, 'A')
        self._DisitckRvtet2PindiodeswitchA = (value >> 1) & 1
        return self._DisitckRvtet2PindiodeswitchA

    @DebugIt()
    def set_DisitckRvtet2PindiodeswitchA(self, DisitckRvtet2PindiodeswitchA):
        self._DisitckRvtet2PindiodeswitchA = DisitckRvtet2PindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2PindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,8, 'B')
        self._DisitckRvtet2PindiodeswitchB = (value >> 1) & 1
        return self._DisitckRvtet2PindiodeswitchB

    @DebugIt()
    def set_DisitckRvtet2PindiodeswitchB(self, DisitckRvtet2PindiodeswitchB):
        self._DisitckRvtet2PindiodeswitchB = DisitckRvtet2PindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2FdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,8, 'A')
        self._DisitckRvtet2FdltrgA = (value >> 2) & 1
        return self._DisitckRvtet2FdltrgA

    @DebugIt()
    def set_DisitckRvtet2FdltrgA(self, DisitckRvtet2FdltrgA):
        self._DisitckRvtet2FdltrgA = DisitckRvtet2FdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2FdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,8, 'B')
        self._DisitckRvtet2FdltrgB = (value >> 2) & 1
        return self._DisitckRvtet2FdltrgB

    @DebugIt()
    def set_DisitckRvtet2FdltrgB(self, DisitckRvtet2FdltrgB):
        self._DisitckRvtet2FdltrgB = DisitckRvtet2FdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2PlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,8, 'A')
        self._DisitckRvtet2PlctxoffA = (value >> 3) & 1
        return self._DisitckRvtet2PlctxoffA

    @DebugIt()
    def set_DisitckRvtet2PlctxoffA(self, DisitckRvtet2PlctxoffA):
        self._DisitckRvtet2PlctxoffA = DisitckRvtet2PlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2PlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,8, 'B')
        self._DisitckRvtet2PlctxoffB = (value >> 3) & 1
        return self._DisitckRvtet2PlctxoffB

    @DebugIt()
    def set_DisitckRvtet2PlctxoffB(self, DisitckRvtet2PlctxoffB):
        self._DisitckRvtet2PlctxoffB = DisitckRvtet2PlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2MpsA(self):
        value = perseus_utils.read_direct(self.perseus,8, 'A')
        self._DisitckRvtet2MpsA = (value >> 4) & 1
        return self._DisitckRvtet2MpsA

    @DebugIt()
    def set_DisitckRvtet2MpsA(self, DisitckRvtet2MpsA):
        self._DisitckRvtet2MpsA = DisitckRvtet2MpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2MpsB(self):
        value = perseus_utils.read_direct(self.perseus,8, 'B')
        self._DisitckRvtet2MpsB = (value >> 4) & 1
        return self._DisitckRvtet2MpsB

    @DebugIt()
    def set_DisitckRvtet2MpsB(self, DisitckRvtet2MpsB):
        self._DisitckRvtet2MpsB = DisitckRvtet2MpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2DiagA(self):
        value = perseus_utils.read_direct(self.perseus,8, 'A')
        self._DisitckRvtet2DiagA = (value >> 5) & 1
        return self._DisitckRvtet2DiagA

    @DebugIt()
    def set_DisitckRvtet2DiagA(self, DisitckRvtet2DiagA):
        self._DisitckRvtet2DiagA = DisitckRvtet2DiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2DiagB(self):
        value = perseus_utils.read_direct(self.perseus,8, 'B')
        self._DisitckRvtet2DiagB = (value >> 5) & 1
        return self._DisitckRvtet2DiagB

    @DebugIt()
    def set_DisitckRvtet2DiagB(self, DisitckRvtet2DiagB):
        self._DisitckRvtet2DiagB = DisitckRvtet2DiagB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,9, 'A')
        self._DisitckRvcircDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckRvcircDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckRvcircDacsoffloopsstbyA(self, DisitckRvcircDacsoffloopsstbyA):
        self._DisitckRvcircDacsoffloopsstbyA = DisitckRvcircDacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,9, 'B')
        self._DisitckRvcircDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckRvcircDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckRvcircDacsoffloopsstbyB(self, DisitckRvcircDacsoffloopsstbyB):
        self._DisitckRvcircDacsoffloopsstbyB = DisitckRvcircDacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,9, 'A')
        self._DisitckRvcircPindiodeswitchA = (value >> 1) & 1
        return self._DisitckRvcircPindiodeswitchA

    @DebugIt()
    def set_DisitckRvcircPindiodeswitchA(self, DisitckRvcircPindiodeswitchA):
        self._DisitckRvcircPindiodeswitchA = DisitckRvcircPindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,9, 'B')
        self._DisitckRvcircPindiodeswitchB = (value >> 1) & 1
        return self._DisitckRvcircPindiodeswitchB

    @DebugIt()
    def set_DisitckRvcircPindiodeswitchB(self, DisitckRvcircPindiodeswitchB):
        self._DisitckRvcircPindiodeswitchB = DisitckRvcircPindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,9, 'A')
        self._DisitckRvcircFdltrgA = (value >> 2) & 1
        return self._DisitckRvcircFdltrgA

    @DebugIt()
    def set_DisitckRvcircFdltrgA(self, DisitckRvcircFdltrgA):
        self._DisitckRvcircFdltrgA = DisitckRvcircFdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,9, 'B')
        self._DisitckRvcircFdltrgB = (value >> 2) & 1
        return self._DisitckRvcircFdltrgB

    @DebugIt()
    def set_DisitckRvcircFdltrgB(self, DisitckRvcircFdltrgB):
        self._DisitckRvcircFdltrgB = DisitckRvcircFdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,9, 'A')
        self._DisitckRvcircPlctxoffA = (value >> 3) & 1
        return self._DisitckRvcircPlctxoffA

    @DebugIt()
    def set_DisitckRvcircPlctxoffA(self, DisitckRvcircPlctxoffA):
        self._DisitckRvcircPlctxoffA = DisitckRvcircPlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,9, 'B')
        self._DisitckRvcircPlctxoffB = (value >> 3) & 1
        return self._DisitckRvcircPlctxoffB

    @DebugIt()
    def set_DisitckRvcircPlctxoffB(self, DisitckRvcircPlctxoffB):
        self._DisitckRvcircPlctxoffB = DisitckRvcircPlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircMpsA(self):
        value = perseus_utils.read_direct(self.perseus,9, 'A')
        self._DisitckRvcircMpsA = (value >> 4) & 1
        return self._DisitckRvcircMpsA

    @DebugIt()
    def set_DisitckRvcircMpsA(self, DisitckRvcircMpsA):
        self._DisitckRvcircMpsA = DisitckRvcircMpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircMpsB(self):
        value = perseus_utils.read_direct(self.perseus,9, 'B')
        self._DisitckRvcircMpsB = (value >> 4) & 1
        return self._DisitckRvcircMpsB

    @DebugIt()
    def set_DisitckRvcircMpsB(self, DisitckRvcircMpsB):
        self._DisitckRvcircMpsB = DisitckRvcircMpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircDiagA(self):
        value = perseus_utils.read_direct(self.perseus,9, 'A')
        self._DisitckRvcircDiagA = (value >> 5) & 1
        return self._DisitckRvcircDiagA

    @DebugIt()
    def set_DisitckRvcircDiagA(self, DisitckRvcircDiagA):
        self._DisitckRvcircDiagA = DisitckRvcircDiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircDiagB(self):
        value = perseus_utils.read_direct(self.perseus,9, 'B')
        self._DisitckRvcircDiagB = (value >> 5) & 1
        return self._DisitckRvcircDiagB

    @DebugIt()
    def set_DisitckRvcircDiagB(self, DisitckRvcircDiagB):
        self._DisitckRvcircDiagB = DisitckRvcircDiagB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,10, 'A')
        self._DisitckFwloadDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckFwloadDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckFwloadDacsoffloopsstbyA(self, DisitckFwloadDacsoffloopsstbyA):
        self._DisitckFwloadDacsoffloopsstbyA = DisitckFwloadDacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,10, 'B')
        self._DisitckFwloadDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckFwloadDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckFwloadDacsoffloopsstbyB(self, DisitckFwloadDacsoffloopsstbyB):
        self._DisitckFwloadDacsoffloopsstbyB = DisitckFwloadDacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,10, 'A')
        self._DisitckFwloadPindiodeswitchA = (value >> 1) & 1
        return self._DisitckFwloadPindiodeswitchA

    @DebugIt()
    def set_DisitckFwloadPindiodeswitchA(self, DisitckFwloadPindiodeswitchA):
        self._DisitckFwloadPindiodeswitchA = DisitckFwloadPindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,10, 'B')
        self._DisitckFwloadPindiodeswitchB = (value >> 1) & 1
        return self._DisitckFwloadPindiodeswitchB

    @DebugIt()
    def set_DisitckFwloadPindiodeswitchB(self, DisitckFwloadPindiodeswitchB):
        self._DisitckFwloadPindiodeswitchB = DisitckFwloadPindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,10, 'A')
        self._DisitckFwloadFdltrgA = (value >> 2) & 1
        return self._DisitckFwloadFdltrgA

    @DebugIt()
    def set_DisitckFwloadFdltrgA(self, DisitckFwloadFdltrgA):
        self._DisitckFwloadFdltrgA = DisitckFwloadFdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,10, 'B')
        self._DisitckFwloadFdltrgB = (value >> 2) & 1
        return self._DisitckFwloadFdltrgB

    @DebugIt()
    def set_DisitckFwloadFdltrgB(self, DisitckFwloadFdltrgB):
        self._DisitckFwloadFdltrgB = DisitckFwloadFdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,10, 'A')
        self._DisitckFwloadPlctxoffA = (value >> 3) & 1
        return self._DisitckFwloadPlctxoffA

    @DebugIt()
    def set_DisitckFwloadPlctxoffA(self, DisitckFwloadPlctxoffA):
        self._DisitckFwloadPlctxoffA = DisitckFwloadPlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,10, 'B')
        self._DisitckFwloadPlctxoffB = (value >> 3) & 1
        return self._DisitckFwloadPlctxoffB

    @DebugIt()
    def set_DisitckFwloadPlctxoffB(self, DisitckFwloadPlctxoffB):
        self._DisitckFwloadPlctxoffB = DisitckFwloadPlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadMpsA(self):
        value = perseus_utils.read_direct(self.perseus,10, 'A')
        self._DisitckFwloadMpsA = (value >> 4) & 1
        return self._DisitckFwloadMpsA

    @DebugIt()
    def set_DisitckFwloadMpsA(self, DisitckFwloadMpsA):
        self._DisitckFwloadMpsA = DisitckFwloadMpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadMpsB(self):
        value = perseus_utils.read_direct(self.perseus,10, 'B')
        self._DisitckFwloadMpsB = (value >> 4) & 1
        return self._DisitckFwloadMpsB

    @DebugIt()
    def set_DisitckFwloadMpsB(self, DisitckFwloadMpsB):
        self._DisitckFwloadMpsB = DisitckFwloadMpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadDiagA(self):
        value = perseus_utils.read_direct(self.perseus,10, 'A')
        self._DisitckFwloadDiagA = (value >> 5) & 1
        return self._DisitckFwloadDiagA

    @DebugIt()
    def set_DisitckFwloadDiagA(self, DisitckFwloadDiagA):
        self._DisitckFwloadDiagA = DisitckFwloadDiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadDiagB(self):
        value = perseus_utils.read_direct(self.perseus,10, 'B')
        self._DisitckFwloadDiagB = (value >> 5) & 1
        return self._DisitckFwloadDiagB

    @DebugIt()
    def set_DisitckFwloadDiagB(self, DisitckFwloadDiagB):
        self._DisitckFwloadDiagB = DisitckFwloadDiagB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,11, 'A')
        self._DisitckFwhybloadDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckFwhybloadDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckFwhybloadDacsoffloopsstbyA(self, DisitckFwhybloadDacsoffloopsstbyA):
        self._DisitckFwhybloadDacsoffloopsstbyA = DisitckFwhybloadDacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,11, 'B')
        self._DisitckFwhybloadDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckFwhybloadDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckFwhybloadDacsoffloopsstbyB(self, DisitckFwhybloadDacsoffloopsstbyB):
        self._DisitckFwhybloadDacsoffloopsstbyB = DisitckFwhybloadDacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,11, 'A')
        self._DisitckFwhybloadPindiodeswitchA = (value >> 1) & 1
        return self._DisitckFwhybloadPindiodeswitchA

    @DebugIt()
    def set_DisitckFwhybloadPindiodeswitchA(self, DisitckFwhybloadPindiodeswitchA):
        self._DisitckFwhybloadPindiodeswitchA = DisitckFwhybloadPindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,11, 'B')
        self._DisitckFwhybloadPindiodeswitchB = (value >> 1) & 1
        return self._DisitckFwhybloadPindiodeswitchB

    @DebugIt()
    def set_DisitckFwhybloadPindiodeswitchB(self, DisitckFwhybloadPindiodeswitchB):
        self._DisitckFwhybloadPindiodeswitchB = DisitckFwhybloadPindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,11, 'A')
        self._DisitckFwhybloadFdltrgA = (value >> 2) & 1
        return self._DisitckFwhybloadFdltrgA

    @DebugIt()
    def set_DisitckFwhybloadFdltrgA(self, DisitckFwhybloadFdltrgA):
        self._DisitckFwhybloadFdltrgA = DisitckFwhybloadFdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,11, 'B')
        self._DisitckFwhybloadFdltrgB = (value >> 2) & 1
        return self._DisitckFwhybloadFdltrgB

    @DebugIt()
    def set_DisitckFwhybloadFdltrgB(self, DisitckFwhybloadFdltrgB):
        self._DisitckFwhybloadFdltrgB = DisitckFwhybloadFdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,11, 'A')
        self._DisitckFwhybloadPlctxoffA = (value >> 3) & 1
        return self._DisitckFwhybloadPlctxoffA

    @DebugIt()
    def set_DisitckFwhybloadPlctxoffA(self, DisitckFwhybloadPlctxoffA):
        self._DisitckFwhybloadPlctxoffA = DisitckFwhybloadPlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,11, 'B')
        self._DisitckFwhybloadPlctxoffB = (value >> 3) & 1
        return self._DisitckFwhybloadPlctxoffB

    @DebugIt()
    def set_DisitckFwhybloadPlctxoffB(self, DisitckFwhybloadPlctxoffB):
        self._DisitckFwhybloadPlctxoffB = DisitckFwhybloadPlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadMpsA(self):
        value = perseus_utils.read_direct(self.perseus,11, 'A')
        self._DisitckFwhybloadMpsA = (value >> 4) & 1
        return self._DisitckFwhybloadMpsA

    @DebugIt()
    def set_DisitckFwhybloadMpsA(self, DisitckFwhybloadMpsA):
        self._DisitckFwhybloadMpsA = DisitckFwhybloadMpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadMpsB(self):
        value = perseus_utils.read_direct(self.perseus,11, 'B')
        self._DisitckFwhybloadMpsB = (value >> 4) & 1
        return self._DisitckFwhybloadMpsB

    @DebugIt()
    def set_DisitckFwhybloadMpsB(self, DisitckFwhybloadMpsB):
        self._DisitckFwhybloadMpsB = DisitckFwhybloadMpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadDiagA(self):
        value = perseus_utils.read_direct(self.perseus,11, 'A')
        self._DisitckFwhybloadDiagA = (value >> 5) & 1
        return self._DisitckFwhybloadDiagA

    @DebugIt()
    def set_DisitckFwhybloadDiagA(self, DisitckFwhybloadDiagA):
        self._DisitckFwhybloadDiagA = DisitckFwhybloadDiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadDiagB(self):
        value = perseus_utils.read_direct(self.perseus,11, 'B')
        self._DisitckFwhybloadDiagB = (value >> 5) & 1
        return self._DisitckFwhybloadDiagB

    @DebugIt()
    def set_DisitckFwhybloadDiagB(self, DisitckFwhybloadDiagB):
        self._DisitckFwhybloadDiagB = DisitckFwhybloadDiagB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,12, 'A')
        self._DisitckRvcavDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckRvcavDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckRvcavDacsoffloopsstbyA(self, DisitckRvcavDacsoffloopsstbyA):
        self._DisitckRvcavDacsoffloopsstbyA = DisitckRvcavDacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,12, 'B')
        self._DisitckRvcavDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckRvcavDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckRvcavDacsoffloopsstbyB(self, DisitckRvcavDacsoffloopsstbyB):
        self._DisitckRvcavDacsoffloopsstbyB = DisitckRvcavDacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,12, 'A')
        self._DisitckRvcavPindiodeswitchA = (value >> 1) & 1
        return self._DisitckRvcavPindiodeswitchA

    @DebugIt()
    def set_DisitckRvcavPindiodeswitchA(self, DisitckRvcavPindiodeswitchA):
        self._DisitckRvcavPindiodeswitchA = DisitckRvcavPindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,12, 'B')
        self._DisitckRvcavPindiodeswitchB = (value >> 1) & 1
        return self._DisitckRvcavPindiodeswitchB

    @DebugIt()
    def set_DisitckRvcavPindiodeswitchB(self, DisitckRvcavPindiodeswitchB):
        self._DisitckRvcavPindiodeswitchB = DisitckRvcavPindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,12, 'A')
        self._DisitckRvcavFdltrgA = (value >> 2) & 1
        return self._DisitckRvcavFdltrgA

    @DebugIt()
    def set_DisitckRvcavFdltrgA(self, DisitckRvcavFdltrgA):
        self._DisitckRvcavFdltrgA = DisitckRvcavFdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,12, 'B')
        self._DisitckRvcavFdltrgB = (value >> 2) & 1
        return self._DisitckRvcavFdltrgB

    @DebugIt()
    def set_DisitckRvcavFdltrgB(self, DisitckRvcavFdltrgB):
        self._DisitckRvcavFdltrgB = DisitckRvcavFdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,12, 'A')
        self._DisitckRvcavPlctxoffA = (value >> 3) & 1
        return self._DisitckRvcavPlctxoffA

    @DebugIt()
    def set_DisitckRvcavPlctxoffA(self, DisitckRvcavPlctxoffA):
        self._DisitckRvcavPlctxoffA = DisitckRvcavPlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,12, 'B')
        self._DisitckRvcavPlctxoffB = (value >> 3) & 1
        return self._DisitckRvcavPlctxoffB

    @DebugIt()
    def set_DisitckRvcavPlctxoffB(self, DisitckRvcavPlctxoffB):
        self._DisitckRvcavPlctxoffB = DisitckRvcavPlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavMpsA(self):
        value = perseus_utils.read_direct(self.perseus,12, 'A')
        self._DisitckRvcavMpsA = (value >> 4) & 1
        return self._DisitckRvcavMpsA

    @DebugIt()
    def set_DisitckRvcavMpsA(self, DisitckRvcavMpsA):
        self._DisitckRvcavMpsA = DisitckRvcavMpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavMpsB(self):
        value = perseus_utils.read_direct(self.perseus,12, 'B')
        self._DisitckRvcavMpsB = (value >> 4) & 1
        return self._DisitckRvcavMpsB

    @DebugIt()
    def set_DisitckRvcavMpsB(self, DisitckRvcavMpsB):
        self._DisitckRvcavMpsB = DisitckRvcavMpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavDiagA(self):
        value = perseus_utils.read_direct(self.perseus,12, 'A')
        self._DisitckRvcavDiagA = (value >> 5) & 1
        return self._DisitckRvcavDiagA

    @DebugIt()
    def set_DisitckRvcavDiagA(self, DisitckRvcavDiagA):
        self._DisitckRvcavDiagA = DisitckRvcavDiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavDiagB(self):
        value = perseus_utils.read_direct(self.perseus,12, 'B')
        self._DisitckRvcavDiagB = (value >> 5) & 1
        return self._DisitckRvcavDiagB

    @DebugIt()
    def set_DisitckRvcavDiagB(self, DisitckRvcavDiagB):
        self._DisitckRvcavDiagB = DisitckRvcavDiagB
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,13, 'A')
        self._DisitckArcsDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckArcsDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckArcsDacsoffloopsstbyA(self, DisitckArcsDacsoffloopsstbyA):
        self._DisitckArcsDacsoffloopsstbyA = DisitckArcsDacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,13, 'B')
        self._DisitckArcsDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckArcsDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckArcsDacsoffloopsstbyB(self, DisitckArcsDacsoffloopsstbyB):
        self._DisitckArcsDacsoffloopsstbyB = DisitckArcsDacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,13, 'A')
        self._DisitckArcsPindiodeswitchA = (value >> 1) & 1
        return self._DisitckArcsPindiodeswitchA

    @DebugIt()
    def set_DisitckArcsPindiodeswitchA(self, DisitckArcsPindiodeswitchA):
        self._DisitckArcsPindiodeswitchA = DisitckArcsPindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,13, 'B')
        self._DisitckArcsPindiodeswitchB = (value >> 1) & 1
        return self._DisitckArcsPindiodeswitchB

    @DebugIt()
    def set_DisitckArcsPindiodeswitchB(self, DisitckArcsPindiodeswitchB):
        self._DisitckArcsPindiodeswitchB = DisitckArcsPindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,13, 'A')
        self._DisitckArcsFdltrgA = (value >> 2) & 1
        return self._DisitckArcsFdltrgA

    @DebugIt()
    def set_DisitckArcsFdltrgA(self, DisitckArcsFdltrgA):
        self._DisitckArcsFdltrgA = DisitckArcsFdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,13, 'B')
        self._DisitckArcsFdltrgB = (value >> 2) & 1
        return self._DisitckArcsFdltrgB

    @DebugIt()
    def set_DisitckArcsFdltrgB(self, DisitckArcsFdltrgB):
        self._DisitckArcsFdltrgB = DisitckArcsFdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,13, 'A')
        self._DisitckArcsPlctxoffA = (value >> 3) & 1
        return self._DisitckArcsPlctxoffA

    @DebugIt()
    def set_DisitckArcsPlctxoffA(self, DisitckArcsPlctxoffA):
        self._DisitckArcsPlctxoffA = DisitckArcsPlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,13, 'B')
        self._DisitckArcsPlctxoffB = (value >> 3) & 1
        return self._DisitckArcsPlctxoffB

    @DebugIt()
    def set_DisitckArcsPlctxoffB(self, DisitckArcsPlctxoffB):
        self._DisitckArcsPlctxoffB = DisitckArcsPlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsMpsA(self):
        value = perseus_utils.read_direct(self.perseus,13, 'A')
        self._DisitckArcsMpsA = (value >> 4) & 1
        return self._DisitckArcsMpsA

    @DebugIt()
    def set_DisitckArcsMpsA(self, DisitckArcsMpsA):
        self._DisitckArcsMpsA = DisitckArcsMpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsMpsB(self):
        value = perseus_utils.read_direct(self.perseus,13, 'B')
        self._DisitckArcsMpsB = (value >> 4) & 1
        return self._DisitckArcsMpsB

    @DebugIt()
    def set_DisitckArcsMpsB(self, DisitckArcsMpsB):
        self._DisitckArcsMpsB = DisitckArcsMpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsDiagA(self):
        value = perseus_utils.read_direct(self.perseus,13, 'A')
        self._DisitckArcsDiagA = (value >> 5) & 1
        return self._DisitckArcsDiagA

    @DebugIt()
    def set_DisitckArcsDiagA(self, DisitckArcsDiagA):
        self._DisitckArcsDiagA = DisitckArcsDiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsDiagB(self):
        value = perseus_utils.read_direct(self.perseus,13, 'B')
        self._DisitckArcsDiagB = (value >> 5) & 1
        return self._DisitckArcsDiagB

    @DebugIt()
    def set_DisitckArcsDiagB(self, DisitckArcsDiagB):
        self._DisitckArcsDiagB = DisitckArcsDiagB
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,14, 'A')
        self._DisitckVacuumDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckVacuumDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckVacuumDacsoffloopsstbyA(self, DisitckVacuumDacsoffloopsstbyA):
        self._DisitckVacuumDacsoffloopsstbyA = DisitckVacuumDacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,14, 'B')
        self._DisitckVacuumDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckVacuumDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckVacuumDacsoffloopsstbyB(self, DisitckVacuumDacsoffloopsstbyB):
        self._DisitckVacuumDacsoffloopsstbyB = DisitckVacuumDacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,14, 'A')
        self._DisitckVacuumPindiodeswitchA = (value >> 1) & 1
        return self._DisitckVacuumPindiodeswitchA

    @DebugIt()
    def set_DisitckVacuumPindiodeswitchA(self, DisitckVacuumPindiodeswitchA):
        self._DisitckVacuumPindiodeswitchA = DisitckVacuumPindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,14, 'B')
        self._DisitckVacuumPindiodeswitchB = (value >> 1) & 1
        return self._DisitckVacuumPindiodeswitchB

    @DebugIt()
    def set_DisitckVacuumPindiodeswitchB(self, DisitckVacuumPindiodeswitchB):
        self._DisitckVacuumPindiodeswitchB = DisitckVacuumPindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,14, 'A')
        self._DisitckVacuumFdltrgA = (value >> 2) & 1
        return self._DisitckVacuumFdltrgA

    @DebugIt()
    def set_DisitckVacuumFdltrgA(self, DisitckVacuumFdltrgA):
        self._DisitckVacuumFdltrgA = DisitckVacuumFdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,14, 'B')
        self._DisitckVacuumFdltrgB = (value >> 2) & 1
        return self._DisitckVacuumFdltrgB

    @DebugIt()
    def set_DisitckVacuumFdltrgB(self, DisitckVacuumFdltrgB):
        self._DisitckVacuumFdltrgB = DisitckVacuumFdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,14, 'A')
        self._DisitckVacuumPlctxoffA = (value >> 3) & 1
        return self._DisitckVacuumPlctxoffA

    @DebugIt()
    def set_DisitckVacuumPlctxoffA(self, DisitckVacuumPlctxoffA):
        self._DisitckVacuumPlctxoffA = DisitckVacuumPlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,14, 'B')
        self._DisitckVacuumPlctxoffB = (value >> 3) & 1
        return self._DisitckVacuumPlctxoffB

    @DebugIt()
    def set_DisitckVacuumPlctxoffB(self, DisitckVacuumPlctxoffB):
        self._DisitckVacuumPlctxoffB = DisitckVacuumPlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumMpsA(self):
        value = perseus_utils.read_direct(self.perseus,14, 'A')
        self._DisitckVacuumMpsA = (value >> 4) & 1
        return self._DisitckVacuumMpsA

    @DebugIt()
    def set_DisitckVacuumMpsA(self, DisitckVacuumMpsA):
        self._DisitckVacuumMpsA = DisitckVacuumMpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumMpsB(self):
        value = perseus_utils.read_direct(self.perseus,14, 'B')
        self._DisitckVacuumMpsB = (value >> 4) & 1
        return self._DisitckVacuumMpsB

    @DebugIt()
    def set_DisitckVacuumMpsB(self, DisitckVacuumMpsB):
        self._DisitckVacuumMpsB = DisitckVacuumMpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumDiagA(self):
        value = perseus_utils.read_direct(self.perseus,14, 'A')
        self._DisitckVacuumDiagA = (value >> 5) & 1
        return self._DisitckVacuumDiagA

    @DebugIt()
    def set_DisitckVacuumDiagA(self, DisitckVacuumDiagA):
        self._DisitckVacuumDiagA = DisitckVacuumDiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumDiagB(self):
        value = perseus_utils.read_direct(self.perseus,14, 'B')
        self._DisitckVacuumDiagB = (value >> 5) & 1
        return self._DisitckVacuumDiagB

    @DebugIt()
    def set_DisitckVacuumDiagB(self, DisitckVacuumDiagB):
        self._DisitckVacuumDiagB = DisitckVacuumDiagB
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,15, 'A')
        self._DisitckManualInterlockDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckManualInterlockDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckManualInterlockDacsoffloopsstbyA(self, DisitckManualInterlockDacsoffloopsstbyA):
        self._DisitckManualInterlockDacsoffloopsstbyA = DisitckManualInterlockDacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,15, 'B')
        self._DisitckManualInterlockDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckManualInterlockDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckManualInterlockDacsoffloopsstbyB(self, DisitckManualInterlockDacsoffloopsstbyB):
        self._DisitckManualInterlockDacsoffloopsstbyB = DisitckManualInterlockDacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,15, 'A')
        self._DisitckManualInterlockPindiodeswitchA = (value >> 1) & 1
        return self._DisitckManualInterlockPindiodeswitchA

    @DebugIt()
    def set_DisitckManualInterlockPindiodeswitchA(self, DisitckManualInterlockPindiodeswitchA):
        self._DisitckManualInterlockPindiodeswitchA = DisitckManualInterlockPindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,15, 'B')
        self._DisitckManualInterlockPindiodeswitchB = (value >> 1) & 1
        return self._DisitckManualInterlockPindiodeswitchB

    @DebugIt()
    def set_DisitckManualInterlockPindiodeswitchB(self, DisitckManualInterlockPindiodeswitchB):
        self._DisitckManualInterlockPindiodeswitchB = DisitckManualInterlockPindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,15, 'A')
        self._DisitckManualInterlockFdltrgA = (value >> 2) & 1
        return self._DisitckManualInterlockFdltrgA

    @DebugIt()
    def set_DisitckManualInterlockFdltrgA(self, DisitckManualInterlockFdltrgA):
        self._DisitckManualInterlockFdltrgA = DisitckManualInterlockFdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,15, 'B')
        self._DisitckManualInterlockFdltrgB = (value >> 2) & 1
        return self._DisitckManualInterlockFdltrgB

    @DebugIt()
    def set_DisitckManualInterlockFdltrgB(self, DisitckManualInterlockFdltrgB):
        self._DisitckManualInterlockFdltrgB = DisitckManualInterlockFdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,15, 'A')
        self._DisitckManualInterlockPlctxoffA = (value >> 3) & 1
        return self._DisitckManualInterlockPlctxoffA

    @DebugIt()
    def set_DisitckManualInterlockPlctxoffA(self, DisitckManualInterlockPlctxoffA):
        self._DisitckManualInterlockPlctxoffA = DisitckManualInterlockPlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,15, 'B')
        self._DisitckManualInterlockPlctxoffB = (value >> 3) & 1
        return self._DisitckManualInterlockPlctxoffB

    @DebugIt()
    def set_DisitckManualInterlockPlctxoffB(self, DisitckManualInterlockPlctxoffB):
        self._DisitckManualInterlockPlctxoffB = DisitckManualInterlockPlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockMpsA(self):
        value = perseus_utils.read_direct(self.perseus,15, 'A')
        self._DisitckManualInterlockMpsA = (value >> 4) & 1
        return self._DisitckManualInterlockMpsA

    @DebugIt()
    def set_DisitckManualInterlockMpsA(self, DisitckManualInterlockMpsA):
        self._DisitckManualInterlockMpsA = DisitckManualInterlockMpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockMpsB(self):
        value = perseus_utils.read_direct(self.perseus,15, 'B')
        self._DisitckManualInterlockMpsB = (value >> 4) & 1
        return self._DisitckManualInterlockMpsB

    @DebugIt()
    def set_DisitckManualInterlockMpsB(self, DisitckManualInterlockMpsB):
        self._DisitckManualInterlockMpsB = DisitckManualInterlockMpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockDiagA(self):
        value = perseus_utils.read_direct(self.perseus,15, 'A')
        self._DisitckManualInterlockDiagA = (value >> 5) & 1
        return self._DisitckManualInterlockDiagA

    @DebugIt()
    def set_DisitckManualInterlockDiagA(self, DisitckManualInterlockDiagA):
        self._DisitckManualInterlockDiagA = DisitckManualInterlockDiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockDiagB(self):
        value = perseus_utils.read_direct(self.perseus,15, 'B')
        self._DisitckManualInterlockDiagB = (value >> 5) & 1
        return self._DisitckManualInterlockDiagB

    @DebugIt()
    def set_DisitckManualInterlockDiagB(self, DisitckManualInterlockDiagB):
        self._DisitckManualInterlockDiagB = DisitckManualInterlockDiagB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,16, 'A')
        self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpDacsoffloopsstbyA(self, DisitckPlungerEndSwitchesUpDacsoffloopsstbyA):
        self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyA = DisitckPlungerEndSwitchesUpDacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,16, 'B')
        self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpDacsoffloopsstbyB(self, DisitckPlungerEndSwitchesUpDacsoffloopsstbyB):
        self._DisitckPlungerEndSwitchesUpDacsoffloopsstbyB = DisitckPlungerEndSwitchesUpDacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,16, 'A')
        self._DisitckPlungerEndSwitchesUpPindiodeswitchA = (value >> 1) & 1
        return self._DisitckPlungerEndSwitchesUpPindiodeswitchA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpPindiodeswitchA(self, DisitckPlungerEndSwitchesUpPindiodeswitchA):
        self._DisitckPlungerEndSwitchesUpPindiodeswitchA = DisitckPlungerEndSwitchesUpPindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,16, 'B')
        self._DisitckPlungerEndSwitchesUpPindiodeswitchB = (value >> 1) & 1
        return self._DisitckPlungerEndSwitchesUpPindiodeswitchB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpPindiodeswitchB(self, DisitckPlungerEndSwitchesUpPindiodeswitchB):
        self._DisitckPlungerEndSwitchesUpPindiodeswitchB = DisitckPlungerEndSwitchesUpPindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,16, 'A')
        self._DisitckPlungerEndSwitchesUpFdltrgA = (value >> 2) & 1
        return self._DisitckPlungerEndSwitchesUpFdltrgA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpFdltrgA(self, DisitckPlungerEndSwitchesUpFdltrgA):
        self._DisitckPlungerEndSwitchesUpFdltrgA = DisitckPlungerEndSwitchesUpFdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,16, 'B')
        self._DisitckPlungerEndSwitchesUpFdltrgB = (value >> 2) & 1
        return self._DisitckPlungerEndSwitchesUpFdltrgB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpFdltrgB(self, DisitckPlungerEndSwitchesUpFdltrgB):
        self._DisitckPlungerEndSwitchesUpFdltrgB = DisitckPlungerEndSwitchesUpFdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,16, 'A')
        self._DisitckPlungerEndSwitchesUpPlctxoffA = (value >> 3) & 1
        return self._DisitckPlungerEndSwitchesUpPlctxoffA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpPlctxoffA(self, DisitckPlungerEndSwitchesUpPlctxoffA):
        self._DisitckPlungerEndSwitchesUpPlctxoffA = DisitckPlungerEndSwitchesUpPlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,16, 'B')
        self._DisitckPlungerEndSwitchesUpPlctxoffB = (value >> 3) & 1
        return self._DisitckPlungerEndSwitchesUpPlctxoffB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpPlctxoffB(self, DisitckPlungerEndSwitchesUpPlctxoffB):
        self._DisitckPlungerEndSwitchesUpPlctxoffB = DisitckPlungerEndSwitchesUpPlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpMpsA(self):
        value = perseus_utils.read_direct(self.perseus,16, 'A')
        self._DisitckPlungerEndSwitchesUpMpsA = (value >> 4) & 1
        return self._DisitckPlungerEndSwitchesUpMpsA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpMpsA(self, DisitckPlungerEndSwitchesUpMpsA):
        self._DisitckPlungerEndSwitchesUpMpsA = DisitckPlungerEndSwitchesUpMpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpMpsB(self):
        value = perseus_utils.read_direct(self.perseus,16, 'B')
        self._DisitckPlungerEndSwitchesUpMpsB = (value >> 4) & 1
        return self._DisitckPlungerEndSwitchesUpMpsB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpMpsB(self, DisitckPlungerEndSwitchesUpMpsB):
        self._DisitckPlungerEndSwitchesUpMpsB = DisitckPlungerEndSwitchesUpMpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpDiagA(self):
        value = perseus_utils.read_direct(self.perseus,16, 'A')
        self._DisitckPlungerEndSwitchesUpDiagA = (value >> 5) & 1
        return self._DisitckPlungerEndSwitchesUpDiagA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpDiagA(self, DisitckPlungerEndSwitchesUpDiagA):
        self._DisitckPlungerEndSwitchesUpDiagA = DisitckPlungerEndSwitchesUpDiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpDiagB(self):
        value = perseus_utils.read_direct(self.perseus,16, 'B')
        self._DisitckPlungerEndSwitchesUpDiagB = (value >> 5) & 1
        return self._DisitckPlungerEndSwitchesUpDiagB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpDiagB(self, DisitckPlungerEndSwitchesUpDiagB):
        self._DisitckPlungerEndSwitchesUpDiagB = DisitckPlungerEndSwitchesUpDiagB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,17, 'A')
        self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownDacsoffloopsstbyA(self, DisitckPlungerEndSwitchesDownDacsoffloopsstbyA):
        self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyA = DisitckPlungerEndSwitchesDownDacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,17, 'B')
        self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownDacsoffloopsstbyB(self, DisitckPlungerEndSwitchesDownDacsoffloopsstbyB):
        self._DisitckPlungerEndSwitchesDownDacsoffloopsstbyB = DisitckPlungerEndSwitchesDownDacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,17, 'A')
        self._DisitckPlungerEndSwitchesDownPindiodeswitchA = (value >> 1) & 1
        return self._DisitckPlungerEndSwitchesDownPindiodeswitchA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownPindiodeswitchA(self, DisitckPlungerEndSwitchesDownPindiodeswitchA):
        self._DisitckPlungerEndSwitchesDownPindiodeswitchA = DisitckPlungerEndSwitchesDownPindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,17, 'B')
        self._DisitckPlungerEndSwitchesDownPindiodeswitchB = (value >> 1) & 1
        return self._DisitckPlungerEndSwitchesDownPindiodeswitchB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownPindiodeswitchB(self, DisitckPlungerEndSwitchesDownPindiodeswitchB):
        self._DisitckPlungerEndSwitchesDownPindiodeswitchB = DisitckPlungerEndSwitchesDownPindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,17, 'A')
        self._DisitckPlungerEndSwitchesDownFdltrgA = (value >> 2) & 1
        return self._DisitckPlungerEndSwitchesDownFdltrgA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownFdltrgA(self, DisitckPlungerEndSwitchesDownFdltrgA):
        self._DisitckPlungerEndSwitchesDownFdltrgA = DisitckPlungerEndSwitchesDownFdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,17, 'B')
        self._DisitckPlungerEndSwitchesDownFdltrgB = (value >> 2) & 1
        return self._DisitckPlungerEndSwitchesDownFdltrgB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownFdltrgB(self, DisitckPlungerEndSwitchesDownFdltrgB):
        self._DisitckPlungerEndSwitchesDownFdltrgB = DisitckPlungerEndSwitchesDownFdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,17, 'A')
        self._DisitckPlungerEndSwitchesDownPlctxoffA = (value >> 3) & 1
        return self._DisitckPlungerEndSwitchesDownPlctxoffA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownPlctxoffA(self, DisitckPlungerEndSwitchesDownPlctxoffA):
        self._DisitckPlungerEndSwitchesDownPlctxoffA = DisitckPlungerEndSwitchesDownPlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,17, 'B')
        self._DisitckPlungerEndSwitchesDownPlctxoffB = (value >> 3) & 1
        return self._DisitckPlungerEndSwitchesDownPlctxoffB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownPlctxoffB(self, DisitckPlungerEndSwitchesDownPlctxoffB):
        self._DisitckPlungerEndSwitchesDownPlctxoffB = DisitckPlungerEndSwitchesDownPlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownMpsA(self):
        value = perseus_utils.read_direct(self.perseus,17, 'A')
        self._DisitckPlungerEndSwitchesDownMpsA = (value >> 4) & 1
        return self._DisitckPlungerEndSwitchesDownMpsA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownMpsA(self, DisitckPlungerEndSwitchesDownMpsA):
        self._DisitckPlungerEndSwitchesDownMpsA = DisitckPlungerEndSwitchesDownMpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownMpsB(self):
        value = perseus_utils.read_direct(self.perseus,17, 'B')
        self._DisitckPlungerEndSwitchesDownMpsB = (value >> 4) & 1
        return self._DisitckPlungerEndSwitchesDownMpsB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownMpsB(self, DisitckPlungerEndSwitchesDownMpsB):
        self._DisitckPlungerEndSwitchesDownMpsB = DisitckPlungerEndSwitchesDownMpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownDiagA(self):
        value = perseus_utils.read_direct(self.perseus,17, 'A')
        self._DisitckPlungerEndSwitchesDownDiagA = (value >> 5) & 1
        return self._DisitckPlungerEndSwitchesDownDiagA

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownDiagA(self, DisitckPlungerEndSwitchesDownDiagA):
        self._DisitckPlungerEndSwitchesDownDiagA = DisitckPlungerEndSwitchesDownDiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownDiagB(self):
        value = perseus_utils.read_direct(self.perseus,17, 'B')
        self._DisitckPlungerEndSwitchesDownDiagB = (value >> 5) & 1
        return self._DisitckPlungerEndSwitchesDownDiagB

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownDiagB(self, DisitckPlungerEndSwitchesDownDiagB):
        self._DisitckPlungerEndSwitchesDownDiagB = DisitckPlungerEndSwitchesDownDiagB
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsDacsoffloopsstbyA(self):
        value = perseus_utils.read_direct(self.perseus,18, 'A')
        self._DisitckMpsDacsoffloopsstbyA = (value >> 0) & 1
        return self._DisitckMpsDacsoffloopsstbyA

    @DebugIt()
    def set_DisitckMpsDacsoffloopsstbyA(self, DisitckMpsDacsoffloopsstbyA):
        self._DisitckMpsDacsoffloopsstbyA = DisitckMpsDacsoffloopsstbyA
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsDacsoffloopsstbyB(self):
        value = perseus_utils.read_direct(self.perseus,18, 'B')
        self._DisitckMpsDacsoffloopsstbyB = (value >> 0) & 1
        return self._DisitckMpsDacsoffloopsstbyB

    @DebugIt()
    def set_DisitckMpsDacsoffloopsstbyB(self, DisitckMpsDacsoffloopsstbyB):
        self._DisitckMpsDacsoffloopsstbyB = DisitckMpsDacsoffloopsstbyB
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsPindiodeswitchA(self):
        value = perseus_utils.read_direct(self.perseus,18, 'A')
        self._DisitckMpsPindiodeswitchA = (value >> 1) & 1
        return self._DisitckMpsPindiodeswitchA

    @DebugIt()
    def set_DisitckMpsPindiodeswitchA(self, DisitckMpsPindiodeswitchA):
        self._DisitckMpsPindiodeswitchA = DisitckMpsPindiodeswitchA
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsPindiodeswitchB(self):
        value = perseus_utils.read_direct(self.perseus,18, 'B')
        self._DisitckMpsPindiodeswitchB = (value >> 1) & 1
        return self._DisitckMpsPindiodeswitchB

    @DebugIt()
    def set_DisitckMpsPindiodeswitchB(self, DisitckMpsPindiodeswitchB):
        self._DisitckMpsPindiodeswitchB = DisitckMpsPindiodeswitchB
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsFdltrgA(self):
        value = perseus_utils.read_direct(self.perseus,18, 'A')
        self._DisitckMpsFdltrgA = (value >> 2) & 1
        return self._DisitckMpsFdltrgA

    @DebugIt()
    def set_DisitckMpsFdltrgA(self, DisitckMpsFdltrgA):
        self._DisitckMpsFdltrgA = DisitckMpsFdltrgA
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsFdltrgB(self):
        value = perseus_utils.read_direct(self.perseus,18, 'B')
        self._DisitckMpsFdltrgB = (value >> 2) & 1
        return self._DisitckMpsFdltrgB

    @DebugIt()
    def set_DisitckMpsFdltrgB(self, DisitckMpsFdltrgB):
        self._DisitckMpsFdltrgB = DisitckMpsFdltrgB
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsPlctxoffA(self):
        value = perseus_utils.read_direct(self.perseus,18, 'A')
        self._DisitckMpsPlctxoffA = (value >> 3) & 1
        return self._DisitckMpsPlctxoffA

    @DebugIt()
    def set_DisitckMpsPlctxoffA(self, DisitckMpsPlctxoffA):
        self._DisitckMpsPlctxoffA = DisitckMpsPlctxoffA
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsPlctxoffB(self):
        value = perseus_utils.read_direct(self.perseus,18, 'B')
        self._DisitckMpsPlctxoffB = (value >> 3) & 1
        return self._DisitckMpsPlctxoffB

    @DebugIt()
    def set_DisitckMpsPlctxoffB(self, DisitckMpsPlctxoffB):
        self._DisitckMpsPlctxoffB = DisitckMpsPlctxoffB
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsMpsA(self):
        value = perseus_utils.read_direct(self.perseus,18, 'A')
        self._DisitckMpsMpsA = (value >> 4) & 1
        return self._DisitckMpsMpsA

    @DebugIt()
    def set_DisitckMpsMpsA(self, DisitckMpsMpsA):
        self._DisitckMpsMpsA = DisitckMpsMpsA
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsMpsB(self):
        value = perseus_utils.read_direct(self.perseus,18, 'B')
        self._DisitckMpsMpsB = (value >> 4) & 1
        return self._DisitckMpsMpsB

    @DebugIt()
    def set_DisitckMpsMpsB(self, DisitckMpsMpsB):
        self._DisitckMpsMpsB = DisitckMpsMpsB
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsDiagA(self):
        value = perseus_utils.read_direct(self.perseus,18, 'A')
        self._DisitckMpsDiagA = (value >> 5) & 1
        return self._DisitckMpsDiagA

    @DebugIt()
    def set_DisitckMpsDiagA(self, DisitckMpsDiagA):
        self._DisitckMpsDiagA = DisitckMpsDiagA
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsDiagB(self):
        value = perseus_utils.read_direct(self.perseus,18, 'B')
        self._DisitckMpsDiagB = (value >> 5) & 1
        return self._DisitckMpsDiagB

    @DebugIt()
    def set_DisitckMpsDiagB(self, DisitckMpsDiagB):
        self._DisitckMpsDiagB = DisitckMpsDiagB
        self.update_fim()

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
        return self._Diag_Timestamp1A

    @DebugIt()
    def read_Diag_Timestamp1B(self):
        return self._Diag_Timestamp1B

    @DebugIt()
    def read_Diag_Timestamp2A(self):
        return self._Diag_Timestamp2A

    @DebugIt()
    def read_Diag_Timestamp2B(self):
        return self._Diag_Timestamp2B

    @DebugIt()
    def read_Diag_Timestamp3A(self):
        return self._Diag_Timestamp3A

    @DebugIt()
    def read_Diag_Timestamp3B(self):
        return self._Diag_Timestamp3B

    @DebugIt()
    def read_Diag_Timestamp4A(self):
        return self._Diag_Timestamp4A

    @DebugIt()
    def read_Diag_Timestamp4B(self):
        return self._Diag_Timestamp4B

    @DebugIt()
    def read_Diag_Timestamp5A(self):
        return self._Diag_Timestamp5A

    @DebugIt()
    def read_Diag_Timestamp5B(self):
        return self._Diag_Timestamp5B

    @DebugIt()
    def read_Diag_Timestamp6A(self):
        return self._Diag_Timestamp6A

    @DebugIt()
    def read_Diag_Timestamp6B(self):
        return self._Diag_Timestamp6B

    @DebugIt()
    def read_Diag_Timestamp7A(self):
        return self._Diag_Timestamp7A

    @DebugIt()
    def read_Diag_Timestamp7B(self):
        return self._Diag_Timestamp7B

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
        perseus_utils.start_reading_diagnostics(self.perseus)

        self._Diag_Irvtet1A = perseus_utils.read_diag_milivolts(self.perseus, 0, 'A')
        self._Diag_Irvtet1B = perseus_utils.read_diag_milivolts(self.perseus, 0, 'B')
        self._Diag_Qrvtet1A = perseus_utils.read_diag_milivolts(self.perseus, 1, 'A')
        self._Diag_Qrvtet1B = perseus_utils.read_diag_milivolts(self.perseus, 1, 'B')
        self._Diag_Amprvtet1A = perseus_utils.read_diag_milivolts(self.perseus, 2, 'A')
        self._Diag_Amprvtet1B = perseus_utils.read_diag_milivolts(self.perseus, 2, 'B')
        self._Diag_Phrvtet1A = perseus_utils.read_diag_angle(self.perseus, 3, 'A')
        self._Diag_Phrvtet1B = perseus_utils.read_diag_angle(self.perseus, 3, 'B')
        self._Diag_Irvtet2A = perseus_utils.read_diag_milivolts(self.perseus, 4, 'A')
        self._Diag_Irvtet2B = perseus_utils.read_diag_milivolts(self.perseus, 4, 'B')
        self._Diag_Qrvtet2A = perseus_utils.read_diag_milivolts(self.perseus, 5, 'A')
        self._Diag_Qrvtet2B = perseus_utils.read_diag_milivolts(self.perseus, 5, 'B')
        self._Diag_Amprvtet2A = perseus_utils.read_diag_milivolts(self.perseus, 6, 'A')
        self._Diag_Amprvtet2B = perseus_utils.read_diag_milivolts(self.perseus, 6, 'B')
        self._Diag_Phrvtet2A = perseus_utils.read_diag_angle(self.perseus, 7, 'A')
        self._Diag_Phrvtet2B = perseus_utils.read_diag_angle(self.perseus, 7, 'B')
        self._Diag_IfwcircA = perseus_utils.read_diag_milivolts(self.perseus, 8, 'A')
        self._Diag_IfwcircB = perseus_utils.read_diag_milivolts(self.perseus, 8, 'B')
        self._Diag_QfwcircA = perseus_utils.read_diag_milivolts(self.perseus, 9, 'A')
        self._Diag_QfwcircB = perseus_utils.read_diag_milivolts(self.perseus, 9, 'B')
        self._Diag_AmpfwcircA = perseus_utils.read_diag_milivolts(self.perseus, 10, 'A')
        self._Diag_AmpfwcircB = perseus_utils.read_diag_milivolts(self.perseus, 10, 'B')
        self._Diag_PhfwcircA = perseus_utils.read_diag_angle(self.perseus, 11, 'A')
        self._Diag_PhfwcircB = perseus_utils.read_diag_angle(self.perseus, 11, 'B')
        self._Diag_IrvcircA = perseus_utils.read_diag_milivolts(self.perseus, 12, 'A')
        self._Diag_IrvcircB = perseus_utils.read_diag_milivolts(self.perseus, 12, 'B')
        self._Diag_QrvcircA = perseus_utils.read_diag_milivolts(self.perseus, 13, 'A')
        self._Diag_QrvcircB = perseus_utils.read_diag_milivolts(self.perseus, 13, 'B')
        self._Diag_AmprvcircA = perseus_utils.read_diag_milivolts(self.perseus, 14, 'A')
        self._Diag_AmprvcircB = perseus_utils.read_diag_milivolts(self.perseus, 14, 'B')
        self._Diag_PhrvcircA = perseus_utils.read_diag_angle(self.perseus, 15, 'A')
        self._Diag_PhrvcircB = perseus_utils.read_diag_angle(self.perseus, 15, 'B')
        self._Diag_IfwloadA = perseus_utils.read_diag_milivolts(self.perseus, 16, 'A')
        self._Diag_IfwloadB = perseus_utils.read_diag_milivolts(self.perseus, 16, 'B')
        self._Diag_QfwloadA = perseus_utils.read_diag_milivolts(self.perseus, 17, 'A')
        self._Diag_QfwloadB = perseus_utils.read_diag_milivolts(self.perseus, 17, 'B')
        self._Diag_AmpfwloadA = perseus_utils.read_diag_milivolts(self.perseus, 18, 'A')
        self._Diag_AmpfwloadB = perseus_utils.read_diag_milivolts(self.perseus, 18, 'B')
        self._Diag_PhfwloadA = perseus_utils.read_diag_angle(self.perseus, 19, 'A')
        self._Diag_PhfwloadB = perseus_utils.read_diag_angle(self.perseus, 19, 'B')
        self._Diag_IfwhybloadA = perseus_utils.read_diag_milivolts(self.perseus, 20, 'A')
        self._Diag_IfwhybloadB = perseus_utils.read_diag_milivolts(self.perseus, 20, 'B')
        self._Diag_QfwhybloadA = perseus_utils.read_diag_milivolts(self.perseus, 21, 'A')
        self._Diag_QfwhybloadB = perseus_utils.read_diag_milivolts(self.perseus, 21, 'B')
        self._Diag_AmpfwhybloadA = perseus_utils.read_diag_milivolts(self.perseus, 22, 'A')
        self._Diag_AmpfwhybloadB = perseus_utils.read_diag_milivolts(self.perseus, 22, 'B')
        self._Diag_PhfwhybloadA = perseus_utils.read_diag_angle(self.perseus, 23, 'A')
        self._Diag_PhfwhybloadB = perseus_utils.read_diag_angle(self.perseus, 23, 'B')
        self._Diag_IrvcavA = perseus_utils.read_diag_milivolts(self.perseus, 24, 'A')
        self._Diag_IrvcavB = perseus_utils.read_diag_milivolts(self.perseus, 24, 'B')
        self._Diag_QrvcavA = perseus_utils.read_diag_milivolts(self.perseus, 25, 'A')
        self._Diag_QrvcavB = perseus_utils.read_diag_milivolts(self.perseus, 25, 'B')
        self._Diag_AmprvcavA = perseus_utils.read_diag_milivolts(self.perseus, 26, 'A')
        self._Diag_AmprvcavB = perseus_utils.read_diag_milivolts(self.perseus, 26, 'B')
        self._Diag_PhrvcavA = perseus_utils.read_diag_angle(self.perseus, 27, 'A')
        self._Diag_PhrvcavB = perseus_utils.read_diag_angle(self.perseus, 27, 'B')
        self._Diag_ImoA = perseus_utils.read_diag_milivolts(self.perseus, 28, 'A')
        self._Diag_ImoB = perseus_utils.read_diag_milivolts(self.perseus, 28, 'B')
        self._Diag_QmoA = perseus_utils.read_diag_milivolts(self.perseus, 29, 'A')
        self._Diag_QmoB = perseus_utils.read_diag_milivolts(self.perseus, 29, 'B')
        self._Diag_AmpmoA = perseus_utils.read_diag_milivolts(self.perseus, 30, 'A')
        self._Diag_AmpmoB = perseus_utils.read_diag_milivolts(self.perseus, 30, 'B')
        self._Diag_PhmoA = perseus_utils.read_diag_angle(self.perseus, 31, 'A')
        self._Diag_PhmoB = perseus_utils.read_diag_angle(self.perseus, 31, 'B')
        self._Diag_IlandauA = perseus_utils.read_diag_milivolts(self.perseus, 32, 'A')
        self._Diag_IlandauB = perseus_utils.read_diag_milivolts(self.perseus, 32, 'B')
        self._Diag_QlandauA = perseus_utils.read_diag_milivolts(self.perseus, 33, 'A')
        self._Diag_QlandauB = perseus_utils.read_diag_milivolts(self.perseus, 33, 'B')
        self._Diag_AmplandauA = perseus_utils.read_diag_milivolts(self.perseus, 34, 'A')
        self._Diag_AmplandauB = perseus_utils.read_diag_milivolts(self.perseus, 34, 'B')
        self._Diag_PhlandauA = perseus_utils.read_diag_angle(self.perseus, 35, 'A')
        self._Diag_PhlandauB = perseus_utils.read_diag_angle(self.perseus, 35, 'B')
        self._Diag_PlungerMovingManualTuningA = bool(perseus_utils.read_diag_direct(self.perseus, 60, 'A'))
        self._Diag_PlungerMovingManualTuningB = bool(perseus_utils.read_diag_direct(self.perseus, 60, 'B'))
        self._Diag_PlungerMovingUpManualTuningA = bool(perseus_utils.read_diag_direct(self.perseus, 61, 'A'))
        self._Diag_PlungerMovingUpManualTuningB = bool(perseus_utils.read_diag_direct(self.perseus, 61, 'B'))
        self._Diag_PlungerMovingAutomaticTuningA = bool(perseus_utils.read_diag_direct(self.perseus, 62, 'A'))
        self._Diag_PlungerMovingAutomaticTuningB = bool(perseus_utils.read_diag_direct(self.perseus, 62, 'B'))
        self._Diag_PlungerMovingUpAutomaticTuningA = bool(perseus_utils.read_diag_direct(self.perseus, 63, 'A'))
        self._Diag_PlungerMovingUpAutomaticTuningB = bool(perseus_utils.read_diag_direct(self.perseus, 63, 'B'))
        self._Diag_DephaseMoLandauA = perseus_utils.read_diag_angle(self.perseus, 64, 'A')
        self._Diag_DephaseMoLandauB = perseus_utils.read_diag_angle(self.perseus, 64, 'B')
        self._Diag_AmpRvtet1b = math.sqrt((self._Diag_Irvtet1B**2) + (self._Diag_Qrvtet1B**2))
        self._Diag_AmpRvtet1a = math.sqrt((self._Diag_Irvtet1A**2) + (self._Diag_Qrvtet1A**2))
        self._Diag_AmpMoa = math.sqrt((self._Diag_ImoA**2) + (self._Diag_QmoA**2))
        self._Diag_AmpLandaua = math.sqrt((self._Diag_IlandauA**2) + (self._Diag_QlandauA**2))
        self._Diag_AmpFwloada = math.sqrt((self._Diag_IfwloadA**2) + (self._Diag_QfwloadA**2))
        self._Diag_AmpRvtet2b = math.sqrt((self._Diag_Irvtet2B**2) + (self._Diag_Qrvtet2B**2))
        self._Diag_AmpRvtet2a = math.sqrt((self._Diag_Irvtet2A**2) + (self._Diag_Qrvtet2A**2))
        self._Diag_AmpFwloadb = math.sqrt((self._Diag_IfwloadB**2) + (self._Diag_QfwloadB**2))
        self._Diag_AmpRvcavb = math.sqrt((self._Diag_IrvcavB**2) + (self._Diag_QrvcavB**2))
        self._Diag_AmpRvcava = math.sqrt((self._Diag_IrvcavA**2) + (self._Diag_QrvcavA**2))
        self._Diag_AmpFwcircb = math.sqrt((self._Diag_IfwcircB**2) + (self._Diag_QfwcircB**2))
        self._Diag_AmpFwcirca = math.sqrt((self._Diag_IfwcircA**2) + (self._Diag_QfwcircA**2))
        self._Diag_AmpMob = math.sqrt((self._Diag_ImoB**2) + (self._Diag_QmoB**2))
        self._Diag_AmpRvcirca = math.sqrt((self._Diag_IrvcircA**2) + (self._Diag_QrvcircA**2))
        self._Diag_AmpRvcircb = math.sqrt((self._Diag_IrvcircB**2) + (self._Diag_QrvcircB**2))
        self._Diag_AmpFwhybloadb = math.sqrt((self._Diag_IfwhybloadB**2) + (self._Diag_QfwhybloadB**2))
        self._Diag_AmpFwhybloada = math.sqrt((self._Diag_IfwhybloadA**2) + (self._Diag_QfwhybloadA**2))
        self._Diag_AmpLandaub = math.sqrt((self._Diag_IlandauB**2) + (self._Diag_QlandauB**2))
        self._Diag_PhRvtet1b = math.degrees(math.atan2(self._Diag_Qrvtet1B, self._Diag_Irvtet1B))
        self._Diag_PhRvtet1a = math.degrees(math.atan2(self._Diag_Qrvtet1A, self._Diag_Irvtet1A))
        self._Diag_PhMoa = math.degrees(math.atan2(self._Diag_QmoA, self._Diag_ImoA))
        self._Diag_PhLandaua = math.degrees(math.atan2(self._Diag_QlandauA, self._Diag_IlandauA))
        self._Diag_PhFwloada = math.degrees(math.atan2(self._Diag_QfwloadA, self._Diag_IfwloadA))
        self._Diag_PhRvtet2b = math.degrees(math.atan2(self._Diag_Qrvtet2B, self._Diag_Irvtet2B))
        self._Diag_PhRvtet2a = math.degrees(math.atan2(self._Diag_Qrvtet2A, self._Diag_Irvtet2A))
        self._Diag_PhFwloadb = math.degrees(math.atan2(self._Diag_QfwloadB, self._Diag_IfwloadB))
        self._Diag_PhRvcavb = math.degrees(math.atan2(self._Diag_QrvcavB, self._Diag_IrvcavB))
        self._Diag_PhRvcava = math.degrees(math.atan2(self._Diag_QrvcavA, self._Diag_IrvcavA))
        self._Diag_PhFwcircb = math.degrees(math.atan2(self._Diag_QfwcircB, self._Diag_IfwcircB))
        self._Diag_PhFwcirca = math.degrees(math.atan2(self._Diag_QfwcircA, self._Diag_IfwcircA))
        self._Diag_PhMob = math.degrees(math.atan2(self._Diag_QmoB, self._Diag_ImoB))
        self._Diag_PhRvcirca = math.degrees(math.atan2(self._Diag_QrvcircA, self._Diag_IrvcircA))
        self._Diag_PhRvcircb = math.degrees(math.atan2(self._Diag_QrvcircB, self._Diag_IrvcircB))
        self._Diag_PhFwhybloadb = math.degrees(math.atan2(self._Diag_QfwhybloadB, self._Diag_IfwhybloadB))
        self._Diag_PhFwhybloada = math.degrees(math.atan2(self._Diag_QfwhybloadA, self._Diag_IfwhybloadA))
        self._Diag_PhLandaub = math.degrees(math.atan2(self._Diag_QlandauB, self._Diag_IlandauB))

    @command
    def tuning_reset(self):
        perseus_utils.write_direct(self.perseus, True, DIAG_TUNING_RESET_ADDRESS)
        perseus_utils.write_direct(self.perseus, False, DIAG_TUNING_RESET_ADDRESS)

    @command
    def reset_manual_itck(self):
        perseus_utils.write_direct(self.perseus, True, RESET_MANUAL_ITCK_ADDRESS)
        perseus_utils.write_direct(self.perseus, False, RESET_MANUAL_ITCK_ADDRESS)

    @command
    def reset_itck(self):
        perseus_utils.write_direct(self.perseus, True, RESET_ITCK_ADDRESS)
        perseus_utils.write_direct(self.perseus, False, RESET_ITCK_ADDRESS)


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

    def update_fim(self):
        self.update_RvTet1()
        self.update_RvTet2()
        self.update_RvCircIn()
        self.update_FwLoad()
        self.update_FwHybLoad()
        self.update_RvCav()
        self.update_Arc()
        self.update_Vacuum()
        self.update_Manual()
        self.update_EndSwUp()
        self.update_EndSwDown()
        self.update_Mps()

    def update_RvTet1(self):
        bit0=self._DisitckRvtet1Dacsoffloopsstby
        bit1=self._DisitckRvtet1Pindiodeswitch
        bit2=self._DisitckRvtet1Fdltrg
        bit3=self._DisitckRvtet1Plctxoff
        bit4=self._DisitckRvtet1Mps
        bit5=self._DisitckRvtet1Diag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 7)

    def update_RvTet2(self):
        bit0=self._DisitckRvtet2Dacsoffloopsstby
        bit1=self._DisitckRvtet2Pindiodeswitch
        bit2=self._DisitckRvtet2Fdltrg
        bit3=self._DisitckRvtet2Plctxoff
        bit4=self._DisitckRvtet2Mps
        bit5=self._DisitckRvtet2Diag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 8)

    def update_RvCircIn(self):
        bit0=self._DisitckRvcircDacsoffloopsstby
        bit1=self._DisitckRvcircPindiodeswitch
        bit2=self._DisitckRvcircFdltrg
        bit3=self._DisitckRvcircPlctxoff
        bit4=self._DisitckRvcircMps
        bit5=self._DisitckRvcircDiag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 9)

    def update_FwLoad(self):
        bit0=self._DisitckFwloadDacsoffloopsstby
        bit1=self._DisitckFwloadPindiodeswitch
        bit2=self._DisitckFwloadFdltrg
        bit3=self._DisitckFwloadPlctxoff
        bit4=self._DisitckFwloadMps
        bit5=self._DisitckFwloadDiag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 10)

    def update_FwHybLoad(self):
        bit0=self._DisitckFwhybloadDacsoffloopsstby
        bit1=self._DisitckFwhybloadPindiodeswitch
        bit2=self._DisitckFwhybloadFdltrg
        bit3=self._DisitckFwhybloadPlctxoff
        bit4=self._DisitckFwhybloadMps
        bit5=self._DisitckFwhybloadDiag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 11)

    def update_RvCav(self):
        bit0=self._DisitckRvcavDacsoffloopsstby
        bit1=self._DisitckRvcavPindiodeswitch
        bit2=self._DisitckRvcavFdltrg
        bit3=self._DisitckRvcavPlctxoff
        bit4=self._DisitckRvcavMps
        bit5=self._DisitckRvcavDiag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 12)

    def update_Arc(self):
        bit0=self._DisitckArcsDacsoffloopsstby
        bit1=self._DisitckArcsPindiodeswitch
        bit2=self._DisitckArcsFdltrg
        bit3=self._DisitckArcsPlctxoff
        bit4=self._DisitckArcsMps
        bit5=self._DisitckArcsDiag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 13)

    def update_Vacuum(self):
        bit0=self._DisitckVacuumDacsoffloopsstby
        bit1=self._DisitckVacuumPindiodeswitch
        bit2=self._DisitckVacuumFdltrg
        bit3=self._DisitckVacuumPlctxoff
        bit4=self._DisitckVacuumMps
        bit5=self._DisitckVacuumDiag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 14)

    def update_Manual(self):
        bit0=self._DisitckManualInterlockDacsoffloopsstby
        bit1=self._DisitckManualInterlockPindiodeswitch
        bit2=self._DisitckManualInterlockFdltrg
        bit3=self._DisitckManualInterlockPlctxoff
        bit4=self._DisitckManualInterlockMps
        bit5=self._DisitckManualInterlockDiag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 15)

    def update_EndSwUp(self):
        bit0=self._DisitckPlungerEndSwitchesUpDacsoffloopsstby
        bit1=self._DisitckPlungerEndSwitchesUpPindiodeswitch
        bit2=self._DisitckPlungerEndSwitchesUpFdltrg
        bit3=self._DisitckPlungerEndSwitchesUpPlctxoff
        bit4=self._DisitckPlungerEndSwitchesUpMps
        bit5=self._DisitckPlungerEndSwitchesUpDiag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 16)

    def update_EndSwDown(self):
        bit0=self._DisitckPlungerEndSwitchesDownDacsoffloopsstby
        bit1=self._DisitckPlungerEndSwitchesDownPindiodeswitch
        bit2=self._DisitckPlungerEndSwitchesDownFdltrg
        bit3=self._DisitckPlungerEndSwitchesDownPlctxoff
        bit4=self._DisitckPlungerEndSwitchesDownMps
        bit5=self._DisitckPlungerEndSwitchesDownDiag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 17)

    def update_Mps(self):
        bit0=self._DisitckMpsDacsoffloopsstby
        bit1=self._DisitckMpsPindiodeswitch
        bit2=self._DisitckMpsFdltrg
        bit3=self._DisitckMpsPlctxoff
        bit4=self._DisitckMpsMps
        bit5=self._DisitckMpsDiag
        value = (bit5 << 5) | (bit4 << 4) | (bit3 << 3) | (bit2 << 2) | (bit1 << 1) | (bit0 << 0)
        perseus_utils.write_direct(self.perseus, value, 18)

def run_device():
    run([NutaqDiags])

if __name__ == "__main__":
    run_device()
