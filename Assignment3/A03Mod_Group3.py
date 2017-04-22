# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 12:19:20 2016

@author: Group 3

Scraping the data from Yelp about Mexican restaurants and Chinese restaurants and save them into csv files.
Make statistic analysis based on the data.
"""

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score
from matplotlib import cm  
from mpl_toolkits.mplot3d import *
import re
import time


def step1(url):
    time.sleep(3)
    myList = []
    filename=str(url)
    pos=filename.find('=')
    pos2=filename.find('+')
    filename=filename[pos+1:pos2]
    while(url):
        time.sleep(3)
        r = requests.get(url)
        data = r.text    
        soup = bs(data, "html.parser")
        lists=soup.findAll('li',{'class':'regular-search-result'})
        for list in lists:
            restaurants = list.findAll('div',{'class':'search-result natural-search-result'})
            for restaurant in restaurants:        
                c = []
                #extract the restaurant Name
                name = restaurant.find('a',{'data-analytics-label':'biz-name'})
                c.append(name.getText().strip())
                
                #extract the address
                address = restaurant.select("address")
                address = str(address)
                street = re.search('\n            (.+?)<br>',address)
                if street is None:
                    c.append('None') #street
                    city = re.search('<br>(.+?),',address)
                    if city is None:
                        c.append('') #city
                        c.append('None') #state
                        c.append('None') #zip
                    elif city is not None:
                        city = re.search('<br>(.+?),',address).group(1)
                        c.append(city)
                        state = re.search(',(.+?)',address)
                        if state is not None:
                            state = state.group(1)
                            c.append(state)
                            zip = re.search(' (\d{5})\n',address)
                            if zip is not None:
                                zip = zip.group(1)
                                c.append(zip)
                            elif zip is None:
                                c.append('None')
                        elif state is None:
                            c.append('None')
                            c.append('None')
                elif street is not None:
                    street = re.search('\n            (.+?)<br>',address).group(1)
                    c.append(street)
                    city = re.search('<br>(.+?),',address).group(1)
                    city = re.search('<br>(.+?),',address)
                    if city is None:
                        c.append('None') #city
                        c.append('None') #state
                        c.append('None') #zip
                    elif city is not None:
                        city = re.search('<br>(.+?),',address).group(1)
                        c.append(city)
                        state = re.search(',(.+?) ',address)
                        if state is not None:
                            state = state.group(1)
                            c.append(state)
                            zip = re.search(' (\d{5})\n',address)
                            if zip is not None:
                                zip = zip.group(1)
                                c.append(zip)
                            elif zip is None:
                                c.append('None')
                        elif state is None:
                            c.append('None')
                            c.append('None')           
                #get the phone number
                phone = restaurant.find('span',{'class':'biz-phone'})
                c.append(phone.getText().strip())
                #get review number
                reviewNum = restaurant.find('span',{'class':'review-count rating-qualifier'})
                if reviewNum is not None:
                    reviewNum = reviewNum.getText().strip().split(' ')
                    c.append(int(reviewNum[0]))
                else:
                    c.append('')
                #get rating stars
                rating = restaurant.find('div',{'class':'rating-large'})
                if rating is not None:
                    rating = rating.img.get('alt')
                    rating = rating.split(' ')
                    c.append(float(rating[0]))
                if rating is None:
                    c.append('')
                #get price
                price = restaurant.find('span',{'class':'bullet-after'})
                if price is not None:
                    c.append(price.getText().strip())
                if price is None:
                    c.append('')

                myList.append(c)
        nexturl = soup.find('a',{'class':'u-decoration-none next pagination-links_anchor'})
        if nexturl is None:
            #add the heading
            headings = ['Name', 'StreetAddress','City','State','Zip','Phone','Number of Reviews','Rating','Price Ranges']
            df = pd.DataFrame(myList, columns=headings)
            #save to csv file
            df.to_csv(filename+'.csv')
            return(df)
            break
        else:
            nexturl = nexturl.get('href')
            url = "https://www.yelp.com"+nexturl


def step2(file1,file2):
    """
    input = the two dataframes
    output = two pdf of the rating plot
    """
    #read the csv files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    dfMexicanRating = df1['Rating']
    dfChineseRating = df2['Rating']
    #plot the histogram of Rating
    plot1 = plt.figure(1)
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.suptitle('Rating for Mexican Food')
    dfMexicanRating.hist()
    #save the figure to file
    plot1.savefig("histRatingMexican.pdf")
    plot2 = plt.figure(2)
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.suptitle('Rating for Chinese Food')
    dfChineseRating.hist()
    plot2.savefig("histRatingChinese.pdf")

    
def step3(file1,file2):
    """
    input = the two dataframes
    output = four pdf for two different relationships of 
             mexican restaurant and chinese restaurant
    """

    #mxy1#
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    dfm = handlePrice(df1)
    #Plot the relationship between Rating (Y) and Price Range (X)
    dfmrating = dfm['Rating']
    dfmprice = dfm['Price Ranges']
    dfmrp = pd.DataFrame({"price":dfmprice,"rating":dfmrating})
    x1 = dfmrp[(dfmrp["price"]==10)]
    x2 = dfmrp[(dfmrp["price"]==20)]
    x3 = dfmrp[(dfmrp["price"]==30)]
    x4 = dfmrp[(dfmrp["price"]==40)]
    dataMRP=[x1 , x2, x3, x4]
    plot3 = plt.figure(3)
    plt.boxplot(dataMRP)
    plt.xlabel('Price Ranges')
    plt.ylabel('Rating')
    plt.title("Relationship between Rating and Price for Mexican")   
    plot3.savefig("MXY1.pdf")

    #mxy2#
    #Plot the relationship between Rating (Y) and Number of reviews (X)
    x = dfm['Number of Reviews']
    y = dfm['Rating']
    fit = np.polyfit(x,y,1)
    fit_fn = np.poly1d(fit)
    plot4 = plt.figure(4)
    plt.xlabel('Number of Reviews')
    plt.ylabel('Rating')
    plt.suptitle('Relationship between Rating and Number of Reviews for Mexican')
    plt.plot(x,y,'yo',x,fit_fn(x), '--k')
    plot4.savefig("MXY2.pdf")
    
    #cxy1#
    dfc = handlePrice(df2)
    dfcrating = dfc['Rating']
    dfcprice = dfc['Price Ranges']
    dfcrp = pd.DataFrame({"price":dfcprice,"rating":dfcrating})
    x1 = dfcrp[(dfcrp["price"]==10)]
    x2 = dfcrp[(dfcrp["price"]==20)]
    x3 = dfcrp[(dfcrp["price"]==30)]
    x4 = dfcrp[(dfcrp["price"]==40)]
    dataCRP=[x1 , x2, x3, x4]
    plot5 = plt.figure(5)
    plt.boxplot(dataCRP)
    plt.xlabel('Price Ranges')
    plt.ylabel('Rating')
    plt.title("Relationship between Rating and Price for Chinese")   
    plot5.savefig("CXY1.pdf")
    #cxy2#
    x = dfc['Number of Reviews']
    y = dfc['Rating']
    fit = np.polyfit(x,y,1)
    fit_fn = np.poly1d(fit)
    plot6 = plt.figure(6)
    plt.xlabel('Number of Reviews')
    plt.ylabel('Rating')
    plt.suptitle('Relationship between Rating and Number of Reviews for Chinese')
    plt.plot(x,y,'yo',x,fit_fn(x), '--k')
    plot6.savefig("CXY2.pdf")


def step4(file1,file2):
    """
    input = the two dataframes
    output = a list of coefficients and the pdf of 3D plot
    """
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df1 = handlePrice(df1)
    df2 = handlePrice(df2)
    df3 = df1.append(df2,ignore_index=True)
    df3 = df3.reset_index()
    myData = df3[[1,2,3]]
    df3 = myData.as_matrix()
    List = regress(df3)
    myPlot(df3,List)
    
def handlePrice (df):
    #convert the $ in price range to numbers
    df = df.dropna()
    price=[]
    for i in df["Price Ranges"]:
        price.append(10*len(i))
    rating = [i for i in df['Rating']]
    reviews = [i for i in df['Number of Reviews']]
    df = pd.DataFrame({"Rating":rating,"Price Ranges":price,"Number of Reviews":reviews})   
    df = df[['Rating','Price Ranges','Number of Reviews']]    
    return(df)
    
def handleNone(df):
    """
    input = a dataframe with None values
    output =  the dataframe without None values
    """
    df = df.dropna()
    df = df.reset_index()
    return(df)
    
def regress(myData):
    """
    Input = numpy array
    Column 1 in the array is the dependent variable
    Column 2 and 3 in the array are the independent variables
    Return = a list of coefficients
    """
    xarr = myData[:,1:]
    X = np.array([np.concatenate((v,[1])) for v in xarr])
    model = linear_model.LinearRegression(fit_intercept = True)
    yarr = myData[:,0]
    fit = model.fit(X,yarr)
    pred = model.predict(X)
    List=[fit.intercept_,fit.coef_[0],fit.coef_[1],r2_score(yarr,pred)]
    print("Intercept : ",fit.intercept_)
    print("Slope : ", fit.coef_)
    pred = model.predict(X)
    r2 = r2_score(yarr,pred) 
    print ('R-squared: %.4f' % (r2))
    return(List)
    
def myPlot(myData, b):
    """
    Input = numpy array with three columns
            Column 1 is the dependent variable
            Columns 2 and 3 are the independent variables
            and
            a column vector with the b coefficients
    Returns = Noting
    Output = 3D plot of the actual data and 
             the surface plot of the linear model
    """      
    fig = plt.figure()
    ax = fig.gca(projection='3d')               # to work in 3d
    plt.hold(True)
    
    x_max = max(myData[:,1])    
    y_max = max(myData[:,2])   
    
    b0 = float(b[0])
    b1 = float(b[1])
    b2 = float(b[2])   
    
    x_surf=np.linspace(0, x_max, 100)                # generate a mesh
    y_surf=np.linspace(0, y_max, 100)
    x_surf, y_surf = np.meshgrid(x_surf, y_surf)
    z_surf = b0 + b1*x_surf +b2*y_surf         # ex. function, which depends on x and y
    ax.plot_surface(x_surf, y_surf, z_surf, cmap=cm.hot, alpha=0.2);    # plot a 3d surface plot
    
    x=myData[:,1]
    y=myData[:,2]
    z=myData[:,0]
    ax.scatter(x, y, z);                        # plot a 3d scatter plot
    
    ax.set_xlabel('Price Range')
    ax.set_ylabel('Number of reviews')
    ax.set_zlabel('Rating')
    ax.set_title('Regress Plot')

    plt.show()
    fig.savefig("regress.pdf")