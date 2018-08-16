#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 15:00:55 2018
Original code to read data files and split them into test versus traing sets
@author: petermoore
"""
import numpy as np
import pandas as pd
#code to take a data frame (df) and place in a staging area of a named connection
import sqlalchemy
import pyodbc
#read .dat or .csv file with a specified schema
def readdatfile(filename, sep, dataschema):
    colHeaders=list(dataschema.keys())
    datafromfile = pd.read_csv(filepath_or_buffer=filename,sep=sep,header=None,names=colHeaders, dtype=dataschema,engine='python')
    rowcount=len(datafromfile)
    #add a local id to account for missing IDs
#    datafromfile["LocalInd"] = datafromfile.index
    return datafromfile, rowcount

#get a dat file, read it (using above function) and split it into trainingproportion
#return training set, test set and the redefined schema
#NB redfined schema incudes row counts
def splitdatdata(trainingproportion, datFILE, datSCHEMA):
    dfdat, dfdatrows = readdatfile(filename=datFILE, sep="::", dataschema=datSCHEMA)
#    newind=np.random.permutation(dfdatrows)#random permutation of indices to reseed
#    dfdat = dfdat.iloc[newind].reset_index(drop=True)
    splitind = int(dfdatrows*trainingproportion)
    dfdattrain = dfdat[0:splitind]
    dfdattest = dfdat[splitind:]#.reset_index(drop=True)
    dfSchema = datSCHEMA
    def endwithcount(x): return x.endswith("ID") #local funtion to isolate "count" fields
    for counted in filter(endwithcount,list(dfSchema.keys())):
        countresult = len(dfdat.groupby(counted)) #loop to get count fields
        dfSchema[counted+"Count"] = countresult
    return dfdattrain,dfdattest,dfdatrows, dfSchema

#code for specific user file functions
def treatuserfile(userstrainingdata):
    #add short two digit zip
    userstrainingdata["ZipShort"] = userstrainingdata.ZipCode.str.slice(0, 2).astype(np.int32)
    userstrainingdata["ZipcodePrimary"] = userstrainingdata.ZipCode.str.slice(0, 5).astype(np.int32)
    return userstrainingdata


#function to check if a table exists
def tableexists(stagetablename ,connectionstring='DSN=MYMSSQL_MOVIES;UID=sa;PWD=notapassword'):
    extant = False
    params=stagetablename
    conn = pyodbc.connect(connectionstring, autocommit=True)
    crsr = conn.cursor()
    rows = crsr.execute("select name from sys.tables where name = ?", params).fetchall()
    crsr.close()
    conn.close()
    if len(rows)> 0:
        extant = True
    return extant


#function to check if a field exists
def fieldexists(stagetablename, stagefieldname,connectionstring='DSN=MYMSSQL_MOVIES;UID=sa;PWD=notapassword'):
    extant = False
    params=[stagetablename, stagefieldname]
    conn = pyodbc.connect(connectionstring, autocommit=True)
    crsr = conn.cursor()
    rows = crsr.execute("SELECT t.name, c.name FROM sys.tables t INNER JOIN sys.columns AS c ON c.object_id = t.object_id WHERE t.name = ?  AND c.name = ?;", params).fetchall()
    crsr.close()
    conn.close()
    if len(rows)> 0:
        extant = True
    return extant




def loadtosqlstage(df,
                   stagetablename,
                   connectionstring="mssql+pyodbc://sa:notapassword@MYMSSQL_Movies",
                   ifexists='replace',
                   index=False,
                   indexlabel=None,
                   dtype=None):
    engine = sqlalchemy.create_engine(connectionstring)

    BuildDF = True
    if ifexists == "fail":#if set to failure when table exists the don't build
        if tableexists(stagetablename):
            BuildDF = False

     # write the DataFrame to a table in the sql database
    if BuildDF:
        df.to_sql(name=stagetablename, con = engine, if_exists=ifexists, index=index, index_label=indexlabel,dtype=dtype)

#function to run SQL from a text file
#indirectly inspired by: https://stackoverflow.com/questions/38856534/execute-sql-file-with-multiple-statements-separated-by-using-pyodbc
def runsqltxt(script,connectionstring='DSN=MYMSSQL_MOVIES;UID=sa;PWD=notapassword'):
    conn = pyodbc.connect(connectionstring, autocommit=True)
    with open(script,'r') as actions:
        sqlScript = actions.read()
        print(sqlScript)
        for statement in sqlScript.split(';'):
            with conn.cursor() as cur:
                cur.execute(statement)
    conn.close()


#function to make a dataframe from a sql startement
#indirectly inspired by: https://stackoverflow.com/questions/39835770/move-data-from-pyodbc-to-pandas
def sqldf(sql,connectionstring='DSN=MYMSSQL_MOVIES;UID=sa;PWD=notapassword'):
    conn = pyodbc.connect(connectionstring, autocommit=True)
    df = pd.read_sql(sql,conn)
    return df

