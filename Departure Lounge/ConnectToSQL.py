#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 16:05:01 2018

@author: petermoore
"""



import pyodbc



#¢the DSN value should be the name of the entry in odbc.ini, not freetds.conf
conn = pyodbc.connect('DSN=MYMSSQL_MOVIES;UID=sa;PWD=l00katy0urd%t%a',autocommit=True)
crsr = conn.cursor()
#rows = crsr.execute("use movies")
#rows = crsr.execute("CREATE TABLE tbl2(MyID INT IDENTITY(1,1) PRIMARY KEY NOT NULL, MyVal VARCHAR(50))")
#rows = crsr.execute("INSERT INTO tbl2(MyVal) VALUES(GETDATE())")
rows = crsr.execute("select * from tbl2").fetchall()
print(rows)
crsr.close()
conn.close()
#
import sqlalchemy

engine = sqlalchemy.create_engine("mssql+pyodbc://sa:l00katy0urd%t%a@MYMSSQL_Movies")

import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))
df.head
# write the DataFrame to a table in the sql database
df.to_sql(name="test", con = engine, if_exists='replace')


conn = pyodbc.connect('DSN=MYMSSQL_MOVIES;UID=sa;PWD=l00katy0urd%t%a',autocommit=True)
crsr = conn.cursor()
#rows = crsr.execute("use movies")
#rows = crsr.execute("CREATE TABLE tbl2(MyID INT IDENTITY(1,1) PRIMARY KEY NOT NULL, MyVal VARCHAR(50))")
#rows = crsr.execute("INSERT INTO tbl2(MyVal) VALUES(GETDATE())")
rows = crsr.execute("select * from test").fetchall()
print(rows)
crsr.close()
conn.close()

#import os
#os.environ

#stagetablename = "tblMovie"
#connectionstring='DSN=MYMSSQL_MOVIES;UID=sa;PWD=l00katy0urd%t%a'
#params=stagetablename
#conn = pyodbc.connect(connectionstring, autocommit=True)
#crsr = conn.cursor()
#rows = crsr.execute("select name from sys.tables where name = ?", params).fetchall()
#crsr.close()
#conn.close()