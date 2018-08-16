#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 06:06:34 2018

@author: petermoore

Inspired by http://pbpython.com/market-basket-analysis.html
"""

import os
#import numpy as np


import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 5)


#change working directory
PATH_FILE = "/Users/petermoore/Documents/GitHub/Movies/Trainspotting Three"#os.path.dirname(os.path.realpath(__file__))
os.chdir(PATH_FILE)
import datainout
PATH_ME = os.getcwd()
#read amalgamated data from data model
sql="""SELECT tu.UserID
     , tr.Rating
     , tm.MovieID
     , tm.Title
     , ta.Age
FROM dbo.tblRating AS tr
    INNER JOIN dbo.tblMovie AS tm
        ON tm.MovieID = tr.MovieID
    INNER JOIN dbo.tblUser AS tu
        ON tu.UserID = tr.UserID
    INNER JOIN dbo.tblAge ta
        ON ta.AgeID = tu.AgeID
    AND tu.UserID IN (SELECT UserID FROM dbo.tblUserSample)"""
#get dataframe from sql statement
df = datainout.sqldf(sql)

#this is very close to the code at http://pbpython.com/market-basket-analysis.html
basket = (df#[df['Age'] =="18-24"]
          .groupby(['UserID', 'MovieID'])['Rating']
          .mean().unstack().reset_index().fillna(0) #take the mean, just in case some one has rated the same movie twice
          .set_index('UserID'))

#invoke the mlxtend repository
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#function a direct copy from http://pbpython.com/market-basket-analysis.html
"""
from http://pbpython.com/market-basket-analysis.html
There are a lot of zeros in the data but we also need to make sure
any positive values are converted to a 1 and anything less the 0 is set to 0.
This step will complete the one hot encoding of the data and
remove the postage column (since that charge is not one we wish to explore
"""
def encode_units(x):
    if x <= 0:
        return 0
    if x>=1:
        return 1


#from http://pbpython.com/market-basket-analysis.html
basket_sets = basket.applymap(encode_units)

#get items iwth support of at least 20% (number ketp low to get some data)
frequent_itemsets = apriori(basket_sets,min_support=0.10,use_colnames=True)
#get the association rules
rules = association_rules(frequent_itemsets, metric = "lift", min_threshold=1)


#only retain those rules with a lift over 1.2 and over 20% confidence
rules2 = rules[ (rules['lift'] >= 2.0) &
        (rules['confidence'] >= 0.2)]


#import association rules to SQL
import pyodbc
conn = pyodbc.connect('DSN=MYMSSQL_MOVIES;UID=sa;PWD=notapassword', autocommit=True)
crsr = conn.cursor()
crsr.execute("DELETE FROM dbo.tblRuleAsssociationxRulePrecedent")
crsr.execute("DELETE FROM dbo.tblRuleAsssociation")
crsr.close()

insertmajor = """
EXEC  dbo.usp_PM_RuleAsssociation_Insert   @antecedentsupport = ?
  , @consequentsupport = ?
  , @support = ?
  , @confidence = ?
  , @lift = ?
  , @leverage = ?
  , @conviction = ?
"""
insertminor = """
EXEC dbo.usp_PM_RuleAsssociationxRulePrecedent_Insert
    @RuleAsssociationFK = ?
  , @RulePrecedentFK = ?
  , @MovieFK =?
"""
for index, row in rules2.iterrows():
    antecedants=(row['antecedants'])
    consequents=(row['consequents'])
    paramsmajor=[row['antecedent support'],row['consequent support'],row['support'],
            row['confidence'],row['lift'],row['leverage'],row['conviction']]
    with conn.cursor() as cur:
        RuleAsssociationID = cur.execute(insertmajor, paramsmajor).fetchall()
        RuleAsssociationID = [int(L[0]) for L in RuleAsssociationID]
        RuleAsssociationID = (int(RuleAsssociationID[0]))
        for _p in list(antecedants):
            paramsminor = [RuleAsssociationID,1,_p]
            cur.execute(insertminor, paramsminor)
        for _q in list(consequents):
            paramsminor = [RuleAsssociationID,2,_q]
            cur.execute(insertminor, paramsminor)
conn.close()






