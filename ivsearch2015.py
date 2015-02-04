#!/usr/bin/python2.6

import os
import sys
import time
import threading

class SearchFile(object):

    def __init__(self):
        
        self.collect = []
        self.target2 = None
        self.target3 = None
        self.target4 = None
        self.locations = ['/Volumes/AV_RAID', '/Volumes/Signiant_Sep13', 
        '/Volumes/Space', '/Volumes/AS_OFFLINE']
        self.startloop = True
        self.extensions = ('.mov', '.mxf', '.h264')
        
        
    def get_location(self):
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
        self.choice = raw_input(
        "Select your folder to search from the choices above.\n").lower()
        return self.choice
       
    def set_target_folder(self, choice):
        """Determines target folders that need to be searched."""
        start = True
        while start:
            if choice == 'q':
                print('Adios!')
                sys.exit(0)
            elif choice == '1':
                self.target = self.locations[0] # AV_RAID
                start = False
            elif choice == '2':
                self.target = self.locations[1] # Signiant
                start = False
            elif choice == '3':
                self.target = self.locations[2] # Space
                start = False
            elif choice == '4':
                self.target = self.locations[3] # AS_OFFLINE
                start = False
            elif choice == '5':
                self.target = self.locations[0]
                self.target2 = self.locations[2]
                start = False
            elif choice == '6':
                self.target = self.locations[0]
                self.target2 = self.locations[1]
                start = False
            elif choice == '7':
                self.target = self.locations[0]
                self.target2 = self.locations[1]
                self.target3 = self.locations[2]
                self.target4 = self.locations[3]
                start = False
            else:
                print("That wasn't recognised.")
                choice = raw_input(
        "Select your folder to search from the choices above.\n").lower()      
        return
    
    def create_target_folder(self):
        """Adds a new folder to locations list"""
        self.new_target = raw_input(
        "Enter the FULL path of the new folder \(eg:/Volumes/Path/to/folder\): ")
        self.locations.append(self.new_target)
        return self.new_target 
        
    def search(self, target_folder, user_entry):
        """Recursive search of folders for specified file."""
        for root, dirs, files in os.walk(target_folder):
            for file in files:
                if user_entry.lower() in file.lower():
                    if file.endswith(self.extensions):
                        print os.path.join(root, file)
                    else:
                        continue 
    
    def set_thread(self, target, search_term):
        """Searches for item on its own thread."""
        t = threading.Thread(target=self.search, args=(target, search_term))
        t.daemon = True
        return t
        
    def start_threads(self):
        """Starts search threads."""
        for item in self.collect:
            #print("starting: {0}".format(item)) 
            item.start()
        return
       
    def stop_threads(self):
        for item in self.collect:
            item.join()
        return
        

            
             
def main():                
    s1 = SearchFile()
    s1.get_location()
    

    s1.set_target_folder(s1.choice)
    search_term = raw_input('\nEnter search item: ')      
   

    if s1.target3:
        # set locations to separate threads
        a = s1.set_thread(s1.target, search_term)
        b = s1.set_thread(s1.target2, search_term)
        c = s1.set_thread(s1.target3, search_term)
        d = s1.set_thread(s1.target4, search_term)
        
        # group threads together
        s1.collect.append(a)
        s1.collect.append(b)
        s1.collect.append(c)
        s1.collect.append(d)
        
        # start searches
        s1.start_threads()
        s1.stop_threads()
        
    elif s1.target2:
        #set locations
        a = s1.set_thread(s1.target, search_term)
        b = s1.set_thread(s1.target2, search_term)
        
        #group threads
        s1.collect.append(a)
        s1.collect.append(b)
        
        s1.start_threads()
        s1.stop_threads()
    else:
        s1.search(s1.target, search_term)
        
if __name__ == '__main__':
    main()

