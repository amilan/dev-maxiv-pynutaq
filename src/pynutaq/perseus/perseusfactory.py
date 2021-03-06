#!/usr/bin/env python

###############################################################################
#     Perseus factory.
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

"""This is the perseus factory module.
"""

__all__ = ["Perseus"]

__author__ = 'antmil'

__docformat__ = 'restructuredtext'

try:
    from pynutaq.perseus.perseusloops import PerseusLoops
    from pynutaq.perseus.perseusdiags import PerseusDiags
except ImportError, e:
    print e
    raise
from pynutaq.perseus.perseussimulated import PerseusSimulated


class Perseus(object):
    def new_perseus(self, perseus_type, perseus_ip):
        if perseus_type.lower() == 'simulated':
            return PerseusSimulated()
        elif perseus_type.lower() == 'loops':
            return PerseusLoops(perseus_ip)
        elif perseus_type.lower() == 'diags':
            return PerseusDiags(perseus_ip)
