library("odbc")
library("dplyr")

con <- dbConnect(odbc(),
                 Driver = "/usr/local/lib/libtdsodbc.so",
                 Server = "10.37.129.10",
                 Database = "Movies",
                 UID = "sa",
                 PWD = "l00katy0urd%t%a",
                 Port = 5171)

result <- dbSendQuery(con, "EXEC dbo.usp_PM_XTab_GenderxGenre")

rest <- dbFetch(result)

chisq.test(rest)
