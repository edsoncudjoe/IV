#!/usr/bin/env python

# Collects IV barcode numbers from CatDV + data usage from GBlabs file history export data.
# The input files are usually created with data from the past month. 
# This script provides the option to output the barcode names and file sizes as a csv file.
# It can also print the amount of data in TB that has been written to LTO tape.
# 
#
# Input: GBLabs 'history.csv' file. Used to draw the IV barcode numbers and size of each LTO tape.
# Input: Separate lists of all IV LTO barcode numbers for each IV client (NGTV, Power etc..) 
# Output: .csv file for past month  which details the IV barcode number plus its size in terabytes.

#__author__ = "Edson Cudjoe"
#__version__ = "1.0.0"
#__email__ = "edson@intervideo.co.uk"
#__status__ = "Development"
# Date: 4 February 2015
#
#
import csv
import re
import sys

def byte2TB(byte):
	"""Converts input number from bytes to terabytes"""
	try:	
		f = float(byte)
		tb = ((((f / 1024) / 1024) / 1024) / 1024)
		return tb
	except ValueError:
		print("Value could not be converted to float. {}".format(str(byte)))

def get_CatDV_data(textfile):
	"""Opens text file from CatDV containing IV barcodes and outputs these barcodes into a list"""
	catdv_list = []
	with open(textfile) as client_barcodes:
		reader = csv.reader(client_barcodes)
		for row in reader:
			catdv_list.append(row[0])
	return catdv_list

def make_csv_file(final):
	"""Input: The IV barcodes and size in TB. Output: a csv file to be used with Excel."""
	fname = raw_input('Enter name of csv file to save into: ')
	with open(fname, 'wb') as csvfile:
		writedata = csv.writer(csvfile, delimiter=',')
		for i in range(len(final)):
			writedata.writerow(final[i])
	print('File has been created.')
    
def lto_to_list(data):
	"""Takes the output of CSV reader as input. converts this data into a list
	to be compared with the individual client barcode lists generated from 
	CatDV data."""
	collect = []
	final = []
	for item in data:
		try:
			collect.append((item[0], item[6])) # add IV name and size to list	
		except:
			print('Unable to add data: {}'.format(item))
			continue
	for c in collect:
		if 'Name' in c[0]:
			final.append(c)
		else:
			if 'test' in c[0]:
				continue
			#1 file has been labelled incorrectly.
			# It will be temporarily skipped until the tape has been fixed.
			elif 'Intervideo' in c[0]:
				continue
			else:
				gb = byte2TB(c[1])
				a = re.search(r'(IV\d\d\d\d)', c[0])
				final.append((str(a.group()), round(gb, 2)))
	return final

def get_client_items(name_size, clientlist):
	"""Separates main list for each client"""
	client_mnth = []
	for p in sorted(clientlist):
		for i in sorted(name_size):
			if i[0] in p:
				client_mnth.append(i)
	return client_mnth

def get_storage_size(client_items):
	"""Sum of disc size for each tape"""
	count = 0
	for i in client_items:
		count += i[1]
	return count


def Main():
	try:
		# lists of current IV barcodes for each client.
		ng_list = set(get_CatDV_data('ngtv2015.txt'))
		power_list = set(get_CatDV_data('power2015.txt'))
		classic_list = set(get_CatDV_data('classicmedia.txt'))

		# Open current LTO data file from Space
		try:
			fname = sys.argv[1]
			lto_file = open(fname)
			data = csv.reader(lto_file)  
		except:
			raise UnboundLocalError
		 
		# Collection of all tapes written
		name_size = lto_to_list(data)

		# Separate LTO Barcodes by client
		ng = get_client_items(name_size, ng_list)
		pw = get_client_items(name_size, power_list)
		cl = get_client_items(name_size, classic_list)

		# Storage size in TB for client
		ng_tb = get_storage_size(ng)
		pw_tb = get_storage_size(pw)
		cl_tb = get_storage_size(cl)

		print('{}TB written for NGTV\n{}TB written for Power\n{}TB written for'
			'Classic Media/Dreamworks\n'.format(ng_tb, pw_tb, cl_tb))
		create_csv = raw_input(
			'Do you wish to write the months archived tape barcodes + sizes to a csv file? [y/n]: ')
		if create_csv == 'y':
			make_csv_file(name_size)
		else:
			print('You have chosen not to write to a csv file.')

	except UnboundLocalError:
		print('\nNo file has been submitted or the file does not exist.\n'
			'Check that the \'.csv\' file has been saved and reopen this script\n' 
			'along with the filename.')	
	finally:
		try:
			lto_file.close()
		except UnboundLocalError: 
			print('\nUnable to close file.')

if __name__ == '__main__':
	Main()
