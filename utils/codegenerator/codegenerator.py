# -*- coding: utf-8 -*-

__author__ = 'antmil'

import argparse
import csv

from jinja2 import Environment, PackageLoader

#attributes_list = [attribute1, attribute2]
# ''.join([i.capitalize() for i in name.split('_')])

def generate_code(input_filename_loops, input_filename_diags, output_filename):

    def _extract_data_from_csv(input_filename):
        with open(input_filename, 'rU') as fd:
            attributes_list = list(csv.DictReader(fd, delimiter=';'))

        for attr in attributes_list:
            attr['name'] = ''.join([a.capitalize() for a in attr['name'].replace('_', ' ').split()])

        #for attr in attributes_list:
        #    attr['name'] = ''.join([a.capitalize() for a in attr['name'].split('_')])
        return attributes_list

    attributes_loops = _extract_data_from_csv(input_filename_loops)
    attributes_diags = _extract_data_from_csv(input_filename_diags)
    env = Environment(loader=PackageLoader('codegenerator', 'templates'), trim_blocks=True, lstrip_blocks=True )
    template = env.get_template('methods.j2')
    output = template.render(attributes=attributes_loops, diags_attributes=attributes_diags)
    fd = open(output_filename, 'w')
    fd.write(output)
    fd.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename_loops', help='Input Filename from where to extract the data')
    parser.add_argument('input_filename_diags', help='Input Filename from where to extract the data')
    parser.add_argument('output_filename', help='Filename for generated file')
    args = parser.parse_args()

    generate_code(args.input_filename_loops, args.input_filename_diags, args.output_filename)