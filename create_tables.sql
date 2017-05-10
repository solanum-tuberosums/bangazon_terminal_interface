------------------------------------------------------------------------
--- Only use these commands once you run the CREATE TABLE statements ---
------------------------------------------------------------------------
DROP TABLE IF EXISTS ProductOrder;
DROP TABLE IF EXISTS CustomerOrder;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS PaymentType;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS ProductType;
------------------------------------------------------------------------


-- Department Table
CREATE TABLE Department(
    id                              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name                            VARCHAR(30),
    budget                          REAL CHECK (budget > 0) NOT NULL);

-- Customer Table
CREATE TABLE Customer(
    id                              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    first_name                      VARCHAR(20) NOT NULL,
    middle_name                     VARCHAR(20),
    last_name                       VARCHAR(30) NOT NULL,
    street_address                  VARCHAR(40),
    city                            VARCHAR(20),
    home_state                      CHAR(2),
    postal_code                     CHAR(5),
    phone_number                    VARCHAR(15),
    date_created                    DATE NOT NULL);

-- PaymentType Table
CREATE TABLE PaymentType(
    id                              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    account_label                   VARCHAR(20),
    account_type                    VARCHAR(20),
    account_number                  VARCHAR(20) NOT NULL,
    customer_id                     INTEGER NOT NULL,
    FOREIGN KEY (customer_id)       REFERENCES Customer(id) ON DELETE CASCADE);

-- ProductType Table
CREATE TABLE ProductType(
    id                               INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    label                            VARCHAR(20));

-- Product Table
CREATE TABLE Product(
    id                              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    price                           REAL NOT NULL,
    title                           VARCHAR(20) NOT NULL,
    description                     VARCHAR(20),
    product_type_id                 INTEGER NOT NULL,
    customer_id                     INTEGER NOT NULL,
    FOREIGN KEY (product_type_id)   REFERENCES ProductType(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id)       REFERENCES Customer(id) ON DELETE CASCADE);

-- CustomerOrder Table (formerly known as 'Order')
CREATE TABLE CustomerOrder(
    id                              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    payment_type_id                 INTEGER,
    date_begun                      DATE NOT NULL,
    customer_id                     INTEGER NOT NULL,
    date_paid                       DATE CHECK(date_begun < date_paid),
    FOREIGN KEY (customer_id)       REFERENCES Customer(id) ON DELETE CASCADE);

-- ProductOrder Table
CREATE TABLE ProductOrder(
    id                              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    product_id                      INTEGER NOT NULL,
    order_id                        INTEGER NOT NULL,
    FOREIGN KEY (product_id)        REFERENCES Product(id) ON DELETE CASCADE,
    FOREIGN KEY (order_id)          REFERENCES CustomerOrder(id) ON DELETE CASCADE);


--INSERT Statements to Create Dummy Products for Testing
INSERT INTO Customer Values(NULL, 'Jeremy', 'Will', 'Smith', '500 Interstate Blvd S.', 'Nashville', 'TN', '37201', '615-888-5555', '05-09-2017');
INSERT INTO Customer Values(NULL, 'Blaise', 'Zak', 'Williams', '500 Interstate Blvd S.', 'Nashville', 'TN', '37201', '615-888-5555', '05-09-2017');
INSERT INTO Customer Values(NULL, 'Jessica', 'Z.', 'Michaels', '500 Interstate Blvd S.', 'Nashville', 'TN', '37201', '615-888-5555', '05-09-2017');
INSERT INTO ProductType Values(NULL, 'Round Toys');
INSERT INTO ProductType Values(NULL, 'Angular Toys');
INSERT INTO Product VALUES (NULL, 19.99, "Red Ball", "Bouncy", 1, 1);
INSERT INTO Product VALUES (NULL, 19.99, "Red Ball", "Bouncy", 1, 2);
INSERT INTO Product VALUES (NULL, 19.99, "Red Ball", "Bouncy", 1, 3);
INSERT INTO Product VALUES (NULL, 15.99, "Green Ball", "Squishy", 1, 1);
INSERT INTO Product VALUES (NULL, 15.99, "Green Ball", "Squishy", 1, 2);
INSERT INTO Product VALUES (NULL, 15.99, "Green Ball", "Squishy", 1, 3);
INSERT INTO Product VALUES (NULL, 15.99, "Green Ball", "Squishy", 1, 1);
INSERT INTO Product VALUES (NULL, 5.99, "Blocks", "Hard", 2, 1);
INSERT INTO Product VALUES (NULL, 5.99, "Blocks", "Hard", 2, 1);
INSERT INTO Product VALUES (NULL, 5.99, "Blocks", "Hard", 2, 1);