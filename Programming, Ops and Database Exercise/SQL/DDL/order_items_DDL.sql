DROP TABLE IF EXISTS greyshop.order_items;

-- create order_items table --
CREATE TABLE greyshop.order_items ( 
order_item_id INT PRIMARY KEY, 
order_id INT, 
product_id INT, 
quantity INT, 
unit_price DECIMAL(10,2), 
FOREIGN KEY (order_id) REFERENCES orders(order_id), 
FOREIGN KEY (product_id) REFERENCES products(product_id) 
);