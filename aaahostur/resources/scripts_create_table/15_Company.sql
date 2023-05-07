DROP TABLE IF EXISTS Company;
CREATE TABLE Company(
    ID_COMPANY INT NOT NULL,
    Range VARCHAR(512) NOT NULL,
    CIF VARCHAR(512) NOT NULL UNIQUE,
    Address VARCHAR(512),
    CP VARCHAR(512),
    City VARCHAR(512),
    Province VARCHAR(512),
    Contact_Name VARCHAR(512) NOT NULL,
    Contact_Phone VARCHAR(512) NOT NULL,
    Contact_Email VARCHAR(512) NOT NULL,
    Description VARCHAR(512),
    Verify BOOLEAN DEFAULT FALSE,
    Active BOOLEAN DEFAULT TRUE,
    Id_Company_Parent INT,
    Id_User_Verify INT,
    PRIMARY KEY (ID_COMPANY),
    FOREIGN KEY (ID_COMPANY) REFERENCES User(ID_USER),
    FOREIGN KEY (Id_Company_Parent) REFERENCES Company(ID_COMPANY),
    FOREIGN KEY (Id_User_Verify) REFERENCES User(ID_USER)
);