CREATE VIEW dbo.vPrecedent
AS
SELECT m.MovieID
     , m.Title
     , axp.RuleAsssociationxRulePrecedentID
     , ra.RuleAsssociationID
     , rpa.RulePrecedentID
     , rpa.RulePrecedent
FROM dbo.tblMovie m
    INNER JOIN dbo.tblRuleAsssociationxRulePrecedent AS axp
        ON axp.MovieFK = m.MovieID
    INNER JOIN dbo.tblRuleAsssociation AS ra
        ON ra.RuleAsssociationID = axp.RuleAsssociationFK
    INNER JOIN dbo.tblRulePrecedent AS rpa
        ON rpa.RulePrecedentID = axp.RulePrecedentFK 
--WHERE rpa.RulePrecedentID = @RPID