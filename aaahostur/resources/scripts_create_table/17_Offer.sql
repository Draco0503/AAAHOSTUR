DROP TABLE IF EXISTS Offer;
CREATE TABLE Offer(
    ID_OFFER INT NOT NULL AUTO_INCREMENT,
    Company_Name VARCHAR(512) NOT NULL,
    Address VARCHAR(512) NOT NULL,
    Contact_Name VARCHAR(512) NOT NULL,
    Contact_Phone VARCHAR(512) NOT NULL,
    Contact_Email VARCHAR(512) NOT NULL,
    Contact_Name_2 VARCHAR(512),
    Contact_Phone_2 VARCHAR(512),
    Contact_Email_2 VARCHAR(512),
    Verify BOOLEAN DEFAULT FALSE,
    Active BOOLEAN DEFAULT TRUE,
    Id_Company INT,
    Id_User_Verify INT,
    PRIMARY KEY (ID_OFFER),
    FOREIGN KEY (Id_Company) REFERENCES Company(ID_COMPANY),
    FOREIGN KEY (Id_User_Verify) REFERENCES User(ID_USER)
);