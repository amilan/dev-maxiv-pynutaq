#!/usr/bin/env python

#############################################################################
##
## This file is part of Taurus, a Tango User Interface Library
##
## http://www.tango-controls.org/static/taurus/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
###########################################################################

"""
configuration file for an example of how to construct a GUI based on TaurusGUI

This configuration file determines the default, permanent, pre-defined
contents of the GUI. While the user may add/remove more elements at run
time and those customizations will also be stored, this file defines what a
user will find when launching the GUI for the first time.
"""

#==============================================================================
# Import section. You probably want to keep this line. Don't edit this block
# unless you know what you are doing
from taurus.qt.qtgui.taurusgui.utils import PanelDescription, ExternalApp, ToolBarDescription, AppletDescription
# (end of import section)
#==============================================================================


#===============================================================================
# General info.
#===============================================================================
GUI_NAME = 'llrfGUI'
ORGANIZATION = 'Max-IV'

#===============================================================================
# Specific logo. It can be an absolute path,or relative to the app dir or a
# resource path. If commented out, ":/taurus.png" will be used
#===============================================================================
#CUSTOM_LOGO = <path GUI-specific logo

#===============================================================================
# You can provide an URI for a manual in html format
# (comment out or make MANUAL_URI=None to skip creating a Manual panel)
#===============================================================================
#MANUAL_URI = 'http://packages.python.org/taurus'

#===============================================================================
# If you want to have a main synoptic panel, set the SYNOPTIC variable
# to the file name of a jdraw file. If a relative path is given, the directory
# containing this configuration file will be used as root
# (comment out or make SYNOPTIC=None to skip creating a synoptic panel)
#===============================================================================
#SYNOPTIC = ['images/beamlines.jdw']

#===============================================================================
# Set INSTRUMENTS_FROM_POOL to True for enabling auto-creation of
# instrument panels based on the Pool Instrument info
#===============================================================================
INSTRUMENTS_FROM_POOL = False

#===============================================================================
# Define panels to be shown.
# To define a panel, instantiate a PanelDescription object (see documentation
# for the gblgui_utils module)
#===============================================================================

trend = PanelDescription('Trend',
                        classname = 'TaurusTrend',
                        model = '')

settings_loops = PanelDescription('SettingsLoops',
                        classname = 'TaurusForm',
                        model = [
                                 'ws/rf/pynutaq-1/KpA',
                                 'ws/rf/pynutaq-1/KiA',
                                 'ws/rf/pynutaq-1/PhaseShiftCav',
                                 'ws/rf/pynutaq-1/PhaseShiftFwcav',
                                 'ws/rf/pynutaq-1/PhaseShiftFwtet1',
                                 'ws/rf/pynutaq-1/PhaseShiftFwtet2',
                                 'ws/rf/pynutaq-1/PilimitA',
                                 'ws/rf/pynutaq-1/SamplesToAverage',
                                 'ws/rf/pynutaq-1/FilterStages',
                                 'ws/rf/pynutaq-1/PhaseShiftFwcircin',
                                 'ws/rf/pynutaq-1/PhaseShiftControlSignalTet1',
                                 'ws/rf/pynutaq-1/PhaseShiftControlSignalTet2',
                                 'ws/rf/pynutaq-1/GainTetrode1',
                                 'ws/rf/pynutaq-1/GainTetrode2',
                                 'ws/rf/pynutaq-1/AutomaticStartupEnable',
                                 'ws/rf/pynutaq-1/CommandStart',
                                 'ws/rf/pynutaq-1/Amprefin',
                                 'ws/rf/pynutaq-1/Phrefin',
                                 'ws/rf/pynutaq-1/Amprefmin',
                                 'ws/rf/pynutaq-1/Phrefmin',
                                 'ws/rf/pynutaq-1/PhaseIncreaseRate',
                                 'ws/rf/pynutaq-1/VoltageRateIncrease',
                                 'ws/rf/pynutaq-1/GainOl',
                                 'ws/rf/pynutaq-1/SpareGpioOutput01',
                                 'ws/rf/pynutaq-1/SpareGpioOutput02',
                                 'ws/rf/pynutaq-1/SpareGpioOutput03',
                                 'ws/rf/pynutaq-1/SpareGpioOutput04',
                                 'ws/rf/pynutaq-1/FdlSwTrigger',
                                 'ws/rf/pynutaq-1/LoopEnableA',
                                 'ws/rf/pynutaq-1/AdcsPhaseshiftEnableA',
                                 'ws/rf/pynutaq-1/DacsPhaseShiftEnableA',
                                 'ws/rf/pynutaq-1/SquarerefEnableA',
                                 'ws/rf/pynutaq-1/FreqsquareA',
                                 'ws/rf/pynutaq-1/ResetkiA',
                                 'ws/rf/pynutaq-1/LookRefA',
                                 'ws/rf/pynutaq-1/QuadrantSelectionA',
                                 'ws/rf/pynutaq-1/SlowIqLoopInputSelection',
                                 'ws/rf/pynutaq-1/FastIqLoopInputSelection',
                                 'ws/rf/pynutaq-1/AmplitudeLoopInputSelection',
                                 'ws/rf/pynutaq-1/PhaseLoopInputSelection',
                                 'ws/rf/pynutaq-1/LoopsInputs',
                                 'ws/rf/pynutaq-1/FastIqLoopEnable',
                                 'ws/rf/pynutaq-1/AmplitudeLoopEnable',
                                 'ws/rf/pynutaq-1/PhaseLoopEnable',
                                 'ws/rf/pynutaq-1/KpFastIqLoop',
                                 'ws/rf/pynutaq-1/KiFastIqLoop',
                                 'ws/rf/pynutaq-1/KpAmpLoop',
                                 'ws/rf/pynutaq-1/KiAmpLoop',
                                 'ws/rf/pynutaq-1/KpPhaseLoop',
                                 'ws/rf/pynutaq-1/KiPhaseLoop',
                                 'ws/rf/pynutaq-1/PiLimitFastPiIq',
                                 'ws/rf/pynutaq-1/PulseModeEnableA',
                                 'ws/rf/pynutaq-1/AutomaticConditioningEnableA',
                                 'ws/rf/pynutaq-1/ConditioningdutyCicleA',
                                 'ws/rf/pynutaq-1/TuningEnableA',
                                 'ws/rf/pynutaq-1/TuningPosEnA',
                                 'ws/rf/pynutaq-1/NumStepsA',
                                 'ws/rf/pynutaq-1/PulsesFrequency',
                                 'ws/rf/pynutaq-1/PhaseOffsetA',
                                 'ws/rf/pynutaq-1/MoveA',
                                 'ws/rf/pynutaq-1/MoveupA',
                                 'ws/rf/pynutaq-1/TuningresetA',
                                 'ws/rf/pynutaq-1/Fwmina',
                                 'ws/rf/pynutaq-1/MarginupA',
                                 'ws/rf/pynutaq-1/MarginlowA',
                                 'ws/rf/pynutaq-1/EpsItckDisable',
                                 'ws/rf/pynutaq-1/FimItckDisable',
                                 'ws/rf/pynutaq-1/MDivider',
                                 'ws/rf/pynutaq-1/NDivider',
                                 'ws/rf/pynutaq-1/Muxsel',
                                 'ws/rf/pynutaq-1/Mux0Divider',
                                 'ws/rf/pynutaq-1/Mux1Divider',
                                 'ws/rf/pynutaq-1/Mux2Divider',
                                 'ws/rf/pynutaq-1/Mux3Divider',
                                 'ws/rf/pynutaq-1/Mux4Divider',
                                 'ws/rf/pynutaq-1/SendWord',
                                 'ws/rf/pynutaq-1/Cpdir',
                                 'ws/rf/pynutaq-1/VcxoOutputInversion',
                        ])

diags_loops = PanelDescription('DiagsLoops',
                        classname = 'TaurusForm',
                        model = [
                                 'ws/rf/pynutaq-1/Diag_IcavLoops',
                                 'ws/rf/pynutaq-1/Diag_QcavLoops',
                                 'ws/rf/pynutaq-1/Diag_Icontrol',
                                 'ws/rf/pynutaq-1/Diag_Qcontrol',
                                 'ws/rf/pynutaq-1/Diag_Icontrol1',
                                 'ws/rf/pynutaq-1/Diag_Qcontrol1',
                                 'ws/rf/pynutaq-1/Diag_Icontrol2',
                                 'ws/rf/pynutaq-1/Diag_Qcontrol2',
                                 'ws/rf/pynutaq-1/Diag_Ierror',
                                 'ws/rf/pynutaq-1/Diag_Qerror',
                                 'ws/rf/pynutaq-1/Diag_Ierroraccum',
                                 'ws/rf/pynutaq-1/Diag_Qerroraccum',
                                 'ws/rf/pynutaq-1/Diag_Iref',
                                 'ws/rf/pynutaq-1/Diag_Qref',
                                 'ws/rf/pynutaq-1/Diag_IFwCavLoops',
                                 'ws/rf/pynutaq-1/Diag_QFwCavLoops',
                                 'ws/rf/pynutaq-1/Diag_IFwTet1Loops',
                                 'ws/rf/pynutaq-1/Diag_QFwTet1Loops',
                                 'ws/rf/pynutaq-1/Diag_IFwTet2Loops',
                                 'ws/rf/pynutaq-1/Diag_QFwTet2Loops',
                                 'ws/rf/pynutaq-1/Diag_IFwCircInLoops',
                                 'ws/rf/pynutaq-1/Diag_QFwCircInLoops',
                                 'ws/rf/pynutaq-1/Diag_Imo',
                                 'ws/rf/pynutaq-1/Diag_Qmo',
                                 'ws/rf/pynutaq-1/Diag_Ispare1',
                                 'ws/rf/pynutaq-1/Diag_Qspare1',
                                 'ws/rf/pynutaq-1/Diag_Ispare2',
                                 'ws/rf/pynutaq-1/Diag_Qspare2',
                                 'ws/rf/pynutaq-1/Diag_IMuxCav',
                                 'ws/rf/pynutaq-1/Diag_QMuxCav',
                                 'ws/rf/pynutaq-1/Diag_IMuxFwCav',
                                 'ws/rf/pynutaq-1/Diag_QMuxFwCav',
                                 'ws/rf/pynutaq-1/Diag_IMuxFwTet1',
                                 'ws/rf/pynutaq-1/Diag_QMuxFwTet1',
                                 'ws/rf/pynutaq-1/Diag_IMuxFwTet2',
                                 'ws/rf/pynutaq-1/Diag_QMuxFwTet2',
                                 'ws/rf/pynutaq-1/Diag_IMuxFwCircIn',
                                 'ws/rf/pynutaq-1/Diag_QMuxFwCircIn',
                                 'ws/rf/pynutaq-1/Diag_AmpCav',
                                 'ws/rf/pynutaq-1/Diag_AmpFw',
                                 'ws/rf/pynutaq-1/Diag_AngCavFw',
                                 'ws/rf/pynutaq-1/Diag_AngCavL',
                                 'ws/rf/pynutaq-1/Diag_AngFwL',
                                 'ws/rf/pynutaq-1/Diag_Vaccum1',
                                 'ws/rf/pynutaq-1/Diag_Vaccum2',
                                 'ws/rf/pynutaq-1/Diag_VcxoPowered',
                                 'ws/rf/pynutaq-1/Diag_VcxoRef',
                                 'ws/rf/pynutaq-1/Diag_VcxoLocked',
                                 'ws/rf/pynutaq-1/Diag_VcxoCableDisconnected',
                                 'ws/rf/pynutaq-1/Diag_TuningOn',
                                 'ws/rf/pynutaq-1/Diag_TuningOnFwMinTuningEnableLatch',
                                 'ws/rf/pynutaq-1/Diag_FreqUp',
                                 'ws/rf/pynutaq-1/Diag_ManualTuningOn',
                                 'ws/rf/pynutaq-1/Diag_ManualTuningFreqUp',
                                 'ws/rf/pynutaq-1/Diag_EpsItckDelay',
                                 'ws/rf/pynutaq-1/Diag_FimItckDelay',
                                 'ws/rf/pynutaq-1/Diag_FdlTrigHwInput',
                                 'ws/rf/pynutaq-1/Diag_FdlTrigSwInput',
                        ])

settings_diags = PanelDescription('SettingsDiags',
                        classname = 'TaurusForm',
                        model = [
                                 'ws/rf/pynutaq-2/Rvtet1',
                                 'ws/rf/pynutaq-2/Rvtet2',
                                 'ws/rf/pynutaq-2/Rvcirc',
                                 'ws/rf/pynutaq-2/Fwload',
                                 'ws/rf/pynutaq-2/Fwhybload',
                                 'ws/rf/pynutaq-2/Rvcav',
                                 'ws/rf/pynutaq-2/ManualInterlock',
                                 'ws/rf/pynutaq-2/DisableItckRvtet1',
                                 'ws/rf/pynutaq-2/DisableItckRvtet2',
                                 'ws/rf/pynutaq-2/DisableItckRvcirc',
                                 'ws/rf/pynutaq-2/DisableItckFwload',
                                 'ws/rf/pynutaq-2/DisableItckFwhybload',
                                 'ws/rf/pynutaq-2/DisableItckRvcav',
                                 'ws/rf/pynutaq-2/DisableItckArcs',
                                 'ws/rf/pynutaq-2/DisableItckVaccum',
                                 'ws/rf/pynutaq-2/DisableItckManualInterlock',
                                 'ws/rf/pynutaq-2/DisableItckPlungerEndSwitchesUp',
                                 'ws/rf/pynutaq-2/DisableItckPlungerEndSwitchesDown',
                                 'ws/rf/pynutaq-2/DisableItckMps',
                                 'ws/rf/pynutaq-2/SamplesToAverage',
                                 'ws/rf/pynutaq-2/PulseupLogicInversion',
                                 'ws/rf/pynutaq-2/EndSwitchesConnectedToNoNcContact',
                                 'ws/rf/pynutaq-2/Lookref',
                                 'ws/rf/pynutaq-2/Quadref',
                                 'ws/rf/pynutaq-2/SpareDo1',
                                 'ws/rf/pynutaq-2/SpareDo2',
                                 'ws/rf/pynutaq-2/SpareDo3',
                                 'ws/rf/pynutaq-2/FdlSwTrigger',
                                 'ws/rf/pynutaq-2/ResetInterlocksCavA',
                                 'ws/rf/pynutaq-2/Landautuningenable',
                                 'ws/rf/pynutaq-2/Landautuningreset',
                                 'ws/rf/pynutaq-2/Movelandauup',
                                 'ws/rf/pynutaq-2/Movelandauplg',
                                 'ws/rf/pynutaq-2/Numsteps',
                                 'ws/rf/pynutaq-2/Landauphaseoffset',
                                 'ws/rf/pynutaq-2/Landaumarginup',
                                 'ws/rf/pynutaq-2/LandauMarginLow',
                                 'ws/rf/pynutaq-2/MinimumLandauAmplitude',
                                 'ws/rf/pynutaq-2/LandauPositiveEnable',
                                 'ws/rf/pynutaq-2/Landauampsetting',
                        ])

diags_diags_ = PanelDescription('DiagsDiags',
                        classname = 'TaurusForm',
                        model = [
                                 'ws/rf/pynutaq-2/Diag_Irvtet1',
                                 'ws/rf/pynutaq-2/Diag_Qrvtet1',
                                 'ws/rf/pynutaq-2/Diag_Amprvtet1',
                                 'ws/rf/pynutaq-2/Diag_Phrvtet1',
                                 'ws/rf/pynutaq-2/Diag_Irvtet2',
                                 'ws/rf/pynutaq-2/Diag_Qrvtet2',
                                 'ws/rf/pynutaq-2/Diag_Amprvtet2',
                                 'ws/rf/pynutaq-2/Diag_Phrvtet2',
                                 'ws/rf/pynutaq-2/Diag_Ifwcirc',
                                 'ws/rf/pynutaq-2/Diag_Qfwcirc',
                                 'ws/rf/pynutaq-2/Diag_Ampfwcirc',
                                 'ws/rf/pynutaq-2/Diag_Phfwcirc',
                                 'ws/rf/pynutaq-2/Diag_Irvcirc',
                                 'ws/rf/pynutaq-2/Diag_Qrvcirc',
                                 'ws/rf/pynutaq-2/Diag_Amprvcirc',
                                 'ws/rf/pynutaq-2/Diag_Phrvcirc',
                                 'ws/rf/pynutaq-2/Diag_Ifwload',
                                 'ws/rf/pynutaq-2/Diag_Qfwload',
                                 'ws/rf/pynutaq-2/Diag_Ampfwload',
                                 'ws/rf/pynutaq-2/Diag_Phfwload',
                                 'ws/rf/pynutaq-2/Diag_Ifwhybload',
                                 'ws/rf/pynutaq-2/Diag_Qfwhybload',
                                 'ws/rf/pynutaq-2/Diag_Ampfwhybload',
                                 'ws/rf/pynutaq-2/Diag_Phfwhybload',
                                 'ws/rf/pynutaq-2/Diag_Irvcav',
                                 'ws/rf/pynutaq-2/Diag_Qrvcav',
                                 'ws/rf/pynutaq-2/Diag_Amprvcav',
                                 'ws/rf/pynutaq-2/Diag_Phrvcav',
                                 'ws/rf/pynutaq-2/Diag_Imo',
                                 'ws/rf/pynutaq-2/Diag_Qmo',
                                 'ws/rf/pynutaq-2/Diag_Ampmo',
                                 'ws/rf/pynutaq-2/Diag_Phmo',
                                 'ws/rf/pynutaq-2/Diag_Ilandau',
                                 'ws/rf/pynutaq-2/Diag_Qlandadu',
                                 'ws/rf/pynutaq-2/Diag_Amplandadu',
                                 'ws/rf/pynutaq-2/Diag_Phlandadu',
                                 'ws/rf/pynutaq-2/Diag_PlungerMovingManualTuning',
                                 'ws/rf/pynutaq-2/Diag_PlungerMovingUpManualTuning',
                                 'ws/rf/pynutaq-2/Diag_PlungerMovingAutomaticTuning',
                                 'ws/rf/pynutaq-2/Diag_PlungerMovingUpAutomaticTuning',
                                 'ws/rf/pynutaq-2/Diag_DephaseMoLandau',
                                 'ws/rf/pynutaq-2/Diag_Rvtet2',
                                 'ws/rf/pynutaq-2/Diag_Rvtet2',
                                 'ws/rf/pynutaq-2/Diag_Rvcirc',
                                 'ws/rf/pynutaq-2/Diag_Fwload',
                                 'ws/rf/pynutaq-2/Diag_Fwhybload',
                                 'ws/rf/pynutaq-2/Diag_Rvcav',
                                 'ws/rf/pynutaq-2/Diag_Arcs',
                                 'ws/rf/pynutaq-2/Diag_Vacuum',
                                 'ws/rf/pynutaq-2/Diag_ManualInterlock',
                                 'ws/rf/pynutaq-2/Diag_ExternalItck',
                                 'ws/rf/pynutaq-2/Diag_PlungerEndSwitchUp',
                                 'ws/rf/pynutaq-2/Diag_PlungerEndSwitchDown',
                                 'ws/rf/pynutaq-2/Diag_Timestamp1',
                                 'ws/rf/pynutaq-2/Diag_Timestamp2',
                                 'ws/rf/pynutaq-2/Diag_Timestamp3',
                                 'ws/rf/pynutaq-2/Diag_Timestamp4',
                                 'ws/rf/pynutaq-2/Diag_Timestamp5',
                                 'ws/rf/pynutaq-2/Diag_Timestamp6',
                                 'ws/rf/pynutaq-2/Diag_Timestamp7',
                                 'ws/rf/pynutaq-2/Diag_DacsDisableCommand',
                                 'ws/rf/pynutaq-2/Diag_PinSwitch',
                                 'ws/rf/pynutaq-2/Diag_FdlTriggerToLoopsdiagboard',
                                 'ws/rf/pynutaq-2/Diag_OutputToPlc',
                                 'ws/rf/pynutaq-2/Diag_OutputToMps',
                                 'ws/rf/pynutaq-2/Diag_LandauMovingLed',
                                 'ws/rf/pynutaq-2/Diag_LandauPulseMotor',
                                 'ws/rf/pynutaq-2/Diag_LandauDirMotor',
                                 'ws/rf/pynutaq-2/Diag_LandayMovingUpLed',
                                 'ws/rf/pynutaq-2/Diag_FdlTriggerForDiagnosticsPurposes',
                                 'ws/rf/pynutaq-2/Diag_SpareDo01',
                                 'ws/rf/pynutaq-2/Diag_SpareDo02',
                                 'ws/rf/pynutaq-2/Diag_SpareDo03',
                        ])


#===============================================================================
# Define custom toolbars to be shown. To define a toolbar, instantiate a
# ToolbarDescription object (see documentation for the gblgui_utils module)
#===============================================================================

# dummytoolbar = ToolBarDescription('Empty Toolbar',
#                         classname = 'QToolBar',
#                         modulename = 'PyQt4.Qt')

#panictoolbar = ToolBarDescription('Panic Toolbar',
#                        classname = 'PanicToolbar',
#                        modulename = 'tangopanic')

#===============================================================================
# Define custom applets to be shown in the applets bar (the wide bar that
# contains the logos). To define an applet, instantiate an AppletDescription
# object (see documentation for the gblgui_utils module)
#===============================================================================

#mon2 = AppletDescription('Dummy Monitor',
#                        classname = 'TaurusMonitorTiny',
#                        model='eval://1000*rand(2)')


#===============================================================================
# Define which External Applications are to be inserted.
# To define an external application, instantiate an ExternalApp object
# See TaurusMainWindow.addExternalAppLauncher for valid values of ExternalApp
#===============================================================================
# xterm = ExternalApp(cmdargs=['xterm','spock'], text="Spock", icon='utilities-terminal')
# hdfview = ExternalApp(["hdfview"])
# pymca = ExternalApp(['pymca'])

#===============================================================================
# Macro execution configuration
# Comment out or make MACRO_SERVER=None or set MACRO_PANELS=False to skip
# creating a macro execution infrastructure.
# Give empty strings if you want to select the values manually in the GUI
#===============================================================================
#MACROSERVER_NAME =
#DOOR_NAME =
#MACROEDITORS_PATH =

#===============================================================================
# Monitor widget (This is *obsolete* now, you can get the same result defining a
# custom applet with classname='TaurusMonitorTiny')
#===============================================================================
# MONITOR = ['sys/tg_test/1/double_scalar_rww']

#===============================================================================
# Adding other widgets to the catalog of the "new panel" dialog.
# pass a tuple of (classname,screenshot)
# -classname may contain the module name.
# -screenshot can either be a file name relative to the application dir or
# a resource URL or None
#===============================================================================
EXTRA_CATALOG_WIDGETS = [('PyQt4.Qt.QLineEdit',':/taurus.png'),
                        ('PyQt4.Qt.QSpinBox','images/syn2.jpg'),
                        ('PyQt4.Qt.QTextEdit','/tmp/kk.png'),
                        ('PyQt4.Qt.QLabel',None)]

#===============================================================================
# Define one or more embedded consoles in the GUI.
# Possible items for console are 'ipython', 'tango', 'spock'
# Note: This is still experimental
#===============================================================================
#CONSOLE = ['tango']