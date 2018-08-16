DROP TABLE IF EXISTS dbo.tblUserSamplexMovie;
GO
SELECT  usr.UserID
     , mov.MovieID
     , CAST(0 AS FLOAT)  AS Recommended
     , CAST(0 AS FLOAT)  AS HasAntecendants	   
	, CAST(0 AS FLOAT) AS Lift

INTO dbo.tblUserSamplexMovie
FROM dbo.tblUser usr
    CROSS JOIN dbo.tblMovie mov
    LEFT OUTER JOIN dbo.tblRecommendation AS tr
        ON tr.UserID = usr.UserID
           AND mov.MovieID = tr.MovieID
           AND tr.AlreadySeen = 0
WHERE usr.UserID IN
      (
          SELECT UserID FROM dbo.tblUserSample
      )
      AND tr.MovieID IS NULL; --ignore stuff already seen


GO
GO
ALTER TABLE dbo.tblUserSamplexMovie ADD CONSTRAINT
	PK_tblUserSamplexMovie PRIMARY KEY CLUSTERED 
	(
	UserID,
	MovieID
	) WITH( STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
