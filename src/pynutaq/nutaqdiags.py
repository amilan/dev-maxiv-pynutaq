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


class NutaqDiag(Device):
    __metaclass__ = DeviceMeta

    Rvtet1 = attribute(label='Rvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Rvtet1",
                                   fset="set_Rvtet1",
                                   doc=""
                                   )

    Rvtet2 = attribute(label='Rvtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Rvtet2",
                                   fset="set_Rvtet2",
                                   doc=""
                                   )

    Rvcirc = attribute(label='Rvcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Rvcirc",
                                   fset="set_Rvcirc",
                                   doc=""
                                   )

    Fwload = attribute(label='Fwload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Fwload",
                                   fset="set_Fwload",
                                   doc=""
                                   )

    Fwhybload = attribute(label='Fwhybload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Fwhybload",
                                   fset="set_Fwhybload",
                                   doc=""
                                   )

    Rvcav = attribute(label='Rvcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Rvcav",
                                   fset="set_Rvcav",
                                   doc=""
                                   )

    ManualInterlock = attribute(label='ManualInterlock',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_ManualInterlock",
                                   fset="set_ManualInterlock",
                                   doc=""
                                   )

    DisableItckRvtet1 = attribute(label='DisableItckRvtet1',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvtet1",
                                   fset="set_DisableItckRvtet1",
                                   doc=""
                                   )

    DisableItckRvtet2 = attribute(label='DisableItckRvtet2',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvtet2",
                                   fset="set_DisableItckRvtet2",
                                   doc=""
                                   )

    DisableItckRvcirc = attribute(label='DisableItckRvcirc',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvcirc",
                                   fset="set_DisableItckRvcirc",
                                   doc=""
                                   )

    DisableItckFwload = attribute(label='DisableItckFwload',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckFwload",
                                   fset="set_DisableItckFwload",
                                   doc=""
                                   )

    DisableItckFwhybload = attribute(label='DisableItckFwhybload',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckFwhybload",
                                   fset="set_DisableItckFwhybload",
                                   doc=""
                                   )

    DisableItckRvcav = attribute(label='DisableItckRvcav',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckRvcav",
                                   fset="set_DisableItckRvcav",
                                   doc=""
                                   )

    DisableItckArcs = attribute(label='DisableItckArcs',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckArcs",
                                   fset="set_DisableItckArcs",
                                   doc=""
                                   )

    DisableItckVaccum = attribute(label='DisableItckVaccum',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckVaccum",
                                   fset="set_DisableItckVaccum",
                                   doc=""
                                   )

    DisableItckManualInterlock = attribute(label='DisableItckManualInterlock',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckManualInterlock",
                                   fset="set_DisableItckManualInterlock",
                                   doc=""
                                   )

    DisableItckPlungerEndSwitchesUp = attribute(label='DisableItckPlungerEndSwitchesUp',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckPlungerEndSwitchesUp",
                                   fset="set_DisableItckPlungerEndSwitchesUp",
                                   doc=""
                                   )

    DisableItckPlungerEndSwitchesDown = attribute(label='DisableItckPlungerEndSwitchesDown',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckPlungerEndSwitchesDown",
                                   fset="set_DisableItckPlungerEndSwitchesDown",
                                   doc=""
                                   )

    DisableItckMps = attribute(label='DisableItckMps',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=63,
                                   fget="get_DisableItckMps",
                                   fset="set_DisableItckMps",
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

    PulseupLogicInversion = attribute(label='PulseupLogicInversion',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_PulseupLogicInversion",
                                   fset="set_PulseupLogicInversion",
                                   doc=""
                                   )

    EndSwitchesConnectedToNoNcContact = attribute(label='EndSwitchesConnectedToNoNcContact',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=1,
                                   fget="get_EndSwitchesConnectedToNoNcContact",
                                   fset="set_EndSwitchesConnectedToNoNcContact",
                                   doc=""
                                   )

    Lookref = attribute(label='Lookref',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_Lookref",
                                   fset="set_Lookref",
                                   doc=""
                                   )

    Quadref = attribute(label='Quadref',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   min_value=0, max_value=3,
                                   fget="get_Quadref",
                                   fset="set_Quadref",
                                   doc=""
                                   )

    SpareDo1 = attribute(label='SpareDo1',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_SpareDo1",
                                   fset="set_SpareDo1",
                                   doc=""
                                   )

    SpareDo2 = attribute(label='SpareDo2',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_SpareDo2",
                                   fset="set_SpareDo2",
                                   doc=""
                                   )

    SpareDo3 = attribute(label='SpareDo3',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_SpareDo3",
                                   fset="set_SpareDo3",
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

    ResetInterlocksCavA = attribute(label='ResetInterlocksCavA',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_ResetInterlocksCavA",
                                   fset="set_ResetInterlocksCavA",
                                   doc=""
                                   )

    Landautuningenable = attribute(label='Landautuningenable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_Landautuningenable",
                                   fset="set_Landautuningenable",
                                   doc=""
                                   )

    Landautuningreset = attribute(label='Landautuningreset',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_Landautuningreset",
                                   fset="set_Landautuningreset",
                                   doc=""
                                   )

    Movelandauup = attribute(label='Movelandauup',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_Movelandauup",
                                   fset="set_Movelandauup",
                                   doc=""
                                   )

    Movelandauplg = attribute(label='Movelandauplg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_Movelandauplg",
                                   fset="set_Movelandauplg",
                                   doc=""
                                   )

    Numsteps = attribute(label='Numsteps',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1500,
                                   fget="get_Numsteps",
                                   fset="set_Numsteps",
                                   doc=""
                                   )

    Landauphaseoffset = attribute(label='Landauphaseoffset',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='6.4f',
                                   min_value=-180, max_value=180,
                                   fget="get_Landauphaseoffset",
                                   fset="set_Landauphaseoffset",
                                   doc=""
                                   )

    Landaumarginup = attribute(label='Landaumarginup',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=50,
                                   fget="get_Landaumarginup",
                                   fset="set_Landaumarginup",
                                   doc=""
                                   )

    LandauMarginLow = attribute(label='LandauMarginLow',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=10,
                                   fget="get_LandauMarginLow",
                                   fset="set_LandauMarginLow",
                                   doc=""
                                   )

    MinimumLandauAmplitude = attribute(label='MinimumLandauAmplitude',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_MinimumLandauAmplitude",
                                   fset="set_MinimumLandauAmplitude",
                                   doc=""
                                   )

    LandauPositiveEnable = attribute(label='LandauPositiveEnable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='6.4f',
                                   fget="get_LandauPositiveEnable",
                                   fset="set_LandauPositiveEnable",
                                   doc=""
                                   )

    Landauampsetting = attribute(label='Landauampsetting',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='6.4f',
                                   min_value=0, max_value=1000,
                                   fget="get_Landauampsetting",
                                   fset="set_Landauampsetting",
                                   doc=""
                                   )

    Diag_Irvtet1 = attribute(label='Diag_Irvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qrvtet1 = attribute(label='Diag_Qrvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Amprvtet1 = attribute(label='Diag_Amprvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Phrvtet1 = attribute(label='Diag_Phrvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Irvtet2 = attribute(label='Diag_Irvtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qrvtet2 = attribute(label='Diag_Qrvtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Amprvtet2 = attribute(label='Diag_Amprvtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Phrvtet2 = attribute(label='Diag_Phrvtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Ifwcirc = attribute(label='Diag_Ifwcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qfwcirc = attribute(label='Diag_Qfwcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Ampfwcirc = attribute(label='Diag_Ampfwcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Phfwcirc = attribute(label='Diag_Phfwcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Irvcirc = attribute(label='Diag_Irvcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qrvcirc = attribute(label='Diag_Qrvcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Amprvcirc = attribute(label='Diag_Amprvcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Phrvcirc = attribute(label='Diag_Phrvcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Ifwload = attribute(label='Diag_Ifwload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qfwload = attribute(label='Diag_Qfwload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Ampfwload = attribute(label='Diag_Ampfwload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Phfwload = attribute(label='Diag_Phfwload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Ifwhybload = attribute(label='Diag_Ifwhybload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qfwhybload = attribute(label='Diag_Qfwhybload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Ampfwhybload = attribute(label='Diag_Ampfwhybload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Phfwhybload = attribute(label='Diag_Phfwhybload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Irvcav = attribute(label='Diag_Irvcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qrvcav = attribute(label='Diag_Qrvcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Amprvcav = attribute(label='Diag_Amprvcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Phrvcav = attribute(label='Diag_Phrvcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
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

    Diag_Ampmo = attribute(label='Diag_Ampmo',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Phmo = attribute(label='Diag_Phmo',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Ilandau = attribute(label='Diag_Ilandau',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Qlandadu = attribute(label='Diag_Qlandadu',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Amplandadu = attribute(label='Diag_Amplandadu',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Phlandadu = attribute(label='Diag_Phlandadu',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PlungerMovingManualTuning = attribute(label='Diag_PlungerMovingManualTuning',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpManualTuning = attribute(label='Diag_PlungerMovingUpManualTuning',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PlungerMovingAutomaticTuning = attribute(label='Diag_PlungerMovingAutomaticTuning',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpAutomaticTuning = attribute(label='Diag_PlungerMovingUpAutomaticTuning',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_DephaseMoLandau = attribute(label='Diag_DephaseMoLandau',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Rvtet1 = attribute(label='Diag_Rvtet1',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Rvtet2 = attribute(label='Diag_Rvtet2',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Rvcirc = attribute(label='Diag_Rvcirc',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Fwload = attribute(label='Diag_Fwload',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Fwhybload = attribute(label='Diag_Fwhybload',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Rvcav = attribute(label='Diag_Rvcav',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Arcs = attribute(label='Diag_Arcs',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Vacuum = attribute(label='Diag_Vacuum',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_ManualInterlock = attribute(label='Diag_ManualInterlock',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_ExternalItck = attribute(label='Diag_ExternalItck',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchUp = attribute(label='Diag_PlungerEndSwitchUp',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchDown = attribute(label='Diag_PlungerEndSwitchDown',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Timestamp1 = attribute(label='Diag_Timestamp1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Timestamp2 = attribute(label='Diag_Timestamp2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Timestamp3 = attribute(label='Diag_Timestamp3',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Timestamp4 = attribute(label='Diag_Timestamp4',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Timestamp5 = attribute(label='Diag_Timestamp5',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Timestamp6 = attribute(label='Diag_Timestamp6',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_Timestamp7 = attribute(label='Diag_Timestamp7',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_DacsDisableCommand = attribute(label='Diag_DacsDisableCommand',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_PinSwitch = attribute(label='Diag_PinSwitch',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_FdlTriggerToLoopsdiagboard = attribute(label='Diag_FdlTriggerToLoopsdiagboard',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_OutputToPlc = attribute(label='Diag_OutputToPlc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_OutputToMps = attribute(label='Diag_OutputToMps',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_LandauMovingLed = attribute(label='Diag_LandauMovingLed',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_LandauPulseMotor = attribute(label='Diag_LandauPulseMotor',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_LandauDirMotor = attribute(label='Diag_LandauDirMotor',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_LandauMovingUpLed = attribute(label='Diag_LandauMovingUpLed',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_FdlTriggerForDiagnosticsPurposes = attribute(label='Diag_FdlTriggerForDiagnosticsPurposes',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_SpareDo01 = attribute(label='Diag_SpareDo01',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_SpareDo02 = attribute(label='Diag_SpareDo02',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )

    Diag_SpareDo03 = attribute(label='Diag_SpareDo03',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='6.4f',
                                   doc=""
                                   )


    perseusType = device_property(dtype=str, default_value='simulated')

    # start protected zone ====
    def init_itck_matrix(self):
        pass
    # end protected zone ====

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
    def get_Rvtet1(self):
        return self.read_milivolts(0)

    @DebugIt()
    def set_Rvtet1(self, Rvtet1):
        self.write_milivolts(Rvtet1, 0)

    @DebugIt()
    def get_Rvtet2(self):
        return self.read_milivolts(1)

    @DebugIt()
    def set_Rvtet2(self, Rvtet2):
        self.write_milivolts(Rvtet2, 1)

    @DebugIt()
    def get_Rvcirc(self):
        return self.read_milivolts(2)

    @DebugIt()
    def set_Rvcirc(self, Rvcirc):
        self.write_milivolts(Rvcirc, 2)

    @DebugIt()
    def get_Fwload(self):
        return self.read_milivolts(3)

    @DebugIt()
    def set_Fwload(self, Fwload):
        self.write_milivolts(Fwload, 3)

    @DebugIt()
    def get_Fwhybload(self):
        return self.read_milivolts(4)

    @DebugIt()
    def set_Fwhybload(self, Fwhybload):
        self.write_milivolts(Fwhybload, 4)

    @DebugIt()
    def get_Rvcav(self):
        return self.read_milivolts(5)

    @DebugIt()
    def set_Rvcav(self, Rvcav):
        self.write_milivolts(Rvcav, 5)

    @DebugIt()
    def get_ManualInterlock(self):
        return self.read_direct(6)

    @DebugIt()
    def set_ManualInterlock(self, ManualInterlock):
        self.write_direct(ManualInterlock, 6)

    @DebugIt()
    def get_DisableItckRvtet1(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckRvtet1(self, DisableItckRvtet1):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_DisableItckRvtet2(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckRvtet2(self, DisableItckRvtet2):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_DisableItckRvcirc(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckRvcirc(self, DisableItckRvcirc):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_DisableItckFwload(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckFwload(self, DisableItckFwload):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_DisableItckFwhybload(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckFwhybload(self, DisableItckFwhybload):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_DisableItckRvcav(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckRvcav(self, DisableItckRvcav):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_DisableItckArcs(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckArcs(self, DisableItckArcs):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_DisableItckVaccum(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckVaccum(self, DisableItckVaccum):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_DisableItckManualInterlock(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckManualInterlock(self, DisableItckManualInterlock):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesUp(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesUp(self, DisableItckPlungerEndSwitchesUp):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesDown(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesDown(self, DisableItckPlungerEndSwitchesDown):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_DisableItckMps(self):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def set_DisableItckMps(self, DisableItckMps):
        #@todo: insert here your code ...
        pass

    @DebugIt()
    def get_SamplesToAverage(self):
        return self.read_direct(19)

    @DebugIt()
    def set_SamplesToAverage(self, SamplesToAverage):
        self.write_direct(SamplesToAverage, 19)

    @DebugIt()
    def get_PulseupLogicInversion(self):
        return self.read_direct(20)

    @DebugIt()
    def set_PulseupLogicInversion(self, PulseupLogicInversion):
        self.write_direct(PulseupLogicInversion, 20)

    @DebugIt()
    def get_EndSwitchesConnectedToNoNcContact(self):
        return self.read_direct(21)

    @DebugIt()
    def set_EndSwitchesConnectedToNoNcContact(self, EndSwitchesConnectedToNoNcContact):
        self.write_direct(EndSwitchesConnectedToNoNcContact, 21)

    @DebugIt()
    def get_Lookref(self):
        return self.read_direct(22)

    @DebugIt()
    def set_Lookref(self, Lookref):
        self.write_direct(Lookref, 22)

    @DebugIt()
    def get_Quadref(self):
        return self.read_direct(23)

    @DebugIt()
    def set_Quadref(self, Quadref):
        self.write_direct(Quadref, 23)

    @DebugIt()
    def get_SpareDo1(self):
        return self.read_direct(24)

    @DebugIt()
    def set_SpareDo1(self, SpareDo1):
        self.write_direct(SpareDo1, 24)

    @DebugIt()
    def get_SpareDo2(self):
        return self.read_direct(25)

    @DebugIt()
    def set_SpareDo2(self, SpareDo2):
        self.write_direct(SpareDo2, 25)

    @DebugIt()
    def get_SpareDo3(self):
        return self.read_direct(26)

    @DebugIt()
    def set_SpareDo3(self, SpareDo3):
        self.write_direct(SpareDo3, 26)

    @DebugIt()
    def get_FdlSwTrigger(self):
        return self.read_direct(27)

    @DebugIt()
    def set_FdlSwTrigger(self, FdlSwTrigger):
        self.write_direct(FdlSwTrigger, 27)

    @DebugIt()
    def get_ResetInterlocksCavA(self):
        return self.read_direct(100)

    @DebugIt()
    def set_ResetInterlocksCavA(self, ResetInterlocksCavA):
        self.write_direct(ResetInterlocksCavA, 100)

    @DebugIt()
    def get_Landautuningenable(self):
        return self.read_direct(200)

    @DebugIt()
    def set_Landautuningenable(self, Landautuningenable):
        self.write_direct(Landautuningenable, 200)

    @DebugIt()
    def get_Landautuningreset(self):
        return self.read_direct(201)

    @DebugIt()
    def set_Landautuningreset(self, Landautuningreset):
        self.write_direct(Landautuningreset, 201)

    @DebugIt()
    def get_Movelandauup(self):
        return self.read_direct(202)

    @DebugIt()
    def set_Movelandauup(self, Movelandauup):
        self.write_direct(Movelandauup, 202)

    @DebugIt()
    def get_Movelandauplg(self):
        return self.read_direct(203)

    @DebugIt()
    def set_Movelandauplg(self, Movelandauplg):
        self.write_direct(Movelandauplg, 203)

    @DebugIt()
    def get_Numsteps(self):
        return self.read_milivolts(204)

    @DebugIt()
    def set_Numsteps(self, Numsteps):
        self.write_milivolts(Numsteps, 204)

    @DebugIt()
    def get_Landauphaseoffset(self):
        return self.read_angle(205)

    @DebugIt()
    def set_Landauphaseoffset(self, Landauphaseoffset):
        self.write_angle(Landauphaseoffset, 205)

    @DebugIt()
    def get_Landaumarginup(self):
        return self.read_milivolts(206)

    @DebugIt()
    def set_Landaumarginup(self, Landaumarginup):
        self.write_milivolts(Landaumarginup, 206)

    @DebugIt()
    def get_LandauMarginLow(self):
        return self.read_milivolts(207)

    @DebugIt()
    def set_LandauMarginLow(self, LandauMarginLow):
        self.write_milivolts(LandauMarginLow, 207)

    @DebugIt()
    def get_MinimumLandauAmplitude(self):
        return self.read_milivolts(208)

    @DebugIt()
    def set_MinimumLandauAmplitude(self, MinimumLandauAmplitude):
        self.write_milivolts(MinimumLandauAmplitude, 208)

    @DebugIt()
    def get_LandauPositiveEnable(self):
        return self.read_direct(209)

    @DebugIt()
    def set_LandauPositiveEnable(self, LandauPositiveEnable):
        self.write_direct(LandauPositiveEnable, 209)

    @DebugIt()
    def get_Landauampsetting(self):
        return self.read_milivolts(210)

    @DebugIt()
    def set_Landauampsetting(self, Landauampsetting):
        self.write_milivolts(Landauampsetting, 210)

    @DebugIt()
    def read_Diag_Irvtet1(self):
        return self._Diag_Irvtet1

    @DebugIt()
    def read_Diag_Qrvtet1(self):
        return self._Diag_Qrvtet1

    @DebugIt()
    def read_Diag_Amprvtet1(self):
        return self._Diag_Amprvtet1

    @DebugIt()
    def read_Diag_Phrvtet1(self):
        return self._Diag_Phrvtet1

    @DebugIt()
    def read_Diag_Irvtet2(self):
        return self._Diag_Irvtet2

    @DebugIt()
    def read_Diag_Qrvtet2(self):
        return self._Diag_Qrvtet2

    @DebugIt()
    def read_Diag_Amprvtet2(self):
        return self._Diag_Amprvtet2

    @DebugIt()
    def read_Diag_Phrvtet2(self):
        return self._Diag_Phrvtet2

    @DebugIt()
    def read_Diag_Ifwcirc(self):
        return self._Diag_Ifwcirc

    @DebugIt()
    def read_Diag_Qfwcirc(self):
        return self._Diag_Qfwcirc

    @DebugIt()
    def read_Diag_Ampfwcirc(self):
        return self._Diag_Ampfwcirc

    @DebugIt()
    def read_Diag_Phfwcirc(self):
        return self._Diag_Phfwcirc

    @DebugIt()
    def read_Diag_Irvcirc(self):
        return self._Diag_Irvcirc

    @DebugIt()
    def read_Diag_Qrvcirc(self):
        return self._Diag_Qrvcirc

    @DebugIt()
    def read_Diag_Amprvcirc(self):
        return self._Diag_Amprvcirc

    @DebugIt()
    def read_Diag_Phrvcirc(self):
        return self._Diag_Phrvcirc

    @DebugIt()
    def read_Diag_Ifwload(self):
        return self._Diag_Ifwload

    @DebugIt()
    def read_Diag_Qfwload(self):
        return self._Diag_Qfwload

    @DebugIt()
    def read_Diag_Ampfwload(self):
        return self._Diag_Ampfwload

    @DebugIt()
    def read_Diag_Phfwload(self):
        return self._Diag_Phfwload

    @DebugIt()
    def read_Diag_Ifwhybload(self):
        return self._Diag_Ifwhybload

    @DebugIt()
    def read_Diag_Qfwhybload(self):
        return self._Diag_Qfwhybload

    @DebugIt()
    def read_Diag_Ampfwhybload(self):
        return self._Diag_Ampfwhybload

    @DebugIt()
    def read_Diag_Phfwhybload(self):
        return self._Diag_Phfwhybload

    @DebugIt()
    def read_Diag_Irvcav(self):
        return self._Diag_Irvcav

    @DebugIt()
    def read_Diag_Qrvcav(self):
        return self._Diag_Qrvcav

    @DebugIt()
    def read_Diag_Amprvcav(self):
        return self._Diag_Amprvcav

    @DebugIt()
    def read_Diag_Phrvcav(self):
        return self._Diag_Phrvcav

    @DebugIt()
    def read_Diag_Imo(self):
        return self._Diag_Imo

    @DebugIt()
    def read_Diag_Qmo(self):
        return self._Diag_Qmo

    @DebugIt()
    def read_Diag_Ampmo(self):
        return self._Diag_Ampmo

    @DebugIt()
    def read_Diag_Phmo(self):
        return self._Diag_Phmo

    @DebugIt()
    def read_Diag_Ilandau(self):
        return self._Diag_Ilandau

    @DebugIt()
    def read_Diag_Qlandadu(self):
        return self._Diag_Qlandadu

    @DebugIt()
    def read_Diag_Amplandadu(self):
        return self._Diag_Amplandadu

    @DebugIt()
    def read_Diag_Phlandadu(self):
        return self._Diag_Phlandadu

    @DebugIt()
    def read_Diag_PlungerMovingManualTuning(self):
        return self._Diag_PlungerMovingManualTuning

    @DebugIt()
    def read_Diag_PlungerMovingUpManualTuning(self):
        return self._Diag_PlungerMovingUpManualTuning

    @DebugIt()
    def read_Diag_PlungerMovingAutomaticTuning(self):
        return self._Diag_PlungerMovingAutomaticTuning

    @DebugIt()
    def read_Diag_PlungerMovingUpAutomaticTuning(self):
        return self._Diag_PlungerMovingUpAutomaticTuning

    @DebugIt()
    def read_Diag_DephaseMoLandau(self):
        return self._Diag_DephaseMoLandau

    @DebugIt()
    def read_Diag_Rvtet1(self):
        return self._Diag_Rvtet1

    @DebugIt()
    def read_Diag_Rvtet2(self):
        return self._Diag_Rvtet2

    @DebugIt()
    def read_Diag_Rvcirc(self):
        return self._Diag_Rvcirc

    @DebugIt()
    def read_Diag_Fwload(self):
        return self._Diag_Fwload

    @DebugIt()
    def read_Diag_Fwhybload(self):
        return self._Diag_Fwhybload

    @DebugIt()
    def read_Diag_Rvcav(self):
        return self._Diag_Rvcav

    @DebugIt()
    def read_Diag_Arcs(self):
        return self._Diag_Arcs

    @DebugIt()
    def read_Diag_Vacuum(self):
        return self._Diag_Vacuum

    @DebugIt()
    def read_Diag_ManualInterlock(self):
        return self._Diag_ManualInterlock

    @DebugIt()
    def read_Diag_ExternalItck(self):
        return self._Diag_ExternalItck

    @DebugIt()
    def read_Diag_PlungerEndSwitchUp(self):
        return self._Diag_PlungerEndSwitchUp

    @DebugIt()
    def read_Diag_PlungerEndSwitchDown(self):
        return self._Diag_PlungerEndSwitchDown

    @DebugIt()
    def read_Diag_Timestamp1(self):
        return self._Diag_Timestamp1

    @DebugIt()
    def read_Diag_Timestamp2(self):
        return self._Diag_Timestamp2

    @DebugIt()
    def read_Diag_Timestamp3(self):
        return self._Diag_Timestamp3

    @DebugIt()
    def read_Diag_Timestamp4(self):
        return self._Diag_Timestamp4

    @DebugIt()
    def read_Diag_Timestamp5(self):
        return self._Diag_Timestamp5

    @DebugIt()
    def read_Diag_Timestamp6(self):
        return self._Diag_Timestamp6

    @DebugIt()
    def read_Diag_Timestamp7(self):
        return self._Diag_Timestamp7

    @DebugIt()
    def read_Diag_DacsDisableCommand(self):
        return self._Diag_DacsDisableCommand

    @DebugIt()
    def read_Diag_PinSwitch(self):
        return self._Diag_PinSwitch

    @DebugIt()
    def read_Diag_FdlTriggerToLoopsdiagboard(self):
        return self._Diag_FdlTriggerToLoopsdiagboard

    @DebugIt()
    def read_Diag_OutputToPlc(self):
        return self._Diag_OutputToPlc

    @DebugIt()
    def read_Diag_OutputToMps(self):
        return self._Diag_OutputToMps

    @DebugIt()
    def read_Diag_LandauMovingLed(self):
        return self._Diag_LandauMovingLed

    @DebugIt()
    def read_Diag_LandauPulseMotor(self):
        return self._Diag_LandauPulseMotor

    @DebugIt()
    def read_Diag_LandauDirMotor(self):
        return self._Diag_LandauDirMotor

    @DebugIt()
    def read_Diag_LandauMovingUpLed(self):
        return self._Diag_LandauMovingUpLed

    @DebugIt()
    def read_Diag_FdlTriggerForDiagnosticsPurposes(self):
        return self._Diag_FdlTriggerForDiagnosticsPurposes

    @DebugIt()
    def read_Diag_SpareDo01(self):
        return self._Diag_SpareDo01

    @DebugIt()
    def read_Diag_SpareDo02(self):
        return self._Diag_SpareDo02

    @DebugIt()
    def read_Diag_SpareDo03(self):
        return self._Diag_SpareDo03

    @command
    def read_diagnostics(self):
        self.start_reading_diagnostics()

        self._Diag_Irvtet1 = self.read_diag_milivolts(0)
        self._Diag_Qrvtet1 = self.read_diag_milivolts(1)
        self._Diag_Amprvtet1 = self.read_diag_milivolts(2)
        self._Diag_Phrvtet1 = self.read_diag_angle(3)
        self._Diag_Irvtet2 = self.read_diag_milivolts(4)
        self._Diag_Qrvtet2 = self.read_diag_milivolts(5)
        self._Diag_Amprvtet2 = self.read_diag_milivolts(6)
        self._Diag_Phrvtet2 = self.read_diag_angle(7)
        self._Diag_Ifwcirc = self.read_diag_milivolts(8)
        self._Diag_Qfwcirc = self.read_diag_milivolts(9)
        self._Diag_Ampfwcirc = self.read_diag_milivolts(10)
        self._Diag_Phfwcirc = self.read_diag_angle(11)
        self._Diag_Irvcirc = self.read_diag_milivolts(12)
        self._Diag_Qrvcirc = self.read_diag_milivolts(13)
        self._Diag_Amprvcirc = self.read_diag_milivolts(14)
        self._Diag_Phrvcirc = self.read_diag_angle(15)
        self._Diag_Ifwload = self.read_diag_milivolts(16)
        self._Diag_Qfwload = self.read_diag_milivolts(17)
        self._Diag_Ampfwload = self.read_diag_milivolts(18)
        self._Diag_Phfwload = self.read_diag_angle(19)
        self._Diag_Ifwhybload = self.read_diag_milivolts(20)
        self._Diag_Qfwhybload = self.read_diag_milivolts(21)
        self._Diag_Ampfwhybload = self.read_diag_milivolts(22)
        self._Diag_Phfwhybload = self.read_diag_angle(23)
        self._Diag_Irvcav = self.read_diag_milivolts(24)
        self._Diag_Qrvcav = self.read_diag_milivolts(25)
        self._Diag_Amprvcav = self.read_diag_milivolts(26)
        self._Diag_Phrvcav = self.read_diag_angle(27)
        self._Diag_Imo = self.read_diag_milivolts(28)
        self._Diag_Qmo = self.read_diag_milivolts(29)
        self._Diag_Ampmo = self.read_diag_milivolts(30)
        self._Diag_Phmo = self.read_diag_angle(31)
        self._Diag_Ilandau = self.read_diag_milivolts(32)
        self._Diag_Qlandadu = self.read_diag_milivolts(33)
        self._Diag_Amplandadu = self.read_diag_milivolts(34)
        self._Diag_Phlandadu = self.read_diag_angle(35)
        self._Diag_DephaseMoLandau = self.read_diag_angle(64)

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
    run([NutaqDiags])
