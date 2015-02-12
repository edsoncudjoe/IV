#!/usr/bin/python2.6

###############################################################################
#
# Name: ivsearch2015.py (ivfilesearch.py)
# Author: E.Cudjoe
# Date: 29 January 2015
#
# Objective: To recursively search through a given directory for 
#                a user-specified file.
#
# Inputs: 1.Volumes to be searched. 2.Search terms to look for.
# Outputs: Results of search 
#
#------------------------------------------------------------------------------
# 
# Version 1.0.2
#       Fixed an error that would appear after choosing to search for a second 
#       item.
#       Added a method for removing a volume from the list of locations.
#       Get_location method has been renamed and now only prints the current volumes.
#       Corrected and cleaned the set_target_folder method.
#
# Version 1.0.1
#       Added threading to perform searches over multiple folders 
#       simultaneously.
#       Rewritten using OOP.
#       Defined search files to specific file types.
#       Added search locations to a list and added a feature to create new
#       search locations.
#       
# 
# Version 1.0 
#       Initial build 
#
# folder options:
#               AV_Raid, Signiant Server, Space Server, All Volumes
#
#------------------------------------------------------------------------------
# TODO - change list output arrangement to select files to be searched
#  
###############################################################################

import os
import sys
import time
import threading

class SearchFile(object):

    def __init__(self):
        
        self.collect = [] # list for collecting threads
        self.targets = [] # For collecting target search folders
        self.target = None
        self.locations = ['/Volumes/AV_RAID', '/Volumes/Signiant_Sep13', 
        '/Volumes/Space', '/Volumes/AS_OFFLINE']
        self.extensions = ('.mov', '.mxf', '.h264', '.wav')
        
    def print_location(self): 
        """User chooses location to search."""
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
      
    def set_target_folder(self):
        """Determines target folders that need to be searched."""
        start = True
        while start:
            try:
                self.choice = raw_input(
        "Select your folder to search from the choices above.\n").lower()
                if self.choice in str(range(1, 8)):
                    start = False
                elif self.choice == 'q':
                    print('Adios!')
                    sys.exit(0)   
                else:
                    raise NameError
            except NameError:
                print('ERROR: That is not a recognised input.')

        
        if self.choice == '1': 
            self.create_thread_targets(0) # AV_RAID
        elif self.choice == '2':
            self.create_thread_targets(1) # Signiant
        elif self.choice == '3':
            self.create_thread_targets(2) # Space
        elif self.choice == '4':
            self.create_thread_targets(3) # AS_OFFLINE 
        elif self.choice == '5':
            self.double_thread(0)
            self.double_thread(2)
        elif self.choice == '6':
            self.double_thread(0)
            self.double_thread(1)
        elif self.choice == '7':
            self.multi_thread(len(self.locations)) # catch in case a new directory is added
              
 
    def create_thread_targets(self, location):
        self.target = self.locations[location]
        return self.target

    def multi_thread(self, num):
        """Applied when all volumes have been selected to be searched."""
        for i in range(num):
            self.targets.append(self.create_thread_targets(i))

    def double_thread(self, n):
        """Applied when two volumes are selected to be searched."""
        self.targets.append(self.create_thread_targets(n))

###############################################################################
# Not currently in use.
    def remove_target_folder(self):
        """Removes old target from list of directories"""
        for location in self.locations:
            print location
        self.old = raw_input('Enter full name of folder to be removed: ')
        self.locations.remove(self.old)

    def create_target_folder(self):
        """Adds a new folder to locations list"""
        self.new_target = raw_input(
        "Enter the FULL path of the new folder \(eg:/Volumes/Path/to/folder\): ")
        self.locations.append(self.new_target)
        return self.new_target
###############################################################################

    def search(self, target_folder, user_entry):
        """Recursive search of folders for specified file."""
        for root, dirs, files in os.walk(target_folder):
            for file in files:
                if user_entry.lower() in file.lower():
                    if file.endswith(self.extensions):
                        print os.path.join(root, file)
                        print('\n') 
    
    def set_thread(self, target, search_term):
        """Searches for item on its own thread."""
        t = threading.Thread(target=self.search, args=(target, search_term))
        t.daemon = True
        return t
        
    def start_threads(self):
        """Starts search threads."""
        for item in self.collect:
            print("starting: {0}".format(item)) 
            item.start()
       
    def stop_threads(self):
        for item in self.collect:
            item.join()
        

            
             
def main():                

    startloop = True
    while startloop:
        s1 = SearchFile()
        s1.print_location()

        s1.set_target_folder() 
        search_term = raw_input('\nEnter search item: ')      

        if len(s1.targets) >= 2:
            s1.collect = [s1.set_thread(s1.targets[i], search_term) for i in range(len(s1.targets))]
            s1.start_threads()
            s1.stop_threads()

        elif s1.target:
            print('Searching {} for : {}'.format(s1.target, search_term))
            s1.search(s1.target, search_term)

        new_search = raw_input('\nWould you like to do another search?[y/n]: ').lower()
        if new_search != 'y':
            startloop = False
    print('Goodbye.')
        
if __name__ == '__main__':
    main()

