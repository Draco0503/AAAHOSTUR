DROP TABLE IF EXISTS Job_Demand_Qualification;
CREATE TABLE Job_Demand_Qualification(
    ID_JOB_DEMAND_QUALIFICATION INT NOT NULL AUTO_INCREMENT,
    Id_Qualification INT,
    Id_Job_Demand INT,
    PRIMARY KEY (ID_JOB_DEMAND_QUALIFICATION),
    FOREIGN KEY (Id_Qualification) REFERENCES Qualification(ID_QUALIFICATION),
    FOREIGN KEY (Id_Job_Demand) REFERENCES Job_Demand(ID_JOB_DEMAND)
);