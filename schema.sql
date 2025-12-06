-- Use your database
USE MerchantOfVenice;
GO

-- Table 1: Customers
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    country VARCHAR(50),
    first_purchase_date DATETIME,
    last_purchase_date DATETIME,
    total_orders INT DEFAULT 0,
    total_spent DECIMAL(10,2) DEFAULT 0
);

-- Table 2: Products
CREATE TABLE products (
    stock_code VARCHAR(20) PRIMARY KEY,
    description VARCHAR(300),
    unit_price DECIMAL(10,2)
);

-- Table 3: Transactions (Raw data)
CREATE TABLE transactions (
    transaction_id INT IDENTITY(1,1) PRIMARY KEY,
    invoice_no VARCHAR(20),
    stock_code VARCHAR(20),
    description VARCHAR(300),
    quantity INT,
    invoice_date DATETIME,
    unit_price DECIMAL(10,2),
    customer_id INT,
    country VARCHAR(50),
    line_total AS (quantity * unit_price) PERSISTED,
    UNIQUE(invoice_no, stock_code, customer_id) -- added multi column constraint to prevent duplicating
);
