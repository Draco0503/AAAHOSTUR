DROP TABLE IF EXISTS Job_Demand_Language;
CREATE TABLE Job_Demand_Language(
    ID_JOB_DEMAND_LANGUAGE INT NOT NULL AUTO_INCREMENT,
    Id_Language INT,
    Id_Job_Demand INT,
    PRIMARY KEY (ID_JOB_DEMAND_LANGUAGE),
    FOREIGN KEY (Id_Language) REFERENCES Language(ID_LANGUAGE),
    FOREIGN KEY (Id_Job_Demand) REFERENCES Job_Demand(ID_JOB_DEMAND)
);