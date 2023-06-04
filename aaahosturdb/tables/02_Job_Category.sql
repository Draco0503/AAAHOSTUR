DROP TABLE IF EXISTS Job_Category;
CREATE TABLE Job_Category(
ID_JOB_CATEGORY INT NOT NULL AUTO_INCREMENT,
Name VARCHAR(512) NOT NULL,
Description VARCHAR(512) NOT NULL,
PRIMARY KEY (ID_JOB_CATEGORY)
);

INSERT INTO Job_Category (Name, Description) 
    VALUES('Cocina', 
    '*under maintenance*');
INSERT INTO Job_Category (Name, Description) 
    VALUES('Turismo', 
    '*under maintenance*');
INSERT INTO Job_Category (Name, Description) 
    VALUES('Servicios', 
    '*under maintenance*');
INSERT INTO Job_Category (Name, Description) 
    VALUES('Docencia', 
    '*under maintenance*');