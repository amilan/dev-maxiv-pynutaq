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

    Rvtet1 = attribute(label='Rvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
                                   fget="get_ManualInterlock",
                                   fset="set_ManualInterlock",
                                   doc=""
                                   )

    DisableItckRvtet1 = attribute(label='DisableItckRvtet1',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
                                   fget="get_PulseupLogicInversion",
                                   fset="set_PulseupLogicInversion",
                                   doc=""
                                   )

    EndSwitchesConnectedToNoNcContact = attribute(label='EndSwitchesConnectedToNoNcContact',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
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
                                   format='%6.2f',
                                   fget="get_Lookref",
                                   fset="set_Lookref",
                                   doc=""
                                   )

    Quadref = attribute(label='Quadref',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
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
                                   format='%6.2f',
                                   fget="get_SpareDo1",
                                   fset="set_SpareDo1",
                                   doc=""
                                   )

    SpareDo2 = attribute(label='SpareDo2',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_SpareDo2",
                                   fset="set_SpareDo2",
                                   doc=""
                                   )

    SpareDo3 = attribute(label='SpareDo3',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_SpareDo3",
                                   fset="set_SpareDo3",
                                   doc=""
                                   )

    FdlSwTrigger = attribute(label='FdlSwTrigger',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_FdlSwTrigger",
                                   fset="set_FdlSwTrigger",
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

    Landautuningenable = attribute(label='Landautuningenable',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_Landautuningenable",
                                   fset="set_Landautuningenable",
                                   doc=""
                                   )

    Landautuningreset = attribute(label='Landautuningreset',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_Landautuningreset",
                                   fset="set_Landautuningreset",
                                   doc=""
                                   )

    Movelandauup = attribute(label='Movelandauup',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_Movelandauup",
                                   fset="set_Movelandauup",
                                   doc=""
                                   )

    Movelandauplg = attribute(label='Movelandauplg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_Movelandauplg",
                                   fset="set_Movelandauplg",
                                   doc=""
                                   )

    Numsteps = attribute(label='Numsteps',
                                   dtype=int,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=10000,
                                   fget="get_Numsteps",
                                   fset="set_Numsteps",
                                   doc=""
                                   )

    Landauphaseoffset = attribute(label='Landauphaseoffset',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='degrees',
                                   format='%6.2f',
                                   min_value=-180, max_value=180,
                                   fget="get_Landauphaseoffset",
                                   fset="set_Landauphaseoffset",
                                   doc=""
                                   )

    Landaumarginup = attribute(label='Landaumarginup',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   min_value=0, max_value=50,
                                   fget="get_Landaumarginup",
                                   fset="set_Landaumarginup",
                                   doc=""
                                   )

    LandauMarginLow = attribute(label='LandauMarginLow',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
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
                                   format='%6.2f',
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
                                   format='%6.2f',
                                   fget="get_LandauPositiveEnable",
                                   fset="set_LandauPositiveEnable",
                                   doc=""
                                   )

    Landauampsetting = attribute(label='Landauampsetting',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='mV',
                                   format='%6.2f',
                                   min_value=0, max_value=1000,
                                   fget="get_Landauampsetting",
                                   fset="set_Landauampsetting",
                                   doc=""
                                   )

    DisitckRvtet1Dacsoffloopsstby = attribute(label='DisitckRvtet1Dacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1Dacsoffloopsstby",
                                   fset="set_DisitckRvtet1Dacsoffloopsstby",
                                   doc=""
                                   )

    DisitckRvtet1Pindiodeswitch = attribute(label='DisitckRvtet1Pindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1Pindiodeswitch",
                                   fset="set_DisitckRvtet1Pindiodeswitch",
                                   doc=""
                                   )

    DisitckRvtet1Fdltrg = attribute(label='DisitckRvtet1Fdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1Fdltrg",
                                   fset="set_DisitckRvtet1Fdltrg",
                                   doc=""
                                   )

    DisitckRvtet1Plctxoff = attribute(label='DisitckRvtet1Plctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1Plctxoff",
                                   fset="set_DisitckRvtet1Plctxoff",
                                   doc=""
                                   )

    DisitckRvtet1Mps = attribute(label='DisitckRvtet1Mps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1Mps",
                                   fset="set_DisitckRvtet1Mps",
                                   doc=""
                                   )

    DisitckRvtet1Diag = attribute(label='DisitckRvtet1Diag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet1Diag",
                                   fset="set_DisitckRvtet1Diag",
                                   doc=""
                                   )

    DisitckRvtet2Dacsoffloopsstby = attribute(label='DisitckRvtet2Dacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2Dacsoffloopsstby",
                                   fset="set_DisitckRvtet2Dacsoffloopsstby",
                                   doc=""
                                   )

    DisitckRvtet2Pindiodeswitch = attribute(label='DisitckRvtet2Pindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2Pindiodeswitch",
                                   fset="set_DisitckRvtet2Pindiodeswitch",
                                   doc=""
                                   )

    DisitckRvtet2Fdltrg = attribute(label='DisitckRvtet2Fdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2Fdltrg",
                                   fset="set_DisitckRvtet2Fdltrg",
                                   doc=""
                                   )

    DisitckRvtet2Plctxoff = attribute(label='DisitckRvtet2Plctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2Plctxoff",
                                   fset="set_DisitckRvtet2Plctxoff",
                                   doc=""
                                   )

    DisitckRvtet2Mps = attribute(label='DisitckRvtet2Mps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2Mps",
                                   fset="set_DisitckRvtet2Mps",
                                   doc=""
                                   )

    DisitckRvtet2Diag = attribute(label='DisitckRvtet2Diag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvtet2Diag",
                                   fset="set_DisitckRvtet2Diag",
                                   doc=""
                                   )

    DisitckRvcircDacsoffloopsstby = attribute(label='DisitckRvcircDacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircDacsoffloopsstby",
                                   fset="set_DisitckRvcircDacsoffloopsstby",
                                   doc=""
                                   )

    DisitckRvcircPindiodeswitch = attribute(label='DisitckRvcircPindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircPindiodeswitch",
                                   fset="set_DisitckRvcircPindiodeswitch",
                                   doc=""
                                   )

    DisitckRvcircFdltrg = attribute(label='DisitckRvcircFdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircFdltrg",
                                   fset="set_DisitckRvcircFdltrg",
                                   doc=""
                                   )

    DisitckRvcircPlctxoff = attribute(label='DisitckRvcircPlctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircPlctxoff",
                                   fset="set_DisitckRvcircPlctxoff",
                                   doc=""
                                   )

    DisitckRvcircMps = attribute(label='DisitckRvcircMps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircMps",
                                   fset="set_DisitckRvcircMps",
                                   doc=""
                                   )

    DisitckRvcircDiag = attribute(label='DisitckRvcircDiag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcircDiag",
                                   fset="set_DisitckRvcircDiag",
                                   doc=""
                                   )

    DisitckFwloadDacsoffloopsstby = attribute(label='DisitckFwloadDacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadDacsoffloopsstby",
                                   fset="set_DisitckFwloadDacsoffloopsstby",
                                   doc=""
                                   )

    DisitckFwloadPindiodeswitch = attribute(label='DisitckFwloadPindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadPindiodeswitch",
                                   fset="set_DisitckFwloadPindiodeswitch",
                                   doc=""
                                   )

    DisitckFwloadFdltrg = attribute(label='DisitckFwloadFdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadFdltrg",
                                   fset="set_DisitckFwloadFdltrg",
                                   doc=""
                                   )

    DisitckFwloadPlctxoff = attribute(label='DisitckFwloadPlctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadPlctxoff",
                                   fset="set_DisitckFwloadPlctxoff",
                                   doc=""
                                   )

    DisitckFwloadMps = attribute(label='DisitckFwloadMps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadMps",
                                   fset="set_DisitckFwloadMps",
                                   doc=""
                                   )

    DisitckFwloadDiag = attribute(label='DisitckFwloadDiag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwloadDiag",
                                   fset="set_DisitckFwloadDiag",
                                   doc=""
                                   )

    DisitckFwhybloadDacsoffloopsstby = attribute(label='DisitckFwhybloadDacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadDacsoffloopsstby",
                                   fset="set_DisitckFwhybloadDacsoffloopsstby",
                                   doc=""
                                   )

    DisitckFwhybloadPindiodeswitch = attribute(label='DisitckFwhybloadPindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadPindiodeswitch",
                                   fset="set_DisitckFwhybloadPindiodeswitch",
                                   doc=""
                                   )

    DisitckFwhybloadFdltrg = attribute(label='DisitckFwhybloadFdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadFdltrg",
                                   fset="set_DisitckFwhybloadFdltrg",
                                   doc=""
                                   )

    DisitckFwhybloadPlctxoff = attribute(label='DisitckFwhybloadPlctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadPlctxoff",
                                   fset="set_DisitckFwhybloadPlctxoff",
                                   doc=""
                                   )

    DisitckFwhybloadMps = attribute(label='DisitckFwhybloadMps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadMps",
                                   fset="set_DisitckFwhybloadMps",
                                   doc=""
                                   )

    DisitckFwhybloadDiag = attribute(label='DisitckFwhybloadDiag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckFwhybloadDiag",
                                   fset="set_DisitckFwhybloadDiag",
                                   doc=""
                                   )

    DisitckRvcavDacsoffloopsstby = attribute(label='DisitckRvcavDacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavDacsoffloopsstby",
                                   fset="set_DisitckRvcavDacsoffloopsstby",
                                   doc=""
                                   )

    DisitckRvcavPindiodeswitch = attribute(label='DisitckRvcavPindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavPindiodeswitch",
                                   fset="set_DisitckRvcavPindiodeswitch",
                                   doc=""
                                   )

    DisitckRvcavFdltrg = attribute(label='DisitckRvcavFdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavFdltrg",
                                   fset="set_DisitckRvcavFdltrg",
                                   doc=""
                                   )

    DisitckRvcavPlctxoff = attribute(label='DisitckRvcavPlctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavPlctxoff",
                                   fset="set_DisitckRvcavPlctxoff",
                                   doc=""
                                   )

    DisitckRvcavMps = attribute(label='DisitckRvcavMps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavMps",
                                   fset="set_DisitckRvcavMps",
                                   doc=""
                                   )

    DisitckRvcavDiag = attribute(label='DisitckRvcavDiag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckRvcavDiag",
                                   fset="set_DisitckRvcavDiag",
                                   doc=""
                                   )

    DisitckArcsDacsoffloopsstby = attribute(label='DisitckArcsDacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsDacsoffloopsstby",
                                   fset="set_DisitckArcsDacsoffloopsstby",
                                   doc=""
                                   )

    DisitckArcsPindiodeswitch = attribute(label='DisitckArcsPindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsPindiodeswitch",
                                   fset="set_DisitckArcsPindiodeswitch",
                                   doc=""
                                   )

    DisitckArcsFdltrg = attribute(label='DisitckArcsFdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsFdltrg",
                                   fset="set_DisitckArcsFdltrg",
                                   doc=""
                                   )

    DisitckArcsPlctxoff = attribute(label='DisitckArcsPlctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsPlctxoff",
                                   fset="set_DisitckArcsPlctxoff",
                                   doc=""
                                   )

    DisitckArcsMps = attribute(label='DisitckArcsMps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsMps",
                                   fset="set_DisitckArcsMps",
                                   doc=""
                                   )

    DisitckArcsDiag = attribute(label='DisitckArcsDiag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckArcsDiag",
                                   fset="set_DisitckArcsDiag",
                                   doc=""
                                   )

    DisitckVacuumDacsoffloopsstby = attribute(label='DisitckVacuumDacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumDacsoffloopsstby",
                                   fset="set_DisitckVacuumDacsoffloopsstby",
                                   doc=""
                                   )

    DisitckVacuumPindiodeswitch = attribute(label='DisitckVacuumPindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumPindiodeswitch",
                                   fset="set_DisitckVacuumPindiodeswitch",
                                   doc=""
                                   )

    DisitckVacuumFdltrg = attribute(label='DisitckVacuumFdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumFdltrg",
                                   fset="set_DisitckVacuumFdltrg",
                                   doc=""
                                   )

    DisitckVacuumPlctxoff = attribute(label='DisitckVacuumPlctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumPlctxoff",
                                   fset="set_DisitckVacuumPlctxoff",
                                   doc=""
                                   )

    DisitckVacuumMps = attribute(label='DisitckVacuumMps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumMps",
                                   fset="set_DisitckVacuumMps",
                                   doc=""
                                   )

    DisitckVacuumDiag = attribute(label='DisitckVacuumDiag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckVacuumDiag",
                                   fset="set_DisitckVacuumDiag",
                                   doc=""
                                   )

    DisitckManualInterlockDacsoffloopsstby = attribute(label='DisitckManualInterlockDacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockDacsoffloopsstby",
                                   fset="set_DisitckManualInterlockDacsoffloopsstby",
                                   doc=""
                                   )

    DisitckManualInterlockPindiodeswitch = attribute(label='DisitckManualInterlockPindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockPindiodeswitch",
                                   fset="set_DisitckManualInterlockPindiodeswitch",
                                   doc=""
                                   )

    DisitckManualInterlockFdltrg = attribute(label='DisitckManualInterlockFdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockFdltrg",
                                   fset="set_DisitckManualInterlockFdltrg",
                                   doc=""
                                   )

    DisitckManualInterlockPlctxoff = attribute(label='DisitckManualInterlockPlctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockPlctxoff",
                                   fset="set_DisitckManualInterlockPlctxoff",
                                   doc=""
                                   )

    DisitckManualInterlockMps = attribute(label='DisitckManualInterlockMps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockMps",
                                   fset="set_DisitckManualInterlockMps",
                                   doc=""
                                   )

    DisitckManualInterlockDiag = attribute(label='DisitckManualInterlockDiag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckManualInterlockDiag",
                                   fset="set_DisitckManualInterlockDiag",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpDacsoffloopsstby = attribute(label='DisitckPlungerEndSwitchesUpDacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpDacsoffloopsstby",
                                   fset="set_DisitckPlungerEndSwitchesUpDacsoffloopsstby",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpPindiodeswitch = attribute(label='DisitckPlungerEndSwitchesUpPindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpPindiodeswitch",
                                   fset="set_DisitckPlungerEndSwitchesUpPindiodeswitch",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpFdltrg = attribute(label='DisitckPlungerEndSwitchesUpFdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpFdltrg",
                                   fset="set_DisitckPlungerEndSwitchesUpFdltrg",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpPlctxoff = attribute(label='DisitckPlungerEndSwitchesUpPlctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpPlctxoff",
                                   fset="set_DisitckPlungerEndSwitchesUpPlctxoff",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpMps = attribute(label='DisitckPlungerEndSwitchesUpMps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpMps",
                                   fset="set_DisitckPlungerEndSwitchesUpMps",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesUpDiag = attribute(label='DisitckPlungerEndSwitchesUpDiag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesUpDiag",
                                   fset="set_DisitckPlungerEndSwitchesUpDiag",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownDacsoffloopsstby = attribute(label='DisitckPlungerEndSwitchesDownDacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownDacsoffloopsstby",
                                   fset="set_DisitckPlungerEndSwitchesDownDacsoffloopsstby",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownPindiodeswitch = attribute(label='DisitckPlungerEndSwitchesDownPindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownPindiodeswitch",
                                   fset="set_DisitckPlungerEndSwitchesDownPindiodeswitch",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownFdltrg = attribute(label='DisitckPlungerEndSwitchesDownFdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownFdltrg",
                                   fset="set_DisitckPlungerEndSwitchesDownFdltrg",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownPlctxoff = attribute(label='DisitckPlungerEndSwitchesDownPlctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownPlctxoff",
                                   fset="set_DisitckPlungerEndSwitchesDownPlctxoff",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownMps = attribute(label='DisitckPlungerEndSwitchesDownMps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownMps",
                                   fset="set_DisitckPlungerEndSwitchesDownMps",
                                   doc=""
                                   )

    DisitckPlungerEndSwitchesDownDiag = attribute(label='DisitckPlungerEndSwitchesDownDiag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckPlungerEndSwitchesDownDiag",
                                   fset="set_DisitckPlungerEndSwitchesDownDiag",
                                   doc=""
                                   )

    DisitckMpsDacsoffloopsstby = attribute(label='DisitckMpsDacsoffloopsstby',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsDacsoffloopsstby",
                                   fset="set_DisitckMpsDacsoffloopsstby",
                                   doc=""
                                   )

    DisitckMpsPindiodeswitch = attribute(label='DisitckMpsPindiodeswitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsPindiodeswitch",
                                   fset="set_DisitckMpsPindiodeswitch",
                                   doc=""
                                   )

    DisitckMpsFdltrg = attribute(label='DisitckMpsFdltrg',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsFdltrg",
                                   fset="set_DisitckMpsFdltrg",
                                   doc=""
                                   )

    DisitckMpsPlctxoff = attribute(label='DisitckMpsPlctxoff',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsPlctxoff",
                                   fset="set_DisitckMpsPlctxoff",
                                   doc=""
                                   )

    DisitckMpsMps = attribute(label='DisitckMpsMps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsMps",
                                   fset="set_DisitckMpsMps",
                                   doc=""
                                   )

    DisitckMpsDiag = attribute(label='DisitckMpsDiag',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit='',
                                   format='%6.2f',
                                   fget="get_DisitckMpsDiag",
                                   fset="set_DisitckMpsDiag",
                                   doc=""
                                   )

    Diag_Irvtet1 = attribute(label='Diag_Irvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvtet1 = attribute(label='Diag_Qrvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvtet1 = attribute(label='Diag_Amprvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvtet1 = attribute(label='Diag_Phrvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Irvtet2 = attribute(label='Diag_Irvtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvtet2 = attribute(label='Diag_Qrvtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvtet2 = attribute(label='Diag_Amprvtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvtet2 = attribute(label='Diag_Phrvtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ifwcirc = attribute(label='Diag_Ifwcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qfwcirc = attribute(label='Diag_Qfwcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ampfwcirc = attribute(label='Diag_Ampfwcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phfwcirc = attribute(label='Diag_Phfwcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Irvcirc = attribute(label='Diag_Irvcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvcirc = attribute(label='Diag_Qrvcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvcirc = attribute(label='Diag_Amprvcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvcirc = attribute(label='Diag_Phrvcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ifwload = attribute(label='Diag_Ifwload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qfwload = attribute(label='Diag_Qfwload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ampfwload = attribute(label='Diag_Ampfwload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phfwload = attribute(label='Diag_Phfwload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ifwhybload = attribute(label='Diag_Ifwhybload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qfwhybload = attribute(label='Diag_Qfwhybload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ampfwhybload = attribute(label='Diag_Ampfwhybload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phfwhybload = attribute(label='Diag_Phfwhybload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Irvcav = attribute(label='Diag_Irvcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qrvcav = attribute(label='Diag_Qrvcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amprvcav = attribute(label='Diag_Amprvcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phrvcav = attribute(label='Diag_Phrvcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Imo = attribute(label='Diag_Imo',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qmo = attribute(label='Diag_Qmo',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ampmo = attribute(label='Diag_Ampmo',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phmo = attribute(label='Diag_Phmo',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Ilandau = attribute(label='Diag_Ilandau',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Qlandau = attribute(label='Diag_Qlandau',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Amplandau = attribute(label='Diag_Amplandau',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Phlandau = attribute(label='Diag_Phlandau',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingManualTuning = attribute(label='Diag_PlungerMovingManualTuning',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpManualTuning = attribute(label='Diag_PlungerMovingUpManualTuning',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingAutomaticTuning = attribute(label='Diag_PlungerMovingAutomaticTuning',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerMovingUpAutomaticTuning = attribute(label='Diag_PlungerMovingUpAutomaticTuning',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_DephaseMoLandau = attribute(label='Diag_DephaseMoLandau',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvtet1 = attribute(label='Diag_Rvtet1',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvtet2 = attribute(label='Diag_Rvtet2',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvcirc = attribute(label='Diag_Rvcirc',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Fwload = attribute(label='Diag_Fwload',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Fwhybload = attribute(label='Diag_Fwhybload',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Rvcav = attribute(label='Diag_Rvcav',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Arcs = attribute(label='Diag_Arcs',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Vacuum = attribute(label='Diag_Vacuum',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ManualInterlock = attribute(label='Diag_ManualInterlock',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_ExternalItck = attribute(label='Diag_ExternalItck',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchUp = attribute(label='Diag_PlungerEndSwitchUp',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PlungerEndSwitchDown = attribute(label='Diag_PlungerEndSwitchDown',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp1 = attribute(label='Diag_Timestamp1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp2 = attribute(label='Diag_Timestamp2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp3 = attribute(label='Diag_Timestamp3',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp4 = attribute(label='Diag_Timestamp4',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp5 = attribute(label='Diag_Timestamp5',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp6 = attribute(label='Diag_Timestamp6',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_Timestamp7 = attribute(label='Diag_Timestamp7',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_DacsDisableCommand = attribute(label='Diag_DacsDisableCommand',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PinSwitch = attribute(label='Diag_PinSwitch',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_FdlTriggerToLoopsdiagboard = attribute(label='Diag_FdlTriggerToLoopsdiagboard',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_OutputToPlc = attribute(label='Diag_OutputToPlc',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_OutputToMps = attribute(label='Diag_OutputToMps',
                                   dtype=bool,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvtet2 = attribute(label='Diag_AmpRvtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvtet1 = attribute(label='Diag_AmpRvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvcav = attribute(label='Diag_AmpRvcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpLandau = attribute(label='Diag_AmpLandau',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpRvcirc = attribute(label='Diag_AmpRvcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwhybload = attribute(label='Diag_AmpFwhybload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwcirc = attribute(label='Diag_AmpFwcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpFwload = attribute(label='Diag_AmpFwload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_AmpMo = attribute(label='Diag_AmpMo',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='mV',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvtet2 = attribute(label='Diag_PhRvtet2',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvtet1 = attribute(label='Diag_PhRvtet1',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvcav = attribute(label='Diag_PhRvcav',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhLandau = attribute(label='Diag_PhLandau',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhRvcirc = attribute(label='Diag_PhRvcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwhybload = attribute(label='Diag_PhFwhybload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwcirc = attribute(label='Diag_PhFwcirc',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhFwload = attribute(label='Diag_PhFwload',
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ,
                                   unit='degrees',
                                   format='%6.2f',
                                   doc=""
                                   )

    Diag_PhMo = attribute(label='Diag_PhMo',
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
    def get_Rvtet1(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 0)

    @DebugIt()
    def set_Rvtet1(self, Rvtet1):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Rvtet1, 0)

    @DebugIt()
    def get_Rvtet2(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 1)

    @DebugIt()
    def set_Rvtet2(self, Rvtet2):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Rvtet2, 1)

    @DebugIt()
    def get_Rvcirc(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 2)

    @DebugIt()
    def set_Rvcirc(self, Rvcirc):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Rvcirc, 2)

    @DebugIt()
    def get_Fwload(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 3)

    @DebugIt()
    def set_Fwload(self, Fwload):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Fwload, 3)

    @DebugIt()
    def get_Fwhybload(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 4)

    @DebugIt()
    def set_Fwhybload(self, Fwhybload):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Fwhybload, 4)

    @DebugIt()
    def get_Rvcav(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 5)

    @DebugIt()
    def set_Rvcav(self, Rvcav):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Rvcav, 5)

    @DebugIt()
    def get_ManualInterlock(self):
        return perseus_utils.read_direct(self.perseus, 6)

    @DebugIt()
    def set_ManualInterlock(self, ManualInterlock):
        perseus_utils.write_direct(self.perseus, ManualInterlock, 6)

    @DebugIt()
    def get_DisableItckRvtet1(self):
        return perseus_utils.read_direct(self.perseus, 7)

    @DebugIt()
    def set_DisableItckRvtet1(self, DisableItckRvtet1):
        perseus_utils.write_direct(self.perseus, DisableItckRvtet1, 7)

    @DebugIt()
    def get_DisableItckRvtet2(self):
        return perseus_utils.read_direct(self.perseus, 8)

    @DebugIt()
    def set_DisableItckRvtet2(self, DisableItckRvtet2):
        perseus_utils.write_direct(self.perseus, DisableItckRvtet2, 8)

    @DebugIt()
    def get_DisableItckRvcirc(self):
        return perseus_utils.read_direct(self.perseus, 9)

    @DebugIt()
    def set_DisableItckRvcirc(self, DisableItckRvcirc):
        perseus_utils.write_direct(self.perseus, DisableItckRvcirc, 9)

    @DebugIt()
    def get_DisableItckFwload(self):
        return perseus_utils.read_direct(self.perseus, 10)

    @DebugIt()
    def set_DisableItckFwload(self, DisableItckFwload):
        perseus_utils.write_direct(self.perseus, DisableItckFwload, 10)

    @DebugIt()
    def get_DisableItckFwhybload(self):
        return perseus_utils.read_direct(self.perseus, 11)

    @DebugIt()
    def set_DisableItckFwhybload(self, DisableItckFwhybload):
        perseus_utils.write_direct(self.perseus, DisableItckFwhybload, 11)

    @DebugIt()
    def get_DisableItckRvcav(self):
        return perseus_utils.read_direct(self.perseus, 12)

    @DebugIt()
    def set_DisableItckRvcav(self, DisableItckRvcav):
        perseus_utils.write_direct(self.perseus, DisableItckRvcav, 12)

    @DebugIt()
    def get_DisableItckArcs(self):
        return perseus_utils.read_direct(self.perseus, 13)

    @DebugIt()
    def set_DisableItckArcs(self, DisableItckArcs):
        perseus_utils.write_direct(self.perseus, DisableItckArcs, 13)

    @DebugIt()
    def get_DisableItckVaccum(self):
        return perseus_utils.read_direct(self.perseus, 14)

    @DebugIt()
    def set_DisableItckVaccum(self, DisableItckVaccum):
        perseus_utils.write_direct(self.perseus, DisableItckVaccum, 14)

    @DebugIt()
    def get_DisableItckManualInterlock(self):
        return perseus_utils.read_direct(self.perseus, 15)

    @DebugIt()
    def set_DisableItckManualInterlock(self, DisableItckManualInterlock):
        perseus_utils.write_direct(self.perseus, DisableItckManualInterlock, 15)

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesUp(self):
        return perseus_utils.read_direct(self.perseus, 16)

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesUp(self, DisableItckPlungerEndSwitchesUp):
        perseus_utils.write_direct(self.perseus, DisableItckPlungerEndSwitchesUp, 16)

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesDown(self):
        return perseus_utils.read_direct(self.perseus, 17)

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesDown(self, DisableItckPlungerEndSwitchesDown):
        perseus_utils.write_direct(self.perseus, DisableItckPlungerEndSwitchesDown, 17)

    @DebugIt()
    def get_DisableItckMps(self):
        return perseus_utils.read_direct(self.perseus, 18)

    @DebugIt()
    def set_DisableItckMps(self, DisableItckMps):
        perseus_utils.write_direct(self.perseus, DisableItckMps, 18)

    @DebugIt()
    def get_SamplesToAverage(self):
        return perseus_utils.read_direct(self.perseus, 19)

    @DebugIt()
    def set_SamplesToAverage(self, SamplesToAverage):
        perseus_utils.write_direct(self.perseus, SamplesToAverage, 19)

    @DebugIt()
    def get_PulseupLogicInversion(self):
        return perseus_utils.read_direct(self.perseus, 20)

    @DebugIt()
    def set_PulseupLogicInversion(self, PulseupLogicInversion):
        perseus_utils.write_direct(self.perseus, PulseupLogicInversion, 20)

    @DebugIt()
    def get_EndSwitchesConnectedToNoNcContact(self):
        return perseus_utils.read_direct(self.perseus, 21)

    @DebugIt()
    def set_EndSwitchesConnectedToNoNcContact(self, EndSwitchesConnectedToNoNcContact):
        perseus_utils.write_direct(self.perseus, EndSwitchesConnectedToNoNcContact, 21)

    @DebugIt()
    def get_Lookref(self):
        return perseus_utils.read_direct(self.perseus, 22)

    @DebugIt()
    def set_Lookref(self, Lookref):
        perseus_utils.write_direct(self.perseus, Lookref, 22)

    @DebugIt()
    def get_Quadref(self):
        return perseus_utils.read_direct(self.perseus, 23)

    @DebugIt()
    def set_Quadref(self, Quadref):
        perseus_utils.write_direct(self.perseus, Quadref, 23)

    @DebugIt()
    def get_SpareDo1(self):
        return perseus_utils.read_direct(self.perseus, 24)

    @DebugIt()
    def set_SpareDo1(self, SpareDo1):
        perseus_utils.write_direct(self.perseus, SpareDo1, 24)

    @DebugIt()
    def get_SpareDo2(self):
        return perseus_utils.read_direct(self.perseus, 25)

    @DebugIt()
    def set_SpareDo2(self, SpareDo2):
        perseus_utils.write_direct(self.perseus, SpareDo2, 25)

    @DebugIt()
    def get_SpareDo3(self):
        return perseus_utils.read_direct(self.perseus, 26)

    @DebugIt()
    def set_SpareDo3(self, SpareDo3):
        perseus_utils.write_direct(self.perseus, SpareDo3, 26)

    @DebugIt()
    def get_FdlSwTrigger(self):
        return perseus_utils.read_direct(self.perseus, 27)

    @DebugIt()
    def set_FdlSwTrigger(self, FdlSwTrigger):
        perseus_utils.write_direct(self.perseus, FdlSwTrigger, 27)

    @DebugIt()
    def get_ResetInterlocksCavA(self):
        return perseus_utils.read_direct(self.perseus, 100)

    @DebugIt()
    def set_ResetInterlocksCavA(self, ResetInterlocksCavA):
        perseus_utils.write_direct(self.perseus, ResetInterlocksCavA, 100)

    @DebugIt()
    def get_Landautuningenable(self):
        return perseus_utils.read_direct(self.perseus, 200)

    @DebugIt()
    def set_Landautuningenable(self, Landautuningenable):
        perseus_utils.write_direct(self.perseus, Landautuningenable, 200)

    @DebugIt()
    def get_Landautuningreset(self):
        return perseus_utils.read_direct(self.perseus, 201)

    @DebugIt()
    def set_Landautuningreset(self, Landautuningreset):
        perseus_utils.write_direct(self.perseus, Landautuningreset, 201)

    @DebugIt()
    def get_Movelandauup(self):
        return perseus_utils.read_direct(self.perseus, 202)

    @DebugIt()
    def set_Movelandauup(self, Movelandauup):
        perseus_utils.write_direct(self.perseus, Movelandauup, 202)

    @DebugIt()
    def get_Movelandauplg(self):
        return perseus_utils.read_direct(self.perseus, 203)

    @DebugIt()
    def set_Movelandauplg(self, Movelandauplg):
        perseus_utils.write_direct(self.perseus, Movelandauplg, 203)

    @DebugIt()
    def get_Numsteps(self):
        return perseus_utils.read_direct(self.perseus, 204)

    @DebugIt()
    def set_Numsteps(self, Numsteps):
        perseus_utils.write_direct(self.perseus, Numsteps, 204)

    @DebugIt()
    def get_Landauphaseoffset(self):
        return perseus_utils.read_angle(self.perseus, 205)

    @DebugIt()
    def set_Landauphaseoffset(self, Landauphaseoffset):
        perseus_utils.write_angle(self.perseus, Landauphaseoffset, 205)

    @DebugIt()
    def get_Landaumarginup(self):
        return perseus_utils.read_settings_diag_percentage(self.perseus, 206)

    @DebugIt()
    def set_Landaumarginup(self, Landaumarginup):
        perseus_utils.write_settings_diag_percentage(self.perseus, Landaumarginup, 206)

    @DebugIt()
    def get_LandauMarginLow(self):
        return perseus_utils.read_settings_diag_percentage(self.perseus, 207)

    @DebugIt()
    def set_LandauMarginLow(self, LandauMarginLow):
        perseus_utils.write_settings_diag_percentage(self.perseus, LandauMarginLow, 207)

    @DebugIt()
    def get_MinimumLandauAmplitude(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 208)

    @DebugIt()
    def set_MinimumLandauAmplitude(self, MinimumLandauAmplitude):
        perseus_utils.write_settings_diag_milivolts(self.perseus, MinimumLandauAmplitude, 208)

    @DebugIt()
    def get_LandauPositiveEnable(self):
        return perseus_utils.read_direct(self.perseus, 209)

    @DebugIt()
    def set_LandauPositiveEnable(self, LandauPositiveEnable):
        perseus_utils.write_direct(self.perseus, LandauPositiveEnable, 209)

    @DebugIt()
    def get_Landauampsetting(self):
        return perseus_utils.read_settings_diag_milivolts(self.perseus, 210)

    @DebugIt()
    def set_Landauampsetting(self, Landauampsetting):
        perseus_utils.write_settings_diag_milivolts(self.perseus, Landauampsetting, 210)

    @DebugIt()
    def get_DisitckRvtet1Dacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,7)
        self._DisitckRvtet1Dacsoffloopsstby = (value >> 0) & 1
        return self._DisitckRvtet1Dacsoffloopsstby

    @DebugIt()
    def set_DisitckRvtet1Dacsoffloopsstby(self, DisitckRvtet1Dacsoffloopsstby):
        self._DisitckRvtet1Dacsoffloopsstby = DisitckRvtet1Dacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1Pindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,7)
        self._DisitckRvtet1Pindiodeswitch = (value >> 1) & 1
        return self._DisitckRvtet1Pindiodeswitch

    @DebugIt()
    def set_DisitckRvtet1Pindiodeswitch(self, DisitckRvtet1Pindiodeswitch):
        self._DisitckRvtet1Pindiodeswitch = DisitckRvtet1Pindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1Fdltrg(self):
        value = perseus_utils.read_direct(self.perseus,7)
        self._DisitckRvtet1Fdltrg = (value >> 2) & 1
        return self._DisitckRvtet1Fdltrg

    @DebugIt()
    def set_DisitckRvtet1Fdltrg(self, DisitckRvtet1Fdltrg):
        self._DisitckRvtet1Fdltrg = DisitckRvtet1Fdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1Plctxoff(self):
        value = perseus_utils.read_direct(self.perseus,7)
        self._DisitckRvtet1Plctxoff = (value >> 3) & 1
        return self._DisitckRvtet1Plctxoff

    @DebugIt()
    def set_DisitckRvtet1Plctxoff(self, DisitckRvtet1Plctxoff):
        self._DisitckRvtet1Plctxoff = DisitckRvtet1Plctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1Mps(self):
        value = perseus_utils.read_direct(self.perseus,7)
        self._DisitckRvtet1Mps = (value >> 4) & 1
        return self._DisitckRvtet1Mps

    @DebugIt()
    def set_DisitckRvtet1Mps(self, DisitckRvtet1Mps):
        self._DisitckRvtet1Mps = DisitckRvtet1Mps
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet1Diag(self):
        value = perseus_utils.read_direct(self.perseus,7)
        self._DisitckRvtet1Diag = (value >> 5) & 1
        return self._DisitckRvtet1Diag

    @DebugIt()
    def set_DisitckRvtet1Diag(self, DisitckRvtet1Diag):
        self._DisitckRvtet1Diag = DisitckRvtet1Diag
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2Dacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,8)
        self._DisitckRvtet2Dacsoffloopsstby = (value >> 0) & 1
        return self._DisitckRvtet2Dacsoffloopsstby

    @DebugIt()
    def set_DisitckRvtet2Dacsoffloopsstby(self, DisitckRvtet2Dacsoffloopsstby):
        self._DisitckRvtet2Dacsoffloopsstby = DisitckRvtet2Dacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2Pindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,8)
        self._DisitckRvtet2Pindiodeswitch = (value >> 1) & 1
        return self._DisitckRvtet2Pindiodeswitch

    @DebugIt()
    def set_DisitckRvtet2Pindiodeswitch(self, DisitckRvtet2Pindiodeswitch):
        self._DisitckRvtet2Pindiodeswitch = DisitckRvtet2Pindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2Fdltrg(self):
        value = perseus_utils.read_direct(self.perseus,8)
        self._DisitckRvtet2Fdltrg = (value >> 2) & 1
        return self._DisitckRvtet2Fdltrg

    @DebugIt()
    def set_DisitckRvtet2Fdltrg(self, DisitckRvtet2Fdltrg):
        self._DisitckRvtet2Fdltrg = DisitckRvtet2Fdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2Plctxoff(self):
        value = perseus_utils.read_direct(self.perseus,8)
        self._DisitckRvtet2Plctxoff = (value >> 3) & 1
        return self._DisitckRvtet2Plctxoff

    @DebugIt()
    def set_DisitckRvtet2Plctxoff(self, DisitckRvtet2Plctxoff):
        self._DisitckRvtet2Plctxoff = DisitckRvtet2Plctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2Mps(self):
        value = perseus_utils.read_direct(self.perseus,8)
        self._DisitckRvtet2Mps = (value >> 4) & 1
        return self._DisitckRvtet2Mps

    @DebugIt()
    def set_DisitckRvtet2Mps(self, DisitckRvtet2Mps):
        self._DisitckRvtet2Mps = DisitckRvtet2Mps
        self.update_fim()

    @DebugIt()
    def get_DisitckRvtet2Diag(self):
        value = perseus_utils.read_direct(self.perseus,8)
        self._DisitckRvtet2Diag = (value >> 5) & 1
        return self._DisitckRvtet2Diag

    @DebugIt()
    def set_DisitckRvtet2Diag(self, DisitckRvtet2Diag):
        self._DisitckRvtet2Diag = DisitckRvtet2Diag
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircDacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,9)
        self._DisitckRvcircDacsoffloopsstby = (value >> 0) & 1
        return self._DisitckRvcircDacsoffloopsstby

    @DebugIt()
    def set_DisitckRvcircDacsoffloopsstby(self, DisitckRvcircDacsoffloopsstby):
        self._DisitckRvcircDacsoffloopsstby = DisitckRvcircDacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircPindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,9)
        self._DisitckRvcircPindiodeswitch = (value >> 1) & 1
        return self._DisitckRvcircPindiodeswitch

    @DebugIt()
    def set_DisitckRvcircPindiodeswitch(self, DisitckRvcircPindiodeswitch):
        self._DisitckRvcircPindiodeswitch = DisitckRvcircPindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircFdltrg(self):
        value = perseus_utils.read_direct(self.perseus,9)
        self._DisitckRvcircFdltrg = (value >> 2) & 1
        return self._DisitckRvcircFdltrg

    @DebugIt()
    def set_DisitckRvcircFdltrg(self, DisitckRvcircFdltrg):
        self._DisitckRvcircFdltrg = DisitckRvcircFdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircPlctxoff(self):
        value = perseus_utils.read_direct(self.perseus,9)
        self._DisitckRvcircPlctxoff = (value >> 3) & 1
        return self._DisitckRvcircPlctxoff

    @DebugIt()
    def set_DisitckRvcircPlctxoff(self, DisitckRvcircPlctxoff):
        self._DisitckRvcircPlctxoff = DisitckRvcircPlctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircMps(self):
        value = perseus_utils.read_direct(self.perseus,9)
        self._DisitckRvcircMps = (value >> 4) & 1
        return self._DisitckRvcircMps

    @DebugIt()
    def set_DisitckRvcircMps(self, DisitckRvcircMps):
        self._DisitckRvcircMps = DisitckRvcircMps
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcircDiag(self):
        value = perseus_utils.read_direct(self.perseus,9)
        self._DisitckRvcircDiag = (value >> 5) & 1
        return self._DisitckRvcircDiag

    @DebugIt()
    def set_DisitckRvcircDiag(self, DisitckRvcircDiag):
        self._DisitckRvcircDiag = DisitckRvcircDiag
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadDacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,10)
        self._DisitckFwloadDacsoffloopsstby = (value >> 0) & 1
        return self._DisitckFwloadDacsoffloopsstby

    @DebugIt()
    def set_DisitckFwloadDacsoffloopsstby(self, DisitckFwloadDacsoffloopsstby):
        self._DisitckFwloadDacsoffloopsstby = DisitckFwloadDacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadPindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,10)
        self._DisitckFwloadPindiodeswitch = (value >> 1) & 1
        return self._DisitckFwloadPindiodeswitch

    @DebugIt()
    def set_DisitckFwloadPindiodeswitch(self, DisitckFwloadPindiodeswitch):
        self._DisitckFwloadPindiodeswitch = DisitckFwloadPindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadFdltrg(self):
        value = perseus_utils.read_direct(self.perseus,10)
        self._DisitckFwloadFdltrg = (value >> 2) & 1
        return self._DisitckFwloadFdltrg

    @DebugIt()
    def set_DisitckFwloadFdltrg(self, DisitckFwloadFdltrg):
        self._DisitckFwloadFdltrg = DisitckFwloadFdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadPlctxoff(self):
        value = perseus_utils.read_direct(self.perseus,10)
        self._DisitckFwloadPlctxoff = (value >> 3) & 1
        return self._DisitckFwloadPlctxoff

    @DebugIt()
    def set_DisitckFwloadPlctxoff(self, DisitckFwloadPlctxoff):
        self._DisitckFwloadPlctxoff = DisitckFwloadPlctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadMps(self):
        value = perseus_utils.read_direct(self.perseus,10)
        self._DisitckFwloadMps = (value >> 4) & 1
        return self._DisitckFwloadMps

    @DebugIt()
    def set_DisitckFwloadMps(self, DisitckFwloadMps):
        self._DisitckFwloadMps = DisitckFwloadMps
        self.update_fim()

    @DebugIt()
    def get_DisitckFwloadDiag(self):
        value = perseus_utils.read_direct(self.perseus,10)
        self._DisitckFwloadDiag = (value >> 5) & 1
        return self._DisitckFwloadDiag

    @DebugIt()
    def set_DisitckFwloadDiag(self, DisitckFwloadDiag):
        self._DisitckFwloadDiag = DisitckFwloadDiag
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadDacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,11)
        self._DisitckFwhybloadDacsoffloopsstby = (value >> 0) & 1
        return self._DisitckFwhybloadDacsoffloopsstby

    @DebugIt()
    def set_DisitckFwhybloadDacsoffloopsstby(self, DisitckFwhybloadDacsoffloopsstby):
        self._DisitckFwhybloadDacsoffloopsstby = DisitckFwhybloadDacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadPindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,11)
        self._DisitckFwhybloadPindiodeswitch = (value >> 1) & 1
        return self._DisitckFwhybloadPindiodeswitch

    @DebugIt()
    def set_DisitckFwhybloadPindiodeswitch(self, DisitckFwhybloadPindiodeswitch):
        self._DisitckFwhybloadPindiodeswitch = DisitckFwhybloadPindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadFdltrg(self):
        value = perseus_utils.read_direct(self.perseus,11)
        self._DisitckFwhybloadFdltrg = (value >> 2) & 1
        return self._DisitckFwhybloadFdltrg

    @DebugIt()
    def set_DisitckFwhybloadFdltrg(self, DisitckFwhybloadFdltrg):
        self._DisitckFwhybloadFdltrg = DisitckFwhybloadFdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadPlctxoff(self):
        value = perseus_utils.read_direct(self.perseus,11)
        self._DisitckFwhybloadPlctxoff = (value >> 3) & 1
        return self._DisitckFwhybloadPlctxoff

    @DebugIt()
    def set_DisitckFwhybloadPlctxoff(self, DisitckFwhybloadPlctxoff):
        self._DisitckFwhybloadPlctxoff = DisitckFwhybloadPlctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadMps(self):
        value = perseus_utils.read_direct(self.perseus,11)
        self._DisitckFwhybloadMps = (value >> 4) & 1
        return self._DisitckFwhybloadMps

    @DebugIt()
    def set_DisitckFwhybloadMps(self, DisitckFwhybloadMps):
        self._DisitckFwhybloadMps = DisitckFwhybloadMps
        self.update_fim()

    @DebugIt()
    def get_DisitckFwhybloadDiag(self):
        value = perseus_utils.read_direct(self.perseus,11)
        self._DisitckFwhybloadDiag = (value >> 5) & 1
        return self._DisitckFwhybloadDiag

    @DebugIt()
    def set_DisitckFwhybloadDiag(self, DisitckFwhybloadDiag):
        self._DisitckFwhybloadDiag = DisitckFwhybloadDiag
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavDacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,12)
        self._DisitckRvcavDacsoffloopsstby = (value >> 0) & 1
        return self._DisitckRvcavDacsoffloopsstby

    @DebugIt()
    def set_DisitckRvcavDacsoffloopsstby(self, DisitckRvcavDacsoffloopsstby):
        self._DisitckRvcavDacsoffloopsstby = DisitckRvcavDacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavPindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,12)
        self._DisitckRvcavPindiodeswitch = (value >> 1) & 1
        return self._DisitckRvcavPindiodeswitch

    @DebugIt()
    def set_DisitckRvcavPindiodeswitch(self, DisitckRvcavPindiodeswitch):
        self._DisitckRvcavPindiodeswitch = DisitckRvcavPindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavFdltrg(self):
        value = perseus_utils.read_direct(self.perseus,12)
        self._DisitckRvcavFdltrg = (value >> 2) & 1
        return self._DisitckRvcavFdltrg

    @DebugIt()
    def set_DisitckRvcavFdltrg(self, DisitckRvcavFdltrg):
        self._DisitckRvcavFdltrg = DisitckRvcavFdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavPlctxoff(self):
        value = perseus_utils.read_direct(self.perseus,12)
        self._DisitckRvcavPlctxoff = (value >> 3) & 1
        return self._DisitckRvcavPlctxoff

    @DebugIt()
    def set_DisitckRvcavPlctxoff(self, DisitckRvcavPlctxoff):
        self._DisitckRvcavPlctxoff = DisitckRvcavPlctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavMps(self):
        value = perseus_utils.read_direct(self.perseus,12)
        self._DisitckRvcavMps = (value >> 4) & 1
        return self._DisitckRvcavMps

    @DebugIt()
    def set_DisitckRvcavMps(self, DisitckRvcavMps):
        self._DisitckRvcavMps = DisitckRvcavMps
        self.update_fim()

    @DebugIt()
    def get_DisitckRvcavDiag(self):
        value = perseus_utils.read_direct(self.perseus,12)
        self._DisitckRvcavDiag = (value >> 5) & 1
        return self._DisitckRvcavDiag

    @DebugIt()
    def set_DisitckRvcavDiag(self, DisitckRvcavDiag):
        self._DisitckRvcavDiag = DisitckRvcavDiag
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsDacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,13)
        self._DisitckArcsDacsoffloopsstby = (value >> 0) & 1
        return self._DisitckArcsDacsoffloopsstby

    @DebugIt()
    def set_DisitckArcsDacsoffloopsstby(self, DisitckArcsDacsoffloopsstby):
        self._DisitckArcsDacsoffloopsstby = DisitckArcsDacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsPindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,13)
        self._DisitckArcsPindiodeswitch = (value >> 1) & 1
        return self._DisitckArcsPindiodeswitch

    @DebugIt()
    def set_DisitckArcsPindiodeswitch(self, DisitckArcsPindiodeswitch):
        self._DisitckArcsPindiodeswitch = DisitckArcsPindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsFdltrg(self):
        value = perseus_utils.read_direct(self.perseus,13)
        self._DisitckArcsFdltrg = (value >> 2) & 1
        return self._DisitckArcsFdltrg

    @DebugIt()
    def set_DisitckArcsFdltrg(self, DisitckArcsFdltrg):
        self._DisitckArcsFdltrg = DisitckArcsFdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsPlctxoff(self):
        value = perseus_utils.read_direct(self.perseus,13)
        self._DisitckArcsPlctxoff = (value >> 3) & 1
        return self._DisitckArcsPlctxoff

    @DebugIt()
    def set_DisitckArcsPlctxoff(self, DisitckArcsPlctxoff):
        self._DisitckArcsPlctxoff = DisitckArcsPlctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsMps(self):
        value = perseus_utils.read_direct(self.perseus,13)
        self._DisitckArcsMps = (value >> 4) & 1
        return self._DisitckArcsMps

    @DebugIt()
    def set_DisitckArcsMps(self, DisitckArcsMps):
        self._DisitckArcsMps = DisitckArcsMps
        self.update_fim()

    @DebugIt()
    def get_DisitckArcsDiag(self):
        value = perseus_utils.read_direct(self.perseus,13)
        self._DisitckArcsDiag = (value >> 5) & 1
        return self._DisitckArcsDiag

    @DebugIt()
    def set_DisitckArcsDiag(self, DisitckArcsDiag):
        self._DisitckArcsDiag = DisitckArcsDiag
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumDacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,14)
        self._DisitckVacuumDacsoffloopsstby = (value >> 0) & 1
        return self._DisitckVacuumDacsoffloopsstby

    @DebugIt()
    def set_DisitckVacuumDacsoffloopsstby(self, DisitckVacuumDacsoffloopsstby):
        self._DisitckVacuumDacsoffloopsstby = DisitckVacuumDacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumPindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,14)
        self._DisitckVacuumPindiodeswitch = (value >> 1) & 1
        return self._DisitckVacuumPindiodeswitch

    @DebugIt()
    def set_DisitckVacuumPindiodeswitch(self, DisitckVacuumPindiodeswitch):
        self._DisitckVacuumPindiodeswitch = DisitckVacuumPindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumFdltrg(self):
        value = perseus_utils.read_direct(self.perseus,14)
        self._DisitckVacuumFdltrg = (value >> 2) & 1
        return self._DisitckVacuumFdltrg

    @DebugIt()
    def set_DisitckVacuumFdltrg(self, DisitckVacuumFdltrg):
        self._DisitckVacuumFdltrg = DisitckVacuumFdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumPlctxoff(self):
        value = perseus_utils.read_direct(self.perseus,14)
        self._DisitckVacuumPlctxoff = (value >> 3) & 1
        return self._DisitckVacuumPlctxoff

    @DebugIt()
    def set_DisitckVacuumPlctxoff(self, DisitckVacuumPlctxoff):
        self._DisitckVacuumPlctxoff = DisitckVacuumPlctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumMps(self):
        value = perseus_utils.read_direct(self.perseus,14)
        self._DisitckVacuumMps = (value >> 4) & 1
        return self._DisitckVacuumMps

    @DebugIt()
    def set_DisitckVacuumMps(self, DisitckVacuumMps):
        self._DisitckVacuumMps = DisitckVacuumMps
        self.update_fim()

    @DebugIt()
    def get_DisitckVacuumDiag(self):
        value = perseus_utils.read_direct(self.perseus,14)
        self._DisitckVacuumDiag = (value >> 5) & 1
        return self._DisitckVacuumDiag

    @DebugIt()
    def set_DisitckVacuumDiag(self, DisitckVacuumDiag):
        self._DisitckVacuumDiag = DisitckVacuumDiag
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockDacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,15)
        self._DisitckManualInterlockDacsoffloopsstby = (value >> 0) & 1
        return self._DisitckManualInterlockDacsoffloopsstby

    @DebugIt()
    def set_DisitckManualInterlockDacsoffloopsstby(self, DisitckManualInterlockDacsoffloopsstby):
        self._DisitckManualInterlockDacsoffloopsstby = DisitckManualInterlockDacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockPindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,15)
        self._DisitckManualInterlockPindiodeswitch = (value >> 1) & 1
        return self._DisitckManualInterlockPindiodeswitch

    @DebugIt()
    def set_DisitckManualInterlockPindiodeswitch(self, DisitckManualInterlockPindiodeswitch):
        self._DisitckManualInterlockPindiodeswitch = DisitckManualInterlockPindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockFdltrg(self):
        value = perseus_utils.read_direct(self.perseus,15)
        self._DisitckManualInterlockFdltrg = (value >> 2) & 1
        return self._DisitckManualInterlockFdltrg

    @DebugIt()
    def set_DisitckManualInterlockFdltrg(self, DisitckManualInterlockFdltrg):
        self._DisitckManualInterlockFdltrg = DisitckManualInterlockFdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockPlctxoff(self):
        value = perseus_utils.read_direct(self.perseus,15)
        self._DisitckManualInterlockPlctxoff = (value >> 3) & 1
        return self._DisitckManualInterlockPlctxoff

    @DebugIt()
    def set_DisitckManualInterlockPlctxoff(self, DisitckManualInterlockPlctxoff):
        self._DisitckManualInterlockPlctxoff = DisitckManualInterlockPlctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockMps(self):
        value = perseus_utils.read_direct(self.perseus,15)
        self._DisitckManualInterlockMps = (value >> 4) & 1
        return self._DisitckManualInterlockMps

    @DebugIt()
    def set_DisitckManualInterlockMps(self, DisitckManualInterlockMps):
        self._DisitckManualInterlockMps = DisitckManualInterlockMps
        self.update_fim()

    @DebugIt()
    def get_DisitckManualInterlockDiag(self):
        value = perseus_utils.read_direct(self.perseus,15)
        self._DisitckManualInterlockDiag = (value >> 5) & 1
        return self._DisitckManualInterlockDiag

    @DebugIt()
    def set_DisitckManualInterlockDiag(self, DisitckManualInterlockDiag):
        self._DisitckManualInterlockDiag = DisitckManualInterlockDiag
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpDacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,16)
        self._DisitckPlungerEndSwitchesUpDacsoffloopsstby = (value >> 0) & 1
        return self._DisitckPlungerEndSwitchesUpDacsoffloopsstby

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpDacsoffloopsstby(self, DisitckPlungerEndSwitchesUpDacsoffloopsstby):
        self._DisitckPlungerEndSwitchesUpDacsoffloopsstby = DisitckPlungerEndSwitchesUpDacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpPindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,16)
        self._DisitckPlungerEndSwitchesUpPindiodeswitch = (value >> 1) & 1
        return self._DisitckPlungerEndSwitchesUpPindiodeswitch

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpPindiodeswitch(self, DisitckPlungerEndSwitchesUpPindiodeswitch):
        self._DisitckPlungerEndSwitchesUpPindiodeswitch = DisitckPlungerEndSwitchesUpPindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpFdltrg(self):
        value = perseus_utils.read_direct(self.perseus,16)
        self._DisitckPlungerEndSwitchesUpFdltrg = (value >> 2) & 1
        return self._DisitckPlungerEndSwitchesUpFdltrg

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpFdltrg(self, DisitckPlungerEndSwitchesUpFdltrg):
        self._DisitckPlungerEndSwitchesUpFdltrg = DisitckPlungerEndSwitchesUpFdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpPlctxoff(self):
        value = perseus_utils.read_direct(self.perseus,16)
        self._DisitckPlungerEndSwitchesUpPlctxoff = (value >> 3) & 1
        return self._DisitckPlungerEndSwitchesUpPlctxoff

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpPlctxoff(self, DisitckPlungerEndSwitchesUpPlctxoff):
        self._DisitckPlungerEndSwitchesUpPlctxoff = DisitckPlungerEndSwitchesUpPlctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpMps(self):
        value = perseus_utils.read_direct(self.perseus,16)
        self._DisitckPlungerEndSwitchesUpMps = (value >> 4) & 1
        return self._DisitckPlungerEndSwitchesUpMps

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpMps(self, DisitckPlungerEndSwitchesUpMps):
        self._DisitckPlungerEndSwitchesUpMps = DisitckPlungerEndSwitchesUpMps
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesUpDiag(self):
        value = perseus_utils.read_direct(self.perseus,16)
        self._DisitckPlungerEndSwitchesUpDiag = (value >> 5) & 1
        return self._DisitckPlungerEndSwitchesUpDiag

    @DebugIt()
    def set_DisitckPlungerEndSwitchesUpDiag(self, DisitckPlungerEndSwitchesUpDiag):
        self._DisitckPlungerEndSwitchesUpDiag = DisitckPlungerEndSwitchesUpDiag
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownDacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,17)
        self._DisitckPlungerEndSwitchesDownDacsoffloopsstby = (value >> 0) & 1
        return self._DisitckPlungerEndSwitchesDownDacsoffloopsstby

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownDacsoffloopsstby(self, DisitckPlungerEndSwitchesDownDacsoffloopsstby):
        self._DisitckPlungerEndSwitchesDownDacsoffloopsstby = DisitckPlungerEndSwitchesDownDacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownPindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,17)
        self._DisitckPlungerEndSwitchesDownPindiodeswitch = (value >> 1) & 1
        return self._DisitckPlungerEndSwitchesDownPindiodeswitch

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownPindiodeswitch(self, DisitckPlungerEndSwitchesDownPindiodeswitch):
        self._DisitckPlungerEndSwitchesDownPindiodeswitch = DisitckPlungerEndSwitchesDownPindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownFdltrg(self):
        value = perseus_utils.read_direct(self.perseus,17)
        self._DisitckPlungerEndSwitchesDownFdltrg = (value >> 2) & 1
        return self._DisitckPlungerEndSwitchesDownFdltrg

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownFdltrg(self, DisitckPlungerEndSwitchesDownFdltrg):
        self._DisitckPlungerEndSwitchesDownFdltrg = DisitckPlungerEndSwitchesDownFdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownPlctxoff(self):
        value = perseus_utils.read_direct(self.perseus,17)
        self._DisitckPlungerEndSwitchesDownPlctxoff = (value >> 3) & 1
        return self._DisitckPlungerEndSwitchesDownPlctxoff

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownPlctxoff(self, DisitckPlungerEndSwitchesDownPlctxoff):
        self._DisitckPlungerEndSwitchesDownPlctxoff = DisitckPlungerEndSwitchesDownPlctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownMps(self):
        value = perseus_utils.read_direct(self.perseus,17)
        self._DisitckPlungerEndSwitchesDownMps = (value >> 4) & 1
        return self._DisitckPlungerEndSwitchesDownMps

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownMps(self, DisitckPlungerEndSwitchesDownMps):
        self._DisitckPlungerEndSwitchesDownMps = DisitckPlungerEndSwitchesDownMps
        self.update_fim()

    @DebugIt()
    def get_DisitckPlungerEndSwitchesDownDiag(self):
        value = perseus_utils.read_direct(self.perseus,17)
        self._DisitckPlungerEndSwitchesDownDiag = (value >> 5) & 1
        return self._DisitckPlungerEndSwitchesDownDiag

    @DebugIt()
    def set_DisitckPlungerEndSwitchesDownDiag(self, DisitckPlungerEndSwitchesDownDiag):
        self._DisitckPlungerEndSwitchesDownDiag = DisitckPlungerEndSwitchesDownDiag
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsDacsoffloopsstby(self):
        value = perseus_utils.read_direct(self.perseus,18)
        self._DisitckMpsDacsoffloopsstby = (value >> 0) & 1
        return self._DisitckMpsDacsoffloopsstby

    @DebugIt()
    def set_DisitckMpsDacsoffloopsstby(self, DisitckMpsDacsoffloopsstby):
        self._DisitckMpsDacsoffloopsstby = DisitckMpsDacsoffloopsstby
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsPindiodeswitch(self):
        value = perseus_utils.read_direct(self.perseus,18)
        self._DisitckMpsPindiodeswitch = (value >> 1) & 1
        return self._DisitckMpsPindiodeswitch

    @DebugIt()
    def set_DisitckMpsPindiodeswitch(self, DisitckMpsPindiodeswitch):
        self._DisitckMpsPindiodeswitch = DisitckMpsPindiodeswitch
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsFdltrg(self):
        value = perseus_utils.read_direct(self.perseus,18)
        self._DisitckMpsFdltrg = (value >> 2) & 1
        return self._DisitckMpsFdltrg

    @DebugIt()
    def set_DisitckMpsFdltrg(self, DisitckMpsFdltrg):
        self._DisitckMpsFdltrg = DisitckMpsFdltrg
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsPlctxoff(self):
        value = perseus_utils.read_direct(self.perseus,18)
        self._DisitckMpsPlctxoff = (value >> 3) & 1
        return self._DisitckMpsPlctxoff

    @DebugIt()
    def set_DisitckMpsPlctxoff(self, DisitckMpsPlctxoff):
        self._DisitckMpsPlctxoff = DisitckMpsPlctxoff
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsMps(self):
        value = perseus_utils.read_direct(self.perseus,18)
        self._DisitckMpsMps = (value >> 4) & 1
        return self._DisitckMpsMps

    @DebugIt()
    def set_DisitckMpsMps(self, DisitckMpsMps):
        self._DisitckMpsMps = DisitckMpsMps
        self.update_fim()

    @DebugIt()
    def get_DisitckMpsDiag(self):
        value = perseus_utils.read_direct(self.perseus,18)
        self._DisitckMpsDiag = (value >> 5) & 1
        return self._DisitckMpsDiag

    @DebugIt()
    def set_DisitckMpsDiag(self, DisitckMpsDiag):
        self._DisitckMpsDiag = DisitckMpsDiag
        self.update_fim()

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
    def read_Diag_Qlandau(self):
        return self._Diag_Qlandau

    @DebugIt()
    def read_Diag_Amplandau(self):
        return self._Diag_Amplandau

    @DebugIt()
    def read_Diag_Phlandau(self):
        return self._Diag_Phlandau

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
        address = 100
        position = 0
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


    @DebugIt()
    def read_Diag_Rvtet2(self):
        address = 100
        position = 1
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


    @DebugIt()
    def read_Diag_Rvcirc(self):
        address = 100
        position = 2
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


    @DebugIt()
    def read_Diag_Fwload(self):
        address = 100
        position = 3
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


    @DebugIt()
    def read_Diag_Fwhybload(self):
        address = 100
        position = 4
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


    @DebugIt()
    def read_Diag_Rvcav(self):
        address = 100
        position = 5
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


    @DebugIt()
    def read_Diag_Arcs(self):
        address = 100
        position = 6
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


    @DebugIt()
    def read_Diag_Vacuum(self):
        address = 100
        position = 7
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


    @DebugIt()
    def read_Diag_ManualInterlock(self):
        address = 100
        position = 8
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


    @DebugIt()
    def read_Diag_ExternalItck(self):
        address = 100
        position = 9
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


    @DebugIt()
    def read_Diag_PlungerEndSwitchUp(self):
        address = 100
        position = 10
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


    @DebugIt()
    def read_Diag_PlungerEndSwitchDown(self):
        address = 100
        position = 11
        if self._itck_number == 0:
            address = 150
        else:
            address = address + self._itck_number
        return extra_func.read_diag_bit_direct(self.perseus, address, position)


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
        address = 152
        return extra_func.read_diag_bit_direct(self.perseus, address, 0)


    @DebugIt()
    def read_Diag_PinSwitch(self):
        address = 152
        return extra_func.read_diag_bit_direct(self.perseus, address, 1)


    @DebugIt()
    def read_Diag_FdlTriggerToLoopsdiagboard(self):
        address = 152
        return extra_func.read_diag_bit_direct(self.perseus, address, 2)


    @DebugIt()
    def read_Diag_OutputToPlc(self):
        address = 152
        return extra_func.read_diag_bit_direct(self.perseus, address, 3)


    @DebugIt()
    def read_Diag_OutputToMps(self):
        address = 152
        return extra_func.read_diag_bit_direct(self.perseus, address, 4)


    @DebugIt()
    def read_Diag_AmpRvtet2(self):
        return self._Diag_AmpRvtet2

    @DebugIt()
    def read_Diag_AmpRvtet1(self):
        return self._Diag_AmpRvtet1

    @DebugIt()
    def read_Diag_AmpRvcav(self):
        return self._Diag_AmpRvcav

    @DebugIt()
    def read_Diag_AmpLandau(self):
        return self._Diag_AmpLandau

    @DebugIt()
    def read_Diag_AmpRvcirc(self):
        return self._Diag_AmpRvcirc

    @DebugIt()
    def read_Diag_AmpFwhybload(self):
        return self._Diag_AmpFwhybload

    @DebugIt()
    def read_Diag_AmpFwcirc(self):
        return self._Diag_AmpFwcirc

    @DebugIt()
    def read_Diag_AmpFwload(self):
        return self._Diag_AmpFwload

    @DebugIt()
    def read_Diag_AmpMo(self):
        return self._Diag_AmpMo

    @DebugIt()
    def read_Diag_PhRvtet2(self):
        return self._Diag_PhRvtet2

    @DebugIt()
    def read_Diag_PhRvtet1(self):
        return self._Diag_PhRvtet1

    @DebugIt()
    def read_Diag_PhRvcav(self):
        return self._Diag_PhRvcav

    @DebugIt()
    def read_Diag_PhLandau(self):
        return self._Diag_PhLandau

    @DebugIt()
    def read_Diag_PhRvcirc(self):
        return self._Diag_PhRvcirc

    @DebugIt()
    def read_Diag_PhFwhybload(self):
        return self._Diag_PhFwhybload

    @DebugIt()
    def read_Diag_PhFwcirc(self):
        return self._Diag_PhFwcirc

    @DebugIt()
    def read_Diag_PhFwload(self):
        return self._Diag_PhFwload

    @DebugIt()
    def read_Diag_PhMo(self):
        return self._Diag_PhMo

    @command
    def read_diagnostics(self):
        perseus_utils.start_reading_diagnostics(self.perseus)

        self._Diag_Irvtet1 = perseus_utils.read_diag_milivolts(self.perseus, 0)
        self._Diag_Qrvtet1 = perseus_utils.read_diag_milivolts(self.perseus, 1)
        self._Diag_Amprvtet1 = perseus_utils.read_diag_milivolts(self.perseus, 2)
        self._Diag_Phrvtet1 = perseus_utils.read_diag_angle(self.perseus, 3)
        self._Diag_Irvtet2 = perseus_utils.read_diag_milivolts(self.perseus, 4)
        self._Diag_Qrvtet2 = perseus_utils.read_diag_milivolts(self.perseus, 5)
        self._Diag_Amprvtet2 = perseus_utils.read_diag_milivolts(self.perseus, 6)
        self._Diag_Phrvtet2 = perseus_utils.read_diag_angle(self.perseus, 7)
        self._Diag_Ifwcirc = perseus_utils.read_diag_milivolts(self.perseus, 8)
        self._Diag_Qfwcirc = perseus_utils.read_diag_milivolts(self.perseus, 9)
        self._Diag_Ampfwcirc = perseus_utils.read_diag_milivolts(self.perseus, 10)
        self._Diag_Phfwcirc = perseus_utils.read_diag_angle(self.perseus, 11)
        self._Diag_Irvcirc = perseus_utils.read_diag_milivolts(self.perseus, 12)
        self._Diag_Qrvcirc = perseus_utils.read_diag_milivolts(self.perseus, 13)
        self._Diag_Amprvcirc = perseus_utils.read_diag_milivolts(self.perseus, 14)
        self._Diag_Phrvcirc = perseus_utils.read_diag_angle(self.perseus, 15)
        self._Diag_Ifwload = perseus_utils.read_diag_milivolts(self.perseus, 16)
        self._Diag_Qfwload = perseus_utils.read_diag_milivolts(self.perseus, 17)
        self._Diag_Ampfwload = perseus_utils.read_diag_milivolts(self.perseus, 18)
        self._Diag_Phfwload = perseus_utils.read_diag_angle(self.perseus, 19)
        self._Diag_Ifwhybload = perseus_utils.read_diag_milivolts(self.perseus, 20)
        self._Diag_Qfwhybload = perseus_utils.read_diag_milivolts(self.perseus, 21)
        self._Diag_Ampfwhybload = perseus_utils.read_diag_milivolts(self.perseus, 22)
        self._Diag_Phfwhybload = perseus_utils.read_diag_angle(self.perseus, 23)
        self._Diag_Irvcav = perseus_utils.read_diag_milivolts(self.perseus, 24)
        self._Diag_Qrvcav = perseus_utils.read_diag_milivolts(self.perseus, 25)
        self._Diag_Amprvcav = perseus_utils.read_diag_milivolts(self.perseus, 26)
        self._Diag_Phrvcav = perseus_utils.read_diag_angle(self.perseus, 27)
        self._Diag_Imo = perseus_utils.read_diag_milivolts(self.perseus, 28)
        self._Diag_Qmo = perseus_utils.read_diag_milivolts(self.perseus, 29)
        self._Diag_Ampmo = perseus_utils.read_diag_milivolts(self.perseus, 30)
        self._Diag_Phmo = perseus_utils.read_diag_angle(self.perseus, 31)
        self._Diag_Ilandau = perseus_utils.read_diag_milivolts(self.perseus, 32)
        self._Diag_Qlandau = perseus_utils.read_diag_milivolts(self.perseus, 33)
        self._Diag_Amplandau = perseus_utils.read_diag_milivolts(self.perseus, 34)
        self._Diag_Phlandau = perseus_utils.read_diag_angle(self.perseus, 35)
        self._Diag_PlungerMovingManualTuning = bool(perseus_utils.read_diag_direct(self.perseus, 60))
        self._Diag_PlungerMovingUpManualTuning = bool(perseus_utils.read_diag_direct(self.perseus, 61))
        self._Diag_PlungerMovingAutomaticTuning = bool(perseus_utils.read_diag_direct(self.perseus, 62))
        self._Diag_PlungerMovingUpAutomaticTuning = bool(perseus_utils.read_diag_direct(self.perseus, 63))
        self._Diag_DephaseMoLandau = perseus_utils.read_diag_angle(self.perseus, 64)
        self._Diag_AmpRvtet2 = math.sqrt((self._Diag_Irvtet2**2) + (self._Diag_Qrvtet2**2))
        self._Diag_AmpRvtet1 = math.sqrt((self._Diag_Irvtet1**2) + (self._Diag_Qrvtet1**2))
        self._Diag_AmpRvcav = math.sqrt((self._Diag_Irvcav**2) + (self._Diag_Qrvcav**2))
        self._Diag_AmpLandau = math.sqrt((self._Diag_Ilandau**2) + (self._Diag_Qlandau**2))
        self._Diag_AmpRvcirc = math.sqrt((self._Diag_Irvcirc**2) + (self._Diag_Qrvcirc**2))
        self._Diag_AmpFwhybload = math.sqrt((self._Diag_Ifwhybload**2) + (self._Diag_Qfwhybload**2))
        self._Diag_AmpFwcirc = math.sqrt((self._Diag_Ifwcirc**2) + (self._Diag_Qfwcirc**2))
        self._Diag_AmpFwload = math.sqrt((self._Diag_Ifwload**2) + (self._Diag_Qfwload**2))
        self._Diag_AmpMo = math.sqrt((self._Diag_Imo**2) + (self._Diag_Qmo**2))
        self._Diag_PhRvtet2 = math.degrees(math.atan2(self._Diag_Qrvtet2, self._Diag_Irvtet2))
        self._Diag_PhRvtet1 = math.degrees(math.atan2(self._Diag_Qrvtet1, self._Diag_Irvtet1))
        self._Diag_PhRvcav = math.degrees(math.atan2(self._Diag_Qrvcav, self._Diag_Irvcav))
        self._Diag_PhLandau = math.degrees(math.atan2(self._Diag_Qlandau, self._Diag_Ilandau))
        self._Diag_PhRvcirc = math.degrees(math.atan2(self._Diag_Qrvcirc, self._Diag_Irvcirc))
        self._Diag_PhFwhybload = math.degrees(math.atan2(self._Diag_Qfwhybload, self._Diag_Ifwhybload))
        self._Diag_PhFwcirc = math.degrees(math.atan2(self._Diag_Qfwcirc, self._Diag_Ifwcirc))
        self._Diag_PhFwload = math.degrees(math.atan2(self._Diag_Qfwload, self._Diag_Ifwload))
        self._Diag_PhMo = math.degrees(math.atan2(self._Diag_Qmo, self._Diag_Imo))

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
