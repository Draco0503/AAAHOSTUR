DROP TABLE IF EXISTS Language;
CREATE TABLE Language(
    ID_LANGUAGE INT  NOT NULL AUTO_INCREMENT,
    Name VARCHAR(512) NOT NULL,
    PRIMARY KEY (ID_LANGUAGE)
);

INSERT INTO Language (Name) 
    VALUES('Español');

INSERT INTO Language (Name) 
    VALUES('Italiano');

INSERT INTO Language (Name) 
    VALUES('Francés');

INSERT INTO Language (Name) 
    VALUES('Alemán');

INSERT INTO Language (Name) 
    VALUES('Inglés');