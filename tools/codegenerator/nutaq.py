#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Prototype for a LLRF python device server based on the Nutaq platform"""

import time
import numpy
import math

from PyTango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from PyTango.server import Device, DeviceMeta, attribute, command, run
from PyTango.server import device_property

from nutaqattributes import attributes_dict
from nutaqdefs import *
from perseusdefs import *
from perseusloops import PerseusLoops
from perseussimulated import PerseusSimulated


class Nutaq(Device):
    __metaclass__ = DeviceMeta

    KpA = attribute(label='KpA',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=10,
                                   fget="get_KpA",
                                   fset="set_KpA",
                                   doc=""
                                   )

    KiA = attribute(label='KiA',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_KiA",
                                   fset="set_KiA",
                                   doc=""
                                   )

    PhaseShiftCav = attribute(label='PhaseShiftCav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftCav",
                                   fset="set_PhaseShiftCav",
                                   doc=""
                                   )

    PhaseShiftFwcav = attribute(label='PhaseShiftFwcav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftFwcav",
                                   fset="set_PhaseShiftFwcav",
                                   doc=""
                                   )

    PhaseShiftFwtet1 = attribute(label='PhaseShiftFwtet1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftFwtet1",
                                   fset="set_PhaseShiftFwtet1",
                                   doc=""
                                   )

    PhaseShiftFwtet2 = attribute(label='PhaseShiftFwtet2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftFwtet2",
                                   fset="set_PhaseShiftFwtet2",
                                   doc=""
                                   )

    PilimitA = attribute(label='PilimitA',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_PilimitA",
                                   fset="set_PilimitA",
                                   doc=""
                                   )

    SamplesToAverage = attribute(label='SamplesToAverage',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_SamplesToAverage",
                                   fset="set_SamplesToAverage",
                                   doc=""
                                   )

    FilterStages = attribute(label='FilterStages',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=3,
                                   fget="get_FilterStages",
                                   fset="set_FilterStages",
                                   doc=""
                                   )

    PhaseShiftFwcircin = attribute(label='PhaseShiftFwcircin',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftFwcircin",
                                   fset="set_PhaseShiftFwcircin",
                                   doc=""
                                   )

    PhaseShiftControlSignalTet1 = attribute(label='PhaseShiftControlSignalTet1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftControlSignalTet1",
                                   fset="set_PhaseShiftControlSignalTet1",
                                   doc=""
                                   )

    PhaseShiftControlSignalTet2 = attribute(label='PhaseShiftControlSignalTet2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_PhaseShiftControlSignalTet2",
                                   fset="set_PhaseShiftControlSignalTet2",
                                   doc=""
                                   )

    GainTetrode1 = attribute(label='GainTetrode1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0.1, max_value=1,
                                   fget="get_GainTetrode1",
                                   fset="set_GainTetrode1",
                                   doc=""
                                   )

    GainTetrode2 = attribute(label='GainTetrode2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0.1, max_value=1,
                                   fget="get_GainTetrode2",
                                   fset="set_GainTetrode2",
                                   doc=""
                                   )

    AutomaticStartupEnable = attribute(label='AutomaticStartupEnable',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_AutomaticStartupEnable",
                                   fset="set_AutomaticStartupEnable",
                                   doc=""
                                   )

    CommandStart = attribute(label='CommandStart',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_CommandStart",
                                   fset="set_CommandStart",
                                   doc=""
                                   )

    Amprefin = attribute(label='Amprefin',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Amprefin",
                                   fset="set_Amprefin",
                                   doc=""
                                   )

    Phrefin = attribute(label='Phrefin',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_Phrefin",
                                   fset="set_Phrefin",
                                   doc=""
                                   )

    Amprefmin = attribute(label='Amprefmin',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Amprefmin",
                                   fset="set_Amprefmin",
                                   doc=""
                                   )

    Phrefmin = attribute(label='Phrefmin',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_Phrefmin",
                                   fset="set_Phrefmin",
                                   doc=""
                                   )

    PhaseIncreaseRate = attribute(label='PhaseIncreaseRate',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_PhaseIncreaseRate",
                                   fset="set_PhaseIncreaseRate",
                                   doc=""
                                   )

    VoltageRateIncrease = attribute(label='VoltageRateIncrease',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_VoltageRateIncrease",
                                   fset="set_VoltageRateIncrease",
                                   doc=""
                                   )

    GainOl = attribute(label='GainOl',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0.5, max_value=2,
                                   fget="get_GainOl",
                                   fset="set_GainOl",
                                   doc=""
                                   )

    SpareGpioOutput01 = attribute(label='SpareGpioOutput01',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_SpareGpioOutput01",
                                   fset="set_SpareGpioOutput01",
                                   doc=""
                                   )

    SpareGpioOutput02 = attribute(label='SpareGpioOutput02',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_SpareGpioOutput02",
                                   fset="set_SpareGpioOutput02",
                                   doc=""
                                   )

    SpareGpioOutput03 = attribute(label='SpareGpioOutput03',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_SpareGpioOutput03",
                                   fset="set_SpareGpioOutput03",
                                   doc=""
                                   )

    SpareGpioOutput04 = attribute(label='SpareGpioOutput04',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_SpareGpioOutput04",
                                   fset="set_SpareGpioOutput04",
                                   doc=""
                                   )

    FdlSwTrigger = attribute(label='FdlSwTrigger',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_FdlSwTrigger",
                                   fset="set_FdlSwTrigger",
                                   doc=""
                                   )

    LoopEnableA = attribute(label='LoopEnableA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_LoopEnableA",
                                   fset="set_LoopEnableA",
                                   doc=""
                                   )

    AdcsPhaseshiftEnableA = attribute(label='AdcsPhaseshiftEnableA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_AdcsPhaseshiftEnableA",
                                   fset="set_AdcsPhaseshiftEnableA",
                                   doc=""
                                   )

    DacsPhaseShiftEnableA = attribute(label='DacsPhaseShiftEnableA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_DacsPhaseShiftEnableA",
                                   fset="set_DacsPhaseShiftEnableA",
                                   doc=""
                                   )

    SquarerefEnableA = attribute(label='SquarerefEnableA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_SquarerefEnableA",
                                   fset="set_SquarerefEnableA",
                                   doc=""
                                   )

    FreqsquareA = attribute(label='FreqsquareA',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=3, max_value=1000,
                                   fget="get_FreqsquareA",
                                   fset="set_FreqsquareA",
                                   doc=""
                                   )

    ResetkiA = attribute(label='ResetkiA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_ResetkiA",
                                   fset="set_ResetkiA",
                                   doc=""
                                   )

    LookRefA = attribute(label='LookRefA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_LookRefA",
                                   fset="set_LookRefA",
                                   doc=""
                                   )

    QuadrantSelectionA = attribute(label='QuadrantSelectionA',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=3,
                                   fget="get_QuadrantSelectionA",
                                   fset="set_QuadrantSelectionA",
                                   doc=""
                                   )

    SlowIqLoopInputSelection = attribute(label='SlowIqLoopInputSelection',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_SlowIqLoopInputSelection",
                                   fset="set_SlowIqLoopInputSelection",
                                   doc=""
                                   )

    FastIqLoopInputSelection = attribute(label='FastIqLoopInputSelection',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=3,
                                   fget="get_FastIqLoopInputSelection",
                                   fset="set_FastIqLoopInputSelection",
                                   doc=""
                                   )

    AmplitudeLoopInputSelection = attribute(label='AmplitudeLoopInputSelection',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_AmplitudeLoopInputSelection",
                                   fset="set_AmplitudeLoopInputSelection",
                                   doc=""
                                   )

    PhaseLoopInputSelection = attribute(label='PhaseLoopInputSelection',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_PhaseLoopInputSelection",
                                   fset="set_PhaseLoopInputSelection",
                                   doc=""
                                   )

    LoopsInputs = attribute(label='LoopsInputs',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_LoopsInputs",
                                   fset="set_LoopsInputs",
                                   doc=""
                                   )

    FastIqLoopEnable = attribute(label='FastIqLoopEnable',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_FastIqLoopEnable",
                                   fset="set_FastIqLoopEnable",
                                   doc=""
                                   )

    AmplitudeLoopEnable = attribute(label='AmplitudeLoopEnable',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_AmplitudeLoopEnable",
                                   fset="set_AmplitudeLoopEnable",
                                   doc=""
                                   )

    PhaseLoopEnable = attribute(label='PhaseLoopEnable',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_PhaseLoopEnable",
                                   fset="set_PhaseLoopEnable",
                                   doc=""
                                   )

    KpFastIqLoop = attribute(label='KpFastIqLoop',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=10,
                                   fget="get_KpFastIqLoop",
                                   fset="set_KpFastIqLoop",
                                   doc=""
                                   )

    KiFastIqLoop = attribute(label='KiFastIqLoop',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_KiFastIqLoop",
                                   fset="set_KiFastIqLoop",
                                   doc=""
                                   )

    KpAmpLoop = attribute(label='KpAmpLoop',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=10,
                                   fget="get_KpAmpLoop",
                                   fset="set_KpAmpLoop",
                                   doc=""
                                   )

    KiAmpLoop = attribute(label='KiAmpLoop',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_KiAmpLoop",
                                   fset="set_KiAmpLoop",
                                   doc=""
                                   )

    KpPhaseLoop = attribute(label='KpPhaseLoop',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=10,
                                   fget="get_KpPhaseLoop",
                                   fset="set_KpPhaseLoop",
                                   doc=""
                                   )

    KiPhaseLoop = attribute(label='KiPhaseLoop',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_KiPhaseLoop",
                                   fset="set_KiPhaseLoop",
                                   doc=""
                                   )

    PiLimitFastPi-Iq = attribute(label='PiLimitFastPi-Iq',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=100,
                                   fget="get_PiLimitFastPi-Iq",
                                   fset="set_PiLimitFastPi-Iq",
                                   doc=""
                                   )

    PulseModeEnableA = attribute(label='PulseModeEnableA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_PulseModeEnableA",
                                   fset="set_PulseModeEnableA",
                                   doc=""
                                   )

    AutomaticConditioningEnableA = attribute(label='AutomaticConditioningEnableA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_AutomaticConditioningEnableA",
                                   fset="set_AutomaticConditioningEnableA",
                                   doc=""
                                   )

    ConditioningdutyCicleA = attribute(label='ConditioningdutyCicleA',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=100,
                                   fget="get_ConditioningdutyCicleA",
                                   fset="set_ConditioningdutyCicleA",
                                   doc=""
                                   )

    TuningEnableA = attribute(label='TuningEnableA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_TuningEnableA",
                                   fset="set_TuningEnableA",
                                   doc=""
                                   )

    TuningPosEnA = attribute(label='TuningPosEnA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_TuningPosEnA",
                                   fset="set_TuningPosEnA",
                                   doc=""
                                   )

    NumStepsA = attribute(label='NumStepsA',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=65535,
                                   fget="get_NumStepsA",
                                   fset="set_NumStepsA",
                                   doc=""
                                   )

    PulsesFrequency = attribute(label='PulsesFrequency',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_PulsesFrequency",
                                   fset="set_PulsesFrequency",
                                   doc=""
                                   )

    PhaseOffsetA = attribute(label='PhaseOffsetA',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=180,
                                   fget="get_PhaseOffsetA",
                                   fset="set_PhaseOffsetA",
                                   doc=""
                                   )

    MoveA = attribute(label='MoveA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_MoveA",
                                   fset="set_MoveA",
                                   doc=""
                                   )

    MoveupA = attribute(label='MoveupA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_MoveupA",
                                   fset="set_MoveupA",
                                   doc=""
                                   )

    TuningresetA = attribute(label='TuningresetA',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_TuningresetA",
                                   fset="set_TuningresetA",
                                   doc=""
                                   )

    Fwmina = attribute(label='Fwmina',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Fwmina",
                                   fset="set_Fwmina",
                                   doc=""
                                   )

    MarginupA = attribute(label='MarginupA',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=10,
                                   fget="get_MarginupA",
                                   fset="set_MarginupA",
                                   doc=""
                                   )

    MarginlowA = attribute(label='MarginlowA',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=5,
                                   fget="get_MarginlowA",
                                   fset="set_MarginlowA",
                                   doc=""
                                   )

    EpsItckDisable = attribute(label='EpsItckDisable',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_EpsItckDisable",
                                   fset="set_EpsItckDisable",
                                   doc=""
                                   )

    FimItckDisable = attribute(label='FimItckDisable',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_FimItckDisable",
                                   fset="set_FimItckDisable",
                                   doc=""
                                   )

    MDivider = attribute(label='MDivider',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=128,
                                   fget="get_MDivider",
                                   fset="set_MDivider",
                                   doc=""
                                   )

    NDivider = attribute(label='NDivider',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=128,
                                   fget="get_NDivider",
                                   fset="set_NDivider",
                                   doc=""
                                   )

    Muxsel = attribute(label='Muxsel',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Muxsel",
                                   fset="set_Muxsel",
                                   doc=""
                                   )

    Mux0Divider = attribute(label='Mux0Divider',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux0Divider",
                                   fset="set_Mux0Divider",
                                   doc=""
                                   )

    Mux1Divider = attribute(label='Mux1Divider',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux1Divider",
                                   fset="set_Mux1Divider",
                                   doc=""
                                   )

    Mux2Divider = attribute(label='Mux2Divider',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux2Divider",
                                   fset="set_Mux2Divider",
                                   doc=""
                                   )

    Mux3Divider = attribute(label='Mux3Divider',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux3Divider",
                                   fset="set_Mux3Divider",
                                   doc=""
                                   )

    Mux4Divider = attribute(label='Mux4Divider',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux4Divider",
                                   fset="set_Mux4Divider",
                                   doc=""
                                   )

    SendWord = attribute(label='SendWord',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_SendWord",
                                   fset="set_SendWord",
                                   doc=""
                                   )

    Cpdir = attribute(label='Cpdir',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Cpdir",
                                   fset="set_Cpdir",
                                   doc=""
                                   )

    VcxoOutputInversion = attribute(label='VcxoOutputInversion',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_VcxoOutputInversion",
                                   fset="set_VcxoOutputInversion",
                                   doc=""
                                   )

    IcavLoops = attribute(label='IcavLoops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QcavLoops = attribute(label='QcavLoops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Icontrol = attribute(label='Icontrol',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qcontrol = attribute(label='Qcontrol',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Icontrol1 = attribute(label='Icontrol1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qcontrol1 = attribute(label='Qcontrol1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Icontrol2 = attribute(label='Icontrol2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qcontrol2 = attribute(label='Qcontrol2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Ierror = attribute(label='Ierror',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qerror = attribute(label='Qerror',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Ierroraccum = attribute(label='Ierroraccum',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qerroraccum = attribute(label='Qerroraccum',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Iref = attribute(label='Iref',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qref = attribute(label='Qref',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    IFwCavLoops = attribute(label='IFwCavLoops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QFwCavLoops = attribute(label='QFwCavLoops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    IFwTet1Loops = attribute(label='IFwTet1Loops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QFwTet1Loops = attribute(label='QFwTet1Loops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    IFwTet2Loops = attribute(label='IFwTet2Loops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QFwTet2Loops = attribute(label='QFwTet2Loops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    IFwCircInLoops = attribute(label='IFwCircInLoops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QFwCircInLoops = attribute(label='QFwCircInLoops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Imo = attribute(label='Imo',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qmo = attribute(label='Qmo',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Ispare1 = attribute(label='Ispare1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qspare1 = attribute(label='Qspare1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Ispare2 = attribute(label='Ispare2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qspare2 = attribute(label='Qspare2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    IMuxCav = attribute(label='IMuxCav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QMuxCav = attribute(label='QMuxCav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    IMuxFwCav = attribute(label='IMuxFwCav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QMuxFwCav = attribute(label='QMuxFwCav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    IMuxFwTet1 = attribute(label='IMuxFwTet1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QMuxFwTet1 = attribute(label='QMuxFwTet1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    IMuxFwTet2 = attribute(label='IMuxFwTet2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QMuxFwTet2 = attribute(label='QMuxFwTet2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    IMuxFwCircIn = attribute(label='IMuxFwCircIn',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QMuxFwCircIn = attribute(label='QMuxFwCircIn',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    AmpCav = attribute(label='AmpCav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    AmpFw = attribute(label='AmpFw',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    AngCavFw = attribute(label='AngCavFw',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    AngCavL = attribute(label='AngCavL',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    AngFwL = attribute(label='AngFwL',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Vaccum1 = attribute(label='Vaccum1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Vaccum2 = attribute(label='Vaccum2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    VcxoPowered = attribute(label='VcxoPowered',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    VcxoRef = attribute(label='VcxoRef',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    VcxoLocked = attribute(label='VcxoLocked',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    VcxoCableDisconnected = attribute(label='VcxoCableDisconnected',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    TuningOn = attribute(label='TuningOn',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    TuningOnFwMinTuningEnableLatch = attribute(label='TuningOnFwMinTuningEnableLatch',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    FreqUp = attribute(label='FreqUp',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    ManualTuningOn = attribute(label='ManualTuningOn',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    ManualTuningFreqUp = attribute(label='ManualTuningFreqUp',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    EpsItckDelay = attribute(label='EpsItckDelay',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    FimItckDelay = attribute(label='FimItckDelay',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    FdlTrigHwInput = attribute(label='FdlTrigHwInput',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    FdlTrigSwInput = attribute(label='FdlTrigSwInput',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )


    isSimulated = device_property(dtype=bool, default_value=False)

    def init_device(self):
        try:
            if self.isSimulated:
                self.perseus = PerseusSimulated()
            else:
                self.perseus = PerseusLoops()
            self.set_state(DevState.ON)
        except Exception, e:
            print e
            self.set_state(DevState.FAULT)

    def read_angle(self, address):
        # =IF(P6>32767;(P6-65536)/32767*180;P6/32767*180)

        self.perseus.write(SETTINGS_READ_OFFSET, address)
        value = self.perseus.read(SETTINGS_READ_OFFSET)

        if value > 32767:
            angle = (value - 65536) * 180.0 / 32767
        else:
            angle = (value * 180.0) / 32767

        return angle

    def write_angle(self, value, address):
        """=ROUND(IF(
                     E6<0; E6/180*32767+65536;
                     IF(E6<=180; E6/180*32767;
                       (E6-360)/180*32767+65536)
                    );0
                )
        """
        if value < 0:
            angle = (value * 32767 / 180.0) + 65536
        elif value <= 180.0:
            angle = (value * 32767) / 180.0
        else:
            angle = ((value - 360) * 32767 / 180.0) + 65536

        value = address << 17 | int(angle)
        self.perseus.write(SETTINGS_WRITE_OFFSET, value)

    def read_milivolts(self, address):
        """
            This method converts the value readed from a register in milivolts usign the following formula:
            VALUE = ROUND(P23*1000/32767*1,6467602581;0)
        :param value: value read from a register.
        :return: value converted in milivolts
        """
        self.perseus.write(SETTINGS_READ_OFFSET, address)
        value = self.perseus.read(SETTINGS_READ_OFFSET)

        milis = value * 1000.0 / 32767 * 1.6467602581
        return milis

    def write_milivolts(self, milivolts, address):
        """
            This method converts the value from milivolts to bit to be written in the register usign the following
            formula:
            VALUE =ROUND(E23/1000*32767/1,6467602581;0)
        :param value: value to be converted.
        :return: value to write in the register.
        """
        value = (milivolts * 32767 / 1.6467602581) / 1000.0

        value = address << 17 | int(value)
        self.perseus.write(SETTINGS_WRITE_OFFSET, value)

    def read_direct(self, address):
        self.perseus.write(SETTINGS_READ_OFFSET, address)
        value = self.perseus.read(SETTINGS_READ_OFFSET)
        return value

    def write_direct(self, value, address):
        value = address << 17 | int(value)
        self.perseus.write(SETTINGS_WRITE_OFFSET, value)

    def read_diag_angle(self, address):
        self.perseus.write(DIAGNOSTICS_OFFSET, address)
        value = self.perseus.read(DIAGNOSTICS_OFFSET)
        # =IF(D49>32767;
        #    (D49-65536)/32767*180;
        #     D49/32767*180)
        if value > 32767:
            angle = (value - (1 << 16)) * 180.0 / 32767
        else:
            angle = value * 180.0 / 32767
        return angle

    def read_diag_milivolts(self, address):
        self.perseus.write(DIAGNOSTICS_OFFSET, address)
        value = self.perseus.read(DIAGNOSTICS_OFFSET)
        #and now convert the value
        #=IF(D9<32768;
        #    D9/32767*1000;
        #   (D9-2^16)/32767*1000)
        if value < 32768:
            milis = value * 1000.0 / 32767
        else:
            milis = ((value - (1 << 16)) * 1000.0) / 32767
        return milis

    def calc_amplitude(self, ivalue, qvalue):
        amplitude = math.sqrt((ivalue**2) + (qvalue**2))
        return amplitude

    def calc_phase(self, ivalue, qvalue):
        phase = math.atan2(qvalue, ivalue)
        return phase


    @DebugIt()
    def get_KpA(self):
        return self.read_direct(0)


    @DebugIt()
    def get_KiA(self):
        return self.read_direct(1)


    @DebugIt()
    def get_PhaseShiftCav(self):
        return self.read_angle(2)


    @DebugIt()
    def get_PhaseShiftFwcav(self):
        return self.read_angle(3)


    @DebugIt()
    def get_PhaseShiftFwtet1(self):
        return self.read_angle(4)


    @DebugIt()
    def get_PhaseShiftFwtet2(self):
        return self.read_angle(5)


    @DebugIt()
    def get_PilimitA(self):
        return self.read_milivolts(6)


    @DebugIt()
    def get_SamplesToAverage(self):
        return self.read_direct(7)


    @DebugIt()
    def get_FilterStages(self):
        return self.read_direct(8)


    @DebugIt()
    def get_PhaseShiftFwcircin(self):
        return self.read_angle(9)


    @DebugIt()
    def get_PhaseShiftControlSignalTet1(self):
        return self.read_angle(10)


    @DebugIt()
    def get_PhaseShiftControlSignalTet2(self):
        return self.read_angle(11)


    @DebugIt()
    def get_GainTetrode1(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_GainTetrode2(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_AutomaticStartupEnable(self):
        return self.read_direct(15)


    @DebugIt()
    def get_CommandStart(self):
        return self.read_direct(16)


    @DebugIt()
    def get_Amprefin(self):
        return self.read_milivolts(19)


    @DebugIt()
    def get_Phrefin(self):
        return self.read_angle(20)


    @DebugIt()
    def get_Amprefmin(self):
        return self.read_milivolts(21)


    @DebugIt()
    def get_Phrefmin(self):
        return self.read_angle(22)


    @DebugIt()
    def get_PhaseIncreaseRate(self):
        return self.read_direct(23)


    @DebugIt()
    def get_VoltageRateIncrease(self):
        return self.read_direct(24)


    @DebugIt()
    def get_GainOl(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_SpareGpioOutput01(self):
        return self.read_direct(28)


    @DebugIt()
    def get_SpareGpioOutput02(self):
        return self.read_direct(29)


    @DebugIt()
    def get_SpareGpioOutput03(self):
        return self.read_direct(30)


    @DebugIt()
    def get_SpareGpioOutput04(self):
        return self.read_direct(31)


    @DebugIt()
    def get_FdlSwTrigger(self):
        return self.read_direct(32)


    @DebugIt()
    def get_LoopEnableA(self):
        return self.read_direct(100)


    @DebugIt()
    def get_AdcsPhaseshiftEnableA(self):
        return self.read_direct(101)


    @DebugIt()
    def get_DacsPhaseShiftEnableA(self):
        return self.read_direct(102)


    @DebugIt()
    def get_SquarerefEnableA(self):
        return self.read_direct(103)


    @DebugIt()
    def get_FreqsquareA(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_ResetkiA(self):
        return self.read_direct(105)


    @DebugIt()
    def get_LookRefA(self):
        return self.read_direct(106)


    @DebugIt()
    def get_QuadrantSelectionA(self):
        return self.read_direct(107)


    @DebugIt()
    def get_SlowIqLoopInputSelection(self):
        return self.read_direct(110)


    @DebugIt()
    def get_FastIqLoopInputSelection(self):
        return self.read_direct(111)


    @DebugIt()
    def get_AmplitudeLoopInputSelection(self):
        return self.read_direct(112)


    @DebugIt()
    def get_PhaseLoopInputSelection(self):
        return self.read_direct(113)


    @DebugIt()
    def get_LoopsInputs(self):
        return self.read_direct(114)


    @DebugIt()
    def get_FastIqLoopEnable(self):
        return self.read_direct(115)


    @DebugIt()
    def get_AmplitudeLoopEnable(self):
        return self.read_direct(116)


    @DebugIt()
    def get_PhaseLoopEnable(self):
        return self.read_direct(117)


    @DebugIt()
    def get_KpFastIqLoop(self):
        return self.read_direct(118)


    @DebugIt()
    def get_KiFastIqLoop(self):
        return self.read_direct(119)


    @DebugIt()
    def get_KpAmpLoop(self):
        return self.read_direct(120)


    @DebugIt()
    def get_KiAmpLoop(self):
        return self.read_direct(121)


    @DebugIt()
    def get_KpPhaseLoop(self):
        return self.read_direct(122)


    @DebugIt()
    def get_KiPhaseLoop(self):
        return self.read_direct(123)


    @DebugIt()
    def get_PiLimitFastPi-Iq(self):
        return self.read_milivolts(124)


    @DebugIt()
    def get_PulseModeEnableA(self):
        return self.read_direct(200)


    @DebugIt()
    def get_AutomaticConditioningEnableA(self):
        return self.read_direct(201)


    @DebugIt()
    def get_ConditioningdutyCicleA(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_TuningEnableA(self):
        return self.read_direct(300)


    @DebugIt()
    def get_TuningPosEnA(self):
        return self.read_direct(301)


    @DebugIt()
    def get_NumStepsA(self):
        return self.read_direct(302)


    @DebugIt()
    def get_PulsesFrequency(self):
        return self.read_direct(303)


    @DebugIt()
    def get_PhaseOffsetA(self):
        return self.read_angle(304)


    @DebugIt()
    def get_MoveA(self):
        return self.read_direct(305)


    @DebugIt()
    def get_MoveupA(self):
        return self.read_direct(306)


    @DebugIt()
    def get_TuningresetA(self):
        return self.read_direct(307)


    @DebugIt()
    def get_Fwmina(self):
        return self.read_direct(308)


    @DebugIt()
    def get_MarginupA(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_MarginlowA(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_EpsItckDisable(self):
        return self.read_direct(400)


    @DebugIt()
    def get_FimItckDisable(self):
        return self.read_direct(401)


    @DebugIt()
    def get_MDivider(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_NDivider(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_Muxsel(self):
        return self.read_direct(502)


    @DebugIt()
    def get_Mux0Divider(self):
        return self.read_direct(503)


    @DebugIt()
    def get_Mux1Divider(self):
        return self.read_direct(504)


    @DebugIt()
    def get_Mux2Divider(self):
        return self.read_direct(505)


    @DebugIt()
    def get_Mux3Divider(self):
        return self.read_direct(506)


    @DebugIt()
    def get_Mux4Divider(self):
        return self.read_direct(507)


    @DebugIt()
    def get_SendWord(self):
        return self.read_direct(508)


    @DebugIt()
    def get_Cpdir(self):
        return self.read_direct(509)


    @DebugIt()
    def get_VcxoOutputInversion(self):
        return self.read_direct(510)


    @DebugIt()
    def read_IcavLoops(self):
        return self._IcavLoops

    @DebugIt()
    def read_QcavLoops(self):
        return self._QcavLoops

    @DebugIt()
    def read_Icontrol(self):
        return self._Icontrol

    @DebugIt()
    def read_Qcontrol(self):
        return self._Qcontrol

    @DebugIt()
    def read_Icontrol1(self):
        return self._Icontrol1

    @DebugIt()
    def read_Qcontrol1(self):
        return self._Qcontrol1

    @DebugIt()
    def read_Icontrol2(self):
        return self._Icontrol2

    @DebugIt()
    def read_Qcontrol2(self):
        return self._Qcontrol2

    @DebugIt()
    def read_Ierror(self):
        return self._Ierror

    @DebugIt()
    def read_Qerror(self):
        return self._Qerror

    @DebugIt()
    def read_Ierroraccum(self):
        return self._Ierroraccum

    @DebugIt()
    def read_Qerroraccum(self):
        return self._Qerroraccum

    @DebugIt()
    def read_Iref(self):
        return self._Iref

    @DebugIt()
    def read_Qref(self):
        return self._Qref

    @DebugIt()
    def read_IFwCavLoops(self):
        return self._IFwCavLoops

    @DebugIt()
    def read_QFwCavLoops(self):
        return self._QFwCavLoops

    @DebugIt()
    def read_IFwTet1Loops(self):
        return self._IFwTet1Loops

    @DebugIt()
    def read_QFwTet1Loops(self):
        return self._QFwTet1Loops

    @DebugIt()
    def read_IFwTet2Loops(self):
        return self._IFwTet2Loops

    @DebugIt()
    def read_QFwTet2Loops(self):
        return self._QFwTet2Loops

    @DebugIt()
    def read_IFwCircInLoops(self):
        return self._IFwCircInLoops

    @DebugIt()
    def read_QFwCircInLoops(self):
        return self._QFwCircInLoops

    @DebugIt()
    def read_Imo(self):
        return self._Imo

    @DebugIt()
    def read_Qmo(self):
        return self._Qmo

    @DebugIt()
    def read_Ispare1(self):
        return self._Ispare1

    @DebugIt()
    def read_Qspare1(self):
        return self._Qspare1

    @DebugIt()
    def read_Ispare2(self):
        return self._Ispare2

    @DebugIt()
    def read_Qspare2(self):
        return self._Qspare2

    @DebugIt()
    def read_IMuxCav(self):
        return self._IMuxCav

    @DebugIt()
    def read_QMuxCav(self):
        return self._QMuxCav

    @DebugIt()
    def read_IMuxFwCav(self):
        return self._IMuxFwCav

    @DebugIt()
    def read_QMuxFwCav(self):
        return self._QMuxFwCav

    @DebugIt()
    def read_IMuxFwTet1(self):
        return self._IMuxFwTet1

    @DebugIt()
    def read_QMuxFwTet1(self):
        return self._QMuxFwTet1

    @DebugIt()
    def read_IMuxFwTet2(self):
        return self._IMuxFwTet2

    @DebugIt()
    def read_QMuxFwTet2(self):
        return self._QMuxFwTet2

    @DebugIt()
    def read_IMuxFwCircIn(self):
        return self._IMuxFwCircIn

    @DebugIt()
    def read_QMuxFwCircIn(self):
        return self._QMuxFwCircIn

    @DebugIt()
    def read_AmpCav(self):
        return self._AmpCav

    @DebugIt()
    def read_AmpFw(self):
        return self._AmpFw

    @DebugIt()
    def read_AngCavFw(self):
        return self._AngCavFw

    @DebugIt()
    def read_AngCavL(self):
        return self._AngCavL

    @DebugIt()
    def read_AngFwL(self):
        return self._AngFwL

    @DebugIt()
    def read_Vaccum1(self):
        return self._Vaccum1

    @DebugIt()
    def read_Vaccum2(self):
        return self._Vaccum2

    @DebugIt()
    def read_VcxoPowered(self):
        return self._VcxoPowered

    @DebugIt()
    def read_VcxoRef(self):
        return self._VcxoRef

    @DebugIt()
    def read_VcxoLocked(self):
        return self._VcxoLocked

    @DebugIt()
    def read_VcxoCableDisconnected(self):
        return self._VcxoCableDisconnected

    @DebugIt()
    def read_TuningOn(self):
        return self._TuningOn

    @DebugIt()
    def read_TuningOnFwMinTuningEnableLatch(self):
        return self._TuningOnFwMinTuningEnableLatch

    @DebugIt()
    def read_FreqUp(self):
        return self._FreqUp

    @DebugIt()
    def read_ManualTuningOn(self):
        return self._ManualTuningOn

    @DebugIt()
    def read_ManualTuningFreqUp(self):
        return self._ManualTuningFreqUp

    @DebugIt()
    def read_EpsItckDelay(self):
        return self._EpsItckDelay

    @DebugIt()
    def read_FimItckDelay(self):
        return self._FimItckDelay

    @DebugIt()
    def read_FdlTrigHwInput(self):
        return self._FdlTrigHwInput

    @DebugIt()
    def read_FdlTrigSwInput(self):
        return self._FdlTrigSwInput

    @command
    def read_diagnostics(self):
        self.start_reading_diagnostics()

        self._IcavLoops = self.read_diag_milivolts(0)
        self._QcavLoops = self.read_diag_milivolts(1)
        self._Icontrol = self.read_diag_milivolts(2)
        self._Qcontrol = self.read_diag_milivolts(3)
        self._Icontrol1 = self.read_diag_milivolts(4)
        self._Qcontrol1 = self.read_diag_milivolts(5)
        self._Icontrol2 = self.read_diag_milivolts(6)
        self._Qcontrol2 = self.read_diag_milivolts(7)
        self._Ierror = self.read_diag_milivolts(8)
        self._Qerror = self.read_diag_milivolts(9)
        self._Ierroraccum = self.read_diag_milivolts(10)
        self._Qerroraccum = self.read_diag_milivolts(11)
        self._Iref = self.read_diag_milivolts(12)
        self._Qref = self.read_diag_milivolts(13)
        self._IFwCavLoops = self.read_diag_milivolts(14)
        self._QFwCavLoops = self.read_diag_milivolts(15)
        self._IFwTet1Loops = self.read_diag_milivolts(16)
        self._QFwTet1Loops = self.read_diag_milivolts(17)
        self._IFwTet2Loops = self.read_diag_milivolts(18)
        self._QFwTet2Loops = self.read_diag_milivolts(19)
        self._IFwCircInLoops = self.read_diag_milivolts(20)
        self._QFwCircInLoops = self.read_diag_milivolts(21)
        self._Imo = self.read_diag_milivolts(22)
        self._Qmo = self.read_diag_milivolts(23)
        self._Ispare1 = self.read_diag_milivolts(24)
        self._Qspare1 = self.read_diag_milivolts(25)
        self._Ispare2 = self.read_diag_milivolts(26)
        self._Qspare2 = self.read_diag_milivolts(27)
        self._IMuxCav = self.read_diag_milivolts(28)
        self._QMuxCav = self.read_diag_milivolts(29)
        self._IMuxFwCav = self.read_diag_milivolts(30)
        self._QMuxFwCav = self.read_diag_milivolts(31)
        self._IMuxFwTet1 = self.read_diag_milivolts(32)
        self._QMuxFwTet1 = self.read_diag_milivolts(33)
        self._IMuxFwTet2 = self.read_diag_milivolts(34)
        self._QMuxFwTet2 = self.read_diag_milivolts(35)
        self._IMuxFwCircIn = self.read_diag_milivolts(36)
        self._QMuxFwCircIn = self.read_diag_milivolts(37)
        self._AmpCav = self.read_diag_milivolts(38)
        self._AmpFw = self.read_diag_milivolts(39)
        self._AngCavFw = self.read_diag_angle(40)
        self._AngCavL = self.read_diag_angle(41)
        self._AngFwL = self.read_diag_angle(42)
        self._Vaccum1 = self.read_direct(43)
        self._Vaccum2 = self.read_direct(44)
        self._VcxoPowered = self.read_direct(50)
        self._VcxoRef = self.read_direct(51)
        self._VcxoLocked = self.read_direct(52)
        self._VcxoCableDisconnected = self.read_direct(53)
        self._TuningOn = self.read_direct(299)
        self._TuningOnFwMinTuningEnableLatch = self.read_direct(300)
        self._FreqUp = self.read_direct(301)
        self._ManualTuningOn = self.read_direct(302)
        self._ManualTuningFreqUp = self.read_direct(303)
        self._EpsItckDelay = self.read_direct(400)
        self._FimItckDelay = self.read_direct(401)
        self._FdlTrigHwInput = self.read_direct(402)
        self._FdlTrigSwInput = self.read_direct(403)

    @command
    def tuning_reset(self):
        self.write_direct(True, TUNING_RESET_ADDRESS)
        self.write_direct(False, TUNING_RESET_ADDRESS)

    def start_reading_diagnostics(self):
        value = 1 << 16
        self.perseus.write(DIAGNOSTICS_OFFSET, value)
        #@warning: I know ... this is not needed
        value = 0 << 16
        #lets continue
        self.perseus.write(DIAGNOSTICS_OFFSET, value)

    def end_reading_diagnostics(self):
        value = 1 << 16
        self.perseus.write(DIAGNOSTICS_OFFSET, value)

if __name__ == "__main__":
    run([Nutaq])
