DROP datatable IF EXISTS Academic_Profile;
CREATE TABLE Academic_Profile (
    ID_ACADEMIC_PROFILE INT NOT NULL AUTO_INCREMENT,
    School VARCHAR(512) NOT NULL,
    Graduation_Date VARCHAR(256) NOT NULL,
    Promotion VARCHAR(256),
    Id_Member INT NOT NULL,
    Id_Qualification INT NOT NULL,
    PRIMARY KEY (ID_ACADEMIC_PROFILE),
    FOREIGN KEY (Id_Member) REFERENCES Member(ID_MEMBER),
    FOREIGN KEY (Id_Qualification) REFERENCES Qualification(ID_QUALIFICATION)
);