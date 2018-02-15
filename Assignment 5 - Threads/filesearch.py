import os
import os.path
import re
from strsearch import strIsInFile

class FileSearch():
                
    def __init__(self, dirPath):

        #self.files = defaultdict(list)
        #for (dirPath, dirL, fileL) in os.walk(dirPath):
            #for f in fileL:
                #self.files[f].append(os.path.join(dirPath, f))
        
        self.files = []
        for (dirPath, dirL, fileL) in os.walk(dirPath):
            for f in fileL:
                self.files.append(tuple((os.path.join(dirPath, f), f)))
        
        #print(self.files)

    def searchName(self, regex, searchString, listResults):
        #print(regex)
        
        for fileTuple in self.files:
            if re.search(regex, fileTuple[1]):
                if strIsInFile(searchString, fileTuple[0]) or len(searchString) == 0:
                    listResults.append(fileTuple)
                
        listResults = [fileTuple for fileTuple in self.files if re.search(regex, fileTuple[1]) and strIsInFile(searchString, fileTuple[0]) or len(searchString) == 0]
        listResults.sort(key=lambda tup: tup[0])
        
        #print(listResults)
        
        #fileNames = (fn for fn in self.files if re.search(regex, fn))
        #return sorted(i for fn in fileNames for i in self.files[fn])
    
    
    #def recursiveScanTree(self, dirPath):
        
        #for entry in scandir(dirPath):
            #if entry.is_dir():
                #yield from self.recursiveScanTree(entry.path)
            #else:
                #yield entry       
