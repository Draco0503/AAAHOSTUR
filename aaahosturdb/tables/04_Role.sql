DROP TABLE IF EXISTS Role;
CREATE TABLE Role (
    ID_ROLE INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(20) NOT NULL,
    Description VARCHAR(512),
    CanVerifyMember BOOLEAN DEFAULT FALSE,
    CanVerifyCompany BOOLEAN DEFAULT FALSE,
    CanVerifyAdmin BOOLEAN DEFAULT FALSE,
    CanVerifyOffer BOOLEAN DEFAULT FALSE,
    CanVerifyReview BOOLEAN DEFAULT FALSE,
    CanSeeOffer BOOLEAN DEFAULT FALSE,
    CanApplyOffer BOOLEAN DEFAULT FALSE,
    CanMakeOffer BOOLEAN DEFAULT FALSE,
    CanSeeSection BOOLEAN DEFAULT FALSE,
    CanMakeSection BOOLEAN DEFAULT FALSE,
    CanActiveMember BOOLEAN DEFAULT FALSE,
    CanActiveCompany BOOLEAN DEFAULT FALSE,
    CanActiveSection BOOLEAN DEFAULT FALSE,
    CanActiveOffer BOOLEAN DEFAULT FALSE,
    CanActiveReview BOOLEAN DEFAULT FALSE,
    CanActiveCompanyBankAcc BOOLEAN DEFAULT FALSE,
    CanActiveMemberBankAcc BOOLEAN DEFAULT FALSE,
    CanSeeReview BOOLEAN DEFAULT FALSE,
    CanMakeReview BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (ID_ROLE)
);

INSERT INTO Role VALUES(101, "SUPERADMIN", "The highest role", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);
INSERT INTO Role VALUES(102, "ADMIN", "The manager", 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);
INSERT INTO Role VALUES(103, "PUBLISHER", "To manage sections", 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0);
INSERT INTO Role VALUES(104, "MEMBER", "Member can apply to offers", 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1);
INSERT INTO Role VALUES(105, "COMPANY", "Companies can make offers", 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1);
-- INSERT INTO Role VALUES(106, "DEFAULT_USER", "Only watching", 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0);
