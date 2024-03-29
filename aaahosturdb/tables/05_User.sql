DROP TABLE IF EXISTS User;
CREATE TABLE User (
    ID_USER INT NOT NULL AUTO_INCREMENT,
    Passwd VARCHAR(512) NOT NULL,
    Email VARCHAR(512) NOT NULL UNIQUE,
    Id_Role INT NOT NULL,
    PRIMARY KEY (ID_USER),
    FOREIGN KEY (Id_Role) REFERENCES Role(ID_ROLE)
);