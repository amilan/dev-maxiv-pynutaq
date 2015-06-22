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
                                   fget="get_VcxoOutputInversionB",
                                   fset="set_VcxoOutputInversionB",
                                   doc=""
                                   )

    Diag_IcavLoopsA = attribute(label='Diag_IcavLoopsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcavLoopsB = attribute(label='Diag_IcavLoopsB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcavLoopsA = attribute(label='Diag_QcavLoopsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcavLoopsB = attribute(label='Diag_QcavLoopsB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolA = attribute(label='Diag_IcontrolA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolB = attribute(label='Diag_IcontrolB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolA = attribute(label='Diag_QcontrolA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolB = attribute(label='Diag_QcontrolB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Icontrol1A = attribute(label='Diag_Icontrol1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Icontrol1B = attribute(label='Diag_Icontrol1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qcontrol1A = attribute(label='Diag_Qcontrol1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qcontrol1B = attribute(label='Diag_Qcontrol1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Icontrol2A = attribute(label='Diag_Icontrol2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Icontrol2B = attribute(label='Diag_Icontrol2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qcontrol2A = attribute(label='Diag_Qcontrol2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qcontrol2B = attribute(label='Diag_Qcontrol2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IerrorA = attribute(label='Diag_IerrorA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IerrorB = attribute(label='Diag_IerrorB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QerrorA = attribute(label='Diag_QerrorA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QerrorB = attribute(label='Diag_QerrorB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IerroraccumA = attribute(label='Diag_IerroraccumA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IerroraccumB = attribute(label='Diag_IerroraccumB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QerroraccumA = attribute(label='Diag_QerroraccumA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QerroraccumB = attribute(label='Diag_QerroraccumB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrefA = attribute(label='Diag_IrefA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrefB = attribute(label='Diag_IrefB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrefA = attribute(label='Diag_QrefA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrefB = attribute(label='Diag_QrefB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwCavLoopsA = attribute(label='Diag_IFwCavLoopsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwCavLoopsB = attribute(label='Diag_IFwCavLoopsB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwCavLoopsA = attribute(label='Diag_QFwCavLoopsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwCavLoopsB = attribute(label='Diag_QFwCavLoopsB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwTet1LoopsA = attribute(label='Diag_IFwTet1LoopsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwTet1LoopsB = attribute(label='Diag_IFwTet1LoopsB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwTet1LoopsA = attribute(label='Diag_QFwTet1LoopsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwTet1LoopsB = attribute(label='Diag_QFwTet1LoopsB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwTet2LoopsA = attribute(label='Diag_IFwTet2LoopsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwTet2LoopsB = attribute(label='Diag_IFwTet2LoopsB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwTet2LoopsA = attribute(label='Diag_QFwTet2LoopsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwTet2LoopsB = attribute(label='Diag_QFwTet2LoopsB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwCircInLoopsA = attribute(label='Diag_IFwCircInLoopsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IFwCircInLoopsB = attribute(label='Diag_IFwCircInLoopsB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwCircInLoopsA = attribute(label='Diag_QFwCircInLoopsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QFwCircInLoopsB = attribute(label='Diag_QFwCircInLoopsB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
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

    Diag_Ispare1A = attribute(label='Diag_Ispare1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ispare1B = attribute(label='Diag_Ispare1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qspare1A = attribute(label='Diag_Qspare1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qspare1B = attribute(label='Diag_Qspare1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ispare2A = attribute(label='Diag_Ispare2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ispare2B = attribute(label='Diag_Ispare2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qspare2A = attribute(label='Diag_Qspare2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qspare2B = attribute(label='Diag_Qspare2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxCavA = attribute(label='Diag_IMuxCavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxCavB = attribute(label='Diag_IMuxCavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxCavA = attribute(label='Diag_QMuxCavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxCavB = attribute(label='Diag_QMuxCavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwCavA = attribute(label='Diag_IMuxFwCavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwCavB = attribute(label='Diag_IMuxFwCavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwCavA = attribute(label='Diag_QMuxFwCavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwCavB = attribute(label='Diag_QMuxFwCavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwTet1A = attribute(label='Diag_IMuxFwTet1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwTet1B = attribute(label='Diag_IMuxFwTet1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwTet1A = attribute(label='Diag_QMuxFwTet1A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwTet1B = attribute(label='Diag_QMuxFwTet1B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwTet2A = attribute(label='Diag_IMuxFwTet2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwTet2B = attribute(label='Diag_IMuxFwTet2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwTet2A = attribute(label='Diag_QMuxFwTet2A',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwTet2B = attribute(label='Diag_QMuxFwTet2B',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwCircInA = attribute(label='Diag_IMuxFwCircInA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IMuxFwCircInB = attribute(label='Diag_IMuxFwCircInB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwCircInA = attribute(label='Diag_QMuxFwCircInA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QMuxFwCircInB = attribute(label='Diag_QMuxFwCircInB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpCavA = attribute(label='Diag_AmpCavA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpCavB = attribute(label='Diag_AmpCavB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwA = attribute(label='Diag_AmpFwA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwB = attribute(label='Diag_AmpFwB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngCavFwA = attribute(label='Diag_AngCavFwA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngCavFwB = attribute(label='Diag_AngCavFwB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngCavLA = attribute(label='Diag_AngCavLA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngCavLB = attribute(label='Diag_AngCavLB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngFwLA = attribute(label='Diag_AngFwLA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AngFwLB = attribute(label='Diag_AngFwLB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Vaccum1A = attribute(label='Diag_Vaccum1A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Vaccum1B = attribute(label='Diag_Vaccum1B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Vaccum2A = attribute(label='Diag_Vaccum2A',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Vaccum2B = attribute(label='Diag_Vaccum2B',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolSlowpiA = attribute(label='Diag_IcontrolSlowpiA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolSlowpiB = attribute(label='Diag_IcontrolSlowpiB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolSlowpiA = attribute(label='Diag_QcontrolSlowpiA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolSlowpiB = attribute(label='Diag_QcontrolSlowpiB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolFastpiA = attribute(label='Diag_IcontrolFastpiA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolFastpiB = attribute(label='Diag_IcontrolFastpiB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolFastpiA = attribute(label='Diag_QcontrolFastpiA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolFastpiB = attribute(label='Diag_QcontrolFastpiB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoPoweredA = attribute(label='Diag_VcxoPoweredA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoPoweredB = attribute(label='Diag_VcxoPoweredB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoRefA = attribute(label='Diag_VcxoRefA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoRefB = attribute(label='Diag_VcxoRefB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoLockedA = attribute(label='Diag_VcxoLockedA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoLockedB = attribute(label='Diag_VcxoLockedB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoCableDisconnectedA = attribute(label='Diag_VcxoCableDisconnectedA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_VcxoCableDisconnectedB = attribute(label='Diag_VcxoCableDisconnectedB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarForAmplitudeLoopA = attribute(label='Diag_IpolarForAmplitudeLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarForAmplitudeLoopB = attribute(label='Diag_IpolarForAmplitudeLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarForAmplitudeLoopA = attribute(label='Diag_QpolarForAmplitudeLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarForAmplitudeLoopB = attribute(label='Diag_QpolarForAmplitudeLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarForPhaseLoopA = attribute(label='Diag_IpolarForPhaseLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarForPhaseLoopB = attribute(label='Diag_IpolarForPhaseLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarForPhaseLoopA = attribute(label='Diag_QpolarForPhaseLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarForPhaseLoopB = attribute(label='Diag_QpolarForPhaseLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpInputOfAmpLoopA = attribute(label='Diag_AmpInputOfAmpLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpInputOfAmpLoopB = attribute(label='Diag_AmpInputOfAmpLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhaseInputOfAmpLoopA = attribute(label='Diag_PhaseInputOfAmpLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhaseInputOfAmpLoopB = attribute(label='Diag_PhaseInputOfAmpLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpInputOfPhaseLoopA = attribute(label='Diag_AmpInputOfPhaseLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpInputOfPhaseLoopB = attribute(label='Diag_AmpInputOfPhaseLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhInputOfPhaseLoopA = attribute(label='Diag_PhInputOfPhaseLoopA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhInputOfPhaseLoopB = attribute(label='Diag_PhInputOfPhaseLoopB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopControlOutputA = attribute(label='Diag_AmpLoopControlOutputA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopControlOutputB = attribute(label='Diag_AmpLoopControlOutputB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopErrorA = attribute(label='Diag_AmpLoopErrorA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopErrorB = attribute(label='Diag_AmpLoopErrorB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopErrorAccumA = attribute(label='Diag_AmpLoopErrorAccumA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopErrorAccumB = attribute(label='Diag_AmpLoopErrorAccumB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopControlOutputA = attribute(label='Diag_PhLoopControlOutputA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopControlOutputB = attribute(label='Diag_PhLoopControlOutputB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopErrorA = attribute(label='Diag_PhLoopErrorA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopErrorB = attribute(label='Diag_PhLoopErrorB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopErrorAccumA = attribute(label='Diag_PhLoopErrorAccumA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopErrorAccumB = attribute(label='Diag_PhLoopErrorAccumB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarControlOutputA = attribute(label='Diag_IpolarControlOutputA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IpolarControlOutputB = attribute(label='Diag_IpolarControlOutputB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarControlOutputA = attribute(label='Diag_QpolarControlOutputA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QpolarControlOutputB = attribute(label='Diag_QpolarControlOutputB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolSlowpiIqA = attribute(label='Diag_IcontrolSlowpiIqA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolSlowpiIqB = attribute(label='Diag_IcontrolSlowpiIqB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolSlowpiqA = attribute(label='Diag_QcontrolSlowpiqA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolSlowpiqB = attribute(label='Diag_QcontrolSlowpiqB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolFastpiIqA = attribute(label='Diag_IcontrolFastpiIqA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IcontrolFastpiIqB = attribute(label='Diag_IcontrolFastpiIqB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolFastpiIqA = attribute(label='Diag_QcontrolFastpiIqA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QcontrolFastpiIqB = attribute(label='Diag_QcontrolFastpiIqB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IloopinputSlowpiIqA = attribute(label='Diag_IloopinputSlowpiIqA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IloopinputSlowpiIqB = attribute(label='Diag_IloopinputSlowpiIqB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QloopinputSlowpiIqA = attribute(label='Diag_QloopinputSlowpiIqA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QloopinputSlowpiIqB = attribute(label='Diag_QloopinputSlowpiIqB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IloopinputFastpiIqA = attribute(label='Diag_IloopinputFastpiIqA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IloopinputFastpiIqB = attribute(label='Diag_IloopinputFastpiIqB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QloopinputFastpiIqA = attribute(label='Diag_QloopinputFastpiIqA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QloopinputFastpiIqB = attribute(label='Diag_QloopinputFastpiIqB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrefloopinputFastpiIqA = attribute(label='Diag_IrefloopinputFastpiIqA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_IrefloopinputFastpiIqB = attribute(label='Diag_IrefloopinputFastpiIqB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrefloopinputFastpiIqA = attribute(label='Diag_QrefloopinputFastpiIqA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_QrefloopinputFastpiIqB = attribute(label='Diag_QrefloopinputFastpiIqB',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_MovingPlungerAutoA = attribute(label='Diag_MovingPlungerAutoA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_MovingPlungerAutoB = attribute(label='Diag_MovingPlungerAutoB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FreqUpA = attribute(label='Diag_FreqUpA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FreqUpB = attribute(label='Diag_FreqUpB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualTuningOnA = attribute(label='Diag_ManualTuningOnA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualTuningOnB = attribute(label='Diag_ManualTuningOnB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualTuningFreqUpA = attribute(label='Diag_ManualTuningFreqUpA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualTuningFreqUpB = attribute(label='Diag_ManualTuningFreqUpB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwminA = attribute(label='Diag_FwminA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FwminB = attribute(label='Diag_FwminB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_EpsItckDelayA = attribute(label='Diag_EpsItckDelayA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_EpsItckDelayB = attribute(label='Diag_EpsItckDelayB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FimItckDelayA = attribute(label='Diag_FimItckDelayA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FimItckDelayB = attribute(label='Diag_FimItckDelayB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTrigHwInputA = attribute(label='Diag_FdlTrigHwInputA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTrigHwInputB = attribute(label='Diag_FdlTrigHwInputB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTrigSwInputA = attribute(label='Diag_FdlTrigSwInputA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTrigSwInputB = attribute(label='Diag_FdlTrigSwInputB',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwcircina = attribute(label='Diag_AmpMuxfwcircina',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpSpare1a = attribute(label='Diag_AmpSpare1a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwcircinb = attribute(label='Diag_AmpMuxfwcircinb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpSpare2a = attribute(label='Diag_AmpSpare2a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpSpare2b = attribute(label='Diag_AmpSpare2b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpErrora = attribute(label='Diag_AmpErrora',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpErrorb = attribute(label='Diag_AmpErrorb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpSpare1b = attribute(label='Diag_AmpSpare1b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpErroraccumb = attribute(label='Diag_AmpErroraccumb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpErroraccuma = attribute(label='Diag_AmpErroraccuma',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlfastpiiqb = attribute(label='Diag_AmpControlfastpiiqb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlfastpiiqa = attribute(label='Diag_AmpControlfastpiiqa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControla = attribute(label='Diag_AmpControla',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarforamplitudeloopa = attribute(label='Diag_AmpPolarforamplitudeloopa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarforamplitudeloopb = attribute(label='Diag_AmpPolarforamplitudeloopb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlb = attribute(label='Diag_AmpControlb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwtet2b = attribute(label='Diag_AmpMuxfwtet2b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopinputfastpiiqb = attribute(label='Diag_AmpLoopinputfastpiiqb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopinputfastpiiqa = attribute(label='Diag_AmpLoopinputfastpiiqa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRefa = attribute(label='Diag_AmpRefa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwcava = attribute(label='Diag_AmpMuxfwcava',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwcavb = attribute(label='Diag_AmpMuxfwcavb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRefb = attribute(label='Diag_AmpRefb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControl2a = attribute(label='Diag_AmpControl2a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControl2b = attribute(label='Diag_AmpControl2b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwtet1loopsb = attribute(label='Diag_AmpFwtet1loopsb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwtet1loopsa = attribute(label='Diag_AmpFwtet1loopsa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarforphaseloopb = attribute(label='Diag_AmpPolarforphaseloopb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarforphaseloopa = attribute(label='Diag_AmpPolarforphaseloopa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarcontroloutputb = attribute(label='Diag_AmpPolarcontroloutputb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpPolarcontroloutputa = attribute(label='Diag_AmpPolarcontroloutputa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwtet2loopsa = attribute(label='Diag_AmpFwtet2loopsa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpCavloopsa = attribute(label='Diag_AmpCavloopsa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpCavloopsb = attribute(label='Diag_AmpCavloopsb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwtet2loopsb = attribute(label='Diag_AmpFwtet2loopsb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopinputslowpiiqa = attribute(label='Diag_AmpLoopinputslowpiiqa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLoopinputslowpiiqb = attribute(label='Diag_AmpLoopinputslowpiiqb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRefloopinputfastpiiqb = attribute(label='Diag_AmpRefloopinputfastpiiqb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRefloopinputfastpiiqa = attribute(label='Diag_AmpRefloopinputfastpiiqa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControl1a = attribute(label='Diag_AmpControl1a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControl1b = attribute(label='Diag_AmpControl1b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwtet2a = attribute(label='Diag_AmpMuxfwtet2a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxcavb = attribute(label='Diag_AmpMuxcavb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxcava = attribute(label='Diag_AmpMuxcava',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwtet1b = attribute(label='Diag_AmpMuxfwtet1b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlfastpib = attribute(label='Diag_AmpControlfastpib',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcircinloopsa = attribute(label='Diag_AmpFwcircinloopsa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcircinloopsb = attribute(label='Diag_AmpFwcircinloopsb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlfastpia = attribute(label='Diag_AmpControlfastpia',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcavloopsa = attribute(label='Diag_AmpFwcavloopsa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMuxfwtet1a = attribute(label='Diag_AmpMuxfwtet1a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcavloopsb = attribute(label='Diag_AmpFwcavloopsb',
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

    Diag_AmpMoa = attribute(label='Diag_AmpMoa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlslowpia = attribute(label='Diag_AmpControlslowpia',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpControlslowpib = attribute(label='Diag_AmpControlslowpib',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwcircina = attribute(label='Diag_PhMuxfwcircina',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhSpare1a = attribute(label='Diag_PhSpare1a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwcircinb = attribute(label='Diag_PhMuxfwcircinb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhSpare2a = attribute(label='Diag_PhSpare2a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhSpare2b = attribute(label='Diag_PhSpare2b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhErrora = attribute(label='Diag_PhErrora',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhErrorb = attribute(label='Diag_PhErrorb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhSpare1b = attribute(label='Diag_PhSpare1b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhErroraccumb = attribute(label='Diag_PhErroraccumb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhErroraccuma = attribute(label='Diag_PhErroraccuma',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlfastpiiqb = attribute(label='Diag_PhControlfastpiiqb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlfastpiiqa = attribute(label='Diag_PhControlfastpiiqa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControla = attribute(label='Diag_PhControla',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarforamplitudeloopa = attribute(label='Diag_PhPolarforamplitudeloopa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarforamplitudeloopb = attribute(label='Diag_PhPolarforamplitudeloopb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlb = attribute(label='Diag_PhControlb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwtet2b = attribute(label='Diag_PhMuxfwtet2b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopinputfastpiiqb = attribute(label='Diag_PhLoopinputfastpiiqb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopinputfastpiiqa = attribute(label='Diag_PhLoopinputfastpiiqa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRefa = attribute(label='Diag_PhRefa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwcava = attribute(label='Diag_PhMuxfwcava',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwcavb = attribute(label='Diag_PhMuxfwcavb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRefb = attribute(label='Diag_PhRefb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControl2a = attribute(label='Diag_PhControl2a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControl2b = attribute(label='Diag_PhControl2b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwtet1loopsb = attribute(label='Diag_PhFwtet1loopsb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwtet1loopsa = attribute(label='Diag_PhFwtet1loopsa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarforphaseloopb = attribute(label='Diag_PhPolarforphaseloopb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarforphaseloopa = attribute(label='Diag_PhPolarforphaseloopa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarcontroloutputb = attribute(label='Diag_PhPolarcontroloutputb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhPolarcontroloutputa = attribute(label='Diag_PhPolarcontroloutputa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwtet2loopsa = attribute(label='Diag_PhFwtet2loopsa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhCavloopsa = attribute(label='Diag_PhCavloopsa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhCavloopsb = attribute(label='Diag_PhCavloopsb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwtet2loopsb = attribute(label='Diag_PhFwtet2loopsb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopinputslowpiiqa = attribute(label='Diag_PhLoopinputslowpiiqa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLoopinputslowpiiqb = attribute(label='Diag_PhLoopinputslowpiiqb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRefloopinputfastpiiqb = attribute(label='Diag_PhRefloopinputfastpiiqb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRefloopinputfastpiiqa = attribute(label='Diag_PhRefloopinputfastpiiqa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControl1a = attribute(label='Diag_PhControl1a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControl1b = attribute(label='Diag_PhControl1b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwtet2a = attribute(label='Diag_PhMuxfwtet2a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxcavb = attribute(label='Diag_PhMuxcavb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxcava = attribute(label='Diag_PhMuxcava',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwtet1b = attribute(label='Diag_PhMuxfwtet1b',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlfastpib = attribute(label='Diag_PhControlfastpib',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcircinloopsa = attribute(label='Diag_PhFwcircinloopsa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcircinloopsb = attribute(label='Diag_PhFwcircinloopsb',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlfastpia = attribute(label='Diag_PhControlfastpia',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcavloopsa = attribute(label='Diag_PhFwcavloopsa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMuxfwtet1a = attribute(label='Diag_PhMuxfwtet1a',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcavloopsb = attribute(label='Diag_PhFwcavloopsb',
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

    Diag_PhMoa = attribute(label='Diag_PhMoa',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlslowpia = attribute(label='Diag_PhControlslowpia',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhControlslowpib = attribute(label='Diag_PhControlslowpib',
                                   dtype=float,
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
            self.set_state(DevState.ON)
        except Exception, e:
            print e
            self.set_state(DevState.FAULT)


    @DebugIt()
    def get_KpA(self):
        return perseus_utils.read_direct(self.perseus, 0, 'A')

    @DebugIt()
    def set_KpA(self, KpA):
        perseus_utils.write_direct(self.perseus, KpA, 0, 'A')

    @DebugIt()
    def get_KpB(self):
        return perseus_utils.read_direct(self.perseus, 0, 'B')

    @DebugIt()
    def set_KpB(self, KpB):
        perseus_utils.write_direct(self.perseus, KpB, 0, 'B')

    @DebugIt()
    def get_KiA(self):
        return perseus_utils.read_direct(self.perseus, 1, 'A')

    @DebugIt()
    def set_KiA(self, KiA):
        perseus_utils.write_direct(self.perseus, KiA, 1, 'A')

    @DebugIt()
    def get_KiB(self):
        return perseus_utils.read_direct(self.perseus, 1, 'B')

    @DebugIt()
    def set_KiB(self, KiB):
        perseus_utils.write_direct(self.perseus, KiB, 1, 'B')

    @DebugIt()
    def get_PhaseShiftCavA(self):
        return perseus_utils.read_angle(self.perseus, 2, 'A')

    @DebugIt()
    def set_PhaseShiftCavA(self, PhaseShiftCavA):
        perseus_utils.write_angle(self.perseus, PhaseShiftCavA, 2, 'A')

    @DebugIt()
    def get_PhaseShiftCavB(self):
        return perseus_utils.read_angle(self.perseus, 2, 'B')

    @DebugIt()
    def set_PhaseShiftCavB(self, PhaseShiftCavB):
        perseus_utils.write_angle(self.perseus, PhaseShiftCavB, 2, 'B')

    @DebugIt()
    def get_PhaseShiftFwcavA(self):
        return perseus_utils.read_angle(self.perseus, 3, 'A')

    @DebugIt()
    def set_PhaseShiftFwcavA(self, PhaseShiftFwcavA):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwcavA, 3, 'A')

    @DebugIt()
    def get_PhaseShiftFwcavB(self):
        return perseus_utils.read_angle(self.perseus, 3, 'B')

    @DebugIt()
    def set_PhaseShiftFwcavB(self, PhaseShiftFwcavB):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwcavB, 3, 'B')

    @DebugIt()
    def get_PhaseShiftFwtet1A(self):
        return perseus_utils.read_angle(self.perseus, 4, 'A')

    @DebugIt()
    def set_PhaseShiftFwtet1A(self, PhaseShiftFwtet1A):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwtet1A, 4, 'A')

    @DebugIt()
    def get_PhaseShiftFwtet1B(self):
        return perseus_utils.read_angle(self.perseus, 4, 'B')

    @DebugIt()
    def set_PhaseShiftFwtet1B(self, PhaseShiftFwtet1B):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwtet1B, 4, 'B')

    @DebugIt()
    def get_PhaseShiftFwtet2A(self):
        return perseus_utils.read_angle(self.perseus, 5, 'A')

    @DebugIt()
    def set_PhaseShiftFwtet2A(self, PhaseShiftFwtet2A):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwtet2A, 5, 'A')

    @DebugIt()
    def get_PhaseShiftFwtet2B(self):
        return perseus_utils.read_angle(self.perseus, 5, 'B')

    @DebugIt()
    def set_PhaseShiftFwtet2B(self, PhaseShiftFwtet2B):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwtet2B, 5, 'B')

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

    @DebugIt()
    def get_SamplesToAverageA(self):
        return perseus_utils.read_direct(self.perseus, 7, 'A')

    @DebugIt()
    def set_SamplesToAverageA(self, SamplesToAverageA):
        perseus_utils.write_direct(self.perseus, SamplesToAverageA, 7, 'A')

    @DebugIt()
    def get_SamplesToAverageB(self):
        return perseus_utils.read_direct(self.perseus, 7, 'B')

    @DebugIt()
    def set_SamplesToAverageB(self, SamplesToAverageB):
        perseus_utils.write_direct(self.perseus, SamplesToAverageB, 7, 'B')

    @DebugIt()
    def get_FilterStagesA(self):
        return perseus_utils.read_direct(self.perseus, 8, 'A')

    @DebugIt()
    def set_FilterStagesA(self, FilterStagesA):
        perseus_utils.write_direct(self.perseus, FilterStagesA, 8, 'A')

    @DebugIt()
    def get_FilterStagesB(self):
        return perseus_utils.read_direct(self.perseus, 8, 'B')

    @DebugIt()
    def set_FilterStagesB(self, FilterStagesB):
        perseus_utils.write_direct(self.perseus, FilterStagesB, 8, 'B')

    @DebugIt()
    def get_PhaseShiftFwcircinA(self):
        return perseus_utils.read_angle(self.perseus, 9, 'A')

    @DebugIt()
    def set_PhaseShiftFwcircinA(self, PhaseShiftFwcircinA):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwcircinA, 9, 'A')

    @DebugIt()
    def get_PhaseShiftFwcircinB(self):
        return perseus_utils.read_angle(self.perseus, 9, 'B')

    @DebugIt()
    def set_PhaseShiftFwcircinB(self, PhaseShiftFwcircinB):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwcircinB, 9, 'B')

    @DebugIt()
    def get_PhaseShiftControlSignalTet1A(self):
        return perseus_utils.read_angle(self.perseus, 10, 'A')

    @DebugIt()
    def set_PhaseShiftControlSignalTet1A(self, PhaseShiftControlSignalTet1A):
        perseus_utils.write_angle(self.perseus, PhaseShiftControlSignalTet1A, 10, 'A')

    @DebugIt()
    def get_PhaseShiftControlSignalTet1B(self):
        return perseus_utils.read_angle(self.perseus, 10, 'B')

    @DebugIt()
    def set_PhaseShiftControlSignalTet1B(self, PhaseShiftControlSignalTet1B):
        perseus_utils.write_angle(self.perseus, PhaseShiftControlSignalTet1B, 10, 'B')

    @DebugIt()
    def get_PhaseShiftControlSignalTet2A(self):
        return perseus_utils.read_angle(self.perseus, 11, 'A')

    @DebugIt()
    def set_PhaseShiftControlSignalTet2A(self, PhaseShiftControlSignalTet2A):
        perseus_utils.write_angle(self.perseus, PhaseShiftControlSignalTet2A, 11, 'A')

    @DebugIt()
    def get_PhaseShiftControlSignalTet2B(self):
        return perseus_utils.read_angle(self.perseus, 11, 'B')

    @DebugIt()
    def set_PhaseShiftControlSignalTet2B(self, PhaseShiftControlSignalTet2B):
        perseus_utils.write_angle(self.perseus, PhaseShiftControlSignalTet2B, 11, 'B')

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

    @DebugIt()
    def get_AutomaticStartupEnableA(self):
        return perseus_utils.read_direct(self.perseus, 15, 'A')

    @DebugIt()
    def set_AutomaticStartupEnableA(self, AutomaticStartupEnableA):
        perseus_utils.write_direct(self.perseus, AutomaticStartupEnableA, 15, 'A')

    @DebugIt()
    def get_AutomaticStartupEnableB(self):
        return perseus_utils.read_direct(self.perseus, 15, 'B')

    @DebugIt()
    def set_AutomaticStartupEnableB(self, AutomaticStartupEnableB):
        perseus_utils.write_direct(self.perseus, AutomaticStartupEnableB, 15, 'B')

    @DebugIt()
    def get_CommandStartA(self):
        return perseus_utils.read_direct(self.perseus, 16, 'A')

    @DebugIt()
    def set_CommandStartA(self, CommandStartA):
        perseus_utils.write_direct(self.perseus, CommandStartA, 16, 'A')

    @DebugIt()
    def get_CommandStartB(self):
        return perseus_utils.read_direct(self.perseus, 16, 'B')

    @DebugIt()
    def set_CommandStartB(self, CommandStartB):
        perseus_utils.write_direct(self.perseus, CommandStartB, 16, 'B')

    @DebugIt()
    def get_AmprefinA(self):
        return perseus_utils.read_milivolts(self.perseus, 19, 'A')

    @DebugIt()
    def set_AmprefinA(self, AmprefinA):
        perseus_utils.write_milivolts(self.perseus, AmprefinA, 19, 'A')

    @DebugIt()
    def get_AmprefinB(self):
        return perseus_utils.read_milivolts(self.perseus, 19, 'B')

    @DebugIt()
    def set_AmprefinB(self, AmprefinB):
        perseus_utils.write_milivolts(self.perseus, AmprefinB, 19, 'B')

    @DebugIt()
    def get_PhrefinA(self):
        return perseus_utils.read_angle(self.perseus, 20, 'A')

    @DebugIt()
    def set_PhrefinA(self, PhrefinA):
        perseus_utils.write_angle(self.perseus, PhrefinA, 20, 'A')

    @DebugIt()
    def get_PhrefinB(self):
        return perseus_utils.read_angle(self.perseus, 20, 'B')

    @DebugIt()
    def set_PhrefinB(self, PhrefinB):
        perseus_utils.write_angle(self.perseus, PhrefinB, 20, 'B')

    @DebugIt()
    def get_AmprefminA(self):
        return perseus_utils.read_milivolts(self.perseus, 21, 'A')

    @DebugIt()
    def set_AmprefminA(self, AmprefminA):
        perseus_utils.write_milivolts(self.perseus, AmprefminA, 21, 'A')

    @DebugIt()
    def get_AmprefminB(self):
        return perseus_utils.read_milivolts(self.perseus, 21, 'B')

    @DebugIt()
    def set_AmprefminB(self, AmprefminB):
        perseus_utils.write_milivolts(self.perseus, AmprefminB, 21, 'B')

    @DebugIt()
    def get_PhrefminA(self):
        return perseus_utils.read_angle(self.perseus, 22, 'A')

    @DebugIt()
    def set_PhrefminA(self, PhrefminA):
        perseus_utils.write_angle(self.perseus, PhrefminA, 22, 'A')

    @DebugIt()
    def get_PhrefminB(self):
        return perseus_utils.read_angle(self.perseus, 22, 'B')

    @DebugIt()
    def set_PhrefminB(self, PhrefminB):
        perseus_utils.write_angle(self.perseus, PhrefminB, 22, 'B')

    @DebugIt()
    def get_PhaseIncreaseRateA(self):
        return perseus_utils.read_direct(self.perseus, 23, 'A')

    @DebugIt()
    def set_PhaseIncreaseRateA(self, PhaseIncreaseRateA):
        perseus_utils.write_direct(self.perseus, PhaseIncreaseRateA, 23, 'A')

    @DebugIt()
    def get_PhaseIncreaseRateB(self):
        return perseus_utils.read_direct(self.perseus, 23, 'B')

    @DebugIt()
    def set_PhaseIncreaseRateB(self, PhaseIncreaseRateB):
        perseus_utils.write_direct(self.perseus, PhaseIncreaseRateB, 23, 'B')

    @DebugIt()
    def get_VoltageIncreaseRateA(self):
        return perseus_utils.read_direct(self.perseus, 24, 'A')

    @DebugIt()
    def set_VoltageIncreaseRateA(self, VoltageIncreaseRateA):
        perseus_utils.write_direct(self.perseus, VoltageIncreaseRateA, 24, 'A')

    @DebugIt()
    def get_VoltageIncreaseRateB(self):
        return perseus_utils.read_direct(self.perseus, 24, 'B')

    @DebugIt()
    def set_VoltageIncreaseRateB(self, VoltageIncreaseRateB):
        perseus_utils.write_direct(self.perseus, VoltageIncreaseRateB, 24, 'B')

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

    @DebugIt()
    def get_SpareGpioOutput01A(self):
        return perseus_utils.read_direct(self.perseus, 28, 'A')

    @DebugIt()
    def set_SpareGpioOutput01A(self, SpareGpioOutput01A):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput01A, 28, 'A')

    @DebugIt()
    def get_SpareGpioOutput01B(self):
        return perseus_utils.read_direct(self.perseus, 28, 'B')

    @DebugIt()
    def set_SpareGpioOutput01B(self, SpareGpioOutput01B):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput01B, 28, 'B')

    @DebugIt()
    def get_SpareGpioOutput02A(self):
        return perseus_utils.read_direct(self.perseus, 29, 'A')

    @DebugIt()
    def set_SpareGpioOutput02A(self, SpareGpioOutput02A):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput02A, 29, 'A')

    @DebugIt()
    def get_SpareGpioOutput02B(self):
        return perseus_utils.read_direct(self.perseus, 29, 'B')

    @DebugIt()
    def set_SpareGpioOutput02B(self, SpareGpioOutput02B):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput02B, 29, 'B')

    @DebugIt()
    def get_SpareGpioOutput03A(self):
        return perseus_utils.read_direct(self.perseus, 30, 'A')

    @DebugIt()
    def set_SpareGpioOutput03A(self, SpareGpioOutput03A):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput03A, 30, 'A')

    @DebugIt()
    def get_SpareGpioOutput03B(self):
        return perseus_utils.read_direct(self.perseus, 30, 'B')

    @DebugIt()
    def set_SpareGpioOutput03B(self, SpareGpioOutput03B):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput03B, 30, 'B')

    @DebugIt()
    def get_SpareGpioOutput04A(self):
        return perseus_utils.read_direct(self.perseus, 31, 'A')

    @DebugIt()
    def set_SpareGpioOutput04A(self, SpareGpioOutput04A):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput04A, 31, 'A')

    @DebugIt()
    def get_SpareGpioOutput04B(self):
        return perseus_utils.read_direct(self.perseus, 31, 'B')

    @DebugIt()
    def set_SpareGpioOutput04B(self, SpareGpioOutput04B):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput04B, 31, 'B')

    @DebugIt()
    def get_FdlSwTriggerA(self):
        return perseus_utils.read_direct(self.perseus, 32, 'A')

    @DebugIt()
    def set_FdlSwTriggerA(self, FdlSwTriggerA):
        perseus_utils.write_direct(self.perseus, FdlSwTriggerA, 32, 'A')

    @DebugIt()
    def get_FdlSwTriggerB(self):
        return perseus_utils.read_direct(self.perseus, 32, 'B')

    @DebugIt()
    def set_FdlSwTriggerB(self, FdlSwTriggerB):
        perseus_utils.write_direct(self.perseus, FdlSwTriggerB, 32, 'B')

    @DebugIt()
    def get_SlowIqLoopEnableA(self):
        return perseus_utils.read_direct(self.perseus, 100, 'A')

    @DebugIt()
    def set_SlowIqLoopEnableA(self, SlowIqLoopEnableA):
        perseus_utils.write_direct(self.perseus, SlowIqLoopEnableA, 100, 'A')

    @DebugIt()
    def get_SlowIqLoopEnableB(self):
        return perseus_utils.read_direct(self.perseus, 100, 'B')

    @DebugIt()
    def set_SlowIqLoopEnableB(self, SlowIqLoopEnableB):
        perseus_utils.write_direct(self.perseus, SlowIqLoopEnableB, 100, 'B')

    @DebugIt()
    def get_AdcsPhaseshiftEnableA(self):
        return perseus_utils.read_direct(self.perseus, 101, 'A')

    @DebugIt()
    def set_AdcsPhaseshiftEnableA(self, AdcsPhaseshiftEnableA):
        perseus_utils.write_direct(self.perseus, AdcsPhaseshiftEnableA, 101, 'A')

    @DebugIt()
    def get_AdcsPhaseshiftEnableB(self):
        return perseus_utils.read_direct(self.perseus, 101, 'B')

    @DebugIt()
    def set_AdcsPhaseshiftEnableB(self, AdcsPhaseshiftEnableB):
        perseus_utils.write_direct(self.perseus, AdcsPhaseshiftEnableB, 101, 'B')

    @DebugIt()
    def get_DacsPhaseShiftEnableA(self):
        return perseus_utils.read_direct(self.perseus, 102, 'A')

    @DebugIt()
    def set_DacsPhaseShiftEnableA(self, DacsPhaseShiftEnableA):
        perseus_utils.write_direct(self.perseus, DacsPhaseShiftEnableA, 102, 'A')

    @DebugIt()
    def get_DacsPhaseShiftEnableB(self):
        return perseus_utils.read_direct(self.perseus, 102, 'B')

    @DebugIt()
    def set_DacsPhaseShiftEnableB(self, DacsPhaseShiftEnableB):
        perseus_utils.write_direct(self.perseus, DacsPhaseShiftEnableB, 102, 'B')

    @DebugIt()
    def get_SquarerefEnableA(self):
        return perseus_utils.read_direct(self.perseus, 103, 'A')

    @DebugIt()
    def set_SquarerefEnableA(self, SquarerefEnableA):
        perseus_utils.write_direct(self.perseus, SquarerefEnableA, 103, 'A')

    @DebugIt()
    def get_SquarerefEnableB(self):
        return perseus_utils.read_direct(self.perseus, 103, 'B')

    @DebugIt()
    def set_SquarerefEnableB(self, SquarerefEnableB):
        perseus_utils.write_direct(self.perseus, SquarerefEnableB, 103, 'B')

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

    @DebugIt()
    def get_LookRefA(self):
        return perseus_utils.read_direct(self.perseus, 106, 'A')

    @DebugIt()
    def set_LookRefA(self, LookRefA):
        perseus_utils.write_direct(self.perseus, LookRefA, 106, 'A')

    @DebugIt()
    def get_LookRefB(self):
        return perseus_utils.read_direct(self.perseus, 106, 'B')

    @DebugIt()
    def set_LookRefB(self, LookRefB):
        perseus_utils.write_direct(self.perseus, LookRefB, 106, 'B')

    @DebugIt()
    def get_QuadrantSelectionA(self):
        return perseus_utils.read_direct(self.perseus, 107, 'A')

    @DebugIt()
    def set_QuadrantSelectionA(self, QuadrantSelectionA):
        perseus_utils.write_direct(self.perseus, QuadrantSelectionA, 107, 'A')

    @DebugIt()
    def get_QuadrantSelectionB(self):
        return perseus_utils.read_direct(self.perseus, 107, 'B')

    @DebugIt()
    def set_QuadrantSelectionB(self, QuadrantSelectionB):
        perseus_utils.write_direct(self.perseus, QuadrantSelectionB, 107, 'B')

    @DebugIt()
    def get_SlowIqLoopInputSelectionA(self):
        return perseus_utils.read_direct(self.perseus, 110, 'A')

    @DebugIt()
    def set_SlowIqLoopInputSelectionA(self, SlowIqLoopInputSelectionA):
        perseus_utils.write_direct(self.perseus, SlowIqLoopInputSelectionA, 110, 'A')

    @DebugIt()
    def get_SlowIqLoopInputSelectionB(self):
        return perseus_utils.read_direct(self.perseus, 110, 'B')

    @DebugIt()
    def set_SlowIqLoopInputSelectionB(self, SlowIqLoopInputSelectionB):
        perseus_utils.write_direct(self.perseus, SlowIqLoopInputSelectionB, 110, 'B')

    @DebugIt()
    def get_FastIqLoopInputSelectionA(self):
        return perseus_utils.read_direct(self.perseus, 111, 'A')

    @DebugIt()
    def set_FastIqLoopInputSelectionA(self, FastIqLoopInputSelectionA):
        perseus_utils.write_direct(self.perseus, FastIqLoopInputSelectionA, 111, 'A')

    @DebugIt()
    def get_FastIqLoopInputSelectionB(self):
        return perseus_utils.read_direct(self.perseus, 111, 'B')

    @DebugIt()
    def set_FastIqLoopInputSelectionB(self, FastIqLoopInputSelectionB):
        perseus_utils.write_direct(self.perseus, FastIqLoopInputSelectionB, 111, 'B')

    @DebugIt()
    def get_AmplitudeLoopInputSelectionA(self):
        return perseus_utils.read_direct(self.perseus, 112, 'A')

    @DebugIt()
    def set_AmplitudeLoopInputSelectionA(self, AmplitudeLoopInputSelectionA):
        perseus_utils.write_direct(self.perseus, AmplitudeLoopInputSelectionA, 112, 'A')

    @DebugIt()
    def get_AmplitudeLoopInputSelectionB(self):
        return perseus_utils.read_direct(self.perseus, 112, 'B')

    @DebugIt()
    def set_AmplitudeLoopInputSelectionB(self, AmplitudeLoopInputSelectionB):
        perseus_utils.write_direct(self.perseus, AmplitudeLoopInputSelectionB, 112, 'B')

    @DebugIt()
    def get_PhaseLoopInputSelectionA(self):
        return perseus_utils.read_direct(self.perseus, 113, 'A')

    @DebugIt()
    def set_PhaseLoopInputSelectionA(self, PhaseLoopInputSelectionA):
        perseus_utils.write_direct(self.perseus, PhaseLoopInputSelectionA, 113, 'A')

    @DebugIt()
    def get_PhaseLoopInputSelectionB(self):
        return perseus_utils.read_direct(self.perseus, 113, 'B')

    @DebugIt()
    def set_PhaseLoopInputSelectionB(self, PhaseLoopInputSelectionB):
        perseus_utils.write_direct(self.perseus, PhaseLoopInputSelectionB, 113, 'B')

    @DebugIt()
    def get_PolarLoopsEnableA(self):
        return perseus_utils.read_direct(self.perseus, 114, 'A')

    @DebugIt()
    def set_PolarLoopsEnableA(self, PolarLoopsEnableA):
        perseus_utils.write_direct(self.perseus, PolarLoopsEnableA, 114, 'A')

    @DebugIt()
    def get_PolarLoopsEnableB(self):
        return perseus_utils.read_direct(self.perseus, 114, 'B')

    @DebugIt()
    def set_PolarLoopsEnableB(self, PolarLoopsEnableB):
        perseus_utils.write_direct(self.perseus, PolarLoopsEnableB, 114, 'B')

    @DebugIt()
    def get_FastIqLoopEnableA(self):
        return perseus_utils.read_direct(self.perseus, 115, 'A')

    @DebugIt()
    def set_FastIqLoopEnableA(self, FastIqLoopEnableA):
        perseus_utils.write_direct(self.perseus, FastIqLoopEnableA, 115, 'A')

    @DebugIt()
    def get_FastIqLoopEnableB(self):
        return perseus_utils.read_direct(self.perseus, 115, 'B')

    @DebugIt()
    def set_FastIqLoopEnableB(self, FastIqLoopEnableB):
        perseus_utils.write_direct(self.perseus, FastIqLoopEnableB, 115, 'B')

    @DebugIt()
    def get_AmplitudeLoopEnableA(self):
        return perseus_utils.read_direct(self.perseus, 116, 'A')

    @DebugIt()
    def set_AmplitudeLoopEnableA(self, AmplitudeLoopEnableA):
        perseus_utils.write_direct(self.perseus, AmplitudeLoopEnableA, 116, 'A')

    @DebugIt()
    def get_AmplitudeLoopEnableB(self):
        return perseus_utils.read_direct(self.perseus, 116, 'B')

    @DebugIt()
    def set_AmplitudeLoopEnableB(self, AmplitudeLoopEnableB):
        perseus_utils.write_direct(self.perseus, AmplitudeLoopEnableB, 116, 'B')

    @DebugIt()
    def get_PhaseLoopEnableA(self):
        return perseus_utils.read_direct(self.perseus, 117, 'A')

    @DebugIt()
    def set_PhaseLoopEnableA(self, PhaseLoopEnableA):
        perseus_utils.write_direct(self.perseus, PhaseLoopEnableA, 117, 'A')

    @DebugIt()
    def get_PhaseLoopEnableB(self):
        return perseus_utils.read_direct(self.perseus, 117, 'B')

    @DebugIt()
    def set_PhaseLoopEnableB(self, PhaseLoopEnableB):
        perseus_utils.write_direct(self.perseus, PhaseLoopEnableB, 117, 'B')

    @DebugIt()
    def get_KpFastIqLoopA(self):
        return perseus_utils.read_direct(self.perseus, 118, 'A')

    @DebugIt()
    def set_KpFastIqLoopA(self, KpFastIqLoopA):
        perseus_utils.write_direct(self.perseus, KpFastIqLoopA, 118, 'A')

    @DebugIt()
    def get_KpFastIqLoopB(self):
        return perseus_utils.read_direct(self.perseus, 118, 'B')

    @DebugIt()
    def set_KpFastIqLoopB(self, KpFastIqLoopB):
        perseus_utils.write_direct(self.perseus, KpFastIqLoopB, 118, 'B')

    @DebugIt()
    def get_KiFastIqLoopA(self):
        return perseus_utils.read_direct(self.perseus, 119, 'A')

    @DebugIt()
    def set_KiFastIqLoopA(self, KiFastIqLoopA):
        perseus_utils.write_direct(self.perseus, KiFastIqLoopA, 119, 'A')

    @DebugIt()
    def get_KiFastIqLoopB(self):
        return perseus_utils.read_direct(self.perseus, 119, 'B')

    @DebugIt()
    def set_KiFastIqLoopB(self, KiFastIqLoopB):
        perseus_utils.write_direct(self.perseus, KiFastIqLoopB, 119, 'B')

    @DebugIt()
    def get_KpAmpLoopA(self):
        return perseus_utils.read_direct(self.perseus, 120, 'A')

    @DebugIt()
    def set_KpAmpLoopA(self, KpAmpLoopA):
        perseus_utils.write_direct(self.perseus, KpAmpLoopA, 120, 'A')

    @DebugIt()
    def get_KpAmpLoopB(self):
        return perseus_utils.read_direct(self.perseus, 120, 'B')

    @DebugIt()
    def set_KpAmpLoopB(self, KpAmpLoopB):
        perseus_utils.write_direct(self.perseus, KpAmpLoopB, 120, 'B')

    @DebugIt()
    def get_KiAmpLoopA(self):
        return perseus_utils.read_direct(self.perseus, 121, 'A')

    @DebugIt()
    def set_KiAmpLoopA(self, KiAmpLoopA):
        perseus_utils.write_direct(self.perseus, KiAmpLoopA, 121, 'A')

    @DebugIt()
    def get_KiAmpLoopB(self):
        return perseus_utils.read_direct(self.perseus, 121, 'B')

    @DebugIt()
    def set_KiAmpLoopB(self, KiAmpLoopB):
        perseus_utils.write_direct(self.perseus, KiAmpLoopB, 121, 'B')

    @DebugIt()
    def get_KpPhaseLoopA(self):
        return perseus_utils.read_direct(self.perseus, 122, 'A')

    @DebugIt()
    def set_KpPhaseLoopA(self, KpPhaseLoopA):
        perseus_utils.write_direct(self.perseus, KpPhaseLoopA, 122, 'A')

    @DebugIt()
    def get_KpPhaseLoopB(self):
        return perseus_utils.read_direct(self.perseus, 122, 'B')

    @DebugIt()
    def set_KpPhaseLoopB(self, KpPhaseLoopB):
        perseus_utils.write_direct(self.perseus, KpPhaseLoopB, 122, 'B')

    @DebugIt()
    def get_KiPhaseLoopA(self):
        return perseus_utils.read_direct(self.perseus, 123, 'A')

    @DebugIt()
    def set_KiPhaseLoopA(self, KiPhaseLoopA):
        perseus_utils.write_direct(self.perseus, KiPhaseLoopA, 123, 'A')

    @DebugIt()
    def get_KiPhaseLoopB(self):
        return perseus_utils.read_direct(self.perseus, 123, 'B')

    @DebugIt()
    def set_KiPhaseLoopB(self, KiPhaseLoopB):
        perseus_utils.write_direct(self.perseus, KiPhaseLoopB, 123, 'B')

    @DebugIt()
    def get_PiLimitFastPiIqA(self):
        return perseus_utils.read_milivolts(self.perseus, 124, 'A')

    @DebugIt()
    def set_PiLimitFastPiIqA(self, PiLimitFastPiIqA):
        perseus_utils.write_milivolts(self.perseus, PiLimitFastPiIqA, 124, 'A')

    @DebugIt()
    def get_PiLimitFastPiIqB(self):
        return perseus_utils.read_milivolts(self.perseus, 124, 'B')

    @DebugIt()
    def set_PiLimitFastPiIqB(self, PiLimitFastPiIqB):
        perseus_utils.write_milivolts(self.perseus, PiLimitFastPiIqB, 124, 'B')

    @DebugIt()
    def get_PulseModeEnableA(self):
        return perseus_utils.read_direct(self.perseus, 200, 'A')

    @DebugIt()
    def set_PulseModeEnableA(self, PulseModeEnableA):
        perseus_utils.write_direct(self.perseus, PulseModeEnableA, 200, 'A')

    @DebugIt()
    def get_PulseModeEnableB(self):
        return perseus_utils.read_direct(self.perseus, 200, 'B')

    @DebugIt()
    def set_PulseModeEnableB(self, PulseModeEnableB):
        perseus_utils.write_direct(self.perseus, PulseModeEnableB, 200, 'B')

    @DebugIt()
    def get_AutomaticConditioningEnableA(self):
        return perseus_utils.read_direct(self.perseus, 201, 'A')

    @DebugIt()
    def set_AutomaticConditioningEnableA(self, AutomaticConditioningEnableA):
        perseus_utils.write_direct(self.perseus, AutomaticConditioningEnableA, 201, 'A')

    @DebugIt()
    def get_AutomaticConditioningEnableB(self):
        return perseus_utils.read_direct(self.perseus, 201, 'B')

    @DebugIt()
    def set_AutomaticConditioningEnableB(self, AutomaticConditioningEnableB):
        perseus_utils.write_direct(self.perseus, AutomaticConditioningEnableB, 201, 'B')

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

    @DebugIt()
    def get_TuningEnableA(self):
        return perseus_utils.read_direct(self.perseus, 300, 'A')

    @DebugIt()
    def set_TuningEnableA(self, TuningEnableA):
        perseus_utils.write_direct(self.perseus, TuningEnableA, 300, 'A')

    @DebugIt()
    def get_TuningEnableB(self):
        return perseus_utils.read_direct(self.perseus, 300, 'B')

    @DebugIt()
    def set_TuningEnableB(self, TuningEnableB):
        perseus_utils.write_direct(self.perseus, TuningEnableB, 300, 'B')

    @DebugIt()
    def get_TuningPosEnA(self):
        return perseus_utils.read_direct(self.perseus, 301, 'A')

    @DebugIt()
    def set_TuningPosEnA(self, TuningPosEnA):
        perseus_utils.write_direct(self.perseus, TuningPosEnA, 301, 'A')

    @DebugIt()
    def get_TuningPosEnB(self):
        return perseus_utils.read_direct(self.perseus, 301, 'B')

    @DebugIt()
    def set_TuningPosEnB(self, TuningPosEnB):
        perseus_utils.write_direct(self.perseus, TuningPosEnB, 301, 'B')

    @DebugIt()
    def get_NumStepsA(self):
        return perseus_utils.read_direct(self.perseus, 302, 'A')

    @DebugIt()
    def set_NumStepsA(self, NumStepsA):
        perseus_utils.write_direct(self.perseus, NumStepsA, 302, 'A')

    @DebugIt()
    def get_NumStepsB(self):
        return perseus_utils.read_direct(self.perseus, 302, 'B')

    @DebugIt()
    def set_NumStepsB(self, NumStepsB):
        perseus_utils.write_direct(self.perseus, NumStepsB, 302, 'B')

    @DebugIt()
    def get_PulsesFrequencyA(self):
        return perseus_utils.read_direct(self.perseus, 303, 'A')

    @DebugIt()
    def set_PulsesFrequencyA(self, PulsesFrequencyA):
        perseus_utils.write_direct(self.perseus, PulsesFrequencyA, 303, 'A')

    @DebugIt()
    def get_PulsesFrequencyB(self):
        return perseus_utils.read_direct(self.perseus, 303, 'B')

    @DebugIt()
    def set_PulsesFrequencyB(self, PulsesFrequencyB):
        perseus_utils.write_direct(self.perseus, PulsesFrequencyB, 303, 'B')

    @DebugIt()
    def get_PhaseOffsetA(self):
        return perseus_utils.read_angle(self.perseus, 304, 'A')

    @DebugIt()
    def set_PhaseOffsetA(self, PhaseOffsetA):
        perseus_utils.write_angle(self.perseus, PhaseOffsetA, 304, 'A')

    @DebugIt()
    def get_PhaseOffsetB(self):
        return perseus_utils.read_angle(self.perseus, 304, 'B')

    @DebugIt()
    def set_PhaseOffsetB(self, PhaseOffsetB):
        perseus_utils.write_angle(self.perseus, PhaseOffsetB, 304, 'B')

    @DebugIt()
    def get_MoveA(self):
        return perseus_utils.read_direct(self.perseus, 305, 'A')

    @DebugIt()
    def set_MoveA(self, MoveA):
        perseus_utils.write_direct(self.perseus, MoveA, 305, 'A')

    @DebugIt()
    def get_MoveB(self):
        return perseus_utils.read_direct(self.perseus, 305, 'B')

    @DebugIt()
    def set_MoveB(self, MoveB):
        perseus_utils.write_direct(self.perseus, MoveB, 305, 'B')

    @DebugIt()
    def get_MoveupA(self):
        return perseus_utils.read_direct(self.perseus, 306, 'A')

    @DebugIt()
    def set_MoveupA(self, MoveupA):
        perseus_utils.write_direct(self.perseus, MoveupA, 306, 'A')

    @DebugIt()
    def get_MoveupB(self):
        return perseus_utils.read_direct(self.perseus, 306, 'B')

    @DebugIt()
    def set_MoveupB(self, MoveupB):
        perseus_utils.write_direct(self.perseus, MoveupB, 306, 'B')

    @DebugIt()
    def get_TuningresetA(self):
        return perseus_utils.read_direct(self.perseus, 307, 'A')

    @DebugIt()
    def set_TuningresetA(self, TuningresetA):
        perseus_utils.write_direct(self.perseus, TuningresetA, 307, 'A')

    @DebugIt()
    def get_TuningresetB(self):
        return perseus_utils.read_direct(self.perseus, 307, 'B')

    @DebugIt()
    def set_TuningresetB(self, TuningresetB):
        perseus_utils.write_direct(self.perseus, TuningresetB, 307, 'B')

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

    @DebugIt()
    def get_MarginupA(self):
        return perseus_utils.read_angle(self.perseus, 309, 'A')

    @DebugIt()
    def set_MarginupA(self, MarginupA):
        perseus_utils.write_angle(self.perseus, MarginupA, 309, 'A')

    @DebugIt()
    def get_MarginupB(self):
        return perseus_utils.read_angle(self.perseus, 309, 'B')

    @DebugIt()
    def set_MarginupB(self, MarginupB):
        perseus_utils.write_angle(self.perseus, MarginupB, 309, 'B')

    @DebugIt()
    def get_MarginlowA(self):
        return perseus_utils.read_angle(self.perseus, 310, 'A')

    @DebugIt()
    def set_MarginlowA(self, MarginlowA):
        perseus_utils.write_angle(self.perseus, MarginlowA, 310, 'A')

    @DebugIt()
    def get_MarginlowB(self):
        return perseus_utils.read_angle(self.perseus, 310, 'B')

    @DebugIt()
    def set_MarginlowB(self, MarginlowB):
        perseus_utils.write_angle(self.perseus, MarginlowB, 310, 'B')

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

    @DebugIt()
    def get_TuningfilterenableA(self):
        return perseus_utils.read_direct(self.perseus, 312, 'A')

    @DebugIt()
    def set_TuningfilterenableA(self, TuningfilterenableA):
        perseus_utils.write_direct(self.perseus, TuningfilterenableA, 312, 'A')

    @DebugIt()
    def get_TuningfilterenableB(self):
        return perseus_utils.read_direct(self.perseus, 312, 'B')

    @DebugIt()
    def set_TuningfilterenableB(self, TuningfilterenableB):
        perseus_utils.write_direct(self.perseus, TuningfilterenableB, 312, 'B')

    @DebugIt()
    def get_TuningtriggerenableA(self):
        return perseus_utils.read_direct(self.perseus, 313, 'A')

    @DebugIt()
    def set_TuningtriggerenableA(self, TuningtriggerenableA):
        perseus_utils.write_direct(self.perseus, TuningtriggerenableA, 313, 'A')

    @DebugIt()
    def get_TuningtriggerenableB(self):
        return perseus_utils.read_direct(self.perseus, 313, 'B')

    @DebugIt()
    def set_TuningtriggerenableB(self, TuningtriggerenableB):
        perseus_utils.write_direct(self.perseus, TuningtriggerenableB, 313, 'B')

    @DebugIt()
    def get_EpsItckDisableA(self):
        return perseus_utils.read_direct(self.perseus, 400, 'A')

    @DebugIt()
    def set_EpsItckDisableA(self, EpsItckDisableA):
        perseus_utils.write_direct(self.perseus, EpsItckDisableA, 400, 'A')

    @DebugIt()
    def get_EpsItckDisableB(self):
        return perseus_utils.read_direct(self.perseus, 400, 'B')

    @DebugIt()
    def set_EpsItckDisableB(self, EpsItckDisableB):
        perseus_utils.write_direct(self.perseus, EpsItckDisableB, 400, 'B')

    @DebugIt()
    def get_FimItckDisableA(self):
        return perseus_utils.read_direct(self.perseus, 401, 'A')

    @DebugIt()
    def set_FimItckDisableA(self, FimItckDisableA):
        perseus_utils.write_direct(self.perseus, FimItckDisableA, 401, 'A')

    @DebugIt()
    def get_FimItckDisableB(self):
        return perseus_utils.read_direct(self.perseus, 401, 'B')

    @DebugIt()
    def set_FimItckDisableB(self, FimItckDisableB):
        perseus_utils.write_direct(self.perseus, FimItckDisableB, 401, 'B')

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

    @DebugIt()
    def get_MuxselA(self):
        return perseus_utils.read_direct(self.perseus, 502, 'A')

    @DebugIt()
    def set_MuxselA(self, MuxselA):
        perseus_utils.write_direct(self.perseus, MuxselA, 502, 'A')

    @DebugIt()
    def get_MuxselB(self):
        return perseus_utils.read_direct(self.perseus, 502, 'B')

    @DebugIt()
    def set_MuxselB(self, MuxselB):
        perseus_utils.write_direct(self.perseus, MuxselB, 502, 'B')

    @DebugIt()
    def get_Mux0DividerA(self):
        return perseus_utils.read_direct(self.perseus, 503, 'A')

    @DebugIt()
    def set_Mux0DividerA(self, Mux0DividerA):
        perseus_utils.write_direct(self.perseus, Mux0DividerA, 503, 'A')

    @DebugIt()
    def get_Mux0DividerB(self):
        return perseus_utils.read_direct(self.perseus, 503, 'B')

    @DebugIt()
    def set_Mux0DividerB(self, Mux0DividerB):
        perseus_utils.write_direct(self.perseus, Mux0DividerB, 503, 'B')

    @DebugIt()
    def get_Mux1DividerA(self):
        return perseus_utils.read_direct(self.perseus, 504, 'A')

    @DebugIt()
    def set_Mux1DividerA(self, Mux1DividerA):
        perseus_utils.write_direct(self.perseus, Mux1DividerA, 504, 'A')

    @DebugIt()
    def get_Mux1DividerB(self):
        return perseus_utils.read_direct(self.perseus, 504, 'B')

    @DebugIt()
    def set_Mux1DividerB(self, Mux1DividerB):
        perseus_utils.write_direct(self.perseus, Mux1DividerB, 504, 'B')

    @DebugIt()
    def get_Mux2DividerA(self):
        return perseus_utils.read_direct(self.perseus, 505, 'A')

    @DebugIt()
    def set_Mux2DividerA(self, Mux2DividerA):
        perseus_utils.write_direct(self.perseus, Mux2DividerA, 505, 'A')

    @DebugIt()
    def get_Mux2DividerB(self):
        return perseus_utils.read_direct(self.perseus, 505, 'B')

    @DebugIt()
    def set_Mux2DividerB(self, Mux2DividerB):
        perseus_utils.write_direct(self.perseus, Mux2DividerB, 505, 'B')

    @DebugIt()
    def get_Mux3DividerA(self):
        return perseus_utils.read_direct(self.perseus, 506, 'A')

    @DebugIt()
    def set_Mux3DividerA(self, Mux3DividerA):
        perseus_utils.write_direct(self.perseus, Mux3DividerA, 506, 'A')

    @DebugIt()
    def get_Mux3DividerB(self):
        return perseus_utils.read_direct(self.perseus, 506, 'B')

    @DebugIt()
    def set_Mux3DividerB(self, Mux3DividerB):
        perseus_utils.write_direct(self.perseus, Mux3DividerB, 506, 'B')

    @DebugIt()
    def get_Mux4DividerA(self):
        return perseus_utils.read_direct(self.perseus, 507, 'A')

    @DebugIt()
    def set_Mux4DividerA(self, Mux4DividerA):
        perseus_utils.write_direct(self.perseus, Mux4DividerA, 507, 'A')

    @DebugIt()
    def get_Mux4DividerB(self):
        return perseus_utils.read_direct(self.perseus, 507, 'B')

    @DebugIt()
    def set_Mux4DividerB(self, Mux4DividerB):
        perseus_utils.write_direct(self.perseus, Mux4DividerB, 507, 'B')

    @DebugIt()
    def get_SendWordA(self):
        return perseus_utils.read_direct(self.perseus, 508, 'A')

    @DebugIt()
    def set_SendWordA(self, SendWordA):
        perseus_utils.write_direct(self.perseus, SendWordA, 508, 'A')

    @DebugIt()
    def get_SendWordB(self):
        return perseus_utils.read_direct(self.perseus, 508, 'B')

    @DebugIt()
    def set_SendWordB(self, SendWordB):
        perseus_utils.write_direct(self.perseus, SendWordB, 508, 'B')

    @DebugIt()
    def get_CpdirA(self):
        return perseus_utils.read_direct(self.perseus, 509, 'A')

    @DebugIt()
    def set_CpdirA(self, CpdirA):
        perseus_utils.write_direct(self.perseus, CpdirA, 509, 'A')

    @DebugIt()
    def get_CpdirB(self):
        return perseus_utils.read_direct(self.perseus, 509, 'B')

    @DebugIt()
    def set_CpdirB(self, CpdirB):
        perseus_utils.write_direct(self.perseus, CpdirB, 509, 'B')

    @DebugIt()
    def get_VcxoOutputInversionA(self):
        return perseus_utils.read_direct(self.perseus, 510, 'A')

    @DebugIt()
    def set_VcxoOutputInversionA(self, VcxoOutputInversionA):
        perseus_utils.write_direct(self.perseus, VcxoOutputInversionA, 510, 'A')

    @DebugIt()
    def get_VcxoOutputInversionB(self):
        return perseus_utils.read_direct(self.perseus, 510, 'B')

    @DebugIt()
    def set_VcxoOutputInversionB(self, VcxoOutputInversionB):
        perseus_utils.write_direct(self.perseus, VcxoOutputInversionB, 510, 'B')

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
        self._Diag_IcavLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 0, 'B')
        self._Diag_QcavLoopsA = perseus_utils.read_diag_milivolts(self.perseus, 1, 'A')
        self._Diag_QcavLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 1, 'B')
        self._Diag_IcontrolA = perseus_utils.read_diag_milivolts(self.perseus, 2, 'A')
        self._Diag_IcontrolB = perseus_utils.read_diag_milivolts(self.perseus, 2, 'B')
        self._Diag_QcontrolA = perseus_utils.read_diag_milivolts(self.perseus, 3, 'A')
        self._Diag_QcontrolB = perseus_utils.read_diag_milivolts(self.perseus, 3, 'B')
        self._Diag_Icontrol1A = perseus_utils.read_diag_milivolts(self.perseus, 4, 'A')
        self._Diag_Icontrol1B = perseus_utils.read_diag_milivolts(self.perseus, 4, 'B')
        self._Diag_Qcontrol1A = perseus_utils.read_diag_milivolts(self.perseus, 5, 'A')
        self._Diag_Qcontrol1B = perseus_utils.read_diag_milivolts(self.perseus, 5, 'B')
        self._Diag_Icontrol2A = perseus_utils.read_diag_milivolts(self.perseus, 6, 'A')
        self._Diag_Icontrol2B = perseus_utils.read_diag_milivolts(self.perseus, 6, 'B')
        self._Diag_Qcontrol2A = perseus_utils.read_diag_milivolts(self.perseus, 7, 'A')
        self._Diag_Qcontrol2B = perseus_utils.read_diag_milivolts(self.perseus, 7, 'B')
        self._Diag_IerrorA = perseus_utils.read_diag_milivolts(self.perseus, 8, 'A')
        self._Diag_IerrorB = perseus_utils.read_diag_milivolts(self.perseus, 8, 'B')
        self._Diag_QerrorA = perseus_utils.read_diag_milivolts(self.perseus, 9, 'A')
        self._Diag_QerrorB = perseus_utils.read_diag_milivolts(self.perseus, 9, 'B')
        self._Diag_IerroraccumA = perseus_utils.read_diag_milivolts(self.perseus, 10, 'A')
        self._Diag_IerroraccumB = perseus_utils.read_diag_milivolts(self.perseus, 10, 'B')
        self._Diag_QerroraccumA = perseus_utils.read_diag_milivolts(self.perseus, 11, 'A')
        self._Diag_QerroraccumB = perseus_utils.read_diag_milivolts(self.perseus, 11, 'B')
        self._Diag_IrefA = perseus_utils.read_diag_milivolts(self.perseus, 12, 'A')
        self._Diag_IrefB = perseus_utils.read_diag_milivolts(self.perseus, 12, 'B')
        self._Diag_QrefA = perseus_utils.read_diag_milivolts(self.perseus, 13, 'A')
        self._Diag_QrefB = perseus_utils.read_diag_milivolts(self.perseus, 13, 'B')
        self._Diag_IFwCavLoopsA = perseus_utils.read_diag_milivolts(self.perseus, 14, 'A')
        self._Diag_IFwCavLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 14, 'B')
        self._Diag_QFwCavLoopsA = perseus_utils.read_diag_milivolts(self.perseus, 15, 'A')
        self._Diag_QFwCavLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 15, 'B')
        self._Diag_IFwTet1LoopsA = perseus_utils.read_diag_milivolts(self.perseus, 16, 'A')
        self._Diag_IFwTet1LoopsB = perseus_utils.read_diag_milivolts(self.perseus, 16, 'B')
        self._Diag_QFwTet1LoopsA = perseus_utils.read_diag_milivolts(self.perseus, 17, 'A')
        self._Diag_QFwTet1LoopsB = perseus_utils.read_diag_milivolts(self.perseus, 17, 'B')
        self._Diag_IFwTet2LoopsA = perseus_utils.read_diag_milivolts(self.perseus, 18, 'A')
        self._Diag_IFwTet2LoopsB = perseus_utils.read_diag_milivolts(self.perseus, 18, 'B')
        self._Diag_QFwTet2LoopsA = perseus_utils.read_diag_milivolts(self.perseus, 19, 'A')
        self._Diag_QFwTet2LoopsB = perseus_utils.read_diag_milivolts(self.perseus, 19, 'B')
        self._Diag_IFwCircInLoopsA = perseus_utils.read_diag_milivolts(self.perseus, 20, 'A')
        self._Diag_IFwCircInLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 20, 'B')
        self._Diag_QFwCircInLoopsA = perseus_utils.read_diag_milivolts(self.perseus, 21, 'A')
        self._Diag_QFwCircInLoopsB = perseus_utils.read_diag_milivolts(self.perseus, 21, 'B')
        self._Diag_ImoA = perseus_utils.read_diag_milivolts(self.perseus, 22, 'A')
        self._Diag_ImoB = perseus_utils.read_diag_milivolts(self.perseus, 22, 'B')
        self._Diag_QmoA = perseus_utils.read_diag_milivolts(self.perseus, 23, 'A')
        self._Diag_QmoB = perseus_utils.read_diag_milivolts(self.perseus, 23, 'B')
        self._Diag_Ispare1A = perseus_utils.read_diag_milivolts(self.perseus, 24, 'A')
        self._Diag_Ispare1B = perseus_utils.read_diag_milivolts(self.perseus, 24, 'B')
        self._Diag_Qspare1A = perseus_utils.read_diag_milivolts(self.perseus, 25, 'A')
        self._Diag_Qspare1B = perseus_utils.read_diag_milivolts(self.perseus, 25, 'B')
        self._Diag_Ispare2A = perseus_utils.read_diag_milivolts(self.perseus, 26, 'A')
        self._Diag_Ispare2B = perseus_utils.read_diag_milivolts(self.perseus, 26, 'B')
        self._Diag_Qspare2A = perseus_utils.read_diag_milivolts(self.perseus, 27, 'A')
        self._Diag_Qspare2B = perseus_utils.read_diag_milivolts(self.perseus, 27, 'B')
        self._Diag_IMuxCavA = perseus_utils.read_diag_milivolts(self.perseus, 28, 'A')
        self._Diag_IMuxCavB = perseus_utils.read_diag_milivolts(self.perseus, 28, 'B')
        self._Diag_QMuxCavA = perseus_utils.read_diag_milivolts(self.perseus, 29, 'A')
        self._Diag_QMuxCavB = perseus_utils.read_diag_milivolts(self.perseus, 29, 'B')
        self._Diag_IMuxFwCavA = perseus_utils.read_diag_milivolts(self.perseus, 30, 'A')
        self._Diag_IMuxFwCavB = perseus_utils.read_diag_milivolts(self.perseus, 30, 'B')
        self._Diag_QMuxFwCavA = perseus_utils.read_diag_milivolts(self.perseus, 31, 'A')
        self._Diag_QMuxFwCavB = perseus_utils.read_diag_milivolts(self.perseus, 31, 'B')
        self._Diag_IMuxFwTet1A = perseus_utils.read_diag_milivolts(self.perseus, 32, 'A')
        self._Diag_IMuxFwTet1B = perseus_utils.read_diag_milivolts(self.perseus, 32, 'B')
        self._Diag_QMuxFwTet1A = perseus_utils.read_diag_milivolts(self.perseus, 33, 'A')
        self._Diag_QMuxFwTet1B = perseus_utils.read_diag_milivolts(self.perseus, 33, 'B')
        self._Diag_IMuxFwTet2A = perseus_utils.read_diag_milivolts(self.perseus, 34, 'A')
        self._Diag_IMuxFwTet2B = perseus_utils.read_diag_milivolts(self.perseus, 34, 'B')
        self._Diag_QMuxFwTet2A = perseus_utils.read_diag_milivolts(self.perseus, 35, 'A')
        self._Diag_QMuxFwTet2B = perseus_utils.read_diag_milivolts(self.perseus, 35, 'B')
        self._Diag_IMuxFwCircInA = perseus_utils.read_diag_milivolts(self.perseus, 36, 'A')
        self._Diag_IMuxFwCircInB = perseus_utils.read_diag_milivolts(self.perseus, 36, 'B')
        self._Diag_QMuxFwCircInA = perseus_utils.read_diag_milivolts(self.perseus, 37, 'A')
        self._Diag_QMuxFwCircInB = perseus_utils.read_diag_milivolts(self.perseus, 37, 'B')
        self._Diag_AmpCavA = perseus_utils.read_diag_milivolts(self.perseus, 38, 'A')
        self._Diag_AmpCavB = perseus_utils.read_diag_milivolts(self.perseus, 38, 'B')
        self._Diag_AmpFwA = perseus_utils.read_diag_milivolts(self.perseus, 39, 'A')
        self._Diag_AmpFwB = perseus_utils.read_diag_milivolts(self.perseus, 39, 'B')
        self._Diag_AngCavFwA = perseus_utils.read_diag_angle(self.perseus, 40, 'A')
        self._Diag_AngCavFwB = perseus_utils.read_diag_angle(self.perseus, 40, 'B')
        self._Diag_AngCavLA = perseus_utils.read_diag_angle(self.perseus, 41, 'A')
        self._Diag_AngCavLB = perseus_utils.read_diag_angle(self.perseus, 41, 'B')
        self._Diag_AngFwLA = perseus_utils.read_diag_angle(self.perseus, 42, 'A')
        self._Diag_AngFwLB = perseus_utils.read_diag_angle(self.perseus, 42, 'B')
        self._Diag_Vaccum1A = bool(perseus_utils.read_diag_direct(self.perseus, 43, 'A'))
        self._Diag_Vaccum1B = bool(perseus_utils.read_diag_direct(self.perseus, 43, 'B'))
        self._Diag_Vaccum2A = bool(perseus_utils.read_diag_direct(self.perseus, 44, 'A'))
        self._Diag_Vaccum2B = bool(perseus_utils.read_diag_direct(self.perseus, 44, 'B'))
        self._Diag_IcontrolSlowpiA = perseus_utils.read_diag_milivolts(self.perseus, 45, 'A')
        self._Diag_IcontrolSlowpiB = perseus_utils.read_diag_milivolts(self.perseus, 45, 'B')
        self._Diag_QcontrolSlowpiA = perseus_utils.read_diag_milivolts(self.perseus, 46, 'A')
        self._Diag_QcontrolSlowpiB = perseus_utils.read_diag_milivolts(self.perseus, 46, 'B')
        self._Diag_IcontrolFastpiA = perseus_utils.read_diag_milivolts(self.perseus, 47, 'A')
        self._Diag_IcontrolFastpiB = perseus_utils.read_diag_milivolts(self.perseus, 47, 'B')
        self._Diag_QcontrolFastpiA = perseus_utils.read_diag_milivolts(self.perseus, 48, 'A')
        self._Diag_QcontrolFastpiB = perseus_utils.read_diag_milivolts(self.perseus, 48, 'B')
        self._Diag_VcxoPoweredA = bool(perseus_utils.read_diag_direct(self.perseus, 50, 'A'))
        self._Diag_VcxoPoweredB = bool(perseus_utils.read_diag_direct(self.perseus, 50, 'B'))
        self._Diag_VcxoRefA = bool(perseus_utils.read_diag_direct(self.perseus, 51, 'A'))
        self._Diag_VcxoRefB = bool(perseus_utils.read_diag_direct(self.perseus, 51, 'B'))
        self._Diag_VcxoLockedA = bool(perseus_utils.read_diag_direct(self.perseus, 52, 'A'))
        self._Diag_VcxoLockedB = bool(perseus_utils.read_diag_direct(self.perseus, 52, 'B'))
        self._Diag_VcxoCableDisconnectedA = bool(perseus_utils.read_diag_direct(self.perseus, 53, 'A'))
        self._Diag_VcxoCableDisconnectedB = bool(perseus_utils.read_diag_direct(self.perseus, 53, 'B'))
        self._Diag_IpolarForAmplitudeLoopA = perseus_utils.read_diag_milivolts(self.perseus, 100, 'A')
        self._Diag_IpolarForAmplitudeLoopB = perseus_utils.read_diag_milivolts(self.perseus, 100, 'B')
        self._Diag_QpolarForAmplitudeLoopA = perseus_utils.read_diag_milivolts(self.perseus, 101, 'A')
        self._Diag_QpolarForAmplitudeLoopB = perseus_utils.read_diag_milivolts(self.perseus, 101, 'B')
        self._Diag_IpolarForPhaseLoopA = perseus_utils.read_diag_milivolts(self.perseus, 102, 'A')
        self._Diag_IpolarForPhaseLoopB = perseus_utils.read_diag_milivolts(self.perseus, 102, 'B')
        self._Diag_QpolarForPhaseLoopA = perseus_utils.read_diag_milivolts(self.perseus, 103, 'A')
        self._Diag_QpolarForPhaseLoopB = perseus_utils.read_diag_milivolts(self.perseus, 103, 'B')
        self._Diag_AmpInputOfAmpLoopA = perseus_utils.read_diag_milivolts(self.perseus, 104, 'A')
        self._Diag_AmpInputOfAmpLoopB = perseus_utils.read_diag_milivolts(self.perseus, 104, 'B')
        self._Diag_PhaseInputOfAmpLoopA = perseus_utils.read_diag_milivolts(self.perseus, 105, 'A')
        self._Diag_PhaseInputOfAmpLoopB = perseus_utils.read_diag_milivolts(self.perseus, 105, 'B')
        self._Diag_AmpInputOfPhaseLoopA = perseus_utils.read_diag_milivolts(self.perseus, 106, 'A')
        self._Diag_AmpInputOfPhaseLoopB = perseus_utils.read_diag_milivolts(self.perseus, 106, 'B')
        self._Diag_PhInputOfPhaseLoopA = perseus_utils.read_diag_milivolts(self.perseus, 107, 'A')
        self._Diag_PhInputOfPhaseLoopB = perseus_utils.read_diag_milivolts(self.perseus, 107, 'B')
        self._Diag_AmpLoopControlOutputA = perseus_utils.read_diag_milivolts(self.perseus, 108, 'A')
        self._Diag_AmpLoopControlOutputB = perseus_utils.read_diag_milivolts(self.perseus, 108, 'B')
        self._Diag_AmpLoopErrorA = perseus_utils.read_diag_milivolts(self.perseus, 109, 'A')
        self._Diag_AmpLoopErrorB = perseus_utils.read_diag_milivolts(self.perseus, 109, 'B')
        self._Diag_AmpLoopErrorAccumA = perseus_utils.read_diag_milivolts(self.perseus, 110, 'A')
        self._Diag_AmpLoopErrorAccumB = perseus_utils.read_diag_milivolts(self.perseus, 110, 'B')
        self._Diag_PhLoopControlOutputA = perseus_utils.read_diag_milivolts(self.perseus, 111, 'A')
        self._Diag_PhLoopControlOutputB = perseus_utils.read_diag_milivolts(self.perseus, 111, 'B')
        self._Diag_PhLoopErrorA = perseus_utils.read_diag_milivolts(self.perseus, 112, 'A')
        self._Diag_PhLoopErrorB = perseus_utils.read_diag_milivolts(self.perseus, 112, 'B')
        self._Diag_PhLoopErrorAccumA = perseus_utils.read_diag_milivolts(self.perseus, 113, 'A')
        self._Diag_PhLoopErrorAccumB = perseus_utils.read_diag_milivolts(self.perseus, 113, 'B')
        self._Diag_IpolarControlOutputA = perseus_utils.read_diag_milivolts(self.perseus, 114, 'A')
        self._Diag_IpolarControlOutputB = perseus_utils.read_diag_milivolts(self.perseus, 114, 'B')
        self._Diag_QpolarControlOutputA = perseus_utils.read_diag_milivolts(self.perseus, 115, 'A')
        self._Diag_QpolarControlOutputB = perseus_utils.read_diag_milivolts(self.perseus, 115, 'B')
        self._Diag_IcontrolSlowpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 116, 'A')
        self._Diag_IcontrolSlowpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 116, 'B')
        self._Diag_QcontrolSlowpiqA = perseus_utils.read_diag_milivolts(self.perseus, 117, 'A')
        self._Diag_QcontrolSlowpiqB = perseus_utils.read_diag_milivolts(self.perseus, 117, 'B')
        self._Diag_IcontrolFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 118, 'A')
        self._Diag_IcontrolFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 118, 'B')
        self._Diag_QcontrolFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 119, 'A')
        self._Diag_QcontrolFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 119, 'B')
        self._Diag_IloopinputSlowpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 120, 'A')
        self._Diag_IloopinputSlowpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 120, 'B')
        self._Diag_QloopinputSlowpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 121, 'A')
        self._Diag_QloopinputSlowpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 121, 'B')
        self._Diag_IloopinputFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 122, 'A')
        self._Diag_IloopinputFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 122, 'B')
        self._Diag_QloopinputFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 123, 'A')
        self._Diag_QloopinputFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 123, 'B')
        self._Diag_IrefloopinputFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 124, 'A')
        self._Diag_IrefloopinputFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 124, 'B')
        self._Diag_QrefloopinputFastpiIqA = perseus_utils.read_diag_milivolts(self.perseus, 125, 'A')
        self._Diag_QrefloopinputFastpiIqB = perseus_utils.read_diag_milivolts(self.perseus, 125, 'B')
        self._Diag_MovingPlungerAutoA = bool(perseus_utils.read_diag_direct(self.perseus, 300, 'A'))
        self._Diag_MovingPlungerAutoB = bool(perseus_utils.read_diag_direct(self.perseus, 300, 'B'))
        self._Diag_FreqUpA = bool(perseus_utils.read_diag_direct(self.perseus, 301, 'A'))
        self._Diag_FreqUpB = bool(perseus_utils.read_diag_direct(self.perseus, 301, 'B'))
        self._Diag_ManualTuningOnA = bool(perseus_utils.read_diag_direct(self.perseus, 302, 'A'))
        self._Diag_ManualTuningOnB = bool(perseus_utils.read_diag_direct(self.perseus, 302, 'B'))
        self._Diag_ManualTuningFreqUpA = bool(perseus_utils.read_diag_direct(self.perseus, 303, 'A'))
        self._Diag_ManualTuningFreqUpB = bool(perseus_utils.read_diag_direct(self.perseus, 303, 'B'))
        self._Diag_FwminA = bool(perseus_utils.read_diag_direct(self.perseus, 307, 'A'))
        self._Diag_FwminB = bool(perseus_utils.read_diag_direct(self.perseus, 307, 'B'))
        self._Diag_EpsItckDelayA = bool(perseus_utils.read_diag_direct(self.perseus, 400, 'A'))
        self._Diag_EpsItckDelayB = bool(perseus_utils.read_diag_direct(self.perseus, 400, 'B'))
        self._Diag_FimItckDelayA = bool(perseus_utils.read_diag_direct(self.perseus, 401, 'A'))
        self._Diag_FimItckDelayB = bool(perseus_utils.read_diag_direct(self.perseus, 401, 'B'))
        self._Diag_FdlTrigHwInputA = bool(perseus_utils.read_diag_direct(self.perseus, 402, 'A'))
        self._Diag_FdlTrigHwInputB = bool(perseus_utils.read_diag_direct(self.perseus, 402, 'B'))
        self._Diag_FdlTrigSwInputA = bool(perseus_utils.read_diag_direct(self.perseus, 403, 'A'))
        self._Diag_FdlTrigSwInputB = bool(perseus_utils.read_diag_direct(self.perseus, 403, 'B'))
        self._Diag_AmpMuxfwcircina = math.sqrt((self._Diag_IMuxFwCircInA**2) + (self._Diag_QMuxFwCircInA**2))
        self._Diag_AmpSpare1a = math.sqrt((self._Diag_Ispare1A**2) + (self._Diag_Qspare1A**2))
        self._Diag_AmpMuxfwcircinb = math.sqrt((self._Diag_IMuxFwCircInB**2) + (self._Diag_QMuxFwCircInB**2))
        self._Diag_AmpSpare2a = math.sqrt((self._Diag_Ispare2A**2) + (self._Diag_Qspare2A**2))
        self._Diag_AmpSpare2b = math.sqrt((self._Diag_Ispare2B**2) + (self._Diag_Qspare2B**2))
        self._Diag_AmpErrora = math.sqrt((self._Diag_IerrorA**2) + (self._Diag_QerrorA**2))
        self._Diag_AmpErrorb = math.sqrt((self._Diag_IerrorB**2) + (self._Diag_QerrorB**2))
        self._Diag_AmpSpare1b = math.sqrt((self._Diag_Ispare1B**2) + (self._Diag_Qspare1B**2))
        self._Diag_AmpErroraccumb = math.sqrt((self._Diag_IerroraccumB**2) + (self._Diag_QerroraccumB**2))
        self._Diag_AmpErroraccuma = math.sqrt((self._Diag_IerroraccumA**2) + (self._Diag_QerroraccumA**2))
        self._Diag_AmpControlfastpiiqb = math.sqrt((self._Diag_IcontrolFastpiIqB**2) + (self._Diag_QcontrolFastpiIqB**2))
        self._Diag_AmpControlfastpiiqa = math.sqrt((self._Diag_IcontrolFastpiIqA**2) + (self._Diag_QcontrolFastpiIqA**2))
        self._Diag_AmpControla = math.sqrt((self._Diag_IcontrolA**2) + (self._Diag_QcontrolA**2))
        self._Diag_AmpPolarforamplitudeloopa = math.sqrt((self._Diag_IpolarForAmplitudeLoopA**2) + (self._Diag_QpolarForAmplitudeLoopA**2))
        self._Diag_AmpPolarforamplitudeloopb = math.sqrt((self._Diag_IpolarForAmplitudeLoopB**2) + (self._Diag_QpolarForAmplitudeLoopB**2))
        self._Diag_AmpControlb = math.sqrt((self._Diag_IcontrolB**2) + (self._Diag_QcontrolB**2))
        self._Diag_AmpMuxfwtet2b = math.sqrt((self._Diag_IMuxFwTet2B**2) + (self._Diag_QMuxFwTet2B**2))
        self._Diag_AmpLoopinputfastpiiqb = math.sqrt((self._Diag_IloopinputFastpiIqB**2) + (self._Diag_QloopinputFastpiIqB**2))
        self._Diag_AmpLoopinputfastpiiqa = math.sqrt((self._Diag_IloopinputFastpiIqA**2) + (self._Diag_QloopinputFastpiIqA**2))
        self._Diag_AmpRefa = math.sqrt((self._Diag_IrefA**2) + (self._Diag_QrefA**2))
        self._Diag_AmpMuxfwcava = math.sqrt((self._Diag_IMuxFwCavA**2) + (self._Diag_QMuxFwCavA**2))
        self._Diag_AmpMuxfwcavb = math.sqrt((self._Diag_IMuxFwCavB**2) + (self._Diag_QMuxFwCavB**2))
        self._Diag_AmpRefb = math.sqrt((self._Diag_IrefB**2) + (self._Diag_QrefB**2))
        self._Diag_AmpControl2a = math.sqrt((self._Diag_Icontrol2A**2) + (self._Diag_Qcontrol2A**2))
        self._Diag_AmpControl2b = math.sqrt((self._Diag_Icontrol2B**2) + (self._Diag_Qcontrol2B**2))
        self._Diag_AmpFwtet1loopsb = math.sqrt((self._Diag_IFwTet1LoopsB**2) + (self._Diag_QFwTet1LoopsB**2))
        self._Diag_AmpFwtet1loopsa = math.sqrt((self._Diag_IFwTet1LoopsA**2) + (self._Diag_QFwTet1LoopsA**2))
        self._Diag_AmpPolarforphaseloopb = math.sqrt((self._Diag_IpolarForPhaseLoopB**2) + (self._Diag_QpolarForPhaseLoopB**2))
        self._Diag_AmpPolarforphaseloopa = math.sqrt((self._Diag_IpolarForPhaseLoopA**2) + (self._Diag_QpolarForPhaseLoopA**2))
        self._Diag_AmpPolarcontroloutputb = math.sqrt((self._Diag_IpolarControlOutputB**2) + (self._Diag_QpolarControlOutputB**2))
        self._Diag_AmpPolarcontroloutputa = math.sqrt((self._Diag_IpolarControlOutputA**2) + (self._Diag_QpolarControlOutputA**2))
        self._Diag_AmpFwtet2loopsa = math.sqrt((self._Diag_IFwTet2LoopsA**2) + (self._Diag_QFwTet2LoopsA**2))
        self._Diag_AmpCavloopsa = math.sqrt((self._Diag_IcavLoopsA**2) + (self._Diag_QcavLoopsA**2))
        self._Diag_AmpCavloopsb = math.sqrt((self._Diag_IcavLoopsB**2) + (self._Diag_QcavLoopsB**2))
        self._Diag_AmpFwtet2loopsb = math.sqrt((self._Diag_IFwTet2LoopsB**2) + (self._Diag_QFwTet2LoopsB**2))
        self._Diag_AmpLoopinputslowpiiqa = math.sqrt((self._Diag_IloopinputSlowpiIqA**2) + (self._Diag_QloopinputSlowpiIqA**2))
        self._Diag_AmpLoopinputslowpiiqb = math.sqrt((self._Diag_IloopinputSlowpiIqB**2) + (self._Diag_QloopinputSlowpiIqB**2))
        self._Diag_AmpRefloopinputfastpiiqb = math.sqrt((self._Diag_IrefloopinputFastpiIqB**2) + (self._Diag_QrefloopinputFastpiIqB**2))
        self._Diag_AmpRefloopinputfastpiiqa = math.sqrt((self._Diag_IrefloopinputFastpiIqA**2) + (self._Diag_QrefloopinputFastpiIqA**2))
        self._Diag_AmpControl1a = math.sqrt((self._Diag_Icontrol1A**2) + (self._Diag_Qcontrol1A**2))
        self._Diag_AmpControl1b = math.sqrt((self._Diag_Icontrol1B**2) + (self._Diag_Qcontrol1B**2))
        self._Diag_AmpMuxfwtet2a = math.sqrt((self._Diag_IMuxFwTet2A**2) + (self._Diag_QMuxFwTet2A**2))
        self._Diag_AmpMuxcavb = math.sqrt((self._Diag_IMuxCavB**2) + (self._Diag_QMuxCavB**2))
        self._Diag_AmpMuxcava = math.sqrt((self._Diag_IMuxCavA**2) + (self._Diag_QMuxCavA**2))
        self._Diag_AmpMuxfwtet1b = math.sqrt((self._Diag_IMuxFwTet1B**2) + (self._Diag_QMuxFwTet1B**2))
        self._Diag_AmpControlfastpib = math.sqrt((self._Diag_IcontrolFastpiB**2) + (self._Diag_QcontrolFastpiB**2))
        self._Diag_AmpFwcircinloopsa = math.sqrt((self._Diag_IFwCircInLoopsA**2) + (self._Diag_QFwCircInLoopsA**2))
        self._Diag_AmpFwcircinloopsb = math.sqrt((self._Diag_IFwCircInLoopsB**2) + (self._Diag_QFwCircInLoopsB**2))
        self._Diag_AmpControlfastpia = math.sqrt((self._Diag_IcontrolFastpiA**2) + (self._Diag_QcontrolFastpiA**2))
        self._Diag_AmpFwcavloopsa = math.sqrt((self._Diag_IFwCavLoopsA**2) + (self._Diag_QFwCavLoopsA**2))
        self._Diag_AmpMuxfwtet1a = math.sqrt((self._Diag_IMuxFwTet1A**2) + (self._Diag_QMuxFwTet1A**2))
        self._Diag_AmpFwcavloopsb = math.sqrt((self._Diag_IFwCavLoopsB**2) + (self._Diag_QFwCavLoopsB**2))
        self._Diag_AmpMob = math.sqrt((self._Diag_ImoB**2) + (self._Diag_QmoB**2))
        self._Diag_AmpMoa = math.sqrt((self._Diag_ImoA**2) + (self._Diag_QmoA**2))
        self._Diag_AmpControlslowpia = math.sqrt((self._Diag_IcontrolSlowpiA**2) + (self._Diag_QcontrolSlowpiA**2))
        self._Diag_AmpControlslowpib = math.sqrt((self._Diag_IcontrolSlowpiB**2) + (self._Diag_QcontrolSlowpiB**2))
        self._Diag_PhMuxfwcircina = math.degrees(math.atan2(self._Diag_QMuxFwCircInA, self._Diag_IMuxFwCircInA))
        self._Diag_PhSpare1a = math.degrees(math.atan2(self._Diag_Qspare1A, self._Diag_Ispare1A))
        self._Diag_PhMuxfwcircinb = math.degrees(math.atan2(self._Diag_QMuxFwCircInB, self._Diag_IMuxFwCircInB))
        self._Diag_PhSpare2a = math.degrees(math.atan2(self._Diag_Qspare2A, self._Diag_Ispare2A))
        self._Diag_PhSpare2b = math.degrees(math.atan2(self._Diag_Qspare2B, self._Diag_Ispare2B))
        self._Diag_PhErrora = math.degrees(math.atan2(self._Diag_QerrorA, self._Diag_IerrorA))
        self._Diag_PhErrorb = math.degrees(math.atan2(self._Diag_QerrorB, self._Diag_IerrorB))
        self._Diag_PhSpare1b = math.degrees(math.atan2(self._Diag_Qspare1B, self._Diag_Ispare1B))
        self._Diag_PhErroraccumb = math.degrees(math.atan2(self._Diag_QerroraccumB, self._Diag_IerroraccumB))
        self._Diag_PhErroraccuma = math.degrees(math.atan2(self._Diag_QerroraccumA, self._Diag_IerroraccumA))
        self._Diag_PhControlfastpiiqb = math.degrees(math.atan2(self._Diag_QcontrolFastpiIqB, self._Diag_IcontrolFastpiIqB))
        self._Diag_PhControlfastpiiqa = math.degrees(math.atan2(self._Diag_QcontrolFastpiIqA, self._Diag_IcontrolFastpiIqA))
        self._Diag_PhControla = math.degrees(math.atan2(self._Diag_QcontrolA, self._Diag_IcontrolA))
        self._Diag_PhPolarforamplitudeloopa = math.degrees(math.atan2(self._Diag_QpolarForAmplitudeLoopA, self._Diag_IpolarForAmplitudeLoopA))
        self._Diag_PhPolarforamplitudeloopb = math.degrees(math.atan2(self._Diag_QpolarForAmplitudeLoopB, self._Diag_IpolarForAmplitudeLoopB))
        self._Diag_PhControlb = math.degrees(math.atan2(self._Diag_QcontrolB, self._Diag_IcontrolB))
        self._Diag_PhMuxfwtet2b = math.degrees(math.atan2(self._Diag_QMuxFwTet2B, self._Diag_IMuxFwTet2B))
        self._Diag_PhLoopinputfastpiiqb = math.degrees(math.atan2(self._Diag_QloopinputFastpiIqB, self._Diag_IloopinputFastpiIqB))
        self._Diag_PhLoopinputfastpiiqa = math.degrees(math.atan2(self._Diag_QloopinputFastpiIqA, self._Diag_IloopinputFastpiIqA))
        self._Diag_PhRefa = math.degrees(math.atan2(self._Diag_QrefA, self._Diag_IrefA))
        self._Diag_PhMuxfwcava = math.degrees(math.atan2(self._Diag_QMuxFwCavA, self._Diag_IMuxFwCavA))
        self._Diag_PhMuxfwcavb = math.degrees(math.atan2(self._Diag_QMuxFwCavB, self._Diag_IMuxFwCavB))
        self._Diag_PhRefb = math.degrees(math.atan2(self._Diag_QrefB, self._Diag_IrefB))
        self._Diag_PhControl2a = math.degrees(math.atan2(self._Diag_Qcontrol2A, self._Diag_Icontrol2A))
        self._Diag_PhControl2b = math.degrees(math.atan2(self._Diag_Qcontrol2B, self._Diag_Icontrol2B))
        self._Diag_PhFwtet1loopsb = math.degrees(math.atan2(self._Diag_QFwTet1LoopsB, self._Diag_IFwTet1LoopsB))
        self._Diag_PhFwtet1loopsa = math.degrees(math.atan2(self._Diag_QFwTet1LoopsA, self._Diag_IFwTet1LoopsA))
        self._Diag_PhPolarforphaseloopb = math.degrees(math.atan2(self._Diag_QpolarForPhaseLoopB, self._Diag_IpolarForPhaseLoopB))
        self._Diag_PhPolarforphaseloopa = math.degrees(math.atan2(self._Diag_QpolarForPhaseLoopA, self._Diag_IpolarForPhaseLoopA))
        self._Diag_PhPolarcontroloutputb = math.degrees(math.atan2(self._Diag_QpolarControlOutputB, self._Diag_IpolarControlOutputB))
        self._Diag_PhPolarcontroloutputa = math.degrees(math.atan2(self._Diag_QpolarControlOutputA, self._Diag_IpolarControlOutputA))
        self._Diag_PhFwtet2loopsa = math.degrees(math.atan2(self._Diag_QFwTet2LoopsA, self._Diag_IFwTet2LoopsA))
        self._Diag_PhCavloopsa = math.degrees(math.atan2(self._Diag_QcavLoopsA, self._Diag_IcavLoopsA))
        self._Diag_PhCavloopsb = math.degrees(math.atan2(self._Diag_QcavLoopsB, self._Diag_IcavLoopsB))
        self._Diag_PhFwtet2loopsb = math.degrees(math.atan2(self._Diag_QFwTet2LoopsB, self._Diag_IFwTet2LoopsB))
        self._Diag_PhLoopinputslowpiiqa = math.degrees(math.atan2(self._Diag_QloopinputSlowpiIqA, self._Diag_IloopinputSlowpiIqA))
        self._Diag_PhLoopinputslowpiiqb = math.degrees(math.atan2(self._Diag_QloopinputSlowpiIqB, self._Diag_IloopinputSlowpiIqB))
        self._Diag_PhRefloopinputfastpiiqb = math.degrees(math.atan2(self._Diag_QrefloopinputFastpiIqB, self._Diag_IrefloopinputFastpiIqB))
        self._Diag_PhRefloopinputfastpiiqa = math.degrees(math.atan2(self._Diag_QrefloopinputFastpiIqA, self._Diag_IrefloopinputFastpiIqA))
        self._Diag_PhControl1a = math.degrees(math.atan2(self._Diag_Qcontrol1A, self._Diag_Icontrol1A))
        self._Diag_PhControl1b = math.degrees(math.atan2(self._Diag_Qcontrol1B, self._Diag_Icontrol1B))
        self._Diag_PhMuxfwtet2a = math.degrees(math.atan2(self._Diag_QMuxFwTet2A, self._Diag_IMuxFwTet2A))
        self._Diag_PhMuxcavb = math.degrees(math.atan2(self._Diag_QMuxCavB, self._Diag_IMuxCavB))
        self._Diag_PhMuxcava = math.degrees(math.atan2(self._Diag_QMuxCavA, self._Diag_IMuxCavA))
        self._Diag_PhMuxfwtet1b = math.degrees(math.atan2(self._Diag_QMuxFwTet1B, self._Diag_IMuxFwTet1B))
        self._Diag_PhControlfastpib = math.degrees(math.atan2(self._Diag_QcontrolFastpiB, self._Diag_IcontrolFastpiB))
        self._Diag_PhFwcircinloopsa = math.degrees(math.atan2(self._Diag_QFwCircInLoopsA, self._Diag_IFwCircInLoopsA))
        self._Diag_PhFwcircinloopsb = math.degrees(math.atan2(self._Diag_QFwCircInLoopsB, self._Diag_IFwCircInLoopsB))
        self._Diag_PhControlfastpia = math.degrees(math.atan2(self._Diag_QcontrolFastpiA, self._Diag_IcontrolFastpiA))
        self._Diag_PhFwcavloopsa = math.degrees(math.atan2(self._Diag_QFwCavLoopsA, self._Diag_IFwCavLoopsA))
        self._Diag_PhMuxfwtet1a = math.degrees(math.atan2(self._Diag_QMuxFwTet1A, self._Diag_IMuxFwTet1A))
        self._Diag_PhFwcavloopsb = math.degrees(math.atan2(self._Diag_QFwCavLoopsB, self._Diag_IFwCavLoopsB))
        self._Diag_PhMob = math.degrees(math.atan2(self._Diag_QmoB, self._Diag_ImoB))
        self._Diag_PhMoa = math.degrees(math.atan2(self._Diag_QmoA, self._Diag_ImoA))
        self._Diag_PhControlslowpia = math.degrees(math.atan2(self._Diag_QcontrolSlowpiA, self._Diag_IcontrolSlowpiA))
        self._Diag_PhControlslowpib = math.degrees(math.atan2(self._Diag_QcontrolSlowpiB, self._Diag_IcontrolSlowpiB))

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
