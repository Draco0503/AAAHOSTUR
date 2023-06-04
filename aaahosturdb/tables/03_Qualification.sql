DROP TABLE IF EXISTS Qualification;
CREATE TABLE Qualification(
ID_QUALIFICATION INT NOT NULL AUTO_INCREMENT,
Name VARCHAR(512) NOT NULL,
Description VARCHAR(512) NOT NULL,
Id_Qualification_Parent INT,
Id_Job_Category INT,
PRIMARY KEY (ID_QUALIFICATION),
FOREIGN KEY (Id_Qualification_Parent) REFERENCES Qualification(ID_QUALIFICATION),
FOREIGN KEY (Id_Job_Category) REFERENCES Job_Category(ID_JOB_CATEGORY)
);

INSERT INTO Qualification (Name, Description, Id_Job_Category) 
    VALUES('Técnico en Cocina y Gastronomía', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Cocina'));

INSERT INTO Qualification (Name, Description, Id_Job_Category) 
    VALUES('Técnico en Comercialización de Productos Alimentarios', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name= 'Cocina'));

INSERT INTO Qualification (Name, Description, Id_Job_Category) 
    VALUES('Título Profesional Básico en Actividades de Panadería y Pastelería', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Cocina'));

INSERT INTO Qualification (Name, Description, Id_Job_Category) 
    VALUES('Técnico Superior en Dirección de Cocina', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Cocina'));

INSERT INTO Qualification (Name, Description, Id_Job_Category) 
    VALUES('Curso de Especialización en Panadería y Bollería Artesanales (Acceso GM)', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Cocina'));


INSERT INTO Qualification (Name, Description, Id_Job_Category) 
    VALUES('Técnico Superior en Agencias de Viajes y Gestión de Eventos', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Turismo'));
INSERT INTO Qualification (Name, Description, Id_Job_Category) 
    VALUES('Técnico Superior en Gestión de Alojamientos Turísticos', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Turismo'));
INSERT INTO Qualification (Name, Description, Id_Job_Category) 
    VALUES('Técnico Superior en Guía, Información y Asistencias Turísticas', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Turismo'));


INSERT INTO Qualification (Name, Description, Id_Job_Category) 
    VALUES('Técnico en Servicios en Restauración', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Servicios'));
    
INSERT INTO Qualification (Name, Description, Id_Job_Category) 
    VALUES('Título Profesional Básico en Alojamiento y Lavandería', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Servicios'));

INSERT INTO Qualification (Name, Description, Id_Job_Category) 
    VALUES('Técnico Superior en Dirección de Servicios de Restauración', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Servicios'));