DROP TABLE IF EXISTS Company_Account;
CREATE TABLE Company_Account(
    ID_COMPANY_ACCOUNT INT NOT NULL AUTO_INCREMENT,
    Account_Holder VARCHAR(512) NOT NULL,
    Account_Number VARCHAR(256) NOT NULL,
    SEPA BOOLEAN DEFAULT FALSE NOT NULL,
    Active BOOLEAN DEFAULT TRUE,
    Id_Company INT,
    PRIMARY KEY (ID_ACCOUNT),
    FOREIGN KEY (Id_Company_Holder) REFERENCES Company(ID_COMPANY)
);