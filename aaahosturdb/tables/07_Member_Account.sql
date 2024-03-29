DROP TABLE IF EXISTS Member_Account;
CREATE TABLE Member_Account (
    ID_MEMBER_ACCOUNT INT NOT NULL AUTO_INCREMENT,
    Account_Holder VARCHAR(512),
    Account_Number VARCHAR(512) UNIQUE,
    SEPA_Form BOOLEAN DEFAULT FALSE,
    Active BOOLEAN DEFAULT TRUE,
    Id_Member INT NOT NULL UNIQUE,
    Id_User_Verify INT,
    PRIMARY KEY (ID_MEMBER_ACCOUNT),
    FOREIGN KEY (Id_Member) REFERENCES Member(ID_MEMBER),
    FOREIGN KEY (Id_User_Verify) REFERENCES User(ID_USER)
);