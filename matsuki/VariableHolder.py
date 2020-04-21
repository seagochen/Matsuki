# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Apr 16, 2020
# LastChg: Apr 16, 2020

import threading
import time

class VariableHolder(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.variables = {}
        self.flag = True

    
    def run(self):
        while self.flag:
            time.sleep(1) # sleep this thread for every 10 seconds


    def put(self, key: str, val: object):
        """
        add val to vailable holder
        """
        self.variables[key] = val

    
    def get(self, key: str):
        """
        get val from variable holder
        """
        if key in self.variables.keys():
            return self.variables[key]
        
        return None

    
    def pop(self, key: str):
        """
        pop key from variable holder
        """
        if key in self.variables.keys():
            return self.variables.pop(key)
        
        return None

    
    def clean(self):
        """
        clean up variable holder
        """
        self.variables.clear()
    

    def keys(self):
        return self.variables.keys()

    
    def close(self):
        self.flag = False

    

def create_variableHolder():
    holder =  VariableHolder()
    holder.start()
    return holder