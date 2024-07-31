# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:53:32 2023

@author: joula
"""
import numpy as np
import re

def Read_txt(file_name):
    with open(file_name, 'r') as file:
            # Read the contents of the file
            content = file.read()
     
            # Extract all the numbers from the content
            numbers = re.findall(r'\d+', content)
            
    somme = np.zeros([101, 5])
    somme[:,0] = np.arange(50, -51, -1)
    
    for i in range(101):
        somme[i,1] = int(numbers[5*i+1])
        somme[i,2] = int(numbers[5*i+2])
        somme[i,3] = int(numbers[5*i+3])
        somme[i,4] = int(numbers[5*i+4])
    
    # difference = np.zeros([101, 5])
    # difference[:,0] = np.arange(50, -51, -1)
    
    # for i in range(101, 202):
    #     difference[i-101,1] = int(numbers[5*i+1])
    #     difference[i-101,2] = int(numbers[5*i+2])
    #     difference[i-101,3] = int(numbers[5*i+3])
    #     difference[i-101,4] = int(numbers[5*i+4])
    
    return somme