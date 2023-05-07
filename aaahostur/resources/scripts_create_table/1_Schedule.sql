DROP datatable IF EXISTS Schedule;
CREATE TABLE Schedule(
ID_SCHEDULE INT AUTO INCREMENT NOT NULL,
Name VARCHAR(512) NOT NULL,
Description VARCHAR(512) NOT NULL,
PRIMARY KEY (ID_SCHEDULE)
);                                                                                                           .