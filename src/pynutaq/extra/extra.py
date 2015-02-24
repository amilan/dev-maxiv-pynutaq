#!/usr/bin/env python

###############################################################################
##     Extra methods to be used by the special attributes in pynutaq device
##     server.
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

__author__ = "amilan"

from perseusdefs import *
from utils import read_direct, write_direct

def get_GainTetrode1(perseus, address):
    try:
        perseus.write(SETTINGS_READ_OFFSET, address)
        value = perseus.read(SETTINGS_READ_OFFSET) / 19898.0
        return value
    except Exception, e:
        raise e

def set_GainTetrode1(perseus, GainTetrode1, address):
    try:
        value = address << 17 | (int(GainTetrode1) * 19898)
        perseus.write(SETTINGS_WRITE_OFFSET, value)
    except Exception, e:
        raise e

def get_GainTetrode2(perseus):
    try:
        perseus.write(SETTINGS_READ_OFFSET, 14)
        value = perseus.read(SETTINGS_READ_OFFSET) / 19898.0
        return value
    except Exception, e:
        raise e

def set_GainTetrode2(perseus, GainTetrode2i, address):
    try:
        value = address << 17 | (int(GainTetrode2) * 19898)
        perseus.write(SETTINGS_WRITE_OFFSET, value)
    except Exception, e:
        raise e

def get_GainOl(perseus, address):
    try:
        perseus.write(SETTINGS_READ_OFFSET, address)
        value = perseus.read(SETTINGS_READ_OFFSET)
        return value
    except Exception, e:
        raise e

def set_GainOl(perseus, GainOl, address):
    try:
        value = address << 17 | int(GainOl)
        perseus.write(SETTINGS_WRITE_OFFSET, value)
    except Exception, e:
        raise e

def get_FreqsquareA(perseus, address):
    try:
        #@warning: read direct??
        perseus.write(SETTINGS_READ_OFFSET, address)
        value = perseus.read(SETTINGS_READ_OFFSET)
        return value
    except Exception, e:
        raise e

def set_FreqsquareA(perseus, FreqsquareA):
    try:
        value = ((1 / FreqsquareA) * 1000000) / 12.5
        value = address << 17 | int(value)
        perseus.write(SETTINGS_WRITE_OFFSET, value)
    except Exception, e:
        raise e

def get_ConditioningdutyCicleA(self, address):
    try:
        value = self.read_direct(address)
        value = (value / 8000000) * 2562 * 100
        return value
    except Exception, e:
        raise e

def set_ConditioningdutyCicleA(perseus, ConditioningdutyCicleA, address):
    try:
        value = ((ConditioningdutyCicleA * 8000000) / 100.0) / 256
        self.write_direct(value, address)
    except Exception, e:
        raise e

def get_MDivider(perseus, address):
    try:
        value = read_direct(address) + 1
        #@warning: read_direct?? or +1
        return value
    except Exception, e:
        raise e

def set_MDivider(perseus, MDivider, address):
    try:
        value = MDivider - 1
        write_direct(value, address)
    except Exception, e:
        raise e

def get_NDivider(perseus, address):
    try:
        value = read_direct(address) + 1
        #@warning: read_direct?? or +1
        return value
    except Exception, e:
        raise e

def set_NDivider(perseus, NDivider, address):
    try:
        value = MDivider - 1
        write_direct(value, address)
    except Exception, e:
        raise e

