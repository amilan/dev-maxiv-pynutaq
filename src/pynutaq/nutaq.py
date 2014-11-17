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

from perseus import Perseus


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
                         unit='mV',
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

    VoltageRateIncrease = attribute(label='VoltageRateIncrease',
                                    dtype=int,
                                    display_level=DispLevel.OPERATOR,
                                    access=AttrWriteType.READ_WRITE,
                                    unit='',
                                    format='6.4f',
                                    min_value=0, max_value=7,
                                    fget="get_VoltageRateIncrease",
                                    fset="set_VoltageRateIncrease",
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

    LoopEnableA = attribute(label='LoopEnableA',
                            dtype=bool,
                            display_level=DispLevel.OPERATOR,
                            access=AttrWriteType.READ_WRITE,
                            unit='',
                            format='6.4f',
                            fget="get_LoopEnableA",
                            fset="set_LoopEnableA",
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

    LoopsInputs = attribute(label='LoopsInputs',
                            dtype=bool,
                            display_level=DispLevel.OPERATOR,
                            access=AttrWriteType.READ_WRITE,
                            unit='',
                            format='6.4f',
                            fget="get_LoopsInputs",
                            fset="set_LoopsInputs",
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
                             min_value=0, max_value=10,
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
                          min_value=0, max_value=10,
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
                            min_value=0, max_value=10,
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
                                min_value=0, max_value=100,
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
                             min_value=-180, max_value=180,
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
                          unit='',
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
                           unit='',
                           format='6.4f',
                           min_value=0, max_value=5,
                           fget="get_MarginlowA",
                           fset="set_MarginlowA",
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

    Diag_TuningOn = attribute(label='Diag_TuningOn',
                              dtype=float,
                              display_level=DispLevel.OPERATOR,
                              access=AttrWriteType.READ,
                              unit='',
                              format='6.4f',
                              doc=""
    )

    Diag_TuningOnFwMinTuningEnableLatch = attribute(label='Diag_TuningOnFwMinTuningEnableLatch',
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

    def init_device(self):
        Device.init_device(self)
        try:
            self.perseus = Perseus().new_perseus(self.perseusType)
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
    def set_KpA(self, KpA):
        self.write_direct(KpA, 0)

    @DebugIt()
    def get_KiA(self):
        return self.read_direct(1)

    @DebugIt()
    def set_KiA(self, KiA):
        self.write_direct(KiA, 1)

    @DebugIt()
    def get_PhaseShiftCav(self):
        return self.read_angle(2)

    @DebugIt()
    def set_PhaseShiftCav(self, PhaseShiftCav):
        self.write_angle(PhaseShiftCav, 2)

    @DebugIt()
    def get_PhaseShiftFwcav(self):
        return self.read_angle(3)

    @DebugIt()
    def set_PhaseShiftFwcav(self, PhaseShiftFwcav):
        self.write_angle(PhaseShiftFwcav, 3)

    @DebugIt()
    def get_PhaseShiftFwtet1(self):
        return self.read_angle(4)

    @DebugIt()
    def set_PhaseShiftFwtet1(self, PhaseShiftFwtet1):
        self.write_angle(PhaseShiftFwtet1, 4)

    @DebugIt()
    def get_PhaseShiftFwtet2(self):
        return self.read_angle(5)

    @DebugIt()
    def set_PhaseShiftFwtet2(self, PhaseShiftFwtet2):
        self.write_angle(PhaseShiftFwtet2, 5)

    @DebugIt()
    def get_PilimitA(self):
        return self.read_milivolts(6)

    @DebugIt()
    def set_PilimitA(self, PilimitA):
        self.write_milivolts(PilimitA, 6)

    @DebugIt()
    def get_SamplesToAverage(self):
        return self.read_direct(7)

    @DebugIt()
    def set_SamplesToAverage(self, SamplesToAverage):
        self.write_direct(SamplesToAverage, 7)

    @DebugIt()
    def get_FilterStages(self):
        return self.read_direct(8)

    @DebugIt()
    def set_FilterStages(self, FilterStages):
        self.write_direct(FilterStages, 8)

    @DebugIt()
    def get_PhaseShiftFwcircin(self):
        return self.read_angle(9)

    @DebugIt()
    def set_PhaseShiftFwcircin(self, PhaseShiftFwcircin):
        self.write_angle(PhaseShiftFwcircin, 9)

    @DebugIt()
    def get_PhaseShiftControlSignalTet1(self):
        return self.read_angle(10)

    @DebugIt()
    def set_PhaseShiftControlSignalTet1(self, PhaseShiftControlSignalTet1):
        self.write_angle(PhaseShiftControlSignalTet1, 10)

    @DebugIt()
    def get_PhaseShiftControlSignalTet2(self):
        return self.read_angle(11)

    @DebugIt()
    def set_PhaseShiftControlSignalTet2(self, PhaseShiftControlSignalTet2):
        self.write_angle(PhaseShiftControlSignalTet2, 11)

    @DebugIt()
    def get_GainTetrode1(self):
        #start protected zone ====
        self.perseus.write(SETTINGS_READ_OFFSET, 13)
        value = self.perseus.read(SETTINGS_READ_OFFSET) / 19898.0
        return value
        #end protected zone ====

    @DebugIt()
    def set_GainTetrode1(self, GainTetrode1):
        #start protected zone ====
        value = 13 << 17 | (int(GainTetrode1) * 19898)
        self.perseus.write(SETTINGS_WRITE_OFFSET, value)
        #end protected zone ====

    @DebugIt()
    def get_GainTetrode2(self):
        #start protected zone ====
        self.perseus.write(SETTINGS_READ_OFFSET, 14)
        value = self.perseus.read(SETTINGS_READ_OFFSET) / 19898.0
        return value
        #end protected zone ====

    @DebugIt()
    def set_GainTetrode2(self, GainTetrode2):
        #start protected zone ====
        value = 14 << 17 | (int(GainTetrode2) * 19898)
        self.perseus.write(SETTINGS_WRITE_OFFSET, value)
        #end protected zone ====

    @DebugIt()
    def get_AutomaticStartupEnable(self):
        return self.read_direct(15)

    @DebugIt()
    def set_AutomaticStartupEnable(self, AutomaticStartupEnable):
        self.write_direct(AutomaticStartupEnable, 15)

    @DebugIt()
    def get_CommandStart(self):
        return self.read_direct(16)

    @DebugIt()
    def set_CommandStart(self, CommandStart):
        self.write_direct(CommandStart, 16)

    @DebugIt()
    def get_Amprefin(self):
        return self.read_milivolts(19)

    @DebugIt()
    def set_Amprefin(self, Amprefin):
        self.write_milivolts(Amprefin, 19)

    @DebugIt()
    def get_Phrefin(self):
        return self.read_angle(20)

    @DebugIt()
    def set_Phrefin(self, Phrefin):
        self.write_angle(Phrefin, 20)

    @DebugIt()
    def get_Amprefmin(self):
        return self.read_milivolts(21)

    @DebugIt()
    def set_Amprefmin(self, Amprefmin):
        self.write_milivolts(Amprefmin, 21)

    @DebugIt()
    def get_Phrefmin(self):
        return self.read_angle(22)

    @DebugIt()
    def set_Phrefmin(self, Phrefmin):
        self.write_angle(Phrefmin, 22)

    @DebugIt()
    def get_PhaseIncreaseRate(self):
        return self.read_direct(23)

    @DebugIt()
    def set_PhaseIncreaseRate(self, PhaseIncreaseRate):
        self.write_direct(PhaseIncreaseRate, 23)

    @DebugIt()
    def get_VoltageRateIncrease(self):
        return self.read_direct(24)

    @DebugIt()
    def set_VoltageRateIncrease(self, VoltageRateIncrease):
        self.write_direct(VoltageRateIncrease, 24)

    @DebugIt()
    def get_GainOl(self):
        # start protected zone ====
        self.perseus.write(SETTINGS_READ_OFFSET, 25)
        value = self.perseus.read(SETTINGS_READ_OFFSET)
        return value
        # end protected zone ====

    @DebugIt()
    def set_GainOl(self, GainOl):
        # start protected zone ====
        value = 25 << 17 | int(value)
        self.perseus.write(SETTINGS_WRITE_OFFSET, value)
        # end protected zone ====

    @DebugIt()
    def get_SpareGpioOutput01(self):
        return self.read_direct(28)

    @DebugIt()
    def set_SpareGpioOutput01(self, SpareGpioOutput01):
        self.write_direct(SpareGpioOutput01, 28)

    @DebugIt()
    def get_SpareGpioOutput02(self):
        return self.read_direct(29)

    @DebugIt()
    def set_SpareGpioOutput02(self, SpareGpioOutput02):
        self.write_direct(SpareGpioOutput02, 29)

    @DebugIt()
    def get_SpareGpioOutput03(self):
        return self.read_direct(30)

    @DebugIt()
    def set_SpareGpioOutput03(self, SpareGpioOutput03):
        self.write_direct(SpareGpioOutput03, 30)

    @DebugIt()
    def get_SpareGpioOutput04(self):
        return self.read_direct(31)

    @DebugIt()
    def set_SpareGpioOutput04(self, SpareGpioOutput04):
        self.write_direct(SpareGpioOutput04, 31)

    @DebugIt()
    def get_FdlSwTrigger(self):
        return self.read_direct(32)

    @DebugIt()
    def set_FdlSwTrigger(self, FdlSwTrigger):
        self.write_direct(FdlSwTrigger, 32)

    @DebugIt()
    def get_LoopEnableA(self):
        return self.read_direct(100)

    @DebugIt()
    def set_LoopEnableA(self, LoopEnableA):
        self.write_direct(LoopEnableA, 100)

    @DebugIt()
    def get_AdcsPhaseshiftEnableA(self):
        return self.read_direct(101)

    @DebugIt()
    def set_AdcsPhaseshiftEnableA(self, AdcsPhaseshiftEnableA):
        self.write_direct(AdcsPhaseshiftEnableA, 101)

    @DebugIt()
    def get_DacsPhaseShiftEnableA(self):
        return self.read_direct(102)

    @DebugIt()
    def set_DacsPhaseShiftEnableA(self, DacsPhaseShiftEnableA):
        self.write_direct(DacsPhaseShiftEnableA, 102)

    @DebugIt()
    def get_SquarerefEnableA(self):
        return self.read_direct(103)

    @DebugIt()
    def set_SquarerefEnableA(self, SquarerefEnableA):
        self.write_direct(SquarerefEnableA, 103)

    @DebugIt()
    def get_FreqsquareA(self):
        # start protected zone ====
        #@warning: read direct??
        address = 104
        self.perseus.write(SETTINGS_READ_OFFSET, address)
        value = self.perseus.read(SETTINGS_READ_OFFSET)
        return value
        # end protected zone ====

    @DebugIt()
    def set_FreqsquareA(self, FreqsquareA):
        # start protected zone ====
        address = 104
        value = ((1 / FreqsquareA) * 1000000) / 12.5
        value = address << 17 | int(value)
        self.perseus.write(SETTINGS_WRITE_OFFSET, value)
        # end protected zone ====

    @DebugIt()
    def get_ResetkiA(self):
        return self.read_direct(105)

    @DebugIt()
    def set_ResetkiA(self, ResetkiA):
        self.write_direct(ResetkiA, 105)

    @DebugIt()
    def get_LookRefA(self):
        return self.read_direct(106)

    @DebugIt()
    def set_LookRefA(self, LookRefA):
        self.write_direct(LookRefA, 106)

    @DebugIt()
    def get_QuadrantSelectionA(self):
        return self.read_direct(107)

    @DebugIt()
    def set_QuadrantSelectionA(self, QuadrantSelectionA):
        self.write_direct(QuadrantSelectionA, 107)

    @DebugIt()
    def get_SlowIqLoopInputSelection(self):
        return self.read_direct(110)

    @DebugIt()
    def set_SlowIqLoopInputSelection(self, SlowIqLoopInputSelection):
        self.write_direct(SlowIqLoopInputSelection, 110)

    @DebugIt()
    def get_FastIqLoopInputSelection(self):
        return self.read_direct(111)

    @DebugIt()
    def set_FastIqLoopInputSelection(self, FastIqLoopInputSelection):
        self.write_direct(FastIqLoopInputSelection, 111)

    @DebugIt()
    def get_AmplitudeLoopInputSelection(self):
        return self.read_direct(112)

    @DebugIt()
    def set_AmplitudeLoopInputSelection(self, AmplitudeLoopInputSelection):
        self.write_direct(AmplitudeLoopInputSelection, 112)

    @DebugIt()
    def get_PhaseLoopInputSelection(self):
        return self.read_direct(113)

    @DebugIt()
    def set_PhaseLoopInputSelection(self, PhaseLoopInputSelection):
        self.write_direct(PhaseLoopInputSelection, 113)

    @DebugIt()
    def get_LoopsInputs(self):
        return self.read_direct(114)

    @DebugIt()
    def set_LoopsInputs(self, LoopsInputs):
        self.write_direct(LoopsInputs, 114)

    @DebugIt()
    def get_FastIqLoopEnable(self):
        return self.read_direct(115)

    @DebugIt()
    def set_FastIqLoopEnable(self, FastIqLoopEnable):
        self.write_direct(FastIqLoopEnable, 115)

    @DebugIt()
    def get_AmplitudeLoopEnable(self):
        return self.read_direct(116)

    @DebugIt()
    def set_AmplitudeLoopEnable(self, AmplitudeLoopEnable):
        self.write_direct(AmplitudeLoopEnable, 116)

    @DebugIt()
    def get_PhaseLoopEnable(self):
        return self.read_direct(117)

    @DebugIt()
    def set_PhaseLoopEnable(self, PhaseLoopEnable):
        self.write_direct(PhaseLoopEnable, 117)

    @DebugIt()
    def get_KpFastIqLoop(self):
        return self.read_direct(118)

    @DebugIt()
    def set_KpFastIqLoop(self, KpFastIqLoop):
        self.write_direct(KpFastIqLoop, 118)

    @DebugIt()
    def get_KiFastIqLoop(self):
        return self.read_direct(119)

    @DebugIt()
    def set_KiFastIqLoop(self, KiFastIqLoop):
        self.write_direct(KiFastIqLoop, 119)

    @DebugIt()
    def get_KpAmpLoop(self):
        return self.read_direct(120)

    @DebugIt()
    def set_KpAmpLoop(self, KpAmpLoop):
        self.write_direct(KpAmpLoop, 120)

    @DebugIt()
    def get_KiAmpLoop(self):
        return self.read_direct(121)

    @DebugIt()
    def set_KiAmpLoop(self, KiAmpLoop):
        self.write_direct(KiAmpLoop, 121)

    @DebugIt()
    def get_KpPhaseLoop(self):
        return self.read_direct(122)

    @DebugIt()
    def set_KpPhaseLoop(self, KpPhaseLoop):
        self.write_direct(KpPhaseLoop, 122)

    @DebugIt()
    def get_KiPhaseLoop(self):
        return self.read_direct(123)

    @DebugIt()
    def set_KiPhaseLoop(self, KiPhaseLoop):
        self.write_direct(KiPhaseLoop, 123)

    @DebugIt()
    def get_PiLimitFastPiIq(self):
        return self.read_milivolts(124)

    @DebugIt()
    def set_PiLimitFastPiIq(self, PiLimitFastPiIq):
        self.write_milivolts(PiLimitFastPiIq, 124)

    @DebugIt()
    def get_PulseModeEnableA(self):
        return self.read_direct(200)

    @DebugIt()
    def set_PulseModeEnableA(self, PulseModeEnableA):
        self.write_direct(PulseModeEnableA, 200)

    @DebugIt()
    def get_AutomaticConditioningEnableA(self):
        return self.read_direct(201)

    @DebugIt()
    def set_AutomaticConditioningEnableA(self, AutomaticConditioningEnableA):
        self.write_direct(AutomaticConditioningEnableA, 201)

    @DebugIt()
    def get_ConditioningdutyCicleA(self):
        # start protected zone ====
        value = self.read_direct(202)
        value = (value / 8000000) * 2562 * 100
        return value
        # end protected zone ====


    @DebugIt()
    def set_ConditioningdutyCicleA(self, ConditioningdutyCicleA):
        # start protected zone ====
        value = ((ConditioningdutyCicleA * 8000000) / 100.0) / 256
        self.write_direct(value, 202)
        pass
        # end protected zone ====


    @DebugIt()
    def get_TuningEnableA(self):
        return self.read_direct(300)

    @DebugIt()
    def set_TuningEnableA(self, TuningEnableA):
        self.write_direct(TuningEnableA, 300)

    @DebugIt()
    def get_TuningPosEnA(self):
        return self.read_direct(301)

    @DebugIt()
    def set_TuningPosEnA(self, TuningPosEnA):
        self.write_direct(TuningPosEnA, 301)

    @DebugIt()
    def get_NumStepsA(self):
        return self.read_direct(302)

    @DebugIt()
    def set_NumStepsA(self, NumStepsA):
        self.write_direct(NumStepsA, 302)

    @DebugIt()
    def get_PulsesFrequency(self):
        return self.read_direct(303)

    @DebugIt()
    def set_PulsesFrequency(self, PulsesFrequency):
        self.write_direct(PulsesFrequency, 303)

    @DebugIt()
    def get_PhaseOffsetA(self):
        return self.read_angle(304)

    @DebugIt()
    def set_PhaseOffsetA(self, PhaseOffsetA):
        self.write_angle(PhaseOffsetA, 304)

    @DebugIt()
    def get_MoveA(self):
        return self.read_direct(305)

    @DebugIt()
    def set_MoveA(self, MoveA):
        self.write_direct(MoveA, 305)

    @DebugIt()
    def get_MoveupA(self):
        return self.read_direct(306)

    @DebugIt()
    def set_MoveupA(self, MoveupA):
        self.write_direct(MoveupA, 306)

    @DebugIt()
    def get_TuningresetA(self):
        return self.read_direct(307)

    @DebugIt()
    def set_TuningresetA(self, TuningresetA):
        self.write_direct(TuningresetA, 307)

    @DebugIt()
    def get_Fwmina(self):
        return self.read_direct(308)

    @DebugIt()
    def set_Fwmina(self, Fwmina):
        self.write_direct(Fwmina, 308)

    @DebugIt()
    def get_MarginupA(self):
        # start protected zone ====
        #=IF(P98>2^15;
        #       (P98-2^16)/2^15*180;
        #    P98/2^15*180)
        address = 309
        value = self.read_direct(address)
        if value > (2 ** 15):
            value = (value - (2 ** 16)) * 180.0 / (2 ** 15)
        else:
            value = (value * 180.0) / (2 ** 15)
        return value
        # end protected zone ====

    @DebugIt()
    def set_MarginupA(self, MarginupA):
        # start protected zone ====
        #=IF(E98>180;
        #       (E98-360)/180*2^15+2^16;
        # IF(E98<0;
        #       E98/180*2^15+2^16;
        # E98/180*2^15))
        address = 309
        if MarginupA > 180:
            value = (((MarginupA - 360.0) * (2 ** 15)) / 180.0) + (2 ** 16)
        elif MarginupA < 0:
            value = ((MarginupA * (2 ** 15)) / 180.0) + (2 ** 16)
        else:
            value = (MarginupA * (2 ** 15)) / 180.0
        self.write_direct(value, address)
        # end protected zone ====


    @DebugIt()
    def get_MarginlowA(self):
        # start protected zone ====
        #=IF(P98>2^15;
        #       (P98-2^16)/2^15*180;
        #    P98/2^15*180)
        address = 310
        value = self.read_direct(address)
        if value > (2 ** 15):
            value = (value - (2 ** 16)) * 180.0 / (2 ** 15)
        else:
            value = (value * 180.0) / (2 ** 15)
        return value
        # end protected zone ====

    @DebugIt()
    def set_MarginlowA(self, MarginlowA):
        #=IF(E98>180;
        #       (E98-360)/180*2^15+2^16;
        # IF(E98<0;
        #       E98/180*2^15+2^16;
        # E98/180*2^15))
        address = 310
        if MarginupA > 180:
            value = (((MarginupA - 360.0) * (2 ** 15)) / 180.0) + (2 ** 16)
        elif MarginupA < 0:
            value = ((MarginupA * (2 ** 15)) / 180.0) + (2 ** 16)
        else:
            value = (MarginupA * (2 ** 15)) / 180.0
        self.write_direct(value, address)
        # end protected zone ====

    @DebugIt()
    def get_EpsItckDisable(self):
        return self.read_direct(400)

    @DebugIt()
    def set_EpsItckDisable(self, EpsItckDisable):
        self.write_direct(EpsItckDisable, 400)

    @DebugIt()
    def get_FimItckDisable(self):
        return self.read_direct(401)

    @DebugIt()
    def set_FimItckDisable(self, FimItckDisable):
        self.write_direct(FimItckDisable, 401)

    @DebugIt()
    def get_MDivider(self):
        # start protected zone ====
        address = 500
        value = self.read_direct(address) + 1
        #@warning: read_direct?? or +1
        return value
        # end protected zone ====

    @DebugIt()
    def set_MDivider(self, MDivider):
        # start protected zone ====
        address = 500
        value = MDivider - 1
        self.write_direct(value, address)
        # end protected zone ====

    @DebugIt()
    def get_NDivider(self):
        # start protected zone ====
        address = 501
        value = self.read_direct(address) + 1
        #@warning: read_direct?? or +1
        return value
        # end protected zone ====

    @DebugIt()
    def set_NDivider(self, NDivider):
        # start protected zone ====
        address = 501
        value = MDivider - 1
        self.write_direct(value, address)
        # end protected zone ====

    @DebugIt()
    def get_Muxsel(self):
        return self.read_direct(502)

    @DebugIt()
    def set_Muxsel(self, Muxsel):
        self.write_direct(Muxsel, 502)

    @DebugIt()
    def get_Mux0Divider(self):
        return self.read_direct(503)

    @DebugIt()
    def set_Mux0Divider(self, Mux0Divider):
        self.write_direct(Mux0Divider, 503)

    @DebugIt()
    def get_Mux1Divider(self):
        return self.read_direct(504)

    @DebugIt()
    def set_Mux1Divider(self, Mux1Divider):
        self.write_direct(Mux1Divider, 504)

    @DebugIt()
    def get_Mux2Divider(self):
        return self.read_direct(505)

    @DebugIt()
    def set_Mux2Divider(self, Mux2Divider):
        self.write_direct(Mux2Divider, 505)

    @DebugIt()
    def get_Mux3Divider(self):
        return self.read_direct(506)

    @DebugIt()
    def set_Mux3Divider(self, Mux3Divider):
        self.write_direct(Mux3Divider, 506)

    @DebugIt()
    def get_Mux4Divider(self):
        return self.read_direct(507)

    @DebugIt()
    def set_Mux4Divider(self, Mux4Divider):
        self.write_direct(Mux4Divider, 507)

    @DebugIt()
    def get_SendWord(self):
        return self.read_direct(508)

    @DebugIt()
    def set_SendWord(self, SendWord):
        self.write_direct(SendWord, 508)

    @DebugIt()
    def get_Cpdir(self):
        return self.read_direct(509)

    @DebugIt()
    def set_Cpdir(self, Cpdir):
        self.write_direct(Cpdir, 509)

    @DebugIt()
    def get_VcxoOutputInversion(self):
        return self.read_direct(510)

    @DebugIt()
    def set_VcxoOutputInversion(self, VcxoOutputInversion):
        self.write_direct(VcxoOutputInversion, 510)

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
    def read_Diag_TuningOn(self):
        return self._Diag_TuningOn

    @DebugIt()
    def read_Diag_TuningOnFwMinTuningEnableLatch(self):
        return self._Diag_TuningOnFwMinTuningEnableLatch

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
        self.start_reading_diagnostics()

        self._Diag_IcavLoops = self.read_diag_milivolts(0)
        self._Diag_QcavLoops = self.read_diag_milivolts(1)
        self._Diag_Icontrol = self.read_diag_milivolts(2)
        self._Diag_Qcontrol = self.read_diag_milivolts(3)
        self._Diag_Icontrol1 = self.read_diag_milivolts(4)
        self._Diag_Qcontrol1 = self.read_diag_milivolts(5)
        self._Diag_Icontrol2 = self.read_diag_milivolts(6)
        self._Diag_Qcontrol2 = self.read_diag_milivolts(7)
        self._Diag_Ierror = self.read_diag_milivolts(8)
        self._Diag_Qerror = self.read_diag_milivolts(9)
        self._Diag_Ierroraccum = self.read_diag_milivolts(10)
        self._Diag_Qerroraccum = self.read_diag_milivolts(11)
        self._Diag_Iref = self.read_diag_milivolts(12)
        self._Diag_Qref = self.read_diag_milivolts(13)
        self._Diag_IFwCavLoops = self.read_diag_milivolts(14)
        self._Diag_QFwCavLoops = self.read_diag_milivolts(15)
        self._Diag_IFwTet1Loops = self.read_diag_milivolts(16)
        self._Diag_QFwTet1Loops = self.read_diag_milivolts(17)
        self._Diag_IFwTet2Loops = self.read_diag_milivolts(18)
        self._Diag_QFwTet2Loops = self.read_diag_milivolts(19)
        self._Diag_IFwCircInLoops = self.read_diag_milivolts(20)
        self._Diag_QFwCircInLoops = self.read_diag_milivolts(21)
        self._Diag_Imo = self.read_diag_milivolts(22)
        self._Diag_Qmo = self.read_diag_milivolts(23)
        self._Diag_Ispare1 = self.read_diag_milivolts(24)
        self._Diag_Qspare1 = self.read_diag_milivolts(25)
        self._Diag_Ispare2 = self.read_diag_milivolts(26)
        self._Diag_Qspare2 = self.read_diag_milivolts(27)
        self._Diag_IMuxCav = self.read_diag_milivolts(28)
        self._Diag_QMuxCav = self.read_diag_milivolts(29)
        self._Diag_IMuxFwCav = self.read_diag_milivolts(30)
        self._Diag_QMuxFwCav = self.read_diag_milivolts(31)
        self._Diag_IMuxFwTet1 = self.read_diag_milivolts(32)
        self._Diag_QMuxFwTet1 = self.read_diag_milivolts(33)
        self._Diag_IMuxFwTet2 = self.read_diag_milivolts(34)
        self._Diag_QMuxFwTet2 = self.read_diag_milivolts(35)
        self._Diag_IMuxFwCircIn = self.read_diag_milivolts(36)
        self._Diag_QMuxFwCircIn = self.read_diag_milivolts(37)
        self._Diag_AmpCav = self.read_diag_milivolts(38)
        self._Diag_AmpFw = self.read_diag_milivolts(39)
        self._Diag_AngCavFw = self.read_diag_angle(40)
        self._Diag_AngCavL = self.read_diag_angle(41)
        self._Diag_AngFwL = self.read_diag_angle(42)
        self._Diag_Vaccum1 = self.read_direct(43)
        self._Diag_Vaccum2 = self.read_direct(44)
        self._Diag_VcxoPowered = self.read_direct(50)
        self._Diag_VcxoRef = self.read_direct(51)
        self._Diag_VcxoLocked = self.read_direct(52)
        self._Diag_VcxoCableDisconnected = self.read_direct(53)
        self._Diag_TuningOn = self.read_direct(299)
        self._Diag_TuningOnFwMinTuningEnableLatch = self.read_direct(300)
        self._Diag_FreqUp = self.read_direct(301)
        self._Diag_ManualTuningOn = self.read_direct(302)
        self._Diag_ManualTuningFreqUp = self.read_direct(303)
        self._Diag_EpsItckDelay = self.read_direct(400)
        self._Diag_FimItckDelay = self.read_direct(401)
        self._Diag_FdlTrigHwInput = self.read_direct(402)
        self._Diag_FdlTrigSwInput = self.read_direct(403)

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
