from Tkinter import *
import ttk
import pprint
#from ivsearch2015 import SearchFile

import os

class App:

    def __init__(self, master):
        frame = Frame(master, bg='grey', width=200, pady=10, padx=20, 
            borderwidth=2, relief=RAISED)
        frame.pack(fill=X)
        
        midframe = Frame(master, bg='#3a434a', width=100, pady=5, padx=10, 
            borderwidth=2, relief=FLAT)
        midframe.pack(fill=X)
        
        btm = Frame(master, bg='grey', width=200, pady=10, padx=20, 
            borderwidth=2, relief=RAISED)
        btm.pack(fill=X)
        
        #Search Button
        self.search = Button(frame, text="SEARCH", bg='grey', command=self.search)
        #self.search.config(command=self.progressCall)
        self.search.pack(side=RIGHT)
        
        #Search Entry Box
        self.user_entry = Entry(frame, width="100")
        self.user_entry.bind("<Return>", self.search)
        self.user_entry.pack(side=RIGHT)
        
        #Quit Button
        self.endapp = Button(btm, text="QUIT", bg='grey', fg='grey', command=frame.quit)
        self.endapp.pack(side=RIGHT, fill=X)
        
        #Results Box
        self.results = Listbox(midframe, height=25)
        self.results.pack(fill='x')  
        
        #Progress Bar
        self.progress = ttk.Progressbar(btm, orient="horizontal", mode="indeterminate")
        self.progress.config(length=300)
        self.progress.pack(side=LEFT)

        self.target_folder = "/Volumes/AV_RAID"
        
        self.extensions = ('.mov', '.mxf', '.h264')  
        
    def print_entry(self):
        """
        Prints the input from search box into the results box.
        """
        e = self.user_entry.get()
        self.results.insert(END, str(e)) 

    def goget(self, event):
        a = self.user_entry.get()
        self.results.insert(END, str(a))
        

    def progressCall(self):
        self.progress.config(maximum=0, value=1)
        

    def search(self):
        """
        Searches through folders to match the user-defineed file.
        Returns found files that match search query.
        """
        name = self.user_entry.get()
        query = name.lower()
        for root, dirs, files in os.walk("/Volumes/AV_RAID"):
            for file in files:
                if file.endswith(self.extensions):
                    if query in file.lower():
                        self.results.insert(END, str(os.path.join(root, file)))
                    else:
                        continue

         
root = Tk()

app = App(root)
root.geometry('1193x545')
root.title('IV-Search')

root.mainloop()
