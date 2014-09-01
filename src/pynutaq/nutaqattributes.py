from PyTango import AttrQuality, AttrWriteType, DispLevel
from PyTango.server import attribute

__author__ = 'antmil'

attributes_dict = {
    "phase_shift_cav": attribute(label='PhaseShiftCav', dtype=float, display_level=DispLevel.OPERATOR,
                                 access=AttrWriteType.READ_WRITE, unit="degrees", format="6.4f",
                                 min_value=-180.0, max_value=360.0,
                                 fget="get_phase_shift_cav", fset="set_phase_shift_cav",
                                 doc=""
                                 ),

    "phase_shift_fw_cav": attribute(label='PhaseShiftFwCav',
                                    dtype=float,
                                    display_level=DispLevel.OPERATOR,
                                    access=AttrWriteType.READ_WRITE,
                                    unit="degrees", format="6.4f",
                                    min_value=-180.0, max_value=360.0,
                                    fget="get_phase_shift_fw_cav",
                                    fset="set_phase_shift_fw_cav",
                                    doc=""
                                    ),

    "phase_shift_fw_tet1": attribute(label='PhaseShiftFwTet1',
                                     dtype=float,
                                     display_level=DispLevel.OPERATOR,
                                     access=AttrWriteType.READ_WRITE,
                                     unit="degrees", format="6.4f",
                                     min_value=-180.0, max_value=360.0,
                                     fget="get_phase_shift_fw_tet1",
                                     fset="set_phase_shift_fw_tet1",
                                     doc=""
                                     ),

    "amp_ref_in": attribute(label='AmpRefIn',
                            dtype=float,
                            display_level=DispLevel.OPERATOR,
                            access=AttrWriteType.READ_WRITE,
                            unit="mV", format="6.4f",
                            fget="get_amp_ref_in",
                            fset="set_amp_ref_in",
                            doc=""
                            ),

    "phase_ref_in": attribute(label='PhaseRefIn',
                              dtype=float,
                              display_level=DispLevel.OPERATOR,
                              access=AttrWriteType.READ_WRITE,
                              unit="degrees", format="6.4f",
                              fget="get_phase_ref_in",
                              fset="set_phase_ref_in",
                              doc=""
                              ),

    "loop_enable": attribute(label='LoopEnable',
                             dtype=bool,
                             display_level=DispLevel.OPERATOR,
                             access=AttrWriteType.READ_WRITE,
                             unit="", format="6.4f",
                             fget="get_loop_enable",
                             fset="set_loop_enable",
                             doc=""
                             ),

    "loop_input_selection": attribute(label='LoopInputSelection',
                                      dtype=int,
                                      display_level=DispLevel.OPERATOR,
                                      access=AttrWriteType.READ_WRITE,
                                      unit="", format="6.4f",
                                      fget="get_loop_input_selection",
                                      fset="set_loop_input_selection",
                                      doc="Enumeration: [0 --> CavVolt, " +
                                          "1 --> FwCav, 2 --> FwTet1, 3 --> FwTet2, 4 --> FwCircIn]"
                                      ),

    "tuning_enable": attribute(label='TuningEnable',
                               dtype=bool,
                               display_level=DispLevel.OPERATOR,
                               access=AttrWriteType.READ_WRITE,
                               unit="", format="6.4f",
                               fget="get_tuning_enable",
                               fset="set_tuning_enable",
                               doc=""
                               ),

    "num_steps": attribute(label='NumSteps',
                           dtype=float,
                           display_level=DispLevel.OPERATOR,
                           access=AttrWriteType.READ_WRITE,
                           unit="", format="6.4f",
                           fget="get_num_steps",
                           fset="set_num_steps",
                           doc=""
                           ),

    "phase_offset": attribute(label='PhaseOffset',
                              dtype=float,
                              display_level=DispLevel.OPERATOR,
                              access=AttrWriteType.READ_WRITE,
                              unit="degree", format="6.4f",
                              fget="get_phase_offset",
                              fset="set_phase_offset",
                              doc=""
                              ),

    "move": attribute(label='move',
                      dtype=bool,
                      display_level=DispLevel.OPERATOR,
                      access=AttrWriteType.READ_WRITE,
                      unit="", format="6.4f",
                      fget="get_move",
                      fset="set_move",
                      doc=""
                      ),

    "move_up": attribute(label='moveUp',
                         dtype=bool,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ_WRITE,
                         unit="", format="6.4f",
                         fget="get_move_up",
                         fset="set_move_up",
                         doc=""
                         ),

    "tuning_reset": attribute(label='TuningReset',
                              dtype=bool,
                              display_level=DispLevel.OPERATOR,
                              access=AttrWriteType.READ_WRITE,
                              unit="", format="6.4f",
                              fget="get_tuning_reset",
                              fset="set_tuning_reset",
                              doc=""
                              ),

    "icav_loops": attribute(label='ICavLoops',
                            dtype=float,
                            display_level=DispLevel.OPERATOR,
                            access=AttrWriteType.READ,
                            unit="mV", format="6.4f",
                            doc=""
                            ),

    "qcav_loops": attribute(label='QCavLoops',
                            dtype=float,
                            display_level=DispLevel.OPERATOR,
                            access=AttrWriteType.READ,
                            unit="mV", format="6.4f",
                            doc=""
                            ),

    "icontrol": attribute(label='IControl',
                          dtype=float,
                          display_level=DispLevel.OPERATOR,
                          access=AttrWriteType.READ,
                          unit="mV", format="6.4f",
                          doc=""
                          ),

    "qcontrol": attribute(label='QControl',
                          dtype=float,
                          display_level=DispLevel.OPERATOR,
                          access=AttrWriteType.READ,
                          unit="mV", format="6.4f",
                          doc=""
                          ),

    "ierror": attribute(label='IError',
                        dtype=float,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ,
                        unit="mV", format="6.4f",
                        doc=""
                        ),

    "qerror": attribute(label='QError',
                        dtype=float,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ,
                        unit="mV", format="6.4f",
                        doc=""
                        ),

    "ifw_cav_loops": attribute(label='IFWCavLoops',
                               dtype=float,
                               display_level=DispLevel.OPERATOR,
                               access=AttrWriteType.READ,
                               unit="mV", format="6.4f",
                               doc=""
                               ),

    "qfw_cav_loops": attribute(label='QFwCavLoops',
                               dtype=float,
                               display_level=DispLevel.OPERATOR,
                               access=AttrWriteType.READ,
                               unit="mV", format="6.4f",
                               doc=""
                               ),

    "ifw_tet1_loops": attribute(label='IFwTet1Loops',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="mV", format="6.4f",
                                doc=""
                                ),

    "qfw_tet1_loops": attribute(label='QFwTet1Loops',
                                dtype=float,
                                display_level=DispLevel.OPERATOR,
                                access=AttrWriteType.READ,
                                unit="mV", format="6.4f",
                                doc=""
                                ),

    "amp_cav": attribute(label='AmpCav',
                         dtype=float,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ,
                         unit="mV", format="6.4f",
                         doc=""
                         ),

    "amp_fw": attribute(label='AmpFw',
                        dtype=float,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ,
                        unit="mV", format="6.4f",
                        doc=""
                        ),

    "ang_cav_fw": attribute(label='AngCavFw',
                            dtype=float,
                            display_level=DispLevel.OPERATOR,
                            access=AttrWriteType.READ,
                            unit="degrees", format="6.4f",
                            doc=""
                            ),

    "ang_cav_l": attribute(label='AngCavL',
                           dtype=float,
                           display_level=DispLevel.OPERATOR,
                           access=AttrWriteType.READ,
                           unit="degrees", format="6.4f",
                           doc=""
                           ),

    "ang_fw_l": attribute(label='AngFwL',
                          dtype=float,
                          display_level=DispLevel.OPERATOR,
                          access=AttrWriteType.READ,
                          unit="degrees", format="6.4f",
                          doc=""
                          ),

    "ispare": attribute(label='ISpare',
                        dtype=float,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ,
                        unit="mV", format="6.4f",
                        doc=""
                        ),

    "qspare": attribute(label='QSpare',
                        dtype=float,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ,
                        unit="mV", format="6.4f",
                        doc=""
                        ),

    "amp_spare": attribute(label='AmpSpare',
                           dtype=float,
                           display_level=DispLevel.OPERATOR,
                           access=AttrWriteType.READ,
                           unit="mV", format="6.4f",
                           doc=""
                           ),

    "phase_spare": attribute(label='PhaseSpare',
                             dtype=float,
                             display_level=DispLevel.OPERATOR,
                             access=AttrWriteType.READ,
                             unit="mV", format="6.4f",
                             doc=""
                             ),
}
