#Gautam Mehta
#Aiden Sun
import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import filedialog
import threading 
import os
import os.path
import sys
import platform
import re
from filesearch import FileSearch

class FindWin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('File Search')               #set title
        self.directory = tk.StringVar()
        startDir = "/Users/gautammehta/Desktop/CIS40/"
        #startDir = os.path.expanduser('~')
        self.directory.set(startDir)
        
        
        CFLabel = tk.Label(self, text='Current Folder').grid(sticky='w')                            
        DirLabel = tk.Label(self, textvariable=self.directory).grid(row=0, column=1, sticky='w')    
    
        CFButton = tk.Button(self, text='Change Folder', command= self.__selectDir).grid(row=1, column=0, stick='w') #no longer need a lambda
        
        self.regexText = tk.StringVar()
        regexLabel = tk.Label(self, text='Regex filter:').grid(row=2, column=0, sticky='e')
        regexEntry = tk.Entry(self, textvariable=self.regexText)
        regexEntry.grid(row=2, column=1, columnspan=3, sticky='ew')
        
        regexEntry.focus_set()
        regexEntry.bind('<Return>', self.__search)   #callback to search method when pressing return
        
        self.searchText = tk.StringVar()
        searchLabel = tk.Label(self, text='Search String:').grid(row=3, column=0, sticky='e')
        searchEntry = tk.Entry(self, textvariable=self.searchText)
        searchEntry.grid(row=3, column=1, columnspan=3, sticky='ew')
        searchEntry.bind('<Return>', self.__search)
        
        resultLabel = tk.Label(self, text='Results:').grid(row=4, column=0, sticky='w')
        
        scrollbar = tk.Scrollbar(self)
        self.resultListbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        self.resultListbox.grid(row=5, columnspan=2, sticky='nesw')
        scrollbar.config(command=self.resultListbox.yview)
        scrollbar.grid(row=5, column=3, sticky='nes')
        
        self.foundFiles = tk.IntVar()
        self.foundFiles.set('Found ' + str(self.foundFiles.get()) + ' files')           #set default files found to 0
        foundLabel = tk.Label(self, textvariable=self.foundFiles).grid(row=6, sticky='sw')
        
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(5, weight=1)
        
        self.result_list = []
        
        self.protocol("WM_DELETE_WINDOW", self._exit)       
        self.update()

        self.FS = FileSearch(self.directory.get())                                      #instantiate FileSearch object
        
    def __selectDir(self):
        os.chdir(filedialog.askdirectory())                                             #ask user for new directory and change directory to that
        
        self.directory.set(os.getcwd())                                                 #set to current working directory
        
        self.resultListbox.delete(0, tk.END)                                            #clears listbox when changing directory
        self.FS = FileSearch(self.directory.get())                                      #once directory is changed, update FileSearch object with new directory
        self.bind('<Return>', self.__search)                                            #callback to search method when pressing return (user input regex)
        
    def __search(self, *args):
        try:
            regex = re.compile(self.regexText.get(), re.I)                              #checks if input regex is valid
        except re.error as e:
            tkmb.showerror(title='Oops', message="Invalid regex: " + str(e))       #error message if not
            return
            
        #self.FS.searchName(regex, self.searchText.get(), self.result_list)        #calling searchName slows down process
        e = threading.Event() 
        t = threading.Thread(target=self.FS.searchName, args= (regex, self.searchText.get(), self.result_list)) # create a child thread 
        
        self.__cancelSearch()
        self.result_list.clear()
        t.start()
           
        self.updateListBox()
        
    def updateListBox(self):
        if t.isAlive() == True:
            self.id =self.after(100, self.updateListBox)
        elif t.isAlive() == False:
            self.numFiles = len(self.result_list)                                           #number of files is the length of sorted list
            self.foundFiles.set('Found ' + str(self.numFiles) + ' files')                   #set found files to number of files  
            
            if self.numFiles > 1000:
                tkmb.showwarning(title='oops', message=str(self.numFiles) + " files found. That's over 1000.")
                
            else:
                self.resultListbox.delete(0, tk.END)                                        #clears listbox
                #for item in self.result_list:   
                    #self.resultListbox.insert(tk.END, item[0])                              #populating listbox    
                self.resultListbox.insert(tk.END, *self.result_list)
                self.result_list[:] = []                                                    #clears result list
    def __cancelSearch(self):
        self.after_cancel(self.id) 
        e.wait()
        t.join()
        
    def _exit(self):
        self.after_cancel(self.id)   #its either this or 
        #t.join() 
        self.destroy()
        
def main() :
    win = FindWin()
    if platform.system() == 'Darwin': 
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))      
    win.mainloop() 
main() 
