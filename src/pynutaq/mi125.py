__author__ = 'antmil'

import eapi
from perseusdecorators import ensure_write_method

class Mi125(object):

    def __init__(self, board_state, board_number):

        self._board_state = board_state
        self.board_number = board_number

        self.power_up()

        self.reset()

        self.read_temperature()
        self.m125_configure()

        self.set_clock_source(clksrc)

    @ensure_write_method
    def power_up(self):
        return eapi.MI125_powerup_send(self._board_state, self.board_number)

    @ensure_write_method
    def reset(self):
        return eapi.MI125_mi125_reset_send(self._board_state, self.board_number)

    def read_temperature(self):
        # tempmode = "templc"
        #tempmode = getattr(eapi, "MI125_" + tempmode.upper())
        #ret,temperature = eapi.MI125_mi125_get_temperature_send(self._board_state, 2, tempmode)
        pass

    def m125_configure(self):
        groupch = "16channels"
        groupch = getattr(eapi, "MI125_" + groupch.upper())
        lvds = "termon1750ua"
        lvds = getattr(eapi, "MI125_" + lvds.upper())
        randmode = "randomizeoff"
        randmode = getattr(eapi, "MI125_" + randmode.upper())
        binmode = "twocomplement"
        binmode = getattr(eapi, "MI125_" + binmode.upper() + "FORMAT")
        self._set_config(groupch, lvds, randmode, binmode)

    @ensure_write_method
    def _set_config(self, groupch, lvds, randmode, binmode):
        return eapi.MI125_mi125_set_config_send(self._board_state, self.board_number, groupch, lvds, randmode, binmode)

    def set_clock_source(self, clksrc):
        if clksrc.lower() == 'bottomfmc':
            clksrc = "BOTTOMFMC"
        elif clksrc.lower() == 'ext':
            clksrc = "EXT"
        clksrc = getattr(eapi, "MI125_CLKSRC" + clksrc.upper())
        self._set_clock_source(clksrc)
        ret, channellanecalib, channelcalibstatus = eapi.MI125_mi125_get_channelcalibstatus_send(self._board_state,
                                                                                                 self.board_number)

    @ensure_write_method
    def _set_clock_source(self, clksrc):
        return eapi.MI125_mi125_set_clksrc_send(self._board_state, self.board_number, clksrc)
