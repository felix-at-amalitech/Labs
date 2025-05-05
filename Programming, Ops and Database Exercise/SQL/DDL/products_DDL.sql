DROP TABLE IF EXISTS greyshop.products;

-- create products table --
CREATE TABLE greyshop.products ( 
product_id INT PRIMARY KEY, 
name VARCHAR(100) NOT NULL, 
category VARCHAR(50), 
price DECIMAL(10,2) 
);