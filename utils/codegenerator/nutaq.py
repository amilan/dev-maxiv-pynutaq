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


class Nutaq(Device):
    __metaclass__ = DeviceMeta

    phase_shift_fw = attribute(label=PhaseShiftFwCav,
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit=degrees, format=6.4f,
                                   min_value=-180.0, max_value=360.0,
                                   fget="get_phase_shift_fw_cav",
                                   fset="set_phase_shift_fw_cav",
                                   doc=
                                   )

    loop_enable = attribute(label=PhaseShiftFwCav,
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit=degrees, format=6.4f,
                                   min_value=-180.0, max_value=360.0,
                                   fget="get_phase_shift_fw_cav",
                                   fset="set_phase_shift_fw_cav",
                                   doc=
                                   )

    phase_shift_fw_cav = attribute(label=PhaseShiftFwCav,
                                   dtype=float,
                                   display_level=DispLevel.OPERATOR,
                                   access=AttrWriteType.READ_WRITE,
                                   unit=degrees, format=6.4f,
                                   min_value=-180.0, max_value=360.0,
                                   fget="get_phase_shift_fw_cav",
                                   fset="set_phase_shift_fw_cav",
                                   doc=
                                   )

    @DebugIt()
    def get_phase_shift_fw_cav(self):
        return self.read_angle(2)

    @DebugIt()
    def set_phase_shift_cav(self, phase_shift_fw):
        self.write_angle(phase_shift_fw, 2)

    @DebugIt()
    def get_loop_enable(self):
        return self.read_direct(3)

    @DebugIt()
    def set_loop_enable(self, loop_enable):
        self.write_direct(loop_enable, 3)

    @DebugIt()
    def get_phase_shift_fw_cav(self):
        return self.read_milivolts(1)

    @DebugIt()
    def set_phase_shift_cav(self, phase_shift_fw_cav):
        self.write_milivolts(phase_shift_fw_cav, 1)

