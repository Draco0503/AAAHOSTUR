DROP datatable IF EXISTS Job_Category;
CREATE TABLE Job_Category(
ID_JOB_CATEGORY INT AUTO INCREMENT NOT NULL,
Name VARCHAR(512) NOT NULL,
Description VARCHAR(512) NOT NULL,
PRIMARY KEY (ID_JOB_CATEGORY)
);