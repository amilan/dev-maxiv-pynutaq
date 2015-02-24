#!/usr/bin/env python

###############################################################################
##     Perseus decorators to be used to ensure communications with the boards.
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

from adp_exception import *
import eapi

def ensure_write_method(meth):
    def _ensure_this_method(self, *args, **kwargs):
        try:
            ret = meth(self, *args, **kwargs)
            if ret is not None and ret < 0:
                msg = "Error in: " + meth.__name__ + ", Error code = " + str(ret)
                raise Exception(msg)
#                raise adp_exception(ret)
            return ret
        except Exception, e:
            raise e

    return _ensure_this_method

def ensure_read_method(meth):
    def _ensure_this_method(self, *args, **kwargs):
        try:
            ret, value = meth(self, *args, **kwargs)
            #value = meth(self, *args, **kwargs)
            if ret < 0:
                msg = "Error in: " + meth.__name__ + ", Error code = " + str(ret)
                raise Exception(msg)
 #               raise adp_exception(ret)
            return value
        except Exception:
            raise

    return _ensure_this_method

def ensure_connect_method(meth):
    def _ensure_this_method(self, *args, **kwargs):
        try:
            ret = meth(self, *args, **kwargs)
            if ret:
                msg = "Error in: " + meth.__name__ + ", Error code = " + str(ret)
                raise Exception(msg)
#                raise adp_exception(ret)
            return ret
        except Exception, e:
            raise e

    return _ensure_this_method
