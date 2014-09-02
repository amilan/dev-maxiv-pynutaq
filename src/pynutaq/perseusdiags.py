__author__ = 'antmil'

import eapi
from perseusdefs import *
from mo1000 import Mo1000
from mi125 import Mi125
from adp_exception import *
from perseusdecorators import ensure_read_method, ensure_write_method

MI125_BOARD_NUMBER = 1

class PerseusDiags(object):

    def __init__(self):
            eapi.eapi_init()
            self._board_state = eapi.connection_state()
            self.connect()

            print "Mi125 2 initialization..."
            self.mi125 = Mi125(self._board_state, MI125_BOARD_NUMBER)
            print "DONE"

            self.configure_gpio_inputs_outputs()

            self.configure_vcxo()

            self.configure_loops_registers()

            print "Init DONE"

    @ensure_write_method
    def connect(self):
        eapi.connect_cce(PERSEUS_DIAG_IP, self._board_state)

    @ensure_write_method
    def custom_write(self, register, data):
        """
           @todo: this method should be merge with self.write when it will be supported in all platforms.
        """
        eapi.custom_register_write_send(self._board_state, register, data)

    @ensure_write_method
    def write(self, address, value):
        eapi.memory_write_send(self._board_state, address, value)

    @ensure_read_method
    def read(self, address):
        eapi.memory_read_send(self._board_state, address)

    def configure_gpio_inputs_outputs(self):
        print "configuring GPIO inputs/outputs"
        register = 13
        values = [0x1, 0x0, 0x1ffff, 0x20000, 0x30001, 0x30001, 0x40001, 0x40000]
        for value in values:
            self.custom_write(register, value)

    def configure_vcxo(self):
        print "configuring VCXO"
        register = 10
        values = [0x3e80009, 0x3eA0007, 0x3eC0000, 0x3eE0000, 0x3f00000,
                  0x3f20000, 0x3f40000, 0x3f60000, 0x3FA0001, 0x3F80000, 0x3F80001]
        for value in values:
            self.custom_write(register, value)

    def configure_diags_registers(self):
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
