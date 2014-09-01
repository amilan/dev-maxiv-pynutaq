__author__ = 'antmil'

import eapi


class Mi125(object):
    def __init__(self, board_state):

        self._board_state = board_state
        ret = eapi.MI125_powerup_send(self._board_state, 2)
        ret = eapi.MI125_mi125_reset_send(self._board_state, 2)
        #tempmode = "templc"
        #tempmode = getattr(eapi, "MI125_" + tempmode.upper())
        #ret,temperature = eapi.MI125_mi125_get_temperature_send(self._board_state, 2, tempmode)
        groupch = "16channels"
        groupch = getattr(eapi, "MI125_" + groupch.upper())
        lvds = "termon1750ua"
        lvds = getattr(eapi, "MI125_" + lvds.upper())
        randmode = "randomizeoff"
        randmode = getattr(eapi, "MI125_" + randmode.upper())
        binmode = "twocomplement"
        binmode = getattr(eapi, "MI125_" + binmode.upper() + "FORMAT")
        ret = eapi.MI125_mi125_set_config_send(self._board_state, 2, groupch, lvds, randmode, binmode)
        clksrc = "BOTTOMFMC"
        clksrc = getattr(eapi, "MI125_CLKSRC" + clksrc.upper())
        ret = eapi.MI125_mi125_set_clksrc_send(self._board_state, 2, clksrc)
        ret, channellanecalib, channelcalibstatus = eapi.MI125_mi125_get_channelcalibstatus_send(self._board_state, 2)