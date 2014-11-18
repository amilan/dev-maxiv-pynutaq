__author__ = 'antmil'

import time
import eapi
from adp_exception import *
from perseusdecorators import ensure_write_method


class Mo1000(object):
    #@todo: finish to extract the board_number

    def __init__(self, board_state, board_number=1):
        self._board_state = board_state
        self._board_number = board_number

        self.power_up()
        self.reset()
        self.init()

        print "DONE"

        self.configure_800MHZ()

        self.configure_dacs()

        self.configure_clock()

        self.configure_ports()

        self.pll_calibration()

        self.pll_sync()

        self.get_status()

        self.calibration()

        # mode = "templc"
        #mode = getattr(eapi, "eMo1000" + mode.capitalize())
        #ret, temp, tdac1, tdac2 = eapi.Mo1000_GetTemperature_send(self._board_state, 1, mode)

    @ensure_write_method
    def power_up(self):
        return eapi.Mo1000_PowerUp_send(self._board_state, self._board_number)

    @ensure_write_method
    def reset(self):
        return eapi.Mo1000_Reset_send(self._board_state, self._board_number)

    @ensure_write_method
    def init(self):
        return eapi.Mo1000_Init_send(self._board_state, self._board_number)

    @ensure_write_method
    def write(self, board_number, device, address, value):
        return eapi.Mo1000_WriteReg_send(self._board_state, board_number, device, address, value)

    def configure_800MHZ(self):
        print "MO1000 1 configure 80MHz ext (DAC 80MSPS 1X)..."
        device = "pll"
        device = getattr(eapi, "eMo1000Device" + device.capitalize())
        # ret = eapi.Mo1000_WriteReg_send(self._board_state, 1, device, 0, 0x8104020)
        values = [0x8104020, 0x8140022, 0x6884030, 0x8140020, 0xEB84031, 0x38040AA, 0x808E012, 0xBD9ABDE, 0x20009D9]
        for i in range(9):
            self.write(self._board_number, device, i, values[i])
        print "DONE"

    def configure_dacs(self):
        mode = "1x"
        mode = getattr(eapi, "eAd9148Inter" + mode.capitalize())
        ret = eapi.Mo1000_SetDacParInterpolation_send(self._board_state, 1, mode)
        ret = eapi.Mo1000_DoDacUpdate_send(self._board_state, self._board_number)

    def configure_clock(self):
        print "MO1000 1 clock configuration (ignore mmcm lock error from here)"
        src_clk = "125mhz"
        src_clk = getattr(eapi, "eMo1000ClkSrc" + src_clk.capitalize())
        master_clk_mode = "manual"
        master_clk_mode = getattr(eapi, "eMo1000MasterClk" + master_clk_mode.capitalize())
        ret = eapi.Mo1000_SetClockConfig_send(self._board_state,1, src_clk, 0, 80000000, master_clk_mode, 80000000)
        print "DONE (end ignore mmcm lock error)"

    def configure_ports(self):
        device = "ports"
        device = getattr(eapi, "eMo1000Device" + device.capitalize())
        self.write(self._board_number, device, 0, 0x9d)
        time.sleep(2)

    def pll_calibration(self):
        print "pll calibration"
        device = "pll"
        device = getattr(eapi, "eMo1000Device" + device.capitalize())
        self.write(self._board_number, device, 6, 0x848E012)
        time.sleep(2)
        print "DONE"

    def pll_sync(self):
        print "MO1000 1 pll sync"
        device = "ports"
        device = getattr(eapi, "eMo1000Device" + device.capitalize())
        self.write(self._board_number, device, 1, 3)
        time.sleep(1)
        device = "core"
        device = getattr(eapi, "eMo1000Device" + device.capitalize())
        self.write(self._board_number, device, 1, 0x10)
        print "DONE"
        time.sleep(1)

    def get_status(self):
        ret, status, compare = eapi.Mo1000_GetStatus_send(self._board_state, self._board_number)
        print "Status = " + status
        print "Compare = " + compare

    def calibration(self):
        print "MO1000 1 calibration"
        ret = eapi.Mo1000_DoDacCalibration_send(self._board_state, self._board_number)
        print "DONE"
        ret, uChannelLaneCalib, uChannelFrameCalib, uChannelSyncCalib, uCalibStatus = eapi.Mo1000_GetChannelCalibStatus_send(
            self._board_state, self._board_number)

    def enable_dac_outputs(self):
        print "MO1000 1 enable dac outputs"

        def get_channel(channel_num):
            channel = str(channel_num)
            channel = getattr(eapi, "eMo1000SelectDac" + channel.capitalize())
            return channel

        state = "enable"
        state = getattr(eapi, "eMo1000Output" + state.capitalize())
        # ret = eapi.Mo1000_SetDacOutCtrl_send(self._board_state, 1, 1, state)
        for i in range(1,9):
            channel = get_channel(i)
            ret = eapi.Mo1000_SetDacOutCtrl_send(self._board_state, 1, channel, state)
            if ret < 0:
                raise adp_exception(ret)
        print "DONE"

    def display_dac_error(self):
        print "Displays any dac error that happened"
        ret, status, compare = eapi.Mo1000_GetStatus_send(self._board_state, self._board_number)
        print "DONE"
