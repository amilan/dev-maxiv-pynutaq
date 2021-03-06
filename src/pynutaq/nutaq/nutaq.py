#!/usr/bin/env python

###############################################################################
#     Nutaq device server.
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

"""This module contains the Nutaq device server for loops.
"""

__all__ = ["Nutaq", "run_device"]

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
from pynutaq.nutaq.nutaqdefs import *

import pynutaq.extra as extra_func

import pynutaq.perseus.perseusutils as perseus_utils

try:
    from pynutaq.perseus.perseusdefs import *
    from pynutaq.perseus.perseusfactory import Perseus
except ImportError, e:
    print e


class Nutaq(Device):
    __metaclass__ = DeviceMeta

    KpA = attribute(label='KpA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=10,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KpA",
                                   fset="set_KpA",
                                   doc=""
                                   )

    KpB = attribute(label='KpB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=10,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KpB",
                                   fset="set_KpB",
                                   doc=""
                                   )

    KiA = attribute(label='KiA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KiA",
                                   fset="set_KiA",
                                   doc=""
                                   )

    KiB = attribute(label='KiB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KiB",
                                   fset="set_KiB",
                                   doc=""
                                   )

    PhaseShiftCavA = attribute(label='PhaseShiftCavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftCavA",
                                   fset="set_PhaseShiftCavA",
                                   doc=""
                                   )

    PhaseShiftCavB = attribute(label='PhaseShiftCavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftCavB",
                                   fset="set_PhaseShiftCavB",
                                   doc=""
                                   )

    PhaseShiftFwcavA = attribute(label='PhaseShiftFwcavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftFwcavA",
                                   fset="set_PhaseShiftFwcavA",
                                   doc=""
                                   )

    PhaseShiftFwcavB = attribute(label='PhaseShiftFwcavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftFwcavB",
                                   fset="set_PhaseShiftFwcavB",
                                   doc=""
                                   )

    PhaseShiftFwtet1A = attribute(label='PhaseShiftFwtet1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftFwtet1A",
                                   fset="set_PhaseShiftFwtet1A",
                                   doc=""
                                   )

    PhaseShiftFwtet1B = attribute(label='PhaseShiftFwtet1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftFwtet1B",
                                   fset="set_PhaseShiftFwtet1B",
                                   doc=""
                                   )

    PhaseShiftFwtet2A = attribute(label='PhaseShiftFwtet2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftFwtet2A",
                                   fset="set_PhaseShiftFwtet2A",
                                   doc=""
                                   )

    PhaseShiftFwtet2B = attribute(label='PhaseShiftFwtet2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftFwtet2B",
                                   fset="set_PhaseShiftFwtet2B",
                                   doc=""
                                   )

    PilimitA = attribute(label='PilimitA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PilimitA",
                                   fset="set_PilimitA",
                                   doc=""
                                   )

    PilimitB = attribute(label='PilimitB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PilimitB",
                                   fset="set_PilimitB",
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

    FilterStagesA = attribute(label='FilterStagesA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FilterStagesA",
                                   fset="set_FilterStagesA",
                                   doc=""
                                   )

    FilterStagesB = attribute(label='FilterStagesB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FilterStagesB",
                                   fset="set_FilterStagesB",
                                   doc=""
                                   )

    PhaseShiftFwcircinA = attribute(label='PhaseShiftFwcircinA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftFwcircinA",
                                   fset="set_PhaseShiftFwcircinA",
                                   doc=""
                                   )

    PhaseShiftFwcircinB = attribute(label='PhaseShiftFwcircinB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftFwcircinB",
                                   fset="set_PhaseShiftFwcircinB",
                                   doc=""
                                   )

    PhaseShiftControlSignalTet1A = attribute(label='PhaseShiftControlSignalTet1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftControlSignalTet1A",
                                   fset="set_PhaseShiftControlSignalTet1A",
                                   doc=""
                                   )

    PhaseShiftControlSignalTet1B = attribute(label='PhaseShiftControlSignalTet1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftControlSignalTet1B",
                                   fset="set_PhaseShiftControlSignalTet1B",
                                   doc=""
                                   )

    PhaseShiftControlSignalTet2A = attribute(label='PhaseShiftControlSignalTet2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftControlSignalTet2A",
                                   fset="set_PhaseShiftControlSignalTet2A",
                                   doc=""
                                   )

    PhaseShiftControlSignalTet2B = attribute(label='PhaseShiftControlSignalTet2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseShiftControlSignalTet2B",
                                   fset="set_PhaseShiftControlSignalTet2B",
                                   doc=""
                                   )

    GainTetrode1A = attribute(label='GainTetrode1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0.1, max_value=1,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_GainTetrode1A",
                                   fset="set_GainTetrode1A",
                                   doc=""
                                   )

    GainTetrode1B = attribute(label='GainTetrode1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0.1, max_value=1,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_GainTetrode1B",
                                   fset="set_GainTetrode1B",
                                   doc=""
                                   )

    GainTetrode2A = attribute(label='GainTetrode2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0.1, max_value=1,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_GainTetrode2A",
                                   fset="set_GainTetrode2A",
                                   doc=""
                                   )

    GainTetrode2B = attribute(label='GainTetrode2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0.1, max_value=1,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_GainTetrode2B",
                                   fset="set_GainTetrode2B",
                                   doc=""
                                   )

    AutomaticStartupEnableA = attribute(label='AutomaticStartupEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_AutomaticStartupEnableA",
                                   fset="set_AutomaticStartupEnableA",
                                   doc=""
                                   )

    AutomaticStartupEnableB = attribute(label='AutomaticStartupEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_AutomaticStartupEnableB",
                                   fset="set_AutomaticStartupEnableB",
                                   doc=""
                                   )

    CommandStartA = attribute(label='CommandStartA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_CommandStartA",
                                   fset="set_CommandStartA",
                                   doc=""
                                   )

    CommandStartB = attribute(label='CommandStartB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_CommandStartB",
                                   fset="set_CommandStartB",
                                   doc=""
                                   )

    AmprefinA = attribute(label='AmprefinA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_AmprefinA",
                                   fset="set_AmprefinA",
                                   doc=""
                                   )

    AmprefinB = attribute(label='AmprefinB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_AmprefinB",
                                   fset="set_AmprefinB",
                                   doc=""
                                   )

    PhrefinA = attribute(label='PhrefinA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhrefinA",
                                   fset="set_PhrefinA",
                                   doc=""
                                   )

    PhrefinB = attribute(label='PhrefinB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhrefinB",
                                   fset="set_PhrefinB",
                                   doc=""
                                   )

    AmprefminA = attribute(label='AmprefminA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_AmprefminA",
                                   fset="set_AmprefminA",
                                   doc=""
                                   )

    AmprefminB = attribute(label='AmprefminB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_AmprefminB",
                                   fset="set_AmprefminB",
                                   doc=""
                                   )

    PhrefminA = attribute(label='PhrefminA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhrefminA",
                                   fset="set_PhrefminA",
                                   doc=""
                                   )

    PhrefminB = attribute(label='PhrefminB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhrefminB",
                                   fset="set_PhrefminB",
                                   doc=""
                                   )

    PhaseIncreaseRateA = attribute(label='PhaseIncreaseRateA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseIncreaseRateA",
                                   fset="set_PhaseIncreaseRateA",
                                   doc=""
                                   )

    PhaseIncreaseRateB = attribute(label='PhaseIncreaseRateB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseIncreaseRateB",
                                   fset="set_PhaseIncreaseRateB",
                                   doc=""
                                   )

    VoltageIncreaseRateA = attribute(label='VoltageIncreaseRateA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_VoltageIncreaseRateA",
                                   fset="set_VoltageIncreaseRateA",
                                   doc=""
                                   )

    VoltageIncreaseRateB = attribute(label='VoltageIncreaseRateB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_VoltageIncreaseRateB",
                                   fset="set_VoltageIncreaseRateB",
                                   doc=""
                                   )

    GainOlA = attribute(label='GainOlA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0.5, max_value=2,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_GainOlA",
                                   fset="set_GainOlA",
                                   doc=""
                                   )

    GainOlB = attribute(label='GainOlB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0.5, max_value=2,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_GainOlB",
                                   fset="set_GainOlB",
                                   doc=""
                                   )

    SpareGpioOutput01A = attribute(label='SpareGpioOutput01A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareGpioOutput01A",
                                   fset="set_SpareGpioOutput01A",
                                   doc=""
                                   )

    SpareGpioOutput01B = attribute(label='SpareGpioOutput01B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareGpioOutput01B",
                                   fset="set_SpareGpioOutput01B",
                                   doc=""
                                   )

    SpareGpioOutput02A = attribute(label='SpareGpioOutput02A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareGpioOutput02A",
                                   fset="set_SpareGpioOutput02A",
                                   doc=""
                                   )

    SpareGpioOutput02B = attribute(label='SpareGpioOutput02B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareGpioOutput02B",
                                   fset="set_SpareGpioOutput02B",
                                   doc=""
                                   )

    SpareGpioOutput03A = attribute(label='SpareGpioOutput03A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareGpioOutput03A",
                                   fset="set_SpareGpioOutput03A",
                                   doc=""
                                   )

    SpareGpioOutput03B = attribute(label='SpareGpioOutput03B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareGpioOutput03B",
                                   fset="set_SpareGpioOutput03B",
                                   doc=""
                                   )

    SpareGpioOutput04A = attribute(label='SpareGpioOutput04A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareGpioOutput04A",
                                   fset="set_SpareGpioOutput04A",
                                   doc=""
                                   )

    SpareGpioOutput04B = attribute(label='SpareGpioOutput04B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SpareGpioOutput04B",
                                   fset="set_SpareGpioOutput04B",
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

    SlowIqLoopEnableA = attribute(label='SlowIqLoopEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SlowIqLoopEnableA",
                                   fset="set_SlowIqLoopEnableA",
                                   doc=""
                                   )

    SlowIqLoopEnableB = attribute(label='SlowIqLoopEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SlowIqLoopEnableB",
                                   fset="set_SlowIqLoopEnableB",
                                   doc=""
                                   )

    AdcsPhaseshiftEnableA = attribute(label='AdcsPhaseshiftEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_AdcsPhaseshiftEnableA",
                                   fset="set_AdcsPhaseshiftEnableA",
                                   doc=""
                                   )

    AdcsPhaseshiftEnableB = attribute(label='AdcsPhaseshiftEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_AdcsPhaseshiftEnableB",
                                   fset="set_AdcsPhaseshiftEnableB",
                                   doc=""
                                   )

    DacsPhaseShiftEnableA = attribute(label='DacsPhaseShiftEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DacsPhaseShiftEnableA",
                                   fset="set_DacsPhaseShiftEnableA",
                                   doc=""
                                   )

    DacsPhaseShiftEnableB = attribute(label='DacsPhaseShiftEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_DacsPhaseShiftEnableB",
                                   fset="set_DacsPhaseShiftEnableB",
                                   doc=""
                                   )

    SquarerefEnableA = attribute(label='SquarerefEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SquarerefEnableA",
                                   fset="set_SquarerefEnableA",
                                   doc=""
                                   )

    SquarerefEnableB = attribute(label='SquarerefEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SquarerefEnableB",
                                   fset="set_SquarerefEnableB",
                                   doc=""
                                   )

    FreqsquareA = attribute(label='FreqsquareA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=3, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FreqsquareA",
                                   fset="set_FreqsquareA",
                                   doc=""
                                   )

    FreqsquareB = attribute(label='FreqsquareB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=3, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FreqsquareB",
                                   fset="set_FreqsquareB",
                                   doc=""
                                   )

    LookRefA = attribute(label='LookRefA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_LookRefA",
                                   fset="set_LookRefA",
                                   doc=""
                                   )

    LookRefB = attribute(label='LookRefB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_LookRefB",
                                   fset="set_LookRefB",
                                   doc=""
                                   )

    QuadrantSelectionA = attribute(label='QuadrantSelectionA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_QuadrantSelectionA",
                                   fset="set_QuadrantSelectionA",
                                   doc=""
                                   )

    QuadrantSelectionB = attribute(label='QuadrantSelectionB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_QuadrantSelectionB",
                                   fset="set_QuadrantSelectionB",
                                   doc=""
                                   )

    SlowIqLoopInputSelectionA = attribute(label='SlowIqLoopInputSelectionA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_SlowIqLoopInputSelectionA",
                                   fset="set_SlowIqLoopInputSelectionA",
                                   doc=""
                                   )

    SlowIqLoopInputSelectionB = attribute(label='SlowIqLoopInputSelectionB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_SlowIqLoopInputSelectionB",
                                   fset="set_SlowIqLoopInputSelectionB",
                                   doc=""
                                   )

    FastIqLoopInputSelectionA = attribute(label='FastIqLoopInputSelectionA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FastIqLoopInputSelectionA",
                                   fset="set_FastIqLoopInputSelectionA",
                                   doc=""
                                   )

    FastIqLoopInputSelectionB = attribute(label='FastIqLoopInputSelectionB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FastIqLoopInputSelectionB",
                                   fset="set_FastIqLoopInputSelectionB",
                                   doc=""
                                   )

    AmplitudeLoopInputSelectionA = attribute(label='AmplitudeLoopInputSelectionA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_AmplitudeLoopInputSelectionA",
                                   fset="set_AmplitudeLoopInputSelectionA",
                                   doc=""
                                   )

    AmplitudeLoopInputSelectionB = attribute(label='AmplitudeLoopInputSelectionB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_AmplitudeLoopInputSelectionB",
                                   fset="set_AmplitudeLoopInputSelectionB",
                                   doc=""
                                   )

    PhaseLoopInputSelectionA = attribute(label='PhaseLoopInputSelectionA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseLoopInputSelectionA",
                                   fset="set_PhaseLoopInputSelectionA",
                                   doc=""
                                   )

    PhaseLoopInputSelectionB = attribute(label='PhaseLoopInputSelectionB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseLoopInputSelectionB",
                                   fset="set_PhaseLoopInputSelectionB",
                                   doc=""
                                   )

    PolarLoopsEnableA = attribute(label='PolarLoopsEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_PolarLoopsEnableA",
                                   fset="set_PolarLoopsEnableA",
                                   doc=""
                                   )

    PolarLoopsEnableB = attribute(label='PolarLoopsEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_PolarLoopsEnableB",
                                   fset="set_PolarLoopsEnableB",
                                   doc=""
                                   )

    FastIqLoopEnableA = attribute(label='FastIqLoopEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_FastIqLoopEnableA",
                                   fset="set_FastIqLoopEnableA",
                                   doc=""
                                   )

    FastIqLoopEnableB = attribute(label='FastIqLoopEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_FastIqLoopEnableB",
                                   fset="set_FastIqLoopEnableB",
                                   doc=""
                                   )

    AmplitudeLoopEnableA = attribute(label='AmplitudeLoopEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_AmplitudeLoopEnableA",
                                   fset="set_AmplitudeLoopEnableA",
                                   doc=""
                                   )

    AmplitudeLoopEnableB = attribute(label='AmplitudeLoopEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_AmplitudeLoopEnableB",
                                   fset="set_AmplitudeLoopEnableB",
                                   doc=""
                                   )

    PhaseLoopEnableA = attribute(label='PhaseLoopEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_PhaseLoopEnableA",
                                   fset="set_PhaseLoopEnableA",
                                   doc=""
                                   )

    PhaseLoopEnableB = attribute(label='PhaseLoopEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_PhaseLoopEnableB",
                                   fset="set_PhaseLoopEnableB",
                                   doc=""
                                   )

    KpFastIqLoopA = attribute(label='KpFastIqLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KpFastIqLoopA",
                                   fset="set_KpFastIqLoopA",
                                   doc=""
                                   )

    KpFastIqLoopB = attribute(label='KpFastIqLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KpFastIqLoopB",
                                   fset="set_KpFastIqLoopB",
                                   doc=""
                                   )

    KiFastIqLoopA = attribute(label='KiFastIqLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KiFastIqLoopA",
                                   fset="set_KiFastIqLoopA",
                                   doc=""
                                   )

    KiFastIqLoopB = attribute(label='KiFastIqLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KiFastIqLoopB",
                                   fset="set_KiFastIqLoopB",
                                   doc=""
                                   )

    KpAmpLoopA = attribute(label='KpAmpLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KpAmpLoopA",
                                   fset="set_KpAmpLoopA",
                                   doc=""
                                   )

    KpAmpLoopB = attribute(label='KpAmpLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KpAmpLoopB",
                                   fset="set_KpAmpLoopB",
                                   doc=""
                                   )

    KiAmpLoopA = attribute(label='KiAmpLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KiAmpLoopA",
                                   fset="set_KiAmpLoopA",
                                   doc=""
                                   )

    KiAmpLoopB = attribute(label='KiAmpLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KiAmpLoopB",
                                   fset="set_KiAmpLoopB",
                                   doc=""
                                   )

    KpPhaseLoopA = attribute(label='KpPhaseLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KpPhaseLoopA",
                                   fset="set_KpPhaseLoopA",
                                   doc=""
                                   )

    KpPhaseLoopB = attribute(label='KpPhaseLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KpPhaseLoopB",
                                   fset="set_KpPhaseLoopB",
                                   doc=""
                                   )

    KiPhaseLoopA = attribute(label='KiPhaseLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KiPhaseLoopA",
                                   fset="set_KiPhaseLoopA",
                                   doc=""
                                   )

    KiPhaseLoopB = attribute(label='KiPhaseLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=32767,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_KiPhaseLoopB",
                                   fset="set_KiPhaseLoopB",
                                   doc=""
                                   )

    PiLimitFastPiIqA = attribute(label='PiLimitFastPiIqA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PiLimitFastPiIqA",
                                   fset="set_PiLimitFastPiIqA",
                                   doc=""
                                   )

    PiLimitFastPiIqB = attribute(label='PiLimitFastPiIqB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PiLimitFastPiIqB",
                                   fset="set_PiLimitFastPiIqB",
                                   doc=""
                                   )

    PulseModeEnableA = attribute(label='PulseModeEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_PulseModeEnableA",
                                   fset="set_PulseModeEnableA",
                                   doc=""
                                   )

    PulseModeEnableB = attribute(label='PulseModeEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_PulseModeEnableB",
                                   fset="set_PulseModeEnableB",
                                   doc=""
                                   )

    AutomaticConditioningEnableA = attribute(label='AutomaticConditioningEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_AutomaticConditioningEnableA",
                                   fset="set_AutomaticConditioningEnableA",
                                   doc=""
                                   )

    AutomaticConditioningEnableB = attribute(label='AutomaticConditioningEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_AutomaticConditioningEnableB",
                                   fset="set_AutomaticConditioningEnableB",
                                   doc=""
                                   )

    ConditioningdutyCicleA = attribute(label='ConditioningdutyCicleA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=100,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_ConditioningdutyCicleA",
                                   fset="set_ConditioningdutyCicleA",
                                   doc=""
                                   )

    ConditioningdutyCicleB = attribute(label='ConditioningdutyCicleB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=100,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_ConditioningdutyCicleB",
                                   fset="set_ConditioningdutyCicleB",
                                   doc=""
                                   )

    TuningEnableA = attribute(label='TuningEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_TuningEnableA",
                                   fset="set_TuningEnableA",
                                   doc=""
                                   )

    TuningEnableB = attribute(label='TuningEnableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_TuningEnableB",
                                   fset="set_TuningEnableB",
                                   doc=""
                                   )

    TuningPosEnA = attribute(label='TuningPosEnA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_TuningPosEnA",
                                   fset="set_TuningPosEnA",
                                   doc=""
                                   )

    TuningPosEnB = attribute(label='TuningPosEnB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_TuningPosEnB",
                                   fset="set_TuningPosEnB",
                                   doc=""
                                   )

    NumStepsA = attribute(label='NumStepsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=65535,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_NumStepsA",
                                   fset="set_NumStepsA",
                                   doc=""
                                   )

    NumStepsB = attribute(label='NumStepsB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=65535,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_NumStepsB",
                                   fset="set_NumStepsB",
                                   doc=""
                                   )

    PulsesFrequencyA = attribute(label='PulsesFrequencyA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PulsesFrequencyA",
                                   fset="set_PulsesFrequencyA",
                                   doc=""
                                   )

    PulsesFrequencyB = attribute(label='PulsesFrequencyB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=7,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PulsesFrequencyB",
                                   fset="set_PulsesFrequencyB",
                                   doc=""
                                   )

    PhaseOffsetA = attribute(label='PhaseOffsetA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseOffsetA",
                                   fset="set_PhaseOffsetA",
                                   doc=""
                                   )

    PhaseOffsetB = attribute(label='PhaseOffsetB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=360,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_PhaseOffsetB",
                                   fset="set_PhaseOffsetB",
                                   doc=""
                                   )

    MoveA = attribute(label='MoveA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_MoveA",
                                   fset="set_MoveA",
                                   doc=""
                                   )

    MoveB = attribute(label='MoveB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_MoveB",
                                   fset="set_MoveB",
                                   doc=""
                                   )

    MoveupA = attribute(label='MoveupA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_MoveupA",
                                   fset="set_MoveupA",
                                   doc=""
                                   )

    MoveupB = attribute(label='MoveupB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_MoveupB",
                                   fset="set_MoveupB",
                                   doc=""
                                   )

    TuningresetA = attribute(label='TuningresetA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_TuningresetA",
                                   fset="set_TuningresetA",
                                   doc=""
                                   )

    TuningresetB = attribute(label='TuningresetB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_TuningresetB",
                                   fset="set_TuningresetB",
                                   doc=""
                                   )

    FwminA = attribute(label='FwminA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FwminA",
                                   fset="set_FwminA",
                                   doc=""
                                   )

    FwminB = attribute(label='FwminB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_FwminB",
                                   fset="set_FwminB",
                                   doc=""
                                   )

    MarginupA = attribute(label='MarginupA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=0, max_value=10,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_MarginupA",
                                   fset="set_MarginupA",
                                   doc=""
                                   )

    MarginupB = attribute(label='MarginupB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=0, max_value=10,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_MarginupB",
                                   fset="set_MarginupB",
                                   doc=""
                                   )

    MarginlowA = attribute(label='MarginlowA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=0, max_value=5,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_MarginlowA",
                                   fset="set_MarginlowA",
                                   doc=""
                                   )

    MarginlowB = attribute(label='MarginlowB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=0, max_value=5,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_MarginlowB",
                                   fset="set_MarginlowB",
                                   doc=""
                                   )

    TuningdelayA = attribute(label='TuningdelayA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_TuningdelayA",
                                   fset="set_TuningdelayA",
                                   doc=""
                                   )

    TuningdelayB = attribute(label='TuningdelayB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=3,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_TuningdelayB",
                                   fset="set_TuningdelayB",
                                   doc=""
                                   )

    TuningfilterenableA = attribute(label='TuningfilterenableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_TuningfilterenableA",
                                   fset="set_TuningfilterenableA",
                                   doc=""
                                   )

    TuningfilterenableB = attribute(label='TuningfilterenableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_TuningfilterenableB",
                                   fset="set_TuningfilterenableB",
                                   doc=""
                                   )

    TuningtriggerenableA = attribute(label='TuningtriggerenableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_TuningtriggerenableA",
                                   fset="set_TuningtriggerenableA",
                                   doc=""
                                   )

    TuningtriggerenableB = attribute(label='TuningtriggerenableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_TuningtriggerenableB",
                                   fset="set_TuningtriggerenableB",
                                   doc=""
                                   )

    EpsItckDisableA = attribute(label='EpsItckDisableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_EpsItckDisableA",
                                   fset="set_EpsItckDisableA",
                                   doc=""
                                   )

    EpsItckDisableB = attribute(label='EpsItckDisableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_EpsItckDisableB",
                                   fset="set_EpsItckDisableB",
                                   doc=""
                                   )

    FimItckDisableA = attribute(label='FimItckDisableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_FimItckDisableA",
                                   fset="set_FimItckDisableA",
                                   doc=""
                                   )

    FimItckDisableB = attribute(label='FimItckDisableB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_FimItckDisableB",
                                   fset="set_FimItckDisableB",
                                   doc=""
                                   )

    MDividerA = attribute(label='MDividerA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=128,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_MDividerA",
                                   fset="set_MDividerA",
                                   doc=""
                                   )

    MDividerB = attribute(label='MDividerB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=128,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_MDividerB",
                                   fset="set_MDividerB",
                                   doc=""
                                   )

    NDividerA = attribute(label='NDividerA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=128,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_NDividerA",
                                   fset="set_NDividerA",
                                   doc=""
                                   )

    NDividerB = attribute(label='NDividerB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=128,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_NDividerB",
                                   fset="set_NDividerB",
                                   doc=""
                                   )

    MuxselA = attribute(label='MuxselA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_MuxselA",
                                   fset="set_MuxselA",
                                   doc=""
                                   )

    MuxselB = attribute(label='MuxselB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_MuxselB",
                                   fset="set_MuxselB",
                                   doc=""
                                   )

    Mux0DividerA = attribute(label='Mux0DividerA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Mux0DividerA",
                                   fset="set_Mux0DividerA",
                                   doc=""
                                   )

    Mux0DividerB = attribute(label='Mux0DividerB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Mux0DividerB",
                                   fset="set_Mux0DividerB",
                                   doc=""
                                   )

    Mux1DividerA = attribute(label='Mux1DividerA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Mux1DividerA",
                                   fset="set_Mux1DividerA",
                                   doc=""
                                   )

    Mux1DividerB = attribute(label='Mux1DividerB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Mux1DividerB",
                                   fset="set_Mux1DividerB",
                                   doc=""
                                   )

    Mux2DividerA = attribute(label='Mux2DividerA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Mux2DividerA",
                                   fset="set_Mux2DividerA",
                                   doc=""
                                   )

    Mux2DividerB = attribute(label='Mux2DividerB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Mux2DividerB",
                                   fset="set_Mux2DividerB",
                                   doc=""
                                   )

    Mux3DividerA = attribute(label='Mux3DividerA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Mux3DividerA",
                                   fset="set_Mux3DividerA",
                                   doc=""
                                   )

    Mux3DividerB = attribute(label='Mux3DividerB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Mux3DividerB",
                                   fset="set_Mux3DividerB",
                                   doc=""
                                   )

    Mux4DividerA = attribute(label='Mux4DividerA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Mux4DividerA",
                                   fset="set_Mux4DividerA",
                                   doc=""
                                   )

    Mux4DividerB = attribute(label='Mux4DividerB',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=4,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   fget="get_Mux4DividerB",
                                   fset="set_Mux4DividerB",
                                   doc=""
                                   )

    SendWordA = attribute(label='SendWordA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SendWordA",
                                   fset="set_SendWordA",
                                   doc=""
                                   )

    SendWordB = attribute(label='SendWordB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_SendWordB",
                                   fset="set_SendWordB",
                                   doc=""
                                   )

    CpdirA = attribute(label='CpdirA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_CpdirA",
                                   fset="set_CpdirA",
                                   doc=""
                                   )

    CpdirB = attribute(label='CpdirB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_CpdirB",
                                   fset="set_CpdirB",
                                   doc=""
                                   )

    VcxoOutputInversionA = attribute(label='VcxoOutputInversionA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_VcxoOutputInversionA",
                                   fset="set_VcxoOutputInversionA",
                                   doc=""
                                   )

    VcxoOutputInversionB = attribute(label='VcxoOutputInversionB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   memorized=True,
                                   unit='',
                                   format='%6.2f',
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   fget="get_VcxoOutputInversionB",
                                   fset="set_VcxoOutputInversionB",
                                   doc=""
                                   )

    Diag_IcavLoopsA = attribute(label='Diag_IcavLoopsA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcavLoopsB = attribute(label='Diag_IcavLoopsB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcavLoopsA = attribute(label='Diag_QcavLoopsA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcavLoopsB = attribute(label='Diag_QcavLoopsB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolA = attribute(label='Diag_IcontrolA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolB = attribute(label='Diag_IcontrolB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolA = attribute(label='Diag_QcontrolA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolB = attribute(label='Diag_QcontrolB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Icontrol1A = attribute(label='Diag_Icontrol1A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Icontrol1B = attribute(label='Diag_Icontrol1B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qcontrol1A = attribute(label='Diag_Qcontrol1A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qcontrol1B = attribute(label='Diag_Qcontrol1B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Icontrol2A = attribute(label='Diag_Icontrol2A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Icontrol2B = attribute(label='Diag_Icontrol2B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qcontrol2A = attribute(label='Diag_Qcontrol2A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qcontrol2B = attribute(label='Diag_Qcontrol2B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IerrorA = attribute(label='Diag_IerrorA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IerrorB = attribute(label='Diag_IerrorB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QerrorA = attribute(label='Diag_QerrorA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QerrorB = attribute(label='Diag_QerrorB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IerroraccumA = attribute(label='Diag_IerroraccumA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IerroraccumB = attribute(label='Diag_IerroraccumB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QerroraccumA = attribute(label='Diag_QerroraccumA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QerroraccumB = attribute(label='Diag_QerroraccumB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrefA = attribute(label='Diag_IrefA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrefB = attribute(label='Diag_IrefB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrefA = attribute(label='Diag_QrefA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrefB = attribute(label='Diag_QrefB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwCavLoopsA = attribute(label='Diag_IFwCavLoopsA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwCavLoopsB = attribute(label='Diag_IFwCavLoopsB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwCavLoopsA = attribute(label='Diag_QFwCavLoopsA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwCavLoopsB = attribute(label='Diag_QFwCavLoopsB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwTet1LoopsA = attribute(label='Diag_IFwTet1LoopsA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwTet1LoopsB = attribute(label='Diag_IFwTet1LoopsB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwTet1LoopsA = attribute(label='Diag_QFwTet1LoopsA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwTet1LoopsB = attribute(label='Diag_QFwTet1LoopsB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwTet2LoopsA = attribute(label='Diag_IFwTet2LoopsA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwTet2LoopsB = attribute(label='Diag_IFwTet2LoopsB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwTet2LoopsA = attribute(label='Diag_QFwTet2LoopsA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwTet2LoopsB = attribute(label='Diag_QFwTet2LoopsB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwCircInLoopsA = attribute(label='Diag_IFwCircInLoopsA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwCircInLoopsB = attribute(label='Diag_IFwCircInLoopsB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwCircInLoopsA = attribute(label='Diag_QFwCircInLoopsA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwCircInLoopsB = attribute(label='Diag_QFwCircInLoopsB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
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

    Diag_Ispare1A = attribute(label='Diag_Ispare1A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ispare1B = attribute(label='Diag_Ispare1B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qspare1A = attribute(label='Diag_Qspare1A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qspare1B = attribute(label='Diag_Qspare1B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ispare2A = attribute(label='Diag_Ispare2A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ispare2B = attribute(label='Diag_Ispare2B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qspare2A = attribute(label='Diag_Qspare2A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qspare2B = attribute(label='Diag_Qspare2B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxCavA = attribute(label='Diag_IMuxCavA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxCavB = attribute(label='Diag_IMuxCavB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxCavA = attribute(label='Diag_QMuxCavA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxCavB = attribute(label='Diag_QMuxCavB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwCavA = attribute(label='Diag_IMuxFwCavA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwCavB = attribute(label='Diag_IMuxFwCavB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwCavA = attribute(label='Diag_QMuxFwCavA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwCavB = attribute(label='Diag_QMuxFwCavB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwTet1A = attribute(label='Diag_IMuxFwTet1A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwTet1B = attribute(label='Diag_IMuxFwTet1B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwTet1A = attribute(label='Diag_QMuxFwTet1A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwTet1B = attribute(label='Diag_QMuxFwTet1B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwTet2A = attribute(label='Diag_IMuxFwTet2A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwTet2B = attribute(label='Diag_IMuxFwTet2B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwTet2A = attribute(label='Diag_QMuxFwTet2A',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwTet2B = attribute(label='Diag_QMuxFwTet2B',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwCircInA = attribute(label='Diag_IMuxFwCircInA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwCircInB = attribute(label='Diag_IMuxFwCircInB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwCircInA = attribute(label='Diag_QMuxFwCircInA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwCircInB = attribute(label='Diag_QMuxFwCircInB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpCavA = attribute(label='Diag_AmpCavA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpCavB = attribute(label='Diag_AmpCavB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwA = attribute(label='Diag_AmpFwA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwB = attribute(label='Diag_AmpFwB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngCavFwA = attribute(label='Diag_AngCavFwA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngCavFwB = attribute(label='Diag_AngCavFwB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngCavLA = attribute(label='Diag_AngCavLA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngCavLB = attribute(label='Diag_AngCavLB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngFwLA = attribute(label='Diag_AngFwLA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngFwLB = attribute(label='Diag_AngFwLB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Vaccum1A = attribute(label='Diag_Vaccum1A',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Vaccum1B = attribute(label='Diag_Vaccum1B',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Vaccum2A = attribute(label='Diag_Vaccum2A',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Vaccum2B = attribute(label='Diag_Vaccum2B',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolSlowpiA = attribute(label='Diag_IcontrolSlowpiA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolSlowpiB = attribute(label='Diag_IcontrolSlowpiB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolSlowpiA = attribute(label='Diag_QcontrolSlowpiA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolSlowpiB = attribute(label='Diag_QcontrolSlowpiB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolFastpiA = attribute(label='Diag_IcontrolFastpiA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolFastpiB = attribute(label='Diag_IcontrolFastpiB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolFastpiA = attribute(label='Diag_QcontrolFastpiA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolFastpiB = attribute(label='Diag_QcontrolFastpiB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoPoweredA = attribute(label='Diag_VcxoPoweredA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoPoweredB = attribute(label='Diag_VcxoPoweredB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoRefA = attribute(label='Diag_VcxoRefA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoRefB = attribute(label='Diag_VcxoRefB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoLockedA = attribute(label='Diag_VcxoLockedA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoLockedB = attribute(label='Diag_VcxoLockedB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoCableDisconnectedA = attribute(label='Diag_VcxoCableDisconnectedA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoCableDisconnectedB = attribute(label='Diag_VcxoCableDisconnectedB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarForAmplitudeLoopA = attribute(label='Diag_IpolarForAmplitudeLoopA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarForAmplitudeLoopB = attribute(label='Diag_IpolarForAmplitudeLoopB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarForAmplitudeLoopA = attribute(label='Diag_QpolarForAmplitudeLoopA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarForAmplitudeLoopB = attribute(label='Diag_QpolarForAmplitudeLoopB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarForPhaseLoopA = attribute(label='Diag_IpolarForPhaseLoopA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarForPhaseLoopB = attribute(label='Diag_IpolarForPhaseLoopB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarForPhaseLoopA = attribute(label='Diag_QpolarForPhaseLoopA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarForPhaseLoopB = attribute(label='Diag_QpolarForPhaseLoopB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpInputOfAmpLoopA = attribute(label='Diag_AmpInputOfAmpLoopA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpInputOfAmpLoopB = attribute(label='Diag_AmpInputOfAmpLoopB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhaseInputOfAmpLoopA = attribute(label='Diag_PhaseInputOfAmpLoopA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhaseInputOfAmpLoopB = attribute(label='Diag_PhaseInputOfAmpLoopB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpInputOfPhaseLoopA = attribute(label='Diag_AmpInputOfPhaseLoopA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpInputOfPhaseLoopB = attribute(label='Diag_AmpInputOfPhaseLoopB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhInputOfPhaseLoopA = attribute(label='Diag_PhInputOfPhaseLoopA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhInputOfPhaseLoopB = attribute(label='Diag_PhInputOfPhaseLoopB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopControlOutputA = attribute(label='Diag_AmpLoopControlOutputA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopControlOutputB = attribute(label='Diag_AmpLoopControlOutputB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopErrorA = attribute(label='Diag_AmpLoopErrorA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopErrorB = attribute(label='Diag_AmpLoopErrorB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopErrorAccumA = attribute(label='Diag_AmpLoopErrorAccumA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopErrorAccumB = attribute(label='Diag_AmpLoopErrorAccumB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopControlOutputA = attribute(label='Diag_PhLoopControlOutputA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopControlOutputB = attribute(label='Diag_PhLoopControlOutputB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopErrorA = attribute(label='Diag_PhLoopErrorA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopErrorB = attribute(label='Diag_PhLoopErrorB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopErrorAccumA = attribute(label='Diag_PhLoopErrorAccumA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopErrorAccumB = attribute(label='Diag_PhLoopErrorAccumB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarControlOutputA = attribute(label='Diag_IpolarControlOutputA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarControlOutputB = attribute(label='Diag_IpolarControlOutputB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarControlOutputA = attribute(label='Diag_QpolarControlOutputA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarControlOutputB = attribute(label='Diag_QpolarControlOutputB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolSlowpiIqA = attribute(label='Diag_IcontrolSlowpiIqA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolSlowpiIqB = attribute(label='Diag_IcontrolSlowpiIqB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolSlowpiqA = attribute(label='Diag_QcontrolSlowpiqA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolSlowpiqB = attribute(label='Diag_QcontrolSlowpiqB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolFastpiIqA = attribute(label='Diag_IcontrolFastpiIqA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolFastpiIqB = attribute(label='Diag_IcontrolFastpiIqB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolFastpiIqA = attribute(label='Diag_QcontrolFastpiIqA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolFastpiIqB = attribute(label='Diag_QcontrolFastpiIqB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IloopinputSlowpiIqA = attribute(label='Diag_IloopinputSlowpiIqA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IloopinputSlowpiIqB = attribute(label='Diag_IloopinputSlowpiIqB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QloopinputSlowpiIqA = attribute(label='Diag_QloopinputSlowpiIqA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QloopinputSlowpiIqB = attribute(label='Diag_QloopinputSlowpiIqB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IloopinputFastpiIqA = attribute(label='Diag_IloopinputFastpiIqA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IloopinputFastpiIqB = attribute(label='Diag_IloopinputFastpiIqB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QloopinputFastpiIqA = attribute(label='Diag_QloopinputFastpiIqA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QloopinputFastpiIqB = attribute(label='Diag_QloopinputFastpiIqB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrefloopinputFastpiIqA = attribute(label='Diag_IrefloopinputFastpiIqA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrefloopinputFastpiIqB = attribute(label='Diag_IrefloopinputFastpiIqB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrefloopinputFastpiIqA = attribute(label='Diag_QrefloopinputFastpiIqA',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrefloopinputFastpiIqB = attribute(label='Diag_QrefloopinputFastpiIqB',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_MovingPlungerAutoA = attribute(label='Diag_MovingPlungerAutoA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_MovingPlungerAutoB = attribute(label='Diag_MovingPlungerAutoB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FreqUpA = attribute(label='Diag_FreqUpA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FreqUpB = attribute(label='Diag_FreqUpB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualTuningOnA = attribute(label='Diag_ManualTuningOnA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualTuningOnB = attribute(label='Diag_ManualTuningOnB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualTuningFreqUpA = attribute(label='Diag_ManualTuningFreqUpA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualTuningFreqUpB = attribute(label='Diag_ManualTuningFreqUpB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwminA = attribute(label='Diag_FwminA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwminB = attribute(label='Diag_FwminB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_EpsItckDelayA = attribute(label='Diag_EpsItckDelayA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_EpsItckDelayB = attribute(label='Diag_EpsItckDelayB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FimItckDelayA = attribute(label='Diag_FimItckDelayA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FimItckDelayB = attribute(label='Diag_FimItckDelayB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTrigHwInputA = attribute(label='Diag_FdlTrigHwInputA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTrigHwInputB = attribute(label='Diag_FdlTrigHwInputB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTrigSwInputA = attribute(label='Diag_FdlTrigSwInputA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTrigSwInputB = attribute(label='Diag_FdlTrigSwInputB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_EpsItckA = attribute(label='Diag_EpsItckA',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_EpsItckB = attribute(label='Diag_EpsItckB',
                                   dtype=bool,
                                   # polling_period=DEFAULT_POLLING_PERIOD,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwcircina = attribute(label='Diag_AmpMuxfwcircina',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpSpare1a = attribute(label='Diag_AmpSpare1a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwcircinb = attribute(label='Diag_AmpMuxfwcircinb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpSpare2a = attribute(label='Diag_AmpSpare2a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpSpare2b = attribute(label='Diag_AmpSpare2b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpErrora = attribute(label='Diag_AmpErrora',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpErrorb = attribute(label='Diag_AmpErrorb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpSpare1b = attribute(label='Diag_AmpSpare1b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpErroraccumb = attribute(label='Diag_AmpErroraccumb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpErroraccuma = attribute(label='Diag_AmpErroraccuma',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlfastpiiqb = attribute(label='Diag_AmpControlfastpiiqb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlfastpiiqa = attribute(label='Diag_AmpControlfastpiiqa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControla = attribute(label='Diag_AmpControla',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarforamplitudeloopa = attribute(label='Diag_AmpPolarforamplitudeloopa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarforamplitudeloopb = attribute(label='Diag_AmpPolarforamplitudeloopb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlb = attribute(label='Diag_AmpControlb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwtet2b = attribute(label='Diag_AmpMuxfwtet2b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopinputfastpiiqb = attribute(label='Diag_AmpLoopinputfastpiiqb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopinputfastpiiqa = attribute(label='Diag_AmpLoopinputfastpiiqa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRefa = attribute(label='Diag_AmpRefa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwcava = attribute(label='Diag_AmpMuxfwcava',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwcavb = attribute(label='Diag_AmpMuxfwcavb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRefb = attribute(label='Diag_AmpRefb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControl2a = attribute(label='Diag_AmpControl2a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControl2b = attribute(label='Diag_AmpControl2b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwtet1loopsb = attribute(label='Diag_AmpFwtet1loopsb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwtet1loopsa = attribute(label='Diag_AmpFwtet1loopsa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarforphaseloopb = attribute(label='Diag_AmpPolarforphaseloopb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarforphaseloopa = attribute(label='Diag_AmpPolarforphaseloopa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarcontroloutputb = attribute(label='Diag_AmpPolarcontroloutputb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarcontroloutputa = attribute(label='Diag_AmpPolarcontroloutputa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwtet2loopsa = attribute(label='Diag_AmpFwtet2loopsa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpCavloopsa = attribute(label='Diag_AmpCavloopsa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpCavloopsb = attribute(label='Diag_AmpCavloopsb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwtet2loopsb = attribute(label='Diag_AmpFwtet2loopsb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopinputslowpiiqa = attribute(label='Diag_AmpLoopinputslowpiiqa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopinputslowpiiqb = attribute(label='Diag_AmpLoopinputslowpiiqb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRefloopinputfastpiiqb = attribute(label='Diag_AmpRefloopinputfastpiiqb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRefloopinputfastpiiqa = attribute(label='Diag_AmpRefloopinputfastpiiqa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControl1a = attribute(label='Diag_AmpControl1a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControl1b = attribute(label='Diag_AmpControl1b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwtet2a = attribute(label='Diag_AmpMuxfwtet2a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxcavb = attribute(label='Diag_AmpMuxcavb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxcava = attribute(label='Diag_AmpMuxcava',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwtet1b = attribute(label='Diag_AmpMuxfwtet1b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlfastpib = attribute(label='Diag_AmpControlfastpib',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcircinloopsa = attribute(label='Diag_AmpFwcircinloopsa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcircinloopsb = attribute(label='Diag_AmpFwcircinloopsb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlfastpia = attribute(label='Diag_AmpControlfastpia',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcavloopsa = attribute(label='Diag_AmpFwcavloopsa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwtet1a = attribute(label='Diag_AmpMuxfwtet1a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcavloopsb = attribute(label='Diag_AmpFwcavloopsb',
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

    Diag_AmpMoa = attribute(label='Diag_AmpMoa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlslowpia = attribute(label='Diag_AmpControlslowpia',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlslowpib = attribute(label='Diag_AmpControlslowpib',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwcircina = attribute(label='Diag_PhMuxfwcircina',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhSpare1a = attribute(label='Diag_PhSpare1a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwcircinb = attribute(label='Diag_PhMuxfwcircinb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhSpare2a = attribute(label='Diag_PhSpare2a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhSpare2b = attribute(label='Diag_PhSpare2b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhErrora = attribute(label='Diag_PhErrora',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhErrorb = attribute(label='Diag_PhErrorb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhSpare1b = attribute(label='Diag_PhSpare1b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhErroraccumb = attribute(label='Diag_PhErroraccumb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhErroraccuma = attribute(label='Diag_PhErroraccuma',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlfastpiiqb = attribute(label='Diag_PhControlfastpiiqb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlfastpiiqa = attribute(label='Diag_PhControlfastpiiqa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControla = attribute(label='Diag_PhControla',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarforamplitudeloopa = attribute(label='Diag_PhPolarforamplitudeloopa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarforamplitudeloopb = attribute(label='Diag_PhPolarforamplitudeloopb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlb = attribute(label='Diag_PhControlb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwtet2b = attribute(label='Diag_PhMuxfwtet2b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopinputfastpiiqb = attribute(label='Diag_PhLoopinputfastpiiqb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopinputfastpiiqa = attribute(label='Diag_PhLoopinputfastpiiqa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRefa = attribute(label='Diag_PhRefa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwcava = attribute(label='Diag_PhMuxfwcava',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwcavb = attribute(label='Diag_PhMuxfwcavb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRefb = attribute(label='Diag_PhRefb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControl2a = attribute(label='Diag_PhControl2a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControl2b = attribute(label='Diag_PhControl2b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwtet1loopsb = attribute(label='Diag_PhFwtet1loopsb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwtet1loopsa = attribute(label='Diag_PhFwtet1loopsa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarforphaseloopb = attribute(label='Diag_PhPolarforphaseloopb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarforphaseloopa = attribute(label='Diag_PhPolarforphaseloopa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarcontroloutputb = attribute(label='Diag_PhPolarcontroloutputb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarcontroloutputa = attribute(label='Diag_PhPolarcontroloutputa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwtet2loopsa = attribute(label='Diag_PhFwtet2loopsa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhCavloopsa = attribute(label='Diag_PhCavloopsa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhCavloopsb = attribute(label='Diag_PhCavloopsb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwtet2loopsb = attribute(label='Diag_PhFwtet2loopsb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopinputslowpiiqa = attribute(label='Diag_PhLoopinputslowpiiqa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopinputslowpiiqb = attribute(label='Diag_PhLoopinputslowpiiqb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRefloopinputfastpiiqb = attribute(label='Diag_PhRefloopinputfastpiiqb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRefloopinputfastpiiqa = attribute(label='Diag_PhRefloopinputfastpiiqa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControl1a = attribute(label='Diag_PhControl1a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControl1b = attribute(label='Diag_PhControl1b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwtet2a = attribute(label='Diag_PhMuxfwtet2a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxcavb = attribute(label='Diag_PhMuxcavb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxcava = attribute(label='Diag_PhMuxcava',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwtet1b = attribute(label='Diag_PhMuxfwtet1b',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlfastpib = attribute(label='Diag_PhControlfastpib',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcircinloopsa = attribute(label='Diag_PhFwcircinloopsa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcircinloopsb = attribute(label='Diag_PhFwcircinloopsb',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlfastpia = attribute(label='Diag_PhControlfastpia',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcavloopsa = attribute(label='Diag_PhFwcavloopsa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwtet1a = attribute(label='Diag_PhMuxfwtet1a',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcavloopsb = attribute(label='Diag_PhFwcavloopsb',
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

    Diag_PhMoa = attribute(label='Diag_PhMoa',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlslowpia = attribute(label='Diag_PhControlslowpia',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlslowpib = attribute(label='Diag_PhControlslowpib',
                                   dtype=float,
                                   rel_change=DEFAULT_REL_CHANGE,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )


    perseusType = device_property(dtype=str, default_value='simulated')
    perseusIp = device_property(dtype=str, default_value='192.168.0.141')
    FDLPath = device_property(dtype=str, default_value='/tmp')

    def init_device(self):
        Device.init_device(self)
        try:
            self.perseus = Perseus().new_perseus(self.perseusType, self.perseusIp)
            self.set_events()
            self.set_state(DevState.ON)
        except Exception, e:
            print e
            self.set_state(DevState.FAULT)

    def set_events(self):
        self.set_change_event('KpA', True)
        self.set_change_event('KpB', True)
        self.set_change_event('KiA', True)
        self.set_change_event('KiB', True)
        self.set_change_event('PhaseShiftCavA', True)
        self.set_change_event('PhaseShiftCavB', True)
        self.set_change_event('PhaseShiftFwcavA', True)
        self.set_change_event('PhaseShiftFwcavB', True)
        self.set_change_event('PhaseShiftFwtet1A', True)
        self.set_change_event('PhaseShiftFwtet1B', True)
        self.set_change_event('PhaseShiftFwtet2A', True)
        self.set_change_event('PhaseShiftFwtet2B', True)
        self.set_change_event('PilimitA', True)
        self.set_change_event('PilimitB', True)
        self.set_change_event('SamplesToAverageA', True)
        self.set_change_event('SamplesToAverageB', True)
        self.set_change_event('FilterStagesA', True)
        self.set_change_event('FilterStagesB', True)
        self.set_change_event('PhaseShiftFwcircinA', True)
        self.set_change_event('PhaseShiftFwcircinB', True)
        self.set_change_event('PhaseShiftControlSignalTet1A', True)
        self.set_change_event('PhaseShiftControlSignalTet1B', True)
        self.set_change_event('PhaseShiftControlSignalTet2A', True)
        self.set_change_event('PhaseShiftControlSignalTet2B', True)
        self.set_change_event('GainTetrode1A', True)
        self.set_change_event('GainTetrode1B', True)
        self.set_change_event('GainTetrode2A', True)
        self.set_change_event('GainTetrode2B', True)
        self.set_change_event('AutomaticStartupEnableA', True)
        self.set_change_event('AutomaticStartupEnableB', True)
        self.set_change_event('CommandStartA', True)
        self.set_change_event('CommandStartB', True)
        self.set_change_event('AmprefinA', True)
        self.set_change_event('AmprefinB', True)
        self.set_change_event('PhrefinA', True)
        self.set_change_event('PhrefinB', True)
        self.set_change_event('AmprefminA', True)
        self.set_change_event('AmprefminB', True)
        self.set_change_event('PhrefminA', True)
        self.set_change_event('PhrefminB', True)
        self.set_change_event('PhaseIncreaseRateA', True)
        self.set_change_event('PhaseIncreaseRateB', True)
        self.set_change_event('VoltageIncreaseRateA', True)
        self.set_change_event('VoltageIncreaseRateB', True)
        self.set_change_event('GainOlA', True)
        self.set_change_event('GainOlB', True)
        self.set_change_event('SpareGpioOutput01A', True)
        self.set_change_event('SpareGpioOutput01B', True)
        self.set_change_event('SpareGpioOutput02A', True)
        self.set_change_event('SpareGpioOutput02B', True)
        self.set_change_event('SpareGpioOutput03A', True)
        self.set_change_event('SpareGpioOutput03B', True)
        self.set_change_event('SpareGpioOutput04A', True)
        self.set_change_event('SpareGpioOutput04B', True)
        self.set_change_event('FdlSwTriggerA', True)
        self.set_change_event('FdlSwTriggerB', True)
        self.set_change_event('SlowIqLoopEnableA', True)
        self.set_change_event('SlowIqLoopEnableB', True)
        self.set_change_event('AdcsPhaseshiftEnableA', True)
        self.set_change_event('AdcsPhaseshiftEnableB', True)
        self.set_change_event('DacsPhaseShiftEnableA', True)
        self.set_change_event('DacsPhaseShiftEnableB', True)
        self.set_change_event('SquarerefEnableA', True)
        self.set_change_event('SquarerefEnableB', True)
        self.set_change_event('FreqsquareA', True)
        self.set_change_event('FreqsquareB', True)
        self.set_change_event('LookRefA', True)
        self.set_change_event('LookRefB', True)
        self.set_change_event('QuadrantSelectionA', True)
        self.set_change_event('QuadrantSelectionB', True)
        self.set_change_event('SlowIqLoopInputSelectionA', True)
        self.set_change_event('SlowIqLoopInputSelectionB', True)
        self.set_change_event('FastIqLoopInputSelectionA', True)
        self.set_change_event('FastIqLoopInputSelectionB', True)
        self.set_change_event('AmplitudeLoopInputSelectionA', True)
        self.set_change_event('AmplitudeLoopInputSelectionB', True)
        self.set_change_event('PhaseLoopInputSelectionA', True)
        self.set_change_event('PhaseLoopInputSelectionB', True)
        self.set_change_event('PolarLoopsEnableA', True)
        self.set_change_event('PolarLoopsEnableB', True)
        self.set_change_event('FastIqLoopEnableA', True)
        self.set_change_event('FastIqLoopEnableB', True)
        self.set_change_event('AmplitudeLoopEnableA', True)
        self.set_change_event('AmplitudeLoopEnableB', True)
        self.set_change_event('PhaseLoopEnableA', True)
        self.set_change_event('PhaseLoopEnableB', True)
        self.set_change_event('KpFastIqLoopA', True)
        self.set_change_event('KpFastIqLoopB', True)
        self.set_change_event('KiFastIqLoopA', True)
        self.set_change_event('KiFastIqLoopB', True)
        self.set_change_event('KpAmpLoopA', True)
        self.set_change_event('KpAmpLoopB', True)
        self.set_change_event('KiAmpLoopA', True)
        self.set_change_event('KiAmpLoopB', True)
        self.set_change_event('KpPhaseLoopA', True)
        self.set_change_event('KpPhaseLoopB', True)
        self.set_change_event('KiPhaseLoopA', True)
        self.set_change_event('KiPhaseLoopB', True)
        self.set_change_event('PiLimitFastPiIqA', True)
        self.set_change_event('PiLimitFastPiIqB', True)
        self.set_change_event('PulseModeEnableA', True)
        self.set_change_event('PulseModeEnableB', True)
        self.set_change_event('AutomaticConditioningEnableA', True)
        self.set_change_event('AutomaticConditioningEnableB', True)
        self.set_change_event('ConditioningdutyCicleA', True)
        self.set_change_event('ConditioningdutyCicleB', True)
        self.set_change_event('TuningEnableA', True)
        self.set_change_event('TuningEnableB', True)
        self.set_change_event('TuningPosEnA', True)
        self.set_change_event('TuningPosEnB', True)
        self.set_change_event('NumStepsA', True)
        self.set_change_event('NumStepsB', True)
        self.set_change_event('PulsesFrequencyA', True)
        self.set_change_event('PulsesFrequencyB', True)
        self.set_change_event('PhaseOffsetA', True)
        self.set_change_event('PhaseOffsetB', True)
        self.set_change_event('MoveA', True)
        self.set_change_event('MoveB', True)
        self.set_change_event('MoveupA', True)
        self.set_change_event('MoveupB', True)
        self.set_change_event('TuningresetA', True)
        self.set_change_event('TuningresetB', True)
        self.set_change_event('FwminA', True)
        self.set_change_event('FwminB', True)
        self.set_change_event('MarginupA', True)
        self.set_change_event('MarginupB', True)
        self.set_change_event('MarginlowA', True)
        self.set_change_event('MarginlowB', True)
        self.set_change_event('TuningdelayA', True)
        self.set_change_event('TuningdelayB', True)
        self.set_change_event('TuningfilterenableA', True)
        self.set_change_event('TuningfilterenableB', True)
        self.set_change_event('TuningtriggerenableA', True)
        self.set_change_event('TuningtriggerenableB', True)
        self.set_change_event('EpsItckDisableA', True)
        self.set_change_event('EpsItckDisableB', True)
        self.set_change_event('FimItckDisableA', True)
        self.set_change_event('FimItckDisableB', True)
        self.set_change_event('MDividerA', True)
        self.set_change_event('MDividerB', True)
        self.set_change_event('NDividerA', True)
        self.set_change_event('NDividerB', True)
        self.set_change_event('MuxselA', True)
        self.set_change_event('MuxselB', True)
        self.set_change_event('Mux0DividerA', True)
        self.set_change_event('Mux0DividerB', True)
        self.set_change_event('Mux1DividerA', True)
        self.set_change_event('Mux1DividerB', True)
        self.set_change_event('Mux2DividerA', True)
        self.set_change_event('Mux2DividerB', True)
        self.set_change_event('Mux3DividerA', True)
        self.set_change_event('Mux3DividerB', True)
        self.set_change_event('Mux4DividerA', True)
        self.set_change_event('Mux4DividerB', True)
        self.set_change_event('SendWordA', True)
        self.set_change_event('SendWordB', True)
        self.set_change_event('CpdirA', True)
        self.set_change_event('CpdirB', True)
        self.set_change_event('VcxoOutputInversionA', True)
        self.set_change_event('VcxoOutputInversionB', True)
        self.set_change_event('Diag_IcavLoopsA', True)
        self.set_change_event('Diag_IcavLoopsB', True)
        self.set_change_event('Diag_QcavLoopsA', True)
        self.set_change_event('Diag_QcavLoopsB', True)
        self.set_change_event('Diag_IcontrolA', True)
        self.set_change_event('Diag_IcontrolB', True)
        self.set_change_event('Diag_QcontrolA', True)
        self.set_change_event('Diag_QcontrolB', True)
        self.set_change_event('Diag_Icontrol1A', True)
        self.set_change_event('Diag_Icontrol1B', True)
        self.set_change_event('Diag_Qcontrol1A', True)
        self.set_change_event('Diag_Qcontrol1B', True)
        self.set_change_event('Diag_Icontrol2A', True)
        self.set_change_event('Diag_Icontrol2B', True)
        self.set_change_event('Diag_Qcontrol2A', True)
        self.set_change_event('Diag_Qcontrol2B', True)
        self.set_change_event('Diag_IerrorA', True)
        self.set_change_event('Diag_IerrorB', True)
        self.set_change_event('Diag_QerrorA', True)
        self.set_change_event('Diag_QerrorB', True)
        self.set_change_event('Diag_IerroraccumA', True)
        self.set_change_event('Diag_IerroraccumB', True)
        self.set_change_event('Diag_QerroraccumA', True)
        self.set_change_event('Diag_QerroraccumB', True)
        self.set_change_event('Diag_IrefA', True)
        self.set_change_event('Diag_IrefB', True)
        self.set_change_event('Diag_QrefA', True)
        self.set_change_event('Diag_QrefB', True)
        self.set_change_event('Diag_IFwCavLoopsA', True)
        self.set_change_event('Diag_IFwCavLoopsB', True)
        self.set_change_event('Diag_QFwCavLoopsA', True)
        self.set_change_event('Diag_QFwCavLoopsB', True)
        self.set_change_event('Diag_IFwTet1LoopsA', True)
        self.set_change_event('Diag_IFwTet1LoopsB', True)
        self.set_change_event('Diag_QFwTet1LoopsA', True)
        self.set_change_event('Diag_QFwTet1LoopsB', True)
        self.set_change_event('Diag_IFwTet2LoopsA', True)
        self.set_change_event('Diag_IFwTet2LoopsB', True)
        self.set_change_event('Diag_QFwTet2LoopsA', True)
        self.set_change_event('Diag_QFwTet2LoopsB', True)
        self.set_change_event('Diag_IFwCircInLoopsA', True)
        self.set_change_event('Diag_IFwCircInLoopsB', True)
        self.set_change_event('Diag_QFwCircInLoopsA', True)
        self.set_change_event('Diag_QFwCircInLoopsB', True)
        self.set_change_event('Diag_ImoA', True)
        self.set_change_event('Diag_ImoB', True)
        self.set_change_event('Diag_QmoA', True)
        self.set_change_event('Diag_QmoB', True)
        self.set_change_event('Diag_Ispare1A', True)
        self.set_change_event('Diag_Ispare1B', True)
        self.set_change_event('Diag_Qspare1A', True)
        self.set_change_event('Diag_Qspare1B', True)
        self.set_change_event('Diag_Ispare2A', True)
        self.set_change_event('Diag_Ispare2B', True)
        self.set_change_event('Diag_Qspare2A', True)
        self.set_change_event('Diag_Qspare2B', True)
        self.set_change_event('Diag_IMuxCavA', True)
        self.set_change_event('Diag_IMuxCavB', True)
        self.set_change_event('Diag_QMuxCavA', True)
        self.set_change_event('Diag_QMuxCavB', True)
        self.set_change_event('Diag_IMuxFwCavA', True)
        self.set_change_event('Diag_IMuxFwCavB', True)
        self.set_change_event('Diag_QMuxFwCavA', True)
        self.set_change_event('Diag_QMuxFwCavB', True)
        self.set_change_event('Diag_IMuxFwTet1A', True)
        self.set_change_event('Diag_IMuxFwTet1B', True)
        self.set_change_event('Diag_QMuxFwTet1A', True)
        self.set_change_event('Diag_QMuxFwTet1B', True)
        self.set_change_event('Diag_IMuxFwTet2A', True)
        self.set_change_event('Diag_IMuxFwTet2B', True)
        self.set_change_event('Diag_QMuxFwTet2A', True)
        self.set_change_event('Diag_QMuxFwTet2B', True)
        self.set_change_event('Diag_IMuxFwCircInA', True)
        self.set_change_event('Diag_IMuxFwCircInB', True)
        self.set_change_event('Diag_QMuxFwCircInA', True)
        self.set_change_event('Diag_QMuxFwCircInB', True)
        self.set_change_event('Diag_AmpCavA', True)
        self.set_change_event('Diag_AmpCavB', True)
        self.set_change_event('Diag_AmpFwA', True)
        self.set_change_event('Diag_AmpFwB', True)
        self.set_change_event('Diag_AngCavFwA', True)
        self.set_change_event('Diag_AngCavFwB', True)
        self.set_change_event('Diag_AngCavLA', True)
        self.set_change_event('Diag_AngCavLB', True)
        self.set_change_event('Diag_AngFwLA', True)
        self.set_change_event('Diag_AngFwLB', True)
        self.set_change_event('Diag_Vaccum1A', True)
        self.set_change_event('Diag_Vaccum1B', True)
        self.set_change_event('Diag_Vaccum2A', True)
        self.set_change_event('Diag_Vaccum2B', True)
        self.set_change_event('Diag_IcontrolSlowpiA', True)
        self.set_change_event('Diag_IcontrolSlowpiB', True)
        self.set_change_event('Diag_QcontrolSlowpiA', True)
        self.set_change_event('Diag_QcontrolSlowpiB', True)
        self.set_change_event('Diag_IcontrolFastpiA', True)
        self.set_change_event('Diag_IcontrolFastpiB', True)
        self.set_change_event('Diag_QcontrolFastpiA', True)
        self.set_change_event('Diag_QcontrolFastpiB', True)
        self.set_change_event('Diag_VcxoPoweredA', True)
        self.set_change_event('Diag_VcxoPoweredB', True)
        self.set_change_event('Diag_VcxoRefA', True)
        self.set_change_event('Diag_VcxoRefB', True)
        self.set_change_event('Diag_VcxoLockedA', True)
        self.set_change_event('Diag_VcxoLockedB', True)
        self.set_change_event('Diag_VcxoCableDisconnectedA', True)
        self.set_change_event('Diag_VcxoCableDisconnectedB', True)
        self.set_change_event('Diag_IpolarForAmplitudeLoopA', True)
        self.set_change_event('Diag_IpolarForAmplitudeLoopB', True)
        self.set_change_event('Diag_QpolarForAmplitudeLoopA', True)
        self.set_change_event('Diag_QpolarForAmplitudeLoopB', True)
        self.set_change_event('Diag_IpolarForPhaseLoopA', True)
        self.set_change_event('Diag_IpolarForPhaseLoopB', True)
        self.set_change_event('Diag_QpolarForPhaseLoopA', True)
        self.set_change_event('Diag_QpolarForPhaseLoopB', True)
        self.set_change_event('Diag_AmpInputOfAmpLoopA', True)
        self.set_change_event('Diag_AmpInputOfAmpLoopB', True)
        self.set_change_event('Diag_PhaseInputOfAmpLoopA', True)
        self.set_change_event('Diag_PhaseInputOfAmpLoopB', True)
        self.set_change_event('Diag_AmpInputOfPhaseLoopA', True)
        self.set_change_event('Diag_AmpInputOfPhaseLoopB', True)
        self.set_change_event('Diag_PhInputOfPhaseLoopA', True)
        self.set_change_event('Diag_PhInputOfPhaseLoopB', True)
        self.set_change_event('Diag_AmpLoopControlOutputA', True)
        self.set_change_event('Diag_AmpLoopControlOutputB', True)
        self.set_change_event('Diag_AmpLoopErrorA', True)
        self.set_change_event('Diag_AmpLoopErrorB', True)
        self.set_change_event('Diag_AmpLoopErrorAccumA', True)
        self.set_change_event('Diag_AmpLoopErrorAccumB', True)
        self.set_change_event('Diag_PhLoopControlOutputA', True)
        self.set_change_event('Diag_PhLoopControlOutputB', True)
        self.set_change_event('Diag_PhLoopErrorA', True)
        self.set_change_event('Diag_PhLoopErrorB', True)
        self.set_change_event('Diag_PhLoopErrorAccumA', True)
        self.set_change_event('Diag_PhLoopErrorAccumB', True)
        self.set_change_event('Diag_IpolarControlOutputA', True)
        self.set_change_event('Diag_IpolarControlOutputB', True)
        self.set_change_event('Diag_QpolarControlOutputA', True)
        self.set_change_event('Diag_QpolarControlOutputB', True)
        self.set_change_event('Diag_IcontrolSlowpiIqA', True)
        self.set_change_event('Diag_IcontrolSlowpiIqB', True)
        self.set_change_event('Diag_QcontrolSlowpiqA', True)
        self.set_change_event('Diag_QcontrolSlowpiqB', True)
        self.set_change_event('Diag_IcontrolFastpiIqA', True)
        self.set_change_event('Diag_IcontrolFastpiIqB', True)
        self.set_change_event('Diag_QcontrolFastpiIqA', True)
        self.set_change_event('Diag_QcontrolFastpiIqB', True)
        self.set_change_event('Diag_IloopinputSlowpiIqA', True)
        self.set_change_event('Diag_IloopinputSlowpiIqB', True)
        self.set_change_event('Diag_QloopinputSlowpiIqA', True)
        self.set_change_event('Diag_QloopinputSlowpiIqB', True)
        self.set_change_event('Diag_IloopinputFastpiIqA', True)
        self.set_change_event('Diag_IloopinputFastpiIqB', True)
        self.set_change_event('Diag_QloopinputFastpiIqA', True)
        self.set_change_event('Diag_QloopinputFastpiIqB', True)
        self.set_change_event('Diag_IrefloopinputFastpiIqA', True)
        self.set_change_event('Diag_IrefloopinputFastpiIqB', True)
        self.set_change_event('Diag_QrefloopinputFastpiIqA', True)
        self.set_change_event('Diag_QrefloopinputFastpiIqB', True)
        self.set_change_event('Diag_MovingPlungerAutoA', True)
        self.set_change_event('Diag_MovingPlungerAutoB', True)
        self.set_change_event('Diag_FreqUpA', True)
        self.set_change_event('Diag_FreqUpB', True)
        self.set_change_event('Diag_ManualTuningOnA', True)
        self.set_change_event('Diag_ManualTuningOnB', True)
        self.set_change_event('Diag_ManualTuningFreqUpA', True)
        self.set_change_event('Diag_ManualTuningFreqUpB', True)
        self.set_change_event('Diag_FwminA', True)
        self.set_change_event('Diag_FwminB', True)
        self.set_change_event('Diag_EpsItckDelayA', True)
        self.set_change_event('Diag_EpsItckDelayB', True)
        self.set_change_event('Diag_FimItckDelayA', True)
        self.set_change_event('Diag_FimItckDelayB', True)
        self.set_change_event('Diag_FdlTrigHwInputA', True)
        self.set_change_event('Diag_FdlTrigHwInputB', True)
        self.set_change_event('Diag_FdlTrigSwInputA', True)
        self.set_change_event('Diag_FdlTrigSwInputB', True)
        self.set_change_event('Diag_EpsItckA', True)
        self.set_change_event('Diag_EpsItckB', True)
        self.set_change_event('Diag_AmpMuxfwcircina', True)
        self.set_change_event('Diag_AmpSpare1a', True)
        self.set_change_event('Diag_AmpMuxfwcircinb', True)
        self.set_change_event('Diag_AmpSpare2a', True)
        self.set_change_event('Diag_AmpSpare2b', True)
        self.set_change_event('Diag_AmpErrora', True)
        self.set_change_event('Diag_AmpErrorb', True)
        self.set_change_event('Diag_AmpSpare1b', True)
        self.set_change_event('Diag_AmpErroraccumb', True)
        self.set_change_event('Diag_AmpErroraccuma', True)
        self.set_change_event('Diag_AmpControlfastpiiqb', True)
        self.set_change_event('Diag_AmpControlfastpiiqa', True)
        self.set_change_event('Diag_AmpControla', True)
        self.set_change_event('Diag_AmpPolarforamplitudeloopa', True)
        self.set_change_event('Diag_AmpPolarforamplitudeloopb', True)
        self.set_change_event('Diag_AmpControlb', True)
        self.set_change_event('Diag_AmpMuxfwtet2b', True)
        self.set_change_event('Diag_AmpLoopinputfastpiiqb', True)
        self.set_change_event('Diag_AmpLoopinputfastpiiqa', True)
        self.set_change_event('Diag_AmpRefa', True)
        self.set_change_event('Diag_AmpMuxfwcava', True)
        self.set_change_event('Diag_AmpMuxfwcavb', True)
        self.set_change_event('Diag_AmpRefb', True)
        self.set_change_event('Diag_AmpControl2a', True)
        self.set_change_event('Diag_AmpControl2b', True)
        self.set_change_event('Diag_AmpFwtet1loopsb', True)
        self.set_change_event('Diag_AmpFwtet1loopsa', True)
        self.set_change_event('Diag_AmpPolarforphaseloopb', True)
        self.set_change_event('Diag_AmpPolarforphaseloopa', True)
        self.set_change_event('Diag_AmpPolarcontroloutputb', True)
        self.set_change_event('Diag_AmpPolarcontroloutputa', True)
        self.set_change_event('Diag_AmpFwtet2loopsa', True)
        self.set_change_event('Diag_AmpCavloopsa', True)
        self.set_change_event('Diag_AmpCavloopsb', True)
        self.set_change_event('Diag_AmpFwtet2loopsb', True)
        self.set_change_event('Diag_AmpLoopinputslowpiiqa', True)
        self.set_change_event('Diag_AmpLoopinputslowpiiqb', True)
        self.set_change_event('Diag_AmpRefloopinputfastpiiqb', True)
        self.set_change_event('Diag_AmpRefloopinputfastpiiqa', True)
        self.set_change_event('Diag_AmpControl1a', True)
        self.set_change_event('Diag_AmpControl1b', True)
        self.set_change_event('Diag_AmpMuxfwtet2a', True)
        self.set_change_event('Diag_AmpMuxcavb', True)
        self.set_change_event('Diag_AmpMuxcava', True)
        self.set_change_event('Diag_AmpMuxfwtet1b', True)
        self.set_change_event('Diag_AmpControlfastpib', True)
        self.set_change_event('Diag_AmpFwcircinloopsa', True)
        self.set_change_event('Diag_AmpFwcircinloopsb', True)
        self.set_change_event('Diag_AmpControlfastpia', True)
        self.set_change_event('Diag_AmpFwcavloopsa', True)
        self.set_change_event('Diag_AmpMuxfwtet1a', True)
        self.set_change_event('Diag_AmpFwcavloopsb', True)
        self.set_change_event('Diag_AmpMob', True)
        self.set_change_event('Diag_AmpMoa', True)
        self.set_change_event('Diag_AmpControlslowpia', True)
        self.set_change_event('Diag_AmpControlslowpib', True)
        self.set_change_event('Diag_PhMuxfwcircina', True)
        self.set_change_event('Diag_PhSpare1a', True)
        self.set_change_event('Diag_PhMuxfwcircinb', True)
        self.set_change_event('Diag_PhSpare2a', True)
        self.set_change_event('Diag_PhSpare2b', True)
        self.set_change_event('Diag_PhErrora', True)
        self.set_change_event('Diag_PhErrorb', True)
        self.set_change_event('Diag_PhSpare1b', True)
        self.set_change_event('Diag_PhErroraccumb', True)
        self.set_change_event('Diag_PhErroraccuma', True)
        self.set_change_event('Diag_PhControlfastpiiqb', True)
        self.set_change_event('Diag_PhControlfastpiiqa', True)
        self.set_change_event('Diag_PhControla', True)
        self.set_change_event('Diag_PhPolarforamplitudeloopa', True)
        self.set_change_event('Diag_PhPolarforamplitudeloopb', True)
        self.set_change_event('Diag_PhControlb', True)
        self.set_change_event('Diag_PhMuxfwtet2b', True)
        self.set_change_event('Diag_PhLoopinputfastpiiqb', True)
        self.set_change_event('Diag_PhLoopinputfastpiiqa', True)
        self.set_change_event('Diag_PhRefa', True)
        self.set_change_event('Diag_PhMuxfwcava', True)
        self.set_change_event('Diag_PhMuxfwcavb', True)
        self.set_change_event('Diag_PhRefb', True)
        self.set_change_event('Diag_PhControl2a', True)
        self.set_change_event('Diag_PhControl2b', True)
        self.set_change_event('Diag_PhFwtet1loopsb', True)
        self.set_change_event('Diag_PhFwtet1loopsa', True)
        self.set_change_event('Diag_PhPolarforphaseloopb', True)
        self.set_change_event('Diag_PhPolarforphaseloopa', True)
        self.set_change_event('Diag_PhPolarcontroloutputb', True)
        self.set_change_event('Diag_PhPolarcontroloutputa', True)
        self.set_change_event('Diag_PhFwtet2loopsa', True)
        self.set_change_event('Diag_PhCavloopsa', True)
        self.set_change_event('Diag_PhCavloopsb', True)
        self.set_change_event('Diag_PhFwtet2loopsb', True)
        self.set_change_event('Diag_PhLoopinputslowpiiqa', True)
        self.set_change_event('Diag_PhLoopinputslowpiiqb', True)
        self.set_change_event('Diag_PhRefloopinputfastpiiqb', True)
        self.set_change_event('Diag_PhRefloopinputfastpiiqa', True)
        self.set_change_event('Diag_PhControl1a', True)
        self.set_change_event('Diag_PhControl1b', True)
        self.set_change_event('Diag_PhMuxfwtet2a', True)
        self.set_change_event('Diag_PhMuxcavb', True)
        self.set_change_event('Diag_PhMuxcava', True)
        self.set_change_event('Diag_PhMuxfwtet1b', True)
        self.set_change_event('Diag_PhControlfastpib', True)
        self.set_change_event('Diag_PhFwcircinloopsa', True)
        self.set_change_event('Diag_PhFwcircinloopsb', True)
        self.set_change_event('Diag_PhControlfastpia', True)
        self.set_change_event('Diag_PhFwcavloopsa', True)
        self.set_change_event('Diag_PhMuxfwtet1a', True)
        self.set_change_event('Diag_PhFwcavloopsb', True)
        self.set_change_event('Diag_PhMob', True)
        self.set_change_event('Diag_PhMoa', True)
        self.set_change_event('Diag_PhControlslowpia', True)
        self.set_change_event('Diag_PhControlslowpib', True)


    @DebugIt()
    def get_KpA(self):
        return perseus_utils.read_direct(self.perseus, 0, 'A')

    @DebugIt()
    def set_KpA(self, KpA):
        perseus_utils.write_direct(self.perseus, KpA, 0, 'A')
        self.push_change_event("KpA", KpA)

    @DebugIt()
    def get_KpB(self):
        return perseus_utils.read_direct(self.perseus, 0, 'B')

    @DebugIt()
    def set_KpB(self, KpB):
        perseus_utils.write_direct(self.perseus, KpB, 0, 'B')
        self.push_change_event("KpB", KpB)

    @DebugIt()
    def get_KiA(self):
        return perseus_utils.read_direct(self.perseus, 1, 'A')

    @DebugIt()
    def set_KiA(self, KiA):
        perseus_utils.write_direct(self.perseus, KiA, 1, 'A')
        self.push_change_event("KiA", KiA)

    @DebugIt()
    def get_KiB(self):
        return perseus_utils.read_direct(self.perseus, 1, 'B')

    @DebugIt()
    def set_KiB(self, KiB):
        perseus_utils.write_direct(self.perseus, KiB, 1, 'B')
        self.push_change_event("KiB", KiB)

    @DebugIt()
    def get_PhaseShiftCavA(self):
        return perseus_utils.read_angle(self.perseus, 2, 'A')

    @DebugIt()
    def set_PhaseShiftCavA(self, PhaseShiftCavA):
        perseus_utils.write_angle(self.perseus, PhaseShiftCavA, 2, 'A')
        self.push_change_event("PhaseShiftCavA", PhaseShiftCavA)

    @DebugIt()
    def get_PhaseShiftCavB(self):
        return perseus_utils.read_angle(self.perseus, 2, 'B')

    @DebugIt()
    def set_PhaseShiftCavB(self, PhaseShiftCavB):
        perseus_utils.write_angle(self.perseus, PhaseShiftCavB, 2, 'B')
        self.push_change_event("PhaseShiftCavB", PhaseShiftCavB)

    @DebugIt()
    def get_PhaseShiftFwcavA(self):
        return perseus_utils.read_angle(self.perseus, 3, 'A')

    @DebugIt()
    def set_PhaseShiftFwcavA(self, PhaseShiftFwcavA):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwcavA, 3, 'A')
        self.push_change_event("PhaseShiftFwcavA", PhaseShiftFwcavA)

    @DebugIt()
    def get_PhaseShiftFwcavB(self):
        return perseus_utils.read_angle(self.perseus, 3, 'B')

    @DebugIt()
    def set_PhaseShiftFwcavB(self, PhaseShiftFwcavB):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwcavB, 3, 'B')
        self.push_change_event("PhaseShiftFwcavB", PhaseShiftFwcavB)

    @DebugIt()
    def get_PhaseShiftFwtet1A(self):
        return perseus_utils.read_angle(self.perseus, 4, 'A')

    @DebugIt()
    def set_PhaseShiftFwtet1A(self, PhaseShiftFwtet1A):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwtet1A, 4, 'A')
        self.push_change_event("PhaseShiftFwtet1A", PhaseShiftFwtet1A)

    @DebugIt()
    def get_PhaseShiftFwtet1B(self):
        return perseus_utils.read_angle(self.perseus, 4, 'B')

    @DebugIt()
    def set_PhaseShiftFwtet1B(self, PhaseShiftFwtet1B):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwtet1B, 4, 'B')
        self.push_change_event("PhaseShiftFwtet1B", PhaseShiftFwtet1B)

    @DebugIt()
    def get_PhaseShiftFwtet2A(self):
        return perseus_utils.read_angle(self.perseus, 5, 'A')

    @DebugIt()
    def set_PhaseShiftFwtet2A(self, PhaseShiftFwtet2A):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwtet2A, 5, 'A')
        self.push_change_event("PhaseShiftFwtet2A", PhaseShiftFwtet2A)

    @DebugIt()
    def get_PhaseShiftFwtet2B(self):
        return perseus_utils.read_angle(self.perseus, 5, 'B')

    @DebugIt()
    def set_PhaseShiftFwtet2B(self, PhaseShiftFwtet2B):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwtet2B, 5, 'B')
        self.push_change_event("PhaseShiftFwtet2B", PhaseShiftFwtet2B)

    @DebugIt()
    def get_PilimitA(self):
        address = 6
        cavity = 'A'
        #@todo: add this method to special methods library ...
        return extra_func.get_Pilimit(self.perseus, address, cavity)

    @DebugIt()
    def set_PilimitA(self, PilimitA):
        address = 6
        cavity = 'A'
        #@todo: add this method to special methods library ...
        extra_func.set_Pilimit(self.perseus, PilimitA, address, cavity)
        self.push_change_event("PilimitA", PilimitA)

    @DebugIt()
    def get_PilimitB(self):
        address = 6
        cavity = 'B'
        #@todo: add this method to special methods library ...
        return extra_func.get_Pilimit(self.perseus, address, cavity)

    @DebugIt()
    def set_PilimitB(self, PilimitB):
        address = 6
        cavity = 'B'
        #@todo: add this method to special methods library ...
        extra_func.set_Pilimit(self.perseus, PilimitB, address, cavity)
        self.push_change_event("PilimitB", PilimitB)

    @DebugIt()
    def get_SamplesToAverageA(self):
        return perseus_utils.read_direct(self.perseus, 7, 'A')

    @DebugIt()
    def set_SamplesToAverageA(self, SamplesToAverageA):
        perseus_utils.write_direct(self.perseus, SamplesToAverageA, 7, 'A')
        self.push_change_event("SamplesToAverageA", SamplesToAverageA)

    @DebugIt()
    def get_SamplesToAverageB(self):
        return perseus_utils.read_direct(self.perseus, 7, 'B')

    @DebugIt()
    def set_SamplesToAverageB(self, SamplesToAverageB):
        perseus_utils.write_direct(self.perseus, SamplesToAverageB, 7, 'B')
        self.push_change_event("SamplesToAverageB", SamplesToAverageB)

    @DebugIt()
    def get_FilterStagesA(self):
        return perseus_utils.read_direct(self.perseus, 8, 'A')

    @DebugIt()
    def set_FilterStagesA(self, FilterStagesA):
        perseus_utils.write_direct(self.perseus, FilterStagesA, 8, 'A')
        self.push_change_event("FilterStagesA", FilterStagesA)

    @DebugIt()
    def get_FilterStagesB(self):
        return perseus_utils.read_direct(self.perseus, 8, 'B')

    @DebugIt()
    def set_FilterStagesB(self, FilterStagesB):
        perseus_utils.write_direct(self.perseus, FilterStagesB, 8, 'B')
        self.push_change_event("FilterStagesB", FilterStagesB)

    @DebugIt()
    def get_PhaseShiftFwcircinA(self):
        return perseus_utils.read_angle(self.perseus, 9, 'A')

    @DebugIt()
    def set_PhaseShiftFwcircinA(self, PhaseShiftFwcircinA):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwcircinA, 9, 'A')
        self.push_change_event("PhaseShiftFwcircinA", PhaseShiftFwcircinA)

    @DebugIt()
    def get_PhaseShiftFwcircinB(self):
        return perseus_utils.read_angle(self.perseus, 9, 'B')

    @DebugIt()
    def set_PhaseShiftFwcircinB(self, PhaseShiftFwcircinB):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwcircinB, 9, 'B')
        self.push_change_event("PhaseShiftFwcircinB", PhaseShiftFwcircinB)

    @DebugIt()
    def get_PhaseShiftControlSignalTet1A(self):
        return perseus_utils.read_angle(self.perseus, 10, 'A')

    @DebugIt()
    def set_PhaseShiftControlSignalTet1A(self, PhaseShiftControlSignalTet1A):
        perseus_utils.write_angle(self.perseus, PhaseShiftControlSignalTet1A, 10, 'A')
        self.push_change_event("PhaseShiftControlSignalTet1A", PhaseShiftControlSignalTet1A)

    @DebugIt()
    def get_PhaseShiftControlSignalTet1B(self):
        return perseus_utils.read_angle(self.perseus, 10, 'B')

    @DebugIt()
    def set_PhaseShiftControlSignalTet1B(self, PhaseShiftControlSignalTet1B):
        perseus_utils.write_angle(self.perseus, PhaseShiftControlSignalTet1B, 10, 'B')
        self.push_change_event("PhaseShiftControlSignalTet1B", PhaseShiftControlSignalTet1B)

    @DebugIt()
    def get_PhaseShiftControlSignalTet2A(self):
        return perseus_utils.read_angle(self.perseus, 11, 'A')

    @DebugIt()
    def set_PhaseShiftControlSignalTet2A(self, PhaseShiftControlSignalTet2A):
        perseus_utils.write_angle(self.perseus, PhaseShiftControlSignalTet2A, 11, 'A')
        self.push_change_event("PhaseShiftControlSignalTet2A", PhaseShiftControlSignalTet2A)

    @DebugIt()
    def get_PhaseShiftControlSignalTet2B(self):
        return perseus_utils.read_angle(self.perseus, 11, 'B')

    @DebugIt()
    def set_PhaseShiftControlSignalTet2B(self, PhaseShiftControlSignalTet2B):
        perseus_utils.write_angle(self.perseus, PhaseShiftControlSignalTet2B, 11, 'B')
        self.push_change_event("PhaseShiftControlSignalTet2B", PhaseShiftControlSignalTet2B)

    @DebugIt()
    def get_GainTetrode1A(self):
        address = 13
        cavity = 'A'
        #@todo: add this method to special methods library ...
        return extra_func.get_GainTetrode1(self.perseus, address, cavity)

    @DebugIt()
    def set_GainTetrode1A(self, GainTetrode1A):
        address = 13
        cavity = 'A'
        #@todo: add this method to special methods library ...
        extra_func.set_GainTetrode1(self.perseus, GainTetrode1A, address, cavity)
        self.push_change_event("GainTetrode1A", GainTetrode1A)

    @DebugIt()
    def get_GainTetrode1B(self):
        address = 13
        cavity = 'B'
        #@todo: add this method to special methods library ...
        return extra_func.get_GainTetrode1(self.perseus, address, cavity)

    @DebugIt()
    def set_GainTetrode1B(self, GainTetrode1B):
        address = 13
        cavity = 'B'
        #@todo: add this method to special methods library ...
        extra_func.set_GainTetrode1(self.perseus, GainTetrode1B, address, cavity)
        self.push_change_event("GainTetrode1B", GainTetrode1B)

    @DebugIt()
    def get_GainTetrode2A(self):
        address = 14
        cavity = 'A'
        #@todo: add this method to special methods library ...
        return extra_func.get_GainTetrode2(self.perseus, address, cavity)

    @DebugIt()
    def set_GainTetrode2A(self, GainTetrode2A):
        address = 14
        cavity = 'A'
        #@todo: add this method to special methods library ...
        extra_func.set_GainTetrode2(self.perseus, GainTetrode2A, address, cavity)
        self.push_change_event("GainTetrode2A", GainTetrode2A)

    @DebugIt()
    def get_GainTetrode2B(self):
        address = 14
        cavity = 'B'
        #@todo: add this method to special methods library ...
        return extra_func.get_GainTetrode2(self.perseus, address, cavity)

    @DebugIt()
    def set_GainTetrode2B(self, GainTetrode2B):
        address = 14
        cavity = 'B'
        #@todo: add this method to special methods library ...
        extra_func.set_GainTetrode2(self.perseus, GainTetrode2B, address, cavity)
        self.push_change_event("GainTetrode2B", GainTetrode2B)

    @DebugIt()
    def get_AutomaticStartupEnableA(self):
        return perseus_utils.read_direct(self.perseus, 15, 'A')

    @DebugIt()
    def set_AutomaticStartupEnableA(self, AutomaticStartupEnableA):
        perseus_utils.write_direct(self.perseus, AutomaticStartupEnableA, 15, 'A')
        self.push_change_event("AutomaticStartupEnableA", AutomaticStartupEnableA)

    @DebugIt()
    def get_AutomaticStartupEnableB(self):
        return perseus_utils.read_direct(self.perseus, 15, 'B')

    @DebugIt()
    def set_AutomaticStartupEnableB(self, AutomaticStartupEnableB):
        perseus_utils.write_direct(self.perseus, AutomaticStartupEnableB, 15, 'B')
        self.push_change_event("AutomaticStartupEnableB", AutomaticStartupEnableB)

    @DebugIt()
    def get_CommandStartA(self):
        return perseus_utils.read_direct(self.perseus, 16, 'A')

    @DebugIt()
    def set_CommandStartA(self, CommandStartA):
        perseus_utils.write_direct(self.perseus, CommandStartA, 16, 'A')
        self.push_change_event("CommandStartA", CommandStartA)

    @DebugIt()
    def get_CommandStartB(self):
        return perseus_utils.read_direct(self.perseus, 16, 'B')

    @DebugIt()
    def set_CommandStartB(self, CommandStartB):
        perseus_utils.write_direct(self.perseus, CommandStartB, 16, 'B')
        self.push_change_event("CommandStartB", CommandStartB)

    @DebugIt()
    def get_AmprefinA(self):
        return perseus_utils.read_milivolts(self.perseus, 19, 'A')

    @DebugIt()
    def set_AmprefinA(self, AmprefinA):
        perseus_utils.write_milivolts(self.perseus, AmprefinA, 19, 'A')
        self.push_change_event("AmprefinA", AmprefinA)

    @DebugIt()
    def get_AmprefinB(self):
        return perseus_utils.read_milivolts(self.perseus, 19, 'B')

    @DebugIt()
    def set_AmprefinB(self, AmprefinB):
        perseus_utils.write_milivolts(self.perseus, AmprefinB, 19, 'B')
        self.push_change_event("AmprefinB", AmprefinB)

    @DebugIt()
    def get_PhrefinA(self):
        return perseus_utils.read_angle(self.perseus, 20, 'A')

    @DebugIt()
    def set_PhrefinA(self, PhrefinA):
        perseus_utils.write_angle(self.perseus, PhrefinA, 20, 'A')
        self.push_change_event("PhrefinA", PhrefinA)

    @DebugIt()
    def get_PhrefinB(self):
        return perseus_utils.read_angle(self.perseus, 20, 'B')

    @DebugIt()
    def set_PhrefinB(self, PhrefinB):
        perseus_utils.write_angle(self.perseus, PhrefinB, 20, 'B')
        self.push_change_event("PhrefinB", PhrefinB)

    @DebugIt()
    def get_AmprefminA(self):
        return perseus_utils.read_milivolts(self.perseus, 21, 'A')

    @DebugIt()
    def set_AmprefminA(self, AmprefminA):
        perseus_utils.write_milivolts(self.perseus, AmprefminA, 21, 'A')
        self.push_change_event("AmprefminA", AmprefminA)

    @DebugIt()
    def get_AmprefminB(self):
        return perseus_utils.read_milivolts(self.perseus, 21, 'B')

    @DebugIt()
    def set_AmprefminB(self, AmprefminB):
        perseus_utils.write_milivolts(self.perseus, AmprefminB, 21, 'B')
        self.push_change_event("AmprefminB", AmprefminB)

    @DebugIt()
    def get_PhrefminA(self):
        return perseus_utils.read_angle(self.perseus, 22, 'A')

    @DebugIt()
    def set_PhrefminA(self, PhrefminA):
        perseus_utils.write_angle(self.perseus, PhrefminA, 22, 'A')
        self.push_change_event("PhrefminA", PhrefminA)

    @DebugIt()
    def get_PhrefminB(self):
        return perseus_utils.read_angle(self.perseus, 22, 'B')

    @DebugIt()
    def set_PhrefminB(self, PhrefminB):
        perseus_utils.write_angle(self.perseus, PhrefminB, 22, 'B')
        self.push_change_event("PhrefminB", PhrefminB)

    @DebugIt()
    def get_PhaseIncreaseRateA(self):
        return perseus_utils.read_direct(self.perseus, 23, 'A')

    @DebugIt()
    def set_PhaseIncreaseRateA(self, PhaseIncreaseRateA):
        perseus_utils.write_direct(self.perseus, PhaseIncreaseRateA, 23, 'A')
        self.push_change_event("PhaseIncreaseRateA", PhaseIncreaseRateA)

    @DebugIt()
    def get_PhaseIncreaseRateB(self):
        return perseus_utils.read_direct(self.perseus, 23, 'B')

    @DebugIt()
    def set_PhaseIncreaseRateB(self, PhaseIncreaseRateB):
        perseus_utils.write_direct(self.perseus, PhaseIncreaseRateB, 23, 'B')
        self.push_change_event("PhaseIncreaseRateB", PhaseIncreaseRateB)

    @DebugIt()
    def get_VoltageIncreaseRateA(self):
        return perseus_utils.read_direct(self.perseus, 24, 'A')

    @DebugIt()
    def set_VoltageIncreaseRateA(self, VoltageIncreaseRateA):
        perseus_utils.write_direct(self.perseus, VoltageIncreaseRateA, 24, 'A')
        self.push_change_event("VoltageIncreaseRateA", VoltageIncreaseRateA)

    @DebugIt()
    def get_VoltageIncreaseRateB(self):
        return perseus_utils.read_direct(self.perseus, 24, 'B')

    @DebugIt()
    def set_VoltageIncreaseRateB(self, VoltageIncreaseRateB):
        perseus_utils.write_direct(self.perseus, VoltageIncreaseRateB, 24, 'B')
        self.push_change_event("VoltageIncreaseRateB", VoltageIncreaseRateB)

    @DebugIt()
    def get_GainOlA(self):
        address = 25
        cavity = 'A'
        #@todo: add this method to special methods library ...
        return extra_func.get_GainOl(self.perseus, address, cavity)

    @DebugIt()
    def set_GainOlA(self, GainOlA):
        address = 25
        cavity = 'A'
        #@todo: add this method to special methods library ...
        extra_func.set_GainOl(self.perseus, GainOlA, address, cavity)
        self.push_change_event("GainOlA", GainOlA)

    @DebugIt()
    def get_GainOlB(self):
        address = 25
        cavity = 'B'
        #@todo: add this method to special methods library ...
        return extra_func.get_GainOl(self.perseus, address, cavity)

    @DebugIt()
    def set_GainOlB(self, GainOlB):
        address = 25
        cavity = 'B'
        #@todo: add this method to special methods library ...
        extra_func.set_GainOl(self.perseus, GainOlB, address, cavity)
        self.push_change_event("GainOlB", GainOlB)

    @DebugIt()
    def get_SpareGpioOutput01A(self):
        return perseus_utils.read_direct(self.perseus, 28, 'A')

    @DebugIt()
    def set_SpareGpioOutput01A(self, SpareGpioOutput01A):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput01A, 28, 'A')
        self.push_change_event("SpareGpioOutput01A", SpareGpioOutput01A)

    @DebugIt()
    def get_SpareGpioOutput01B(self):
        return perseus_utils.read_direct(self.perseus, 28, 'B')

    @DebugIt()
    def set_SpareGpioOutput01B(self, SpareGpioOutput01B):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput01B, 28, 'B')
        self.push_change_event("SpareGpioOutput01B", SpareGpioOutput01B)

    @DebugIt()
    def get_SpareGpioOutput02A(self):
        return perseus_utils.read_direct(self.perseus, 29, 'A')

    @DebugIt()
    def set_SpareGpioOutput02A(self, SpareGpioOutput02A):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput02A, 29, 'A')
        self.push_change_event("SpareGpioOutput02A", SpareGpioOutput02A)

    @DebugIt()
    def get_SpareGpioOutput02B(self):
        return perseus_utils.read_direct(self.perseus, 29, 'B')

    @DebugIt()
    def set_SpareGpioOutput02B(self, SpareGpioOutput02B):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput02B, 29, 'B')
        self.push_change_event("SpareGpioOutput02B", SpareGpioOutput02B)

    @DebugIt()
    def get_SpareGpioOutput03A(self):
        return perseus_utils.read_direct(self.perseus, 30, 'A')

    @DebugIt()
    def set_SpareGpioOutput03A(self, SpareGpioOutput03A):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput03A, 30, 'A')
        self.push_change_event("SpareGpioOutput03A", SpareGpioOutput03A)

    @DebugIt()
    def get_SpareGpioOutput03B(self):
        return perseus_utils.read_direct(self.perseus, 30, 'B')

    @DebugIt()
    def set_SpareGpioOutput03B(self, SpareGpioOutput03B):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput03B, 30, 'B')
        self.push_change_event("SpareGpioOutput03B", SpareGpioOutput03B)

    @DebugIt()
    def get_SpareGpioOutput04A(self):
        return perseus_utils.read_direct(self.perseus, 31, 'A')

    @DebugIt()
    def set_SpareGpioOutput04A(self, SpareGpioOutput04A):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput04A, 31, 'A')
        self.push_change_event("SpareGpioOutput04A", SpareGpioOutput04A)

    @DebugIt()
    def get_SpareGpioOutput04B(self):
        return perseus_utils.read_direct(self.perseus, 31, 'B')

    @DebugIt()
    def set_SpareGpioOutput04B(self, SpareGpioOutput04B):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput04B, 31, 'B')
        self.push_change_event("SpareGpioOutput04B", SpareGpioOutput04B)

    @DebugIt()
    def get_FdlSwTriggerA(self):
        return perseus_utils.read_direct(self.perseus, 32, 'A')

    @DebugIt()
    def set_FdlSwTriggerA(self, FdlSwTriggerA):
        perseus_utils.write_direct(self.perseus, FdlSwTriggerA, 32, 'A')
        self.push_change_event("FdlSwTriggerA", FdlSwTriggerA)

    @DebugIt()
    def get_FdlSwTriggerB(self):
        return perseus_utils.read_direct(self.perseus, 32, 'B')

    @DebugIt()
    def set_FdlSwTriggerB(self, FdlSwTriggerB):
        perseus_utils.write_direct(self.perseus, FdlSwTriggerB, 32, 'B')
        self.push_change_event("FdlSwTriggerB", FdlSwTriggerB)

    @DebugIt()
    def get_SlowIqLoopEnableA(self):
        return perseus_utils.read_direct(self.perseus, 100, 'A')

    @DebugIt()
    def set_SlowIqLoopEnableA(self, SlowIqLoopEnableA):
        perseus_utils.write_direct(self.perseus, SlowIqLoopEnableA, 100, 'A')
        self.push_change_event("SlowIqLoopEnableA", SlowIqLoopEnableA)

    @DebugIt()
    def get_SlowIqLoopEnableB(self):
        return perseus_utils.read_direct(self.perseus, 100, 'B')

    @DebugIt()
    def set_SlowIqLoopEnableB(self, SlowIqLoopEnableB):
        perseus_utils.write_direct(self.perseus, SlowIqLoopEnableB, 100, 'B')
        self.push_change_event("SlowIqLoopEnableB", SlowIqLoopEnableB)

    @DebugIt()
    def get_AdcsPhaseshiftEnableA(self):
        return perseus_utils.read_direct(self.perseus, 101, 'A')

    @DebugIt()
    def set_AdcsPhaseshiftEnableA(self, AdcsPhaseshiftEnableA):
        perseus_utils.write_direct(self.perseus, AdcsPhaseshiftEnableA, 101, 'A')
        self.push_change_event("AdcsPhaseshiftEnableA", AdcsPhaseshiftEnableA)

    @DebugIt()
    def get_AdcsPhaseshiftEnableB(self):
        return perseus_utils.read_direct(self.perseus, 101, 'B')

    @DebugIt()
    def set_AdcsPhaseshiftEnableB(self, AdcsPhaseshiftEnableB):
        perseus_utils.write_direct(self.perseus, AdcsPhaseshiftEnableB, 101, 'B')
        self.push_change_event("AdcsPhaseshiftEnableB", AdcsPhaseshiftEnableB)

    @DebugIt()
    def get_DacsPhaseShiftEnableA(self):
        return perseus_utils.read_direct(self.perseus, 102, 'A')

    @DebugIt()
    def set_DacsPhaseShiftEnableA(self, DacsPhaseShiftEnableA):
        perseus_utils.write_direct(self.perseus, DacsPhaseShiftEnableA, 102, 'A')
        self.push_change_event("DacsPhaseShiftEnableA", DacsPhaseShiftEnableA)

    @DebugIt()
    def get_DacsPhaseShiftEnableB(self):
        return perseus_utils.read_direct(self.perseus, 102, 'B')

    @DebugIt()
    def set_DacsPhaseShiftEnableB(self, DacsPhaseShiftEnableB):
        perseus_utils.write_direct(self.perseus, DacsPhaseShiftEnableB, 102, 'B')
        self.push_change_event("DacsPhaseShiftEnableB", DacsPhaseShiftEnableB)

    @DebugIt()
    def get_SquarerefEnableA(self):
        return perseus_utils.read_direct(self.perseus, 103, 'A')

    @DebugIt()
    def set_SquarerefEnableA(self, SquarerefEnableA):
        perseus_utils.write_direct(self.perseus, SquarerefEnableA, 103, 'A')
        self.push_change_event("SquarerefEnableA", SquarerefEnableA)

    @DebugIt()
    def get_SquarerefEnableB(self):
        return perseus_utils.read_direct(self.perseus, 103, 'B')

    @DebugIt()
    def set_SquarerefEnableB(self, SquarerefEnableB):
        perseus_utils.write_direct(self.perseus, SquarerefEnableB, 103, 'B')
        self.push_change_event("SquarerefEnableB", SquarerefEnableB)

    @DebugIt()
    def get_FreqsquareA(self):
        address = 104
        cavity = 'A'
        #@todo: add this method to special methods library ...
        return extra_func.get_Freqsquare(self.perseus, address, cavity)

    @DebugIt()
    def set_FreqsquareA(self, FreqsquareA):
        address = 104
        cavity = 'A'
        #@todo: add this method to special methods library ...
        extra_func.set_Freqsquare(self.perseus, FreqsquareA, address, cavity)
        self.push_change_event("FreqsquareA", FreqsquareA)

    @DebugIt()
    def get_FreqsquareB(self):
        address = 104
        cavity = 'B'
        #@todo: add this method to special methods library ...
        return extra_func.get_Freqsquare(self.perseus, address, cavity)

    @DebugIt()
    def set_FreqsquareB(self, FreqsquareB):
        address = 104
        cavity = 'B'
        #@todo: add this method to special methods library ...
        extra_func.set_Freqsquare(self.perseus, FreqsquareB, address, cavity)
        self.push_change_event("FreqsquareB", FreqsquareB)

    @DebugIt()
    def get_LookRefA(self):
        return perseus_utils.read_direct(self.perseus, 106, 'A')

    @DebugIt()
    def set_LookRefA(self, LookRefA):
        perseus_utils.write_direct(self.perseus, LookRefA, 106, 'A')
        self.push_change_event("LookRefA", LookRefA)

    @DebugIt()
    def get_LookRefB(self):
        return perseus_utils.read_direct(self.perseus, 106, 'B')

    @DebugIt()
    def set_LookRefB(self, LookRefB):
        perseus_utils.write_direct(self.perseus, LookRefB, 106, 'B')
        self.push_change_event("LookRefB", LookRefB)

    @DebugIt()
    def get_QuadrantSelectionA(self):
        return perseus_utils.read_direct(self.perseus, 107, 'A')

    @DebugIt()
    def set_QuadrantSelectionA(self, QuadrantSelectionA):
        perseus_utils.write_direct(self.perseus, QuadrantSelectionA, 107, 'A')
        self.push_change_event("QuadrantSelectionA", QuadrantSelectionA)

    @DebugIt()
    def get_QuadrantSelectionB(self):
        return perseus_utils.read_direct(self.perseus, 107, 'B')

    @DebugIt()
    def set_QuadrantSelectionB(self, QuadrantSelectionB):
        perseus_utils.write_direct(self.perseus, QuadrantSelectionB, 107, 'B')
        self.push_change_event("QuadrantSelectionB", QuadrantSelectionB)

    @DebugIt()
    def get_SlowIqLoopInputSelectionA(self):
        return perseus_utils.read_direct(self.perseus, 110, 'A')

    @DebugIt()
    def set_SlowIqLoopInputSelectionA(self, SlowIqLoopInputSelectionA):
        perseus_utils.write_direct(self.perseus, SlowIqLoopInputSelectionA, 110, 'A')
        self.push_change_event("SlowIqLoopInputSelectionA", SlowIqLoopInputSelectionA)

    @DebugIt()
    def get_SlowIqLoopInputSelectionB(self):
        return perseus_utils.read_direct(self.perseus, 110, 'B')

    @DebugIt()
    def set_SlowIqLoopInputSelectionB(self, SlowIqLoopInputSelectionB):
        perseus_utils.write_direct(self.perseus, SlowIqLoopInputSelectionB, 110, 'B')
        self.push_change_event("SlowIqLoopInputSelectionB", SlowIqLoopInputSelectionB)

    @DebugIt()
    def get_FastIqLoopInputSelectionA(self):
        return perseus_utils.read_direct(self.perseus, 111, 'A')

    @DebugIt()
    def set_FastIqLoopInputSelectionA(self, FastIqLoopInputSelectionA):
        perseus_utils.write_direct(self.perseus, FastIqLoopInputSelectionA, 111, 'A')
        self.push_change_event("FastIqLoopInputSelectionA", FastIqLoopInputSelectionA)

    @DebugIt()
    def get_FastIqLoopInputSelectionB(self):
        return perseus_utils.read_direct(self.perseus, 111, 'B')

    @DebugIt()
    def set_FastIqLoopInputSelectionB(self, FastIqLoopInputSelectionB):
        perseus_utils.write_direct(self.perseus, FastIqLoopInputSelectionB, 111, 'B')
        self.push_change_event("FastIqLoopInputSelectionB", FastIqLoopInputSelectionB)

    @DebugIt()
    def get_AmplitudeLoopInputSelectionA(self):
        return perseus_utils.read_direct(self.perseus, 112, 'A')

    @DebugIt()
    def set_AmplitudeLoopInputSelectionA(self, AmplitudeLoopInputSelectionA):
        perseus_utils.write_direct(self.perseus, AmplitudeLoopInputSelectionA, 112, 'A')
        self.push_change_event("AmplitudeLoopInputSelectionA", AmplitudeLoopInputSelectionA)

    @DebugIt()
    def get_AmplitudeLoopInputSelectionB(self):
        return perseus_utils.read_direct(self.perseus, 112, 'B')

    @DebugIt()
    def set_AmplitudeLoopInputSelectionB(self, AmplitudeLoopInputSelectionB):
        perseus_utils.write_direct(self.perseus, AmplitudeLoopInputSelectionB, 112, 'B')
        self.push_change_event("AmplitudeLoopInputSelectionB", AmplitudeLoopInputSelectionB)

    @DebugIt()
    def get_PhaseLoopInputSelectionA(self):
        return perseus_utils.read_direct(self.perseus, 113, 'A')

    @DebugIt()
    def set_PhaseLoopInputSelectionA(self, PhaseLoopInputSelectionA):
        perseus_utils.write_direct(self.perseus, PhaseLoopInputSelectionA, 113, 'A')
        self.push_change_event("PhaseLoopInputSelectionA", PhaseLoopInputSelectionA)

    @DebugIt()
    def get_PhaseLoopInputSelectionB(self):
        return perseus_utils.read_direct(self.perseus, 113, 'B')

    @DebugIt()
    def set_PhaseLoopInputSelectionB(self, PhaseLoopInputSelectionB):
        perseus_utils.write_direct(self.perseus, PhaseLoopInputSelectionB, 113, 'B')
        self.push_change_event("PhaseLoopInputSelectionB", PhaseLoopInputSelectionB)

    @DebugIt()
    def get_PolarLoopsEnableA(self):
        return perseus_utils.read_direct(self.perseus, 114, 'A')

    @DebugIt()
    def set_PolarLoopsEnableA(self, PolarLoopsEnableA):
        perseus_utils.write_direct(self.perseus, PolarLoopsEnableA, 114, 'A')
        self.push_change_event("PolarLoopsEnableA", PolarLoopsEnableA)

    @DebugIt()
    def get_PolarLoopsEnableB(self):
        return perseus_utils.read_direct(self.perseus, 114, 'B')

    @DebugIt()
    def set_PolarLoopsEnableB(self, PolarLoopsEnableB):
        perseus_utils.write_direct(self.perseus, PolarLoopsEnableB, 114, 'B')
        self.push_change_event("PolarLoopsEnableB", PolarLoopsEnableB)

    @DebugIt()
    def get_FastIqLoopEnableA(self):
        return perseus_utils.read_direct(self.perseus, 115, 'A')

    @DebugIt()
    def set_FastIqLoopEnableA(self, FastIqLoopEnableA):
        perseus_utils.write_direct(self.perseus, FastIqLoopEnableA, 115, 'A')
        self.push_change_event("FastIqLoopEnableA", FastIqLoopEnableA)

    @DebugIt()
    def get_FastIqLoopEnableB(self):
        return perseus_utils.read_direct(self.perseus, 115, 'B')

    @DebugIt()
    def set_FastIqLoopEnableB(self, FastIqLoopEnableB):
        perseus_utils.write_direct(self.perseus, FastIqLoopEnableB, 115, 'B')
        self.push_change_event("FastIqLoopEnableB", FastIqLoopEnableB)

    @DebugIt()
    def get_AmplitudeLoopEnableA(self):
        return perseus_utils.read_direct(self.perseus, 116, 'A')

    @DebugIt()
    def set_AmplitudeLoopEnableA(self, AmplitudeLoopEnableA):
        perseus_utils.write_direct(self.perseus, AmplitudeLoopEnableA, 116, 'A')
        self.push_change_event("AmplitudeLoopEnableA", AmplitudeLoopEnableA)

    @DebugIt()
    def get_AmplitudeLoopEnableB(self):
        return perseus_utils.read_direct(self.perseus, 116, 'B')

    @DebugIt()
    def set_AmplitudeLoopEnableB(self, AmplitudeLoopEnableB):
        perseus_utils.write_direct(self.perseus, AmplitudeLoopEnableB, 116, 'B')
        self.push_change_event("AmplitudeLoopEnableB", AmplitudeLoopEnableB)

    @DebugIt()
    def get_PhaseLoopEnableA(self):
        return perseus_utils.read_direct(self.perseus, 117, 'A')

    @DebugIt()
    def set_PhaseLoopEnableA(self, PhaseLoopEnableA):
        perseus_utils.write_direct(self.perseus, PhaseLoopEnableA, 117, 'A')
        self.push_change_event("PhaseLoopEnableA", PhaseLoopEnableA)

    @DebugIt()
    def get_PhaseLoopEnableB(self):
        return perseus_utils.read_direct(self.perseus, 117, 'B')

    @DebugIt()
    def set_PhaseLoopEnableB(self, PhaseLoopEnableB):
        perseus_utils.write_direct(self.perseus, PhaseLoopEnableB, 117, 'B')
        self.push_change_event("PhaseLoopEnableB", PhaseLoopEnableB)

    @DebugIt()
    def get_KpFastIqLoopA(self):
        return perseus_utils.read_direct(self.perseus, 118, 'A')

    @DebugIt()
    def set_KpFastIqLoopA(self, KpFastIqLoopA):
        perseus_utils.write_direct(self.perseus, KpFastIqLoopA, 118, 'A')
        self.push_change_event("KpFastIqLoopA", KpFastIqLoopA)

    @DebugIt()
    def get_KpFastIqLoopB(self):
        return perseus_utils.read_direct(self.perseus, 118, 'B')

    @DebugIt()
    def set_KpFastIqLoopB(self, KpFastIqLoopB):
        perseus_utils.write_direct(self.perseus, KpFastIqLoopB, 118, 'B')
        self.push_change_event("KpFastIqLoopB", KpFastIqLoopB)

    @DebugIt()
    def get_KiFastIqLoopA(self):
        return perseus_utils.read_direct(self.perseus, 119, 'A')

    @DebugIt()
    def set_KiFastIqLoopA(self, KiFastIqLoopA):
        perseus_utils.write_direct(self.perseus, KiFastIqLoopA, 119, 'A')
        self.push_change_event("KiFastIqLoopA", KiFastIqLoopA)

    @DebugIt()
    def get_KiFastIqLoopB(self):
        return perseus_utils.read_direct(self.perseus, 119, 'B')

    @DebugIt()
    def set_KiFastIqLoopB(self, KiFastIqLoopB):
        perseus_utils.write_direct(self.perseus, KiFastIqLoopB, 119, 'B')
        self.push_change_event("KiFastIqLoopB", KiFastIqLoopB)

    @DebugIt()
    def get_KpAmpLoopA(self):
        return perseus_utils.read_direct(self.perseus, 120, 'A')

    @DebugIt()
    def set_KpAmpLoopA(self, KpAmpLoopA):
        perseus_utils.write_direct(self.perseus, KpAmpLoopA, 120, 'A')
        self.push_change_event("KpAmpLoopA", KpAmpLoopA)

    @DebugIt()
    def get_KpAmpLoopB(self):
        return perseus_utils.read_direct(self.perseus, 120, 'B')

    @DebugIt()
    def set_KpAmpLoopB(self, KpAmpLoopB):
        perseus_utils.write_direct(self.perseus, KpAmpLoopB, 120, 'B')
        self.push_change_event("KpAmpLoopB", KpAmpLoopB)

    @DebugIt()
    def get_KiAmpLoopA(self):
        return perseus_utils.read_direct(self.perseus, 121, 'A')

    @DebugIt()
    def set_KiAmpLoopA(self, KiAmpLoopA):
        perseus_utils.write_direct(self.perseus, KiAmpLoopA, 121, 'A')
        self.push_change_event("KiAmpLoopA", KiAmpLoopA)

    @DebugIt()
    def get_KiAmpLoopB(self):
        return perseus_utils.read_direct(self.perseus, 121, 'B')

    @DebugIt()
    def set_KiAmpLoopB(self, KiAmpLoopB):
        perseus_utils.write_direct(self.perseus, KiAmpLoopB, 121, 'B')
        self.push_change_event("KiAmpLoopB", KiAmpLoopB)

    @DebugIt()
    def get_KpPhaseLoopA(self):
        return perseus_utils.read_direct(self.perseus, 122, 'A')

    @DebugIt()
    def set_KpPhaseLoopA(self, KpPhaseLoopA):
        perseus_utils.write_direct(self.perseus, KpPhaseLoopA, 122, 'A')
        self.push_change_event("KpPhaseLoopA", KpPhaseLoopA)

    @DebugIt()
    def get_KpPhaseLoopB(self):
        return perseus_utils.read_direct(self.perseus, 122, 'B')

    @DebugIt()
    def set_KpPhaseLoopB(self, KpPhaseLoopB):
        perseus_utils.write_direct(self.perseus, KpPhaseLoopB, 122, 'B')
        self.push_change_event("KpPhaseLoopB", KpPhaseLoopB)

    @DebugIt()
    def get_KiPhaseLoopA(self):
        return perseus_utils.read_direct(self.perseus, 123, 'A')

    @DebugIt()
    def set_KiPhaseLoopA(self, KiPhaseLoopA):
        perseus_utils.write_direct(self.perseus, KiPhaseLoopA, 123, 'A')
        self.push_change_event("KiPhaseLoopA", KiPhaseLoopA)

    @DebugIt()
    def get_KiPhaseLoopB(self):
        return perseus_utils.read_direct(self.perseus, 123, 'B')

    @DebugIt()
    def set_KiPhaseLoopB(self, KiPhaseLoopB):
        perseus_utils.write_direct(self.perseus, KiPhaseLoopB, 123, 'B')
        self.push_change_event("KiPhaseLoopB", KiPhaseLoopB)

    @DebugIt()
    def get_PiLimitFastPiIqA(self):
        return perseus_utils.read_milivolts(self.perseus, 124, 'A')

    @DebugIt()
    def set_PiLimitFastPiIqA(self, PiLimitFastPiIqA):
        perseus_utils.write_milivolts(self.perseus, PiLimitFastPiIqA, 124, 'A')
        self.push_change_event("PiLimitFastPiIqA", PiLimitFastPiIqA)

    @DebugIt()
    def get_PiLimitFastPiIqB(self):
        return perseus_utils.read_milivolts(self.perseus, 124, 'B')

    @DebugIt()
    def set_PiLimitFastPiIqB(self, PiLimitFastPiIqB):
        perseus_utils.write_milivolts(self.perseus, PiLimitFastPiIqB, 124, 'B')
        self.push_change_event("PiLimitFastPiIqB", PiLimitFastPiIqB)

    @DebugIt()
    def get_PulseModeEnableA(self):
        return perseus_utils.read_direct(self.perseus, 200, 'A')

    @DebugIt()
    def set_PulseModeEnableA(self, PulseModeEnableA):
        perseus_utils.write_direct(self.perseus, PulseModeEnableA, 200, 'A')
        self.push_change_event("PulseModeEnableA", PulseModeEnableA)

    @DebugIt()
    def get_PulseModeEnableB(self):
        return perseus_utils.read_direct(self.perseus, 200, 'B')

    @DebugIt()
    def set_PulseModeEnableB(self, PulseModeEnableB):
        perseus_utils.write_direct(self.perseus, PulseModeEnableB, 200, 'B')
        self.push_change_event("PulseModeEnableB", PulseModeEnableB)

    @DebugIt()
    def get_AutomaticConditioningEnableA(self):
        return perseus_utils.read_direct(self.perseus, 201, 'A')

    @DebugIt()
    def set_AutomaticConditioningEnableA(self, AutomaticConditioningEnableA):
        perseus_utils.write_direct(self.perseus, AutomaticConditioningEnableA, 201, 'A')
        self.push_change_event("AutomaticConditioningEnableA", AutomaticConditioningEnableA)

    @DebugIt()
    def get_AutomaticConditioningEnableB(self):
        return perseus_utils.read_direct(self.perseus, 201, 'B')

    @DebugIt()
    def set_AutomaticConditioningEnableB(self, AutomaticConditioningEnableB):
        perseus_utils.write_direct(self.perseus, AutomaticConditioningEnableB, 201, 'B')
        self.push_change_event("AutomaticConditioningEnableB", AutomaticConditioningEnableB)

    @DebugIt()
    def get_ConditioningdutyCicleA(self):
        address = 202
        cavity = 'A'
        #@todo: add this method to special methods library ...
        return extra_func.get_ConditioningdutyCicle(self.perseus, address, cavity)

    @DebugIt()
    def set_ConditioningdutyCicleA(self, ConditioningdutyCicleA):
        address = 202
        cavity = 'A'
        #@todo: add this method to special methods library ...
        extra_func.set_ConditioningdutyCicle(self.perseus, ConditioningdutyCicleA, address, cavity)
        self.push_change_event("ConditioningdutyCicleA", ConditioningdutyCicleA)

    @DebugIt()
    def get_ConditioningdutyCicleB(self):
        address = 202
        cavity = 'B'
        #@todo: add this method to special methods library ...
        return extra_func.get_ConditioningdutyCicle(self.perseus, address, cavity)

    @DebugIt()
    def set_ConditioningdutyCicleB(self, ConditioningdutyCicleB):
        address = 202
        cavity = 'B'
        #@todo: add this method to special methods library ...
        extra_func.set_ConditioningdutyCicle(self.perseus, ConditioningdutyCicleB, address, cavity)
        self.push_change_event("ConditioningdutyCicleB", ConditioningdutyCicleB)

    @DebugIt()
    def get_TuningEnableA(self):
        return perseus_utils.read_direct(self.perseus, 300, 'A')

    @DebugIt()
    def set_TuningEnableA(self, TuningEnableA):
        perseus_utils.write_direct(self.perseus, TuningEnableA, 300, 'A')
        self.push_change_event("TuningEnableA", TuningEnableA)

    @DebugIt()
    def get_TuningEnableB(self):
        return perseus_utils.read_direct(self.perseus, 300, 'B')

    @DebugIt()
    def set_TuningEnableB(self, TuningEnableB):
        perseus_utils.write_direct(self.perseus, TuningEnableB, 300, 'B')
        self.push_change_event("TuningEnableB", TuningEnableB)

    @DebugIt()
    def get_TuningPosEnA(self):
        return perseus_utils.read_direct(self.perseus, 301, 'A')

    @DebugIt()
    def set_TuningPosEnA(self, TuningPosEnA):
        perseus_utils.write_direct(self.perseus, TuningPosEnA, 301, 'A')
        self.push_change_event("TuningPosEnA", TuningPosEnA)

    @DebugIt()
    def get_TuningPosEnB(self):
        return perseus_utils.read_direct(self.perseus, 301, 'B')

    @DebugIt()
    def set_TuningPosEnB(self, TuningPosEnB):
        perseus_utils.write_direct(self.perseus, TuningPosEnB, 301, 'B')
        self.push_change_event("TuningPosEnB", TuningPosEnB)

    @DebugIt()
    def get_NumStepsA(self):
        return perseus_utils.read_direct(self.perseus, 302, 'A')

    @DebugIt()
    def set_NumStepsA(self, NumStepsA):
        perseus_utils.write_direct(self.perseus, NumStepsA, 302, 'A')
        self.push_change_event("NumStepsA", NumStepsA)

    @DebugIt()
    def get_NumStepsB(self):
        return perseus_utils.read_direct(self.perseus, 302, 'B')

    @DebugIt()
    def set_NumStepsB(self, NumStepsB):
        perseus_utils.write_direct(self.perseus, NumStepsB, 302, 'B')
        self.push_change_event("NumStepsB", NumStepsB)

    @DebugIt()
    def get_PulsesFrequencyA(self):
        return perseus_utils.read_direct(self.perseus, 303, 'A')

    @DebugIt()
    def set_PulsesFrequencyA(self, PulsesFrequencyA):
        perseus_utils.write_direct(self.perseus, PulsesFrequencyA, 303, 'A')
        self.push_change_event("PulsesFrequencyA", PulsesFrequencyA)

    @DebugIt()
    def get_PulsesFrequencyB(self):
        return perseus_utils.read_direct(self.perseus, 303, 'B')

    @DebugIt()
    def set_PulsesFrequencyB(self, PulsesFrequencyB):
        perseus_utils.write_direct(self.perseus, PulsesFrequencyB, 303, 'B')
        self.push_change_event("PulsesFrequencyB", PulsesFrequencyB)

    @DebugIt()
    def get_PhaseOffsetA(self):
        return perseus_utils.read_angle(self.perseus, 304, 'A')

    @DebugIt()
    def set_PhaseOffsetA(self, PhaseOffsetA):
        perseus_utils.write_angle(self.perseus, PhaseOffsetA, 304, 'A')
        self.push_change_event("PhaseOffsetA", PhaseOffsetA)

    @DebugIt()
    def get_PhaseOffsetB(self):
        return perseus_utils.read_angle(self.perseus, 304, 'B')

    @DebugIt()
    def set_PhaseOffsetB(self, PhaseOffsetB):
        perseus_utils.write_angle(self.perseus, PhaseOffsetB, 304, 'B')
        self.push_change_event("PhaseOffsetB", PhaseOffsetB)

    @DebugIt()
    def get_MoveA(self):
        return perseus_utils.read_direct(self.perseus, 305, 'A')

    @DebugIt()
    def set_MoveA(self, MoveA):
        perseus_utils.write_direct(self.perseus, MoveA, 305, 'A')
        self.push_change_event("MoveA", MoveA)

    @DebugIt()
    def get_MoveB(self):
        return perseus_utils.read_direct(self.perseus, 305, 'B')

    @DebugIt()
    def set_MoveB(self, MoveB):
        perseus_utils.write_direct(self.perseus, MoveB, 305, 'B')
        self.push_change_event("MoveB", MoveB)

    @DebugIt()
    def get_MoveupA(self):
        return perseus_utils.read_direct(self.perseus, 306, 'A')

    @DebugIt()
    def set_MoveupA(self, MoveupA):
        perseus_utils.write_direct(self.perseus, MoveupA, 306, 'A')
        self.push_change_event("MoveupA", MoveupA)

    @DebugIt()
    def get_MoveupB(self):
        return perseus_utils.read_direct(self.perseus, 306, 'B')

    @DebugIt()
    def set_MoveupB(self, MoveupB):
        perseus_utils.write_direct(self.perseus, MoveupB, 306, 'B')
        self.push_change_event("MoveupB", MoveupB)

    @DebugIt()
    def get_TuningresetA(self):
        return perseus_utils.read_direct(self.perseus, 307, 'A')

    @DebugIt()
    def set_TuningresetA(self, TuningresetA):
        perseus_utils.write_direct(self.perseus, TuningresetA, 307, 'A')
        self.push_change_event("TuningresetA", TuningresetA)

    @DebugIt()
    def get_TuningresetB(self):
        return perseus_utils.read_direct(self.perseus, 307, 'B')

    @DebugIt()
    def set_TuningresetB(self, TuningresetB):
        perseus_utils.write_direct(self.perseus, TuningresetB, 307, 'B')
        self.push_change_event("TuningresetB", TuningresetB)

    @DebugIt()
    def get_FwminA(self):
        address = 308
        cavity = 'A'
        #@todo: add this method to special methods library ...
        return extra_func.get_Fwmin(self.perseus, address, cavity)

    @DebugIt()
    def set_FwminA(self, FwminA):
        address = 308
        cavity = 'A'
        #@todo: add this method to special methods library ...
        extra_func.set_Fwmin(self.perseus, FwminA, address, cavity)
        self.push_change_event("FwminA", FwminA)

    @DebugIt()
    def get_FwminB(self):
        address = 308
        cavity = 'B'
        #@todo: add this method to special methods library ...
        return extra_func.get_Fwmin(self.perseus, address, cavity)

    @DebugIt()
    def set_FwminB(self, FwminB):
        address = 308
        cavity = 'B'
        #@todo: add this method to special methods library ...
        extra_func.set_Fwmin(self.perseus, FwminB, address, cavity)
        self.push_change_event("FwminB", FwminB)

    @DebugIt()
    def get_MarginupA(self):
        return perseus_utils.read_angle(self.perseus, 309, 'A')

    @DebugIt()
    def set_MarginupA(self, MarginupA):
        perseus_utils.write_angle(self.perseus, MarginupA, 309, 'A')
        self.push_change_event("MarginupA", MarginupA)

    @DebugIt()
    def get_MarginupB(self):
        return perseus_utils.read_angle(self.perseus, 309, 'B')

    @DebugIt()
    def set_MarginupB(self, MarginupB):
        perseus_utils.write_angle(self.perseus, MarginupB, 309, 'B')
        self.push_change_event("MarginupB", MarginupB)

    @DebugIt()
    def get_MarginlowA(self):
        return perseus_utils.read_angle(self.perseus, 310, 'A')

    @DebugIt()
    def set_MarginlowA(self, MarginlowA):
        perseus_utils.write_angle(self.perseus, MarginlowA, 310, 'A')
        self.push_change_event("MarginlowA", MarginlowA)

    @DebugIt()
    def get_MarginlowB(self):
        return perseus_utils.read_angle(self.perseus, 310, 'B')

    @DebugIt()
    def set_MarginlowB(self, MarginlowB):
        perseus_utils.write_angle(self.perseus, MarginlowB, 310, 'B')
        self.push_change_event("MarginlowB", MarginlowB)

    @DebugIt()
    def get_TuningdelayA(self):
        address = 311
        cavity = 'A'
        #@todo: add this method to special methods library ...
        return extra_func.get_Tuningdelay(self.perseus, address, cavity)

    @DebugIt()
    def set_TuningdelayA(self, TuningdelayA):
        address = 311
        cavity = 'A'
        #@todo: add this method to special methods library ...
        extra_func.set_Tuningdelay(self.perseus, TuningdelayA, address, cavity)
        self.push_change_event("TuningdelayA", TuningdelayA)

    @DebugIt()
    def get_TuningdelayB(self):
        address = 311
        cavity = 'B'
        #@todo: add this method to special methods library ...
        return extra_func.get_Tuningdelay(self.perseus, address, cavity)

    @DebugIt()
    def set_TuningdelayB(self, TuningdelayB):
        address = 311
        cavity = 'B'
        #@todo: add this method to special methods library ...
        extra_func.set_Tuningdelay(self.perseus, TuningdelayB, address, cavity)
        self.push_change_event("TuningdelayB", TuningdelayB)

    @DebugIt()
    def get_TuningfilterenableA(self):
        return perseus_utils.read_direct(self.perseus, 312, 'A')

    @DebugIt()
    def set_TuningfilterenableA(self, TuningfilterenableA):
        perseus_utils.write_direct(self.perseus, TuningfilterenableA, 312, 'A')
        self.push_change_event("TuningfilterenableA", TuningfilterenableA)

    @DebugIt()
    def get_TuningfilterenableB(self):
        return perseus_utils.read_direct(self.perseus, 312, 'B')

    @DebugIt()
    def set_TuningfilterenableB(self, TuningfilterenableB):
        perseus_utils.write_direct(self.perseus, TuningfilterenableB, 312, 'B')
        self.push_change_event("TuningfilterenableB", TuningfilterenableB)

    @DebugIt()
    def get_TuningtriggerenableA(self):
        return perseus_utils.read_direct(self.perseus, 313, 'A')

    @DebugIt()
    def set_TuningtriggerenableA(self, TuningtriggerenableA):
        perseus_utils.write_direct(self.perseus, TuningtriggerenableA, 313, 'A')
        self.push_change_event("TuningtriggerenableA", TuningtriggerenableA)

    @DebugIt()
    def get_TuningtriggerenableB(self):
        return perseus_utils.read_direct(self.perseus, 313, 'B')

    @DebugIt()
    def set_TuningtriggerenableB(self, TuningtriggerenableB):
        perseus_utils.write_direct(self.perseus, TuningtriggerenableB, 313, 'B')
        self.push_change_event("TuningtriggerenableB", TuningtriggerenableB)

    @DebugIt()
    def get_EpsItckDisableA(self):
        return perseus_utils.read_direct(self.perseus, 400, 'A')

    @DebugIt()
    def set_EpsItckDisableA(self, EpsItckDisableA):
        perseus_utils.write_direct(self.perseus, EpsItckDisableA, 400, 'A')
        self.push_change_event("EpsItckDisableA", EpsItckDisableA)

    @DebugIt()
    def get_EpsItckDisableB(self):
        return perseus_utils.read_direct(self.perseus, 400, 'B')

    @DebugIt()
    def set_EpsItckDisableB(self, EpsItckDisableB):
        perseus_utils.write_direct(self.perseus, EpsItckDisableB, 400, 'B')
        self.push_change_event("EpsItckDisableB", EpsItckDisableB)

    @DebugIt()
    def get_FimItckDisableA(self):
        return perseus_utils.read_direct(self.perseus, 401, 'A')

    @DebugIt()
    def set_FimItckDisableA(self, FimItckDisableA):
        perseus_utils.write_direct(self.perseus, FimItckDisableA, 401, 'A')
        self.push_change_event("FimItckDisableA", FimItckDisableA)

    @DebugIt()
    def get_FimItckDisableB(self):
        return perseus_utils.read_direct(self.perseus, 401, 'B')

    @DebugIt()
    def set_FimItckDisableB(self, FimItckDisableB):
        perseus_utils.write_direct(self.perseus, FimItckDisableB, 401, 'B')
        self.push_change_event("FimItckDisableB", FimItckDisableB)

    @DebugIt()
    def get_MDividerA(self):
        address = 500
        cavity = 'A'
        #@todo: add this method to special methods library ...
        return extra_func.get_MDivider(self.perseus, address, cavity)

    @DebugIt()
    def set_MDividerA(self, MDividerA):
        address = 500
        cavity = 'A'
        #@todo: add this method to special methods library ...
        extra_func.set_MDivider(self.perseus, MDividerA, address, cavity)
        self.push_change_event("MDividerA", MDividerA)

    @DebugIt()
    def get_MDividerB(self):
        address = 500
        cavity = 'B'
        #@todo: add this method to special methods library ...
        return extra_func.get_MDivider(self.perseus, address, cavity)

    @DebugIt()
    def set_MDividerB(self, MDividerB):
        address = 500
        cavity = 'B'
        #@todo: add this method to special methods library ...
        extra_func.set_MDivider(self.perseus, MDividerB, address, cavity)
        self.push_change_event("MDividerB", MDividerB)

    @DebugIt()
    def get_NDividerA(self):
        address = 501
        cavity = 'A'
        #@todo: add this method to special methods library ...
        return extra_func.get_NDivider(self.perseus, address, cavity)

    @DebugIt()
    def set_NDividerA(self, NDividerA):
        address = 501
        cavity = 'A'
        #@todo: add this method to special methods library ...
        extra_func.set_NDivider(self.perseus, NDividerA, address, cavity)
        self.push_change_event("NDividerA", NDividerA)

    @DebugIt()
    def get_NDividerB(self):
        address = 501
        cavity = 'B'
        #@todo: add this method to special methods library ...
        return extra_func.get_NDivider(self.perseus, address, cavity)

    @DebugIt()
    def set_NDividerB(self, NDividerB):
        address = 501
        cavity = 'B'
        #@todo: add this method to special methods library ...
        extra_func.set_NDivider(self.perseus, NDividerB, address, cavity)
        self.push_change_event("NDividerB", NDividerB)

    @DebugIt()
    def get_MuxselA(self):
        return perseus_utils.read_direct(self.perseus, 502, 'A')

    @DebugIt()
    def set_MuxselA(self, MuxselA):
        perseus_utils.write_direct(self.perseus, MuxselA, 502, 'A')
        self.push_change_event("MuxselA", MuxselA)

    @DebugIt()
    def get_MuxselB(self):
        return perseus_utils.read_direct(self.perseus, 502, 'B')

    @DebugIt()
    def set_MuxselB(self, MuxselB):
        perseus_utils.write_direct(self.perseus, MuxselB, 502, 'B')
        self.push_change_event("MuxselB", MuxselB)

    @DebugIt()
    def get_Mux0DividerA(self):
        return perseus_utils.read_direct(self.perseus, 503, 'A')

    @DebugIt()
    def set_Mux0DividerA(self, Mux0DividerA):
        perseus_utils.write_direct(self.perseus, Mux0DividerA, 503, 'A')
        self.push_change_event("Mux0DividerA", Mux0DividerA)

    @DebugIt()
    def get_Mux0DividerB(self):
        return perseus_utils.read_direct(self.perseus, 503, 'B')

    @DebugIt()
    def set_Mux0DividerB(self, Mux0DividerB):
        perseus_utils.write_direct(self.perseus, Mux0DividerB, 503, 'B')
        self.push_change_event("Mux0DividerB", Mux0DividerB)

    @DebugIt()
    def get_Mux1DividerA(self):
        return perseus_utils.read_direct(self.perseus, 504, 'A')

    @DebugIt()
    def set_Mux1DividerA(self, Mux1DividerA):
        perseus_utils.write_direct(self.perseus, Mux1DividerA, 504, 'A')
        self.push_change_event("Mux1DividerA", Mux1DividerA)

    @DebugIt()
    def get_Mux1DividerB(self):
        return perseus_utils.read_direct(self.perseus, 504, 'B')

    @DebugIt()
    def set_Mux1DividerB(self, Mux1DividerB):
        perseus_utils.write_direct(self.perseus, Mux1DividerB, 504, 'B')
        self.push_change_event("Mux1DividerB", Mux1DividerB)

    @DebugIt()
    def get_Mux2DividerA(self):
        return perseus_utils.read_direct(self.perseus, 505, 'A')

    @DebugIt()
    def set_Mux2DividerA(self, Mux2DividerA):
        perseus_utils.write_direct(self.perseus, Mux2DividerA, 505, 'A')
        self.push_change_event("Mux2DividerA", Mux2DividerA)

    @DebugIt()
    def get_Mux2DividerB(self):
        return perseus_utils.read_direct(self.perseus, 505, 'B')

    @DebugIt()
    def set_Mux2DividerB(self, Mux2DividerB):
        perseus_utils.write_direct(self.perseus, Mux2DividerB, 505, 'B')
        self.push_change_event("Mux2DividerB", Mux2DividerB)

    @DebugIt()
    def get_Mux3DividerA(self):
        return perseus_utils.read_direct(self.perseus, 506, 'A')

    @DebugIt()
    def set_Mux3DividerA(self, Mux3DividerA):
        perseus_utils.write_direct(self.perseus, Mux3DividerA, 506, 'A')
        self.push_change_event("Mux3DividerA", Mux3DividerA)

    @DebugIt()
    def get_Mux3DividerB(self):
        return perseus_utils.read_direct(self.perseus, 506, 'B')

    @DebugIt()
    def set_Mux3DividerB(self, Mux3DividerB):
        perseus_utils.write_direct(self.perseus, Mux3DividerB, 506, 'B')
        self.push_change_event("Mux3DividerB", Mux3DividerB)

    @DebugIt()
    def get_Mux4DividerA(self):
        return perseus_utils.read_direct(self.perseus, 507, 'A')

    @DebugIt()
    def set_Mux4DividerA(self, Mux4DividerA):
        perseus_utils.write_direct(self.perseus, Mux4DividerA, 507, 'A')
        self.push_change_event("Mux4DividerA", Mux4DividerA)

    @DebugIt()
    def get_Mux4DividerB(self):
        return perseus_utils.read_direct(self.perseus, 507, 'B')

    @DebugIt()
    def set_Mux4DividerB(self, Mux4DividerB):
        perseus_utils.write_direct(self.perseus, Mux4DividerB, 507, 'B')
        self.push_change_event("Mux4DividerB", Mux4DividerB)

    @DebugIt()
    def get_SendWordA(self):
        return perseus_utils.read_direct(self.perseus, 508, 'A')

    @DebugIt()
    def set_SendWordA(self, SendWordA):
        perseus_utils.write_direct(self.perseus, SendWordA, 508, 'A')
        self.push_change_event("SendWordA", SendWordA)

    @DebugIt()
    def get_SendWordB(self):
        return perseus_utils.read_direct(self.perseus, 508, 'B')

    @DebugIt()
    def set_SendWordB(self, SendWordB):
        perseus_utils.write_direct(self.perseus, SendWordB, 508, 'B')
        self.push_change_event("SendWordB", SendWordB)

    @DebugIt()
    def get_CpdirA(self):
        return perseus_utils.read_direct(self.perseus, 509, 'A')

    @DebugIt()
    def set_CpdirA(self, CpdirA):
        perseus_utils.write_direct(self.perseus, CpdirA, 509, 'A')
        self.push_change_event("CpdirA", CpdirA)

    @DebugIt()
    def get_CpdirB(self):
        return perseus_utils.read_direct(self.perseus, 509, 'B')

    @DebugIt()
    def set_CpdirB(self, CpdirB):
        perseus_utils.write_direct(self.perseus, CpdirB, 509, 'B')
        self.push_change_event("CpdirB", CpdirB)

    @DebugIt()
    def get_VcxoOutputInversionA(self):
        return perseus_utils.read_direct(self.perseus, 510, 'A')

    @DebugIt()
    def set_VcxoOutputInversionA(self, VcxoOutputInversionA):
        perseus_utils.write_direct(self.perseus, VcxoOutputInversionA, 510, 'A')
        self.push_change_event("VcxoOutputInversionA", VcxoOutputInversionA)

    @DebugIt()
    def get_VcxoOutputInversionB(self):
        return perseus_utils.read_direct(self.perseus, 510, 'B')

    @DebugIt()
    def set_VcxoOutputInversionB(self, VcxoOutputInversionB):
        perseus_utils.write_direct(self.perseus, VcxoOutputInversionB, 510, 'B')
        self.push_change_event("VcxoOutputInversionB", VcxoOutputInversionB)

    @DebugIt()
    def read_Diag_IcavLoopsA(self):
        return self._Diag_IcavLoopsA

    @DebugIt()
    def read_Diag_IcavLoopsB(self):
        return self._Diag_IcavLoopsB

    @DebugIt()
    def read_Diag_QcavLoopsA(self):
        return self._Diag_QcavLoopsA

    @DebugIt()
    def read_Diag_QcavLoopsB(self):
        return self._Diag_QcavLoopsB

    @DebugIt()
    def read_Diag_IcontrolA(self):
        return self._Diag_IcontrolA

    @DebugIt()
    def read_Diag_IcontrolB(self):
        return self._Diag_IcontrolB

    @DebugIt()
    def read_Diag_QcontrolA(self):
        return self._Diag_QcontrolA

    @DebugIt()
    def read_Diag_QcontrolB(self):
        return self._Diag_QcontrolB

    @DebugIt()
    def read_Diag_Icontrol1A(self):
        return self._Diag_Icontrol1A

    @DebugIt()
    def read_Diag_Icontrol1B(self):
        return self._Diag_Icontrol1B

    @DebugIt()
    def read_Diag_Qcontrol1A(self):
        return self._Diag_Qcontrol1A

    @DebugIt()
    def read_Diag_Qcontrol1B(self):
        return self._Diag_Qcontrol1B

    @DebugIt()
    def read_Diag_Icontrol2A(self):
        return self._Diag_Icontrol2A

    @DebugIt()
    def read_Diag_Icontrol2B(self):
        return self._Diag_Icontrol2B

    @DebugIt()
    def read_Diag_Qcontrol2A(self):
        return self._Diag_Qcontrol2A

    @DebugIt()
    def read_Diag_Qcontrol2B(self):
        return self._Diag_Qcontrol2B

    @DebugIt()
    def read_Diag_IerrorA(self):
        return self._Diag_IerrorA

    @DebugIt()
    def read_Diag_IerrorB(self):
        return self._Diag_IerrorB

    @DebugIt()
    def read_Diag_QerrorA(self):
        return self._Diag_QerrorA

    @DebugIt()
    def read_Diag_QerrorB(self):
        return self._Diag_QerrorB

    @DebugIt()
    def read_Diag_IerroraccumA(self):
        return self._Diag_IerroraccumA

    @DebugIt()
    def read_Diag_IerroraccumB(self):
        return self._Diag_IerroraccumB

    @DebugIt()
    def read_Diag_QerroraccumA(self):
        return self._Diag_QerroraccumA

    @DebugIt()
    def read_Diag_QerroraccumB(self):
        return self._Diag_QerroraccumB

    @DebugIt()
    def read_Diag_IrefA(self):
        return self._Diag_IrefA

    @DebugIt()
    def read_Diag_IrefB(self):
        return self._Diag_IrefB

    @DebugIt()
    def read_Diag_QrefA(self):
        return self._Diag_QrefA

    @DebugIt()
    def read_Diag_QrefB(self):
        return self._Diag_QrefB

    @DebugIt()
    def read_Diag_IFwCavLoopsA(self):
        return self._Diag_IFwCavLoopsA

    @DebugIt()
    def read_Diag_IFwCavLoopsB(self):
        return self._Diag_IFwCavLoopsB

    @DebugIt()
    def read_Diag_QFwCavLoopsA(self):
        return self._Diag_QFwCavLoopsA

    @DebugIt()
    def read_Diag_QFwCavLoopsB(self):
        return self._Diag_QFwCavLoopsB

    @DebugIt()
    def read_Diag_IFwTet1LoopsA(self):
        return self._Diag_IFwTet1LoopsA

    @DebugIt()
    def read_Diag_IFwTet1LoopsB(self):
        return self._Diag_IFwTet1LoopsB

    @DebugIt()
    def read_Diag_QFwTet1LoopsA(self):
        return self._Diag_QFwTet1LoopsA

    @DebugIt()
    def read_Diag_QFwTet1LoopsB(self):
        return self._Diag_QFwTet1LoopsB

    @DebugIt()
    def read_Diag_IFwTet2LoopsA(self):
        return self._Diag_IFwTet2LoopsA

    @DebugIt()
    def read_Diag_IFwTet2LoopsB(self):
        return self._Diag_IFwTet2LoopsB

    @DebugIt()
    def read_Diag_QFwTet2LoopsA(self):
        return self._Diag_QFwTet2LoopsA

    @DebugIt()
    def read_Diag_QFwTet2LoopsB(self):
        return self._Diag_QFwTet2LoopsB

    @DebugIt()
    def read_Diag_IFwCircInLoopsA(self):
        return self._Diag_IFwCircInLoopsA

    @DebugIt()
    def read_Diag_IFwCircInLoopsB(self):
        return self._Diag_IFwCircInLoopsB

    @DebugIt()
    def read_Diag_QFwCircInLoopsA(self):
        return self._Diag_QFwCircInLoopsA

    @DebugIt()
    def read_Diag_QFwCircInLoopsB(self):
        return self._Diag_QFwCircInLoopsB

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
    def read_Diag_Ispare1A(self):
        return self._Diag_Ispare1A

    @DebugIt()
    def read_Diag_Ispare1B(self):
        return self._Diag_Ispare1B

    @DebugIt()
    def read_Diag_Qspare1A(self):
        return self._Diag_Qspare1A

    @DebugIt()
    def read_Diag_Qspare1B(self):
        return self._Diag_Qspare1B

    @DebugIt()
    def read_Diag_Ispare2A(self):
        return self._Diag_Ispare2A

    @DebugIt()
    def read_Diag_Ispare2B(self):
        return self._Diag_Ispare2B

    @DebugIt()
    def read_Diag_Qspare2A(self):
        return self._Diag_Qspare2A

    @DebugIt()
    def read_Diag_Qspare2B(self):
        return self._Diag_Qspare2B

    @DebugIt()
    def read_Diag_IMuxCavA(self):
        return self._Diag_IMuxCavA

    @DebugIt()
    def read_Diag_IMuxCavB(self):
        return self._Diag_IMuxCavB

    @DebugIt()
    def read_Diag_QMuxCavA(self):
        return self._Diag_QMuxCavA

    @DebugIt()
    def read_Diag_QMuxCavB(self):
        return self._Diag_QMuxCavB

    @DebugIt()
    def read_Diag_IMuxFwCavA(self):
        return self._Diag_IMuxFwCavA

    @DebugIt()
    def read_Diag_IMuxFwCavB(self):
        return self._Diag_IMuxFwCavB

    @DebugIt()
    def read_Diag_QMuxFwCavA(self):
        return self._Diag_QMuxFwCavA

    @DebugIt()
    def read_Diag_QMuxFwCavB(self):
        return self._Diag_QMuxFwCavB

    @DebugIt()
    def read_Diag_IMuxFwTet1A(self):
        return self._Diag_IMuxFwTet1A

    @DebugIt()
    def read_Diag_IMuxFwTet1B(self):
        return self._Diag_IMuxFwTet1B

    @DebugIt()
    def read_Diag_QMuxFwTet1A(self):
        return self._Diag_QMuxFwTet1A

    @DebugIt()
    def read_Diag_QMuxFwTet1B(self):
        return self._Diag_QMuxFwTet1B

    @DebugIt()
    def read_Diag_IMuxFwTet2A(self):
        return self._Diag_IMuxFwTet2A

    @DebugIt()
    def read_Diag_IMuxFwTet2B(self):
        return self._Diag_IMuxFwTet2B

    @DebugIt()
    def read_Diag_QMuxFwTet2A(self):
        return self._Diag_QMuxFwTet2A

    @DebugIt()
    def read_Diag_QMuxFwTet2B(self):
        return self._Diag_QMuxFwTet2B

    @DebugIt()
    def read_Diag_IMuxFwCircInA(self):
        return self._Diag_IMuxFwCircInA

    @DebugIt()
    def read_Diag_IMuxFwCircInB(self):
        return self._Diag_IMuxFwCircInB

    @DebugIt()
    def read_Diag_QMuxFwCircInA(self):
        return self._Diag_QMuxFwCircInA

    @DebugIt()
    def read_Diag_QMuxFwCircInB(self):
        return self._Diag_QMuxFwCircInB

    @DebugIt()
    def read_Diag_AmpCavA(self):
        return self._Diag_AmpCavA

    @DebugIt()
    def read_Diag_AmpCavB(self):
        return self._Diag_AmpCavB

    @DebugIt()
    def read_Diag_AmpFwA(self):
        return self._Diag_AmpFwA

    @DebugIt()
    def read_Diag_AmpFwB(self):
        return self._Diag_AmpFwB

    @DebugIt()
    def read_Diag_AngCavFwA(self):
        return self._Diag_AngCavFwA

    @DebugIt()
    def read_Diag_AngCavFwB(self):
        return self._Diag_AngCavFwB

    @DebugIt()
    def read_Diag_AngCavLA(self):
        return self._Diag_AngCavLA

    @DebugIt()
    def read_Diag_AngCavLB(self):
        return self._Diag_AngCavLB

    @DebugIt()
    def read_Diag_AngFwLA(self):
        return self._Diag_AngFwLA

    @DebugIt()
    def read_Diag_AngFwLB(self):
        return self._Diag_AngFwLB

    @DebugIt()
    def read_Diag_Vaccum1A(self):
        return self._Diag_Vaccum1A

    @DebugIt()
    def read_Diag_Vaccum1B(self):
        return self._Diag_Vaccum1B

    @DebugIt()
    def read_Diag_Vaccum2A(self):
        return self._Diag_Vaccum2A

    @DebugIt()
    def read_Diag_Vaccum2B(self):
        return self._Diag_Vaccum2B

    @DebugIt()
    def read_Diag_IcontrolSlowpiA(self):
        return self._Diag_IcontrolSlowpiA

    @DebugIt()
    def read_Diag_IcontrolSlowpiB(self):
        return self._Diag_IcontrolSlowpiB

    @DebugIt()
    def read_Diag_QcontrolSlowpiA(self):
        return self._Diag_QcontrolSlowpiA

    @DebugIt()
    def read_Diag_QcontrolSlowpiB(self):
        return self._Diag_QcontrolSlowpiB

    @DebugIt()
    def read_Diag_IcontrolFastpiA(self):
        return self._Diag_IcontrolFastpiA

    @DebugIt()
    def read_Diag_IcontrolFastpiB(self):
        return self._Diag_IcontrolFastpiB

    @DebugIt()
    def read_Diag_QcontrolFastpiA(self):
        return self._Diag_QcontrolFastpiA

    @DebugIt()
    def read_Diag_QcontrolFastpiB(self):
        return self._Diag_QcontrolFastpiB

    @DebugIt()
    def read_Diag_VcxoPoweredA(self):
        return self._Diag_VcxoPoweredA

    @DebugIt()
    def read_Diag_VcxoPoweredB(self):
        return self._Diag_VcxoPoweredB

    @DebugIt()
    def read_Diag_VcxoRefA(self):
        return self._Diag_VcxoRefA

    @DebugIt()
    def read_Diag_VcxoRefB(self):
        return self._Diag_VcxoRefB

    @DebugIt()
    def read_Diag_VcxoLockedA(self):
        return self._Diag_VcxoLockedA

    @DebugIt()
    def read_Diag_VcxoLockedB(self):
        return self._Diag_VcxoLockedB

    @DebugIt()
    def read_Diag_VcxoCableDisconnectedA(self):
        return self._Diag_VcxoCableDisconnectedA

    @DebugIt()
    def read_Diag_VcxoCableDisconnectedB(self):
        return self._Diag_VcxoCableDisconnectedB

    @DebugIt()
    def read_Diag_IpolarForAmplitudeLoopA(self):
        return self._Diag_IpolarForAmplitudeLoopA

    @DebugIt()
    def read_Diag_IpolarForAmplitudeLoopB(self):
        return self._Diag_IpolarForAmplitudeLoopB

    @DebugIt()
    def read_Diag_QpolarForAmplitudeLoopA(self):
        return self._Diag_QpolarForAmplitudeLoopA

    @DebugIt()
    def read_Diag_QpolarForAmplitudeLoopB(self):
        return self._Diag_QpolarForAmplitudeLoopB

    @DebugIt()
    def read_Diag_IpolarForPhaseLoopA(self):
        return self._Diag_IpolarForPhaseLoopA

    @DebugIt()
    def read_Diag_IpolarForPhaseLoopB(self):
        return self._Diag_IpolarForPhaseLoopB

    @DebugIt()
    def read_Diag_QpolarForPhaseLoopA(self):
        return self._Diag_QpolarForPhaseLoopA

    @DebugIt()
    def read_Diag_QpolarForPhaseLoopB(self):
        return self._Diag_QpolarForPhaseLoopB

    @DebugIt()
    def read_Diag_AmpInputOfAmpLoopA(self):
        return self._Diag_AmpInputOfAmpLoopA

    @DebugIt()
    def read_Diag_AmpInputOfAmpLoopB(self):
        return self._Diag_AmpInputOfAmpLoopB

    @DebugIt()
    def read_Diag_PhaseInputOfAmpLoopA(self):
        return self._Diag_PhaseInputOfAmpLoopA

    @DebugIt()
    def read_Diag_PhaseInputOfAmpLoopB(self):
        return self._Diag_PhaseInputOfAmpLoopB

    @DebugIt()
    def read_Diag_AmpInputOfPhaseLoopA(self):
        return self._Diag_AmpInputOfPhaseLoopA

    @DebugIt()
    def read_Diag_AmpInputOfPhaseLoopB(self):
        return self._Diag_AmpInputOfPhaseLoopB

    @DebugIt()
    def read_Diag_PhInputOfPhaseLoopA(self):
        return self._Diag_PhInputOfPhaseLoopA

    @DebugIt()
    def read_Diag_PhInputOfPhaseLoopB(self):
        return self._Diag_PhInputOfPhaseLoopB

    @DebugIt()
    def read_Diag_AmpLoopControlOutputA(self):
        return self._Diag_AmpLoopControlOutputA

    @DebugIt()
    def read_Diag_AmpLoopControlOutputB(self):
        return self._Diag_AmpLoopControlOutputB

    @DebugIt()
    def read_Diag_AmpLoopErrorA(self):
        return self._Diag_AmpLoopErrorA

    @DebugIt()
    def read_Diag_AmpLoopErrorB(self):
        return self._Diag_AmpLoopErrorB

    @DebugIt()
    def read_Diag_AmpLoopErrorAccumA(self):
        return self._Diag_AmpLoopErrorAccumA

    @DebugIt()
    def read_Diag_AmpLoopErrorAccumB(self):
        return self._Diag_AmpLoopErrorAccumB

    @DebugIt()
    def read_Diag_PhLoopControlOutputA(self):
        return self._Diag_PhLoopControlOutputA

    @DebugIt()
    def read_Diag_PhLoopControlOutputB(self):
        return self._Diag_PhLoopControlOutputB

    @DebugIt()
    def read_Diag_PhLoopErrorA(self):
        return self._Diag_PhLoopErrorA

    @DebugIt()
    def read_Diag_PhLoopErrorB(self):
        return self._Diag_PhLoopErrorB

    @DebugIt()
    def read_Diag_PhLoopErrorAccumA(self):
        return self._Diag_PhLoopErrorAccumA

    @DebugIt()
    def read_Diag_PhLoopErrorAccumB(self):
        return self._Diag_PhLoopErrorAccumB

    @DebugIt()
    def read_Diag_IpolarControlOutputA(self):
        return self._Diag_IpolarControlOutputA

    @DebugIt()
    def read_Diag_IpolarControlOutputB(self):
        return self._Diag_IpolarControlOutputB

    @DebugIt()
    def read_Diag_QpolarControlOutputA(self):
        return self._Diag_QpolarControlOutputA

    @DebugIt()
    def read_Diag_QpolarControlOutputB(self):
        return self._Diag_QpolarControlOutputB

    @DebugIt()
    def read_Diag_IcontrolSlowpiIqA(self):
        return self._Diag_IcontrolSlowpiIqA

    @DebugIt()
    def read_Diag_IcontrolSlowpiIqB(self):
        return self._Diag_IcontrolSlowpiIqB

    @DebugIt()
    def read_Diag_QcontrolSlowpiqA(self):
        return self._Diag_QcontrolSlowpiqA

    @DebugIt()
    def read_Diag_QcontrolSlowpiqB(self):
        return self._Diag_QcontrolSlowpiqB

    @DebugIt()
    def read_Diag_IcontrolFastpiIqA(self):
        return self._Diag_IcontrolFastpiIqA

    @DebugIt()
    def read_Diag_IcontrolFastpiIqB(self):
        return self._Diag_IcontrolFastpiIqB

    @DebugIt()
    def read_Diag_QcontrolFastpiIqA(self):
        return self._Diag_QcontrolFastpiIqA

    @DebugIt()
    def read_Diag_QcontrolFastpiIqB(self):
        return self._Diag_QcontrolFastpiIqB

    @DebugIt()
    def read_Diag_IloopinputSlowpiIqA(self):
        return self._Diag_IloopinputSlowpiIqA

    @DebugIt()
    def read_Diag_IloopinputSlowpiIqB(self):
        return self._Diag_IloopinputSlowpiIqB

    @DebugIt()
    def read_Diag_QloopinputSlowpiIqA(self):
        return self._Diag_QloopinputSlowpiIqA

    @DebugIt()
    def read_Diag_QloopinputSlowpiIqB(self):
        return self._Diag_QloopinputSlowpiIqB

    @DebugIt()
    def read_Diag_IloopinputFastpiIqA(self):
        return self._Diag_IloopinputFastpiIqA

    @DebugIt()
    def read_Diag_IloopinputFastpiIqB(self):
        return self._Diag_IloopinputFastpiIqB

    @DebugIt()
    def read_Diag_QloopinputFastpiIqA(self):
        return self._Diag_QloopinputFastpiIqA

    @DebugIt()
    def read_Diag_QloopinputFastpiIqB(self):
        return self._Diag_QloopinputFastpiIqB

    @DebugIt()
    def read_Diag_IrefloopinputFastpiIqA(self):
        return self._Diag_IrefloopinputFastpiIqA

    @DebugIt()
    def read_Diag_IrefloopinputFastpiIqB(self):
        return self._Diag_IrefloopinputFastpiIqB

    @DebugIt()
    def read_Diag_QrefloopinputFastpiIqA(self):
        return self._Diag_QrefloopinputFastpiIqA

    @DebugIt()
    def read_Diag_QrefloopinputFastpiIqB(self):
        return self._Diag_QrefloopinputFastpiIqB

    @DebugIt()
    def read_Diag_MovingPlungerAutoA(self):
        return self._Diag_MovingPlungerAutoA

    @DebugIt()
    def read_Diag_MovingPlungerAutoB(self):
        return self._Diag_MovingPlungerAutoB

    @DebugIt()
    def read_Diag_FreqUpA(self):
        return self._Diag_FreqUpA

    @DebugIt()
    def read_Diag_FreqUpB(self):
        return self._Diag_FreqUpB

    @DebugIt()
    def read_Diag_ManualTuningOnA(self):
        return self._Diag_ManualTuningOnA

    @DebugIt()
    def read_Diag_ManualTuningOnB(self):
        return self._Diag_ManualTuningOnB

    @DebugIt()
    def read_Diag_ManualTuningFreqUpA(self):
        return self._Diag_ManualTuningFreqUpA

    @DebugIt()
    def read_Diag_ManualTuningFreqUpB(self):
        return self._Diag_ManualTuningFreqUpB

    @DebugIt()
    def read_Diag_FwminA(self):
        return self._Diag_FwminA

    @DebugIt()
    def read_Diag_FwminB(self):
        return self._Diag_FwminB

    @DebugIt()
    def read_Diag_EpsItckDelayA(self):
        return self._Diag_EpsItckDelayA

    @DebugIt()
    def read_Diag_EpsItckDelayB(self):
        return self._Diag_EpsItckDelayB

    @DebugIt()
    def read_Diag_FimItckDelayA(self):
        return self._Diag_FimItckDelayA

    @DebugIt()
    def read_Diag_FimItckDelayB(self):
        return self._Diag_FimItckDelayB

    @DebugIt()
    def read_Diag_FdlTrigHwInputA(self):
        return self._Diag_FdlTrigHwInputA

    @DebugIt()
    def read_Diag_FdlTrigHwInputB(self):
        return self._Diag_FdlTrigHwInputB

    @DebugIt()
    def read_Diag_FdlTrigSwInputA(self):
        return self._Diag_FdlTrigSwInputA

    @DebugIt()
    def read_Diag_FdlTrigSwInputB(self):
        return self._Diag_FdlTrigSwInputB

    @DebugIt()
    def read_Diag_EpsItckA(self):
        return self._Diag_EpsItckA

    @DebugIt()
    def read_Diag_EpsItckB(self):
        return self._Diag_EpsItckB

    @DebugIt()
    def read_Diag_AmpMuxfwcircina(self):
        return self._Diag_AmpMuxfwcircina

    @DebugIt()
    def read_Diag_AmpSpare1a(self):
        return self._Diag_AmpSpare1a

    @DebugIt()
    def read_Diag_AmpMuxfwcircinb(self):
        return self._Diag_AmpMuxfwcircinb

    @DebugIt()
    def read_Diag_AmpSpare2a(self):
        return self._Diag_AmpSpare2a

    @DebugIt()
    def read_Diag_AmpSpare2b(self):
        return self._Diag_AmpSpare2b

    @DebugIt()
    def read_Diag_AmpErrora(self):
        return self._Diag_AmpErrora

    @DebugIt()
    def read_Diag_AmpErrorb(self):
        return self._Diag_AmpErrorb

    @DebugIt()
    def read_Diag_AmpSpare1b(self):
        return self._Diag_AmpSpare1b

    @DebugIt()
    def read_Diag_AmpErroraccumb(self):
        return self._Diag_AmpErroraccumb

    @DebugIt()
    def read_Diag_AmpErroraccuma(self):
        return self._Diag_AmpErroraccuma

    @DebugIt()
    def read_Diag_AmpControlfastpiiqb(self):
        return self._Diag_AmpControlfastpiiqb

    @DebugIt()
    def read_Diag_AmpControlfastpiiqa(self):
        return self._Diag_AmpControlfastpiiqa

    @DebugIt()
    def read_Diag_AmpControla(self):
        return self._Diag_AmpControla

    @DebugIt()
    def read_Diag_AmpPolarforamplitudeloopa(self):
        return self._Diag_AmpPolarforamplitudeloopa

    @DebugIt()
    def read_Diag_AmpPolarforamplitudeloopb(self):
        return self._Diag_AmpPolarforamplitudeloopb

    @DebugIt()
    def read_Diag_AmpControlb(self):
        return self._Diag_AmpControlb

    @DebugIt()
    def read_Diag_AmpMuxfwtet2b(self):
        return self._Diag_AmpMuxfwtet2b

    @DebugIt()
    def read_Diag_AmpLoopinputfastpiiqb(self):
        return self._Diag_AmpLoopinputfastpiiqb

    @DebugIt()
    def read_Diag_AmpLoopinputfastpiiqa(self):
        return self._Diag_AmpLoopinputfastpiiqa

    @DebugIt()
    def read_Diag_AmpRefa(self):
        return self._Diag_AmpRefa

    @DebugIt()
    def read_Diag_AmpMuxfwcava(self):
        return self._Diag_AmpMuxfwcava

    @DebugIt()
    def read_Diag_AmpMuxfwcavb(self):
        return self._Diag_AmpMuxfwcavb

    @DebugIt()
    def read_Diag_AmpRefb(self):
        return self._Diag_AmpRefb

    @DebugIt()
    def read_Diag_AmpControl2a(self):
        return self._Diag_AmpControl2a

    @DebugIt()
    def read_Diag_AmpControl2b(self):
        return self._Diag_AmpControl2b

    @DebugIt()
    def read_Diag_AmpFwtet1loopsb(self):
        return self._Diag_AmpFwtet1loopsb

    @DebugIt()
    def read_Diag_AmpFwtet1loopsa(self):
        return self._Diag_AmpFwtet1loopsa

    @DebugIt()
    def read_Diag_AmpPolarforphaseloopb(self):
        return self._Diag_AmpPolarforphaseloopb

    @DebugIt()
    def read_Diag_AmpPolarforphaseloopa(self):
        return self._Diag_AmpPolarforphaseloopa

    @DebugIt()
    def read_Diag_AmpPolarcontroloutputb(self):
        return self._Diag_AmpPolarcontroloutputb

    @DebugIt()
    def read_Diag_AmpPolarcontroloutputa(self):
        return self._Diag_AmpPolarcontroloutputa

    @DebugIt()
    def read_Diag_AmpFwtet2loopsa(self):
        return self._Diag_AmpFwtet2loopsa

    @DebugIt()
    def read_Diag_AmpCavloopsa(self):
        return self._Diag_AmpCavloopsa

    @DebugIt()
    def read_Diag_AmpCavloopsb(self):
        return self._Diag_AmpCavloopsb

    @DebugIt()
    def read_Diag_AmpFwtet2loopsb(self):
        return self._Diag_AmpFwtet2loopsb

    @DebugIt()
    def read_Diag_AmpLoopinputslowpiiqa(self):
        return self._Diag_AmpLoopinputslowpiiqa

    @DebugIt()
    def read_Diag_AmpLoopinputslowpiiqb(self):
        return self._Diag_AmpLoopinputslowpiiqb

    @DebugIt()
    def read_Diag_AmpRefloopinputfastpiiqb(self):
        return self._Diag_AmpRefloopinputfastpiiqb

    @DebugIt()
    def read_Diag_AmpRefloopinputfastpiiqa(self):
        return self._Diag_AmpRefloopinputfastpiiqa

    @DebugIt()
    def read_Diag_AmpControl1a(self):
        return self._Diag_AmpControl1a

    @DebugIt()
    def read_Diag_AmpControl1b(self):
        return self._Diag_AmpControl1b

    @DebugIt()
    def read_Diag_AmpMuxfwtet2a(self):
        return self._Diag_AmpMuxfwtet2a

    @DebugIt()
    def read_Diag_AmpMuxcavb(self):
        return self._Diag_AmpMuxcavb

    @DebugIt()
    def read_Diag_AmpMuxcava(self):
        return self._Diag_AmpMuxcava

    @DebugIt()
    def read_Diag_AmpMuxfwtet1b(self):
        return self._Diag_AmpMuxfwtet1b

    @DebugIt()
    def read_Diag_AmpControlfastpib(self):
        return self._Diag_AmpControlfastpib

    @DebugIt()
    def read_Diag_AmpFwcircinloopsa(self):
        return self._Diag_AmpFwcircinloopsa

    @DebugIt()
    def read_Diag_AmpFwcircinloopsb(self):
        return self._Diag_AmpFwcircinloopsb

    @DebugIt()
    def read_Diag_AmpControlfastpia(self):
        return self._Diag_AmpControlfastpia

    @DebugIt()
    def read_Diag_AmpFwcavloopsa(self):
        return self._Diag_AmpFwcavloopsa

    @DebugIt()
    def read_Diag_AmpMuxfwtet1a(self):
        return self._Diag_AmpMuxfwtet1a

    @DebugIt()
    def read_Diag_AmpFwcavloopsb(self):
        return self._Diag_AmpFwcavloopsb

    @DebugIt()
    def read_Diag_AmpMob(self):
        return self._Diag_AmpMob

    @DebugIt()
    def read_Diag_AmpMoa(self):
        return self._Diag_AmpMoa

    @DebugIt()
    def read_Diag_AmpControlslowpia(self):
        return self._Diag_AmpControlslowpia

    @DebugIt()
    def read_Diag_AmpControlslowpib(self):
        return self._Diag_AmpControlslowpib

    @DebugIt()
    def read_Diag_PhMuxfwcircina(self):
        return self._Diag_PhMuxfwcircina

    @DebugIt()
    def read_Diag_PhSpare1a(self):
        return self._Diag_PhSpare1a

    @DebugIt()
    def read_Diag_PhMuxfwcircinb(self):
        return self._Diag_PhMuxfwcircinb

    @DebugIt()
    def read_Diag_PhSpare2a(self):
        return self._Diag_PhSpare2a

    @DebugIt()
    def read_Diag_PhSpare2b(self):
        return self._Diag_PhSpare2b

    @DebugIt()
    def read_Diag_PhErrora(self):
        return self._Diag_PhErrora

    @DebugIt()
    def read_Diag_PhErrorb(self):
        return self._Diag_PhErrorb

    @DebugIt()
    def read_Diag_PhSpare1b(self):
        return self._Diag_PhSpare1b

    @DebugIt()
    def read_Diag_PhErroraccumb(self):
        return self._Diag_PhErroraccumb

    @DebugIt()
    def read_Diag_PhErroraccuma(self):
        return self._Diag_PhErroraccuma

    @DebugIt()
    def read_Diag_PhControlfastpiiqb(self):
        return self._Diag_PhControlfastpiiqb

    @DebugIt()
    def read_Diag_PhControlfastpiiqa(self):
        return self._Diag_PhControlfastpiiqa

    @DebugIt()
    def read_Diag_PhControla(self):
        return self._Diag_PhControla

    @DebugIt()
    def read_Diag_PhPolarforamplitudeloopa(self):
        return self._Diag_PhPolarforamplitudeloopa

    @DebugIt()
    def read_Diag_PhPolarforamplitudeloopb(self):
        return self._Diag_PhPolarforamplitudeloopb

    @DebugIt()
    def read_Diag_PhControlb(self):
        return self._Diag_PhControlb

    @DebugIt()
    def read_Diag_PhMuxfwtet2b(self):
        return self._Diag_PhMuxfwtet2b

    @DebugIt()
    def read_Diag_PhLoopinputfastpiiqb(self):
        return self._Diag_PhLoopinputfastpiiqb

    @DebugIt()
    def read_Diag_PhLoopinputfastpiiqa(self):
        return self._Diag_PhLoopinputfastpiiqa

    @DebugIt()
    def read_Diag_PhRefa(self):
        return self._Diag_PhRefa

    @DebugIt()
    def read_Diag_PhMuxfwcava(self):
        return self._Diag_PhMuxfwcava

    @DebugIt()
    def read_Diag_PhMuxfwcavb(self):
        return self._Diag_PhMuxfwcavb

    @DebugIt()
    def read_Diag_PhRefb(self):
        return self._Diag_PhRefb

    @DebugIt()
    def read_Diag_PhControl2a(self):
        return self._Diag_PhControl2a

    @DebugIt()
    def read_Diag_PhControl2b(self):
        return self._Diag_PhControl2b

    @DebugIt()
    def read_Diag_PhFwtet1loopsb(self):
        return self._Diag_PhFwtet1loopsb

    @DebugIt()
    def read_Diag_PhFwtet1loopsa(self):
        return self._Diag_PhFwtet1loopsa

    @DebugIt()
    def read_Diag_PhPolarforphaseloopb(self):
        return self._Diag_PhPolarforphaseloopb

    @DebugIt()
    def read_Diag_PhPolarforphaseloopa(self):
        return self._Diag_PhPolarforphaseloopa

    @DebugIt()
    def read_Diag_PhPolarcontroloutputb(self):
        return self._Diag_PhPolarcontroloutputb

    @DebugIt()
    def read_Diag_PhPolarcontroloutputa(self):
        return self._Diag_PhPolarcontroloutputa

    @DebugIt()
    def read_Diag_PhFwtet2loopsa(self):
        return self._Diag_PhFwtet2loopsa

    @DebugIt()
    def read_Diag_PhCavloopsa(self):
        return self._Diag_PhCavloopsa

    @DebugIt()
    def read_Diag_PhCavloopsb(self):
        return self._Diag_PhCavloopsb

    @DebugIt()
    def read_Diag_PhFwtet2loopsb(self):
        return self._Diag_PhFwtet2loopsb

    @DebugIt()
    def read_Diag_PhLoopinputslowpiiqa(self):
        return self._Diag_PhLoopinputslowpiiqa

    @DebugIt()
    def read_Diag_PhLoopinputslowpiiqb(self):
        return self._Diag_PhLoopinputslowpiiqb

    @DebugIt()
    def read_Diag_PhRefloopinputfastpiiqb(self):
        return self._Diag_PhRefloopinputfastpiiqb

    @DebugIt()
    def read_Diag_PhRefloopinputfastpiiqa(self):
        return self._Diag_PhRefloopinputfastpiiqa

    @DebugIt()
    def read_Diag_PhControl1a(self):
        return self._Diag_PhControl1a

    @DebugIt()
    def read_Diag_PhControl1b(self):
        return self._Diag_PhControl1b

    @DebugIt()
    def read_Diag_PhMuxfwtet2a(self):
        return self._Diag_PhMuxfwtet2a

    @DebugIt()
    def read_Diag_PhMuxcavb(self):
        return self._Diag_PhMuxcavb

    @DebugIt()
    def read_Diag_PhMuxcava(self):
        return self._Diag_PhMuxcava

    @DebugIt()
    def read_Diag_PhMuxfwtet1b(self):
        return self._Diag_PhMuxfwtet1b

    @DebugIt()
    def read_Diag_PhControlfastpib(self):
        return self._Diag_PhControlfastpib

    @DebugIt()
    def read_Diag_PhFwcircinloopsa(self):
        return self._Diag_PhFwcircinloopsa

    @DebugIt()
    def read_Diag_PhFwcircinloopsb(self):
        return self._Diag_PhFwcircinloopsb

    @DebugIt()
    def read_Diag_PhControlfastpia(self):
        return self._Diag_PhControlfastpia

    @DebugIt()
    def read_Diag_PhFwcavloopsa(self):
        return self._Diag_PhFwcavloopsa

    @DebugIt()
    def read_Diag_PhMuxfwtet1a(self):
        return self._Diag_PhMuxfwtet1a

    @DebugIt()
    def read_Diag_PhFwcavloopsb(self):
        return self._Diag_PhFwcavloopsb

    @DebugIt()
    def read_Diag_PhMob(self):
        return self._Diag_PhMob

    @DebugIt()
    def read_Diag_PhMoa(self):
        return self._Diag_PhMoa

    @DebugIt()
    def read_Diag_PhControlslowpia(self):
        return self._Diag_PhControlslowpia

    @DebugIt()
    def read_Diag_PhControlslowpib(self):
        return self._Diag_PhControlslowpib

    @command
    def read_diagnostics(self):
        perseus_utils.start_reading_diagnostics(self.perseus, 'A')
        perseus_utils.start_reading_diagnostics(self.perseus, 'B')

        self._Diag_IcavLoopsA = perseus_utils.read_diag_milivolts(self.perseus, 0, 'A')
        self.push_change_event("Diag_IcavLoopsA", self._Diag_IcavLoopsA)
        self._Diag_IcavLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 0, 'B')
        self.push_change_event("Diag_IcavLoopsB", self._Diag_IcavLoopsB)
        self._Diag_QcavLoopsA = perseus_utils.read_diag_milivolts(self.perseus, 1, 'A')
        self.push_change_event("Diag_QcavLoopsA", self._Diag_QcavLoopsA)
        self._Diag_QcavLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 1, 'B')
        self.push_change_event("Diag_QcavLoopsB", self._Diag_QcavLoopsB)
        self._Diag_IcontrolA = perseus_utils.read_diag_milivolts(self.perseus, 2, 'A')
        self.push_change_event("Diag_IcontrolA", self._Diag_IcontrolA)
        self._Diag_IcontrolB = perseus_utils.read_diag_milivolts(self.perseus, 2, 'B')
        self.push_change_event("Diag_IcontrolB", self._Diag_IcontrolB)
        self._Diag_QcontrolA = perseus_utils.read_diag_milivolts(self.perseus, 3, 'A')
        self.push_change_event("Diag_QcontrolA", self._Diag_QcontrolA)
        self._Diag_QcontrolB = perseus_utils.read_diag_milivolts(self.perseus, 3, 'B')
        self.push_change_event("Diag_QcontrolB", self._Diag_QcontrolB)
        self._Diag_Icontrol1A = perseus_utils.read_diag_milivolts(self.perseus, 4, 'A')
        self.push_change_event("Diag_Icontrol1A", self._Diag_Icontrol1A)
        self._Diag_Icontrol1B = perseus_utils.read_diag_milivolts(self.perseus, 4, 'B')
        self.push_change_event("Diag_Icontrol1B", self._Diag_Icontrol1B)
        self._Diag_Qcontrol1A = perseus_utils.read_diag_milivolts(self.perseus, 5, 'A')
        self.push_change_event("Diag_Qcontrol1A", self._Diag_Qcontrol1A)
        self._Diag_Qcontrol1B = perseus_utils.read_diag_milivolts(self.perseus, 5, 'B')
        self.push_change_event("Diag_Qcontrol1B", self._Diag_Qcontrol1B)
        self._Diag_Icontrol2A = perseus_utils.read_diag_milivolts(self.perseus, 6, 'A')
        self.push_change_event("Diag_Icontrol2A", self._Diag_Icontrol2A)
        self._Diag_Icontrol2B = perseus_utils.read_diag_milivolts(self.perseus, 6, 'B')
        self.push_change_event("Diag_Icontrol2B", self._Diag_Icontrol2B)
        self._Diag_Qcontrol2A = perseus_utils.read_diag_milivolts(self.perseus, 7, 'A')
        self.push_change_event("Diag_Qcontrol2A", self._Diag_Qcontrol2A)
        self._Diag_Qcontrol2B = perseus_utils.read_diag_milivolts(self.perseus, 7, 'B')
        self.push_change_event("Diag_Qcontrol2B", self._Diag_Qcontrol2B)
        self._Diag_IerrorA = perseus_utils.read_diag_milivolts(self.perseus, 8, 'A')
        self.push_change_event("Diag_IerrorA", self._Diag_IerrorA)
        self._Diag_IerrorB = perseus_utils.read_diag_milivolts(self.perseus, 8, 'B')
        self.push_change_event("Diag_IerrorB", self._Diag_IerrorB)
        self._Diag_QerrorA = perseus_utils.read_diag_milivolts(self.perseus, 9, 'A')
        self.push_change_event("Diag_QerrorA", self._Diag_QerrorA)
        self._Diag_QerrorB = perseus_utils.read_diag_milivolts(self.perseus, 9, 'B')
        self.push_change_event("Diag_QerrorB", self._Diag_QerrorB)
        self._Diag_IerroraccumA = perseus_utils.read_diag_milivolts(self.perseus, 10, 'A')
        self.push_change_event("Diag_IerroraccumA", self._Diag_IerroraccumA)
        self._Diag_IerroraccumB = perseus_utils.read_diag_milivolts(self.perseus, 10, 'B')
        self.push_change_event("Diag_IerroraccumB", self._Diag_IerroraccumB)
        self._Diag_QerroraccumA = perseus_utils.read_diag_milivolts(self.perseus, 11, 'A')
        self.push_change_event("Diag_QerroraccumA", self._Diag_QerroraccumA)
        self._Diag_QerroraccumB = perseus_utils.read_diag_milivolts(self.perseus, 11, 'B')
        self.push_change_event("Diag_QerroraccumB", self._Diag_QerroraccumB)
        self._Diag_IrefA = perseus_utils.read_diag_milivolts(self.perseus, 12, 'A')
        self.push_change_event("Diag_IrefA", self._Diag_IrefA)
        self._Diag_IrefB = perseus_utils.read_diag_milivolts(self.perseus, 12, 'B')
        self.push_change_event("Diag_IrefB", self._Diag_IrefB)
        self._Diag_QrefA = perseus_utils.read_diag_milivolts(self.perseus, 13, 'A')
        self.push_change_event("Diag_QrefA", self._Diag_QrefA)
        self._Diag_QrefB = perseus_utils.read_diag_milivolts(self.perseus, 13, 'B')
        self.push_change_event("Diag_QrefB", self._Diag_QrefB)
        self._Diag_IFwCavLoopsA = perseus_utils.read_diag_milivolts(self.perseus, 14, 'A')
        self.push_change_event("Diag_IFwCavLoopsA", self._Diag_IFwCavLoopsA)
        self._Diag_IFwCavLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 14, 'B')
        self.push_change_event("Diag_IFwCavLoopsB", self._Diag_IFwCavLoopsB)
        self._Diag_QFwCavLoopsA = perseus_utils.read_diag_milivolts(self.perseus, 15, 'A')
        self.push_change_event("Diag_QFwCavLoopsA", self._Diag_QFwCavLoopsA)
        self._Diag_QFwCavLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 15, 'B')
        self.push_change_event("Diag_QFwCavLoopsB", self._Diag_QFwCavLoopsB)
        self._Diag_IFwTet1LoopsA = perseus_utils.read_diag_milivolts(self.perseus, 16, 'A')
        self.push_change_event("Diag_IFwTet1LoopsA", self._Diag_IFwTet1LoopsA)
        self._Diag_IFwTet1LoopsB = perseus_utils.read_diag_milivolts(self.perseus, 16, 'B')
        self.push_change_event("Diag_IFwTet1LoopsB", self._Diag_IFwTet1LoopsB)
        self._Diag_QFwTet1LoopsA = perseus_utils.read_diag_milivolts(self.perseus, 17, 'A')
        self.push_change_event("Diag_QFwTet1LoopsA", self._Diag_QFwTet1LoopsA)
        self._Diag_QFwTet1LoopsB = perseus_utils.read_diag_milivolts(self.perseus, 17, 'B')
        self.push_change_event("Diag_QFwTet1LoopsB", self._Diag_QFwTet1LoopsB)
        self._Diag_IFwTet2LoopsA = perseus_utils.read_diag_milivolts(self.perseus, 18, 'A')
        self.push_change_event("Diag_IFwTet2LoopsA", self._Diag_IFwTet2LoopsA)
        self._Diag_IFwTet2LoopsB = perseus_utils.read_diag_milivolts(self.perseus, 18, 'B')
        self.push_change_event("Diag_IFwTet2LoopsB", self._Diag_IFwTet2LoopsB)
        self._Diag_QFwTet2LoopsA = perseus_utils.read_diag_milivolts(self.perseus, 19, 'A')
        self.push_change_event("Diag_QFwTet2LoopsA", self._Diag_QFwTet2LoopsA)
        self._Diag_QFwTet2LoopsB = perseus_utils.read_diag_milivolts(self.perseus, 19, 'B')
        self.push_change_event("Diag_QFwTet2LoopsB", self._Diag_QFwTet2LoopsB)
        self._Diag_IFwCircInLoopsA = perseus_utils.read_diag_milivolts(self.perseus, 20, 'A')
        self.push_change_event("Diag_IFwCircInLoopsA", self._Diag_IFwCircInLoopsA)
        self._Diag_IFwCircInLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 20, 'B')
        self.push_change_event("Diag_IFwCircInLoopsB", self._Diag_IFwCircInLoopsB)
        self._Diag_QFwCircInLoopsA = perseus_utils.read_diag_milivolts(self.perseus, 21, 'A')
        self.push_change_event("Diag_QFwCircInLoopsA", self._Diag_QFwCircInLoopsA)
        self._Diag_QFwCircInLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 21, 'B')
        self.push_change_event("Diag_QFwCircInLoopsB", self._Diag_QFwCircInLoopsB)
        self._Diag_ImoA = perseus_utils.read_diag_milivolts(self.perseus, 22, 'A')
        self.push_change_event("Diag_ImoA", self._Diag_ImoA)
        self._Diag_ImoB = perseus_utils.read_diag_milivolts(self.perseus, 22, 'B')
        self.push_change_event("Diag_ImoB", self._Diag_ImoB)
        self._Diag_QmoA = perseus_utils.read_diag_milivolts(self.perseus, 23, 'A')
        self.push_change_event("Diag_QmoA", self._Diag_QmoA)
        self._Diag_QmoB = perseus_utils.read_diag_milivolts(self.perseus, 23, 'B')
        self.push_change_event("Diag_QmoB", self._Diag_QmoB)
        self._Diag_Ispare1A = perseus_utils.read_diag_milivolts(self.perseus, 24, 'A')
        self.push_change_event("Diag_Ispare1A", self._Diag_Ispare1A)
        self._Diag_Ispare1B = perseus_utils.read_diag_milivolts(self.perseus, 24, 'B')
        self.push_change_event("Diag_Ispare1B", self._Diag_Ispare1B)
        self._Diag_Qspare1A = perseus_utils.read_diag_milivolts(self.perseus, 25, 'A')
        self.push_change_event("Diag_Qspare1A", self._Diag_Qspare1A)
        self._Diag_Qspare1B = perseus_utils.read_diag_milivolts(self.perseus, 25, 'B')
        self.push_change_event("Diag_Qspare1B", self._Diag_Qspare1B)
        self._Diag_Ispare2A = perseus_utils.read_diag_milivolts(self.perseus, 26, 'A')
        self.push_change_event("Diag_Ispare2A", self._Diag_Ispare2A)
        self._Diag_Ispare2B = perseus_utils.read_diag_milivolts(self.perseus, 26, 'B')
        self.push_change_event("Diag_Ispare2B", self._Diag_Ispare2B)
        self._Diag_Qspare2A = perseus_utils.read_diag_milivolts(self.perseus, 27, 'A')
        self.push_change_event("Diag_Qspare2A", self._Diag_Qspare2A)
        self._Diag_Qspare2B = perseus_utils.read_diag_milivolts(self.perseus, 27, 'B')
        self.push_change_event("Diag_Qspare2B", self._Diag_Qspare2B)
        self._Diag_IMuxCavA = perseus_utils.read_diag_milivolts(self.perseus, 28, 'A')
        self.push_change_event("Diag_IMuxCavA", self._Diag_IMuxCavA)
        self._Diag_IMuxCavB = perseus_utils.read_diag_milivolts(self.perseus, 28, 'B')
        self.push_change_event("Diag_IMuxCavB", self._Diag_IMuxCavB)
        self._Diag_QMuxCavA = perseus_utils.read_diag_milivolts(self.perseus, 29, 'A')
        self.push_change_event("Diag_QMuxCavA", self._Diag_QMuxCavA)
        self._Diag_QMuxCavB = perseus_utils.read_diag_milivolts(self.perseus, 29, 'B')
        self.push_change_event("Diag_QMuxCavB", self._Diag_QMuxCavB)
        self._Diag_IMuxFwCavA = perseus_utils.read_diag_milivolts(self.perseus, 30, 'A')
        self.push_change_event("Diag_IMuxFwCavA", self._Diag_IMuxFwCavA)
        self._Diag_IMuxFwCavB = perseus_utils.read_diag_milivolts(self.perseus, 30, 'B')
        self.push_change_event("Diag_IMuxFwCavB", self._Diag_IMuxFwCavB)
        self._Diag_QMuxFwCavA = perseus_utils.read_diag_milivolts(self.perseus, 31, 'A')
        self.push_change_event("Diag_QMuxFwCavA", self._Diag_QMuxFwCavA)
        self._Diag_QMuxFwCavB = perseus_utils.read_diag_milivolts(self.perseus, 31, 'B')
        self.push_change_event("Diag_QMuxFwCavB", self._Diag_QMuxFwCavB)
        self._Diag_IMuxFwTet1A = perseus_utils.read_diag_milivolts(self.perseus, 32, 'A')
        self.push_change_event("Diag_IMuxFwTet1A", self._Diag_IMuxFwTet1A)
        self._Diag_IMuxFwTet1B = perseus_utils.read_diag_milivolts(self.perseus, 32, 'B')
        self.push_change_event("Diag_IMuxFwTet1B", self._Diag_IMuxFwTet1B)
        self._Diag_QMuxFwTet1A = perseus_utils.read_diag_milivolts(self.perseus, 33, 'A')
        self.push_change_event("Diag_QMuxFwTet1A", self._Diag_QMuxFwTet1A)
        self._Diag_QMuxFwTet1B = perseus_utils.read_diag_milivolts(self.perseus, 33, 'B')
        self.push_change_event("Diag_QMuxFwTet1B", self._Diag_QMuxFwTet1B)
        self._Diag_IMuxFwTet2A = perseus_utils.read_diag_milivolts(self.perseus, 34, 'A')
        self.push_change_event("Diag_IMuxFwTet2A", self._Diag_IMuxFwTet2A)
        self._Diag_IMuxFwTet2B = perseus_utils.read_diag_milivolts(self.perseus, 34, 'B')
        self.push_change_event("Diag_IMuxFwTet2B", self._Diag_IMuxFwTet2B)
        self._Diag_QMuxFwTet2A = perseus_utils.read_diag_milivolts(self.perseus, 35, 'A')
        self.push_change_event("Diag_QMuxFwTet2A", self._Diag_QMuxFwTet2A)
        self._Diag_QMuxFwTet2B = perseus_utils.read_diag_milivolts(self.perseus, 35, 'B')
        self.push_change_event("Diag_QMuxFwTet2B", self._Diag_QMuxFwTet2B)
        self._Diag_IMuxFwCircInA = perseus_utils.read_diag_milivolts(self.perseus, 36, 'A')
        self.push_change_event("Diag_IMuxFwCircInA", self._Diag_IMuxFwCircInA)
        self._Diag_IMuxFwCircInB = perseus_utils.read_diag_milivolts(self.perseus, 36, 'B')
        self.push_change_event("Diag_IMuxFwCircInB", self._Diag_IMuxFwCircInB)
        self._Diag_QMuxFwCircInA = perseus_utils.read_diag_milivolts(self.perseus, 37, 'A')
        self.push_change_event("Diag_QMuxFwCircInA", self._Diag_QMuxFwCircInA)
        self._Diag_QMuxFwCircInB = perseus_utils.read_diag_milivolts(self.perseus, 37, 'B')
        self.push_change_event("Diag_QMuxFwCircInB", self._Diag_QMuxFwCircInB)
        self._Diag_AmpCavA = perseus_utils.read_diag_milivolts(self.perseus, 38, 'A')
        self.push_change_event("Diag_AmpCavA", self._Diag_AmpCavA)
        self._Diag_AmpCavB = perseus_utils.read_diag_milivolts(self.perseus, 38, 'B')
        self.push_change_event("Diag_AmpCavB", self._Diag_AmpCavB)
        self._Diag_AmpFwA = perseus_utils.read_diag_milivolts(self.perseus, 39, 'A')
        self.push_change_event("Diag_AmpFwA", self._Diag_AmpFwA)
        self._Diag_AmpFwB = perseus_utils.read_diag_milivolts(self.perseus, 39, 'B')
        self.push_change_event("Diag_AmpFwB", self._Diag_AmpFwB)
        self._Diag_AngCavFwA = perseus_utils.read_diag_angle(self.perseus, 40, 'A')
        self.push_change_event("Diag_AngCavFwA", self._Diag_AngCavFwA)
        self._Diag_AngCavFwB = perseus_utils.read_diag_angle(self.perseus, 40, 'B')
        self.push_change_event("Diag_AngCavFwB", self._Diag_AngCavFwB)
        self._Diag_AngCavLA = perseus_utils.read_diag_angle(self.perseus, 41, 'A')
        self.push_change_event("Diag_AngCavLA", self._Diag_AngCavLA)
        self._Diag_AngCavLB = perseus_utils.read_diag_angle(self.perseus, 41, 'B')
        self.push_change_event("Diag_AngCavLB", self._Diag_AngCavLB)
        self._Diag_AngFwLA = perseus_utils.read_diag_angle(self.perseus, 42, 'A')
        self.push_change_event("Diag_AngFwLA", self._Diag_AngFwLA)
        self._Diag_AngFwLB = perseus_utils.read_diag_angle(self.perseus, 42, 'B')
        self.push_change_event("Diag_AngFwLB", self._Diag_AngFwLB)
        self._Diag_Vaccum1A = bool(perseus_utils.read_diag_direct(self.perseus, 43, 'A'))
        self.push_change_event("Diag_Vaccum1A", self._Diag_Vaccum1A)
        self._Diag_Vaccum1B = bool(perseus_utils.read_diag_direct(self.perseus, 43, 'B'))
        self.push_change_event("Diag_Vaccum1B", self._Diag_Vaccum1B)
        self._Diag_Vaccum2A = bool(perseus_utils.read_diag_direct(self.perseus, 44, 'A'))
        self.push_change_event("Diag_Vaccum2A", self._Diag_Vaccum2A)
        self._Diag_Vaccum2B = bool(perseus_utils.read_diag_direct(self.perseus, 44, 'B'))
        self.push_change_event("Diag_Vaccum2B", self._Diag_Vaccum2B)
        self._Diag_IcontrolSlowpiA = perseus_utils.read_diag_milivolts(self.perseus, 45, 'A')
        self.push_change_event("Diag_IcontrolSlowpiA", self._Diag_IcontrolSlowpiA)
        self._Diag_IcontrolSlowpiB = perseus_utils.read_diag_milivolts(self.perseus, 45, 'B')
        self.push_change_event("Diag_IcontrolSlowpiB", self._Diag_IcontrolSlowpiB)
        self._Diag_QcontrolSlowpiA = perseus_utils.read_diag_milivolts(self.perseus, 46, 'A')
        self.push_change_event("Diag_QcontrolSlowpiA", self._Diag_QcontrolSlowpiA)
        self._Diag_QcontrolSlowpiB = perseus_utils.read_diag_milivolts(self.perseus, 46, 'B')
        self.push_change_event("Diag_QcontrolSlowpiB", self._Diag_QcontrolSlowpiB)
        self._Diag_IcontrolFastpiA = perseus_utils.read_diag_milivolts(self.perseus, 47, 'A')
        self.push_change_event("Diag_IcontrolFastpiA", self._Diag_IcontrolFastpiA)
        self._Diag_IcontrolFastpiB = perseus_utils.read_diag_milivolts(self.perseus, 47, 'B')
        self.push_change_event("Diag_IcontrolFastpiB", self._Diag_IcontrolFastpiB)
        self._Diag_QcontrolFastpiA = perseus_utils.read_diag_milivolts(self.perseus, 48, 'A')
        self.push_change_event("Diag_QcontrolFastpiA", self._Diag_QcontrolFastpiA)
        self._Diag_QcontrolFastpiB = perseus_utils.read_diag_milivolts(self.perseus, 48, 'B')
        self.push_change_event("Diag_QcontrolFastpiB", self._Diag_QcontrolFastpiB)
        self._Diag_VcxoPoweredA = bool(perseus_utils.read_diag_direct(self.perseus, 50, 'A'))
        self.push_change_event("Diag_VcxoPoweredA", self._Diag_VcxoPoweredA)
        self._Diag_VcxoPoweredB = bool(perseus_utils.read_diag_direct(self.perseus, 50, 'B'))
        self.push_change_event("Diag_VcxoPoweredB", self._Diag_VcxoPoweredB)
        self._Diag_VcxoRefA = bool(perseus_utils.read_diag_direct(self.perseus, 51, 'A'))
        self.push_change_event("Diag_VcxoRefA", self._Diag_VcxoRefA)
        self._Diag_VcxoRefB = bool(perseus_utils.read_diag_direct(self.perseus, 51, 'B'))
        self.push_change_event("Diag_VcxoRefB", self._Diag_VcxoRefB)
        self._Diag_VcxoLockedA = bool(perseus_utils.read_diag_direct(self.perseus, 52, 'A'))
        self.push_change_event("Diag_VcxoLockedA", self._Diag_VcxoLockedA)
        self._Diag_VcxoLockedB = bool(perseus_utils.read_diag_direct(self.perseus, 52, 'B'))
        self.push_change_event("Diag_VcxoLockedB", self._Diag_VcxoLockedB)
        self._Diag_VcxoCableDisconnectedA = bool(perseus_utils.read_diag_direct(self.perseus, 53, 'A'))
        self.push_change_event("Diag_VcxoCableDisconnectedA", self._Diag_VcxoCableDisconnectedA)
        self._Diag_VcxoCableDisconnectedB = bool(perseus_utils.read_diag_direct(self.perseus, 53, 'B'))
        self.push_change_event("Diag_VcxoCableDisconnectedB", self._Diag_VcxoCableDisconnectedB)
        self._Diag_IpolarForAmplitudeLoopA = perseus_utils.read_diag_milivolts(self.perseus, 100, 'A')
        self.push_change_event("Diag_IpolarForAmplitudeLoopA", self._Diag_IpolarForAmplitudeLoopA)
        self._Diag_IpolarForAmplitudeLoopB = perseus_utils.read_diag_milivolts(self.perseus, 100, 'B')
        self.push_change_event("Diag_IpolarForAmplitudeLoopB", self._Diag_IpolarForAmplitudeLoopB)
        self._Diag_QpolarForAmplitudeLoopA = perseus_utils.read_diag_milivolts(self.perseus, 101, 'A')
        self.push_change_event("Diag_QpolarForAmplitudeLoopA", self._Diag_QpolarForAmplitudeLoopA)
        self._Diag_QpolarForAmplitudeLoopB = perseus_utils.read_diag_milivolts(self.perseus, 101, 'B')
        self.push_change_event("Diag_QpolarForAmplitudeLoopB", self._Diag_QpolarForAmplitudeLoopB)
        self._Diag_IpolarForPhaseLoopA = perseus_utils.read_diag_milivolts(self.perseus, 102, 'A')
        self.push_change_event("Diag_IpolarForPhaseLoopA", self._Diag_IpolarForPhaseLoopA)
        self._Diag_IpolarForPhaseLoopB = perseus_utils.read_diag_milivolts(self.perseus, 102, 'B')
        self.push_change_event("Diag_IpolarForPhaseLoopB", self._Diag_IpolarForPhaseLoopB)
        self._Diag_QpolarForPhaseLoopA = perseus_utils.read_diag_milivolts(self.perseus, 103, 'A')
        self.push_change_event("Diag_QpolarForPhaseLoopA", self._Diag_QpolarForPhaseLoopA)
        self._Diag_QpolarForPhaseLoopB = perseus_utils.read_diag_milivolts(self.perseus, 103, 'B')
        self.push_change_event("Diag_QpolarForPhaseLoopB", self._Diag_QpolarForPhaseLoopB)
        self._Diag_AmpInputOfAmpLoopA = perseus_utils.read_diag_milivolts(self.perseus, 104, 'A')
        self.push_change_event("Diag_AmpInputOfAmpLoopA", self._Diag_AmpInputOfAmpLoopA)
        self._Diag_AmpInputOfAmpLoopB = perseus_utils.read_diag_milivolts(self.perseus, 104, 'B')
        self.push_change_event("Diag_AmpInputOfAmpLoopB", self._Diag_AmpInputOfAmpLoopB)
        self._Diag_PhaseInputOfAmpLoopA = perseus_utils.read_diag_milivolts(self.perseus, 105, 'A')
        self.push_change_event("Diag_PhaseInputOfAmpLoopA", self._Diag_PhaseInputOfAmpLoopA)
        self._Diag_PhaseInputOfAmpLoopB = perseus_utils.read_diag_milivolts(self.perseus, 105, 'B')
        self.push_change_event("Diag_PhaseInputOfAmpLoopB", self._Diag_PhaseInputOfAmpLoopB)
        self._Diag_AmpInputOfPhaseLoopA = perseus_utils.read_diag_milivolts(self.perseus, 106, 'A')
        self.push_change_event("Diag_AmpInputOfPhaseLoopA", self._Diag_AmpInputOfPhaseLoopA)
        self._Diag_AmpInputOfPhaseLoopB = perseus_utils.read_diag_milivolts(self.perseus, 106, 'B')
        self.push_change_event("Diag_AmpInputOfPhaseLoopB", self._Diag_AmpInputOfPhaseLoopB)
        self._Diag_PhInputOfPhaseLoopA = perseus_utils.read_diag_milivolts(self.perseus, 107, 'A')
        self.push_change_event("Diag_PhInputOfPhaseLoopA", self._Diag_PhInputOfPhaseLoopA)
        self._Diag_PhInputOfPhaseLoopB = perseus_utils.read_diag_milivolts(self.perseus, 107, 'B')
        self.push_change_event("Diag_PhInputOfPhaseLoopB", self._Diag_PhInputOfPhaseLoopB)
        self._Diag_AmpLoopControlOutputA = perseus_utils.read_diag_milivolts(self.perseus, 108, 'A')
        self.push_change_event("Diag_AmpLoopControlOutputA", self._Diag_AmpLoopControlOutputA)
        self._Diag_AmpLoopControlOutputB = perseus_utils.read_diag_milivolts(self.perseus, 108, 'B')
        self.push_change_event("Diag_AmpLoopControlOutputB", self._Diag_AmpLoopControlOutputB)
        self._Diag_AmpLoopErrorA = perseus_utils.read_diag_milivolts(self.perseus, 109, 'A')
        self.push_change_event("Diag_AmpLoopErrorA", self._Diag_AmpLoopErrorA)
        self._Diag_AmpLoopErrorB = perseus_utils.read_diag_milivolts(self.perseus, 109, 'B')
        self.push_change_event("Diag_AmpLoopErrorB", self._Diag_AmpLoopErrorB)
        self._Diag_AmpLoopErrorAccumA = perseus_utils.read_diag_milivolts(self.perseus, 110, 'A')
        self.push_change_event("Diag_AmpLoopErrorAccumA", self._Diag_AmpLoopErrorAccumA)
        self._Diag_AmpLoopErrorAccumB = perseus_utils.read_diag_milivolts(self.perseus, 110, 'B')
        self.push_change_event("Diag_AmpLoopErrorAccumB", self._Diag_AmpLoopErrorAccumB)
        self._Diag_PhLoopControlOutputA = perseus_utils.read_diag_milivolts(self.perseus, 111, 'A')
        self.push_change_event("Diag_PhLoopControlOutputA", self._Diag_PhLoopControlOutputA)
        self._Diag_PhLoopControlOutputB = perseus_utils.read_diag_milivolts(self.perseus, 111, 'B')
        self.push_change_event("Diag_PhLoopControlOutputB", self._Diag_PhLoopControlOutputB)
        self._Diag_PhLoopErrorA = perseus_utils.read_diag_milivolts(self.perseus, 112, 'A')
        self.push_change_event("Diag_PhLoopErrorA", self._Diag_PhLoopErrorA)
        self._Diag_PhLoopErrorB = perseus_utils.read_diag_milivolts(self.perseus, 112, 'B')
        self.push_change_event("Diag_PhLoopErrorB", self._Diag_PhLoopErrorB)
        self._Diag_PhLoopErrorAccumA = perseus_utils.read_diag_milivolts(self.perseus, 113, 'A')
        self.push_change_event("Diag_PhLoopErrorAccumA", self._Diag_PhLoopErrorAccumA)
        self._Diag_PhLoopErrorAccumB = perseus_utils.read_diag_milivolts(self.perseus, 113, 'B')
        self.push_change_event("Diag_PhLoopErrorAccumB", self._Diag_PhLoopErrorAccumB)
        self._Diag_IpolarControlOutputA = perseus_utils.read_diag_milivolts(self.perseus, 114, 'A')
        self.push_change_event("Diag_IpolarControlOutputA", self._Diag_IpolarControlOutputA)
        self._Diag_IpolarControlOutputB = perseus_utils.read_diag_milivolts(self.perseus, 114, 'B')
        self.push_change_event("Diag_IpolarControlOutputB", self._Diag_IpolarControlOutputB)
        self._Diag_QpolarControlOutputA = perseus_utils.read_diag_milivolts(self.perseus, 115, 'A')
        self.push_change_event("Diag_QpolarControlOutputA", self._Diag_QpolarControlOutputA)
        self._Diag_QpolarControlOutputB = perseus_utils.read_diag_milivolts(self.perseus, 115, 'B')
        self.push_change_event("Diag_QpolarControlOutputB", self._Diag_QpolarControlOutputB)
        self._Diag_IcontrolSlowpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 116, 'A')
        self.push_change_event("Diag_IcontrolSlowpiIqA", self._Diag_IcontrolSlowpiIqA)
        self._Diag_IcontrolSlowpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 116, 'B')
        self.push_change_event("Diag_IcontrolSlowpiIqB", self._Diag_IcontrolSlowpiIqB)
        self._Diag_QcontrolSlowpiqA = perseus_utils.read_diag_milivolts(self.perseus, 117, 'A')
        self.push_change_event("Diag_QcontrolSlowpiqA", self._Diag_QcontrolSlowpiqA)
        self._Diag_QcontrolSlowpiqB = perseus_utils.read_diag_milivolts(self.perseus, 117, 'B')
        self.push_change_event("Diag_QcontrolSlowpiqB", self._Diag_QcontrolSlowpiqB)
        self._Diag_IcontrolFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 118, 'A')
        self.push_change_event("Diag_IcontrolFastpiIqA", self._Diag_IcontrolFastpiIqA)
        self._Diag_IcontrolFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 118, 'B')
        self.push_change_event("Diag_IcontrolFastpiIqB", self._Diag_IcontrolFastpiIqB)
        self._Diag_QcontrolFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 119, 'A')
        self.push_change_event("Diag_QcontrolFastpiIqA", self._Diag_QcontrolFastpiIqA)
        self._Diag_QcontrolFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 119, 'B')
        self.push_change_event("Diag_QcontrolFastpiIqB", self._Diag_QcontrolFastpiIqB)
        self._Diag_IloopinputSlowpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 120, 'A')
        self.push_change_event("Diag_IloopinputSlowpiIqA", self._Diag_IloopinputSlowpiIqA)
        self._Diag_IloopinputSlowpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 120, 'B')
        self.push_change_event("Diag_IloopinputSlowpiIqB", self._Diag_IloopinputSlowpiIqB)
        self._Diag_QloopinputSlowpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 121, 'A')
        self.push_change_event("Diag_QloopinputSlowpiIqA", self._Diag_QloopinputSlowpiIqA)
        self._Diag_QloopinputSlowpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 121, 'B')
        self.push_change_event("Diag_QloopinputSlowpiIqB", self._Diag_QloopinputSlowpiIqB)
        self._Diag_IloopinputFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 122, 'A')
        self.push_change_event("Diag_IloopinputFastpiIqA", self._Diag_IloopinputFastpiIqA)
        self._Diag_IloopinputFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 122, 'B')
        self.push_change_event("Diag_IloopinputFastpiIqB", self._Diag_IloopinputFastpiIqB)
        self._Diag_QloopinputFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 123, 'A')
        self.push_change_event("Diag_QloopinputFastpiIqA", self._Diag_QloopinputFastpiIqA)
        self._Diag_QloopinputFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 123, 'B')
        self.push_change_event("Diag_QloopinputFastpiIqB", self._Diag_QloopinputFastpiIqB)
        self._Diag_IrefloopinputFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 124, 'A')
        self.push_change_event("Diag_IrefloopinputFastpiIqA", self._Diag_IrefloopinputFastpiIqA)
        self._Diag_IrefloopinputFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 124, 'B')
        self.push_change_event("Diag_IrefloopinputFastpiIqB", self._Diag_IrefloopinputFastpiIqB)
        self._Diag_QrefloopinputFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 125, 'A')
        self.push_change_event("Diag_QrefloopinputFastpiIqA", self._Diag_QrefloopinputFastpiIqA)
        self._Diag_QrefloopinputFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 125, 'B')
        self.push_change_event("Diag_QrefloopinputFastpiIqB", self._Diag_QrefloopinputFastpiIqB)
        self._Diag_MovingPlungerAutoA = bool(perseus_utils.read_diag_direct(self.perseus, 300, 'A'))
        self.push_change_event("Diag_MovingPlungerAutoA", self._Diag_MovingPlungerAutoA)
        self._Diag_MovingPlungerAutoB = bool(perseus_utils.read_diag_direct(self.perseus, 300, 'B'))
        self.push_change_event("Diag_MovingPlungerAutoB", self._Diag_MovingPlungerAutoB)
        self._Diag_FreqUpA = bool(perseus_utils.read_diag_direct(self.perseus, 301, 'A'))
        self.push_change_event("Diag_FreqUpA", self._Diag_FreqUpA)
        self._Diag_FreqUpB = bool(perseus_utils.read_diag_direct(self.perseus, 301, 'B'))
        self.push_change_event("Diag_FreqUpB", self._Diag_FreqUpB)
        self._Diag_ManualTuningOnA = bool(perseus_utils.read_diag_direct(self.perseus, 302, 'A'))
        self.push_change_event("Diag_ManualTuningOnA", self._Diag_ManualTuningOnA)
        self._Diag_ManualTuningOnB = bool(perseus_utils.read_diag_direct(self.perseus, 302, 'B'))
        self.push_change_event("Diag_ManualTuningOnB", self._Diag_ManualTuningOnB)
        self._Diag_ManualTuningFreqUpA = bool(perseus_utils.read_diag_direct(self.perseus, 303, 'A'))
        self.push_change_event("Diag_ManualTuningFreqUpA", self._Diag_ManualTuningFreqUpA)
        self._Diag_ManualTuningFreqUpB = bool(perseus_utils.read_diag_direct(self.perseus, 303, 'B'))
        self.push_change_event("Diag_ManualTuningFreqUpB", self._Diag_ManualTuningFreqUpB)
        self._Diag_FwminA = bool(perseus_utils.read_diag_direct(self.perseus, 307, 'A'))
        self.push_change_event("Diag_FwminA", self._Diag_FwminA)
        self._Diag_FwminB = bool(perseus_utils.read_diag_direct(self.perseus, 307, 'B'))
        self.push_change_event("Diag_FwminB", self._Diag_FwminB)
        self._Diag_EpsItckDelayA = bool(perseus_utils.read_diag_direct(self.perseus, 400, 'A'))
        self.push_change_event("Diag_EpsItckDelayA", self._Diag_EpsItckDelayA)
        self._Diag_EpsItckDelayB = bool(perseus_utils.read_diag_direct(self.perseus, 400, 'B'))
        self.push_change_event("Diag_EpsItckDelayB", self._Diag_EpsItckDelayB)
        self._Diag_FimItckDelayA = bool(perseus_utils.read_diag_direct(self.perseus, 401, 'A'))
        self.push_change_event("Diag_FimItckDelayA", self._Diag_FimItckDelayA)
        self._Diag_FimItckDelayB = bool(perseus_utils.read_diag_direct(self.perseus, 401, 'B'))
        self.push_change_event("Diag_FimItckDelayB", self._Diag_FimItckDelayB)
        self._Diag_FdlTrigHwInputA = bool(perseus_utils.read_diag_direct(self.perseus, 402, 'A'))
        self.push_change_event("Diag_FdlTrigHwInputA", self._Diag_FdlTrigHwInputA)
        self._Diag_FdlTrigHwInputB = bool(perseus_utils.read_diag_direct(self.perseus, 402, 'B'))
        self.push_change_event("Diag_FdlTrigHwInputB", self._Diag_FdlTrigHwInputB)
        self._Diag_FdlTrigSwInputA = bool(perseus_utils.read_diag_direct(self.perseus, 403, 'A'))
        self.push_change_event("Diag_FdlTrigSwInputA", self._Diag_FdlTrigSwInputA)
        self._Diag_FdlTrigSwInputB = bool(perseus_utils.read_diag_direct(self.perseus, 403, 'B'))
        self.push_change_event("Diag_FdlTrigSwInputB", self._Diag_FdlTrigSwInputB)
        self._Diag_EpsItckA = bool(perseus_utils.read_diag_direct(self.perseus, 404, 'A'))
        self.push_change_event("Diag_EpsItckA", self._Diag_EpsItckA)
        self._Diag_EpsItckB = bool(perseus_utils.read_diag_direct(self.perseus, 404, 'B'))
        self.push_change_event("Diag_EpsItckB", self._Diag_EpsItckB)
        self._Diag_AmpMuxfwcircina = math.sqrt((self._Diag_IMuxFwCircInA**2) + (self._Diag_QMuxFwCircInA**2))
        self.push_change_event("Diag_AmpMuxfwcircina", self._Diag_AmpMuxfwcircina)
        self._Diag_AmpSpare1a = math.sqrt((self._Diag_Ispare1A**2) + (self._Diag_Qspare1A**2))
        self.push_change_event("Diag_AmpSpare1a", self._Diag_AmpSpare1a)
        self._Diag_AmpMuxfwcircinb = math.sqrt((self._Diag_IMuxFwCircInB**2) + (self._Diag_QMuxFwCircInB**2))
        self.push_change_event("Diag_AmpMuxfwcircinb", self._Diag_AmpMuxfwcircinb)
        self._Diag_AmpSpare2a = math.sqrt((self._Diag_Ispare2A**2) + (self._Diag_Qspare2A**2))
        self.push_change_event("Diag_AmpSpare2a", self._Diag_AmpSpare2a)
        self._Diag_AmpSpare2b = math.sqrt((self._Diag_Ispare2B**2) + (self._Diag_Qspare2B**2))
        self.push_change_event("Diag_AmpSpare2b", self._Diag_AmpSpare2b)
        self._Diag_AmpErrora = math.sqrt((self._Diag_IerrorA**2) + (self._Diag_QerrorA**2))
        self.push_change_event("Diag_AmpErrora", self._Diag_AmpErrora)
        self._Diag_AmpErrorb = math.sqrt((self._Diag_IerrorB**2) + (self._Diag_QerrorB**2))
        self.push_change_event("Diag_AmpErrorb", self._Diag_AmpErrorb)
        self._Diag_AmpSpare1b = math.sqrt((self._Diag_Ispare1B**2) + (self._Diag_Qspare1B**2))
        self.push_change_event("Diag_AmpSpare1b", self._Diag_AmpSpare1b)
        self._Diag_AmpErroraccumb = math.sqrt((self._Diag_IerroraccumB**2) + (self._Diag_QerroraccumB**2))
        self.push_change_event("Diag_AmpErroraccumb", self._Diag_AmpErroraccumb)
        self._Diag_AmpErroraccuma = math.sqrt((self._Diag_IerroraccumA**2) + (self._Diag_QerroraccumA**2))
        self.push_change_event("Diag_AmpErroraccuma", self._Diag_AmpErroraccuma)
        self._Diag_AmpControlfastpiiqb = math.sqrt((self._Diag_IcontrolFastpiIqB**2) + (self._Diag_QcontrolFastpiIqB**2))
        self.push_change_event("Diag_AmpControlfastpiiqb", self._Diag_AmpControlfastpiiqb)
        self._Diag_AmpControlfastpiiqa = math.sqrt((self._Diag_IcontrolFastpiIqA**2) + (self._Diag_QcontrolFastpiIqA**2))
        self.push_change_event("Diag_AmpControlfastpiiqa", self._Diag_AmpControlfastpiiqa)
        self._Diag_AmpControla = math.sqrt((self._Diag_IcontrolA**2) + (self._Diag_QcontrolA**2))
        self.push_change_event("Diag_AmpControla", self._Diag_AmpControla)
        self._Diag_AmpPolarforamplitudeloopa = math.sqrt((self._Diag_IpolarForAmplitudeLoopA**2) + (self._Diag_QpolarForAmplitudeLoopA**2))
        self.push_change_event("Diag_AmpPolarforamplitudeloopa", self._Diag_AmpPolarforamplitudeloopa)
        self._Diag_AmpPolarforamplitudeloopb = math.sqrt((self._Diag_IpolarForAmplitudeLoopB**2) + (self._Diag_QpolarForAmplitudeLoopB**2))
        self.push_change_event("Diag_AmpPolarforamplitudeloopb", self._Diag_AmpPolarforamplitudeloopb)
        self._Diag_AmpControlb = math.sqrt((self._Diag_IcontrolB**2) + (self._Diag_QcontrolB**2))
        self.push_change_event("Diag_AmpControlb", self._Diag_AmpControlb)
        self._Diag_AmpMuxfwtet2b = math.sqrt((self._Diag_IMuxFwTet2B**2) + (self._Diag_QMuxFwTet2B**2))
        self.push_change_event("Diag_AmpMuxfwtet2b", self._Diag_AmpMuxfwtet2b)
        self._Diag_AmpLoopinputfastpiiqb = math.sqrt((self._Diag_IloopinputFastpiIqB**2) + (self._Diag_QloopinputFastpiIqB**2))
        self.push_change_event("Diag_AmpLoopinputfastpiiqb", self._Diag_AmpLoopinputfastpiiqb)
        self._Diag_AmpLoopinputfastpiiqa = math.sqrt((self._Diag_IloopinputFastpiIqA**2) + (self._Diag_QloopinputFastpiIqA**2))
        self.push_change_event("Diag_AmpLoopinputfastpiiqa", self._Diag_AmpLoopinputfastpiiqa)
        self._Diag_AmpRefa = math.sqrt((self._Diag_IrefA**2) + (self._Diag_QrefA**2))
        self.push_change_event("Diag_AmpRefa", self._Diag_AmpRefa)
        self._Diag_AmpMuxfwcava = math.sqrt((self._Diag_IMuxFwCavA**2) + (self._Diag_QMuxFwCavA**2))
        self.push_change_event("Diag_AmpMuxfwcava", self._Diag_AmpMuxfwcava)
        self._Diag_AmpMuxfwcavb = math.sqrt((self._Diag_IMuxFwCavB**2) + (self._Diag_QMuxFwCavB**2))
        self.push_change_event("Diag_AmpMuxfwcavb", self._Diag_AmpMuxfwcavb)
        self._Diag_AmpRefb = math.sqrt((self._Diag_IrefB**2) + (self._Diag_QrefB**2))
        self.push_change_event("Diag_AmpRefb", self._Diag_AmpRefb)
        self._Diag_AmpControl2a = math.sqrt((self._Diag_Icontrol2A**2) + (self._Diag_Qcontrol2A**2))
        self.push_change_event("Diag_AmpControl2a", self._Diag_AmpControl2a)
        self._Diag_AmpControl2b = math.sqrt((self._Diag_Icontrol2B**2) + (self._Diag_Qcontrol2B**2))
        self.push_change_event("Diag_AmpControl2b", self._Diag_AmpControl2b)
        self._Diag_AmpFwtet1loopsb = math.sqrt((self._Diag_IFwTet1LoopsB**2) + (self._Diag_QFwTet1LoopsB**2))
        self.push_change_event("Diag_AmpFwtet1loopsb", self._Diag_AmpFwtet1loopsb)
        self._Diag_AmpFwtet1loopsa = math.sqrt((self._Diag_IFwTet1LoopsA**2) + (self._Diag_QFwTet1LoopsA**2))
        self.push_change_event("Diag_AmpFwtet1loopsa", self._Diag_AmpFwtet1loopsa)
        self._Diag_AmpPolarforphaseloopb = math.sqrt((self._Diag_IpolarForPhaseLoopB**2) + (self._Diag_QpolarForPhaseLoopB**2))
        self.push_change_event("Diag_AmpPolarforphaseloopb", self._Diag_AmpPolarforphaseloopb)
        self._Diag_AmpPolarforphaseloopa = math.sqrt((self._Diag_IpolarForPhaseLoopA**2) + (self._Diag_QpolarForPhaseLoopA**2))
        self.push_change_event("Diag_AmpPolarforphaseloopa", self._Diag_AmpPolarforphaseloopa)
        self._Diag_AmpPolarcontroloutputb = math.sqrt((self._Diag_IpolarControlOutputB**2) + (self._Diag_QpolarControlOutputB**2))
        self.push_change_event("Diag_AmpPolarcontroloutputb", self._Diag_AmpPolarcontroloutputb)
        self._Diag_AmpPolarcontroloutputa = math.sqrt((self._Diag_IpolarControlOutputA**2) + (self._Diag_QpolarControlOutputA**2))
        self.push_change_event("Diag_AmpPolarcontroloutputa", self._Diag_AmpPolarcontroloutputa)
        self._Diag_AmpFwtet2loopsa = math.sqrt((self._Diag_IFwTet2LoopsA**2) + (self._Diag_QFwTet2LoopsA**2))
        self.push_change_event("Diag_AmpFwtet2loopsa", self._Diag_AmpFwtet2loopsa)
        self._Diag_AmpCavloopsa = math.sqrt((self._Diag_IcavLoopsA**2) + (self._Diag_QcavLoopsA**2))
        self.push_change_event("Diag_AmpCavloopsa", self._Diag_AmpCavloopsa)
        self._Diag_AmpCavloopsb = math.sqrt((self._Diag_IcavLoopsB**2) + (self._Diag_QcavLoopsB**2))
        self.push_change_event("Diag_AmpCavloopsb", self._Diag_AmpCavloopsb)
        self._Diag_AmpFwtet2loopsb = math.sqrt((self._Diag_IFwTet2LoopsB**2) + (self._Diag_QFwTet2LoopsB**2))
        self.push_change_event("Diag_AmpFwtet2loopsb", self._Diag_AmpFwtet2loopsb)
        self._Diag_AmpLoopinputslowpiiqa = math.sqrt((self._Diag_IloopinputSlowpiIqA**2) + (self._Diag_QloopinputSlowpiIqA**2))
        self.push_change_event("Diag_AmpLoopinputslowpiiqa", self._Diag_AmpLoopinputslowpiiqa)
        self._Diag_AmpLoopinputslowpiiqb = math.sqrt((self._Diag_IloopinputSlowpiIqB**2) + (self._Diag_QloopinputSlowpiIqB**2))
        self.push_change_event("Diag_AmpLoopinputslowpiiqb", self._Diag_AmpLoopinputslowpiiqb)
        self._Diag_AmpRefloopinputfastpiiqb = math.sqrt((self._Diag_IrefloopinputFastpiIqB**2) + (self._Diag_QrefloopinputFastpiIqB**2))
        self.push_change_event("Diag_AmpRefloopinputfastpiiqb", self._Diag_AmpRefloopinputfastpiiqb)
        self._Diag_AmpRefloopinputfastpiiqa = math.sqrt((self._Diag_IrefloopinputFastpiIqA**2) + (self._Diag_QrefloopinputFastpiIqA**2))
        self.push_change_event("Diag_AmpRefloopinputfastpiiqa", self._Diag_AmpRefloopinputfastpiiqa)
        self._Diag_AmpControl1a = math.sqrt((self._Diag_Icontrol1A**2) + (self._Diag_Qcontrol1A**2))
        self.push_change_event("Diag_AmpControl1a", self._Diag_AmpControl1a)
        self._Diag_AmpControl1b = math.sqrt((self._Diag_Icontrol1B**2) + (self._Diag_Qcontrol1B**2))
        self.push_change_event("Diag_AmpControl1b", self._Diag_AmpControl1b)
        self._Diag_AmpMuxfwtet2a = math.sqrt((self._Diag_IMuxFwTet2A**2) + (self._Diag_QMuxFwTet2A**2))
        self.push_change_event("Diag_AmpMuxfwtet2a", self._Diag_AmpMuxfwtet2a)
        self._Diag_AmpMuxcavb = math.sqrt((self._Diag_IMuxCavB**2) + (self._Diag_QMuxCavB**2))
        self.push_change_event("Diag_AmpMuxcavb", self._Diag_AmpMuxcavb)
        self._Diag_AmpMuxcava = math.sqrt((self._Diag_IMuxCavA**2) + (self._Diag_QMuxCavA**2))
        self.push_change_event("Diag_AmpMuxcava", self._Diag_AmpMuxcava)
        self._Diag_AmpMuxfwtet1b = math.sqrt((self._Diag_IMuxFwTet1B**2) + (self._Diag_QMuxFwTet1B**2))
        self.push_change_event("Diag_AmpMuxfwtet1b", self._Diag_AmpMuxfwtet1b)
        self._Diag_AmpControlfastpib = math.sqrt((self._Diag_IcontrolFastpiB**2) + (self._Diag_QcontrolFastpiB**2))
        self.push_change_event("Diag_AmpControlfastpib", self._Diag_AmpControlfastpib)
        self._Diag_AmpFwcircinloopsa = math.sqrt((self._Diag_IFwCircInLoopsA**2) + (self._Diag_QFwCircInLoopsA**2))
        self.push_change_event("Diag_AmpFwcircinloopsa", self._Diag_AmpFwcircinloopsa)
        self._Diag_AmpFwcircinloopsb = math.sqrt((self._Diag_IFwCircInLoopsB**2) + (self._Diag_QFwCircInLoopsB**2))
        self.push_change_event("Diag_AmpFwcircinloopsb", self._Diag_AmpFwcircinloopsb)
        self._Diag_AmpControlfastpia = math.sqrt((self._Diag_IcontrolFastpiA**2) + (self._Diag_QcontrolFastpiA**2))
        self.push_change_event("Diag_AmpControlfastpia", self._Diag_AmpControlfastpia)
        self._Diag_AmpFwcavloopsa = math.sqrt((self._Diag_IFwCavLoopsA**2) + (self._Diag_QFwCavLoopsA**2))
        self.push_change_event("Diag_AmpFwcavloopsa", self._Diag_AmpFwcavloopsa)
        self._Diag_AmpMuxfwtet1a = math.sqrt((self._Diag_IMuxFwTet1A**2) + (self._Diag_QMuxFwTet1A**2))
        self.push_change_event("Diag_AmpMuxfwtet1a", self._Diag_AmpMuxfwtet1a)
        self._Diag_AmpFwcavloopsb = math.sqrt((self._Diag_IFwCavLoopsB**2) + (self._Diag_QFwCavLoopsB**2))
        self.push_change_event("Diag_AmpFwcavloopsb", self._Diag_AmpFwcavloopsb)
        self._Diag_AmpMob = math.sqrt((self._Diag_ImoB**2) + (self._Diag_QmoB**2))
        self.push_change_event("Diag_AmpMob", self._Diag_AmpMob)
        self._Diag_AmpMoa = math.sqrt((self._Diag_ImoA**2) + (self._Diag_QmoA**2))
        self.push_change_event("Diag_AmpMoa", self._Diag_AmpMoa)
        self._Diag_AmpControlslowpia = math.sqrt((self._Diag_IcontrolSlowpiA**2) + (self._Diag_QcontrolSlowpiA**2))
        self.push_change_event("Diag_AmpControlslowpia", self._Diag_AmpControlslowpia)
        self._Diag_AmpControlslowpib = math.sqrt((self._Diag_IcontrolSlowpiB**2) + (self._Diag_QcontrolSlowpiB**2))
        self.push_change_event("Diag_AmpControlslowpib", self._Diag_AmpControlslowpib)
        self._Diag_PhMuxfwcircina = math.degrees(math.atan2(self._Diag_QMuxFwCircInA, self._Diag_IMuxFwCircInA))
        self.push_change_event("Diag_PhMuxfwcircina", self._Diag_PhMuxfwcircina)
        self._Diag_PhSpare1a = math.degrees(math.atan2(self._Diag_Qspare1A, self._Diag_Ispare1A))
        self.push_change_event("Diag_PhSpare1a", self._Diag_PhSpare1a)
        self._Diag_PhMuxfwcircinb = math.degrees(math.atan2(self._Diag_QMuxFwCircInB, self._Diag_IMuxFwCircInB))
        self.push_change_event("Diag_PhMuxfwcircinb", self._Diag_PhMuxfwcircinb)
        self._Diag_PhSpare2a = math.degrees(math.atan2(self._Diag_Qspare2A, self._Diag_Ispare2A))
        self.push_change_event("Diag_PhSpare2a", self._Diag_PhSpare2a)
        self._Diag_PhSpare2b = math.degrees(math.atan2(self._Diag_Qspare2B, self._Diag_Ispare2B))
        self.push_change_event("Diag_PhSpare2b", self._Diag_PhSpare2b)
        self._Diag_PhErrora = math.degrees(math.atan2(self._Diag_QerrorA, self._Diag_IerrorA))
        self.push_change_event("Diag_PhErrora", self._Diag_PhErrora)
        self._Diag_PhErrorb = math.degrees(math.atan2(self._Diag_QerrorB, self._Diag_IerrorB))
        self.push_change_event("Diag_PhErrorb", self._Diag_PhErrorb)
        self._Diag_PhSpare1b = math.degrees(math.atan2(self._Diag_Qspare1B, self._Diag_Ispare1B))
        self.push_change_event("Diag_PhSpare1b", self._Diag_PhSpare1b)
        self._Diag_PhErroraccumb = math.degrees(math.atan2(self._Diag_QerroraccumB, self._Diag_IerroraccumB))
        self.push_change_event("Diag_PhErroraccumb", self._Diag_PhErroraccumb)
        self._Diag_PhErroraccuma = math.degrees(math.atan2(self._Diag_QerroraccumA, self._Diag_IerroraccumA))
        self.push_change_event("Diag_PhErroraccuma", self._Diag_PhErroraccuma)
        self._Diag_PhControlfastpiiqb = math.degrees(math.atan2(self._Diag_QcontrolFastpiIqB, self._Diag_IcontrolFastpiIqB))
        self.push_change_event("Diag_PhControlfastpiiqb", self._Diag_PhControlfastpiiqb)
        self._Diag_PhControlfastpiiqa = math.degrees(math.atan2(self._Diag_QcontrolFastpiIqA, self._Diag_IcontrolFastpiIqA))
        self.push_change_event("Diag_PhControlfastpiiqa", self._Diag_PhControlfastpiiqa)
        self._Diag_PhControla = math.degrees(math.atan2(self._Diag_QcontrolA, self._Diag_IcontrolA))
        self.push_change_event("Diag_PhControla", self._Diag_PhControla)
        self._Diag_PhPolarforamplitudeloopa = math.degrees(math.atan2(self._Diag_QpolarForAmplitudeLoopA, self._Diag_IpolarForAmplitudeLoopA))
        self.push_change_event("Diag_PhPolarforamplitudeloopa", self._Diag_PhPolarforamplitudeloopa)
        self._Diag_PhPolarforamplitudeloopb = math.degrees(math.atan2(self._Diag_QpolarForAmplitudeLoopB, self._Diag_IpolarForAmplitudeLoopB))
        self.push_change_event("Diag_PhPolarforamplitudeloopb", self._Diag_PhPolarforamplitudeloopb)
        self._Diag_PhControlb = math.degrees(math.atan2(self._Diag_QcontrolB, self._Diag_IcontrolB))
        self.push_change_event("Diag_PhControlb", self._Diag_PhControlb)
        self._Diag_PhMuxfwtet2b = math.degrees(math.atan2(self._Diag_QMuxFwTet2B, self._Diag_IMuxFwTet2B))
        self.push_change_event("Diag_PhMuxfwtet2b", self._Diag_PhMuxfwtet2b)
        self._Diag_PhLoopinputfastpiiqb = math.degrees(math.atan2(self._Diag_QloopinputFastpiIqB, self._Diag_IloopinputFastpiIqB))
        self.push_change_event("Diag_PhLoopinputfastpiiqb", self._Diag_PhLoopinputfastpiiqb)
        self._Diag_PhLoopinputfastpiiqa = math.degrees(math.atan2(self._Diag_QloopinputFastpiIqA, self._Diag_IloopinputFastpiIqA))
        self.push_change_event("Diag_PhLoopinputfastpiiqa", self._Diag_PhLoopinputfastpiiqa)
        self._Diag_PhRefa = math.degrees(math.atan2(self._Diag_QrefA, self._Diag_IrefA))
        self.push_change_event("Diag_PhRefa", self._Diag_PhRefa)
        self._Diag_PhMuxfwcava = math.degrees(math.atan2(self._Diag_QMuxFwCavA, self._Diag_IMuxFwCavA))
        self.push_change_event("Diag_PhMuxfwcava", self._Diag_PhMuxfwcava)
        self._Diag_PhMuxfwcavb = math.degrees(math.atan2(self._Diag_QMuxFwCavB, self._Diag_IMuxFwCavB))
        self.push_change_event("Diag_PhMuxfwcavb", self._Diag_PhMuxfwcavb)
        self._Diag_PhRefb = math.degrees(math.atan2(self._Diag_QrefB, self._Diag_IrefB))
        self.push_change_event("Diag_PhRefb", self._Diag_PhRefb)
        self._Diag_PhControl2a = math.degrees(math.atan2(self._Diag_Qcontrol2A, self._Diag_Icontrol2A))
        self.push_change_event("Diag_PhControl2a", self._Diag_PhControl2a)
        self._Diag_PhControl2b = math.degrees(math.atan2(self._Diag_Qcontrol2B, self._Diag_Icontrol2B))
        self.push_change_event("Diag_PhControl2b", self._Diag_PhControl2b)
        self._Diag_PhFwtet1loopsb = math.degrees(math.atan2(self._Diag_QFwTet1LoopsB, self._Diag_IFwTet1LoopsB))
        self.push_change_event("Diag_PhFwtet1loopsb", self._Diag_PhFwtet1loopsb)
        self._Diag_PhFwtet1loopsa = math.degrees(math.atan2(self._Diag_QFwTet1LoopsA, self._Diag_IFwTet1LoopsA))
        self.push_change_event("Diag_PhFwtet1loopsa", self._Diag_PhFwtet1loopsa)
        self._Diag_PhPolarforphaseloopb = math.degrees(math.atan2(self._Diag_QpolarForPhaseLoopB, self._Diag_IpolarForPhaseLoopB))
        self.push_change_event("Diag_PhPolarforphaseloopb", self._Diag_PhPolarforphaseloopb)
        self._Diag_PhPolarforphaseloopa = math.degrees(math.atan2(self._Diag_QpolarForPhaseLoopA, self._Diag_IpolarForPhaseLoopA))
        self.push_change_event("Diag_PhPolarforphaseloopa", self._Diag_PhPolarforphaseloopa)
        self._Diag_PhPolarcontroloutputb = math.degrees(math.atan2(self._Diag_QpolarControlOutputB, self._Diag_IpolarControlOutputB))
        self.push_change_event("Diag_PhPolarcontroloutputb", self._Diag_PhPolarcontroloutputb)
        self._Diag_PhPolarcontroloutputa = math.degrees(math.atan2(self._Diag_QpolarControlOutputA, self._Diag_IpolarControlOutputA))
        self.push_change_event("Diag_PhPolarcontroloutputa", self._Diag_PhPolarcontroloutputa)
        self._Diag_PhFwtet2loopsa = math.degrees(math.atan2(self._Diag_QFwTet2LoopsA, self._Diag_IFwTet2LoopsA))
        self.push_change_event("Diag_PhFwtet2loopsa", self._Diag_PhFwtet2loopsa)
        self._Diag_PhCavloopsa = math.degrees(math.atan2(self._Diag_QcavLoopsA, self._Diag_IcavLoopsA))
        self.push_change_event("Diag_PhCavloopsa", self._Diag_PhCavloopsa)
        self._Diag_PhCavloopsb = math.degrees(math.atan2(self._Diag_QcavLoopsB, self._Diag_IcavLoopsB))
        self.push_change_event("Diag_PhCavloopsb", self._Diag_PhCavloopsb)
        self._Diag_PhFwtet2loopsb = math.degrees(math.atan2(self._Diag_QFwTet2LoopsB, self._Diag_IFwTet2LoopsB))
        self.push_change_event("Diag_PhFwtet2loopsb", self._Diag_PhFwtet2loopsb)
        self._Diag_PhLoopinputslowpiiqa = math.degrees(math.atan2(self._Diag_QloopinputSlowpiIqA, self._Diag_IloopinputSlowpiIqA))
        self.push_change_event("Diag_PhLoopinputslowpiiqa", self._Diag_PhLoopinputslowpiiqa)
        self._Diag_PhLoopinputslowpiiqb = math.degrees(math.atan2(self._Diag_QloopinputSlowpiIqB, self._Diag_IloopinputSlowpiIqB))
        self.push_change_event("Diag_PhLoopinputslowpiiqb", self._Diag_PhLoopinputslowpiiqb)
        self._Diag_PhRefloopinputfastpiiqb = math.degrees(math.atan2(self._Diag_QrefloopinputFastpiIqB, self._Diag_IrefloopinputFastpiIqB))
        self.push_change_event("Diag_PhRefloopinputfastpiiqb", self._Diag_PhRefloopinputfastpiiqb)
        self._Diag_PhRefloopinputfastpiiqa = math.degrees(math.atan2(self._Diag_QrefloopinputFastpiIqA, self._Diag_IrefloopinputFastpiIqA))
        self.push_change_event("Diag_PhRefloopinputfastpiiqa", self._Diag_PhRefloopinputfastpiiqa)
        self._Diag_PhControl1a = math.degrees(math.atan2(self._Diag_Qcontrol1A, self._Diag_Icontrol1A))
        self.push_change_event("Diag_PhControl1a", self._Diag_PhControl1a)
        self._Diag_PhControl1b = math.degrees(math.atan2(self._Diag_Qcontrol1B, self._Diag_Icontrol1B))
        self.push_change_event("Diag_PhControl1b", self._Diag_PhControl1b)
        self._Diag_PhMuxfwtet2a = math.degrees(math.atan2(self._Diag_QMuxFwTet2A, self._Diag_IMuxFwTet2A))
        self.push_change_event("Diag_PhMuxfwtet2a", self._Diag_PhMuxfwtet2a)
        self._Diag_PhMuxcavb = math.degrees(math.atan2(self._Diag_QMuxCavB, self._Diag_IMuxCavB))
        self.push_change_event("Diag_PhMuxcavb", self._Diag_PhMuxcavb)
        self._Diag_PhMuxcava = math.degrees(math.atan2(self._Diag_QMuxCavA, self._Diag_IMuxCavA))
        self.push_change_event("Diag_PhMuxcava", self._Diag_PhMuxcava)
        self._Diag_PhMuxfwtet1b = math.degrees(math.atan2(self._Diag_QMuxFwTet1B, self._Diag_IMuxFwTet1B))
        self.push_change_event("Diag_PhMuxfwtet1b", self._Diag_PhMuxfwtet1b)
        self._Diag_PhControlfastpib = math.degrees(math.atan2(self._Diag_QcontrolFastpiB, self._Diag_IcontrolFastpiB))
        self.push_change_event("Diag_PhControlfastpib", self._Diag_PhControlfastpib)
        self._Diag_PhFwcircinloopsa = math.degrees(math.atan2(self._Diag_QFwCircInLoopsA, self._Diag_IFwCircInLoopsA))
        self.push_change_event("Diag_PhFwcircinloopsa", self._Diag_PhFwcircinloopsa)
        self._Diag_PhFwcircinloopsb = math.degrees(math.atan2(self._Diag_QFwCircInLoopsB, self._Diag_IFwCircInLoopsB))
        self.push_change_event("Diag_PhFwcircinloopsb", self._Diag_PhFwcircinloopsb)
        self._Diag_PhControlfastpia = math.degrees(math.atan2(self._Diag_QcontrolFastpiA, self._Diag_IcontrolFastpiA))
        self.push_change_event("Diag_PhControlfastpia", self._Diag_PhControlfastpia)
        self._Diag_PhFwcavloopsa = math.degrees(math.atan2(self._Diag_QFwCavLoopsA, self._Diag_IFwCavLoopsA))
        self.push_change_event("Diag_PhFwcavloopsa", self._Diag_PhFwcavloopsa)
        self._Diag_PhMuxfwtet1a = math.degrees(math.atan2(self._Diag_QMuxFwTet1A, self._Diag_IMuxFwTet1A))
        self.push_change_event("Diag_PhMuxfwtet1a", self._Diag_PhMuxfwtet1a)
        self._Diag_PhFwcavloopsb = math.degrees(math.atan2(self._Diag_QFwCavLoopsB, self._Diag_IFwCavLoopsB))
        self.push_change_event("Diag_PhFwcavloopsb", self._Diag_PhFwcavloopsb)
        self._Diag_PhMob = math.degrees(math.atan2(self._Diag_QmoB, self._Diag_ImoB))
        self.push_change_event("Diag_PhMob", self._Diag_PhMob)
        self._Diag_PhMoa = math.degrees(math.atan2(self._Diag_QmoA, self._Diag_ImoA))
        self.push_change_event("Diag_PhMoa", self._Diag_PhMoa)
        self._Diag_PhControlslowpia = math.degrees(math.atan2(self._Diag_QcontrolSlowpiA, self._Diag_IcontrolSlowpiA))
        self.push_change_event("Diag_PhControlslowpia", self._Diag_PhControlslowpia)
        self._Diag_PhControlslowpib = math.degrees(math.atan2(self._Diag_QcontrolSlowpiB, self._Diag_IcontrolSlowpiB))
        self.push_change_event("Diag_PhControlslowpib", self._Diag_PhControlslowpib)

    @command
    def read_attrs(self):

        data = self.get_KpA()
        self.push_change_event("KpA", data)
        data = self.get_KpB()
        self.push_change_event("KpB", data)
        data = self.get_KiA()
        self.push_change_event("KiA", data)
        data = self.get_KiB()
        self.push_change_event("KiB", data)
        data = self.get_PhaseShiftCavA()
        self.push_change_event("PhaseShiftCavA", data)
        data = self.get_PhaseShiftCavB()
        self.push_change_event("PhaseShiftCavB", data)
        data = self.get_PhaseShiftFwcavA()
        self.push_change_event("PhaseShiftFwcavA", data)
        data = self.get_PhaseShiftFwcavB()
        self.push_change_event("PhaseShiftFwcavB", data)
        data = self.get_PhaseShiftFwtet1A()
        self.push_change_event("PhaseShiftFwtet1A", data)
        data = self.get_PhaseShiftFwtet1B()
        self.push_change_event("PhaseShiftFwtet1B", data)
        data = self.get_PhaseShiftFwtet2A()
        self.push_change_event("PhaseShiftFwtet2A", data)
        data = self.get_PhaseShiftFwtet2B()
        self.push_change_event("PhaseShiftFwtet2B", data)
        data = self.get_PilimitA()
        self.push_change_event("PilimitA", data)
        data = self.get_PilimitB()
        self.push_change_event("PilimitB", data)
        data = self.get_SamplesToAverageA()
        self.push_change_event("SamplesToAverageA", data)
        data = self.get_SamplesToAverageB()
        self.push_change_event("SamplesToAverageB", data)
        data = self.get_FilterStagesA()
        self.push_change_event("FilterStagesA", data)
        data = self.get_FilterStagesB()
        self.push_change_event("FilterStagesB", data)
        data = self.get_PhaseShiftFwcircinA()
        self.push_change_event("PhaseShiftFwcircinA", data)
        data = self.get_PhaseShiftFwcircinB()
        self.push_change_event("PhaseShiftFwcircinB", data)
        data = self.get_PhaseShiftControlSignalTet1A()
        self.push_change_event("PhaseShiftControlSignalTet1A", data)
        data = self.get_PhaseShiftControlSignalTet1B()
        self.push_change_event("PhaseShiftControlSignalTet1B", data)
        data = self.get_PhaseShiftControlSignalTet2A()
        self.push_change_event("PhaseShiftControlSignalTet2A", data)
        data = self.get_PhaseShiftControlSignalTet2B()
        self.push_change_event("PhaseShiftControlSignalTet2B", data)
        data = self.get_GainTetrode1A()
        self.push_change_event("GainTetrode1A", data)
        data = self.get_GainTetrode1B()
        self.push_change_event("GainTetrode1B", data)
        data = self.get_GainTetrode2A()
        self.push_change_event("GainTetrode2A", data)
        data = self.get_GainTetrode2B()
        self.push_change_event("GainTetrode2B", data)
        data = bool(self.get_AutomaticStartupEnableA())
        self.push_change_event("AutomaticStartupEnableA", data)
        data = bool(self.get_AutomaticStartupEnableB())
        self.push_change_event("AutomaticStartupEnableB", data)
        data = self.get_CommandStartA()
        self.push_change_event("CommandStartA", data)
        data = self.get_CommandStartB()
        self.push_change_event("CommandStartB", data)
        data = self.get_AmprefinA()
        self.push_change_event("AmprefinA", data)
        data = self.get_AmprefinB()
        self.push_change_event("AmprefinB", data)
        data = self.get_PhrefinA()
        self.push_change_event("PhrefinA", data)
        data = self.get_PhrefinB()
        self.push_change_event("PhrefinB", data)
        data = self.get_AmprefminA()
        self.push_change_event("AmprefminA", data)
        data = self.get_AmprefminB()
        self.push_change_event("AmprefminB", data)
        data = self.get_PhrefminA()
        self.push_change_event("PhrefminA", data)
        data = self.get_PhrefminB()
        self.push_change_event("PhrefminB", data)
        data = self.get_PhaseIncreaseRateA()
        self.push_change_event("PhaseIncreaseRateA", data)
        data = self.get_PhaseIncreaseRateB()
        self.push_change_event("PhaseIncreaseRateB", data)
        data = self.get_VoltageIncreaseRateA()
        self.push_change_event("VoltageIncreaseRateA", data)
        data = self.get_VoltageIncreaseRateB()
        self.push_change_event("VoltageIncreaseRateB", data)
        data = self.get_GainOlA()
        self.push_change_event("GainOlA", data)
        data = self.get_GainOlB()
        self.push_change_event("GainOlB", data)
        data = bool(self.get_SpareGpioOutput01A())
        self.push_change_event("SpareGpioOutput01A", data)
        data = bool(self.get_SpareGpioOutput01B())
        self.push_change_event("SpareGpioOutput01B", data)
        data = bool(self.get_SpareGpioOutput02A())
        self.push_change_event("SpareGpioOutput02A", data)
        data = bool(self.get_SpareGpioOutput02B())
        self.push_change_event("SpareGpioOutput02B", data)
        data = bool(self.get_SpareGpioOutput03A())
        self.push_change_event("SpareGpioOutput03A", data)
        data = bool(self.get_SpareGpioOutput03B())
        self.push_change_event("SpareGpioOutput03B", data)
        data = bool(self.get_SpareGpioOutput04A())
        self.push_change_event("SpareGpioOutput04A", data)
        data = bool(self.get_SpareGpioOutput04B())
        self.push_change_event("SpareGpioOutput04B", data)
        data = bool(self.get_FdlSwTriggerA())
        self.push_change_event("FdlSwTriggerA", data)
        data = bool(self.get_FdlSwTriggerB())
        self.push_change_event("FdlSwTriggerB", data)
        data = bool(self.get_SlowIqLoopEnableA())
        self.push_change_event("SlowIqLoopEnableA", data)
        data = bool(self.get_SlowIqLoopEnableB())
        self.push_change_event("SlowIqLoopEnableB", data)
        data = bool(self.get_AdcsPhaseshiftEnableA())
        self.push_change_event("AdcsPhaseshiftEnableA", data)
        data = bool(self.get_AdcsPhaseshiftEnableB())
        self.push_change_event("AdcsPhaseshiftEnableB", data)
        data = bool(self.get_DacsPhaseShiftEnableA())
        self.push_change_event("DacsPhaseShiftEnableA", data)
        data = bool(self.get_DacsPhaseShiftEnableB())
        self.push_change_event("DacsPhaseShiftEnableB", data)
        data = bool(self.get_SquarerefEnableA())
        self.push_change_event("SquarerefEnableA", data)
        data = bool(self.get_SquarerefEnableB())
        self.push_change_event("SquarerefEnableB", data)
        data = self.get_FreqsquareA()
        self.push_change_event("FreqsquareA", data)
        data = self.get_FreqsquareB()
        self.push_change_event("FreqsquareB", data)
        data = bool(self.get_LookRefA())
        self.push_change_event("LookRefA", data)
        data = bool(self.get_LookRefB())
        self.push_change_event("LookRefB", data)
        data = self.get_QuadrantSelectionA()
        self.push_change_event("QuadrantSelectionA", data)
        data = self.get_QuadrantSelectionB()
        self.push_change_event("QuadrantSelectionB", data)
        data = self.get_SlowIqLoopInputSelectionA()
        self.push_change_event("SlowIqLoopInputSelectionA", data)
        data = self.get_SlowIqLoopInputSelectionB()
        self.push_change_event("SlowIqLoopInputSelectionB", data)
        data = self.get_FastIqLoopInputSelectionA()
        self.push_change_event("FastIqLoopInputSelectionA", data)
        data = self.get_FastIqLoopInputSelectionB()
        self.push_change_event("FastIqLoopInputSelectionB", data)
        data = self.get_AmplitudeLoopInputSelectionA()
        self.push_change_event("AmplitudeLoopInputSelectionA", data)
        data = self.get_AmplitudeLoopInputSelectionB()
        self.push_change_event("AmplitudeLoopInputSelectionB", data)
        data = self.get_PhaseLoopInputSelectionA()
        self.push_change_event("PhaseLoopInputSelectionA", data)
        data = self.get_PhaseLoopInputSelectionB()
        self.push_change_event("PhaseLoopInputSelectionB", data)
        data = bool(self.get_PolarLoopsEnableA())
        self.push_change_event("PolarLoopsEnableA", data)
        data = bool(self.get_PolarLoopsEnableB())
        self.push_change_event("PolarLoopsEnableB", data)
        data = bool(self.get_FastIqLoopEnableA())
        self.push_change_event("FastIqLoopEnableA", data)
        data = bool(self.get_FastIqLoopEnableB())
        self.push_change_event("FastIqLoopEnableB", data)
        data = bool(self.get_AmplitudeLoopEnableA())
        self.push_change_event("AmplitudeLoopEnableA", data)
        data = bool(self.get_AmplitudeLoopEnableB())
        self.push_change_event("AmplitudeLoopEnableB", data)
        data = bool(self.get_PhaseLoopEnableA())
        self.push_change_event("PhaseLoopEnableA", data)
        data = bool(self.get_PhaseLoopEnableB())
        self.push_change_event("PhaseLoopEnableB", data)
        data = self.get_KpFastIqLoopA()
        self.push_change_event("KpFastIqLoopA", data)
        data = self.get_KpFastIqLoopB()
        self.push_change_event("KpFastIqLoopB", data)
        data = self.get_KiFastIqLoopA()
        self.push_change_event("KiFastIqLoopA", data)
        data = self.get_KiFastIqLoopB()
        self.push_change_event("KiFastIqLoopB", data)
        data = self.get_KpAmpLoopA()
        self.push_change_event("KpAmpLoopA", data)
        data = self.get_KpAmpLoopB()
        self.push_change_event("KpAmpLoopB", data)
        data = self.get_KiAmpLoopA()
        self.push_change_event("KiAmpLoopA", data)
        data = self.get_KiAmpLoopB()
        self.push_change_event("KiAmpLoopB", data)
        data = self.get_KpPhaseLoopA()
        self.push_change_event("KpPhaseLoopA", data)
        data = self.get_KpPhaseLoopB()
        self.push_change_event("KpPhaseLoopB", data)
        data = self.get_KiPhaseLoopA()
        self.push_change_event("KiPhaseLoopA", data)
        data = self.get_KiPhaseLoopB()
        self.push_change_event("KiPhaseLoopB", data)
        data = self.get_PiLimitFastPiIqA()
        self.push_change_event("PiLimitFastPiIqA", data)
        data = self.get_PiLimitFastPiIqB()
        self.push_change_event("PiLimitFastPiIqB", data)
        data = bool(self.get_PulseModeEnableA())
        self.push_change_event("PulseModeEnableA", data)
        data = bool(self.get_PulseModeEnableB())
        self.push_change_event("PulseModeEnableB", data)
        data = bool(self.get_AutomaticConditioningEnableA())
        self.push_change_event("AutomaticConditioningEnableA", data)
        data = bool(self.get_AutomaticConditioningEnableB())
        self.push_change_event("AutomaticConditioningEnableB", data)
        data = self.get_ConditioningdutyCicleA()
        self.push_change_event("ConditioningdutyCicleA", data)
        data = self.get_ConditioningdutyCicleB()
        self.push_change_event("ConditioningdutyCicleB", data)
        data = bool(self.get_TuningEnableA())
        self.push_change_event("TuningEnableA", data)
        data = bool(self.get_TuningEnableB())
        self.push_change_event("TuningEnableB", data)
        data = bool(self.get_TuningPosEnA())
        self.push_change_event("TuningPosEnA", data)
        data = bool(self.get_TuningPosEnB())
        self.push_change_event("TuningPosEnB", data)
        data = self.get_NumStepsA()
        self.push_change_event("NumStepsA", data)
        data = self.get_NumStepsB()
        self.push_change_event("NumStepsB", data)
        data = self.get_PulsesFrequencyA()
        self.push_change_event("PulsesFrequencyA", data)
        data = self.get_PulsesFrequencyB()
        self.push_change_event("PulsesFrequencyB", data)
        data = self.get_PhaseOffsetA()
        self.push_change_event("PhaseOffsetA", data)
        data = self.get_PhaseOffsetB()
        self.push_change_event("PhaseOffsetB", data)
        data = bool(self.get_MoveA())
        self.push_change_event("MoveA", data)
        data = bool(self.get_MoveB())
        self.push_change_event("MoveB", data)
        data = bool(self.get_MoveupA())
        self.push_change_event("MoveupA", data)
        data = bool(self.get_MoveupB())
        self.push_change_event("MoveupB", data)
        data = bool(self.get_TuningresetA())
        self.push_change_event("TuningresetA", data)
        data = bool(self.get_TuningresetB())
        self.push_change_event("TuningresetB", data)
        data = self.get_FwminA()
        self.push_change_event("FwminA", data)
        data = self.get_FwminB()
        self.push_change_event("FwminB", data)
        data = self.get_MarginupA()
        self.push_change_event("MarginupA", data)
        data = self.get_MarginupB()
        self.push_change_event("MarginupB", data)
        data = self.get_MarginlowA()
        self.push_change_event("MarginlowA", data)
        data = self.get_MarginlowB()
        self.push_change_event("MarginlowB", data)
        data = self.get_TuningdelayA()
        self.push_change_event("TuningdelayA", data)
        data = self.get_TuningdelayB()
        self.push_change_event("TuningdelayB", data)
        data = bool(self.get_TuningfilterenableA())
        self.push_change_event("TuningfilterenableA", data)
        data = bool(self.get_TuningfilterenableB())
        self.push_change_event("TuningfilterenableB", data)
        data = bool(self.get_TuningtriggerenableA())
        self.push_change_event("TuningtriggerenableA", data)
        data = bool(self.get_TuningtriggerenableB())
        self.push_change_event("TuningtriggerenableB", data)
        data = bool(self.get_EpsItckDisableA())
        self.push_change_event("EpsItckDisableA", data)
        data = bool(self.get_EpsItckDisableB())
        self.push_change_event("EpsItckDisableB", data)
        data = bool(self.get_FimItckDisableA())
        self.push_change_event("FimItckDisableA", data)
        data = bool(self.get_FimItckDisableB())
        self.push_change_event("FimItckDisableB", data)
        data = self.get_MDividerA()
        self.push_change_event("MDividerA", data)
        data = self.get_MDividerB()
        self.push_change_event("MDividerB", data)
        data = self.get_NDividerA()
        self.push_change_event("NDividerA", data)
        data = self.get_NDividerB()
        self.push_change_event("NDividerB", data)
        data = self.get_MuxselA()
        self.push_change_event("MuxselA", data)
        data = self.get_MuxselB()
        self.push_change_event("MuxselB", data)
        data = self.get_Mux0DividerA()
        self.push_change_event("Mux0DividerA", data)
        data = self.get_Mux0DividerB()
        self.push_change_event("Mux0DividerB", data)
        data = self.get_Mux1DividerA()
        self.push_change_event("Mux1DividerA", data)
        data = self.get_Mux1DividerB()
        self.push_change_event("Mux1DividerB", data)
        data = self.get_Mux2DividerA()
        self.push_change_event("Mux2DividerA", data)
        data = self.get_Mux2DividerB()
        self.push_change_event("Mux2DividerB", data)
        data = self.get_Mux3DividerA()
        self.push_change_event("Mux3DividerA", data)
        data = self.get_Mux3DividerB()
        self.push_change_event("Mux3DividerB", data)
        data = self.get_Mux4DividerA()
        self.push_change_event("Mux4DividerA", data)
        data = self.get_Mux4DividerB()
        self.push_change_event("Mux4DividerB", data)
        data = bool(self.get_SendWordA())
        self.push_change_event("SendWordA", data)
        data = bool(self.get_SendWordB())
        self.push_change_event("SendWordB", data)
        data = bool(self.get_CpdirA())
        self.push_change_event("CpdirA", data)
        data = bool(self.get_CpdirB())
        self.push_change_event("CpdirB", data)
        data = bool(self.get_VcxoOutputInversionA())
        self.push_change_event("VcxoOutputInversionA", data)
        data = bool(self.get_VcxoOutputInversionB())
        self.push_change_event("VcxoOutputInversionB", data)


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
        perseus_utils.write_direct(self.perseus, True, TUNING_RESET_ADDRESS, 'A')
        perseus_utils.write_direct(self.perseus, False, TUNING_RESET_ADDRESS, 'A')

    @command
    def tuning_resetB(self):
        perseus_utils.write_direct(self.perseus, True, TUNING_RESET_ADDRESS, 'B')
        perseus_utils.write_direct(self.perseus, False, TUNING_RESET_ADDRESS, 'B')

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
        filename = now.strftime("{0}/%Y_%m_%d__%H_%M_%S_loops_data.bin").format(self.FDLPath)
        self.perseus.get_ram_data(filename)

        # Check transfer data complete
        while self.perseus.get_transfer_over_register() is not RAM_TRANSFER_OVER:
            time.sleep(0.1) # @warning: super dangerous way of checking it ... who restarts the register?

        # Clear FDL trigger attribute
        # ... but ... HOW?

        # Restart RAM
        self.perseus.init_fast_data_logger()


def run_device():
    run([Nutaq])

if __name__ == "__main__":
    run_device()
