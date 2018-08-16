#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 06:06:34 2018

@author: petermoore

Inspired by http://www.awesomestats.in/python-recommending-movies/
"""

import os
#import numpy as np

import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


#change working directory
PATH_FILE = "/Users/petermoore/Documents/GitHub/Movies/Trainspotting Three"#os.path.dirname(os.path.realpath(__file__))
os.chdir(PATH_FILE)
import datainout
PATH_ME = os.getcwd()

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
    INNER JOIN dbo.tblRecommendation trm
        ON trm.UserID = tu.UserID
           AND trm.MovieID = tm.MovieID;"""

df = datainout.sqldf(sql)


rating_df = datainout.sqldf("select * from tblRating")
movies_df = datainout.sqldf("select * from tblMovie")

rating_df.drop( "Timestamp", inplace = True, axis = 1 )


from sklearn.metrics import pairwise_distances



#Create the pivot tablen(straight from http://www.awesomestats.in/python-recommending-movies/)
user_movies_df = rating_df.pivot( index='UserID', columns='MovieID', values = "Rating" ).reset_index(drop=True)
user_movies_df.fillna( 0, inplace = True )

user_sim = 1 - pairwise_distances(user_movies_df.as_matrix(), metric="cosine" )


np.fill_diagonal( user_sim, 0 )

user_sim_df = pd.DataFrame(user_sim)
user_sim_df.set_index(index)
user_sim_dfT = user_sim_df.T
type(user_sim_dfT)
user_sim_dfT.shape
datainout.loadtosqlstage(df=user_sim_df, stagetablename="tblUserxUserCollaborativeFiltering", ifexists="replace")