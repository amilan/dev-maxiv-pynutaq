#!/usr/bin/env python

###############################################################################
#     Extra methods to be used by the special attributes in pynutaq device
#     server.
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

"""This module defines the extra methods used for the special attributes in the
device servers
"""

__author__ = 'antmil'

__docformat__ = 'restructuredtext'

import math

try:

    from pynutaq.perseus.perseusdefs import *

except ImportError, e:
    print "#############################################"
    print "It's not possible to import perseusdefs. "
    print "This device can run only in simulated mode.  "
    print "#############################################"
    raise

from pynutaq.perseus.perseusutils import read_direct, write_direct, read_diag_direct

def get_GainTetrode1(perseus, address):
    try:
        perseus.write(SETTINGS_READ_OFFSET_A, address)
        value = perseus.read(SETTINGS_READ_OFFSET_A) / 19898.0
        return value
    except Exception, e:
        raise e

def set_GainTetrode1(perseus, GainTetrode1, address):
    try:
        value = address << 17 | (int(GainTetrode1 * 19898.0))
        perseus.write(SETTINGS_WRITE_OFFSET_A, value)
    except Exception, e:
        raise e

def get_GainTetrode2(perseus, address):
    try:
        perseus.write(SETTINGS_READ_OFFSET_A, address)
        value = perseus.read(SETTINGS_READ_OFFSET_A) / 19898.0
        return value
    except Exception, e:
        raise e

def set_GainTetrode2(perseus, GainTetrode2, address):
    try:
        value = address << 17 | (int(GainTetrode2 * 19898.0))
        perseus.write(SETTINGS_WRITE_OFFSET_A, value)
    except Exception, e:
        raise e

def get_GainOl(perseus, address):
    try:
        perseus.write(SETTINGS_READ_OFFSET_A, address)
        value = perseus.read(SETTINGS_READ_OFFSET_A)
        # value = math.floor((value * 2.0) / 127)
        value = (value * 2.0) / 127
        return value
    except Exception, e:
        raise e

def set_GainOl(perseus, GainOl, address):
    try:
        value = math.ceil((GainOl/2.0) * 127)
        value = address << 17 | int(value)
        perseus.write(SETTINGS_WRITE_OFFSET_A, value)
    except Exception, e:
        raise e

def get_FreqsquareA(perseus, address):
    try:
        # @warning: read direct??
        perseus.write(SETTINGS_READ_OFFSET_A, address)
        value = perseus.read(SETTINGS_READ_OFFSET_A) / 80000.0
        return value
    except Exception, e:
        raise e

def set_FreqsquareA(perseus, FreqsquareA, address):
    try:
        value = ((1 / FreqsquareA) * 1000000.0) / 12.5
        value = address << 17 | int(value)
        perseus.write(SETTINGS_WRITE_OFFSET_A, value)
    except Exception, e:
        raise e

def get_ConditioningdutyCicleA(perseus, address):
    try:
        value = read_direct(perseus, address)
        value = (value / 8000000.0) * 256 * 100.0
        return value
    except Exception, e:
        raise e

def set_ConditioningdutyCicleA(perseus, ConditioningdutyCicleA, address):
    try:
        value = ((ConditioningdutyCicleA * 8000000.0) / 100.0) / 256
        write_direct(perseus, value, address)
    except Exception, e:
        raise e

def get_MDivider(perseus, address):
    try:
        value = read_direct(perseus, address) + 1
        # @warning: read_direct?? or +1
        return value
    except Exception, e:
        raise e

def set_MDivider(perseus, MDivider, address):
    try:
        value = MDivider - 1
        write_direct(perseus, value, address)
    except Exception, e:
        raise e

def get_NDivider(perseus, address):
    try:
        value = read_direct(perseus, address) + 1
        # @warning: read_direct?? or +1
        return value
    except Exception, e:
        raise e

def set_NDivider(perseus, NDivider, address):
    try:
        value = NDivider - 1
        write_direct(perseus, value, address)
    except Exception, e:
        raise e

def get_PilimitA(perseus, address):
    try:
        value = read_direct(perseus, address)
        value = (value* 1000.0) / 32767
        return  value
    except Exception, e:
        raise e

def set_PilimitA(perseus, PiLimitA, address):
    try:
        value = (PiLimitA/1000.0) * 32767
        write_direct(perseus, value, address)
    except Exception, e:
        raise e

def get_Fwmina(perseus, address):
    try:
        value = read_direct(perseus, address)
        value = (value* 1000.0) / 32767
        return  value
    except Exception, e:
        raise e

def set_Fwmina(perseus, Fwmina, address):
    try:
        value = (Fwmina/1000.0) * 32767
        write_direct(perseus, value, address)
    except Exception, e:
        raise e

def get_Tuningdelay(perseus, address):
    try:
        # P100/80000000*2^12
        value = read_direct(perseus, address)
        value = (value/80000000.0) * (2**12)
        return  value
    except Exception, e:
        raise e

def set_Tuningdelay(perseus, TuningDelay, address):
    try:
        # E100*80000000/2^12
        value = (TuningDelay*80000000.0) / (2**12)
        write_direct(perseus, value, address)
    except Exception, e:
        raise e

# Diagnostics device methods
# def get_Rvtet1(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 0
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e
#
# def get_Rvtet2(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 1
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e
#
# def get_Rvcirc(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 2
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e
#
# def get_Fwload(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 3
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e
#
# def get_Fwhybload(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 4
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e
#
# def get_Rvcav(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 5
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e
#
# def get_Arcs(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 6
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e
#
# def get_Vacuum(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 7
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e
#
# def get_ManualInterlock(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 8
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e
#
# def get_ExternalItck(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 9
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e
#
# def get_PlungerEndSwitchUp(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 10
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e
#
# def get_PlungerEndSwitchDown(perseus, address, itck_number):
#     try:
#         if itck_number == 0:
#             address = 150
#         pos = 11
#         address = address + itck_number
#         value = read_direct(perseus, address)
#         return bool((value >> pos) & 1)
#     except Exception, e:
#         raise e

def read_bit_direct(perseus, address, position):
    try:
        value = read_direct(perseus, address)
        return bool((value >> position) & 1)
    except Exception, e:
        raise e

def read_diag_bit_direct(perseus, address, position):
    try:
        value = read_diag_direct(perseus, address)
        return bool((value >> position) & 1)
    except Exception, e:
        raise e
