#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo power supply tango device server"""

import time
import numpy

from PyTango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from PyTango.server import Device, DeviceMeta, attribute, command, run
from PyTango.server import device_property


## nutaq imports
#from adp_exception import *
#from adp_commander import * #adp_commander
#from mi125_commander import * #mi125_commander
#from mo1000_commander import * #mo1000_commander
#from perseus_commander import perseus_commander
import eapi
##


class Nutaq(Device):
    __metaclass__ = DeviceMeta
    
    phase_shift_cav = attribute(label='PhaseShiftCav',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ_WRITE,
                                unit="degrees",format="6.4f",
                                min_value=-180.0 , max_value=360.0, 
                                fget="get_phase_shift_cav",
                                fset="set_phase_shift_cav",
                                doc=""
                                )

    amp_ref_in = attribute(label='AmpRefIn',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ_WRITE,
                                unit="mV",format="6.4f",
                                fget="get_amp_ref_in",
                                fset="set_amp_ref_in",
                                doc=""
                                )

    phase_ref_in = attribute(label='PhaseRefIn',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ_WRITE,
                                unit="degrees",format="6.4f",
                                fget="get_phase_ref_in",
                                fset="set_phase_ref_in",
                                doc=""
                                )

    loop_enable = attribute(label='LoopEnable',
                                dtype=bool,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ_WRITE,
                                unit="",format="6.4f",
                                fget="get_loop_enable",
                                fset="set_loop_enable",
                                doc=""
                                )

    tuning_enable = attribute(label='TuningEnable',
                                dtype=bool,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ_WRITE,
                                unit="",format="6.4f",
                                fget="get_tuning_enable",
                                fset="set_tuning_enable",
                                doc=""
                                )

    num_steps = attribute(label='NumSteps',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ_WRITE,
                                unit="",format="6.4f",
                                fget="get_num_steps",
                                fset="set_num_steps",
                                doc=""
                                )

    phase_offset = attribute(label='PhaseOffset',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ_WRITE,
                                unit="degree",format="6.4f",
                                fget="get_phase_offset",
                                fset="set_phase_offset",
                                doc=""
                                )

    move = attribute(label='move',
                                dtype=bool,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ_WRITE,
                                unit="",format="6.4f",
                                fget="get_move",
                                fset="set_move",
                                doc=""
                                )

    move_up = attribute(label='moveUp',
                                dtype=bool,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ_WRITE,
                                unit="",format="6.4f",
                                fget="get_move_up",
                                fset="set_move_up",
                                doc=""
                                )

    tuning_reset = attribute(label='TuningReset',
                                dtype=bool,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ_WRITE,
                                unit="",format="6.4f",
                                fget="get_tuning_reset",
                                fset="set_tuning_reset",
                                doc=""
                                )

    icav_loops = attribute(label='ICavLoops',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="mV",format="6.4f",
                                doc=""
                                )
    
    qcav_loops = attribute(label='QCavLoops',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="mV",format="6.4f",
                                doc=""
                                )
    
    icontrol = attribute(label='IControl',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="mV",format="6.4f",
                                doc=""
                                )
    
    qcontrol = attribute(label='QControl',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="mV",format="6.4f",
                                doc=""
                                )
    
    ierror = attribute(label='IError',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="mV",format="6.4f",
                                doc=""
                                )
    
    qerror = attribute(label='QError',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="mV",format="6.4f",
                                doc=""
                                )
    
    amp_cav = attribute(label='AmpCav',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="mV",format="6.4f",
                                doc=""
                                )
    
    amp_fw = attribute(label='AmpFw',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="mV",format="6.4f",
                                doc=""
                                )
    
    ang_cav_fw = attribute(label='AngCavFw',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="degrees",format="6.4f",
                                doc=""
                                )
    
    ang_cav_l = attribute(label='AngCavL',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="degrees",format="6.4f",
                                doc=""
                                )
    
    ang_fw_l = attribute(label='AngFwL',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="degrees",format="6.4f",
                                doc=""
                                )

    ipAddress = device_property(dtype=str)
    
    def init_device(self):
        try:
            eapi.eapi_init()
            self._board_state = eapi.connection_state()
            ret = eapi.connect_cce('192.168.0.101', self._board_state)
            ret = eapi.custom_register_write_send(self._board_state, 4, 1)

            print "MO1000 1 initialization..."
            ret = eapi.Mo1000_PowerUp_send(self._board_state,1)
            ret = eapi.Mo1000_Reset_send(self._board_state,1)
            ret = eapi.Mo1000_Init_send(self._board_state,1)
            print "DONE"
            print "MO1000 1 configure 80MHz ext (DAC 80MSPS 1X)..."

            device = "pll"
            device = getattr(eapi, "eMo1000Device" + device.capitalize())
            ret = eapi.Mo1000_WriteReg_send(self._board_state,
                                            1, device, 0, 0x8104020)
            ret = eapi.Mo1000_WriteReg_send(self._board_state,
                                            1, device, 0, 0x8104020 )
            ret = eapi.Mo1000_WriteReg_send(self._board_state,
                                            1, device, 1, 0x8140022 )
            ret = eapi.Mo1000_WriteReg_send(self._board_state,
                                            1, device, 2, 0x6884030 )
            ret = eapi.Mo1000_WriteReg_send(self._board_state,
                                            1, device, 3, 0x8140020 )
            ret = eapi.Mo1000_WriteReg_send(self._board_state,
                                            1, device, 4, 0xEB84031 )
            ret = eapi.Mo1000_WriteReg_send(self._board_state,
                                            1, device, 5, 0x38040AA )
            ret = eapi.Mo1000_WriteReg_send(self._board_state,
                                            1, device, 6, 0x808E012 )
            ret = eapi.Mo1000_WriteReg_send(self._board_state,
                                            1, device, 7, 0xBD9ABDE )
            ret = eapi.Mo1000_WriteReg_send(self._board_state,
                                            1, device, 8, 0x20009D9 )
            print "DONE"
            mode = "1x"
            mode = getattr(eapi, "eAd9148Inter" + mode.capitalize())
            ret = eapi.Mo1000_SetDacParInterpolation_send(self._board_state,
                                                          1, mode)
            ret = eapi.Mo1000_DoDacUpdate_send(self._board_state, 1)
            print "MO1000 1 clock configuration (ignore mmcm lock error from here)"
            src_clk = "125mhz"
            src_clk = getattr(eapi, "eMo1000ClkSrc" + src_clk.capitalize())
            master_clk_mode = "manual"
            master_clk_mode = getattr(eapi, "eMo1000MasterClk" + master_clk_mode.capitalize())
            ret = eapi.Mo1000_SetClockConfig_send(self._board_state, 
                                                  1, src_clk,
                                                  0, 80000000,
                                                  master_clk_mode, 80000000
                                                  )
            print "DONE (end ignore mmcm lock error)"
            device = "ports"
            device = getattr(eapi, "eMo1000Device" + device.capitalize())
            ret = eapi.Mo1000_WriteReg_send(self._board_state,1, device, 0, 0x9d )
            time.sleep(2)
            print "pll calibration"
            device = "pll"
            device = getattr(eapi, "eMo1000Device" + device.capitalize())
            ret = eapi.Mo1000_WriteReg_send(self._board_state,1, device, 6, 0x848E012 )
            time.sleep(2)
            print "DONE"
            print "MO1000 1 pll sync"
            device = "ports"
            device = getattr(eapi, "eMo1000Device" + device.capitalize())
            ret = eapi.Mo1000_WriteReg_send(self._board_state,1, device, 1, 3 )
            time.sleep(1)
            device = "core"
            device = getattr(eapi, "eMo1000Device" + device.capitalize())
            ret = eapi.Mo1000_WriteReg_send(self._board_state,1, device, 1, 0x10 )
            print "DONE"
            time.sleep(1)
            ret, status, compare = eapi.Mo1000_GetStatus_send(self._board_state, 1)
            print "Status = " + status
            print "Compare = " + compare
            
            print "MO1000 1 calibration"
            ret = eapi.Mo1000_DoDacCalibration_send(self._board_state, 1)

            print "DONE"
            ret, uChannelLaneCalib, uChannelFrameCalib, uChannelSyncCalib, uCalibStatus = eapi.Mo1000_GetChannelCalibStatus_send(self._board_state, 1)
            #mode = "templc"
            #mode = getattr(eapi, "eMo1000" + mode.capitalize())
            #ret, temp, tdac1, tdac2 = eapi.Mo1000_GetTemperature_send(self._board_state, 1, mode)
            
            print "Mi125 2 initialization..."
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
            ret,channellanecalib,channelcalibstatus = eapi.MI125_mi125_get_channelcalibstatus_send(self._board_state, 2)
            print "DONE"
            
            print "MO1000 1 enable dac outputs"
            state = "enable"
            state = getattr(eapi, "eMo1000Output" + state.capitalize())
            ret = eapi.Mo1000_SetDacOutCtrl_send(self._board_state, 1, 1, state)
            ret = eapi.Mo1000_SetDacOutCtrl_send(self._board_state, 1, 1, state )
            ret = eapi.Mo1000_SetDacOutCtrl_send(self._board_state, 1, 2, state )
            ret = eapi.Mo1000_SetDacOutCtrl_send(self._board_state, 1, 3, state )
            ret = eapi.Mo1000_SetDacOutCtrl_send(self._board_state, 1, 4, state )
            ret = eapi.Mo1000_SetDacOutCtrl_send(self._board_state, 1, 5, state )
            ret = eapi.Mo1000_SetDacOutCtrl_send(self._board_state, 1, 6, state )
            ret = eapi.Mo1000_SetDacOutCtrl_send(self._board_state, 1, 7, state )
            ret = eapi.Mo1000_SetDacOutCtrl_send(self._board_state, 1, 8, state )
            print "DONE"
            print "Remove reset MI125 - MO1000 intercore fifo"
            ret = eapi.custom_register_write_send(self._board_state, 4, 0)
            print "DONE"
            print "Displays any dac error that happened"
            ret, status, compare = eapi.Mo1000_GetStatus_send(self._board_state, 1)
            
            print "DONE"

            print "configuring GPIO inputs/outputs"

            ret = eapi.custom_register_write_send(self._board_state, 13, 0x1 )
            ret = eapi.custom_register_write_send(self._board_state, 13, 0x0 )
            ret = eapi.custom_register_write_send(self._board_state, 13, 0x1ffff )
            ret = eapi.custom_register_write_send(self._board_state, 13, 0x20000 )
            ret = eapi.custom_register_write_send(self._board_state, 13, 0x30001 )
            ret = eapi.custom_register_write_send(self._board_state, 13, 0x30001 )
            ret = eapi.custom_register_write_send(self._board_state, 13, 0x40001 )
            ret = eapi.custom_register_write_send(self._board_state, 13, 0x40000 )

            print "configuring VCXO"
            ret = eapi.custom_register_write_send(self._board_state, 10, 0x3e80009 )
            ret = eapi.custom_register_write_send(self._board_state, 10, 0x3eA0007 )
            ret = eapi.custom_register_write_send(self._board_state, 10, 0x3eC0000 )
            ret = eapi.custom_register_write_send(self._board_state, 10, 0x3eE0000 )
            ret = eapi.custom_register_write_send(self._board_state, 10, 0x3f00000 )
            ret = eapi.custom_register_write_send(self._board_state, 10, 0x3f20000 )
            ret = eapi.custom_register_write_send(self._board_state, 10, 0x3f40000 )
            ret = eapi.custom_register_write_send(self._board_state, 10, 0x3f60000 )
            ret = eapi.custom_register_write_send(self._board_state, 10, 0x3FA0001 )
            ret = eapi.custom_register_write_send(self._board_state, 10, 0x3F80000 )
            ret = eapi.custom_register_write_send(self._board_state, 10, 0x3F80001 )

            print "configuring Loops Board registers"

            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00000000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00020001 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00040000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00060000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00080000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x000A0000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x000C3FFF )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x000E0000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00100000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00120000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00140000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00160000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00180000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x001A4DBA )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x001C4DBA )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x001E0000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00200005 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00220000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00240000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x002607C6 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00282000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x002A07C6 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x002C0E39 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x002E0007 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x0032003F )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00340000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00360000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00380000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x003A0000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x003C0000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x003E0000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00DC0006 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x03200001 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00C80000 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x00CA0000 )

            print "configuring Frequency of tuning pulses"
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x025E0003 )
            print "configuring direction of tuning loop - tuning pos enabled"
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x025A0001 )

            print "configuring limit up and down of tuning deadband"
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x026A0222 )
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x026C00B6 )

            print "disabling Fast interlocks"
            ret = eapi.memory_write_send(self._board_state, 0x70000040, 0x03220001 )
            
            print "Init DONE"
            self.set_state(DevState.ON)
        except Exception,e:
            print e
            self.set_state(DevState.FAULT)

    def read_angle(self, value):
        #=IF(P6>32767;(P6-65536)/32767*180;P6/32767*180)
        if value > 32767:
            angle = (value - 65536) * 180.0 / 32767
        else:
            angle = (value * 180.0) / 32767
        return angle

    def write_angle(self, value):
        """=ROUND(IF(
                     E6<0; E6/180*32767+65536;
                     IF(E6<=180; E6/180*32767;
                       (E6-360)/180*32767+65536)
                    );0
                )
        """
        if value < 0:
            angle = (value*32767 / 180.0) + 65536
        elif value <= 180.0:
            angle = ( value * 32767 ) / 180.0
        else:
            angle = ( ( value - 360 ) * 32767 / 180.0 ) + 65536
        return angle

    def read_milivolts(self):
        pass
    
    def write_milivolts(self):
        pass
    
    def read_direct(self):
        pass
    
    def write_direct(self):
        pass

    def read_diag_angle(self):
        pass
        
    def read_diag_milivolts(self):
        pass
    
    @DebugIt()
    def get_phase_shift_cav(self):
        address = hex(2<<17)
        address = 2
        ret = eapi.memory_write_send(self._board_state, 0x70000044, address)
        ret, value = eapi.memory_read_send(self._board_state, 0x70000044)
        self._phase_shift_cav = self.read_angle(value)
        return self._phase_shift_cav

    @DebugIt()
    def set_phase_shift_cav(self, phase_shift_cav):
        self._phase_shift_cav = phase_shift_cav
        phase = self.write_angle(phase_shift_cav)
        value = 2<<17 | int(phase)
        ret = eapi.memory_write_send(self._board_state, 0x70000040, value)

    @DebugIt()
    def get_amp_ref_in(self):
        pass

    @DebugIt()
    def set_amp_ref_in(self):
        pass

    @DebugIt()
    def get_phase_ref_in(self):
        pass

    @DebugIt()
    def set_phase_ref_in(self):
        pass

    @DebugIt()
    def get_loop_enable(self):
        pass

    @DebugIt()
    def set_loop_enable(self):
        pass

    @DebugIt()
    def get_tuning_enable(self):
        pass

    @DebugIt()
    def set_tuning_enable(self):
        pass

    @DebugIt()
    def get_num_steps(self):
        pass

    @DebugIt()
    def set_num_steps(self):
        pass

    @DebugIt()
    def get_phase_offset(self):
        pass

    @DebugIt()
    def set_phase_offset(self):
        pass

    @DebugIt()
    def get_move(self):
        pass

    @DebugIt()
    def set_move(self):
        pass

    @DebugIt()
    def get_move_up(self):
        pass

    @DebugIt()
    def set_move_up(self):
        pass

    @DebugIt()
    def get_tuning_reset(self):
        pass

    @DebugIt()
    def set_tuning_reset(self):
        pass

    @DebugIt()
    def read_icav_loops(self):
        pass

    @DebugIt()
    def read_qcav_loops(self):
        pass

    @DebugIt()
    def read_icontrol(self):
        pass

    @DebugIt()
    def read_qcontrol(self):
        pass

    @DebugIt()
    def read_ierror(self):
        pass

    @DebugIt()
    def read_qerror(self):
        pass

    @DebugIt()
    def read_amp_cav(self):
        pass

    @DebugIt()
    def read_amp_fw(self):
        pass

    @DebugIt()
    def read_ang_cav_fw(self):
        pass

    @DebugIt()
    def read_ang_cav_l(self):
        pass

    @DebugIt()
    def read_ang_fw_l(self):
        pass

if __name__ == "__main__":
    run([Nutaq])
