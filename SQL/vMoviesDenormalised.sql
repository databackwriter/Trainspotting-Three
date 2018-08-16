ALTER VIEW [dbo].[vMoviesDenormalised]
AS
SELECT r.Rating
     , r.Timestamp
     , m.MovieID
     , m.Title
     --, mg.MoviexGenreID
     --, g.GenreID
     --, g.Genre
     , u.UserID
     , u.Gender
     , o.OccupationID
     , o.Occupation
     , a.AgeID
     , a.Age
     , zc.ZipcodePrimary
     , ISNULL(zc.City + ',', '') + ISNULL(zc.State + ',', '') + 'USA' AS CityState
     , zc.City
     , zc.State
     , IIF(trm.UserID IS NULL, 0, 1) AS Recommended
FROM dbo.tblRating AS r
    INNER JOIN dbo.tblMovie AS m
        ON m.MovieID = r.MovieID
    --INNER JOIN dbo.MoviexGenre AS mg
    --    ON mg.MovieID = m.MovieID
    --INNER JOIN dbo.genres AS g
    --    ON g.GenreID = mg.GenreID
    INNER JOIN dbo.tblUser AS u
        ON u.UserID = r.UserID
    INNER JOIN dbo.tblOccupation AS o
        ON o.OccupationID = u.OccupationID
    INNER JOIN dbo.tblAge AS a
        ON a.AgeID = u.AgeID
    LEFT OUTER JOIN dbo.ZipCode AS zc
        ON zc.ZipcodePrimary = u.ZipcodePrimary
    LEFT OUTER JOIN dbo.tblRecommendation trm
        ON trm.UserID = u.UserID
           AND trm.MovieID = m.MovieID;

GO


