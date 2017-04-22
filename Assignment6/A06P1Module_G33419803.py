# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:29:06 2016

@author: Zhian Wang
GWID: G33419803

This program is define functions to read jason file, creat and solve LP problems and
define two types of outputs.
"""

import pulp as pu

def readLPData(fn):
    """
    Input = name of JSON file
    Returns = JSON object
    """
    import json
    try:
        with open(fn,"r") as f:
            LPdata = json.load(f)
        return LPdata
    except:
        return None
        
#a = readLPData("/home/zwang/1-ProgrammingForBA/Homework/HW6/introLP.json")
b = readLPData("/home/zwang/1-ProgrammingForBA/Homework/HW6/whiskas.json")

def createAndSolveLP(LPdata):
    """
    Input = JSON object
    Returns = a dictionary with 2 elements
    The first element is the key value pair of the objective function and the value of
    the
    objective function and the second element is a dictionary whose key value pair is
    the
    decision variables and their values
    """    
    #initialise the model
    if LPdata['objective'] == "MIN":
        my_model = pu.LpProblem(LPdata['name'], pu.LpMinimize)
    elif LPdata['objective'] == "MAX":
        my_model = pu.LpProblem(LPdata['name'], pu.LpMaximize)
    else:
        print("Neither max nor min")
        exit(0)
    
    #make a list of decision variables    
    decVars = LPdata['variables']
    #print (decVars)
    #input("Enter to continue...")    
    
    #create a dictionary of pulp variabes with keys from input vars
    #the default lower bound is -inf, make it 0
    x = pu.LpVariable.dict('%s', decVars, lowBound = 0)
    
    #Objective function data
    objCoeffList = LPdata["objCoeffs"]
    objective = dict(zip(decVars, objCoeffList))
    
    #create the objective function
    my_model += sum([objective[i] * x[i] for i in decVars])
    
    #create the constraints
    constraintKeys = LPdata["LHS"].keys()
    
    for key in constraintKeys:
        LHScoeffs = dict(zip(decVars, LPdata["LHS"][key]))
        if LPdata["conditions"][key] == '<=':
            my_model += sum([LHScoeffs[j] * x[j] for j in decVars]) <= LPdata['RHS'][key]    
        elif LPdata["conditions"][key] == '>=':
            my_model += sum([LHScoeffs[j] * x[j] for j in decVars]) >= LPdata['RHS'][key]  
        elif LPdata["conditions"][key] == '==':
            my_model += sum([LHScoeffs[j] * x[j] for j in decVars]) == LPdata['RHS'][key]  
        else:
            print ("Problems with constraint {} ".format(key))
            exit(0)
            
    # Save and solve the problem
    my_model.writeLP(LPdata['name']+".lp")
    my_model.solve()              
    #my_model.solve(plp.GLPK())      
    #print ("Status:", pu.LpStatus[my_model.status])
    
    lpDict = {}
    lpDict["Objective Function"] = pu.value(my_model.objective)

    d = {}
    for v in my_model.variables():
        d.update({v.name:v.varValue})
    
    lpDict["Variables"] = d       
    
    return (lpDict)
    
#createAndSolveLP(a)
B=createAndSolveLP(b)
#print(B)
         
def writeFile(filename,LPdata,myData): 
    """
    Input = name of output file
    Output = text file with the detailed output or error message if the write
    operation was unsuccessful
    """
    try:
        with open(filename,"w") as f:
            if LPdata['objective'] == "MIN":
                text = "The minimum value is {:.3f}\n".format(myData["Objective Function"])
            elif LPdata['objective'] == "MAX":
                text = "The maximum value is {:.3f}\n".format(myData["Objective Function"])
            #text = "The minimum value is {:.3f}\n".format(myData["Objective Function"])
            text += "The decision variables and their values are:" + "\n"
            for i in myData["Variables"]:
                text += i+": " + "{:.3f}".format(myData["Variables"][i]) +"\n"
            f.write(text)
            #print (text)
            print ("Output being sent to " + filename)
            print ("Output written to" + filename)

    except:
        print ("Fail to write file")


def detailedOutput(LPdata,myData):
    if LPdata['objective'] == "MIN":
        text = "The minimum value is {:.3f}".format(myData["Objective Function"])
    elif LPdata['objective'] == "MAX":
        text = "The maximum value is {:.3f}".format(myData["Objective Function"])
    print (text)
    print ("The decision variables and their values are:")
    for i in myData["Variables"]:
        print (i+": " + "{:.3f}".format(myData["Variables"][i])) 





    

    
    
    
    
    
    
    
    