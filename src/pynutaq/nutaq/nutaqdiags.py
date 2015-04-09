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

__all__ = ["NutaqDiags", "run"]

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

    Diag_LandayMovingUpLed = attribute(label='Diag_LandayMovingUpLed',
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
    FDLPath = device_property(dtype=str, default_value='/tmp')

    def init_device(self):
        Device.init_device(self)
        try:
            self.perseus = Perseus().new_perseus(self.perseusType)
            self.set_state(DevState.ON)
        except Exception, e:
            print e
            self.set_state(DevState.FAULT)


    @DebugIt()
    def get_Rvtet1(self):
        return perseus_utils.read_milivolts(self.perseus, 0)

    @DebugIt()
    def set_Rvtet1(self, Rvtet1):
        perseus_utils.write_milivolts(self.perseus, Rvtet1, 0)

    @DebugIt()
    def get_Rvtet2(self):
        return perseus_utils.read_milivolts(self.perseus, 1)

    @DebugIt()
    def set_Rvtet2(self, Rvtet2):
        perseus_utils.write_milivolts(self.perseus, Rvtet2, 1)

    @DebugIt()
    def get_Rvcirc(self):
        return perseus_utils.read_milivolts(self.perseus, 2)

    @DebugIt()
    def set_Rvcirc(self, Rvcirc):
        perseus_utils.write_milivolts(self.perseus, Rvcirc, 2)

    @DebugIt()
    def get_Fwload(self):
        return perseus_utils.read_milivolts(self.perseus, 3)

    @DebugIt()
    def set_Fwload(self, Fwload):
        perseus_utils.write_milivolts(self.perseus, Fwload, 3)

    @DebugIt()
    def get_Fwhybload(self):
        return perseus_utils.read_milivolts(self.perseus, 4)

    @DebugIt()
    def set_Fwhybload(self, Fwhybload):
        perseus_utils.write_milivolts(self.perseus, Fwhybload, 4)

    @DebugIt()
    def get_Rvcav(self):
        return perseus_utils.read_milivolts(self.perseus, 5)

    @DebugIt()
    def set_Rvcav(self, Rvcav):
        perseus_utils.write_milivolts(self.perseus, Rvcav, 5)

    @DebugIt()
    def get_ManualInterlock(self):
        return perseus_utils.read_direct(self.perseus, 6)

    @DebugIt()
    def set_ManualInterlock(self, ManualInterlock):
        perseus_utils.write_direct(self.perseus, ManualInterlock, 6)

    @DebugIt()
    def get_DisableItckRvtet1(self):
        address = 7
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckRvtet1(self.perseus, address)

    @DebugIt()
    def set_DisableItckRvtet1(self, DisableItckRvtet1):
        address = 7
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckRvtet1(self.perseus, DisableItckRvtet1, address)

    @DebugIt()
    def get_DisableItckRvtet2(self):
        address = 8
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckRvtet2(self.perseus, address)

    @DebugIt()
    def set_DisableItckRvtet2(self, DisableItckRvtet2):
        address = 8
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckRvtet2(self.perseus, DisableItckRvtet2, address)

    @DebugIt()
    def get_DisableItckRvcirc(self):
        address = 9
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckRvcirc(self.perseus, address)

    @DebugIt()
    def set_DisableItckRvcirc(self, DisableItckRvcirc):
        address = 9
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckRvcirc(self.perseus, DisableItckRvcirc, address)

    @DebugIt()
    def get_DisableItckFwload(self):
        address = 10
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckFwload(self.perseus, address)

    @DebugIt()
    def set_DisableItckFwload(self, DisableItckFwload):
        address = 10
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckFwload(self.perseus, DisableItckFwload, address)

    @DebugIt()
    def get_DisableItckFwhybload(self):
        address = 11
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckFwhybload(self.perseus, address)

    @DebugIt()
    def set_DisableItckFwhybload(self, DisableItckFwhybload):
        address = 11
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckFwhybload(self.perseus, DisableItckFwhybload, address)

    @DebugIt()
    def get_DisableItckRvcav(self):
        address = 12
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckRvcav(self.perseus, address)

    @DebugIt()
    def set_DisableItckRvcav(self, DisableItckRvcav):
        address = 12
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckRvcav(self.perseus, DisableItckRvcav, address)

    @DebugIt()
    def get_DisableItckArcs(self):
        address = 13
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckArcs(self.perseus, address)

    @DebugIt()
    def set_DisableItckArcs(self, DisableItckArcs):
        address = 13
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckArcs(self.perseus, DisableItckArcs, address)

    @DebugIt()
    def get_DisableItckVaccum(self):
        address = 14
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckVaccum(self.perseus, address)

    @DebugIt()
    def set_DisableItckVaccum(self, DisableItckVaccum):
        address = 14
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckVaccum(self.perseus, DisableItckVaccum, address)

    @DebugIt()
    def get_DisableItckManualInterlock(self):
        address = 15
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckManualInterlock(self.perseus, address)

    @DebugIt()
    def set_DisableItckManualInterlock(self, DisableItckManualInterlock):
        address = 15
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckManualInterlock(self.perseus, DisableItckManualInterlock, address)

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesUp(self):
        address = 16
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckPlungerEndSwitchesUp(self.perseus, address)

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesUp(self, DisableItckPlungerEndSwitchesUp):
        address = 16
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckPlungerEndSwitchesUp(self.perseus, DisableItckPlungerEndSwitchesUp, address)

    @DebugIt()
    def get_DisableItckPlungerEndSwitchesDown(self):
        address = 17
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckPlungerEndSwitchesDown(self.perseus, address)

    @DebugIt()
    def set_DisableItckPlungerEndSwitchesDown(self, DisableItckPlungerEndSwitchesDown):
        address = 17
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckPlungerEndSwitchesDown(self.perseus, DisableItckPlungerEndSwitchesDown, address)

    @DebugIt()
    def get_DisableItckMps(self):
        address = 18
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckMps(self.perseus, address)

    @DebugIt()
    def set_DisableItckMps(self, DisableItckMps):
        address = 18
        #@todo: add this method to special methods library ...
        extra_func.get_DisableItckMps(self.perseus, DisableItckMps, address)

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
        return perseus_utils.read_milivolts(self.perseus, 204)

    @DebugIt()
    def set_Numsteps(self, Numsteps):
        perseus_utils.write_milivolts(self.perseus, Numsteps, 204)

    @DebugIt()
    def get_Landauphaseoffset(self):
        return perseus_utils.read_angle(self.perseus, 205)

    @DebugIt()
    def set_Landauphaseoffset(self, Landauphaseoffset):
        perseus_utils.write_angle(self.perseus, Landauphaseoffset, 205)

    @DebugIt()
    def get_Landaumarginup(self):
        return perseus_utils.read_milivolts(self.perseus, 206)

    @DebugIt()
    def set_Landaumarginup(self, Landaumarginup):
        perseus_utils.write_milivolts(self.perseus, Landaumarginup, 206)

    @DebugIt()
    def get_LandauMarginLow(self):
        return perseus_utils.read_milivolts(self.perseus, 207)

    @DebugIt()
    def set_LandauMarginLow(self, LandauMarginLow):
        perseus_utils.write_milivolts(self.perseus, LandauMarginLow, 207)

    @DebugIt()
    def get_MinimumLandauAmplitude(self):
        return perseus_utils.read_milivolts(self.perseus, 208)

    @DebugIt()
    def set_MinimumLandauAmplitude(self, MinimumLandauAmplitude):
        perseus_utils.write_milivolts(self.perseus, MinimumLandauAmplitude, 208)

    @DebugIt()
    def get_LandauPositiveEnable(self):
        return perseus_utils.read_direct(self.perseus, 209)

    @DebugIt()
    def set_LandauPositiveEnable(self, LandauPositiveEnable):
        perseus_utils.write_direct(self.perseus, LandauPositiveEnable, 209)

    @DebugIt()
    def get_Landauampsetting(self):
        return perseus_utils.read_milivolts(self.perseus, 210)

    @DebugIt()
    def set_Landauampsetting(self, Landauampsetting):
        perseus_utils.write_milivolts(self.perseus, Landauampsetting, 210)

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
    def read_Diag_LandayMovingUpLed(self):
        return self._Diag_LandayMovingUpLed

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
        self._Diag_Qlandadu = perseus_utils.read_diag_milivolts(self.perseus, 33)
        self._Diag_Amplandadu = perseus_utils.read_diag_milivolts(self.perseus, 34)
        self._Diag_Phlandadu = perseus_utils.read_diag_angle(self.perseus, 35)
        self._Diag_DephaseMoLandau = perseus_utils.read_diag_angle(self.perseus, 64)

    @command
    def tuning_reset(self):
        perseus_utils.write_direct(True, TUNING_RESET_ADDRESS)
        perseus_utils.write_direct(False, TUNING_RESET_ADDRESS)

    @command
    def sw_fast_data_logger(self):
        # Ram init ... probably this should be done in init_device
        # but for the moment ...
        self.perseus.init_fast_data_logger()

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


def run_device():
    run([NutaqDiags])

if __name__ == "__main__":
    run_device()
