from Tkinter import *
import pprint

import os

class App:

    def __init__(self, master):
        frame = Frame(master, bg='blue', width=200, pady=10, padx=20)
        frame.pack()
        
        midframe = Frame(master, bg='yellow', height=20, width=100, pady=10, padx=20, relief=RIDGE)
        midframe.pack(fill=BOTH, expand=1)
        
        btm = Frame(master, bg='green', height=10, width=200, pady=10, padx=20)
        btm.pack(fill=BOTH, expand=1)
        
        #Search Entry Box
        self.user_entry = Entry(frame, width="90")
        self.user_entry.bind("<Return>", self.search)
        self.user_entry.pack(side=LEFT)

        #Search Button
        self.search = Button(frame, text="SEARCH", command=self.print_entry)
        self.search.config(fg='yellow', borderwidth=5) # Check these work
        self.search.pack(side=LEFT)
        
        #Quit Button
        self.endapp = Button(btm, text="QUIT", padx=15, command=frame.quit)
        self.endapp.pack(side=RIGHT)
        
        #Results box
        self.result_title = Label(midframe, fg='red', text='Results', width=100)
        self.result_title.pack(fill=BOTH, expand=1)
        
        #Results Box
        self.results = Listbox(midframe)
        self.results.pack(fill='x')  
        

        self.target_folder = "/Volumes/AV_RAID"  
        
    def print_entry(self):
        """Prints input from search box into results box"""
        e = self.user_entry.get()
        self.results.insert(END, str(e)) 

    def goget(self, event):
        a = self.user_entry.get()
        self.results.insert(END, str(a))
        
    def search(self, user_entry):
        """Recursive search of folders for specified file."""
        name = self.user_entry.get()
        for root, dirs, files in os.walk("/Volumes/AV_RAID"):
            for file in files:
                if name in file.lower():
                    print os.path.join(root, file)
                else:
                    continue
        
root = Tk()

app = App(root)
root.geometry('850x360')
root.title('IV-Search')

root.mainloop()
