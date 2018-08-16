#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 12:34:58 2018

@author: petermoore

PCA code inpired by http://scikit-learn.org/stable/auto_examples/decomposition/plot_pca_iris.html
and http://jotterbach.github.io/2016/03/24/Principal_Component_Analysis/
"elbow" curve inspired by http://www.michaeljgrogan.com/k-means-clustering-python-sklearn/

The following quote about Zip Codes comes from https://people.howstuffworks.com/usps4.htm
"The first digit represents the state. Numbers increase as you move west. Several states share each digit — 2,
for example, represents the District of Columbia, Maryland, North Carolina, South Carolina, Virginia and West Virginia."
"""

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import datainout
plt.rcParams['figure.figsize'] = (5,4)
BASEDIR="/Users/petermoore/Documents/GitHub/Movies/Trainspotting Two";MOVIEDIR = BASEDIR+"/ml-1m";USERSFILE = MOVIEDIR+"/users.dat"
USERSSCHEMA={"UserID":np.int32, "Gender":np.object, "Age":np.float32, "Occupation":np.int32, "ZipCode":np.object}#NB names changed to match readme schema: UserID::Gender::Age::Occupation::Zip-code

userstrainingdata, userstestdata, usersrowcount, usersschemaout = datainout.splitdatdata(trainingproportion=1.0, datFILE=USERSFILE, datSCHEMA=USERSSCHEMA)
r,c=userstrainingdata.shape
userlocal = userstrainingdata
userlocal.insert(loc=c, column="ShortZip", value=userstrainingdata.ZipCode.str.slice(0, 2).astype(np.int32), allow_duplicates=False)# first two digits of zip code
userlocal["GenderN"] = 0.0

def normalizedata(Y): return (Y - Y.mean()) / (Y.max() - Y.min())
userlocal.loc[userlocal["Gender"] == "M","GenderN"] = 0 # make male and female numeric (because pca likes floats)
userlocal.loc[userlocal["Gender"] == "F","GenderN"] = 1
userlocal["AgeN"] =  normalizedata(userlocal["Age"])
userlocal["OccupationN"] =  normalizedata(userlocal["Occupation"])
userlocal["ShortZipN"] =  normalizedata(userlocal["ShortZip"])


X=userlocal[["GenderN", "Occupation", "Age"]]

#try some Kmeans
ntrials = 20
Nc = range(1,ntrials+1)
#fieldlist = ["GenderN", "OccupationN", "AgeN", "ShortZipN"]
ltitle = "Elbow curve for: "
for l in list(X):#fieldlist:
    Y = X[[l]]
    kmeans = [KMeans(n_clusters=i) for i in Nc]
    score = [kmeans[i].fit(Y).score(Y) for i in range(len(kmeans))]
    plt.plot(Nc,score, label =l)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Score')
    ltitle = ltitle + l +','

plt.title(ltitle)
leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)
plt.show()



X=X.values#copnvert to numpy array


fig=plt.figure()
ax = Axes3D(fig)
ax.scatter(X[:,0], X[:,1], X[:,2])
k = 3
kmeans = KMeans(n_clusters=k)
kmeans = kmeans.fit(X)
labels = kmeans.predict(X)

C=kmeans.cluster_centers_

fig=plt.figure()
ax = Axes3D(fig)
ax.scatter(X[:,0], X[:,1], X[:,2])
ax.scatter(C[:,0], C[:,1], C[:,2], marker="*",c="#050505", s=1000)



