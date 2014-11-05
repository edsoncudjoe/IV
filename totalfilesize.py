#####################################################################
#
# Name: totalfilesize.py
# Date: 04112014
# Author: E.Cudjoe
#
# Purpose: Gathers the file sizes from a CatDV .txt 
#			output and calculates the total size.
# 
# Inputs: Filename
# Outputs: Total file size in terabytes and gigabytes.
#####################################################################

import re
import sys

#def Main():
file = sys.argv[1]
if file.endswith('.txt'):
	data = open(sys.argv[1]).read()

	# Separate MB values from GB values
	m = re.findall(r'\t(\d*.\d*)\sMB\r', data)
	g = re.findall(r'\t(\d*.\d*)\sGB\r', data)

	mega = [float(item) for item in m]
	giga = [float(item) for item in g]

	totalgigs = sum(mega) / 1000 + sum(giga)
	tera = totalgigs / 1000

	print('total GB: {0:,.2f}GB'.format(totalgigs))
	print('total TB: {0:.2f}TB'.format(tera))
	start = False
else:
	print('Please use a \'.txt\' file.')
		
#if __name__ == '__main__':
#	Main()