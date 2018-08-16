UPDATE rec
SET rec.AlreadySeen = 1
FROM dbo.tblRecommendation AS rec
    INNER JOIN dbo.tblUser usr
        ON usr.UserID = rec.UserID
    INNER JOIN dbo.tblMovie AS tm
        ON tm.MovieID = rec.MovieID
    INNER JOIN dbo.tblRating AS rat
        ON rat.MovieID = tm.MovieID
           AND rat.UserID = usr.UserID;