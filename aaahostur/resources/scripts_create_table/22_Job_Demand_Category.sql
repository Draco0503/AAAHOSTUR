DROP TABLE IF EXISTS Job_Demand_Category;
CREATE TABLE Job_Demand_Category(
    ID_JOB_DEMAND_CATEGORY INT NOT NULL AUTO_INCREMENT,
    Id_Category INT,
    Id_Job_Demand INT,
    PRIMARY KEY (ID_JOB_DEMAND_CATEGORY),
    FOREIGN KEY (Id_Category) REFERENCES Category(ID_CATEGORY),
    FOREIGN KEY (Id_Job_Demand) REFERENCES Job_Demand(ID_JOB_DEMAND)
);