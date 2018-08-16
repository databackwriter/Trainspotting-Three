#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parts of the code herein were
inspried by original code at cognitiveclass.ai
it can be found here (but you may have go sign up):
https://courses.cognitiveclass.ai/courses/course-v1:CognitiveClass+ML0120ENv2+2018/courseware/89227024130b43f684d95376901b65c8/e7c36d2c4c6840fe8b81b97147ea9c16/

I have marked _their_ code with #CCAI.
I have marked _their comments_ with #CCOM

"""
#get tensorflow
import tensorflow as tf
#get others
import numpy as np
import pandas as pd
import os
#import sqlalchemy

#change working directory
PATH_FILE = "/Users/petermoore/Documents/GitHub/Movies/Trainspotting Three"#os.path.dirname(os.path.realpath(__file__))
os.chdir(PATH_FILE)
import datainout
PATH_ME = os.getcwd()
PATH_DD = os.path.join(PATH_ME, "downloaded data")
PATH_LOG = os.path.join(PATH_ME,"Log")
PATH_RATINGS = os.path.join(PATH_DD,"ratings.dat")
PATH_MOVIES = os.path.join(PATH_DD,"movies.dat")
PATH_USERS = os.path.join(PATH_DD,"users.dat")
DEVICE = "/cpu:0"

#PM dictionaries for schemas
#numpy schema for python
RATINGSSCHEMA={"UserID":np.int32, "MovieID":np.int32, "Rating":np.int32, "Timestamp":np.int32}#NB names changed to match readme schema: UserID::MovieID::Rating::Timestamp
MOVIESSCHEMA={"MovieID":np.int32, "Title":np.object, "Genres":np.object}#NB names changed to match readme schema: MovieID::Title::Genres
USERSSCHEMA={"UserID":np.int32, "Gender":np.object, "AgeID":np.float32, "OccupationID":np.int32, "ZipCode":np.object}#NB names changed to match readme schema: UserID::Gender::Age::Occupation::Zip-code
##sql schema for DB
#RATINGSSCHEMA_SQL={"UserID":sqlalchemy.types.INTEGER(), "MovieID":sqlalchemy.types.INTEGER(), "Rating":sqlalchemy.types.INTEGER(), "Timestamp":sqlalchemy.types.INTEGER()}#NB names changed to match readme schema: UserID::MovieID::Rating::Timestamp
#MOVIESSCHEMA_SQL={"MovieID":sqlalchemy.types.INTEGER(), "Title":sqlalchemy.types.NVARCHAR(length=255), "Genres":sqlalchemy.types.NVARCHAR(length=255)}#NB names changed to match readme schema: MovieID::Title::Genres
#USERSSCHEMA=_SQL={"UserID":sqlalchemy.types.INTEGER(), "Gender":sqlalchemy.types.NVARCHAR(length=255), "Age":sqlalchemy.types.Float(precision=3, asdecimal=True), "Occupation":sqlalchemy.types.INTEGER(), "ZipCode":sqlalchemy.types.NVARCHAR(length=255)}#NB names changed to match readme schema: UserID::Gender::Age::Occupation::Zip-code

#get ratings, movies and users data according to schema and...
TRAININGPROPORTION = 1.0#...training proportion (initially set ot 1.0 i.e. NO TEST DATA)
                        #this is because of the way CCAI splits the data
ratingstrainingdata, ratingstestdata, ratingsrowcount, ratingsschemaout = datainout.splitdatdata(trainingproportion=TRAININGPROPORTION, datFILE=PATH_RATINGS, datSCHEMA=RATINGSSCHEMA)
moviestrainingdata, moviestestdata, moviesrowcount, moviesschemaout = datainout.splitdatdata(trainingproportion=TRAININGPROPORTION, datFILE=PATH_MOVIES, datSCHEMA=MOVIESSCHEMA)
userstrainingdata, userstestdata, usersrowcount, usersschemaout = datainout.splitdatdata(trainingproportion=TRAININGPROPORTION, datFILE=PATH_USERS, datSCHEMA=USERSSCHEMA)
#sort out problematic user fields (e.g. Zip code)
userstrainingdata = datainout.treatuserfile(userstrainingdata)


#load to a sql database
datainout.loadtosqlstage(df =ratingstrainingdata, stagetablename="tblRating", ifexists="fail")
datainout.loadtosqlstage(df =moviestrainingdata, stagetablename="tblMovie", ifexists="fail")
datainout.loadtosqlstage(df =userstrainingdata, stagetablename="tblUser", ifexists="fail")

#get release year for movie intra-SQL based on what we already have
if not datainout.fieldexists("tblMovie", "ReleaseYear"):
    PATH_YEARSQL = os.path.join(PATH_ME, "Split Movie Year.txt")
    datainout.runsqltxt(script=PATH_YEARSQL)


#build age and occupation based off readme data
dictAge={
 1:"Under 18",
18:"18-24",
25:"25-34",
35:"35-44",
45:"45-49",
50:"50-55",
56:"56+"}

dictOccupation={
 0:"other or not specified",
 1:"academic/educator",
 2:"artist",
 3:"clerical/admin",
 4:"college/grad student",
 5:"customer service",
 6:"doctor/health care",
 7:"executive/managerial",
 8:"farmer",
 9:"homemaker",
10:"K-12 student",
11:"lawyer",
12:"programmer",
13:"retired",
14:"sales/marketing",
15:"scientist",
16:"self-employed",
17:"technician/engineer",
18:"tradesman/craftsman",
19:"unemployed",
20:"writer"}

dfAge = pd.DataFrame.from_dict(data=dictAge, orient='index',columns=["Age"])
datainout.loadtosqlstage(df=dfAge, stagetablename="tblAge", ifexists="fail",index=True,indexlabel="AgeID")
dfOccupation = pd.DataFrame.from_dict(data=dictOccupation, orient='index',columns=["Occupation"])
datainout.loadtosqlstage(df=dfOccupation, stagetablename="tblOccupation", ifexists="fail",index=True,indexlabel="OccupationID")

#build a genre table intra-SQL based on what we already have
if not datainout.tableexists("tblGenre"):
    PATH_GENRESQL = os.path.join(PATH_ME, "Build Movie x Genre.txt")
    datainout.runsqltxt(script=PATH_GENRESQL)

#to this line the code is original, from this point the code echoes CCAI more closely
#############################START OF CCAI TRAINING MODEL#############################
"""
CCOM
 For our model, the input is going to contain X neurons, where X is
 the amount of movies in our dataset. Each of these neurons will possess
 a normalized rating value varying from 0 to 1 -- 0 meaning that a user
 has not watched that movie and the closer the value is to 1, the more
 the user likes the movie that neuron's representing. These normalized
 values, of course, will be extracted and normalized from the ratings
 dataset.

After passing in the input, we train the RBM on it and have the hidden
layer learn its features. These features are what we use to reconstruct
the input, which in our case, will predict the ratings for movies that
the input hasn't watched, which is exactly what we can use to recommend
movies!

We will now begin to format our dataset to follow the model's expected input
"""
#get a new unborken ID (there are missing MovieIDs)
moviestrainingdata['List Index'] = moviestrainingdata.index #PM duplicate with my code to be tidied if time
#CCAI Merging movies_df with ratings_df by MovieID
merged_df = moviestrainingdata.merge(ratingstrainingdata, on='MovieID')
#CCAI Dropping unecessary columns
merged_df = merged_df.drop('Timestamp', axis=1).drop('Title', axis=1).drop('Genres', axis=1)


#Group up by UserID
userGroup = merged_df.groupby('UserID')

"""
CCOM
Now, we can start formatting the data into input for the RBM.
We're going to store the normalized users ratings into a list of lists called trX.
"""
#CCAI: Amount of users used for training
amountOfUsedUsers = 1000 #PM changed from 1000
#CCAI: Creating the training list
trX = []
#CCAI: For each user in the group
for userID, curUser in userGroup:
    #CCAI: Create a temp that stores every movie's rating
    temp = [0]*moviesrowcount#PM changed from len(movies_df)
    #CCAI: For each movie in curUser's movie list
    for num, movie in curUser.iterrows():
        #CCAI: Divide the rating by 5 and store it
        temp[movie['List Index']] = movie['Rating']/5.0
    #CCAI: Now add the list of ratings into the training list
    trX.append(temp)
    #CCAI: Check to see if we finished adding in the amount of users for training
    if amountOfUsedUsers == 0:
        break
    amountOfUsedUsers -= 1

"""
PM
NB up to this point we haven't done anything in Tensorflow,
we've just rearranged the data so that users movies and ratings
are iterable
"""

hiddenUnits = 40 #PM changed from 20
visibleUnits = moviesrowcount#PM changed from len(movies_df)
#CCAI: Phase 1: Input Processing
sess = tf.Session()
sess.run(tf.global_variables_initializer())


import LearnModel

prv_w, prv_vb, prv_hb, W, vb, hb, v0 = LearnModel.buildviewinghabits(sess,trX,hiddenUnits, visibleUnits)

"""
CCOM
Recommendation
We can now predict movies that an arbitrarily selected user might like.
This can be accomplished by feeding in the user's watched movie
preferences into the RBM and then reconstructing the input.
The values that the RBM gives us will attempt to estimate the user's preferences
for movies that he hasn't watched based on the preferences of the users that
the RBM was trained on.
"""


#PM Selecting the input user coverted to loop
#usrs =[]
for pu in range(len(trX)):
    #CCIA: Feeding in the user and reconstructing the input
    UserID = merged_df.iloc[pu]["UserID"]
    hh0 = tf.nn.sigmoid(tf.matmul(v0, W) + hb)
    vv1 = tf.nn.sigmoid(tf.matmul(hh0, tf.transpose(W)) + vb)
    feed = sess.run(hh0, feed_dict={ v0: [trX[pu]], W: prv_w, hb: prv_hb})
    rec = sess.run(vv1, feed_dict={ hh0: feed, W: prv_w, vb: prv_vb})

    #CCIA:  We can then list the 20 most recommended movies for our mock user by sorting it by their scores given by our model.
    scored_movies_df = moviestrainingdata #PM names changed to a generic name
    scored_movies_df["Recommendation Score"] = rec[0]
    px = scored_movies_df.sort_values(["Recommendation Score"], ascending=False).head(20)
    px["UserID"] = UserID
    datainout.loadtosqlstage(df=px, stagetablename="tblRecommendation", ifexists="append")
    if pu % 25 == 0:
        print("Now loaded through " + str(pu) + " iterations")

print("fin")