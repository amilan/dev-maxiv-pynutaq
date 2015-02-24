__author__ = 'antmil'

class InterlocksDiags(object):
    def __init__(self):
        itck_inputs = ['RvTet1', 'RvTet2', 'RvCircIn', 'FwLoad', 'FwHybLoad',
                       'RvCav', 'Arc', 'Vaccum', 'Manual', 'EndSwUp',
                       'EndSwdown', 'MPS']

        itck_outputs = ['DACsOffLoopsStby', 'PinDiodeSwitch', 'FDLTrg',
                        'PLCTxOff', 'MPS', 'Diag']

        self._itck_dict = {}

        for input in itck_inputs:
            for output in itck_outputs:
                self._itck_dict[input][output] = 0

    def get_itck(self, input, output):
        return self._itck_dict[input][output]

    def set_itck(self, input, output, value):
        self._itck_dict[input][output] = value
