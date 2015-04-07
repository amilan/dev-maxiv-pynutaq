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

__all__ = ["Nutaq", "run"]

__author__ = 'antmil'

__docformat__ = 'restructuredtext'

# standard library imports
import time
import numpy
import math

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
    raise


class Nutaq(Device):
    __metaclass__ = DeviceMeta

    KpA = attribute(label='KpA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=10,
                                   fget="get_KpA",
                                   fset="set_KpA",
                                   doc=""
                                   )

    KiA = attribute(label='KiA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_KiA",
                                   fset="set_KiA",
                                   doc=""
                                   )

    PhaseShiftCav = attribute(label='PhaseShiftCav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftCav",
                                   fset="set_PhaseShiftCav",
                                   doc=""
                                   )

    PhaseShiftFwcav = attribute(label='PhaseShiftFwcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftFwcav",
                                   fset="set_PhaseShiftFwcav",
                                   doc=""
                                   )

    PhaseShiftFwtet1 = attribute(label='PhaseShiftFwtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftFwtet1",
                                   fset="set_PhaseShiftFwtet1",
                                   doc=""
                                   )

    PhaseShiftFwtet2 = attribute(label='PhaseShiftFwtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftFwtet2",
                                   fset="set_PhaseShiftFwtet2",
                                   doc=""
                                   )

    PilimitA = attribute(label='PilimitA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_PilimitA",
                                   fset="set_PilimitA",
                                   doc=""
                                   )

    SamplesToAverage = attribute(label='SamplesToAverage',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_SamplesToAverage",
                                   fset="set_SamplesToAverage",
                                   doc=""
                                   )

    FilterStages = attribute(label='FilterStages',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=3,
                                   fget="get_FilterStages",
                                   fset="set_FilterStages",
                                   doc=""
                                   )

    PhaseShiftFwcircin = attribute(label='PhaseShiftFwcircin',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftFwcircin",
                                   fset="set_PhaseShiftFwcircin",
                                   doc=""
                                   )

    PhaseShiftControlSignalTet1 = attribute(label='PhaseShiftControlSignalTet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftControlSignalTet1",
                                   fset="set_PhaseShiftControlSignalTet1",
                                   doc=""
                                   )

    PhaseShiftControlSignalTet2 = attribute(label='PhaseShiftControlSignalTet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftControlSignalTet2",
                                   fset="set_PhaseShiftControlSignalTet2",
                                   doc=""
                                   )

    GainTetrode1 = attribute(label='GainTetrode1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0.1, max_value=1,
                                   fget="get_GainTetrode1",
                                   fset="set_GainTetrode1",
                                   doc=""
                                   )

    GainTetrode2 = attribute(label='GainTetrode2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0.1, max_value=1,
                                   fget="get_GainTetrode2",
                                   fset="set_GainTetrode2",
                                   doc=""
                                   )

    AutomaticStartupEnable = attribute(label='AutomaticStartupEnable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_AutomaticStartupEnable",
                                   fset="set_AutomaticStartupEnable",
                                   doc=""
                                   )

    CommandStart = attribute(label='CommandStart',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_CommandStart",
                                   fset="set_CommandStart",
                                   doc=""
                                   )

    Amprefin = attribute(label='Amprefin',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Amprefin",
                                   fset="set_Amprefin",
                                   doc=""
                                   )

    Phrefin = attribute(label='Phrefin',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_Phrefin",
                                   fset="set_Phrefin",
                                   doc=""
                                   )

    Amprefmin = attribute(label='Amprefmin',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Amprefmin",
                                   fset="set_Amprefmin",
                                   doc=""
                                   )

    Phrefmin = attribute(label='Phrefmin',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_Phrefmin",
                                   fset="set_Phrefmin",
                                   doc=""
                                   )

    PhaseIncreaseRate = attribute(label='PhaseIncreaseRate',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_PhaseIncreaseRate",
                                   fset="set_PhaseIncreaseRate",
                                   doc=""
                                   )

    VoltageIncreaseRate = attribute(label='VoltageIncreaseRate',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_VoltageIncreaseRate",
                                   fset="set_VoltageIncreaseRate",
                                   doc=""
                                   )

    GainOl = attribute(label='GainOl',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0.5, max_value=2,
                                   fget="get_GainOl",
                                   fset="set_GainOl",
                                   doc=""
                                   )

    SpareGpioOutput01 = attribute(label='SpareGpioOutput01',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_SpareGpioOutput01",
                                   fset="set_SpareGpioOutput01",
                                   doc=""
                                   )

    SpareGpioOutput02 = attribute(label='SpareGpioOutput02',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_SpareGpioOutput02",
                                   fset="set_SpareGpioOutput02",
                                   doc=""
                                   )

    SpareGpioOutput03 = attribute(label='SpareGpioOutput03',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_SpareGpioOutput03",
                                   fset="set_SpareGpioOutput03",
                                   doc=""
                                   )

    SpareGpioOutput04 = attribute(label='SpareGpioOutput04',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_SpareGpioOutput04",
                                   fset="set_SpareGpioOutput04",
                                   doc=""
                                   )

    FdlSwTrigger = attribute(label='FdlSwTrigger',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_FdlSwTrigger",
                                   fset="set_FdlSwTrigger",
                                   doc=""
                                   )

    SlowIqLoopEnable = attribute(label='SlowIqLoopEnable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_SlowIqLoopEnable",
                                   fset="set_SlowIqLoopEnable",
                                   doc=""
                                   )

    AdcsPhaseshiftEnableA = attribute(label='AdcsPhaseshiftEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_AdcsPhaseshiftEnableA",
                                   fset="set_AdcsPhaseshiftEnableA",
                                   doc=""
                                   )

    DacsPhaseShiftEnableA = attribute(label='DacsPhaseShiftEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_DacsPhaseShiftEnableA",
                                   fset="set_DacsPhaseShiftEnableA",
                                   doc=""
                                   )

    SquarerefEnableA = attribute(label='SquarerefEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_SquarerefEnableA",
                                   fset="set_SquarerefEnableA",
                                   doc=""
                                   )

    FreqsquareA = attribute(label='FreqsquareA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=3, max_value=1000,
                                   fget="get_FreqsquareA",
                                   fset="set_FreqsquareA",
                                   doc=""
                                   )

    ResetkiA = attribute(label='ResetkiA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_ResetkiA",
                                   fset="set_ResetkiA",
                                   doc=""
                                   )

    LookRefA = attribute(label='LookRefA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_LookRefA",
                                   fset="set_LookRefA",
                                   doc=""
                                   )

    QuadrantSelectionA = attribute(label='QuadrantSelectionA',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=3,
                                   fget="get_QuadrantSelectionA",
                                   fset="set_QuadrantSelectionA",
                                   doc=""
                                   )

    SlowIqLoopInputSelection = attribute(label='SlowIqLoopInputSelection',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_SlowIqLoopInputSelection",
                                   fset="set_SlowIqLoopInputSelection",
                                   doc=""
                                   )

    FastIqLoopInputSelection = attribute(label='FastIqLoopInputSelection',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=3,
                                   fget="get_FastIqLoopInputSelection",
                                   fset="set_FastIqLoopInputSelection",
                                   doc=""
                                   )

    AmplitudeLoopInputSelection = attribute(label='AmplitudeLoopInputSelection',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_AmplitudeLoopInputSelection",
                                   fset="set_AmplitudeLoopInputSelection",
                                   doc=""
                                   )

    PhaseLoopInputSelection = attribute(label='PhaseLoopInputSelection',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_PhaseLoopInputSelection",
                                   fset="set_PhaseLoopInputSelection",
                                   doc=""
                                   )

    PolarLoopsEnable = attribute(label='PolarLoopsEnable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_PolarLoopsEnable",
                                   fset="set_PolarLoopsEnable",
                                   doc=""
                                   )

    FastIqLoopEnable = attribute(label='FastIqLoopEnable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_FastIqLoopEnable",
                                   fset="set_FastIqLoopEnable",
                                   doc=""
                                   )

    AmplitudeLoopEnable = attribute(label='AmplitudeLoopEnable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_AmplitudeLoopEnable",
                                   fset="set_AmplitudeLoopEnable",
                                   doc=""
                                   )

    PhaseLoopEnable = attribute(label='PhaseLoopEnable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_PhaseLoopEnable",
                                   fset="set_PhaseLoopEnable",
                                   doc=""
                                   )

    KpFastIqLoop = attribute(label='KpFastIqLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_KpFastIqLoop",
                                   fset="set_KpFastIqLoop",
                                   doc=""
                                   )

    KiFastIqLoop = attribute(label='KiFastIqLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_KiFastIqLoop",
                                   fset="set_KiFastIqLoop",
                                   doc=""
                                   )

    KpAmpLoop = attribute(label='KpAmpLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_KpAmpLoop",
                                   fset="set_KpAmpLoop",
                                   doc=""
                                   )

    KiAmpLoop = attribute(label='KiAmpLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_KiAmpLoop",
                                   fset="set_KiAmpLoop",
                                   doc=""
                                   )

    KpPhaseLoop = attribute(label='KpPhaseLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_KpPhaseLoop",
                                   fset="set_KpPhaseLoop",
                                   doc=""
                                   )

    KiPhaseLoop = attribute(label='KiPhaseLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_KiPhaseLoop",
                                   fset="set_KiPhaseLoop",
                                   doc=""
                                   )

    PiLimitFastPiIq = attribute(label='PiLimitFastPiIq',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_PiLimitFastPiIq",
                                   fset="set_PiLimitFastPiIq",
                                   doc=""
                                   )

    PulseModeEnableA = attribute(label='PulseModeEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_PulseModeEnableA",
                                   fset="set_PulseModeEnableA",
                                   doc=""
                                   )

    AutomaticConditioningEnableA = attribute(label='AutomaticConditioningEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_AutomaticConditioningEnableA",
                                   fset="set_AutomaticConditioningEnableA",
                                   doc=""
                                   )

    ConditioningdutyCicleA = attribute(label='ConditioningdutyCicleA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=100,
                                   fget="get_ConditioningdutyCicleA",
                                   fset="set_ConditioningdutyCicleA",
                                   doc=""
                                   )

    TuningEnableA = attribute(label='TuningEnableA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_TuningEnableA",
                                   fset="set_TuningEnableA",
                                   doc=""
                                   )

    TuningPosEnA = attribute(label='TuningPosEnA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_TuningPosEnA",
                                   fset="set_TuningPosEnA",
                                   doc=""
                                   )

    NumStepsA = attribute(label='NumStepsA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=65535,
                                   fget="get_NumStepsA",
                                   fset="set_NumStepsA",
                                   doc=""
                                   )

    PulsesFrequency = attribute(label='PulsesFrequency',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_PulsesFrequency",
                                   fset="set_PulsesFrequency",
                                   doc=""
                                   )

    PhaseOffsetA = attribute(label='PhaseOffsetA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseOffsetA",
                                   fset="set_PhaseOffsetA",
                                   doc=""
                                   )

    MoveA = attribute(label='MoveA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_MoveA",
                                   fset="set_MoveA",
                                   doc=""
                                   )

    MoveupA = attribute(label='MoveupA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_MoveupA",
                                   fset="set_MoveupA",
                                   doc=""
                                   )

    TuningresetA = attribute(label='TuningresetA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_TuningresetA",
                                   fset="set_TuningresetA",
                                   doc=""
                                   )

    Fwmina = attribute(label='Fwmina',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Fwmina",
                                   fset="set_Fwmina",
                                   doc=""
                                   )

    MarginupA = attribute(label='MarginupA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=0, max_value=10,
                                   fget="get_MarginupA",
                                   fset="set_MarginupA",
                                   doc=""
                                   )

    MarginlowA = attribute(label='MarginlowA',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=0, max_value=5,
                                   fget="get_MarginlowA",
                                   fset="set_MarginlowA",
                                   doc=""
                                   )

    Tuningdelay = attribute(label='Tuningdelay',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=3,
                                   fget="get_Tuningdelay",
                                   fset="set_Tuningdelay",
                                   doc=""
                                   )

    Tuningfilterenable = attribute(label='Tuningfilterenable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_Tuningfilterenable",
                                   fset="set_Tuningfilterenable",
                                   doc=""
                                   )

    Tuningtriggerenable = attribute(label='Tuningtriggerenable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_Tuningtriggerenable",
                                   fset="set_Tuningtriggerenable",
                                   doc=""
                                   )

    EpsItckDisable = attribute(label='EpsItckDisable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_EpsItckDisable",
                                   fset="set_EpsItckDisable",
                                   doc=""
                                   )

    FimItckDisable = attribute(label='FimItckDisable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_FimItckDisable",
                                   fset="set_FimItckDisable",
                                   doc=""
                                   )

    MDivider = attribute(label='MDivider',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=128,
                                   fget="get_MDivider",
                                   fset="set_MDivider",
                                   doc=""
                                   )

    NDivider = attribute(label='NDivider',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=128,
                                   fget="get_NDivider",
                                   fset="set_NDivider",
                                   doc=""
                                   )

    Muxsel = attribute(label='Muxsel',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Muxsel",
                                   fset="set_Muxsel",
                                   doc=""
                                   )

    Mux0Divider = attribute(label='Mux0Divider',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux0Divider",
                                   fset="set_Mux0Divider",
                                   doc=""
                                   )

    Mux1Divider = attribute(label='Mux1Divider',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux1Divider",
                                   fset="set_Mux1Divider",
                                   doc=""
                                   )

    Mux2Divider = attribute(label='Mux2Divider',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux2Divider",
                                   fset="set_Mux2Divider",
                                   doc=""
                                   )

    Mux3Divider = attribute(label='Mux3Divider',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux3Divider",
                                   fset="set_Mux3Divider",
                                   doc=""
                                   )

    Mux4Divider = attribute(label='Mux4Divider',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux4Divider",
                                   fset="set_Mux4Divider",
                                   doc=""
                                   )

    SendWord = attribute(label='SendWord',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_SendWord",
                                   fset="set_SendWord",
                                   doc=""
                                   )

    Cpdir = attribute(label='Cpdir',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_Cpdir",
                                   fset="set_Cpdir",
                                   doc=""
                                   )

    VcxoOutputInversion = attribute(label='VcxoOutputInversion',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_VcxoOutputInversion",
                                   fset="set_VcxoOutputInversion",
                                   doc=""
                                   )

    Diag_IcavLoops = attribute(label='Diag_IcavLoops',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QcavLoops = attribute(label='Diag_QcavLoops',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Icontrol = attribute(label='Diag_Icontrol',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qcontrol = attribute(label='Diag_Qcontrol',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Icontrol1 = attribute(label='Diag_Icontrol1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qcontrol1 = attribute(label='Diag_Qcontrol1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Icontrol2 = attribute(label='Diag_Icontrol2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qcontrol2 = attribute(label='Diag_Qcontrol2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Ierror = attribute(label='Diag_Ierror',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qerror = attribute(label='Diag_Qerror',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Ierroraccum = attribute(label='Diag_Ierroraccum',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qerroraccum = attribute(label='Diag_Qerroraccum',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Iref = attribute(label='Diag_Iref',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qref = attribute(label='Diag_Qref',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IFwCavLoops = attribute(label='Diag_IFwCavLoops',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QFwCavLoops = attribute(label='Diag_QFwCavLoops',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IFwTet1Loops = attribute(label='Diag_IFwTet1Loops',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QFwTet1Loops = attribute(label='Diag_QFwTet1Loops',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IFwTet2Loops = attribute(label='Diag_IFwTet2Loops',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QFwTet2Loops = attribute(label='Diag_QFwTet2Loops',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IFwCircInLoops = attribute(label='Diag_IFwCircInLoops',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QFwCircInLoops = attribute(label='Diag_QFwCircInLoops',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Imo = attribute(label='Diag_Imo',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qmo = attribute(label='Diag_Qmo',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Ispare1 = attribute(label='Diag_Ispare1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qspare1 = attribute(label='Diag_Qspare1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Ispare2 = attribute(label='Diag_Ispare2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qspare2 = attribute(label='Diag_Qspare2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IMuxCav = attribute(label='Diag_IMuxCav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QMuxCav = attribute(label='Diag_QMuxCav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IMuxFwCav = attribute(label='Diag_IMuxFwCav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QMuxFwCav = attribute(label='Diag_QMuxFwCav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IMuxFwTet1 = attribute(label='Diag_IMuxFwTet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QMuxFwTet1 = attribute(label='Diag_QMuxFwTet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IMuxFwTet2 = attribute(label='Diag_IMuxFwTet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QMuxFwTet2 = attribute(label='Diag_QMuxFwTet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IMuxFwCircIn = attribute(label='Diag_IMuxFwCircIn',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QMuxFwCircIn = attribute(label='Diag_QMuxFwCircIn',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_AmpCav = attribute(label='Diag_AmpCav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_AmpFw = attribute(label='Diag_AmpFw',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_AngCavFw = attribute(label='Diag_AngCavFw',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_AngCavL = attribute(label='Diag_AngCavL',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_AngFwL = attribute(label='Diag_AngFwL',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Vaccum1 = attribute(label='Diag_Vaccum1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Vaccum2 = attribute(label='Diag_Vaccum2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IcontrolSlowpi = attribute(label='Diag_IcontrolSlowpi',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QcontrolSlowpi = attribute(label='Diag_QcontrolSlowpi',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IcontrolFastpi = attribute(label='Diag_IcontrolFastpi',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QcontrolFastpi = attribute(label='Diag_QcontrolFastpi',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_VcxoPowered = attribute(label='Diag_VcxoPowered',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_VcxoRef = attribute(label='Diag_VcxoRef',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_VcxoLocked = attribute(label='Diag_VcxoLocked',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_VcxoCableDisconnected = attribute(label='Diag_VcxoCableDisconnected',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IpolarForAmplitudeLoop = attribute(label='Diag_IpolarForAmplitudeLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QpolarForAmplitudeLoop = attribute(label='Diag_QpolarForAmplitudeLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IPolarForPhaseLoop = attribute(label='Diag_IPolarForPhaseLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QpolarForPhaseLoop = attribute(label='Diag_QpolarForPhaseLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_AmpInputOfAmpLoop = attribute(label='Diag_AmpInputOfAmpLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PaseInputOfAmpLoop = attribute(label='Diag_PaseInputOfAmpLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_AmpInputOfPhaseLoop = attribute(label='Diag_AmpInputOfPhaseLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PhInputOfPhaseLoop = attribute(label='Diag_PhInputOfPhaseLoop',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_AmpLoopControlOutput = attribute(label='Diag_AmpLoopControlOutput',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_AmpLoopError = attribute(label='Diag_AmpLoopError',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_AmpLoopErrorAccum = attribute(label='Diag_AmpLoopErrorAccum',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PhLoopControlOutput = attribute(label='Diag_PhLoopControlOutput',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PhLoopError = attribute(label='Diag_PhLoopError',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PhLoopErrorAccum = attribute(label='Diag_PhLoopErrorAccum',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IpolarControlOutput = attribute(label='Diag_IpolarControlOutput',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QpolarControlOutput = attribute(label='Diag_QpolarControlOutput',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IcontrolSlowpiIq = attribute(label='Diag_IcontrolSlowpiIq',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QcontrolSlowpiq = attribute(label='Diag_QcontrolSlowpiq',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IcontrolFastpiIq = attribute(label='Diag_IcontrolFastpiIq',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_QcontrolFastpiIq = attribute(label='Diag_QcontrolFastpiIq',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IloopinputSlowpiIq = attribute(label='Diag_IloopinputSlowpiIq',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_IloopinputSlowpiIq = attribute(label='Diag_IloopinputSlowpiIq',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Fwmin = attribute(label='Diag_Fwmin',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_MovingPlungerAuto = attribute(label='Diag_MovingPlungerAuto',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_FreqUp = attribute(label='Diag_FreqUp',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_ManualTuningOn = attribute(label='Diag_ManualTuningOn',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_ManualTuningFreqUp = attribute(label='Diag_ManualTuningFreqUp',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_EpsItckDelay = attribute(label='Diag_EpsItckDelay',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_FimItckDelay = attribute(label='Diag_FimItckDelay',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_FdlTrigHwInput = attribute(label='Diag_FdlTrigHwInput',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_FdlTrigSwInput = attribute(label='Diag_FdlTrigSwInput',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )


    perseusType = device_property(dtype=str, default_value='simulated')
    perseusIp = device_property(dtype=str, default_value='127.0.0.1')

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
        return perseus_utils.read_direct(self.perseus, 0)

    @DebugIt()
    def set_KpA(self, KpA):
        perseus_utils.write_direct(self.perseus, KpA, 0)

    @DebugIt()
    def get_KiA(self):
        return perseus_utils.read_direct(self.perseus, 1)

    @DebugIt()
    def set_KiA(self, KiA):
        perseus_utils.write_direct(self.perseus, KiA, 1)

    @DebugIt()
    def get_PhaseShiftCav(self):
        return perseus_utils.read_angle(self.perseus, 2)

    @DebugIt()
    def set_PhaseShiftCav(self, PhaseShiftCav):
        perseus_utils.write_angle(self.perseus, PhaseShiftCav, 2)

    @DebugIt()
    def get_PhaseShiftFwcav(self):
        return perseus_utils.read_angle(self.perseus, 3)

    @DebugIt()
    def set_PhaseShiftFwcav(self, PhaseShiftFwcav):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwcav, 3)

    @DebugIt()
    def get_PhaseShiftFwtet1(self):
        return perseus_utils.read_angle(self.perseus, 4)

    @DebugIt()
    def set_PhaseShiftFwtet1(self, PhaseShiftFwtet1):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwtet1, 4)

    @DebugIt()
    def get_PhaseShiftFwtet2(self):
        return perseus_utils.read_angle(self.perseus, 5)

    @DebugIt()
    def set_PhaseShiftFwtet2(self, PhaseShiftFwtet2):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwtet2, 5)

    @DebugIt()
    def get_PilimitA(self):
        address = 6
        #@todo: add this method to special methods library ...
        extra_func.get_PilimitA(self.perseus, address)

    @DebugIt()
    def set_PilimitA(self, PilimitA):
        address = 6
        #@todo: add this method to special methods library ...
        extra_func.get_PilimitA(self.perseus, PilimitA, address)

    @DebugIt()
    def get_SamplesToAverage(self):
        return perseus_utils.read_direct(self.perseus, 7)

    @DebugIt()
    def set_SamplesToAverage(self, SamplesToAverage):
        perseus_utils.write_direct(self.perseus, SamplesToAverage, 7)

    @DebugIt()
    def get_FilterStages(self):
        return perseus_utils.read_direct(self.perseus, 8)

    @DebugIt()
    def set_FilterStages(self, FilterStages):
        perseus_utils.write_direct(self.perseus, FilterStages, 8)

    @DebugIt()
    def get_PhaseShiftFwcircin(self):
        return perseus_utils.read_angle(self.perseus, 9)

    @DebugIt()
    def set_PhaseShiftFwcircin(self, PhaseShiftFwcircin):
        perseus_utils.write_angle(self.perseus, PhaseShiftFwcircin, 9)

    @DebugIt()
    def get_PhaseShiftControlSignalTet1(self):
        return perseus_utils.read_angle(self.perseus, 10)

    @DebugIt()
    def set_PhaseShiftControlSignalTet1(self, PhaseShiftControlSignalTet1):
        perseus_utils.write_angle(self.perseus, PhaseShiftControlSignalTet1, 10)

    @DebugIt()
    def get_PhaseShiftControlSignalTet2(self):
        return perseus_utils.read_angle(self.perseus, 11)

    @DebugIt()
    def set_PhaseShiftControlSignalTet2(self, PhaseShiftControlSignalTet2):
        perseus_utils.write_angle(self.perseus, PhaseShiftControlSignalTet2, 11)

    @DebugIt()
    def get_GainTetrode1(self):
        address = 13
        #@todo: add this method to special methods library ...
        extra_func.get_GainTetrode1(self.perseus, address)

    @DebugIt()
    def set_GainTetrode1(self, GainTetrode1):
        address = 13
        #@todo: add this method to special methods library ...
        extra_func.get_GainTetrode1(self.perseus, GainTetrode1, address)

    @DebugIt()
    def get_GainTetrode2(self):
        address = 14
        #@todo: add this method to special methods library ...
        extra_func.get_GainTetrode2(self.perseus, address)

    @DebugIt()
    def set_GainTetrode2(self, GainTetrode2):
        address = 14
        #@todo: add this method to special methods library ...
        extra_func.get_GainTetrode2(self.perseus, GainTetrode2, address)

    @DebugIt()
    def get_AutomaticStartupEnable(self):
        return perseus_utils.read_direct(self.perseus, 15)

    @DebugIt()
    def set_AutomaticStartupEnable(self, AutomaticStartupEnable):
        perseus_utils.write_direct(self.perseus, AutomaticStartupEnable, 15)

    @DebugIt()
    def get_CommandStart(self):
        return perseus_utils.read_direct(self.perseus, 16)

    @DebugIt()
    def set_CommandStart(self, CommandStart):
        perseus_utils.write_direct(self.perseus, CommandStart, 16)

    @DebugIt()
    def get_Amprefin(self):
        return perseus_utils.read_milivolts(self.perseus, 19)

    @DebugIt()
    def set_Amprefin(self, Amprefin):
        perseus_utils.write_milivolts(self.perseus, Amprefin, 19)

    @DebugIt()
    def get_Phrefin(self):
        return perseus_utils.read_angle(self.perseus, 20)

    @DebugIt()
    def set_Phrefin(self, Phrefin):
        perseus_utils.write_angle(self.perseus, Phrefin, 20)

    @DebugIt()
    def get_Amprefmin(self):
        return perseus_utils.read_milivolts(self.perseus, 21)

    @DebugIt()
    def set_Amprefmin(self, Amprefmin):
        perseus_utils.write_milivolts(self.perseus, Amprefmin, 21)

    @DebugIt()
    def get_Phrefmin(self):
        return perseus_utils.read_angle(self.perseus, 22)

    @DebugIt()
    def set_Phrefmin(self, Phrefmin):
        perseus_utils.write_angle(self.perseus, Phrefmin, 22)

    @DebugIt()
    def get_PhaseIncreaseRate(self):
        return perseus_utils.read_direct(self.perseus, 23)

    @DebugIt()
    def set_PhaseIncreaseRate(self, PhaseIncreaseRate):
        perseus_utils.write_direct(self.perseus, PhaseIncreaseRate, 23)

    @DebugIt()
    def get_VoltageIncreaseRate(self):
        return perseus_utils.read_direct(self.perseus, 24)

    @DebugIt()
    def set_VoltageIncreaseRate(self, VoltageIncreaseRate):
        perseus_utils.write_direct(self.perseus, VoltageIncreaseRate, 24)

    @DebugIt()
    def get_GainOl(self):
        address = 25
        #@todo: add this method to special methods library ...
        extra_func.get_GainOl(self.perseus, address)

    @DebugIt()
    def set_GainOl(self, GainOl):
        address = 25
        #@todo: add this method to special methods library ...
        extra_func.get_GainOl(self.perseus, GainOl, address)

    @DebugIt()
    def get_SpareGpioOutput01(self):
        return perseus_utils.read_direct(self.perseus, 28)

    @DebugIt()
    def set_SpareGpioOutput01(self, SpareGpioOutput01):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput01, 28)

    @DebugIt()
    def get_SpareGpioOutput02(self):
        return perseus_utils.read_direct(self.perseus, 29)

    @DebugIt()
    def set_SpareGpioOutput02(self, SpareGpioOutput02):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput02, 29)

    @DebugIt()
    def get_SpareGpioOutput03(self):
        return perseus_utils.read_direct(self.perseus, 30)

    @DebugIt()
    def set_SpareGpioOutput03(self, SpareGpioOutput03):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput03, 30)

    @DebugIt()
    def get_SpareGpioOutput04(self):
        return perseus_utils.read_direct(self.perseus, 31)

    @DebugIt()
    def set_SpareGpioOutput04(self, SpareGpioOutput04):
        perseus_utils.write_direct(self.perseus, SpareGpioOutput04, 31)

    @DebugIt()
    def get_FdlSwTrigger(self):
        return perseus_utils.read_direct(self.perseus, 32)

    @DebugIt()
    def set_FdlSwTrigger(self, FdlSwTrigger):
        perseus_utils.write_direct(self.perseus, FdlSwTrigger, 32)

    @DebugIt()
    def get_SlowIqLoopEnable(self):
        return perseus_utils.read_direct(self.perseus, 100)

    @DebugIt()
    def set_SlowIqLoopEnable(self, SlowIqLoopEnable):
        perseus_utils.write_direct(self.perseus, SlowIqLoopEnable, 100)

    @DebugIt()
    def get_AdcsPhaseshiftEnableA(self):
        return perseus_utils.read_direct(self.perseus, 101)

    @DebugIt()
    def set_AdcsPhaseshiftEnableA(self, AdcsPhaseshiftEnableA):
        perseus_utils.write_direct(self.perseus, AdcsPhaseshiftEnableA, 101)

    @DebugIt()
    def get_DacsPhaseShiftEnableA(self):
        return perseus_utils.read_direct(self.perseus, 102)

    @DebugIt()
    def set_DacsPhaseShiftEnableA(self, DacsPhaseShiftEnableA):
        perseus_utils.write_direct(self.perseus, DacsPhaseShiftEnableA, 102)

    @DebugIt()
    def get_SquarerefEnableA(self):
        return perseus_utils.read_direct(self.perseus, 103)

    @DebugIt()
    def set_SquarerefEnableA(self, SquarerefEnableA):
        perseus_utils.write_direct(self.perseus, SquarerefEnableA, 103)

    @DebugIt()
    def get_FreqsquareA(self):
        address = 104
        #@todo: add this method to special methods library ...
        extra_func.get_FreqsquareA(self.perseus, address)

    @DebugIt()
    def set_FreqsquareA(self, FreqsquareA):
        address = 104
        #@todo: add this method to special methods library ...
        extra_func.get_FreqsquareA(self.perseus, FreqsquareA, address)

    @DebugIt()
    def get_ResetkiA(self):
        return perseus_utils.read_direct(self.perseus, 105)

    @DebugIt()
    def set_ResetkiA(self, ResetkiA):
        perseus_utils.write_direct(self.perseus, ResetkiA, 105)

    @DebugIt()
    def get_LookRefA(self):
        return perseus_utils.read_direct(self.perseus, 106)

    @DebugIt()
    def set_LookRefA(self, LookRefA):
        perseus_utils.write_direct(self.perseus, LookRefA, 106)

    @DebugIt()
    def get_QuadrantSelectionA(self):
        return perseus_utils.read_direct(self.perseus, 107)

    @DebugIt()
    def set_QuadrantSelectionA(self, QuadrantSelectionA):
        perseus_utils.write_direct(self.perseus, QuadrantSelectionA, 107)

    @DebugIt()
    def get_SlowIqLoopInputSelection(self):
        return perseus_utils.read_direct(self.perseus, 110)

    @DebugIt()
    def set_SlowIqLoopInputSelection(self, SlowIqLoopInputSelection):
        perseus_utils.write_direct(self.perseus, SlowIqLoopInputSelection, 110)

    @DebugIt()
    def get_FastIqLoopInputSelection(self):
        return perseus_utils.read_direct(self.perseus, 111)

    @DebugIt()
    def set_FastIqLoopInputSelection(self, FastIqLoopInputSelection):
        perseus_utils.write_direct(self.perseus, FastIqLoopInputSelection, 111)

    @DebugIt()
    def get_AmplitudeLoopInputSelection(self):
        return perseus_utils.read_direct(self.perseus, 112)

    @DebugIt()
    def set_AmplitudeLoopInputSelection(self, AmplitudeLoopInputSelection):
        perseus_utils.write_direct(self.perseus, AmplitudeLoopInputSelection, 112)

    @DebugIt()
    def get_PhaseLoopInputSelection(self):
        return perseus_utils.read_direct(self.perseus, 113)

    @DebugIt()
    def set_PhaseLoopInputSelection(self, PhaseLoopInputSelection):
        perseus_utils.write_direct(self.perseus, PhaseLoopInputSelection, 113)

    @DebugIt()
    def get_PolarLoopsEnable(self):
        return perseus_utils.read_direct(self.perseus, 114)

    @DebugIt()
    def set_PolarLoopsEnable(self, PolarLoopsEnable):
        perseus_utils.write_direct(self.perseus, PolarLoopsEnable, 114)

    @DebugIt()
    def get_FastIqLoopEnable(self):
        return perseus_utils.read_direct(self.perseus, 115)

    @DebugIt()
    def set_FastIqLoopEnable(self, FastIqLoopEnable):
        perseus_utils.write_direct(self.perseus, FastIqLoopEnable, 115)

    @DebugIt()
    def get_AmplitudeLoopEnable(self):
        return perseus_utils.read_direct(self.perseus, 116)

    @DebugIt()
    def set_AmplitudeLoopEnable(self, AmplitudeLoopEnable):
        perseus_utils.write_direct(self.perseus, AmplitudeLoopEnable, 116)

    @DebugIt()
    def get_PhaseLoopEnable(self):
        return perseus_utils.read_direct(self.perseus, 117)

    @DebugIt()
    def set_PhaseLoopEnable(self, PhaseLoopEnable):
        perseus_utils.write_direct(self.perseus, PhaseLoopEnable, 117)

    @DebugIt()
    def get_KpFastIqLoop(self):
        return perseus_utils.read_direct(self.perseus, 118)

    @DebugIt()
    def set_KpFastIqLoop(self, KpFastIqLoop):
        perseus_utils.write_direct(self.perseus, KpFastIqLoop, 118)

    @DebugIt()
    def get_KiFastIqLoop(self):
        return perseus_utils.read_direct(self.perseus, 119)

    @DebugIt()
    def set_KiFastIqLoop(self, KiFastIqLoop):
        perseus_utils.write_direct(self.perseus, KiFastIqLoop, 119)

    @DebugIt()
    def get_KpAmpLoop(self):
        return perseus_utils.read_direct(self.perseus, 120)

    @DebugIt()
    def set_KpAmpLoop(self, KpAmpLoop):
        perseus_utils.write_direct(self.perseus, KpAmpLoop, 120)

    @DebugIt()
    def get_KiAmpLoop(self):
        return perseus_utils.read_direct(self.perseus, 121)

    @DebugIt()
    def set_KiAmpLoop(self, KiAmpLoop):
        perseus_utils.write_direct(self.perseus, KiAmpLoop, 121)

    @DebugIt()
    def get_KpPhaseLoop(self):
        return perseus_utils.read_direct(self.perseus, 122)

    @DebugIt()
    def set_KpPhaseLoop(self, KpPhaseLoop):
        perseus_utils.write_direct(self.perseus, KpPhaseLoop, 122)

    @DebugIt()
    def get_KiPhaseLoop(self):
        return perseus_utils.read_direct(self.perseus, 123)

    @DebugIt()
    def set_KiPhaseLoop(self, KiPhaseLoop):
        perseus_utils.write_direct(self.perseus, KiPhaseLoop, 123)

    @DebugIt()
    def get_PiLimitFastPiIq(self):
        return perseus_utils.read_milivolts(self.perseus, 124)

    @DebugIt()
    def set_PiLimitFastPiIq(self, PiLimitFastPiIq):
        perseus_utils.write_milivolts(self.perseus, PiLimitFastPiIq, 124)

    @DebugIt()
    def get_PulseModeEnableA(self):
        return perseus_utils.read_direct(self.perseus, 200)

    @DebugIt()
    def set_PulseModeEnableA(self, PulseModeEnableA):
        perseus_utils.write_direct(self.perseus, PulseModeEnableA, 200)

    @DebugIt()
    def get_AutomaticConditioningEnableA(self):
        return perseus_utils.read_direct(self.perseus, 201)

    @DebugIt()
    def set_AutomaticConditioningEnableA(self, AutomaticConditioningEnableA):
        perseus_utils.write_direct(self.perseus, AutomaticConditioningEnableA, 201)

    @DebugIt()
    def get_ConditioningdutyCicleA(self):
        address = 202
        #@todo: add this method to special methods library ...
        extra_func.get_ConditioningdutyCicleA(self.perseus, address)

    @DebugIt()
    def set_ConditioningdutyCicleA(self, ConditioningdutyCicleA):
        address = 202
        #@todo: add this method to special methods library ...
        extra_func.get_ConditioningdutyCicleA(self.perseus, ConditioningdutyCicleA, address)

    @DebugIt()
    def get_TuningEnableA(self):
        return perseus_utils.read_direct(self.perseus, 300)

    @DebugIt()
    def set_TuningEnableA(self, TuningEnableA):
        perseus_utils.write_direct(self.perseus, TuningEnableA, 300)

    @DebugIt()
    def get_TuningPosEnA(self):
        return perseus_utils.read_direct(self.perseus, 301)

    @DebugIt()
    def set_TuningPosEnA(self, TuningPosEnA):
        perseus_utils.write_direct(self.perseus, TuningPosEnA, 301)

    @DebugIt()
    def get_NumStepsA(self):
        return perseus_utils.read_direct(self.perseus, 302)

    @DebugIt()
    def set_NumStepsA(self, NumStepsA):
        perseus_utils.write_direct(self.perseus, NumStepsA, 302)

    @DebugIt()
    def get_PulsesFrequency(self):
        return perseus_utils.read_direct(self.perseus, 303)

    @DebugIt()
    def set_PulsesFrequency(self, PulsesFrequency):
        perseus_utils.write_direct(self.perseus, PulsesFrequency, 303)

    @DebugIt()
    def get_PhaseOffsetA(self):
        return perseus_utils.read_angle(self.perseus, 304)

    @DebugIt()
    def set_PhaseOffsetA(self, PhaseOffsetA):
        perseus_utils.write_angle(self.perseus, PhaseOffsetA, 304)

    @DebugIt()
    def get_MoveA(self):
        return perseus_utils.read_direct(self.perseus, 305)

    @DebugIt()
    def set_MoveA(self, MoveA):
        perseus_utils.write_direct(self.perseus, MoveA, 305)

    @DebugIt()
    def get_MoveupA(self):
        return perseus_utils.read_direct(self.perseus, 306)

    @DebugIt()
    def set_MoveupA(self, MoveupA):
        perseus_utils.write_direct(self.perseus, MoveupA, 306)

    @DebugIt()
    def get_TuningresetA(self):
        return perseus_utils.read_direct(self.perseus, 307)

    @DebugIt()
    def set_TuningresetA(self, TuningresetA):
        perseus_utils.write_direct(self.perseus, TuningresetA, 307)

    @DebugIt()
    def get_Fwmina(self):
        address = 308
        #@todo: add this method to special methods library ...
        extra_func.get_Fwmina(self.perseus, address)

    @DebugIt()
    def set_Fwmina(self, Fwmina):
        address = 308
        #@todo: add this method to special methods library ...
        extra_func.get_Fwmina(self.perseus, Fwmina, address)

    @DebugIt()
    def get_MarginupA(self):
        return perseus_utils.read_angle(self.perseus, 309)

    @DebugIt()
    def set_MarginupA(self, MarginupA):
        perseus_utils.write_angle(self.perseus, MarginupA, 309)

    @DebugIt()
    def get_MarginlowA(self):
        return perseus_utils.read_angle(self.perseus, 310)

    @DebugIt()
    def set_MarginlowA(self, MarginlowA):
        perseus_utils.write_angle(self.perseus, MarginlowA, 310)

    @DebugIt()
    def get_Tuningdelay(self):
        address = 311
        #@todo: add this method to special methods library ...
        extra_func.get_Tuningdelay(self.perseus, address)

    @DebugIt()
    def set_Tuningdelay(self, Tuningdelay):
        address = 311
        #@todo: add this method to special methods library ...
        extra_func.get_Tuningdelay(self.perseus, Tuningdelay, address)

    @DebugIt()
    def get_Tuningfilterenable(self):
        return perseus_utils.read_direct(self.perseus, 312)

    @DebugIt()
    def set_Tuningfilterenable(self, Tuningfilterenable):
        perseus_utils.write_direct(self.perseus, Tuningfilterenable, 312)

    @DebugIt()
    def get_Tuningtriggerenable(self):
        return perseus_utils.read_direct(self.perseus, 313)

    @DebugIt()
    def set_Tuningtriggerenable(self, Tuningtriggerenable):
        perseus_utils.write_direct(self.perseus, Tuningtriggerenable, 313)

    @DebugIt()
    def get_EpsItckDisable(self):
        return perseus_utils.read_direct(self.perseus, 400)

    @DebugIt()
    def set_EpsItckDisable(self, EpsItckDisable):
        perseus_utils.write_direct(self.perseus, EpsItckDisable, 400)

    @DebugIt()
    def get_FimItckDisable(self):
        return perseus_utils.read_direct(self.perseus, 401)

    @DebugIt()
    def set_FimItckDisable(self, FimItckDisable):
        perseus_utils.write_direct(self.perseus, FimItckDisable, 401)

    @DebugIt()
    def get_MDivider(self):
        address = 500
        #@todo: add this method to special methods library ...
        extra_func.get_MDivider(self.perseus, address)

    @DebugIt()
    def set_MDivider(self, MDivider):
        address = 500
        #@todo: add this method to special methods library ...
        extra_func.get_MDivider(self.perseus, MDivider, address)

    @DebugIt()
    def get_NDivider(self):
        address = 501
        #@todo: add this method to special methods library ...
        extra_func.get_NDivider(self.perseus, address)

    @DebugIt()
    def set_NDivider(self, NDivider):
        address = 501
        #@todo: add this method to special methods library ...
        extra_func.get_NDivider(self.perseus, NDivider, address)

    @DebugIt()
    def get_Muxsel(self):
        return perseus_utils.read_direct(self.perseus, 502)

    @DebugIt()
    def set_Muxsel(self, Muxsel):
        perseus_utils.write_direct(self.perseus, Muxsel, 502)

    @DebugIt()
    def get_Mux0Divider(self):
        return perseus_utils.read_direct(self.perseus, 503)

    @DebugIt()
    def set_Mux0Divider(self, Mux0Divider):
        perseus_utils.write_direct(self.perseus, Mux0Divider, 503)

    @DebugIt()
    def get_Mux1Divider(self):
        return perseus_utils.read_direct(self.perseus, 504)

    @DebugIt()
    def set_Mux1Divider(self, Mux1Divider):
        perseus_utils.write_direct(self.perseus, Mux1Divider, 504)

    @DebugIt()
    def get_Mux2Divider(self):
        return perseus_utils.read_direct(self.perseus, 505)

    @DebugIt()
    def set_Mux2Divider(self, Mux2Divider):
        perseus_utils.write_direct(self.perseus, Mux2Divider, 505)

    @DebugIt()
    def get_Mux3Divider(self):
        return perseus_utils.read_direct(self.perseus, 506)

    @DebugIt()
    def set_Mux3Divider(self, Mux3Divider):
        perseus_utils.write_direct(self.perseus, Mux3Divider, 506)

    @DebugIt()
    def get_Mux4Divider(self):
        return perseus_utils.read_direct(self.perseus, 507)

    @DebugIt()
    def set_Mux4Divider(self, Mux4Divider):
        perseus_utils.write_direct(self.perseus, Mux4Divider, 507)

    @DebugIt()
    def get_SendWord(self):
        return perseus_utils.read_direct(self.perseus, 508)

    @DebugIt()
    def set_SendWord(self, SendWord):
        perseus_utils.write_direct(self.perseus, SendWord, 508)

    @DebugIt()
    def get_Cpdir(self):
        return perseus_utils.read_direct(self.perseus, 509)

    @DebugIt()
    def set_Cpdir(self, Cpdir):
        perseus_utils.write_direct(self.perseus, Cpdir, 509)

    @DebugIt()
    def get_VcxoOutputInversion(self):
        return perseus_utils.read_direct(self.perseus, 510)

    @DebugIt()
    def set_VcxoOutputInversion(self, VcxoOutputInversion):
        perseus_utils.write_direct(self.perseus, VcxoOutputInversion, 510)

    @DebugIt()
    def read_Diag_IcavLoops(self):
        return self._Diag_IcavLoops

    @DebugIt()
    def read_Diag_QcavLoops(self):
        return self._Diag_QcavLoops

    @DebugIt()
    def read_Diag_Icontrol(self):
        return self._Diag_Icontrol

    @DebugIt()
    def read_Diag_Qcontrol(self):
        return self._Diag_Qcontrol

    @DebugIt()
    def read_Diag_Icontrol1(self):
        return self._Diag_Icontrol1

    @DebugIt()
    def read_Diag_Qcontrol1(self):
        return self._Diag_Qcontrol1

    @DebugIt()
    def read_Diag_Icontrol2(self):
        return self._Diag_Icontrol2

    @DebugIt()
    def read_Diag_Qcontrol2(self):
        return self._Diag_Qcontrol2

    @DebugIt()
    def read_Diag_Ierror(self):
        return self._Diag_Ierror

    @DebugIt()
    def read_Diag_Qerror(self):
        return self._Diag_Qerror

    @DebugIt()
    def read_Diag_Ierroraccum(self):
        return self._Diag_Ierroraccum

    @DebugIt()
    def read_Diag_Qerroraccum(self):
        return self._Diag_Qerroraccum

    @DebugIt()
    def read_Diag_Iref(self):
        return self._Diag_Iref

    @DebugIt()
    def read_Diag_Qref(self):
        return self._Diag_Qref

    @DebugIt()
    def read_Diag_IFwCavLoops(self):
        return self._Diag_IFwCavLoops

    @DebugIt()
    def read_Diag_QFwCavLoops(self):
        return self._Diag_QFwCavLoops

    @DebugIt()
    def read_Diag_IFwTet1Loops(self):
        return self._Diag_IFwTet1Loops

    @DebugIt()
    def read_Diag_QFwTet1Loops(self):
        return self._Diag_QFwTet1Loops

    @DebugIt()
    def read_Diag_IFwTet2Loops(self):
        return self._Diag_IFwTet2Loops

    @DebugIt()
    def read_Diag_QFwTet2Loops(self):
        return self._Diag_QFwTet2Loops

    @DebugIt()
    def read_Diag_IFwCircInLoops(self):
        return self._Diag_IFwCircInLoops

    @DebugIt()
    def read_Diag_QFwCircInLoops(self):
        return self._Diag_QFwCircInLoops

    @DebugIt()
    def read_Diag_Imo(self):
        return self._Diag_Imo

    @DebugIt()
    def read_Diag_Qmo(self):
        return self._Diag_Qmo

    @DebugIt()
    def read_Diag_Ispare1(self):
        return self._Diag_Ispare1

    @DebugIt()
    def read_Diag_Qspare1(self):
        return self._Diag_Qspare1

    @DebugIt()
    def read_Diag_Ispare2(self):
        return self._Diag_Ispare2

    @DebugIt()
    def read_Diag_Qspare2(self):
        return self._Diag_Qspare2

    @DebugIt()
    def read_Diag_IMuxCav(self):
        return self._Diag_IMuxCav

    @DebugIt()
    def read_Diag_QMuxCav(self):
        return self._Diag_QMuxCav

    @DebugIt()
    def read_Diag_IMuxFwCav(self):
        return self._Diag_IMuxFwCav

    @DebugIt()
    def read_Diag_QMuxFwCav(self):
        return self._Diag_QMuxFwCav

    @DebugIt()
    def read_Diag_IMuxFwTet1(self):
        return self._Diag_IMuxFwTet1

    @DebugIt()
    def read_Diag_QMuxFwTet1(self):
        return self._Diag_QMuxFwTet1

    @DebugIt()
    def read_Diag_IMuxFwTet2(self):
        return self._Diag_IMuxFwTet2

    @DebugIt()
    def read_Diag_QMuxFwTet2(self):
        return self._Diag_QMuxFwTet2

    @DebugIt()
    def read_Diag_IMuxFwCircIn(self):
        return self._Diag_IMuxFwCircIn

    @DebugIt()
    def read_Diag_QMuxFwCircIn(self):
        return self._Diag_QMuxFwCircIn

    @DebugIt()
    def read_Diag_AmpCav(self):
        return self._Diag_AmpCav

    @DebugIt()
    def read_Diag_AmpFw(self):
        return self._Diag_AmpFw

    @DebugIt()
    def read_Diag_AngCavFw(self):
        return self._Diag_AngCavFw

    @DebugIt()
    def read_Diag_AngCavL(self):
        return self._Diag_AngCavL

    @DebugIt()
    def read_Diag_AngFwL(self):
        return self._Diag_AngFwL

    @DebugIt()
    def read_Diag_Vaccum1(self):
        return self._Diag_Vaccum1

    @DebugIt()
    def read_Diag_Vaccum2(self):
        return self._Diag_Vaccum2

    @DebugIt()
    def read_Diag_IcontrolSlowpi(self):
        return self._Diag_IcontrolSlowpi

    @DebugIt()
    def read_Diag_QcontrolSlowpi(self):
        return self._Diag_QcontrolSlowpi

    @DebugIt()
    def read_Diag_IcontrolFastpi(self):
        return self._Diag_IcontrolFastpi

    @DebugIt()
    def read_Diag_QcontrolFastpi(self):
        return self._Diag_QcontrolFastpi

    @DebugIt()
    def read_Diag_VcxoPowered(self):
        return self._Diag_VcxoPowered

    @DebugIt()
    def read_Diag_VcxoRef(self):
        return self._Diag_VcxoRef

    @DebugIt()
    def read_Diag_VcxoLocked(self):
        return self._Diag_VcxoLocked

    @DebugIt()
    def read_Diag_VcxoCableDisconnected(self):
        return self._Diag_VcxoCableDisconnected

    @DebugIt()
    def read_Diag_IpolarForAmplitudeLoop(self):
        return self._Diag_IpolarForAmplitudeLoop

    @DebugIt()
    def read_Diag_QpolarForAmplitudeLoop(self):
        return self._Diag_QpolarForAmplitudeLoop

    @DebugIt()
    def read_Diag_IPolarForPhaseLoop(self):
        return self._Diag_IPolarForPhaseLoop

    @DebugIt()
    def read_Diag_QpolarForPhaseLoop(self):
        return self._Diag_QpolarForPhaseLoop

    @DebugIt()
    def read_Diag_AmpInputOfAmpLoop(self):
        return self._Diag_AmpInputOfAmpLoop

    @DebugIt()
    def read_Diag_PaseInputOfAmpLoop(self):
        return self._Diag_PaseInputOfAmpLoop

    @DebugIt()
    def read_Diag_AmpInputOfPhaseLoop(self):
        return self._Diag_AmpInputOfPhaseLoop

    @DebugIt()
    def read_Diag_PhInputOfPhaseLoop(self):
        return self._Diag_PhInputOfPhaseLoop

    @DebugIt()
    def read_Diag_AmpLoopControlOutput(self):
        return self._Diag_AmpLoopControlOutput

    @DebugIt()
    def read_Diag_AmpLoopError(self):
        return self._Diag_AmpLoopError

    @DebugIt()
    def read_Diag_AmpLoopErrorAccum(self):
        return self._Diag_AmpLoopErrorAccum

    @DebugIt()
    def read_Diag_PhLoopControlOutput(self):
        return self._Diag_PhLoopControlOutput

    @DebugIt()
    def read_Diag_PhLoopError(self):
        return self._Diag_PhLoopError

    @DebugIt()
    def read_Diag_PhLoopErrorAccum(self):
        return self._Diag_PhLoopErrorAccum

    @DebugIt()
    def read_Diag_IpolarControlOutput(self):
        return self._Diag_IpolarControlOutput

    @DebugIt()
    def read_Diag_QpolarControlOutput(self):
        return self._Diag_QpolarControlOutput

    @DebugIt()
    def read_Diag_IcontrolSlowpiIq(self):
        return self._Diag_IcontrolSlowpiIq

    @DebugIt()
    def read_Diag_QcontrolSlowpiq(self):
        return self._Diag_QcontrolSlowpiq

    @DebugIt()
    def read_Diag_IcontrolFastpiIq(self):
        return self._Diag_IcontrolFastpiIq

    @DebugIt()
    def read_Diag_QcontrolFastpiIq(self):
        return self._Diag_QcontrolFastpiIq

    @DebugIt()
    def read_Diag_IloopinputSlowpiIq(self):
        return self._Diag_IloopinputSlowpiIq

    @DebugIt()
    def read_Diag_IloopinputSlowpiIq(self):
        return self._Diag_IloopinputSlowpiIq

    @DebugIt()
    def read_Diag_Fwmin(self):
        return self._Diag_Fwmin

    @DebugIt()
    def read_Diag_MovingPlungerAuto(self):
        return self._Diag_MovingPlungerAuto

    @DebugIt()
    def read_Diag_FreqUp(self):
        return self._Diag_FreqUp

    @DebugIt()
    def read_Diag_ManualTuningOn(self):
        return self._Diag_ManualTuningOn

    @DebugIt()
    def read_Diag_ManualTuningFreqUp(self):
        return self._Diag_ManualTuningFreqUp

    @DebugIt()
    def read_Diag_EpsItckDelay(self):
        return self._Diag_EpsItckDelay

    @DebugIt()
    def read_Diag_FimItckDelay(self):
        return self._Diag_FimItckDelay

    @DebugIt()
    def read_Diag_FdlTrigHwInput(self):
        return self._Diag_FdlTrigHwInput

    @DebugIt()
    def read_Diag_FdlTrigSwInput(self):
        return self._Diag_FdlTrigSwInput

    @command
    def read_diagnostics(self):
        perseus_utils.start_reading_diagnostics(self.perseus)

        self._Diag_IcavLoops = perseus_utils.read_diag_milivolts(self.perseus, 0)
        self._Diag_QcavLoops = perseus_utils.read_diag_milivolts(self.perseus, 1)
        self._Diag_Icontrol = perseus_utils.read_diag_milivolts(self.perseus, 2)
        self._Diag_Qcontrol = perseus_utils.read_diag_milivolts(self.perseus, 3)
        self._Diag_Icontrol1 = perseus_utils.read_diag_milivolts(self.perseus, 4)
        self._Diag_Qcontrol1 = perseus_utils.read_diag_milivolts(self.perseus, 5)
        self._Diag_Icontrol2 = perseus_utils.read_diag_milivolts(self.perseus, 6)
        self._Diag_Qcontrol2 = perseus_utils.read_diag_milivolts(self.perseus, 7)
        self._Diag_Ierror = perseus_utils.read_diag_milivolts(self.perseus, 8)
        self._Diag_Qerror = perseus_utils.read_diag_milivolts(self.perseus, 9)
        self._Diag_Ierroraccum = perseus_utils.read_diag_milivolts(self.perseus, 10)
        self._Diag_Qerroraccum = perseus_utils.read_diag_milivolts(self.perseus, 11)
        self._Diag_Iref = perseus_utils.read_diag_milivolts(self.perseus, 12)
        self._Diag_Qref = perseus_utils.read_diag_milivolts(self.perseus, 13)
        self._Diag_IFwCavLoops = perseus_utils.read_diag_milivolts(self.perseus, 14)
        self._Diag_QFwCavLoops = perseus_utils.read_diag_milivolts(self.perseus, 15)
        self._Diag_IFwTet1Loops = perseus_utils.read_diag_milivolts(self.perseus, 16)
        self._Diag_QFwTet1Loops = perseus_utils.read_diag_milivolts(self.perseus, 17)
        self._Diag_IFwTet2Loops = perseus_utils.read_diag_milivolts(self.perseus, 18)
        self._Diag_QFwTet2Loops = perseus_utils.read_diag_milivolts(self.perseus, 19)
        self._Diag_IFwCircInLoops = perseus_utils.read_diag_milivolts(self.perseus, 20)
        self._Diag_QFwCircInLoops = perseus_utils.read_diag_milivolts(self.perseus, 21)
        self._Diag_Imo = perseus_utils.read_diag_milivolts(self.perseus, 22)
        self._Diag_Qmo = perseus_utils.read_diag_milivolts(self.perseus, 23)
        self._Diag_Ispare1 = perseus_utils.read_diag_milivolts(self.perseus, 24)
        self._Diag_Qspare1 = perseus_utils.read_diag_milivolts(self.perseus, 25)
        self._Diag_Ispare2 = perseus_utils.read_diag_milivolts(self.perseus, 26)
        self._Diag_Qspare2 = perseus_utils.read_diag_milivolts(self.perseus, 27)
        self._Diag_IMuxCav = perseus_utils.read_diag_milivolts(self.perseus, 28)
        self._Diag_QMuxCav = perseus_utils.read_diag_milivolts(self.perseus, 29)
        self._Diag_IMuxFwCav = perseus_utils.read_diag_milivolts(self.perseus, 30)
        self._Diag_QMuxFwCav = perseus_utils.read_diag_milivolts(self.perseus, 31)
        self._Diag_IMuxFwTet1 = perseus_utils.read_diag_milivolts(self.perseus, 32)
        self._Diag_QMuxFwTet1 = perseus_utils.read_diag_milivolts(self.perseus, 33)
        self._Diag_IMuxFwTet2 = perseus_utils.read_diag_milivolts(self.perseus, 34)
        self._Diag_QMuxFwTet2 = perseus_utils.read_diag_milivolts(self.perseus, 35)
        self._Diag_IMuxFwCircIn = perseus_utils.read_diag_milivolts(self.perseus, 36)
        self._Diag_QMuxFwCircIn = perseus_utils.read_diag_milivolts(self.perseus, 37)
        self._Diag_AmpCav = perseus_utils.read_diag_milivolts(self.perseus, 38)
        self._Diag_AmpFw = perseus_utils.read_diag_milivolts(self.perseus, 39)
        self._Diag_AngCavFw = perseus_utils.read_diag_angle(self.perseus, 40)
        self._Diag_AngCavL = perseus_utils.read_diag_angle(self.perseus, 41)
        self._Diag_AngFwL = perseus_utils.read_diag_angle(self.perseus, 42)
        self._Diag_Vaccum1 = perseus_utils.read_direct(self.perseus, 43)
        self._Diag_Vaccum2 = perseus_utils.read_direct(self.perseus, 44)
        self._Diag_IcontrolSlowpi = perseus_utils.read_diag_milivolts(self.perseus, 45)
        self._Diag_QcontrolSlowpi = perseus_utils.read_diag_milivolts(self.perseus, 46)
        self._Diag_IcontrolFastpi = perseus_utils.read_diag_milivolts(self.perseus, 47)
        self._Diag_QcontrolFastpi = perseus_utils.read_diag_milivolts(self.perseus, 48)
        self._Diag_VcxoPowered = perseus_utils.read_direct(self.perseus, 50)
        self._Diag_VcxoRef = perseus_utils.read_direct(self.perseus, 51)
        self._Diag_VcxoLocked = perseus_utils.read_direct(self.perseus, 52)
        self._Diag_VcxoCableDisconnected = perseus_utils.read_direct(self.perseus, 53)
        self._Diag_IpolarForAmplitudeLoop = perseus_utils.read_diag_milivolts(self.perseus, 100)
        self._Diag_QpolarForAmplitudeLoop = perseus_utils.read_diag_milivolts(self.perseus, 101)
        self._Diag_IPolarForPhaseLoop = perseus_utils.read_diag_milivolts(self.perseus, 102)
        self._Diag_QpolarForPhaseLoop = perseus_utils.read_diag_milivolts(self.perseus, 103)
        self._Diag_AmpInputOfAmpLoop = perseus_utils.read_diag_milivolts(self.perseus, 104)
        self._Diag_PaseInputOfAmpLoop = perseus_utils.read_diag_milivolts(self.perseus, 105)
        self._Diag_AmpInputOfPhaseLoop = perseus_utils.read_diag_milivolts(self.perseus, 106)
        self._Diag_PhInputOfPhaseLoop = perseus_utils.read_diag_milivolts(self.perseus, 107)
        self._Diag_AmpLoopControlOutput = perseus_utils.read_diag_milivolts(self.perseus, 108)
        self._Diag_AmpLoopError = perseus_utils.read_diag_milivolts(self.perseus, 109)
        self._Diag_AmpLoopErrorAccum = perseus_utils.read_diag_milivolts(self.perseus, 110)
        self._Diag_PhLoopControlOutput = perseus_utils.read_diag_milivolts(self.perseus, 111)
        self._Diag_PhLoopError = perseus_utils.read_diag_milivolts(self.perseus, 112)
        self._Diag_PhLoopErrorAccum = perseus_utils.read_diag_milivolts(self.perseus, 113)
        self._Diag_IpolarControlOutput = perseus_utils.read_diag_milivolts(self.perseus, 114)
        self._Diag_QpolarControlOutput = perseus_utils.read_diag_milivolts(self.perseus, 115)
        self._Diag_IcontrolSlowpiIq = perseus_utils.read_diag_milivolts(self.perseus, 116)
        self._Diag_QcontrolSlowpiq = perseus_utils.read_diag_milivolts(self.perseus, 117)
        self._Diag_IcontrolFastpiIq = perseus_utils.read_diag_milivolts(self.perseus, 118)
        self._Diag_QcontrolFastpiIq = perseus_utils.read_diag_milivolts(self.perseus, 119)
        self._Diag_IloopinputSlowpiIq = perseus_utils.read_diag_milivolts(self.perseus, 120)
        self._Diag_IloopinputSlowpiIq = perseus_utils.read_diag_milivolts(self.perseus, 121)
        self._Diag_Fwmin = perseus_utils.read_direct(self.perseus, 299)
        self._Diag_MovingPlungerAuto = perseus_utils.read_direct(self.perseus, 300)
        self._Diag_FreqUp = perseus_utils.read_direct(self.perseus, 301)
        self._Diag_ManualTuningOn = perseus_utils.read_direct(self.perseus, 302)
        self._Diag_ManualTuningFreqUp = perseus_utils.read_direct(self.perseus, 303)
        self._Diag_EpsItckDelay = perseus_utils.read_direct(self.perseus, 400)
        self._Diag_FimItckDelay = perseus_utils.read_direct(self.perseus, 401)
        self._Diag_FdlTrigHwInput = perseus_utils.read_direct(self.perseus, 402)
        self._Diag_FdlTrigSwInput = perseus_utils.read_direct(self.perseus, 403)

    @command
    def tuning_reset(self):
        perseus_utils.write_direct(True, TUNING_RESET_ADDRESS)
        perseus_utils.write_direct(False, TUNING_RESET_ADDRESS)

def run_device():
    run([Nutaq])

if __name__ == "__main__":
    run_device()
