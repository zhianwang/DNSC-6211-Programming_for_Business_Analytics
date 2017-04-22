# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 16:01:42 2016

@author: Group3

Main function of scraping Yelp.
"""

import A03Mod_Group3 as md

url="https://www.yelp.com/search?find_desc=mexican+food&find_loc=Washington%2C+DC"

md.step1(url)

url2=url="https://www.yelp.com/search?find_desc=chinese+food&find_loc=Washington%2C+DC"

md.step1(url2)

md.step2("mexican.csv","chinese.csv")

md.step3("mexican.csv","chinese.csv")

md.step4("mexican.csv","chinese.csv")
