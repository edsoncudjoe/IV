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

def Main():
	file = sys.argv[1]
	if file.endswith('.txt'):
		data = open(sys.argv[1]).read()

		# Separate MB values from GB values
		megb = re.findall(r'\t(\d*.\d*)\sMB\r', data)
		gigb = re.findall(r'\t(\d*.\d*)\sGB\r', data)

		mg = [float(m) for m in megb]
		gg = [float(g) for g in gigb]

	#	Add to separate collections	
	#	mg, gg = zip(*[(float(mg), float(gg)) for mg, gg in zip(megb, gigb)])

		totalgigs = sum(mg) / 1000 + sum(gg)
		tera = totalgigs / 1000

		# Select output in Terabytes or Gigabytes
		output = raw_input(
			'Select \'T\' for terabytes or \'G\' for gigabytes:\n').lower()
		if output == 't':
			print('Total TB: {0:.2f}TB'.format(tera))
		elif output == 'g':
			print('Total GB: {0:,.2f}GB'.format(totalgigs))
		else:
			print('Total TB: {0:.2f}TB'.format(tera))
	else:
		print('Please use a \'.txt\' file.')
		
if __name__ == '__main__':
	Main()