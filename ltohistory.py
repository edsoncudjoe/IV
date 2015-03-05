#!/usr/bin/env python

# Collects IV barcode numbers from CatDV + data usage from GBlabs file history export data.
# The input files are usually created with data from the past month. 
# This script provides the option to output the barcode names and file sizes as a csv file.
# It can also print the amount of data in TB that has been written to LTO tape.
# 
# 
# Input: GBLabs 'history' file. Both CSV and JSON files can be used as input. 
#			The program will collect the Intervideo barcode numbers and size of
#			 each LTO tape from these files. 
# Input: Choice of using data from the CatDV API or text files that will have
#		 to be manually created using the export option within CatDV. 
#		The text files are separate lists of all IV LTO barcode numbers for
#		 each Intervideo client (NGTV, Power etc..). 
# Output: CSV file which details the Intervideo barcode numbers plus the tape size in terabytes.

__author__ = "Edson Cudjoe"
__version__ = "1.0.0"
__email__ = "edson@intervideo.co.uk"
__status__ = "Development"
__date__ = "4 February 2015"


import csv
import re
import sys
import time
import json
from CatDVlib import Cdvlib

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
	name_ext = fname + ".csv"
	with open(name_ext, 'wb') as csvfile:
		writedata = csv.writer(csvfile, delimiter=',')
		for i in range(len(final)):
			writedata.writerow(final[i])
	print('File has been created.')
    
def lto_to_list(data):
	"""
	Takes the output of CSV reader as input. converts this data into a list
	to be compared with the individual client barcode lists generated from 
	CatDV data.
	"""
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
				gb = byte2TB(c[1]) # converts GB byte data to TB
				a = re.search(r'(IV\d\d\d\d)', c[0]) #removes unicode from IV numbers
				final.append((str(a.group()), round(gb, 2))) 
	return final

# retrieve data from GBlabs JSON output
def get_json(submitted):
	lto = open(submitted, 'r')
	jfile = json.load(lto)
	return jfile

def json_to_list(json):
	json_collect = []
	for i in json['tapes']:
		json_collect.append((i['name'], i['used_size']))
	return json_collect 

def json_final(current):
	final = []
	for c in current:
		tb = byte2TB(c[1]) # converts GB byte data to TB
		a = re.search(r'(IV\d\d\d\d)', c[0]) #removes unicode from IV numbers
		final.append((str(a.group()), round(tb, 2))) 
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

def catdv_login():
	"""Enter CatDV server login details to get access to the API"""
	try:
		user.getAuth()
		print('\nGetting catalog data...\n')
		user.getSessionKey()
		user.getCatalogName()
		time.sleep(1)
		print('Catalog names and ID\'s have been loaded')
	except:
		raise AttributeError
		
def get_barcodes(group_id):
	"""Gets a list of IV barcodes for user-specified client."""
	user.iv_barcodes = []
	user.getCatalogClips(group_id)
	user.collectIVNumbers()
	return user.sortBarcodes()

#def Main():
dload = '/Users/Edit4/Downloads/'
try:
	# Get latest LTO data file from Space LTO. Catches different file types.
	try:
		# Auto adds path. Only filename is needed
		fname = dload + sys.argv[1] 
		if '.json' in fname: 
			jdata = get_json(fname)
			current = json_to_list(jdata)
			name_size = json_final(current)
		elif '.csv' in fname:
			lto_file = open(fname)
			data = csv.reader(lto_file)
			name_size = lto_to_list(data)
		else:
			print('\nCould not recognise the type of file submitted.'
				'\nPlease use a \'.csv\' or \'.json\' file.\n')
	except:
		raise IndexError 

	# Collect barcodes direct from CatDV API.
	user = Cdvlib()
	
	# Login to CatDV API
	start = True
	while start:
		auth = raw_input('Login to CatDV Api? [y/n]: ').lower()
		if auth == 'y':
			catdv_login()

			# Lists created from data obtained by the CatDV API.
			con_api = get_barcodes(user.catalog_names[1][1])
			ng_api = get_barcodes(user.catalog_names[2][1])
			ng_b = get_barcodes(user.catalog_names[3][1])
			for i in ng_b:
				ng_api.append(i)
			cl_api = get_barcodes(user.catalog_names[0][1])
			pw_api = get_barcodes(user.catalog_names[4][1])

			user.deleteSession()

			ng_2 = set(get_client_items(name_size, ng_api))
			pw_2 = set(get_client_items(name_size, pw_api))
			cl_2 = set(get_client_items(name_size, cl_api))

			ng_tb_2 = get_storage_size(ng_2)
			pw_tb_2 = get_storage_size(pw_2)
			cl_tb_2 = get_storage_size(cl_2)
			print('\nFrom the API:\n{}TB written for NGTV\n{}TB written for' 
				' Power\n{}TB written for'
				' Classic Media/Dreamworks\n'.format(ng_tb_2, pw_tb_2, cl_tb_2))
			
			start = False
		
		elif auth == 'n':	
			print('You chose not to access the CatDV API.')
			# Physical lists of current IV barcodes for each client.
			# Manually collected from CatDV	
			ng_list = set(get_CatDV_data(dload + 'ngtv2015_2.txt'))
			power_list = set(get_CatDV_data(dload + 'power2015_2.txt'))
			classic_list = set(get_CatDV_data(dload + 'classic2015_2.txt'))
			content_list = set(get_CatDV_data(dload + 'content2015_2.txt'))

			# Separate LTO Barcodes by client
			ng = get_client_items(name_size, ng_list)
			pw = get_client_items(name_size, power_list)
			cl = get_client_items(name_size, classic_list)
			cn = get_client_items(name_size, content_list)

			# Storage size in TB for client
			ng_tb = get_storage_size(ng)
			pw_tb = get_storage_size(pw)
			cl_tb = get_storage_size(cl)
			cn_tb = get_storage_size(cn)
			
			print('{}TB written for NGTV\n{}TB written for' 
				' Power\n{}TB written for'
				' Classic Media/Dreamworks\n'.format(ng_tb, pw_tb, cl_tb))

			start = False
		else:
			print('Not a recognised input. Please try again.')

	# May no longer be needed
	create_csv = raw_input(
		'Do you wish to write the months archived tape barcodes + sizes to a csv file? [y/n]: ')
	if create_csv == 'y':
		make_csv_file(name_size)
	else:
		print('You have chosen not to write to a csv file.')
except NameError, e: # Name_size var has not been created. check CatDV 
	print(e, 'Check CatDV data inputs: API login and/or filenames.')
except IndexError:
	print('No LTO file submitted. Reopen this program with the LTO history file.')
except IOError:
	print('The submitted CatDV file used for getting IV numbers was not found')
except AttributeError:
	print('\nUnable to access the CatDV API. Please try again later.')
except UnboundLocalError:
	print('\nNo file has been submitted or the file does not exist.\n'
		'Check that the \'.csv\' or \'.json\' file has been saved and' 
		'reopen this script along with the filename.')	
finally:
	try:
		if lto_file:
			lto_file.close()
	except NameError:
		print('Closing application')
	print('Goodbye!')
#if __name__ == '__main__':
#	Main()
