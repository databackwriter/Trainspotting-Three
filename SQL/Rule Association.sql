/*
DROP TABLE IF EXISTS dbo.tblRuleAsssociation;
GO

CREATE TABLE [dbo].[tblRuleAsssociation]
(
    RuleAsssociationID INT IDENTITY(1, 1) PRIMARY KEY NOT NULL
  , [antecedentsupport] [FLOAT] NULL
  , [consequentsupport] [FLOAT] NULL
  , [support] [FLOAT] NULL
  , [confidence] [FLOAT] NULL
  , [lift] [FLOAT] NULL
  , [leverage] [FLOAT] NULL
  , [conviction] [FLOAT] NULL
) ON [PRIMARY];
GO


DROP TABLE IF EXISTS dbo.tblRulePrecedent;
GO

CREATE TABLE dbo.tblRulePrecedent
(
    RulePrecedentID INT IDENTITY(1, 1) PRIMARY KEY NOT NULL
  , RulePrecedent VARCHAR(50)
);
GO
INSERT INTO dbo.tblRulePrecedent
(
    RulePrecedent
)
VALUES
('Antecedent')
, ('Consequent');


DROP PROCEDURE IF EXISTS dbo.usp_PM_RuleAsssociation_Insert;
GO
CREATE PROCEDURE dbo.usp_PM_RuleAsssociation_Insert
    @antecedentsupport FLOAT
  , @consequentsupport FLOAT
  , @support FLOAT
  , @confidence FLOAT
  , @lift FLOAT
  , @leverage FLOAT
  , @conviction FLOAT
AS
SET NOCOUNT ON;
BEGIN
    INSERT INTO dbo.tblRuleAsssociation
    (
        antecedentsupport
      , consequentsupport
      , support
      , confidence
      , lift
      , leverage
      , conviction
    )
    VALUES
    (@antecedentsupport, @consequentsupport, @support, @confidence, @lift, @leverage, @conviction);

    SELECT SCOPE_IDENTITY() AS LatestID;
END;
SET NOCOUNT OFF;


DROP TABLE IF EXISTS [tblRuleAsssociationxRulePrecedent]
GO
CREATE TABLE [dbo].[tblRuleAsssociationxRulePrecedent]
(
    RuleAsssociationxRulePrecedentID INT IDENTITY(1, 1)  NOT NULL	 ,
    RuleAsssociationFK INT NOT NULL,
    RulePrecedentFK INT NOT NULL,
    MovieFK INT NOT NULL,
    PRIMARY KEY( RuleAsssociationFK, RulePrecedentFK,MovieFK)
    )


--SET QUOTED_IDENTIFIER ON|OFF
--SET ANSI_NULLS ON|OFF
--GO
DROP PROCEDURE IF EXISTS dbo.usp_PM_RuleAsssociationxRulePrecedent_Insert;
GO
CREATE PROCEDURE dbo.usp_PM_RuleAsssociationxRulePrecedent_Insert
    @RuleAsssociationFK INT
  , @RulePrecedentFK INT
  , @MovieFK INT
AS
SET NOCOUNT ON;
BEGIN

    INSERT INTO dbo.tblRuleAsssociationxRulePrecedent
    (
        RuleAsssociationFK
      , RulePrecedentFK
      , MovieFK
    )
    VALUES
    (@RuleAsssociationFK, @RulePrecedentFK, @MovieFK);

END;
SET NOCOUNT OFF;