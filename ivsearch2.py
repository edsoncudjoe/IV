###############################################################################
#
# name: ivsearch2.py
# Author: E.Cudjoe
#
# Objective: To recursively search through a given directory for 
#                a user-specified file.
#
# Inputs: 1.Volumes to be searched. 2.Search terms to look for.
# Outputs: Results of search 
#
#------------------------------------------------------------------------------
# Version 1.1 - 171114
#       Added threading for simultaneous searches
# Version 1.0
#       Initial build
#
# folder options:
#               AV_Raid, Signiant Server, Space Server, All Volumes
#
#------------------------------------------------------------------------------
# TODO - add wildcard searches such as *
# TODO - GUI
###############################################################################

import os
import sys
import time
import threading

def search(target_folder, user_entry):
    """Recursive search of folders for specified file."""
    #start = time.time()
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if user_entry.lower() in file.lower():
                print os.path.join(root, file)
            else:
                continue

def elapsed_time(start, end):
    """Reports time taken for search."""
    time_elapsed = end - start
    if time_elapsed >= 60:
        print('Time elapsed: {:.2f} minutes.'.format(time_elapsed / 60))
    else:
        print('\nTime elapsed: {:.2f} seconds'.format(time_elapsed))
    return

def Main():
    
    target2 = None
    target3 = None
    target4 = None
    startloop = True
    while startloop:
        try:
            print(""" 
	    Volume Options:
	
	    1. AV_RAID
	    2. Signiant
	    3. Space(Ftp, Archive, etc)
	    4. AS_OFFLINE
	    5. AV_RAID + Space Server
	    6. AV_RAID + Signiant
	    7. All Volumes
	    
	    Q. Quit
    """)
            choice = raw_input(
            "Select your folder to search from the choices above.\n").lower()
            if choice == 'q':
                print('Goodbye.')
                sys.exit(0)
            elif choice == '1':
                target = '/Volumes/AV_RAID'
                startloop = False
            elif choice == '2':
                target = '/Volumes/Signiant_Sep13'
                startloop = False
            elif choice == '3':
                target = '/Volumes/Space'
                startloop = False
            elif choice == '4':
                target = '/Volumes/AS_OFFLINE'
                startloop = False
            elif choice == '5':
                target = '/Volumes/AV_RAID' 
                target2 = '/Volumes/Space'
                startloop = False
            elif choice == '6':
                target = '/Volumes/AV_RAID'
                target2 = '/Volumes/Signiant_Sep13'
                startloop = False
            elif choice == '7':
                target = '/Volumes/AV_RAID'
                target2 = '/Volumes/Signiant_Sep13'
                target3 = '/Volumes/Space'
                target4 = '/Volumes/As_OFFLINE'
                startloop = False
            else:
                raise ValueError('\nwrong input\n')
        except ValueError:
            print(
                '\nSorry, that option is not available.\nPlease try again. \n')
    
    search_term = raw_input('\nEnter search item: ')
    
    if target3:
        print('Searching all main volumes.')
        #start = time.time()
        for i in range(5):
            t = threading.Thread(target=search, args=(target+str(i), search_term))
            t.start()
            #t.join()
        #end = time.time()  
    elif target2:
        print(
        '\nSearching directories: \'{}\' and \'{}\'. Press CTRL+C to cancel.\n'
            .format(target, target2))
        t1 = threading.Thread(name='directory1', target=search, 
            args=(target, search_term))
        t2 = threading.Thread(name='directory2', target=search, 
            args=(target2, search_term))
        
        start = time.time()
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        end = time.time()
    else:
        print(
        '\nSearching: \'{}\'. Press CTRL+C to cancel.\n'.format(target))
        start = time.time()
        search(target, search_term)
        end = time.time()
    
    
    #elapsed_time(start, end)
        
    
    #
        
if __name__ == '__main__':
    Main()
    

   
