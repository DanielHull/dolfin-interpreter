
from dolfinParser import *
from graphicalInterpretation import GraphInterpreter

# Future CLI tool development
DESC = 'CLI tool for parsing and handling data outputs of dolfin scripts'
USAGE = \
    "Basic Usage:" \
    "file_name file to find all spectrum and fluorescence data in addition to other experimental fields" \
    "file_loc pathway to access file" \
    "--new_name (opt) (str) how you want to save the output file"

import argparse
parser = argparse.ArgumentParser(description=DESC, usage=USAGE)
parser.add_argument('file_name', type=str)
parser.add_argument('file_loc', type=str)
parser.add_argument('--offset', nargs='+', default=[], help= '(O,int) selection of which droplets you want to grab"')
parser.add_argument('--blank_label', type=str, default='blank_')
parser.add_argument('--drop_label', type=str, default='drop_')
parser.add_argument('--start_number', type=int, default=1)
parser.add_argument('--normalization_factor', type=float, default=1.0)
parser.add_argument('--output_name', type=str)
parser.add_argument('--end_number', type=int, default=8)
parser.add_argument('--save_loc', type=str, default='C:\Users\dhull\Documents\code_directory\dolfininterpreter\\test')
parser.add_argument('--merge_label', type=str, default='Merge ')

args = parser.parse_args()

with open('kinetic.log', 'w'):
    pass
import logging
logging.basicConfig(format='%(asctime)s %(message)s', \
                    filename='kinetic.log', level=logging.DEBUG, datefmt='%I:%M:%S %p')
# Gives user ability to set file name of their choice, if not default to the original file name
if not args.output_name:
    output_name = args.file_name.split('.')[0]
else:
    output_name = args.output_name
# gives user ability to control the detections they want the kinetic analysis to happen on
if args.offset:
    offsets = [int(i) for i in args.offset]
else:
    offsets = args.offset

my_filter = {'Absorbance': [], 'Fluorescence': [], "Time": ['start_time', 'end_time']}
blank_filter = {}
for i in range(args.start_number,args.end_number+1):
    my_filter['Time'].extend([args.merge_label + str(i)])
    my_filter['Fluorescence'].extend([args.drop_label+str(i), args.blank_label+str(i)])
    blank_filter[args.drop_label+str(i)] = [args.blank_label+str(i),args.merge_label+str(i)]

do = dolfinParser(args.file_name, my_filter, args.file_loc, args.normalization_factor)
do.get_id_info()
do.get_blank_subtracted_vals(blank_filter, offsets)
gI = GraphInterpreter(do, args.save_loc, output_name)
gI.plot_spectrums()
gI.export_data()
