#!/usr/bin/env python
#
# Rough and ready report PDF from summary csv

import pandas
import argparse
from fpdf import FPDF

# Parse arguments
parser = argparse.ArgumentParser(description='Report PDF from summary csv')
parser.add_argument('-i', '--incsv', help='Input CSV file')
parser.add_argument('-o', '--outpdf', help='Output PDF file')
args = parser.parse_args()

# Load summary CSV and prettyprint with pandas
csv=pandas.read_csv(args.incsv)
pandas.set_option('display.max_colwidth',100)
print(csv.loc[:,('Condition','PctAccuracy','MeanCorrectRTms','MedianCorrectRTms')])
print(csv.loc[:,('Condition','OnsetsSec')])
print(csv.loc[:,('Condition','DurationsSec')])
print(csv.loc[:,('Condition','Accuracy')])
print(csv.loc[:,('Condition','RTms')])


#pdf = FPDF()
#pdf.add_page()
#pdf.set_font('Courier', size = 9)
#f = open(args.incsv, 'r')
#for line in f:
#	x = line.encode("latin1","ignore").decode("latin1")
#	pdf.multi_cell(193, 5, txt = x)
#pdf.output(args.outpdf)

