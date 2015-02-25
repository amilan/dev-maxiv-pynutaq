#!/usr/bin/env python

###############################################################################
##     Code generator for the generation of the device servers. 
##
##     Copyright (C) 2013  Max IV Laboratory, Lund Sweden
##
##     This program is free software: you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation, either version 3 of the License, or
##     (at your option) any later version.
##
##     This program is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.
##
##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see [http://www.gnu.org/licenses/].
###############################################################################

__author__ = 'antmil'

import argparse
import csv

from jinja2 import Environment, PackageLoader

#attributes_list = [attribute1, attribute2]
# ''.join([i.capitalize() for i in name.split('_')])

def generate_code(input_filename_loops, input_filename_diags, output_filename, nutaq_type):

    def _extract_data_from_csv(input_filename):
        with open(input_filename, 'rU') as fd:
            attributes_list = list(csv.DictReader(fd, delimiter=';'))

        for attr in attributes_list:
            attr['name'] = ''.join([a.capitalize() for a in attr['name'].replace('_', ' ').replace('-',' ').split()])

        #for attr in attributes_list:
        #    attr['name'] = ''.join([a.capitalize() for a in attr['name'].split('_')])
        return attributes_list

    attributes_loops = _extract_data_from_csv(input_filename_loops)
    attributes_diags = _extract_data_from_csv(input_filename_diags)
    env = Environment(loader=PackageLoader('codegenerator', 'templates'), trim_blocks=True, lstrip_blocks=True )
    template = env.get_template('methods.j2')
    output = template.render(attributes=attributes_loops, diags_attributes=attributes_diags, nutaq_type=nutaq_type)
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
