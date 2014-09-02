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

    Kpa = attribute(label='Kpa',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=10,
                                   fget="get_Kpa",
                                   fset="set_Kpa",
                                   doc=""
                                   )

    Kia = attribute(label='Kia',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=32767,
                                   fget="get_Kia",
                                   fset="set_Kia",
                                   doc=""
                                   )

    Phaseshiftcav = attribute(label='Phaseshiftcav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_Phaseshiftcav",
                                   fset="set_Phaseshiftcav",
                                   doc=""
                                   )

    Phaseshiftfwcav = attribute(label='Phaseshiftfwcav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_Phaseshiftfwcav",
                                   fset="set_Phaseshiftfwcav",
                                   doc=""
                                   )

    Phaseshiftfwtet1 = attribute(label='Phaseshiftfwtet1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_Phaseshiftfwtet1",
                                   fset="set_Phaseshiftfwtet1",
                                   doc=""
                                   )

    Phaseshiftfwtet2 = attribute(label='Phaseshiftfwtet2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_Phaseshiftfwtet2",
                                   fset="set_Phaseshiftfwtet2",
                                   doc=""
                                   )

    Pilimita = attribute(label='Pilimita',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Pilimita",
                                   fset="set_Pilimita",
                                   doc=""
                                   )

    Samplestoaverage = attribute(label='Samplestoaverage',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_Samplestoaverage",
                                   fset="set_Samplestoaverage",
                                   doc=""
                                   )

    Filterstages = attribute(label='Filterstages',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=3,
                                   fget="get_Filterstages",
                                   fset="set_Filterstages",
                                   doc=""
                                   )

    Phaseshiftfwcircin = attribute(label='Phaseshiftfwcircin',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_Phaseshiftfwcircin",
                                   fset="set_Phaseshiftfwcircin",
                                   doc=""
                                   )

    Phaseshiftcontrolsignaltet1 = attribute(label='Phaseshiftcontrolsignaltet1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_Phaseshiftcontrolsignaltet1",
                                   fset="set_Phaseshiftcontrolsignaltet1",
                                   doc=""
                                   )

    Phaseshiftcontrolsignaltet2 = attribute(label='Phaseshiftcontrolsignaltet2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=360,
                                   fget="get_Phaseshiftcontrolsignaltet2",
                                   fset="set_Phaseshiftcontrolsignaltet2",
                                   doc=""
                                   )

    Gaintetrode1 = attribute(label='Gaintetrode1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0.1, max_value=1,
                                   fget="get_Gaintetrode1",
                                   fset="set_Gaintetrode1",
                                   doc=""
                                   )

    Gaintetrode2 = attribute(label='Gaintetrode2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0.1, max_value=1,
                                   fget="get_Gaintetrode2",
                                   fset="set_Gaintetrode2",
                                   doc=""
                                   )

    Automaticstartupenable = attribute(label='Automaticstartupenable',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Automaticstartupenable",
                                   fset="set_Automaticstartupenable",
                                   doc=""
                                   )

    Commandstart = attribute(label='Commandstart',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_Commandstart",
                                   fset="set_Commandstart",
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

    Phaseincreaserate = attribute(label='Phaseincreaserate',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_Phaseincreaserate",
                                   fset="set_Phaseincreaserate",
                                   doc=""
                                   )

    Gainol = attribute(label='Gainol',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0.5, max_value=2,
                                   fget="get_Gainol",
                                   fset="set_Gainol",
                                   doc=""
                                   )

    Sparegpiooutput01 = attribute(label='Sparegpiooutput01',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Sparegpiooutput01",
                                   fset="set_Sparegpiooutput01",
                                   doc=""
                                   )

    Sparegpiooutput02 = attribute(label='Sparegpiooutput02',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Sparegpiooutput02",
                                   fset="set_Sparegpiooutput02",
                                   doc=""
                                   )

    Sparegpiooutput03 = attribute(label='Sparegpiooutput03',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Sparegpiooutput03",
                                   fset="set_Sparegpiooutput03",
                                   doc=""
                                   )

    Sparegpiooutput04 = attribute(label='Sparegpiooutput04',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Sparegpiooutput04",
                                   fset="set_Sparegpiooutput04",
                                   doc=""
                                   )

    Fdlswtrigger = attribute(label='Fdlswtrigger',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Fdlswtrigger",
                                   fset="set_Fdlswtrigger",
                                   doc=""
                                   )

    Loopenablea = attribute(label='Loopenablea',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Loopenablea",
                                   fset="set_Loopenablea",
                                   doc=""
                                   )

    Adcsphaseshiftenablea = attribute(label='Adcsphaseshiftenablea',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Adcsphaseshiftenablea",
                                   fset="set_Adcsphaseshiftenablea",
                                   doc=""
                                   )

    Dacsphaseshiftenablea = attribute(label='Dacsphaseshiftenablea',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Dacsphaseshiftenablea",
                                   fset="set_Dacsphaseshiftenablea",
                                   doc=""
                                   )

    Squarerefenablea = attribute(label='Squarerefenablea',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Squarerefenablea",
                                   fset="set_Squarerefenablea",
                                   doc=""
                                   )

    Freqsquarea = attribute(label='Freqsquarea',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=3, max_value=1000,
                                   fget="get_Freqsquarea",
                                   fset="set_Freqsquarea",
                                   doc=""
                                   )

    Resetkia = attribute(label='Resetkia',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Resetkia",
                                   fset="set_Resetkia",
                                   doc=""
                                   )

    Lookrefa = attribute(label='Lookrefa',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Lookrefa",
                                   fset="set_Lookrefa",
                                   doc=""
                                   )

    Quadrantselectiona = attribute(label='Quadrantselectiona',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=3,
                                   fget="get_Quadrantselectiona",
                                   fset="set_Quadrantselectiona",
                                   doc=""
                                   )

    Voltagerateincreasea = attribute(label='Voltagerateincreasea',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_Voltagerateincreasea",
                                   fset="set_Voltagerateincreasea",
                                   doc=""
                                   )

    Loopinputselection = attribute(label='Loopinputselection',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Loopinputselection",
                                   fset="set_Loopinputselection",
                                   doc=""
                                   )

    Pulsemodeenablea = attribute(label='Pulsemodeenablea',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Pulsemodeenablea",
                                   fset="set_Pulsemodeenablea",
                                   doc=""
                                   )

    Automaticconditioningenablea = attribute(label='Automaticconditioningenablea',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Automaticconditioningenablea",
                                   fset="set_Automaticconditioningenablea",
                                   doc=""
                                   )

    Conditioningdutyciclea = attribute(label='Conditioningdutyciclea',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=100,
                                   fget="get_Conditioningdutyciclea",
                                   fset="set_Conditioningdutyciclea",
                                   doc=""
                                   )

    Tuningenablea = attribute(label='Tuningenablea',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Tuningenablea",
                                   fset="set_Tuningenablea",
                                   doc=""
                                   )

    Tuningposena = attribute(label='Tuningposena',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Tuningposena",
                                   fset="set_Tuningposena",
                                   doc=""
                                   )

    Numstepsa = attribute(label='Numstepsa',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=65535,
                                   fget="get_Numstepsa",
                                   fset="set_Numstepsa",
                                   doc=""
                                   )

    Pulsesfrequency = attribute(label='Pulsesfrequency',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=7,
                                   fget="get_Pulsesfrequency",
                                   fset="set_Pulsesfrequency",
                                   doc=""
                                   )

    Phaseoffseta = attribute(label='Phaseoffseta',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=180,
                                   fget="get_Phaseoffseta",
                                   fset="set_Phaseoffseta",
                                   doc=""
                                   )

    Movea = attribute(label='Movea',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Movea",
                                   fset="set_Movea",
                                   doc=""
                                   )

    Moveupa = attribute(label='Moveupa',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Moveupa",
                                   fset="set_Moveupa",
                                   doc=""
                                   )

    Tuningreseta = attribute(label='Tuningreseta',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Tuningreseta",
                                   fset="set_Tuningreseta",
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

    Marginupa = attribute(label='Marginupa',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=10,
                                   fget="get_Marginupa",
                                   fset="set_Marginupa",
                                   doc=""
                                   )

    Marginlowa = attribute(label='Marginlowa',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=5,
                                   fget="get_Marginlowa",
                                   fset="set_Marginlowa",
                                   doc=""
                                   )

    Epsitckdisable = attribute(label='Epsitckdisable',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Epsitckdisable",
                                   fset="set_Epsitckdisable",
                                   doc=""
                                   )

    Fimitckdisable = attribute(label='Fimitckdisable',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Fimitckdisable",
                                   fset="set_Fimitckdisable",
                                   doc=""
                                   )

    Mdivider = attribute(label='Mdivider',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=128,
                                   fget="get_Mdivider",
                                   fset="set_Mdivider",
                                   doc=""
                                   )

    Ndivider = attribute(label='Ndivider',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=128,
                                   fget="get_Ndivider",
                                   fset="set_Ndivider",
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

    Mux0divider = attribute(label='Mux0divider',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux0divider",
                                   fset="set_Mux0divider",
                                   doc=""
                                   )

    Mux1divider = attribute(label='Mux1divider',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux1divider",
                                   fset="set_Mux1divider",
                                   doc=""
                                   )

    Mux2divider = attribute(label='Mux2divider',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux2divider",
                                   fset="set_Mux2divider",
                                   doc=""
                                   )

    Mux3divider = attribute(label='Mux3divider',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux3divider",
                                   fset="set_Mux3divider",
                                   doc=""
                                   )

    Mux4divider = attribute(label='Mux4divider',
                                   dtype=int,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=4,
                                   fget="get_Mux4divider",
                                   fset="set_Mux4divider",
                                   doc=""
                                   )

    Sendword = attribute(label='Sendword',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Sendword",
                                   fset="set_Sendword",
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

    Vcxooutputinversion = attribute(label='Vcxooutputinversion',
                                   dtype=bool,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ_WRITE",
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_Vcxooutputinversion",
                                   fset="set_Vcxooutputinversion",
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

    IfwcavLoops = attribute(label='IfwcavLoops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QfwcavLoops = attribute(label='QfwcavLoops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Ifwtet1Loops = attribute(label='Ifwtet1Loops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qfwtet1Loops = attribute(label='Qfwtet1Loops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Ifwtet2Loops = attribute(label='Ifwtet2Loops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qfwtet2Loops = attribute(label='Qfwtet2Loops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    IfwcircinLoops = attribute(label='IfwcircinLoops',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    QfwcircinLoops = attribute(label='QfwcircinLoops',
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

    Imuxcav = attribute(label='Imuxcav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qmuxcav = attribute(label='Qmuxcav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Imuxfwcav = attribute(label='Imuxfwcav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qmuxfwcav = attribute(label='Qmuxfwcav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Imuxfwtet1 = attribute(label='Imuxfwtet1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qmuxfwtet1 = attribute(label='Qmuxfwtet1',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Imuxfwtet2 = attribute(label='Imuxfwtet2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qmuxfwtet2 = attribute(label='Qmuxfwtet2',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Imuxfwcircin = attribute(label='Imuxfwcircin',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Qmuxfwcircin = attribute(label='Qmuxfwcircin',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Ampcav = attribute(label='Ampcav',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Ampfw = attribute(label='Ampfw',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Angcavfw = attribute(label='Angcavfw',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Angcavl = attribute(label='Angcavl',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Angfwl = attribute(label='Angfwl',
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

    Vcxocabledisconnected = attribute(label='Vcxocabledisconnected',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Tuningon = attribute(label='Tuningon',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Tuningonfwmintuningenablelatch = attribute(label='Tuningonfwmintuningenablelatch',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Frequp = attribute(label='Frequp',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Manualtuningon = attribute(label='Manualtuningon',
                                   dtype=float,
                                   display_level='DispLevel.OPERATOR',
                                   access="AttrWriteType.READ",
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Manualtuningfrequp = attribute(label='Manualtuningfrequp',
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
    def get_Kpa(self):
        return self.read_direct(0)


    @DebugIt()
    def get_Kia(self):
        return self.read_direct(1)


    @DebugIt()
    def get_Phaseshiftcav(self):
        return self.read_angle(2)


    @DebugIt()
    def get_Phaseshiftfwcav(self):
        return self.read_angle(3)


    @DebugIt()
    def get_Phaseshiftfwtet1(self):
        return self.read_angle(4)


    @DebugIt()
    def get_Phaseshiftfwtet2(self):
        return self.read_angle(5)


    @DebugIt()
    def get_Pilimita(self):
        return self.read_milivolts(6)


    @DebugIt()
    def get_Samplestoaverage(self):
        return self.read_direct(7)


    @DebugIt()
    def get_Filterstages(self):
        return self.read_direct(8)


    @DebugIt()
    def get_Phaseshiftfwcircin(self):
        return self.read_angle(9)


    @DebugIt()
    def get_Phaseshiftcontrolsignaltet1(self):
        return self.read_angle(10)


    @DebugIt()
    def get_Phaseshiftcontrolsignaltet2(self):
        return self.read_angle(11)


    @DebugIt()
    def get_Gaintetrode1(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_Gaintetrode2(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_Automaticstartupenable(self):
        return self.read_direct(15)


    @DebugIt()
    def get_Commandstart(self):
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
    def get_Phaseincreaserate(self):
        return self.read_direct(23)


    @DebugIt()
    def get_Gainol(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_Sparegpiooutput01(self):
        return self.read_direct(28)


    @DebugIt()
    def get_Sparegpiooutput02(self):
        return self.read_direct(29)


    @DebugIt()
    def get_Sparegpiooutput03(self):
        return self.read_direct(30)


    @DebugIt()
    def get_Sparegpiooutput04(self):
        return self.read_direct(31)


    @DebugIt()
    def get_Fdlswtrigger(self):
        return self.read_direct(32)


    @DebugIt()
    def get_Loopenablea(self):
        return self.read_direct(100)


    @DebugIt()
    def get_Adcsphaseshiftenablea(self):
        return self.read_direct(101)


    @DebugIt()
    def get_Dacsphaseshiftenablea(self):
        return self.read_direct(102)


    @DebugIt()
    def get_Squarerefenablea(self):
        return self.read_direct(103)


    @DebugIt()
    def get_Freqsquarea(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_Resetkia(self):
        return self.read_direct(105)


    @DebugIt()
    def get_Lookrefa(self):
        return self.read_direct(106)


    @DebugIt()
    def get_Quadrantselectiona(self):
        return self.read_direct(107)


    @DebugIt()
    def get_Voltagerateincreasea(self):
        return self.read_direct(110)


    @DebugIt()
    def get_Loopinputselection(self):
        return self.read_direct(112)


    @DebugIt()
    def get_Pulsemodeenablea(self):
        return self.read_direct(200)


    @DebugIt()
    def get_Automaticconditioningenablea(self):
        return self.read_direct(201)


    @DebugIt()
    def get_Conditioningdutyciclea(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_Tuningenablea(self):
        return self.read_direct(300)


    @DebugIt()
    def get_Tuningposena(self):
        return self.read_direct(301)


    @DebugIt()
    def get_Numstepsa(self):
        return self.read_direct(302)


    @DebugIt()
    def get_Pulsesfrequency(self):
        return self.read_direct(303)


    @DebugIt()
    def get_Phaseoffseta(self):
        return self.read_angle(304)


    @DebugIt()
    def get_Movea(self):
        return self.read_direct(305)


    @DebugIt()
    def get_Moveupa(self):
        return self.read_direct(306)


    @DebugIt()
    def get_Tuningreseta(self):
        return self.read_direct(307)


    @DebugIt()
    def get_Fwmina(self):
        return self.read_direct(308)


    @DebugIt()
    def get_Marginupa(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_Marginlowa(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_Epsitckdisable(self):
        return self.read_direct(400)


    @DebugIt()
    def get_Fimitckdisable(self):
        return self.read_direct(401)


    @DebugIt()
    def get_Mdivider(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_Ndivider(self):
        #@todo: insert here your code ...
        pass


    @DebugIt()
    def get_Muxsel(self):
        return self.read_direct(502)


    @DebugIt()
    def get_Mux0divider(self):
        return self.read_direct(503)


    @DebugIt()
    def get_Mux1divider(self):
        return self.read_direct(504)


    @DebugIt()
    def get_Mux2divider(self):
        return self.read_direct(505)


    @DebugIt()
    def get_Mux3divider(self):
        return self.read_direct(506)


    @DebugIt()
    def get_Mux4divider(self):
        return self.read_direct(507)


    @DebugIt()
    def get_Sendword(self):
        return self.read_direct(508)


    @DebugIt()
    def get_Cpdir(self):
        return self.read_direct(509)


    @DebugIt()
    def get_Vcxooutputinversion(self):
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
    def read_IfwcavLoops(self):
        return self._IfwcavLoops

    @DebugIt()
    def read_QfwcavLoops(self):
        return self._QfwcavLoops

    @DebugIt()
    def read_Ifwtet1Loops(self):
        return self._Ifwtet1Loops

    @DebugIt()
    def read_Qfwtet1Loops(self):
        return self._Qfwtet1Loops

    @DebugIt()
    def read_Ifwtet2Loops(self):
        return self._Ifwtet2Loops

    @DebugIt()
    def read_Qfwtet2Loops(self):
        return self._Qfwtet2Loops

    @DebugIt()
    def read_IfwcircinLoops(self):
        return self._IfwcircinLoops

    @DebugIt()
    def read_QfwcircinLoops(self):
        return self._QfwcircinLoops

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
    def read_Imuxcav(self):
        return self._Imuxcav

    @DebugIt()
    def read_Qmuxcav(self):
        return self._Qmuxcav

    @DebugIt()
    def read_Imuxfwcav(self):
        return self._Imuxfwcav

    @DebugIt()
    def read_Qmuxfwcav(self):
        return self._Qmuxfwcav

    @DebugIt()
    def read_Imuxfwtet1(self):
        return self._Imuxfwtet1

    @DebugIt()
    def read_Qmuxfwtet1(self):
        return self._Qmuxfwtet1

    @DebugIt()
    def read_Imuxfwtet2(self):
        return self._Imuxfwtet2

    @DebugIt()
    def read_Qmuxfwtet2(self):
        return self._Qmuxfwtet2

    @DebugIt()
    def read_Imuxfwcircin(self):
        return self._Imuxfwcircin

    @DebugIt()
    def read_Qmuxfwcircin(self):
        return self._Qmuxfwcircin

    @DebugIt()
    def read_Ampcav(self):
        return self._Ampcav

    @DebugIt()
    def read_Ampfw(self):
        return self._Ampfw

    @DebugIt()
    def read_Angcavfw(self):
        return self._Angcavfw

    @DebugIt()
    def read_Angcavl(self):
        return self._Angcavl

    @DebugIt()
    def read_Angfwl(self):
        return self._Angfwl

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
    def read_Vcxocabledisconnected(self):
        return self._Vcxocabledisconnected

    @DebugIt()
    def read_Tuningon(self):
        return self._Tuningon

    @DebugIt()
    def read_Tuningonfwmintuningenablelatch(self):
        return self._Tuningonfwmintuningenablelatch

    @DebugIt()
    def read_Frequp(self):
        return self._Frequp

    @DebugIt()
    def read_Manualtuningon(self):
        return self._Manualtuningon

    @DebugIt()
    def read_Manualtuningfrequp(self):
        return self._Manualtuningfrequp

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
        self._IfwcavLoops = self.read_diag_milivolts(14)
        self._QfwcavLoops = self.read_diag_milivolts(15)
        self._Ifwtet1Loops = self.read_diag_milivolts(16)
        self._Qfwtet1Loops = self.read_diag_milivolts(17)
        self._Ifwtet2Loops = self.read_diag_milivolts(18)
        self._Qfwtet2Loops = self.read_diag_milivolts(19)
        self._IfwcircinLoops = self.read_diag_milivolts(20)
        self._QfwcircinLoops = self.read_diag_milivolts(21)
        self._Imo = self.read_diag_milivolts(22)
        self._Qmo = self.read_diag_milivolts(23)
        self._Ispare1 = self.read_diag_milivolts(24)
        self._Qspare1 = self.read_diag_milivolts(25)
        self._Ispare2 = self.read_diag_milivolts(26)
        self._Qspare2 = self.read_diag_milivolts(27)
        self._Imuxcav = self.read_diag_milivolts(28)
        self._Qmuxcav = self.read_diag_milivolts(29)
        self._Imuxfwcav = self.read_diag_milivolts(30)
        self._Qmuxfwcav = self.read_diag_milivolts(31)
        self._Imuxfwtet1 = self.read_diag_milivolts(32)
        self._Qmuxfwtet1 = self.read_diag_milivolts(33)
        self._Imuxfwtet2 = self.read_diag_milivolts(34)
        self._Qmuxfwtet2 = self.read_diag_milivolts(35)
        self._Imuxfwcircin = self.read_diag_milivolts(36)
        self._Qmuxfwcircin = self.read_diag_milivolts(37)
        self._Ampcav = self.read_diag_milivolts(38)
        self._Ampfw = self.read_diag_milivolts(39)
        self._Angcavfw = self.read_diag_angle(40)
        self._Angcavl = self.read_diag_angle(41)
        self._Angfwl = self.read_diag_angle(42)
        self._Vaccum1 = self.read_direct(43)
        self._Vaccum2 = self.read_direct(44)
        self._VcxoPowered = self.read_direct(50)
        self._VcxoRef = self.read_direct(51)
        self._VcxoLocked = self.read_direct(52)
        self._Vcxocabledisconnected = self.read_direct(53)
        self._Tuningon = self.read_direct(299)
        self._Tuningonfwmintuningenablelatch = self.read_direct(300)
        self._Frequp = self.read_direct(301)
        self._Manualtuningon = self.read_direct(302)
        self._Manualtuningfrequp = self.read_direct(303)
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
