#!/usr/bin/env python

###############################################################################
#     Perseus module to handle the loops boards.
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

"""This module contains the main class for the perseus loops.
"""

__all__ = ["PerseusLoops"]

__author__ = 'antmil'

__docformat__ = 'restructuredtext'

try:
    import eapi
    from adp_exception import *
except ImportError, e:
    print e
    #raise

from pynutaq.perseus.perseusdefs import *
from pynutaq.boards.mo1000 import Mo1000
from pynutaq.boards.mi125 import Mi125
from pynutaq.perseus.perseusdecorators import ensure_read_method, ensure_write_method, ensure_connect_method

MO1000_BOARD_NUMBER = 1
MI125_BOARD_NUMBER = 2
MI125_CLK_SRC = "bottomfmc"

class PerseusLoops(object):

    def __init__(self, perseus_ip=PERSEUS_LOOP_IP):
        self.perseus_ip = perseus_ip

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
        return eapi.connect_cce(self.perseus_ip, self._board_state)

    @ensure_read_method
    def custom_read(self, register):
        return eapi.custom_register_read_send(self._board_state, register)

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
        values = [0x3e80009, 0x3eA0001, 0x3eC0001, 0x3eE0000, 0x3f00002,
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
            self.write(SETTINGS_WRITE_OFFSET_A, value)

    @ensure_write_method
    def init_fast_data_logger(self):
        """Initialize ram"""
        return eapi.ram_init(self._board_state)

    def write_fast_data_logger_delay(self):
        # set 10ms delay to continue recording data after a trigger
        self.write(RAM_INIT_OFFSET, RAM_INIT_VALUE)

    @ensure_write_method
    def start_recording_data_in_ram(self, size=65536, triggersource=0):
        """Start recording data in RAM"""
        return eapi.recplay_record(self._board_state, size, triggersource)

    # @ensure_read_method
    def get_ram_data(self, filename, channel=0, bufsize=65536, framesize=1024, framegap=200):
        if channel < 0 or channel > 7:
            print 'ERROR: channel must be in range [0,7]!'
            raise ValueError
        if framesize < 4 or framesize > 4294967295:
            print 'ERROR: frame size (32 bits) must be greater than 4 bytes!'
            raise ValueError
        if (bufsize <= 0) or (int(bufsize / 64) * 64) != bufsize or (bufsize > 4294967295):
            print 'ERROR: transfer size (32 bits) must be a positive multiple of 64 bytes!'
            raise ValueError
        if (int(bufsize / framesize) * framesize) != bufsize:
            print 'ERROR: transfer size must be a multiple of frame size!'
            raise ValueError
        if framegap < 0 or framegap > 4294967295:
            print 'ERROR: frame gap must be a positive value and fit on 32 bits!'
            raise ValueError

        # try:
        #     useoffset = 0
        #     startaddr = int(args[5], 0)
        # except IndexError:
        #     try:
        #        startaddr = self.trigaddr
        #        useoffset = self.trigoffset
        #        print 'INFO: using last recorded memory address: ', startaddr
        #        print '      using last recorded bytes offset: ', useoffset
        #     except AttributeError:
        #        startaddr = 0
        #        useoffset = 0
        #        print 'INFO: using default memory address: ', startaddr
        # if (startaddr < 0) or (int(startaddr / 8) * 8) != startaddr or (startaddr > 4294967295):
        #     print 'ERROR: memory address (32 bits) must be a positive multiple of 8 bytes!'
        #     raise ValueError
        # if useoffset != 0:
        #     addbytes = framesize / self.gcd(64,framesize) * 64
        #     if (4294967295 < addbytes):
        #         print 'ERROR: additionnal transfer size bytes to offset does not fit on 32 bits: ', addbytes
        #         raise ValueError
        #     if (4294967295 - addbytes) < bufsize:
        #         print 'ERROR: transfer size + offset needed does not fit on 32 bits. Max size: ', (4294967295 - addbytes)
        #         raise ValueError
        #     neededsize = bufsize + addbytes
        # else:
        #     neededsize = bufsize

        # Assuming default values for useoffset and startaddr
        startaddr = 0
        useoffset = 0
        neededsize = bufsize

        # This is for the new API
        # return eapi.ram_get(self._board_state, channel, startaddr, useoffset,
        #                    neededsize, framesize, framegap, filename)

        # Back to the old API ... @todo: to be remove
        with open(filename, 'wb') as file:
            ret, rsize, data = eapi.ram_get(self._board_state, channel, startaddr, neededsize, framesize, framegap)
            # if ret<0:
            #     raise adp_exception(ret)
            if (neededsize != bufsize):
                if (bufsize + useoffset) > rsize:
                    print 'WARNING: not enough data in buffer to offset correctly, offset: ', useoffset
                    print '         buffer read size: ', rsize
                    print '         expected minimum read size: ', (bufsize + useoffset)
                mdata = data[useoffset : (bufsize + useoffset)]
                file.write(mdata)
            else:
                file.write(data)
            file.close()
            if rsize != neededsize:
                lostsize = neededsize - rsize
                print 'WARNING: transfer data bytes lost: ', lostsize

    @ensure_read_method
    def get_transfer_over_register(self):
        return self.custom_read(RAM_TRANSFER_REGISTER)

    def check_transfer_done(self, timeout):
        ret, addr, trigoffset = eapi.recplay_record_check_transfer_done(self._board_state, timeout)

    def fast_data_logger(self, filename):
        print "# Ram init"
        self.init_fast_data_logger()

        print "# record data at 125Mhz/sec for 2944000 bytes ..."
        self.start_recording_data_in_ram(2944000, 1)

        print "# Wait for trigger and record data ready"
        self.write(0x70000040, 0x400000)
        self.write(0x70000040, 0x400001)
        self.write(0x70000040, 0x400000)

        print "# Waiting for transfer done"
        self.check_transfer_done(200)

        print "# Get ram data to host"
        self.get_ram_data(filename, 0, 65536, 1024, 50000)
