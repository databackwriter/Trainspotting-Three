DROP PROCEDURE IF EXISTS dbo.usp_PM_ROC_Curve;
GO
CREATE PROCEDURE dbo.usp_PM_ROC_Curve
AS
SELECT ra.RuleAsssociationID
     , ra.antecedentsupport
     , ra.consequentsupport
     , ra.support
     , ra.confidence
     , ra.lift
     , ra.leverage
     , ra.conviction
     , x.MovieID AS AntecendantMovieID
     , y.MovieID AS ConsequentMovieID
     , x.Title AS AntecendantTitle
     , y.Title AS ConsequentTitle
INTO dbo.#MovieTruth
FROM dbo.tblRuleAsssociation AS ra
    INNER JOIN
    (SELECT * FROM dbo.vPrecedent WHERE RulePrecedentID = 1) x --Antecedant    
        ON x.RuleAsssociationID = ra.RuleAsssociationID
    INNER JOIN
    (SELECT * FROM dbo.vPrecedent WHERE RulePrecedentID = 2) y --Consequent
        ON y.RuleAsssociationID = ra.RuleAsssociationID;

SELECT usr.UserID
     , tm.MovieID
INTO dbo.#TensorRecommends
FROM dbo.tblRecommendation AS rec
    INNER JOIN dbo.tblUser usr
        ON usr.UserID = rec.UserID
    INNER JOIN dbo.tblMovie AS tm
        ON tm.MovieID = rec.MovieID
WHERE usr.UserID IN
      (
          SELECT UserID FROM dbo.tblUserSample
      );

SELECT usr.UserID
     , tm.MovieID
INTO dbo.#AlreadySeen
FROM dbo.tblRating AS rat
    INNER JOIN dbo.tblUser usr
        ON usr.UserID = rat.UserID
    INNER JOIN dbo.tblMovie AS tm
        ON tm.MovieID = rat.MovieID
WHERE usr.UserID IN
      (
          SELECT UserID FROM dbo.tblUserSample
      );

UPDATE tusm
SET tusm.Recommended = 1
FROM dbo.tblUserSamplexMovie AS tusm
    INNER JOIN dbo.tblUser AS tu
        ON tu.UserID = tusm.UserID
    INNER JOIN dbo.tblMovie AS tm
        ON tm.MovieID = tusm.MovieID
    INNER JOIN dbo.#TensorRecommends AS tr
        ON tr.UserID = tu.UserID
           AND tr.MovieID = tm.MovieID;

UPDATE tusm
SET tusm.HasAntecendants = 1
  , tusm.Lift = mt.lift
FROM dbo.tblUserSamplexMovie AS tusm
    INNER JOIN dbo.tblUser AS tu
        ON tu.UserID = tusm.UserID
    INNER JOIN dbo.tblMovie AS tm
        ON tm.MovieID = tusm.MovieID
    INNER JOIN dbo.#MovieTruth mt
        ON tm.MovieID = mt.ConsequentMovieID --movie in row is the consequential movie
    INNER JOIN dbo.#AlreadySeen AS ase
        ON mt.AntecendantMovieID = ase.MovieID -- looking for the antecendent movie 
           AND ase.UserID = tu.UserID; --to exist for that user


SELECT uxs.Lift
     , SUM(   CASE
                  WHEN Recommended = 1
                       AND HasAntecendants = 1 THEN
                      1.0
                  ELSE
                      0.0
              END
          ) AS TruePositive
     , SUM(   CASE
                  WHEN Recommended = 1
                       AND HasAntecendants = 0 THEN
                      1.0
                  ELSE
                      0.0
              END
          ) AS FalsePositive
     , SUM(   CASE
                  WHEN Recommended = 0
                       AND HasAntecendants = 1 THEN
                      1.0
                  ELSE
                      0.0
              END
          ) AS FalseNegative
     , SUM(   CASE
                  WHEN Recommended = 0
                       AND HasAntecendants = 0 THEN
                      1.0
                  ELSE
                      0.0
              END
          ) AS TrueNegative
     , CAST(0 AS FLOAT) AS FPR
     , CAST(0 AS FLOAT) AS TPR
INTO dbo.#StayPositive
FROM dbo.tblUserSamplexMovie uxs
GROUP BY uxs.Lift;

UPDATE dbo.#StayPositive
SET TPR = TruePositive / (TruePositive + FalseNegative)
  , FPR = FalsePositive / (FalsePositive + TrueNegative)
WHERE (TruePositive + FalseNegative) > 0
      AND (FalsePositive + TrueNegative) > 0;
SELECT *
FROM dbo.#StayPositive;

DROP TABLE dbo.#MovieTruth;
DROP TABLE dbo.#TensorRecommends;
DROP TABLE dbo.#AlreadySeen;
DROP TABLE dbo.#StayPositive;


