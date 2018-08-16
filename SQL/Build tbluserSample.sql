---create a set of 100 sample users (all of whom have recommendations) for querying

SELECT usr.UserID, IDENTITY(INT,1,1) AS MyID
INTO dbo.#T
FROM dbo.tblRecommendation AS rec
    INNER JOIN dbo.tblUser usr
        ON usr.UserID = rec.UserID
    INNER JOIN dbo.tblMovie AS tm
        ON tm.MovieID = rec.MovieID
ORDER BY  IIF( usr.UserID % 10 = 0	, 1, 0) DESC, IIF( usr.UserID % 9 = 0	, 1, 0) DESC


SELECT DISTINCT TOP 100
       t.UserID
INTO dbo.tblUserSample
FROM dbo.#T AS t;


DROP TABLE  dbo.#T

