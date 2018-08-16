SELECT tu.UserID
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
           AND trm.MovieID = tm.MovieID;