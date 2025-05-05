
CREATE TABLE IF NOT EXISTS  greyshop.product_inventory (
product_id INT PRIMARY KEY NOT NULL,
quantity_sold INT NOT NULL,
quantity_available INT NOT NULL,
category VARCHAR(20) NOT NULL,
unit_price DECIMAL(10,2) NOT NULL
);