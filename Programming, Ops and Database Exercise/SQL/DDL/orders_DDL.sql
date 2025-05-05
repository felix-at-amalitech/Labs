DROP TABLE IF EXISTS greyshop.orders;

-- create orders table --
CREATE TABLE greyshop.orders ( 
order_id INT PRIMARY KEY, 
customer_id INT, 
order_date DATE, 
status VARCHAR(20), 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id) 
);