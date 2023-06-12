-- LAGUAGE INSERTS
INSERT ignore INTO Language (ID_LANGUAGE, Name) 
    VALUES(1, 'Español');

INSERT ignore INTO Language (ID_LANGUAGE, Name) 
    VALUES(2, 'Italiano');

INSERT ignore INTO Language (ID_LANGUAGE, Name) 
    VALUES(3, 'Francés');

INSERT ignore INTO Language (ID_LANGUAGE, Name) 
    VALUES(4, 'Alemán');

INSERT ignore INTO Language (ID_LANGUAGE, Name) 
    VALUES(5, 'Inglés');

-- JOB CATEGORY
INSERT ignore INTO Job_Category (ID_JOB_CATEGORY, Name, Description) 
    VALUES(1, 'Cocina', 
    '*under maintenance*');
INSERT ignore INTO Job_Category (ID_JOB_CATEGORY, Name, Description) 
    VALUES(2, 'Turismo', 
    '*under maintenance*');
INSERT ignore INTO Job_Category (ID_JOB_CATEGORY, Name, Description) 
    VALUES(3, 'Servicios', 
    '*under maintenance*');
INSERT ignore INTO Job_Category (ID_JOB_CATEGORY, Name, Description) 
    VALUES(4, 'Docencia', 
    '*under maintenance*');

-- QUALIFICATION
INSERT ignore INTO Qualification (ID_QUALIFICATION, Name, Description, Id_Job_Category) 
    VALUES(1, 'Técnico en Cocina y Gastronomía', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Cocina'));
INSERT ignore INTO Qualification (ID_QUALIFICATION, Name, Description, Id_Job_Category) 
    VALUES(2, 'Técnico en Comercialización de Productos Alimentarios', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name= 'Cocina'));
INSERT ignore INTO Qualification (ID_QUALIFICATION, Name, Description, Id_Job_Category) 
    VALUES(3, 'Título Profesional Básico en Actividades de Panadería y Pastelería', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Cocina'));
INSERT ignore INTO Qualification (ID_QUALIFICATION, Name, Description, Id_Job_Category) 
    VALUES(4, 'Técnico Superior en Dirección de Cocina', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Cocina'));
INSERT ignore INTO Qualification (ID_QUALIFICATION, Name, Description, Id_Job_Category) 
    VALUES(5, 'Curso de Especialización en Panadería y Bollería Artesanales (Acceso GM)', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Cocina'));
INSERT ignore INTO Qualification (ID_QUALIFICATION, Name, Description, Id_Job_Category) 
    VALUES(6, 'Técnico Superior en Agencias de Viajes y Gestión de Eventos', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Turismo'));
INSERT ignore INTO Qualification (ID_QUALIFICATION, Name, Description, Id_Job_Category) 
    VALUES(7, 'Técnico Superior en Gestión de Alojamientos Turísticos', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Turismo'));
INSERT ignore INTO Qualification (ID_QUALIFICATION, Name, Description, Id_Job_Category) 
    VALUES(8, 'Técnico Superior en Guía, Información y Asistencias Turísticas', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Turismo'));
INSERT ignore INTO Qualification (ID_QUALIFICATION, Name, Description, Id_Job_Category) 
    VALUES(9, 'Técnico en Servicios en Restauración', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Servicios'));
INSERT ignore INTO Qualification (ID_QUALIFICATION, Name, Description, Id_Job_Category) 
    VALUES(10, 'Título Profesional Básico en Alojamiento y Lavandería', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Servicios'));
INSERT ignore INTO Qualification (ID_QUALIFICATION, Name, Description, Id_Job_Category) 
    VALUES(11, 'Técnico Superior en Dirección de Servicios de Restauración', 
    '*under maintenance*', 
    (SELECT ID_JOB_CATEGORY FROM Job_Category WHERE Name='Servicios'));

-- ROLE
INSERT IGNORE INTO Role(ID_ROLE, Name, Description, CanVerifyMember,
                 CanVerifyCompany, CanVerifyAdmin, CanVerifyOffer,
                 CanVerifyReview, CanSeeOffer, CanApplyOffer,
                 CanMakeOffer, CanSeeSection, CanMakeSection,
                 CanActiveMember, CanActiveCompany, CanActiveSection,
                 CanActiveOffer, CanActiveReview, CanActiveCompanyBankAcc,
                 CanActiveMemberBankAcc, CanSeeReview, CanMakeReview,
                 CanSeeApiRole, CanSeeApiLanguage, CanSeeApiJobCategory,
                 CanSeeApiQualification, CanSeeApiUser, CanSeeApiSection,
                 CanSeeApiCompany, CanSeeApiMember, CanSeeApiOffer,
                 CanSeeApiReview, IsAAAHOSTUR, IsMember, IsCompany)
         VALUES(101, "SUPERADMIN", "The highest role",
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0);
INSERT IGNORE INTO Role(ID_ROLE, Name, Description, CanVerifyMember,
                 CanVerifyCompany, CanVerifyAdmin, CanVerifyOffer,
                 CanVerifyReview, CanSeeOffer, CanApplyOffer,
                 CanMakeOffer, CanSeeSection, CanMakeSection,
                 CanActiveMember, CanActiveCompany, CanActiveSection,
                 CanActiveOffer, CanActiveReview, CanActiveCompanyBankAcc,
                 CanActiveMemberBankAcc, CanSeeReview, CanMakeReview,
                 CanSeeApiRole, CanSeeApiLanguage, CanSeeApiJobCategory,
                 CanSeeApiQualification, CanSeeApiUser, CanSeeApiSection,
                 CanSeeApiCompany, CanSeeApiMember, CanSeeApiOffer,
                 CanSeeApiReview, IsAAAHOSTUR, IsMember, IsCompany)
          VALUES(102, "ADMIN", "The manager",
          1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0);
INSERT IGNORE INTO Role(ID_ROLE, Name, Description, CanVerifyMember,
                 CanVerifyCompany, CanVerifyAdmin, CanVerifyOffer,
                 CanVerifyReview, CanSeeOffer, CanApplyOffer,
                 CanMakeOffer, CanSeeSection, CanMakeSection,
                 CanActiveMember, CanActiveCompany, CanActiveSection,
                 CanActiveOffer, CanActiveReview, CanActiveCompanyBankAcc,
                 CanActiveMemberBankAcc, CanSeeReview, CanMakeReview,
                 CanSeeApiRole, CanSeeApiLanguage, CanSeeApiJobCategory,
                 CanSeeApiQualification, CanSeeApiUser, CanSeeApiSection,
                 CanSeeApiCompany, CanSeeApiMember, CanSeeApiOffer,
                 CanSeeApiReview, IsAAAHOSTUR, IsMember, IsCompany)
          VALUES(103, "PUBLISHER", "To manage sections",
          0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0,
          0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0);
INSERT IGNORE INTO Role(ID_ROLE, Name, Description, CanVerifyMember,
                 CanVerifyCompany, CanVerifyAdmin, CanVerifyOffer,
                 CanVerifyReview, CanSeeOffer, CanApplyOffer,
                 CanMakeOffer, CanSeeSection, CanMakeSection,
                 CanActiveMember, CanActiveCompany, CanActiveSection,
                 CanActiveOffer, CanActiveReview, CanActiveCompanyBankAcc,
                 CanActiveMemberBankAcc, CanSeeReview, CanMakeReview,
                 CanSeeApiRole, CanSeeApiLanguage, CanSeeApiJobCategory,
                 CanSeeApiQualification, CanSeeApiUser, CanSeeApiSection,
                 CanSeeApiCompany, CanSeeApiMember, CanSeeApiOffer,
                 CanSeeApiReview, IsAAAHOSTUR, IsMember, IsCompany)
          VALUES(104, "MEMBER", "Member can apply to offers",
          0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
          0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0);
INSERT IGNORE INTO Role(ID_ROLE, Name, Description, CanVerifyMember,
                 CanVerifyCompany, CanVerifyAdmin, CanVerifyOffer,
                 CanVerifyReview, CanSeeOffer, CanApplyOffer,
                 CanMakeOffer, CanSeeSection, CanMakeSection,
                 CanActiveMember, CanActiveCompany, CanActiveSection,
                 CanActiveOffer, CanActiveReview, CanActiveCompanyBankAcc,
                 CanActiveMemberBankAcc, CanSeeReview, CanMakeReview,
                 CanSeeApiRole, CanSeeApiLanguage, CanSeeApiJobCategory,
                 CanSeeApiQualification, CanSeeApiUser, CanSeeApiSection,
                 CanSeeApiCompany, CanSeeApiMember, CanSeeApiOffer,
                 CanSeeApiReview, IsAAAHOSTUR, IsMember, IsCompany)
          VALUES(105, "COMPANY", "Companies can make offers",
          0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
          0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1);

-- USERS (SUPERADM, ADM, PUBLISHER, MEMBER & COMPANY)
insert ignore into `User` (`Email`, `ID_USER`, `Id_Role`, `Passwd`) 
	values ('aaahostur@aaahostur.es', '88f430eb-ffa1-11ed-acd2-2cf05d6ddc4a', 101, '$2b$12$/bR0pON1bQs5ieKEojVCKur0JBcXsj4krgmAWLd8qJQkuNKV2y3cC');
  
insert ignore into `User` (`Email`, `ID_USER`, `Id_Role`, `Passwd`) 
	values ('admin@aaahostur.es', '3ff878e1-0601-11ee-acd2-2cf05d6ddc4a', 102, '$2b$12$/bR0pON1bQs5ieKEojVCKur0JBcXsj4krgmAWLd8qJQkuNKV2y3cC');

insert ignore into `User` (`Email`, `ID_USER`, `Id_Role`, `Passwd`) 
	values ('publisher@aaahostur.es', 'b54b27b9-0601-11ee-acd2-2cf05d6ddc4a', 103, '$2b$12$/bR0pON1bQs5ieKEojVCKur0JBcXsj4krgmAWLd8qJQkuNKV2y3cC');
  
insert ignore into `User` (`Email`, `ID_USER`, `Id_Role`, `Passwd`) 
	values ('alejandro@gmail.com', '45c30679-0602-11ee-acd2-2cf05d6ddc4a', 104, '$2b$12$/bR0pON1bQs5ieKEojVCKur0JBcXsj4krgmAWLd8qJQkuNKV2y3cC');

insert ignore into `Member` (`Active`, `Address`, `Birth_Date`, `CP`, 
                             `Cancellation_Date`, `City`, `DNI`, `Disability_Grade`, 
                             `Gender`, `Geographical_Mobility`, `ID_MEMBER`, `Id_User_Verify`, 
                             `Join_Date`, `Land_Line`, `Mobile`, `Name`, 
                             `PNA_Address`, `PNA_CP`, `PNA_City`, `PNA_Province`, 
                             `Profile_Picture`, `Province`, `Surname`, `Vehicle`, `Verify`) 
	values (1, 'Calle de la Piruleta', '2001-01-05', '28047', 
          '', 'Madrid', '12345678D', 0, 
          'H', 1, '45c30679-0602-11ee-acd2-2cf05d6ddc4a', NULL, 
          '23-05-30 13:20:37', '', '600112233', 'Alejandro', 
          NULL, NULL, NULL, NULL, 
          NULL, 'Madrid', 'Esc Gar', 0, 0);

insert ignore into `User` (`Email`, `ID_USER`, `Id_Role`, `Passwd`) 
	values ('manolo@resmanolo.es', '4e0351af-0602-11ee-acd2-2cf05d6ddc4a', 105, '$2b$12$/bR0pON1bQs5ieKEojVCKur0JBcXsj4krgmAWLd8qJQkuNKV2y3cC');
  
insert ignore into `Company` (`Active`, `Address`, `CIF`, `CP`, 
                       `City`, `Contact_Email`, `Contact_Name`, `Contact_Phone`, 
                       `Description`, `ID_COMPANY`, `Id_Company_Parent`, `Id_User_Verify`, 
                       `Name`, `Province`, `Type`, `Verify`)
  values (1, 'Calle de la Piruleta Empresarial', '123456f', '12345',
          'Madrid', 'manolo@resmanolo.es', 'Manolo Perez', '666666660', 
          'Restaurante Manolo donde comes', '4e0351af-0602-11ee-acd2-2cf05d6ddc4a', NULL, NULL, 
          'Empresa', 'Madrid', 'National', 0);