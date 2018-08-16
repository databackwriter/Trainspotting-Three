ALTER TABLE tblMovie ADD ReleaseYear SMALLINT;
GO
UPDATE tm
SET tm.Title = REPLACE(tm.Title, u.ShortYear, '')
  , tm.ReleaseYear = REPLACE(REPLACE(u.ShortYear, '(', ''), ')', '')
FROM dbo.tblMovie tm
    INNER JOIN
    (
        SELECT MovieID
             , REVERSE(LEFT(REVERSE(RTRIM(Title)), 6)) AS ShortYear
        FROM dbo.tblMovie
    ) u
        ON tm.MovieID = u.MovieID;