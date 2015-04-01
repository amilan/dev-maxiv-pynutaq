# -*- coding: utf-8 -*-

__author__ = 'antmil'

from jinja2 import Environment, PackageLoader
attributes_dict = {
                    "attribute1": {"name": "phase_shift_fw_cav",
                                   "label": 'PhaseShiftFwCav',
                                   "dtype": "float",
                                   "display_level": "DispLevel.OPERATOR",
                                   "access": "AttrWriteType.READ_WRITE",
                                   "unit": "degrees", "format": "6.4f",
                                   "min_value": -180.0, "max_value": 360.0,
                                   "fget": "get_phase_shift_fw_cav",
                                   "fset": "set_phase_shift_fw_cav",
                                   "doc": "",
                                   "type": "milivolts",
                                   "address": 1
                                  },

                    "attribute2": {"name": "phase_shift_fw",
                                   "label": 'PhaseShiftFwCav',
                                   "dtype": "float",
                                   "display_level": "DispLevel.OPERATOR",
                                   "access": "AttrWriteType.READ_WRITE",
                                   "unit": "degrees", "format": "6.4f",
                                   "min_value": -180.0, "max_value": 360.0,
                                   "fget": "get_phase_shift_fw_cav",
                                   "fset": "set_phase_shift_fw_cav",
                                   "doc": "",
                                   "type": "angle",
                                   "address": 2
                                   },

                    "attribute3": {"name": "loop_enable",
                                   "label": 'PhaseShiftFwCav',
                                   "dtype": "float",
                                   "display_level": "DispLevel.OPERATOR",
                                   "access": "AttrWriteType.READ_WRITE",
                                   "unit": "degrees", "format": "6.4f",
                                   "min_value": -180.0, "max_value": 360.0,
                                   "fget": "get_phase_shift_fw_cav",
                                   "fset": "set_phase_shift_fw_cav",
                                   "doc": "",
                                   "type": "bool",
                                   "address": 3
                                   },
                    }

#attributes_list = [attribute1, attribute2]

def print_my_template():
    # Template part
    env = Environment(loader=PackageLoader('codegenerator', 'templates'), trim_blocks=True, lstrip_blocks=True )
    template = env.get_template('methods.j2')
    print template.render(attributes=attributes_dict)

if __name__ == '__main__':
    print_my_template()