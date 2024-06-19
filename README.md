## DATABASE SCHEMA FOR FLASKAPP

#### Customers                  
| KEY              | COLUMN NAME         | TYPE         |                     
| :------------    | :-------------------| :----------- |
| PRIMARY_KEY      | Customer_ID         | VARCHAR(32)  |
|                  | Name                | VARCHAR(32)  |
|                  | Age                 | TINYINT      |
|                  | Bill                | INT          |

#### Vehicles
| KEY                   | COLUMN NAME         | TYPE         |
|:------------          |:--------------------|:------------ |
| PRIMARY_KEY           | Reg_num             | VARCHAR(32)  |
|FOREIGN_KEY (Customers)| Owner_ID            | VARCHAR(32)  |
|                       | Model_name          | VARCHAR(32)  |
|                       | Color               | VARCHAR(32)  |
|                       | V_Type              | VARCHAR (32) |   
|                       | Entry_time          | DATETIME     |