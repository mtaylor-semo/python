#! /usr/bin/env python
#from __future__ import print_function

import os
import glob
import csv
import openpyxl # from https://pythonhosted.org/openpyxl/ or PyPI (e.g. via pip)

for csvfile in glob.glob(os.path.join('.', '*.csv')):
 #   csx = os.path.splitext(csvfile)[0]
    wb = openpyxl.Workbook()
    ws = wb.active
    with open(csvfile, 'rU') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader, start=0):
            for c, val in enumerate(row, start=0):
                ws.cell(row=r, column=c).value = val
    wb.save(os.path.splitext(csvfile)[0] + '.xlsx')