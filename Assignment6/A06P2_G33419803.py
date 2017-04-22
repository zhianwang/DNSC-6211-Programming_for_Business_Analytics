# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 21:03:27 2016

@author: Zhian Wang
GWID: G33419803

This program is used to call the fileinput, read and store, create and solve LP and produce the outputs.
Besides the default output, user can choose other different outputs through '-t' and '-d'.
"""

import A06P2Module_G33419803 as md2

import argparse as ap

def Main():
    myP = ap.ArgumentParser()
    
    myP.add_argument('-t', dest='textFile', action='store', help='output file')
    myP.add_argument('-d', dest='tableName', action='store', help='output file')
    
    myArgs = myP.parse_args()
    
    file_names = md2.getFileNames()
    myLP = md2.readAndStore(file_names)
    
      
    #if (myArgs.textFile and myArgs.tableName):
    #    for x in myLP:
    #        result = md2.createAndSolveLP(x)
    #        print("The optimal value for", x['name'],"is","{:.3f}".format(result['Objective Function']))
    #    md2.writeTXT(myArgs.textFile,myLP)
    #    md2.writeDatabase(myLP,myArgs.tableName)
      
    for x in myLP:
        optimal = md2.createAndSolveLP(x)
        print("The optimal value for", x['name'],"is","{:.3f}".format(optimal['Objective Function']))
       
        
    #This is output sent to the textfile
    
    if myArgs.textFile:
        file_names = md2.getFileNames()
        myLP = md2.readAndStore(file_names)
            
        md2.writeTXT(myArgs.textFile,myLP)

    
#This is output sent to table       
    if myArgs.tableName:
        file_names = md2.getFileNames()
        myLP = md2.readAndStore(file_names)
        
        md2.writeDatabase(myArgs.tableName,myLP)
        
        
# Main Function

if __name__ == "__main__":
    Main()