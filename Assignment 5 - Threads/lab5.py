import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import filedialog
import os
import os.path
import re
from filesearch import FileSearch

class FindWin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('File Search')               #set title
    
        #os.chdir(os.path.expanduser('~'))       #change directory to home directory
        self.directory = tk.StringVar()
        #self.directory.set(os.getcwd())         #set directory to current working directory
        startDir = 'D:\CIS41B'
        self.directory.set(startDir)
        #startDir = os.path.expanduser('~')
        
        CFLabel = tk.Label(self, text='Current Folder').grid(sticky='w')                            
        DirLabel = tk.Label(self, textvariable=self.directory).grid(row=0, column=1, sticky='w')    
    
        CFButton = tk.Button(self, text='Change Folder', command=lambda:self.__selectDir()).grid(row=1, column=0, stick='w')
        
        self.regexText = tk.StringVar()
        regexLabel = tk.Label(self, text='Regex filter:').grid(row=2, column=0, sticky='e')
        regexEntry = tk.Entry(self, textvariable=self.regexText)
        regexEntry.grid(row=2, column=1, columnspan=3, sticky='ew')
        #self.initial_focus = regexEntry
        regexEntry.focus_set()
        regexEntry.bind('<Return>', self.__search)   #callback to search method when pressing return
        
        self.searchText = tk.StringVar()
        searchLabel = tk.Label(self, text='Search String').grid(row=3, column=0, sticky='e')
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
            
        self.FS.searchName(regex, self.searchText.get(), self.result_list)                                         #calls searchName from object and pass in regex
        print(self.result_list)
        self.updateListBox()
        
    def updateListBox(self):
        self.numFiles = len(self.result_list)                                           #number of files is the length of sorted list
        self.foundFiles.set('Found ' + str(self.numFiles) + ' files')                   #set found files to number of files  
        
        if self.numFiles > 1000:
            tkmb.showwarning(title='oops', message=str(self.numFiles) + " files found. That's over 1000.")
        else:
            self.resultListbox.delete(0, tk.END)                                        #clears listbox
            for item in self.result_list:   
                self.resultListbox.insert(tk.END, item[0])                              #populating listbox    
            self.result_list[:] = []                                                    #clears result list
    
def main() :
    win = FindWin()
    win.mainloop()

main()    
