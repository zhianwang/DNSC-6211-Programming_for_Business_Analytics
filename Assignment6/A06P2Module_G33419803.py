# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 15:50:24 2016

@author: Zhian Wang
GWID: G33419803

This program is define functions to read jason file, store it into MongoDB, creat and solve LP problems and
define two types of outputs.
"""

def getFileNames():
    """
    Input = name of JSON file
    Returns = JSON object
    """
    
    import os
    included_extensions = ['json'];
    file_names = [fn for fn in os.listdir(os.getcwd())
                  if any ([fn.endswith(ext)
                          for ext in included_extensions])];
    return file_names
    
    
def readAndStore(file_names):
    import json
    import pymongo
    # Start a mongodb client on the local machine using port 27017
    client = pymongo.MongoClient('localhost:27017')
    db = client['myDB']
    collection = db['A06']
    if (collection.count() != 0):
        collection.drop()
    collection = db['A06']
    length = len(file_names)
    #print(length)
    for i in range(0,length):
        #print(i)
        with open('/home/zwang/1-ProgrammingForBA/Homework/HW6/'+file_names[i], 'r') as f:
            jsonfile = json.load(f)
        db.A06.insert_one(jsonfile)
    
    myLP = db.A06.find()
    #print (myLP.count())
    return myLP


    
def createAndSolveLP(LPdata):
    import pulp as pu
    
    #initialise the model
    if LPdata["objective"]=="MIN":
        my_model = pu.LpProblem("My Model", pu.LpMinimize)          
    elif LPdata["objective"]=="MAX":
        my_model = pu.LpProblem("My Model", pu.LpMaximize) 
    else:
        print ("Neither max or min")
        exit(0)
        
    #make a list of decision variables
    decVars = LPdata["variables"] 
    #print (decVars)
    #input("Enter to continue...")
    
    #create a dictionary of pulp variabes with keys from input vars
    #the default lower bound is -inf, make it 0
    x = pu.LpVariable.dict('x_%s', decVars, lowBound = 0) 
    
    #Objective function data
    objCoeffList = LPdata["objCoeffs"]   
    objective = dict(zip(decVars, objCoeffList))
    
    #create the objective function
    my_model += sum([objective[i]*x[i] for i in decVars])
    
    #create the constraints
    constraintKeys = LPdata["LHS"].keys()
    
    for key in constraintKeys:
        LHScoeffs = dict(zip(decVars,LPdata["LHS"][key]))
        
        if LPdata["conditions"][key] == '<=':
            my_model +=  sum([LHScoeffs[j]*x[j] for j in decVars]) <= LPdata["RHS"][key]
        elif LPdata["conditions"][key] == '>=':
            my_model +=  sum([LHScoeffs[j]*x[j] for j in decVars]) >= LPdata["RHS"][key]   
        elif LPdata["conditions"][key] == '==':
            my_model +=  sum([LHScoeffs[j]*x[j] for j in decVars]) == LPdata["RHS"][key]                      
        else:
            print ("Problems with constraint {} ".format(key))
            exit(0)

    # Save and solve the problem
    my_model.writeLP(LPdata['name']+".lp")
    my_model.solve()
    #myProblem.solve(pu.GLPK())  
    
    lpDict = {}
    lpDict["Objective Function"] = pu.value(my_model.objective)   
    
    d = {}
    for v in my_model.variables():
        d.update({v.name:v.varValue})
    lpDict["Variables"] = d       
    #print(lpDict)
    return (lpDict)
    

def writeDatabase(tableName,myLP):
    import pymysql as myDB
    conn = myDB.connect('localhost','root','Zhianwang')
    cursor = conn.cursor()
    
    sql = 'SHOW DATABASES;'
    cursor.execute(sql)
    
    sql = 'DROP DATABASE IF EXISTS LP;'
    cursor.execute(sql)
    
    sql = 'CREATE DATABASE LP;'
    cursor.execute(sql)
    
    sql = ' USE LP; ' 
    cursor.execute(sql)
    
    sql = '''
            DROP TABLE IF EXISTS %s;
            CREATE TABLE %s(
            ProblemName CHAR(20),
            OptimalValue CHAR(20));
            '''%(tableName,tableName)
    cursor.execute(sql)
    
    for x in myLP:
        optimal = createAndSolveLP(x)
        #print(x)
        #print(optimal)
        problem_Name = x['name']
        opt_Val = optimal['Objective Function']
        sql = '''
                INSERT INTO %s VALUES ("%s","%s");
                '''%(tableName,problem_Name,opt_Val)
        cursor.execute(sql)
    cursor.execute('SELECT * FROM %s;'%(tableName))

    print("Output being sent to table: ",tableName," in the LP database")
    print("Output written to table: ",tableName," in the LP database")
    
    cursor.close()
    
    
    
def writeTXT(textFile,myLP):
    try:
        for x in myLP:
            #print(x)
            optimal = createAndSolveLP(x)
            #print(optimal)

            with open(textFile, 'a') as f:
                f.write("The problem name is "+x['name']+"\n")
                f.write("The optimal value is {:.3f}".format(optimal['Objective Function'])+"\n")
                
        print ("Output being sent to file: " + textFile)
        print ("Output written to file: " + textFile)
                
    except:
        print ("Fail to write file")
