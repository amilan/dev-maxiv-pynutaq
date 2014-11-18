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
