#!/usr/bin/env python

###############################################################################
##     Perseus module to handle the loops boards.
##
##     Copyright (C) 2013  Max IV Laboratory, Lund Sweden
##
##     This program is free software: you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation, either version 3 of the License, or
##     (at your option) any later version.
##
##     This program is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.
##
##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see [http://www.gnu.org/licenses/].
###############################################################################

__author__ = 'antmil'

import eapi
from perseusdefs import *
from boards.mo1000 import Mo1000
from boards.mi125 import Mi125
from adp_exception import *
from perseusdecorators import ensure_read_method, ensure_write_method, ensure_connect_method

MO1000_BOARD_NUMBER = 1
MI125_BOARD_NUMBER = 2
MI125_CLK_SRC = "bottomfmc"

class PerseusLoops(object):

    def __init__(self):
            eapi.eapi_init()
            self._board_state = eapi.connection_state()
            self.connect()

            self.custom_write(4, 1)

            print "MO1000 1 initialization..."
            self.mo1000 = Mo1000(self._board_state, MO1000_BOARD_NUMBER)

            print "Mi125 2 initialization..."
            self.mi125 = Mi125(self._board_state, MI125_BOARD_NUMBER, MI125_CLK_SRC)
            print "DONE"

            self.mo1000.enable_dac_outputs()

            print "Remove reset MI125 - MO1000 intercore fifo"
            self.custom_write(4, 0)
            print "DONE"

            self.mo1000.display_dac_error()

            self.configure_gpio_inputs_outputs()

            self.configure_vcxo()

            self.configure_loops_registers()

            print "Init DONE"

    @ensure_connect_method
    def connect(self):
        return eapi.connect_cce(PERSEUS_LOOP_IP, self._board_state)

    @ensure_write_method
    def custom_write(self, register, data):
        """
           @todo: this method should be merge with self.write when it will be supported in all platforms.
        """
        return eapi.custom_register_write_send(self._board_state, register, data)

    @ensure_write_method
    def write(self, address, value):
        return eapi.memory_write_send(self._board_state, address, value)

    @ensure_read_method
    def read(self, address):
        return eapi.memory_read_send(self._board_state, address)

    def configure_gpio_inputs_outputs(self):
        print "configuring GPIO inputs/outputs"
        register = 13
        values = [0x1, 0x0, 0x1ffff, 0x20000, 0x30000, 0x30001, 0x40001, 0x40000]
        for value in values:
            self.custom_write(register, value)

    def configure_vcxo(self):
        print "configuring VCXO"
        register = 10
        values = [0x3e80009, 0x3eA0007, 0x3eC0000, 0x3eE0000, 0x3f00000,
                  0x3f20000, 0x3f40000, 0x3f60000, 0x3FA0001, 0x3F80000, 0x3F80001]
        for value in values:
            self.custom_write(register, value)

    def configure_loops_registers(self):
        print "configuring Loops Board registers"
        values = [0x00000000, 0x00020001, 0x00040000, 0x00060000, 0x00080000, 0x000A0000,
                  0x000C3FFF, 0x000E0000, 0x00100000, 0x00120000, 0x00140000, 0x00160000,
                  0x00180000, 0x001A4DBA, 0x001C4DBA, 0x001E0000, 0x00200005, 0x00220000,
                  0x00240000, 0x002607C6, 0x00282000, 0x002A07C6, 0x002C0E39, 0x002E0007,
                  0x0032003F, 0x00340000, 0x00360000, 0x00380000, 0x003A0000, 0x003C0000,
                  0x003E0000, 0x00DC0006, 0x03200001, 0x00C80000, 0x00CA0000, 0x025E0003,
                  0x025A0001, 0x026A0222, 0x026C00B6, 0x03220001]

        for i, value in enumerate(values):
            self.write(SETTINGS_WRITE_OFFSET, value)
