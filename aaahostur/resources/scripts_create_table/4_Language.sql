DROP TABLE IF EXISTS Language;
CREATE TABLE Language(
ID_LANGUAGE INT  NOT NULL AUTO_INCREMENT,
Name VARCHAR(512) NOT NULL,
Lvl VARCHAR(512) NOT NULL,
Certificate VARCHAR(512) NOT NULL,
PRIMARY KEY (ID_LANGUAGE)
);