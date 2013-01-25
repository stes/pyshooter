'''
Created on 24.12.2012

@author: stes
'''

class Logger():
    
    def __init__(self, path):
        self.path = path
        self.file = open(path, 'w+')
        self.update = 10
    
    def log(self, tank1, tank2, world):
        self.file.write(str(tank1.location))
        if (self.update == 0):
            self.update = 10
            self.file.flush()
            
    def __del__(self):
        self.file.flush()
        self.file.close()