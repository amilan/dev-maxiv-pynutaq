__author__ = 'antmil'

try:
    from perseusloops import PerseusLoops
    from perseusdiags import PerseusDiags
except Exception, e:
    print e
from perseussimulated import PerseusSimulated


class Perseus(object):
    def new_perseus(self, perseus_type):
        if perseus_type.lower() == 'simulated':
            return PerseusSimulated()
        elif perseus_type.lower() == 'loops':
            return PerseusLoops()
        elif perseus_type.lower() == 'diags':
            return PerseusDiags()
