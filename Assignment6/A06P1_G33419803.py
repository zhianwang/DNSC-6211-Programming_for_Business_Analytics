# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:29:06 2016

@author: Zhian Wang
GWID: G33419803

This program is used to call the fileinput, create and solve LP and produce the outputs.
Besides the default output, user can choose other different outputs through '-b','-d' and '-o'.
"""

import A06P1Module_G33419803 as md1

import argparse as ap

def Main():
    myP = ap.ArgumentParser()
    
    myGroup = myP.add_mutually_exclusive_group()
    myGroup.add_argument("-b","--brief", action = "store_true")                      
    myGroup.add_argument("-d","--detailed", action = "store_true")                           
    
    myP.add_argument("myFile", help="the Name of input JSON file")
    myP.add_argument('-o', '--outfile', help='output file')
    
    myArgs = myP.parse_args()
    
    Data = md1.readLPData(myArgs.myFile)
    myData = md1.createAndSolveLP(Data)
    #print(myData)
    
#This is the brief output    
    if myArgs.brief:                                                                   
        print(myData["Objective Function"])
         
#This is the detailed output    
    elif myArgs.detailed:
        md1.detailedOutput(Data,myData)                                                                   
  

#This is the default output    
    else:                                                                            
        print ('The optimal value is {:.3f}'.format(myData["Objective Function"]))                

#This is the output file         
    if myArgs.outfile:
       md1.writeFile(myArgs.outfile,Data,myData)


# Main Function

if __name__ == "__main__":
    Main()