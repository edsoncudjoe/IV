#! /usr/local/bin python
###############################################################################
#
# Name: cdvtxt2xlsx.py
# Objective: Converts CatDV output file to an excel worksheet.
# Date: 25/11/14
# Author: E.Cudjoe
#
# Inputs: CatDV .txt document
# Output: .xlsx document 
#
#------------------------------------------------------------------------------
#
# Version 1.0
#       Initial Build
#
###############################################################################

import sys
import xlsxwriter

collection = []
cdvfile = sys.argv[1]
row = 1
col = 0


with open(cdvfile, 'r') as data:
    for d in data:
        if d.startswith('IV'):
            d = d.split()
            collection.append(d)
            
# new spreadsheet
filename = raw_input("Enter name to save spreadsheet as: ")
workbook = xlsxwriter.Workbook(
    '/Users/Edit4/Desktop/Imported and archived/{}.xlsx'.format(filename))
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})

#headers
worksheet.write('A1', 'Tape Numbers', bold)
worksheet.write('B1', 'Name', bold)
worksheet.set_column('A:A', 20)
worksheet.set_column('B:B', 100)
# get data from list
for item in collection:
    if len(item) > 2:
        worksheet.write(row, col, item[0])
        spaced_items = item[1:]
        joined_items = '_'.join(spaced_items)
        worksheet.write(row, col + 1, joined_items)
        row += 1
    else:
        worksheet.write(row, col, item[0])
        worksheet.write(row, col + 1, item[1])
        row += 1
    
workbook.close()
