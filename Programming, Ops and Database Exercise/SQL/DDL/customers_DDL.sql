DROP TABLE IF EXISTS greyshop.customers;

-- create customers table -- 
CREATE TABLE greyshop.customers ( 
customer_id INT PRIMARY KEY, 
name VARCHAR(100) NOT NULL, 
email VARCHAR(100) UNIQUE NOT NULL, 
country VARCHAR(50) 
);