USE flaskapp;

CREATE TABLE Customers (
    Customer_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(32) NOT NULL,
    Age TINYINT NOT NULL,
    Bill_Amount INT
);

CREATE TABLE Vehicles (
    Vehicle_ID INT AUTO_INCREMENT PRIMARY KEY,
    Reg_Num varchar(32) NOT NULL, 
    Model_name varchar(32),
    Color varchar(32), 
    V_Type varchar(32) CHECK (V_Type in ('LMV', 'MCWG', 'HMV')),
    Entry_time DATETIME NOT NULL,
    Customer_ID INT,
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID)
);

ALTER TABLE Customers AUTO_INCREMENT = 1;
ALTER TABLE Vehicles AUTO_INCREMENT = 1;