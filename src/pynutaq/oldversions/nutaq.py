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

    phase_shift_cav = attributes_dict['phase_shift_cav']

    phase_shift_fw_cav = attributes_dict['phase_shift_fw_cav']

    phase_shift_fw_tet1 = attributes_dict['phase_shift_fw_tet1']

    amp_ref_in = attributes_dict['amp_ref_in']

    phase_ref_in = attributes_dict['phase_ref_in']

    loop_enable = attributes_dict['loop_enable']

    loop_input_selection = attributes_dict['loop_input_selection']

    tuning_enable = attributes_dict['tuning_enable']

    num_steps = attributes_dict['num_steps']

    phase_offset = attributes_dict['phase_offset']

    move = attributes_dict['move']

    move_up = attributes_dict['move_up']

    tuning_reset = attributes_dict['tuning_reset']

    icav_loops = attributes_dict['icav_loops']

    qcav_loops = attributes_dict['qcav_loops']

    icontrol = attributes_dict['icontrol']

    qcontrol = attributes_dict['qcontrol']

    ierror = attributes_dict['ierror']

    qerror = attributes_dict['qerror']

    ifw_cav_loops = attributes_dict['ifw_cav_loops']

    qfw_cav_loops = attributes_dict['qfw_cav_loops']

    ifw_tet1_loops = attributes_dict['ifw_tet1_loops']

    qfw_tet1_loops = attributes_dict['qfw_tet1_loops']

    amp_cav = attributes_dict['amp_cav']

    amp_fw = attributes_dict['amp_fw']

    ang_cav_fw = attributes_dict['ang_cav_fw']

    ang_cav_l = attributes_dict['ang_cav_l']

    ang_fw_l = attributes_dict['ang_fw_l']

    ispare = attributes_dict['ispare']

    qspare = attributes_dict['qspare']

    amp_spare = attributes_dict['amp_spare']

    phase_spare = attributes_dict['phase_spare']

    ipAddress = device_property(dtype=str)
    isSimulated = device_property(dtype=bool, default_value=False)

    # def __init__(self):
    #
    #     self._icav_loops = None
    #     self._qcav_loops = None
    #     self._icontrol = None
    #     self._qcontrol = None
    #
    #     self._ierror = None
    #     self._qerror = None
    #
    #     self._ifw_cav_loops = None
    #     self._qfw_cav_loops = None
    #     self._ifw_tet1_loops = None
    #     self._qfw_tet1_loops = None
    #
    #     self._ispare = None
    #     self._qspare = None
    #     self._amp_spare = None
    #     self._phase_spare = None
    #
    #     self._amp_cav = None
    #     self._amp_fw = None
    #     self._ang_cav_fw = None
    #     self._ang_cav_l = None
    #     self._ang_fw_l = None
    #     self.perseus = None

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
    def get_phase_shift_cav(self):
        return self.read_angle(PHASE_SHIFT_CAV_ADDRESS)

    @DebugIt()
    def set_phase_shift_cav(self, phase_shift_cav):
        self.write_angle(phase_shift_cav, PHASE_SHIFT_CAV_ADDRESS)

    @DebugIt()
    def get_phase_shift_fw_cav(self):
        return self.read_angle(PHASE_SHIFT_FW_CAV_ADDRESS)

    @DebugIt()
    def set_phase_shift_fw_cav(self, phase_shift_fw_cav):
        self.write_angle(phase_shift_fw_cav, PHASE_SHIFT_FW_CAV_ADDRESS)

    @DebugIt()
    def get_phase_shift_fw_tet1(self):
        return self.read_angle(PHASE_SHIFT_FW_TET1_ADDRESS)

    @DebugIt()
    def set_phase_shift_fw_tet1(self, phase_shift_fw_tet1):
        self.write_angle(phase_shift_fw_tet1, PHASE_SHIFT_FW_TET1_ADDRESS)

    @DebugIt()
    def get_amp_ref_in(self):
        return self.read_milivolts(AMP_REF_IN_ADDRESS)

    @DebugIt()
    def set_amp_ref_in(self, amp_ref_in):
        self.write_milivolts(amp_ref_in, AMP_REF_IN_ADDRESS)

    @DebugIt()
    def get_phase_ref_in(self):
        return self.read_angle(PHASE_REF_IN_ADDRESS)

    @DebugIt()
    def set_phase_ref_in(self, phase_ref_in):
        self.write_angle(phase_ref_in, PHASE_REF_IN_ADDRESS)

    @DebugIt()
    def get_loop_enable(self):
        return self.read_direct(LOOP_ENABLE_ADDRESS)

    @DebugIt()
    def set_loop_enable(self, loop_enable):
        self.write_direct(loop_enable, LOOP_ENABLE_ADDRESS)

    @DebugIt()
    def get_loop_input_selection(self):
        #@todo: Translate the values to corresponding strings
        return self.read_direct(LOOP_INPUT_SELECTION_ADDRESS)

    @DebugIt()
    def set_loop_input_selection(self, loop_input_selection):
        #@todo: Translate the values to corresponding strings
        self.write_direct(loop_input_selection, LOOP_INPUT_SELECTION_ADDRESS)

    @DebugIt()
    def get_tuning_enable(self):
        return self.read_direct(TUNING_ENABLE_ADDRESS)

    @DebugIt()
    def set_tuning_enable(self, tuning_enable):
        self.write_direct(tuning_enable, TUNING_ENABLE_ADDRESS)

    @DebugIt()
    def get_num_steps(self):
        return self.read_direct(NUM_STEPS_ADDRESS)

    @DebugIt()
    def set_num_steps(self, num_steps):
        self.write_direct(num_steps, NUM_STEPS_ADDRESS)

    @DebugIt()
    def get_phase_offset(self):
        return self.read_angle(PHASE_OFFSET_ADDRESS)

    @DebugIt()
    def set_phase_offset(self, phase_offset):
        self.write_angle(phase_offset, PHASE_OFFSET_ADDRESS)

    @DebugIt()
    def get_move(self):
        return self.read_direct(MOVE_ADDRESS)

    @DebugIt()
    def set_move(self, move):
        self.write_direct(move, MOVE_ADDRESS)

    @DebugIt()
    def get_move_up(self):
        return self.read_direct(MOVE_UP_ADDRESS)

    @DebugIt()
    def set_move_up(self, move_up):
        self.write_direct(move_up, MOVE_UP_ADDRESS)

    @DebugIt()
    def get_tuning_reset(self):
        return self.read_direct(TUNING_RESET_ADDRESS)

    @DebugIt()
    def set_tuning_reset(self, tuning_reset):
        self.write_direct(tuning_reset, TUNING_RESET_ADDRESS)

    @DebugIt()
    def read_icav_loops(self):
        return self._icav_loops

    @DebugIt()
    def read_qcav_loops(self):
        return self._qcav_loops

    @DebugIt()
    def read_icontrol(self):
        return self._icontrol

    @DebugIt()
    def read_qcontrol(self):
        return self._qcontrol

    @DebugIt()
    def read_ierror(self):
        return self._ierror

    @DebugIt()
    def read_qerror(self):
        return self._qerror

    @DebugIt()
    def read_ifw_cav_loops(self):
        return self._ifw_cav_loops

    @DebugIt()
    def read_qfw_cav_loops(self):
        return self._qfw_cav_loops

    @DebugIt()
    def read_ifw_tet1_loops(self):
        return self._ifw_tet1_loops

    @DebugIt()
    def read_qfw_tet1_loops(self):
        return self._qfw_tet1_loops

    @DebugIt()
    def read_ispare(self):
        return self._ispare

    @DebugIt()
    def read_qspare(self):
        return self._qspare

    @DebugIt()
    def read_amp_spare(self):
        return self._amp_spare

    @DebugIt()
    def read_phase_spare(self):
        return self._phase_spare

    @DebugIt()
    def read_amp_cav(self):
        return self._amp_cav

    @DebugIt()
    def read_amp_fw(self):
        return self._amp_fw

    @DebugIt()
    def read_ang_cav_fw(self):
        return self._ang_cav_fw

    @DebugIt()
    def read_ang_cav_l(self):
        return self._ang_cav_l

    @DebugIt()
    def read_ang_fw_l(self):
        return self._ang_fw_l

    @command
    def tuning_reset(self):
        self.write_direct(True, TUNING_RESET_ADDRESS)
        self.write_direct(False, TUNING_RESET_ADDRESS)

    @command
    def read_diagnostics(self):
        self.start_reading_diagnostics()

        self._icav_loops = self.read_diag_milivolts(ICAV_LOOPS_ADDRESS)
        self._qcav_loops = self.read_diag_milivolts(QCAV_LOOPS_ADDRESS)
        self._icontrol = self.read_diag_milivolts(ICONTROL_ADDRESS)
        self._qcontrol = self.read_diag_milivolts(QCONTROL_ADDRESS)

        self._ierror = self.read_diag_milivolts(IERROR_ADDRESS)
        self._qerror = self.read_diag_milivolts(QERROR_ADDRESS)

        self._ifw_cav_loops = self.read_diag_milivolts(IFW_CAV_LOOPS_ADDRESS)
        self._qfw_cav_loops = self.read_diag_milivolts(QFW_CAV_LOOPS_ADDRESS)
        self._ifw_tet1_loops = self.read_diag_milivolts(IFW_TET1_LOOPS_ADDRESS)
        self._qfw_tet1_loops = self.read_diag_milivolts(QFW_TET1_LOOPS_ADDRESS)

        self._ispare = self.read_diag_milivolts(ISPARE_ADDRESS)
        self._qspare = self.read_diag_milivolts(QSPARE_ADDRESS)
        self._amp_spare = self.calc_amplitude(self._ispare, self._qspare)
        self._phase_spare = self.calc_phase(self._ispare, self._qspare)

        self._amp_cav = self.read_diag_milivolts(AMP_CAV_ADDRESS)
        self._amp_fw = self.read_diag_milivolts(AMP_FW_ADDRESS)
        self._ang_cav_fw = self.read_diag_angle(ANG_CAV_FW_ADDRESS)
        self._ang_cav_l = self.read_diag_angle(ANG_CAV_L_ADDRESS)
        self._ang_fw_l = self.read_diag_angle(ANG_FW_L_ADDRESS)

        #self.end_reading_diagnostics()

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
