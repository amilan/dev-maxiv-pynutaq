#!/usr/bin/env python

###############################################################################
#     Code generator for the generation of the device servers.
#
#     Copyright (C) 2013  Max IV Laboratory, Lund Sweden
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see [http://www.gnu.org/licenses/].
###############################################################################

__author__ = 'antmil'

import argparse
import csv

from jinja2 import Environment, PackageLoader

#attributes_list = [attribute1, attribute2]
# ''.join([i.capitalize() for i in name.split('_')])


EXCLUDED_IQ_ATTRIBUTES = [
    'polarforamplitudeloop',
    'polarforphaseloop',
]

def create_new_attribute_dict(name, attribute_type, units):
    """attribute type must be {amp|ph}"""

    if name not in EXCLUDED_IQ_ATTRIBUTES:

        if attribute_type == 'amp':
            attr_name = 'Amp{0}'.format(name.capitalize())

        elif attribute_type == 'ph':
            attr_name = 'Ph{0}'.format(name.capitalize())

        else:
            raise Exception('Wrong type of attribute')

        i_parent = 'I{0}'.format(name)
        q_parent = 'Q{0}'.format(name)

        attr = {
            'address': '',
            'name': attr_name,
            'access': 'read_diag_{0}'.format(attribute_type),
            'dtype': 'float',
            'type': units,
            'min_value': '',
            'max_value': '',
            'i_parent': i_parent,
            'q_parent': q_parent
        }
        return attr
    else:
        return None


def get_extended_list_of_attributes(attributes_list):
    import collections

    # Get list of I,Q attributes and remove the I,Q from the name
    my_list = [x['name'][1::] for x in attributes_list if x['name'].startswith('I') or x['name'].startswith('Q')]

    # Look for the I,Q pairs of attributes and keep only the common defining part of the name.
    list_of_items = [x for x, y in collections.Counter(my_list).items() if y == 2 and x.lower() not in EXCLUDED_IQ_ATTRIBUTES]

    # Create a list of Amp, Ph attributes
    # amp_list = ['Amp{0}'.format(x.capitalize()) for x in list_of_items]
    # ph_list = ['Ph{0}'.format(x.capitalize()) for x in list_of_items]

    # Create the list of dicts with the info for each attribute
    # amp_list_of_dicts = map(lambda x: create_new_attribute_dict(x, 'amp', 'mv'), amp_list)
    # ph_list_of_dicts = map(lambda x: create_new_attribute_dict(x, 'ph', 'angle'), ph_list)

    amp_list_of_dicts = map(lambda x: create_new_attribute_dict(x, 'amp', 'mv'), list_of_items)
    ph_list_of_dicts = map(lambda x: create_new_attribute_dict(x, 'ph', 'angle'), list_of_items)

    # Concatenate the three lists
    new_attributes_extended_list = attributes_list + amp_list_of_dicts + ph_list_of_dicts

    return new_attributes_extended_list


def _create_attributes_for_both_cavities(attributes_list):
    final_attributes_list = []
    for attr in attributes_list:
        temp_attr = attr.copy()
        temp_attr['name'] = attr['name']+'B'
        temp_attr['cavity'] = 'B'

        attr['name'] += 'A'
        attr['cavity'] = 'A'

        final_attributes_list.append(attr)
        final_attributes_list.append(temp_attr)

    return final_attributes_list

def generate_code(input_filename_loops, input_filename_diags, output_filename, nutaq_type):

    def _extract_data_from_csv(input_filename):
        with open(input_filename, 'rU') as fd:
            attributes_list = list(csv.DictReader(fd, delimiter=';'))

        for attr in attributes_list:
            attr['name'] = ''.join([a.capitalize() for a in attr['name'].replace('_', ' ').replace('-',' ').split()])

        #for attr in attributes_list:
        #    attr['name'] = ''.join([a.capitalize() for a in attr['name'].split('_')])
        return attributes_list

    # Extract data from csv
    attributes_loops = _extract_data_from_csv(input_filename_loops)
    attributes_diags = _extract_data_from_csv(input_filename_diags)

    # Get attributes for cavity A and cavity B
    attributes_loops = _create_attributes_for_both_cavities(attributes_loops)
    attributes_diags = _create_attributes_for_both_cavities(attributes_diags)

    # Extend list of attributes
    attributes_diags = get_extended_list_of_attributes(attributes_diags)

    # Prepare environment
    env = Environment(loader=PackageLoader('codegenerator', 'templates'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('methods.j2')

    # Code Generation
    output = template.render(attributes=attributes_loops, diags_attributes=attributes_diags, nutaq_type=nutaq_type)

    # Write files
    fd = open(output_filename, 'w')
    fd.write(output)
    fd.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename_loops', help='Input Filename from where to extract the data')
    parser.add_argument('input_filename_diags', help='Input Filename from where to extract the data')
    parser.add_argument('output_filename', help='Filename for generated file')
    parser.add_argument('nutaq_type', help='Nutaq type: {loops | diags}')
    args = parser.parse_args()

    generate_code(args.input_filename_loops, args.input_filename_diags, args.output_filename, args.nutaq_type)
