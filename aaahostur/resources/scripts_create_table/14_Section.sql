DROP datatable IF EXISTS Section;
CREATE TABLE Section (
    ID_SECTION INT NOT NULL AUTO_INCREMENT,
    Category ENUM("Actividad", "Curso", "Noticia"),
    Description VARCHAR(1024) NOT NULL,
    Publication_Date VARCHAR(256) NOT NULL,
    Schedule VARCHAR(256) NOT NULL,
    Img_Resource BLOB,
    Price VARCHAR(128),
    Active BOOLEAN DEFAULT TRUE,
    Id_User_Creator INT NOT NULL,
    PRIMARY KEY (ID_SECTION),
    FOREIGN KEY (Id_User_Creator) REFERENCES User(ID_USER)
);