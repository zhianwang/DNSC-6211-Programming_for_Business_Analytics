# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 16:49:09 2016

@author: Zhian Wang
GWID: G33419803

Analyzing sereal data files by puting them into a dataframe, 
compute the total births, seclect top 5 names, plot a graph, etc.
"""

import time
import pandas as pd

def getData():
    """
    Reads multiple files and returns contents in a pandas dataframe.
    
    Args:
        None:
    Requests for the name of the path for the files in the program
    Returns:
        a list with the file contents
    """
    
    start_time = time.time()
    
    #get path name, ending with /
    pathname = input("Please provide the path for the name files ...")
    
    
    # Create empty dataframe
    dfAll=pd.DataFrame({'Name' : [],'Sex' : [],'Count' : [],'Year' : []})

    print ('Started ...')
    for year in range(1880,2016):
        filename = 'yob'+str(year)+'.txt'
        filepath = pathname + filename
        # Read a new file into a dataframe
        df = pd.read_csv(filepath, header=None)
        df.columns = ['Name', 'Sex', 'Count']
        df['Year'] = str(year)
        dfAll = pd.concat([dfAll,df])  
    
    print('Done...')
    print ('It took', round(time.time()-start_time,4), 'seconds to read all the data into a dataframe.')
    
    return (dfAll)
    
#Part1
def q1(myDF):
    """
    Compute total number of births for each year and provide a formatted printout of that
    
    Args:
        filename: the pandas dataframe with all data
    Returns:
        Nothing
    """
    
    dfCount = myDF['Count'].groupby(myDF['Year']).sum()
    s = '{:>5}'.format('Year')
    s = s + '{:>10}'.format('Births')
    print(s)
    for myIndex, myValue in dfCount.iteritems():
        s = '{:>5}'.format(myIndex)
        s = s + '{:>10}'.format(str(int(myValue)))
        print (s)
        
#Part2        
def q2(myDF):
    """
    Compute the total births each year (from 1990 to 2014) for males and females
    and provide a plot for that.
    
    Args:
        filename: the pandas dataframe with all data
    Returns:
        Nothing
    """
    
    import matplotlib                # import the libraries to plot
    matplotlib.style.use('ggplot')   # set the plot style to ggplot type

    # Exceute the condition provided in the assignment
    dfSubset = myDF[ (myDF['Year'] >= '1990') & (myDF['Year'] <= '2014') ]
    # Subset by sex and sum the variable of interest 
    dfCountBySex = dfSubset['Count'].groupby(dfSubset['Sex']).sum()
    # dfCountBySex                     # Display the data frame
    dfCountBySex.plot.bar()            # Draw the bar plot
    
    
# Part3
def q3(myDF):
    """
    Print the top 5 names for each year starting 1950.
    
    Args:
        filename: the pandas dataframe with all data
    Returns:
        Nothing
    """
    
    # Prepare header
    s = ''
    s = '{:>5}'.format('Year')
    s = s + '{:>10}'.format('Name 1')
    s = s + '{:>10}'.format('Name 2')
    s = s + '{:>10}'.format('Name 3')
    s = s + '{:>10}'.format('Name 4')
    s = s + '{:>10}'.format('Name 5')
    # Print header
    print (s)
    # Now go through all the years for the report
    for i in range(1950,1954):
        fn = myDF[(myDF['Year'] == str(i))]                   # Create a data frame for a matching year
        fn = fn.sort_values('Count', ascending=False).head(5)   # Sort by count and retain the top five rows
        s = ''
        s = s = s + '{:>5}'.format(str(i))
        # Now iterate through the data frame with five records
        for idx, row in fn.iterrows():
            s = s + '{:>10}'.format(row["Name"])
        print(s)


# Part4    
def q4(dfAll):
    """
    Find the top 3 female and top 3 male names for years 2010 and up
    and plot the frequency by gender.
    
    Args:
        filename: the pandas dataframe with all data
    Returns:
        Nothing
    """
    
    # Prepare header
    s = ''
    s = '{:>5}'.format('Year')
    s = s + '{:>10}'.format('Female1')
    s = s + '{:>10}'.format('Female2')
    s = s + '{:>10}'.format('Female3')
    s = s + '{:>10}'.format('Male1')
    s = s + '{:>10}'.format('Male2')
    s = s + '{:>10}'.format('Male3')
    # Print header
    print (s)
    
    # creat a dataframe for concatanating the data of each year
    totalgraph=pd.DataFrame({'Count' : [],'Name' : [],'Sex' : [],'Year': []})
    
    # Now go through all the years for the report
    for i in range(2010,2016):
        #rearrange the data by year and sex
        fnFemale = dfAll[(dfAll['Year'] == str(i)) & (dfAll['Sex'] == 'F')] 
        fnMale = dfAll[(dfAll['Year'] == str(i)) & (dfAll['Sex'] == 'M')] 
        # sort by Count and retain the top three
        fn1 = fnFemale.sort_values('Count', ascending=False).head(3)  
        fn2 = fnMale.sort_values('Count', ascending=False).head(3)
        # concatanate the female data and male data
        FandM = pd.concat([fn1,fn2])
        #concatanate the data of each year in the new blank dataframe
        totalgraph = pd.concat([totalgraph,FandM])
        
        #print the table
        s = ''
        s = s + '{:>5}'.format(str(i))
    
        for idx, row in FandM.iterrows():
            s = s + '{:>10}'.format(row["Name"])

        print(s)
    
    
    
    import matplotlib                # import the libraries to plot             
    matplotlib.style.use('ggplot')   # set the plot style to ggplot type
    
    
    dfCountBySex = totalgraph['Count'].groupby(totalgraph['Sex']).sum()
    # dfCountBySex                     # Display the data frame
    dfCountBySex.plot.bar()            # Draw the bar plot


# Part5    
def q5(dfAll):
    """
    Plot the trend of the Names'John','Harry','Mary'and'Marilyn' over all of the years of the data set.
    a. Stack 4 plots one over the other
    b. Plot all four trends in one plot
    
    Args:
        filename: the pandas dataframe with all data
    Returns:
        Nothing
    """
    #extract the name accordingly
    FnJ = dfAll[(dfAll['Name'] == 'John')]
    FnJ = FnJ['Count'].groupby(FnJ['Year']).sum()
    
    FnH = dfAll[(dfAll['Name'] == 'Harry')]
    FnH = FnH['Count'].groupby(FnH['Year']).sum()
    
    FnM = dfAll[(dfAll['Name'] == 'Mary')]
    FnM = FnM['Count'].groupby(FnM['Year']).sum()
    
    FnMln = dfAll[(dfAll['Name'] == 'Marilyn')]
    FnMln = FnMln['Count'].groupby(FnMln['Year']).sum()
    
    
    import matplotlib.pyplot as plt
    
    #draw the plot using the data provided above
    plt.figure(1)
    #define the x and y axis limit
    #plt.xlim([1880,2020])
    #plt.ylim([0,90000])
    FnJ.plot().text(110,80000,'---John',color='r',fontsize=15)
    
    plt.figure(2)
    FnH.plot().text(110,9000,'---Harry',color='r',fontsize=15)
    
    plt.figure(3)
    FnM.plot().text(110,70000,'---Mary',color='r',fontsize=15)
    
    plt.figure(4)
    FnMln.plot().text(90,10500,'---Marilyn',color='r',fontsize=15)
    
    #plot all trends in one plot
    plt.figure(5)
    plt.plot(FnJ,'r')
    #add the title of each line to clarify
    plt.text(1995,80000,'---John',color='r',fontsize=12)
    plt.plot(FnH,'b')
    plt.text(1995,74000,'---Harry',color='b',fontsize=12)
    plt.plot(FnM,'k')
    plt.text(1995,68000,'---Mary',color='k',fontsize=12)
    plt.plot(FnMln,'g')
    plt.text(1995,62000,'---Marilyn',color='g',fontsize=12)
    


# Part6  
def q6(dfAll):
    """
    Find the ten names that have showen the greatest variation over the years. Plot this.
    
    Args:
        filename: the pandas dataframe with all data
    Returns:
        Nothing
    """
    # Exceute the condition in the assignment
    dfCountByName = dfAll.groupby(['Name','Year']).sum()
    t = dfCountByName.reset_index()
    #compute the variation
    variation = t.groupby('Name').var()
    #sort by Count and retain the top ten
    topten = variation.sort_values('Count', ascending=False).head(10)
    
    import matplotlib.pyplot as plt
    
    plt.figure(1)
    topten.plot.bar()
    