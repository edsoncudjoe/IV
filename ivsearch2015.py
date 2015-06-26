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
# Version 1.0.3
#       Changed the collection of drive volumes into dictionary plus how 
#       methods will access the volumes.
#       Removed the create and remove target folder methods.
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
        self.locations = {
        0: ['/Volumes/AV_RAID', 'AV_RAID'], 
        1: ['/Volumes/Signiant_Sep13', 'Signiant'],
        2: ['/Volumes/Space', 'Space'],
        3: ['/Volumes/AS_OFFLINE', 'AS_OFFLINE']
        }
        self.extensions = ('.mov', '.mxf', '.h264', '.wav')
        
    
    def print_location(self): 
        """User chooses location to search."""
        length = len(self.locations)
        print('\n\t\t Volume Options:\n')
        for k, v in self.locations.items():
            print('\t\t {0}. {1}'.format(k + 1, v[1]))
        print(
            '\t\t {0}. AV_RAID + Space\n\t\t {1}. AV_RAID + Signiant\n\t\t {2}.'
             ' All Volumes'.format(
                length + 1, length + 2, length + 3))
      
    def set_target_folder(self):
        """Determines target folders that need to be searched."""
        start = True
        while start:
            try:
                self.choice = raw_input(
        "\nSelect your folder to search from the choices above.\n").lower()
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
            self.multi_thread(len(self.locations))
              
 
    def create_thread_targets(self, location):
        self.target = self.locations[location][0]
        return self.target

    def multi_thread(self, num):
        """Applied when all volumes have been selected to be searched."""
        for i in range(num):
            self.targets.append(self.create_thread_targets(i))

    def double_thread(self, n):
        """Applied when only two volumes are selected to be searched."""
        self.targets.append(self.create_thread_targets(n))

    def search(self, target_folder, user_entry):
        """Recursive search of folders for a user specified file. 
        This method will only search for video and audio filetypes."""
        for root, dirs, files in os.walk(target_folder):
            for file in files:
                if user_entry.lower() in file.lower():
                    if file.endswith(self.extensions):
                        print os.path.join(root, file)
                        print('\n') 
    
    def set_thread(self, target, search_term):
        """Searches for one item on its own thread."""
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
            print('Searching {0} for : {1}'.format(s1.target, search_term)) # fix for zero length field error.
            s1.search(s1.target, search_term)

        new_search = raw_input('\nWould you like to do another search?[y/n]: ').lower()
        if new_search != 'y':
            startloop = False
    print('Goodbye.')
        
if __name__ == '__main__':
    main()

