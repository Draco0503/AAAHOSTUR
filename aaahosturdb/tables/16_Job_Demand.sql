DROP TABLE IF EXISTS Job_Demand;
CREATE TABLE Job_Demand(
    ID_JOB_DEMAND INT NOT NULL AUTO_INCREMENT,
    Vacancies INT NOT NULL,
    Monthly_Salary INT,
    Contract_Type VARCHAR(512),
    Schedule VARCHAR(512) NOT NULL,
    Working_Day VARCHAR(512) NOT NULL,
    Shift VARCHAR(512) NOT NULL,
    Holidays INT,
    Experience VARCHAR(512),
    Vehicle BOOLEAN DEFAULT FALSE,
    Geographical_Mobility BOOLEAN DEFAULT FALSE,
    Disability_Grade INT DEFAULT 0,
    Others VARCHAR(512),
    Id_Offer INT,
    PRIMARY KEY (ID_JOB_DEMAND),
    FOREIGN KEY (Id_Offer) REFERENCES Offer(ID_OFFER)
);