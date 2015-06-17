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

"""This module contains useful functions to be used in the devices.
"""

__author__ = 'antmil'

__docformat__ = 'restructuredtext'

import math
from pynutaq.perseus.perseusdefs import *

def get_offset(type, cavity):
    if type == 'read':
        if cavity == 'A':
            return SETTINGS_READ_OFFSET_A
        elif cavity == 'B':
            return SETTINGS_READ_OFFSET_B
        else:
            raise 'Unknown cavity. Must be A or B.'
    elif type == 'write':
        if cavity == 'A':
            return SETTINGS_WRITE_OFFSET_A
        elif cavity == 'B':
            return SETTINGS_WRITE_OFFSET_B
        else:
            raise 'Unknown cavity. Must be A or B.'
    elif type == 'diag':
        if cavity == 'A':
            return DIAGNOSTICS_OFFSET_A
        elif cavity == 'B':
            return DIAGNOSTICS_OFFSET_B
        else:
            raise 'Unknown cavity. Must be A or B.'
    else:
        raise 'Wrong type of offset!'


def read_angle(perseus, address, cavity):
    # =IF(P6>32767;(P6-65536)/32767*180;P6/32767*180)

    offset = get_offset('read', cavity)

    perseus.write(offset, address)
    value = perseus.read(offset)

    if value > 32767:
        angle = (value - 65536) * 180.0 / 32767
    else:
        angle = (value * 180.0) / 32767
    return angle

def write_angle(perseus, value, address, cavity):
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

    offset = get_offset('write', cavity)
    perseus.write(offset, value)

def read_milivolts(perseus, address, cavity):
    """
        This method converts the value readed from a register in milivolts usign the following formula:
        VALUE = ROUND(P23*1000/32767*1,6467602581;0)
    :param value: value read from a register.
    :return: value converted in milivolts
    """
    offset = get_offset('read', cavity)

    perseus.write(offset, address)
    value = perseus.read(offset)

    milis = value * 1000.0 / 32767 * 1.6467602581
    return milis

def write_milivolts(perseus, milivolts, address, cavity):
    """
        This method converts the value from milivolts to bit to be written in the register usign the following
        formula:
        VALUE =ROUND(E23/1000*32767/1,6467602581;0)
    :param value: value to be converted.
    :return: value to write in the register.
    """
    value = (milivolts * 32767 / 1.6467602581) / 1000.0

    value = address << 17 | int(value)

    offset = get_offset('write', cavity)
    perseus.write(offset, value)

def read_settings_diag_milivolts(perseus, address, cavity):
    """
        This method converts the value readed from a register in milivolts usign the following formula:
        VALUE = ROUND(P23*1000/32767*1,6467602581;0)
    :param value: value read from a register.
    :return: value converted in milivolts
    """

    offset = get_offset('read', cavity)

    perseus.write(offset, address)
    value = perseus.read(offset)

    milis = value * 1000.0 / 32767
    return milis

def write_settings_diag_milivolts(perseus, milivolts, address, cavity):
    """
        This method converts the value from milivolts to bit to be written in the register usign the following
        formula:
        VALUE =ROUND(E23/1000*32767/1,6467602581;0)
    :param value: value to be converted.
    :return: value to write in the register.
    """
    value = (milivolts / 1000.0) * 32767

    value = address << 17 | int(value)

    offset = get_offset('write', cavity)

    perseus.write(offset, value)

def read_settings_diag_percentage(perseus, address, cavity):
    """
        This method converts the value readed from a register in milivolts usign the following formula:
        VALUE = ROUND(P23*1000/32767*1,6467602581;0)
    :param value: value read from a register.
    :return: value converted in milivolts
    """

    offset = get_offset('read', cavity)
    perseus.write(offset, address)
    value = perseus.read(offset)

    percentage = value * 100.0 / 32767
    return percentage

def write_settings_diag_percentage(perseus, percentage, address, cavity):
    """
        This method converts the value from milivolts to bit to be written in the register usign the following
        formula:
        VALUE =ROUND(E23/1000*32767/1,6467602581;0)
    :param value: value to be converted.
    :return: value to write in the register.
    """
    value = (percentage / 100.0) * 32767

    value = address << 17 | int(value)

    offset = get_offset('write', cavity)
    perseus.write(offset, value)

def read_direct(perseus, address, cavity):

    offset = get_offset('read', cavity)

    perseus.write(offset, address)
    value = perseus.read(offset)
    return value

def write_direct(perseus, value, address, cavity):
    value = address << 17 | int(value)

    offset = get_offset('write', cavity)
    perseus.write(offset, value)

def read_diag_angle(perseus, address, cavity):

    offset = get_offset('diag', cavity)

    perseus.write(offset, address)
    value = perseus.read(offset)
    # =IF(D49>32767;
    #    (D49-65536)/32767*180;
    #     D49/32767*180)
    if value > 32767:
        angle = (value - (1 << 16)) * 180.0 / 32767
    else:
        angle = value * 180.0 / 32767
    return angle

def read_diag_direct(perseus, address, cavity):

    offset = get_offset('diag', cavity)

    perseus.write(offset, address)
    value = perseus.read(offset)
    return value

def read_diag_milivolts(perseus, address, cavity):

    offset = get_offset('diag', cavity)
    perseus.write(offset, address)
    value = perseus.read(offset)
    #and now convert the value
    #=IF(D9<32768;
    #    D9/32767*1000;
    #   (D9-2^16)/32767*1000)
    if value < 32768:
        milis = value * 1000.0 / 32767
    else:
        milis = ((value - (1 << 16)) * 1000.0) / 32767
    return milis

def calc_amplitude(perseus, ivalue, qvalue):
    amplitude = math.sqrt((ivalue**2) + (qvalue**2))
    return amplitude

def calc_phase(perseus, ivalue, qvalue):
    phase = math.atan2(qvalue, ivalue)
    return phase


def start_reading_diagnostics(perseus, cavity):

    offset = get_offset('diag', cavity)
    value = 1 << 16
    perseus.write(offset, value)
    #@warning: I know ... this is not needed
    value = 0 << 16
    #lets continue
    perseus.write(offset, value)

def end_reading_diagnostics(perseus, cavity):

    offset = get_offset('diag', cavity)
    value = 1 << 16
    perseus.write(offset, value)
