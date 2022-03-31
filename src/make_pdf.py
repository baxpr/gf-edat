#!/usr/bin/env python3
#
# Rough and ready report PDF from summary csv

import datetime
import io
import pandas
import argparse
from fpdf import FPDF

# Parse arguments
parser = argparse.ArgumentParser(description='Report PDF from summary csv')
parser.add_argument('--incsv',help='Input CSV file',required=True)
parser.add_argument('--outpdf',help='Output PDF file',required=True)
parser.add_argument('--project',default='NO_PROJ')
parser.add_argument('--subject',default='NO_SUBJ')
parser.add_argument('--session',default='NO_SESS')
parser.add_argument('--scan',default='NO_SCAN')
parser.add_argument('--task',default='NO_TASK')
args = parser.parse_args()

# Load CSV and get pandas' display summaries of it into a string
csv=pandas.read_csv(args.incsv)
pandas.set_option('display.max_colwidth',80)
f = io.StringIO()
print('%s: %s %s %s %s\n' % (args.task,args.project,args.subject,args.session,args.scan),file=f)
print(datetime.datetime.now(),file=f)
print('\n\n',file=f)
print(csv.loc[:,('Condition','PctAccuracy','MeanCorrectRTms','MedianCorrectRTms','MinCorrectRTms','MaxCorrectRTms')],file=f)
print('\n',file=f)
print(csv.loc[:,('Condition','OnsetsSec')],file=f)
print('\n',file=f)
print(csv.loc[:,('Condition','DurationsSec')],file=f)
print('\n',file=f)
print(csv.loc[:,('Condition','Accuracy')],file=f)
print('\n',file=f)
print(csv.loc[:,('Condition','RTms')],file=f)
    
print(f.getvalue())


pdf = FPDF()
pdf.add_page()
pdf.set_font('Courier', size = 7)
pdf.multi_cell(193, 3, txt = f.getvalue())
pdf.output(args.outpdf)

