# name: ivfilesearch.py
# Author: E.Cudjoe
#
# Objective: to create a search application that can search for a file through multiple 
# 		volumes in one attempt.
# Inputs: 1.Volumes to be searched. 2.Terms to look for.
# Outputs: Results of search 
#
#--------------------------------------------------------------------------------------
#
# select folder(s) to search through
# get search term
# open folders
# search folders for term
# return results for each folder

#folder options
# Raid, Signiant, Space, All

import os

startloop = True #Select folder to search through
while startloop:
    try:
        print(""" 
	Volume Options:
	
	1. AV_RAID
	2. Signiant
	3. Space(Ftp, Archive, etc)
	4. All Volumes
	Q. Quit

""")
        choice = raw_input("Select your folder to search from the choices above.\n")
        if choice == '1':
            target = '/Volumes/AV_RAID'
            startloop = False
        elif choice == '2':
            target = '/Volumes/Signiant_Sep13'
            startloop = False
        elif choice == '3':
            target = '/Volumes/Space'
            startloop = False
        elif choice == '4':
            target = '/Volumes'
            startloop = False
        #elif choice == 'Q' or 'q': # move to function that closes app
        #    startloop = False
        else:
            raise ValueError('\nwrong input\n')
    except ValueError:
        print('\nSorry, that option is not available.\nPlease try again. \n')

folder = [f for f in os.listdir(target) if os.path.isfile(f)] #open folder

search_term = raw_input('Search: ') #get search term

for f in folder:
    if search_term in f:
        print f
        
 

   
